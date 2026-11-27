"""EXP-027 (X2 / H-032) : auto-cohérence de rendus redondants de PHerc1667.

Méthode fixée dans README.md. Fonctions pures testées dans tests/test_redundancy.py.
CLI : python experiments/EXP-027/redundancy.py [--catalog PATH] [--out results.json]
Cache : <VESRES_WORK>/cache/exp027/ (écritures atomiques). Aucune image d'encre n'est écrite dans le dépôt.
"""
import argparse
import io
import json
import os
import re
import sys
import time
import urllib.request
from itertools import combinations
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image
from scipy.spatial import cKDTree
from scipy.stats import rankdata

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from vesres.paths import WORK  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
BASE = "https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/"
CACHE = WORK / "cache" / "exp027"
SAMPLE = "PHerc1667"
VOLUME = "20251217075048-2.399um.tifxyz/"      # repère volumique commun (volume 2,399 µm)
MODEL = "new_canon_autoresearch_recipe"          # modèle présent sur tous les segments avec encre
VOXEL_UM = 2.399
TOL_VOX = 2.0
COS_MIN = 0.9
MIN_NODES = 2000
N_SHIFTS = 20
MIN_SHIFT_MM = 3.0
DS = 8                                           # facteur de la prédiction « -ds8.jpg »


# ---------------------------------------------------------------- fonctions pures
def valid_mask(X, Y, Z):
    return np.isfinite(X) & np.isfinite(Y) & np.isfinite(Z) & ~((X == -1) & (Y == -1) & (Z == -1))


