"""EXP-023 / W1.1 : inventaire de couverture (surface identifiée vs surface physique estimée) par rouleau.

Méthode fixée dans experiments/EXP-023/README.md. Usage :
    python -m vesres.coverage <metadata.min.json> <sortie.csv> <sortie.md> [results.json]

Les fonctions « pures » (pas, enveloppe, surface, ligne) ne font aucun accès réseau ; la lecture HTTP anonyme
(plans/blocs OME-Zarr v2 non compressés, requêtes `Range`) est isolée dans `Zarr` et mise en cache atomiquement
sous `<VESRES_WORK>/cache/coverage/`.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from scipy import ndimage

from vesres.paths import WORK

BASE = "https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/"
CACHE = WORK / "cache" / "coverage"
WORKERS = 8
ENV_LEVEL = 5            # enveloppe (niveau 5 : facteur 32)
BAND_LEVEL = 2           # bandes radiales (niveau 2 : facteur 4)
BAND_W = 128             # largeur de bande = 1 bloc
HEIGHT_FRACS = (0.25, 0.5, 0.75)
PITCH_LO, PITCH_HI = 80.0, 600.0
MIN_CORR = 0.15          # autocorrélation minimale du pic pour qu'une bande soit « valide »
MIN_BANDS = 6
MAX_ENV_VOXELS = 300e6   # plafond (budget réseau) sur le niveau 5 d'un volume candidat
MAX_PIXEL_UM = 10.0      # au-delà, un pas de 80 µm n'est plus échantillonné (Nyquist au niveau 2)
EXT_HI = 1500.0         # borne haute élargie, sensibilité uniquement (jamais utilisée pour le verdict)
MIN_RUN = 64             # longueur minimale (échantillons) du tronçon radial analysé

_bytes = {"n": 0}


# --------------------------------------------------------------------------- fonctions pures

def estimate_pitch(profile, px_um: float, lo: float = PITCH_LO, hi: float = PITCH_HI,
                   min_corr: float = MIN_CORR) -> float | None:
    """Pas (µm) = premier pic d'autocorrélation du profil sans tendance dans [lo, hi] µm ; None si absent."""
    p = np.asarray(profile, dtype=float)
    n = len(p)
    if n < 8 or px_um <= 0:
        return None
    w = int(min(n // 2 * 2 - 1, max(3, 2 * round(hi / px_um) + 1)))  # fenêtre impaire de retrait de tendance
    kernel = np.ones(w) / w
    padded = np.pad(p, w // 2, mode="reflect") if w // 2 < n else np.pad(p, w // 2, mode="edge")
    trend = np.convolve(padded, kernel, mode="valid")[:n]
    x = p - trend
    x = x - x.mean()
    var = float(np.dot(x, x))
    if var <= 1e-12:
        return None
    kmax = min(n - 4, int(np.ceil(hi / px_um)) + 1)
    ac = np.empty(kmax + 1)
    for k in range(kmax + 1):  # autocorrélation non biaisée, normalisée à 1 en 0
        ac[k] = np.dot(x[: n - k], x[k:]) / (n - k) / (var / n)
    k0 = max(1, int(np.floor(lo / px_um)))
    for k in range(max(k0, 1), kmax):
        if ac[k] > ac[k - 1] and ac[k] >= ac[k + 1] and ac[k] >= min_corr:
            a, b, c = ac[k - 1], ac[k], ac[k + 1]
            den = a - 2 * b + c
            off = 0.5 * (a - c) / den if den != 0 else 0.0
            pitch = (k + off) * px_um
            if lo <= pitch <= hi:
                return float(pitch)
    return None


def envelope_areas(vol) -> np.ndarray:
    """Aire (voxels) par tranche z de `vol > 0` après remplissage des trous."""
    return np.array([ndimage.binary_fill_holes(vol[z] > 0).sum() for z in range(vol.shape[0])], dtype=float)


def height_extent(areas) -> tuple[int, int]:
    nz = np.flatnonzero(np.asarray(areas) > 0)
    return (int(nz[0]), int(nz[-1])) if len(nz) else (0, -1)


def surface_cm2(areas_px, voxel_um: float, pitch_um: float) -> float:
    """Σ_z aire(z) / pas × Δz, en cm² (une face du feuillet) ; `voxel_um` = pas d'échantillonnage du niveau d'enveloppe."""
    area_um2 = float(np.sum(areas_px)) * voxel_um ** 2
    return area_um2 / pitch_um * voxel_um / 1e8


def percentiles(pitches) -> tuple[float, float, float]:
    a = np.asarray(pitches, dtype=float)
    return float(np.median(a)), float(np.percentile(a, 25)), float(np.percentile(a, 75))


def longest_run(valid) -> tuple[int, int]:
    best = (0, 0)
    i, n = 0, len(valid)
    while i < n:
        if valid[i]:
            j = i
            while j < n and valid[j]:
                j += 1
            if j - i > best[1] - best[0]:
                best = (i, j)
            i = j
        else:
            i += 1
    return best


def band_profile(patch: np.ndarray, min_frac: float = 0.5) -> np.ndarray | None:
    """Patch 2D (largeur de bande, axe radial) -> profil radial moyen (voxels non nuls) sur le plus long tronçon couvert."""
    nz = patch > 0
    frac = nz.mean(axis=0)
    a, b = longest_run(frac >= min_frac)
    if b - a < MIN_RUN:
        return None
    sub, m = patch[:, a:b].astype(float), nz[:, a:b]
    return (sub * m).sum(axis=0) / np.maximum(m.sum(axis=0), 1)


def inventory_row(rid: str, vol_id: str | None, pixel_um: float | None, n_seg: int, n_no_area: int,
                  n_fallback: int, ident_cm2: float, height_mm: float | None, pitches: list[float],
                  areas_px: np.ndarray | None, env_voxel_um: float | None, reason: str = "") -> dict:
    row = {"id": rid, "volume_utilise": vol_id or "", "pixel_um": pixel_um if pixel_um is not None else "",
           "n_segments": n_seg, "n_segments_sans_area": n_no_area, "n_segments_area_secours": n_fallback,
           "surface_identifiee_cm2": round(ident_cm2, 2),
           "hauteur_mm": round(height_mm, 2) if height_mm is not None else "",
           "pas_um_median": "", "pas_um_p25": "", "pas_um_p75": "", "n_bandes_valides": len(pitches),
           "surface_estimee_basse_cm2": "", "surface_estimee_mediane_cm2": "", "surface_estimee_haute_cm2": "",
           "ratio_bas": "", "ratio_median": "", "ratio_haut": "", "statut": "inconnue", "raison": reason}
    if pitches:
        med, p25, p75 = percentiles(pitches)
        row.update(pas_um_median=round(med, 1), pas_um_p25=round(p25, 1), pas_um_p75=round(p75, 1))
    if len(pitches) >= MIN_BANDS and areas_px is not None and env_voxel_um:
        low = surface_cm2(areas_px, env_voxel_um, p75)
        mid = surface_cm2(areas_px, env_voxel_um, med)
        high = surface_cm2(areas_px, env_voxel_um, p25)
        row.update(surface_estimee_basse_cm2=round(low, 1), surface_estimee_mediane_cm2=round(mid, 1),
                   surface_estimee_haute_cm2=round(high, 1),
                   ratio_bas=round(ident_cm2 / high, 3), ratio_median=round(ident_cm2 / mid, 3),
                   ratio_haut=round(ident_cm2 / low, 3), statut="estimée", raison="")
    elif not reason:
        row["raison"] = f"{len(pitches)} bandes valides < {MIN_BANDS}"
    return row


def verdict(rows: list[dict]) -> dict:
    """Règle H-028 du README sur les rouleaux `estimée`."""
    est = [r for r in rows if r["statut"] == "estimée"]
    n = len(est)
    n_sup = sum(r["ratio_haut"] < 0.5 for r in est)   # identifiée / estimée_basse < 0,5
    n_ref = sum(r["ratio_bas"] >= 0.5 for r in est)   # identifiée / estimée_haute >= 0,5
    v = "soutenue" if n_sup > n / 2 else "réfutée" if n_ref > n / 2 else "indéterminée"
    return {"n_estimes": n, "n_ratio_haut_lt_0.5": n_sup, "n_ratio_bas_ge_0.5": n_ref, "verdict": v}


# --------------------------------------------------------------------------- accès réseau / cache

def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def _http(url: str, rng: tuple[int, int] | None = None) -> bytes | None:
    import requests
    headers = {"Range": f"bytes={rng[0]}-{rng[1]}"} if rng else {}
    for attempt in range(4):
        try:
            r = requests.get(url, headers=headers, timeout=60)
            if r.status_code == 404:
                return None
            if r.status_code in (200, 206):
                data = r.content
                _bytes["n"] += len(data)
                if rng and r.status_code == 200:
                    data = data[rng[0]: rng[1] + 1]
                return data
        except requests.RequestException:
            pass
        time.sleep(1 + attempt)
    raise RuntimeError(f"échec HTTP {url}")


def cached_get(rel: str, key: str, rng: tuple[int, int] | None = None) -> bytes | None:
    """`rel` = chemin dans le bucket ; `key` = nom de cache. 404 mémorisé comme fichier vide."""
    p = CACHE / key
    if p.exists():
        d = p.read_bytes()
        return d if d else None
    d = _http(BASE + rel, rng)
    _atomic_write(p, d or b"")
    return d


def cached_json(rel: str, key: str) -> dict | None:
    d = cached_get(rel, key)
    return json.loads(d) if d else None


class Zarr:
    """Niveau d'un OME-Zarr v2 non compressé (blocs z/y/x, dimension_separator '/')."""

    def __init__(self, vol_path: str, level: int):
        self.path, self.level = vol_path.rstrip("/"), level
        self.tag = re.sub(r"[^A-Za-z0-9.-]", "_", self.path.replace("/volumes/", "_")) + f"/L{level}"
        za = cached_json(f"{self.path}/{level}/.zarray", f"{self.tag}/zarray.json")
        if za is None or za.get("compressor") or za.get("dtype") != "|u1" or za.get("dimension_separator") != "/":
            raise RuntimeError(f"format zarr non pris en charge : {self.path}/{level}")
        self.shape, self.chunks = tuple(za["shape"]), tuple(za["chunks"])

    def _chunk_url(self, c) -> str:
        return f"{self.path}/{self.level}/{c[0]}/{c[1]}/{c[2]}"

    def full(self) -> np.ndarray:
        """Volume entier (réservé au niveau d'enveloppe)."""
        cz, cy, cx = self.chunks
        grid = [-(-s // c) for s, c in zip(self.shape, self.chunks)]
        out = np.zeros(self.shape, np.uint8)
        coords = [(i, j, k) for i in range(grid[0]) for j in range(grid[1]) for k in range(grid[2])]

        def get(c):
            d = cached_get(self._chunk_url(c), f"{self.tag}/c{c[0]}_{c[1]}_{c[2]}.bin")
            return c, d

        with ThreadPoolExecutor(WORKERS) as ex:
            for c, d in ex.map(get, coords):
                if not d:
                    continue
                blk = np.frombuffer(d, np.uint8).reshape(self.chunks)
                z0, y0, x0 = c[0] * cz, c[1] * cy, c[2] * cx
                sub = blk[: self.shape[0] - z0, : self.shape[1] - y0, : self.shape[2] - x0]
                out[z0:z0 + sub.shape[0], y0:y0 + sub.shape[1], x0:x0 + sub.shape[2]] = sub
        return out

    def plane(self, z: int, y0: int, y1: int, x0: int, x1: int) -> np.ndarray:
        """Sous-rectangle [y0:y1, x0:x1] du plan z (requêtes Range d'un plan par bloc)."""
        cz, cy, cx = self.chunks
        zc, zi = divmod(z, cz)
        coords = [(j, k) for j in range(y0 // cy, (y1 - 1) // cy + 1) for k in range(x0 // cx, (x1 - 1) // cx + 1)]
        out = np.zeros((y1 - y0, x1 - x0), np.uint8)

        def get(jk):
            j, k = jk
            off = zi * cy * cx
            d = cached_get(self._chunk_url((zc, j, k)), f"{self.tag}/p{zc}_{j}_{k}_{zi}.bin", (off, off + cy * cx - 1))
            return jk, d

        with ThreadPoolExecutor(WORKERS) as ex:
            for (j, k), d in ex.map(get, coords):
                if not d or len(d) != cy * cx:
                    continue
                blk = np.frombuffer(d, np.uint8).reshape(cy, cx)
                ya, yb = max(y0, j * cy), min(y1, (j + 1) * cy)
                xa, xb = max(x0, k * cx), min(x1, (k + 1) * cx)
                out[ya - y0:yb - y0, xa - x0:xb - x0] = blk[ya - j * cy:yb - j * cy, xa - k * cx:xb - k * cx]
        return out


# --------------------------------------------------------------------------- catalogue -> rouleaux

def _seg_meta(path: str) -> dict | None:
    return cached_json(path.rstrip("/") + "/meta.json", "meta/" + re.sub(r"[^A-Za-z0-9.-]", "_", path) + ".json")


def segment_area(seg: dict, vol_id: str | None = None, pixel_um: float | None = None) -> tuple[float | None, bool]:
    """(area_cm2, secours?) : `area_cm2` de tifxyz_original ; à défaut `area_vx2` × pixel² du tifxyz-transformed sur `vol_id`."""
    by = {}
    for d in seg.get("data", []):
        if d.get("origins"):
            by.setdefault(d["type"], []).append(d["origins"][0]["path"])
    if "tifxyz" in by:
        m = _seg_meta(by["tifxyz"][0])
        if m and m.get("area_cm2") is not None:
            return float(m["area_cm2"]), False
    if vol_id and pixel_um:
        for path in by.get("tifxyz-transformed", []):
            if f"-on-{vol_id}" in path:
                m = _seg_meta(path)
                if m and m.get("area_vx2") is not None:
                    return float(m["area_vx2"]) * (pixel_um * 1e-4) ** 2, True
    return None, False


def masked_volumes(s: dict) -> list[dict]:
    out = []
    for vid, v in s.get("volumes", {}).items():
        for d in v.get("data", []):
            if d.get("type") == "ome-zarr":
                path = d["origins"][0]["path"].rstrip("/")
                out.append({"id": vid, "path": path, "pixel_um": v.get("properties", {}).get("pixel_size_um"),
                            "masked": path.endswith("-masked.zarr")})
    return out


def segments_per_volume(s: dict) -> dict[str, int]:
    cnt: dict[str, int] = {}
    for g in s.get("segments", {}).values():
        vids = set()
        for d in g.get("data", []):
            if d.get("type") == "tifxyz-transformed" and d.get("origins"):
                m = re.search(r"-on-(\d{14})", d["origins"][0]["path"])
                if m:
                    vids.add(m.group(1))
        for v in vids:
            cnt[v] = cnt.get(v, 0) + 1
    return cnt


def choose_volume(s: dict) -> tuple[dict | None, str]:
    vols = masked_volumes(s)
    if not vols:
        return None, "aucun volume OME-Zarr"
    masked = [v for v in vols if v["masked"]]
    if not masked:
        return None, "aucun volume masqué"
    cnt = segments_per_volume(s)
    ok = [v for v in masked if v["pixel_um"] and v["pixel_um"] <= MAX_PIXEL_UM]
    if not ok:
        return None, f"aucun volume masqué <= {MAX_PIXEL_UM} µm"
    ok.sort(key=lambda v: (-cnt.get(v["id"], 0), v["pixel_um"], v["id"]))
    for v in ok:
        try:
            z = Zarr(v["path"], ENV_LEVEL)
        except RuntimeError:
            continue
        if float(np.prod(z.shape)) <= MAX_ENV_VOXELS:
            return v, ""
    return None, f"niveau {ENV_LEVEL} > {MAX_ENV_VOXELS / 1e6:.0f} M voxels pour tous les volumes candidats"


def analyse_volume(vol: dict) -> dict:
    """Enveloppe (niveau 5) + pas par bandes (niveau 2). Résultat mis en cache JSON (déterministe)."""
    key = "results/" + re.sub(r"[^A-Za-z0-9.-]", "_", vol["path"]) + f".v2.json"
    p = CACHE / key
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    px = float(vol["pixel_um"])
    zenv = Zarr(vol["path"], ENV_LEVEL)
    arr = zenv.full()
    areas = envelope_areas(arr)
    z0, z1 = height_extent(areas)
    res = {"pixel_um": px, "env_voxel_um": px * 2 ** ENV_LEVEL, "areas_px": [int(a) for a in areas],
           "z_extent": [z0, z1], "pitches": [], "pitches_ext": [], "n_bands_tried": 0, "error": ""}
    if z1 >= z0:
        filled = np.stack([ndimage.binary_fill_holes(arr[z] > 0) for z in range(z0, z1 + 1)])
        cz_, cy_, cx_ = [float(v) for v in ndimage.center_of_mass(filled)]
        f = 2 ** (ENV_LEVEL - BAND_LEVEL)
        zb = Zarr(vol["path"], BAND_LEVEL)
        cy2, cx2 = int(round((cy_ + 0.5) * f)), int(round((cx_ + 0.5) * f))
        px_b = px * 2 ** BAND_LEVEL
        for hf in HEIGHT_FRACS:
            zs = z0 + int(round(hf * (z1 - z0)))
            z2 = min(zb.shape[0] - 1, int(zs * f + f // 2))
            ya, yb = max(0, cy2 - BAND_W // 2), min(zb.shape[1], cy2 + BAND_W // 2)
            xa, xb = max(0, cx2 - BAND_W // 2), min(zb.shape[2], cx2 + BAND_W // 2)
            for name, (y0, y1, x0, x1, axis, rev) in {
                "+x": (ya, yb, cx2, zb.shape[2], 1, False), "-x": (ya, yb, 0, cx2, 1, True),
                "+y": (cy2, zb.shape[1], xa, xb, 0, False), "-y": (0, cy2, xa, xb, 0, True)}.items():
                patch = zb.plane(z2, y0, y1, x0, x1)
                if axis == 0:
                    patch = patch.T
                if rev:
                    patch = patch[:, ::-1]
                res["n_bands_tried"] += 1
                prof = band_profile(patch)
                pitch = estimate_pitch(prof, px_b) if prof is not None else None
                if pitch is not None:
                    res["pitches"].append(round(pitch, 3))
                pe = estimate_pitch(prof, px_b, hi=EXT_HI) if prof is not None else None  # sensibilité hors verdict
                if pe is not None:
                    res["pitches_ext"].append(round(pe, 3))
    _atomic_write(p, json.dumps(res, sort_keys=True).encode("utf-8"))
    return res


def process_scroll(rid: str, s: dict) -> dict:
    segs = s.get("segments", {}) or {}
    areas, n_no, n_fb = [], 0, 0
    vol, why = choose_volume(s)
    for sid in sorted(segs):
        a, fb = segment_area(segs[sid], vol["id"] if vol else None, vol["pixel_um"] if vol else None)
        if a is None:
            n_no += 1
        else:
            areas.append(a)
            n_fb += fb
    ident = float(sum(areas))
    if vol is None:
        return inventory_row(rid, None, None, len(segs), n_no, n_fb, ident, None, [], None, None, why)
    try:
        r = analyse_volume(vol)
    except Exception as e:  # échec réseau/format : rouleau « inconnue », jamais d'arrêt global
        return inventory_row(rid, vol["id"], vol["pixel_um"], len(segs), n_no, n_fb, ident, None, [], None, None,
                             f"échec analyse : {type(e).__name__}")
    z0, z1 = r["z_extent"]
    h = (z1 - z0 + 1) * r["env_voxel_um"] / 1000 if z1 >= z0 else None
    row = inventory_row(rid, vol["id"], vol["pixel_um"], len(segs), n_no, n_fb, ident, h, r["pitches"],
                        np.array(r["areas_px"]), r["env_voxel_um"], "" if z1 >= z0 else "enveloppe vide")
    row["_ext_pitches"] = r.get("pitches_ext", [])
    return row


# --------------------------------------------------------------------------- sorties

COLS = ["id", "volume_utilise", "pixel_um", "n_segments", "n_segments_sans_area", "n_segments_area_secours",
        "surface_identifiee_cm2", "hauteur_mm", "pas_um_median", "pas_um_p25", "pas_um_p75", "n_bandes_valides",
        "surface_estimee_basse_cm2", "surface_estimee_mediane_cm2", "surface_estimee_haute_cm2",
        "ratio_bas", "ratio_median", "ratio_haut", "statut", "raison"]

MD_COLS = ["id", "volume_utilise", "pixel_um", "n_segments", "n_segments_sans_area", "surface_identifiee_cm2",
           "hauteur_mm", "pas_um_median", "n_bandes_valides", "statut"]


def write_outputs(rows: list[dict], csv_path: Path, md_path: Path, source_note: str) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    v = verdict(rows)
    v1 = verdict([r for r in rows if r["n_segments"] > 0])

    def interval(r):
        return (f"{r['surface_estimee_basse_cm2']}–{r['surface_estimee_haute_cm2']} (méd. {r['surface_estimee_mediane_cm2']})"
                if r["statut"] == "estimée" else "—")

    def ratio(r):
        return f"{r['ratio_bas']}–{r['ratio_haut']}" if r["statut"] == "estimée" else "—"

    lines = [
        "# Couverture par rouleau : surface identifiée vs surface physique estimée (généré, EXP-023 / W1.1)",
        "",
        source_note,
        "",
        "Méthode : `experiments/EXP-023/README.md` (`src/vesres/coverage.py`). Surface identifiée = somme des `area_cm2` des segments "
        "publiés (borne haute, chevauchements non dédupliqués) ; surface estimée = Σ_z aire(enveloppe) / pas × Δz (une face), "
        "intervalle [p75, p25] du pas. Le ratio n'a de sens qu'avec son intervalle [identifiée/estimée_haute – identifiée/estimée_basse].",
        "",
        f"Rouleaux : {len(rows)} ; estimés : {v['n_estimes']} ; H-028 (rouleaux estimés) : "
        f"{v['n_ratio_haut_lt_0.5']} avec ratio_haut < 0,5, {v['n_ratio_bas_ge_0.5']} avec ratio_bas ≥ 0,5 → **{v['verdict']}**. "
        f"Sous-ensemble avec ≥ 1 segment publié : {v1['n_estimes']} estimés, {v1['n_ratio_haut_lt_0.5']} / {v1['n_ratio_bas_ge_0.5']} → {v1['verdict']}.",
        "",
        "## Limites",
        "- Segments publiés ≠ tout le travail de segmentation existant (non publié, en cours).",
        "- Chevauchements non dédupliqués ; pas variable avec le rayon et la compression ; enveloppe incluant d'éventuels vides.",
        "- Estimation d'une seule face ; fragments détachés et morceaux externes non distingués ; fragments (type `fragment`) exclus.",
        f"- Écarts d'implémentation : quand `tifxyz_original` (ou son `area_cm2`) est absent, secours = `area_vx2` × pixel² du `tifxyz-transformed` "
        f"sur le volume utilisé (colonne `n_segments_area_secours` ; écart de ≈ 8 % mesuré sur PHerc0800 : 2,45 vs 2,28 cm²) ; volume limité aux masqués ≤ {MAX_PIXEL_UM:g} µm dont le niveau {ENV_LEVEL} ≤ "
        f"{MAX_ENV_VOXELS / 1e6:.0f} M voxels (budget réseau), le plus de segments d'abord ; bande valide = pic d'autocorrélation ≥ {MIN_CORR}, "
        f"tronçon radial ≥ {MIN_RUN} échantillons ; directions ±x, ±y (axes du volume) ; centroïde de l'enveloppe remplie.",
        "- Rouleaux sans segment publié : identifiée = 0, donc ratio = 0 (trivial) ; voir le sous-ensemble ci-dessus.",
        "",
        "| " + " | ".join(MD_COLS + ["surface_estimee_cm2 [bas–haut]", "ratio [bas–haut]", "raison"]) + " |",
        "|" + "---|" * (len(MD_COLS) + 3),
    ]
    for r in rows:
        lines.append("| " + " | ".join(str(r[c]) for c in MD_COLS) + f" | {interval(r)} | {ratio(r)} | {r['raison']} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_results(rows: list[dict], path: Path) -> None:
    """results.json : verdict H-028 + contrôles de vraisemblance + sensibilité (hors verdict)."""
    keep = ["id", "volume_utilise", "pixel_um", "surface_identifiee_cm2", "hauteur_mm", "n_segments", "n_segments_sans_area",
            "n_bandes_valides", "pas_um_median", "surface_estimee_basse_cm2", "surface_estimee_haute_cm2", "ratio_bas",
            "ratio_haut", "statut", "raison"]
    ext = {r["id"]: {"n_bandes_hi1500": len(r.get("_ext_pitches", [])),
                     "pas_med_hi1500": round(float(np.median(r["_ext_pitches"])), 1) if r.get("_ext_pitches") else None}
           for r in rows if r.get("volume_utilise")}
    out = {"hypothese": "H-028", "regle": "soutenue si ratio_haut<0.5 pour >50 % des estimés ; réfutée si ratio_bas>=0.5 pour >50 % ; sinon indéterminée",
           "tous_rouleaux": verdict(rows), "rouleaux_avec_segments": verdict([r for r in rows if r["n_segments"] > 0]),
           "n_rouleaux": len(rows), "n_inconnue": sum(r["statut"] == "inconnue" for r in rows),
           "controles": {r["id"]: {k: r[k] for k in keep} for r in rows if r["id"] in ("PHerc0172", "PHerc1667", "PHercParis4")},
           "sensibilite_hors_verdict_hi1500um": ext}
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    src, out_csv, out_md = map(Path, argv[1:4])
    meta = json.loads(src.read_text(encoding="utf-8"))
    t0 = time.time()
    scrolls = sorted(k for k, s in meta["samples"].items() if s.get("sample", {}).get("properties", {}).get("type") == "scroll")
    rows = []
    for rid in scrolls:
        rows.append(process_scroll(rid, meta["samples"][rid]))
        print(rid, rows[-1]["statut"], rows[-1]["raison"], f"{_bytes['n'] / 1e6:.0f} MB", flush=True)
    rows.sort(key=lambda r: (-r["n_segments"], r["id"]))
    write_outputs(rows, out_csv, out_md, f"Source : {src.name}")
    if len(argv) > 4:
        write_results(rows, Path(argv[4]))
    print(f"{len(rows)} rouleaux -> {out_csv}, {out_md} ; {_bytes['n'] / 1e6:.0f} MB téléchargés en {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
