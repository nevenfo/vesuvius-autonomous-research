"""EXP-009 — H-007 : la qualité géométrique de la surface prédit-elle les erreurs locales de reader-v2 ? (PHerc0841)

Usage : PYTHONPATH=src python experiments/EXP-009/analyze.py <work_dir> <out.json>
Surface : tifxyz `*-on-20250821151531-9.366um.tifxyz` (même volume que le surface-volume ; scale 0,05 → un sommet
tous les STEP = 20 px de la grille de prédiction ; vérifié : forme × 20 = forme des prédictions).
Métriques par sommet (différences finies, sommets invalides = −1 exclus) :
- stretch : |log(‖∂P/∂u‖ / STEP)| + |log(‖∂P/∂v‖ / STEP)| (écart à l'isométrie, voxels) ;
- shear : |90° − angle(∂P/∂u, ∂P/∂v)| ;
- normal_var : angle moyen entre la normale et celles des 4 voisins (courbure / plis).
Tuilage, erreur (Brier) et contrôles identiques à EXP-007 (tuiles 64 px, supervision ≥ 50 %, ρ partiel sur rangs
contrôlant proba moyenne, prévalence et Brier attendu E[p(1−p)]). Métriques géométriques : moyenne et max par tuile.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
import tifffile
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-007"))
from analyze import partial_rho, prob  # noqa: E402  (EXP-007)

from vesres import eval_ink  # noqa: E402

TILE, MIN_COV, STEP = 64, 0.5, 20
SEGS = {
    "20260220213127-w00": "EXP-001",
    "20260220214732-auto_grown_20260220144552896": "E1/20260220214732-auto_grown_20260220144552896",
    "20260221022814-auto_grown_20260220174252405": "E1/20260221022814-auto_grown_20260220174252405",
}
GEO = ("stretch", "shear", "normal_var")


def geometry(d: Path) -> dict[str, np.ndarray]:
    P = np.stack([tifffile.imread(d / f"{c}.tif").astype(np.float64) for c in "xyz"], -1)
    ok = (P != -1).all(-1)
    du, dv = np.zeros_like(P), np.zeros_like(P)
    du[:, :-1], dv[:-1] = P[:, 1:] - P[:, :-1], P[1:] - P[:-1]
    oku = np.zeros_like(ok); oku[:, :-1] = ok[:, 1:] & ok[:, :-1]
    okv = np.zeros_like(ok); okv[:-1] = ok[1:] & ok[:-1]
    g = oku & okv
    lu, lv = np.linalg.norm(du, axis=-1), np.linalg.norm(dv, axis=-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        stretch = np.abs(np.log(lu / STEP)) + np.abs(np.log(lv / STEP))
        cos = (du * dv).sum(-1) / (lu * lv)
        shear = np.abs(90 - np.degrees(np.arccos(np.clip(cos, -1, 1))))
        n = np.cross(du, dv)
        n /= np.linalg.norm(n, axis=-1, keepdims=True)
    nv, cnt = np.zeros(ok.shape), np.zeros(ok.shape)
    for ax, sh in ((0, 1), (0, -1), (1, 1), (1, -1)):
        nn, gg = np.roll(n, sh, ax), np.roll(g, sh, ax)
        m = g & gg
        a = np.degrees(np.arccos(np.clip((n * nn).sum(-1), -1, 1)))
        nv[m] += a[m]; cnt[m] += 1
    out = {"stretch": stretch, "shear": shear, "normal_var": np.where(cnt > 0, nv / np.maximum(cnt, 1), np.nan)}
    return {k: np.where(g, v, np.nan) for k, v in out.items()}


def tiles(seg: str, rel: str, work: Path) -> dict[str, np.ndarray]:
    sd = work / "cache" / "segments" / "PHerc0841" / seg
    r2 = prob(tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif"))
    H, W = r2.shape
    geo = geometry(sd / "tifxyz_9.366")
    assert geo["stretch"].shape[0] * STEP == H and geo["stretch"].shape[1] * STEP == W
    geo = {k: cv2.resize(v.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST) for k, v in geo.items()}
    m = eval_ink.load_segment_masks(sd, r2.shape)
    reg, ink = m["valid"] & m["supervision"], m["inklabels"].astype(np.float32)
    maps = {"brier": (r2 - ink) ** 2, "mean_p": r2, "prevalence": ink, "exp_brier": r2 * (1 - r2)}
    out = {k: [] for k in (*maps, *GEO, *(f"{g}_max" for g in GEO))}
    for y in range(0, H - TILE + 1, TILE):
        for x in range(0, W - TILE + 1, TILE):
            msk = reg[y:y + TILE, x:x + TILE]
            if msk.mean() < MIN_COV:
                continue
            gt = {g: geo[g][y:y + TILE, x:x + TILE][msk] for g in GEO}
            if not all(np.isfinite(v).any() for v in gt.values()):
                continue
            for k, v in maps.items():
                out[k].append(float(v[y:y + TILE, x:x + TILE][msk].mean()))
            for g, v in gt.items():
                out[g].append(float(np.nanmean(v))); out[f"{g}_max"].append(float(np.nanmax(v)))
    return {k: np.array(v) for k, v in out.items()}


def stats(t: dict[str, np.ndarray]) -> dict:
    r = {"n_tiles": int(len(t["brier"]))}
    for g in (*GEO, *(f"{g}_max" for g in GEO)):
        r[g] = {"median": round(float(np.median(t[g])), 3),
                "spearman": round(float(spearmanr(t[g], t["brier"])[0]), 3),
                "partial_vs_meanp_prev": round(partial_rho(t[g], t["brier"], [t["mean_p"], t["prevalence"]]), 3),
                "partial_vs_meanp_prev_expbrier": round(partial_rho(t[g], t["brier"],
                                                                    [t["mean_p"], t["prevalence"], t["exp_brier"]]), 3),
                "spearman_vs_exp_brier": round(float(spearmanr(t[g], t["exp_brier"])[0]), 3)}
    return r


def main(work: Path, out: Path) -> None:
    res, pool = {}, {}
    for seg, rel in SEGS.items():
        t = tiles(seg, rel, work)
        res[seg] = stats(t)
        for k, v in t.items():
            pool.setdefault(k, []).append(v)
        print(seg[:14], json.dumps(res[seg]), flush=True)
    res["pooled"] = stats({k: np.concatenate(v) for k, v in pool.items()})
    print("pooled", json.dumps(res["pooled"]), flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