def grid_normals(X, Y, Z):
    """Normales unitaires (rows, cols, 3) par différences finies centrales ; NaN si un voisin manque."""
    P = np.stack([X, Y, Z], axis=-1).astype(np.float64)
    P[~valid_mask(X, Y, Z)] = np.nan
    dr = np.full_like(P, np.nan)
    dc = np.full_like(P, np.nan)
    dr[1:-1] = P[2:] - P[:-2]
    dc[:, 1:-1] = P[:, 2:] - P[:, :-2]
    n = np.cross(dr, dc)
    norm = np.linalg.norm(n, axis=-1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        n = n / norm
    n[(norm[..., 0] == 0)] = np.nan
    return n


def match_nodes(PA, NA, PB, NB, tol=TOL_VOX, cos_min=COS_MIN, tree_b=None):
    """Appariement 1-1 de nœuds : distance <= tol et |cos| >= cos_min. Retourne (ia, ib, dist)
    (indices dans PA/PB). Pour chaque nœud de A le plus proche B compatible ; chaque B gardé une fois (le plus proche)."""
    if len(PA) == 0 or len(PB) == 0:
        e = np.zeros(0, dtype=np.int64)
        return e, e.copy(), np.zeros(0)
    tree = tree_b if tree_b is not None else cKDTree(PB)
    k = min(4, len(PB))
    d, j = tree.query(PA, k=k, distance_upper_bound=tol)
    d = d.reshape(len(PA), -1)
    j = j.reshape(len(PA), -1)
    best_d = np.full(len(PA), np.inf)
    best_j = np.full(len(PA), -1, dtype=np.int64)
    for c in range(d.shape[1]):
        ok = np.isfinite(d[:, c]) & (best_j < 0)
        idx = np.where(ok)[0]
        if len(idx) == 0:
            continue
        cosv = np.abs(np.einsum("ij,ij->i", NA[idx], NB[j[idx, c]]))
        good = idx[cosv >= cos_min]
        best_j[good] = j[good, c]
        best_d[good] = d[good, c]
    ia = np.where(best_j >= 0)[0]
    ib = best_j[ia]
    dist = best_d[ia]
    order = np.argsort(dist, kind="stable")
    ia, ib, dist = ia[order], ib[order], dist[order]
    _, first = np.unique(ib, return_index=True)
    keep = np.sort(first)
    return ia[keep], ib[keep], dist[keep]


def spearman(a, b):
    if len(a) < 3:
        return float("nan")
    ra, rb = rankdata(a), rankdata(b)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def node_ink(ds_img, shape, scale=0.05):
    """Valeur d'encre par nœud (rows, cols) : moyenne de la prédiction sur la cellule de rendu du nœud.
    ds_img = prédiction réduite d'un facteur DS ; un nœud = 1/scale px de rendu = 1/(scale*DS) px réduits
    (2,5 px). Cellule approchée par boxFilter 3x3 échantillonnée en bilinéaire au centre du nœud."""
    import cv2
    img = ds_img.astype(np.float32)
    box = cv2.blur(img, (3, 3))
    step = 1.0 / (scale * DS)
    # nœud (i,j) = pixel plein (i/scale, j/scale) -> pixel réduit (i*step, j*step) (décalage de pixel < 0,5 px réduit ignoré)
    rows, cols = shape
    mx = ((np.arange(cols) + 0.0) * step).astype(np.float32)
    my = ((np.arange(rows) + 0.0) * step).astype(np.float32)
    MX, MY = np.meshgrid(mx, my)
    return cv2.remap(box, MX, MY, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)


def circular_null(values_b, ia, ib, values_a, axis, min_shift, n_shifts=N_SHIFTS):
    """Distribution nulle : ρ(a[ia], roll(b, s, axis)[ib]) pour n_shifts décalages circulaires uniformes
    dans [min_shift, n-min_shift] le long de `axis` de la grille 2D values_b."""
    n = values_b.shape[axis]
    lo, hi = int(min_shift), n - int(min_shift)
    if hi <= lo:
        return np.array([])
    shifts = np.unique(np.linspace(lo, hi, n_shifts).astype(int))
    va = values_a.reshape(-1)[ia]
    out = []
    for s in shifts:
        vb = np.roll(values_b, int(s), axis=axis).reshape(-1)[ib]
        ok = np.isfinite(va) & np.isfinite(vb)
        out.append(spearman(va[ok], vb[ok]))
    return np.array(out)


def classify_pair(name_a, name_b):
    """'derivee' si même numéro de spire wNNN ou suffixe merged/straightened, sinon 'independante'."""
    wa, wb = re.match(r"w(\d+)", name_a), re.match(r"w(\d+)", name_b)
    if (wa and wb and wa.group(1) == wb.group(1)) or any(
            t in nm for nm in (name_a, name_b) for t in ("merged", "straightened")):
        return "derivee"
    return "independante"


def verdict(rhos, null_p95, min_pairs=3):
    """Règle H-032 : indéterminée si < 3 paires ; soutenue si médiane >= 0,5 et >= 80 % des paires > p95 nul."""
    rhos, null_p95 = np.asarray(rhos, float), np.asarray(null_p95, float)
    if len(rhos) < min_pairs:
        return {"verdict": "indeterminee", "n_pairs": int(len(rhos))}
    med = float(np.median(rhos))
    frac = float(np.mean(rhos > null_p95))
    ok = med >= 0.5 and frac >= 0.8
    return {"verdict": "soutenue" if ok else "refutee", "n_pairs": int(len(rhos)),
            "median_rho": med, "frac_above_null_p95": frac}


# ---------------------------------------------------------------- E/S
def _get(path, dest):
    dest = Path(dest)
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(BASE + path, timeout=120) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    os.replace(tmp, dest)
    return dest


def select_segments(meta):
    segs = meta["samples"][SAMPLE]["segments"]
    out = {}
    for sid, v in segs.items():
        tx = ds = None
        for e in v["data"]:
            p = e["origins"][0]["path"]
            if e["type"] == "tifxyz-transformed" and p.endswith("-on-" + VOLUME):
                tx = p
            elif (e["type"] == "ink-detection-downsampled" and MODEL in p and "-t2-" not in p
                  and "-2.399um-" in p and p.endswith("-ds8.jpg")):
                ds = p
        if tx and ds:
            out[sid] = {"name": v["suffix"], "tifxyz": tx, "ds": ds}
    return out


def load_segment(sid, info):
    d = CACHE / sid
    for f in ("x.tif", "y.tif", "z.tif", "meta.json"):
        _get(info["tifxyz"] + f, d / f)
    _get(info["ds"], d / "ds8.jpg")
    X, Y, Z = (tifffile.imread(d / f"{c}.tif").astype(np.float32) for c in "xyz")
    meta = json.loads((d / "meta.json").read_text())
    ds = np.asarray(Image.open(d / "ds8.jpg").convert("L"))
    return X, Y, Z, meta, ds


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default=str(WORK / "cache/catalog/metadata.min.2026-11-27.json"))
    ap.add_argument("--out", default=str(Path(__file__).with_name("results.json")))
    ap.add_argument("--tol", type=float, default=TOL_VOX)
    a = ap.parse_args(argv)
    t0 = time.time()
    meta = json.load(open(a.catalog, encoding="utf-8"))
    segs = select_segments(meta)
    print(len(segs), "segments", flush=True)
    data = {}
    for sid, info in segs.items():
        X, Y, Z, m, ds = load_segment(sid, info)
        ok = valid_mask(X, Y, Z)
        scale = float(m["scale"][0])
        ink = node_ink(ds, X.shape, scale)
        N = grid_normals(X, Y, Z)
        okn = ok & np.isfinite(N[..., 0])
        idx = np.flatnonzero(okn.reshape(-1))
        P = np.stack([X, Y, Z], -1).reshape(-1, 3)[idx].astype(np.float64)
        data[sid] = dict(name=info["name"], shape=X.shape, scale=scale, idx=idx, P=P,
                         N=N.reshape(-1, 3)[idx], ink=ink, ds_shape=ds.shape,
                         bbox=(P.min(0), P.max(0)), tree=None)
        print(sid, info["name"], X.shape, ds.shape, len(idx), flush=True)
    results = []
    for sa, sb in combinations(sorted(data), 2):
        A, B = data[sa], data[sb]
        if np.any(A["bbox"][1] + a.tol < B["bbox"][0]) or np.any(B["bbox"][1] + a.tol < A["bbox"][0]):
            continue
        if B["tree"] is None:
            B["tree"] = cKDTree(B["P"])
        ia, ib, dist = match_nodes(A["P"], A["N"], B["P"], B["N"], tol=a.tol, tree_b=B["tree"])
        if len(ia) == 0:
            continue
        ga, gb = A["idx"][ia], B["idx"][ib]
        va, vb = A["ink"].reshape(-1)[ga], B["ink"].reshape(-1)[gb]
        okv = np.isfinite(va) & np.isfinite(vb)
        n = int(okv.sum())
        rec = {"a": sa, "b": sb, "name_a": A["name"], "name_b": B["name"],
               "categorie": classify_pair(A["name"], B["name"]), "n_nodes": n,
               "median_match_dist_vox": float(np.median(dist)) if len(dist) else None,
               "frac_exact_nodes": float(np.mean(dist < 0.05)) if len(dist) else None}
        if n >= MIN_NODES:
            rec["chevauchante"] = True
            rec["rho"] = spearman(va[okv], vb[okv])
            axis = 0 if B["shape"][0] >= B["shape"][1] else 1
            # nœud = 1/scale voxels ; 3 mm = 3000/VOXEL_UM voxels
            min_shift = (MIN_SHIFT_MM * 1000.0 / VOXEL_UM) * B["scale"]
            null = circular_null(B["ink"], ia=ga[okv], ib=gb[okv], values_a=A["ink"], axis=axis,
                                 min_shift=int(np.ceil(min_shift)))
            rec["null_rho"] = [float(x) for x in null]
            rec["null_p95"] = float(np.nanpercentile(null, 95)) if len(null) else None
            rec["null_axis"] = axis
            rec["min_shift_nodes"] = int(np.ceil(min_shift))
        else:
            rec["chevauchante"] = False
        results.append(rec)
        print(rec["a"], rec["b"], rec["categorie"], n, rec.get("rho"), rec.get("null_p95"), flush=True)
    ov = [r for r in results if r["chevauchante"]]
    summ = {}
    for label, sel in (("independantes", [r for r in ov if r["categorie"] == "independante"]),
                       ("derivees", [r for r in ov if r["categorie"] == "derivee"]),
                       ("toutes", ov)):
        summ[label] = verdict([r["rho"] for r in sel], [r["null_p95"] for r in sel])
    out = {"experience": "EXP-027", "hypothese": "H-032", "volume": VOLUME, "modele": MODEL,
           "tol_vox": a.tol, "cos_min": COS_MIN, "min_nodes": MIN_NODES,
           "segments": {sid: {"name": d["name"], "grid_shape": list(d["shape"]), "n_valid_nodes": int(len(d["idx"]))}
                        for sid, d in data.items()},
           "n_pairs_bbox_and_matched": len(results), "pairs": results, "verdicts": summ,
           "duree_s": round(time.time() - t0, 1)}
    Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(summ, indent=1))
    return out


if __name__ == "__main__":
    main()
