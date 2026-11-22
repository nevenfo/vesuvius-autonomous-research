"""EXP-007 — H-006 : un indicateur sans label prédit-il les erreurs locales de reader-v2 ? (PHerc0841, région supervision)

Usage : PYTHONPATH=src python experiments/EXP-007/analyze.py <work_dir> <out.json>
Tuiles TILE×TILE px (grille 9,366 µm) dont ≥ MIN_COV des pixels sont valides et en supervision.
Erreur locale = Brier de reader-v2 (proba = pred / max dtype) vs inklabels.
Indicateurs sans label : |reader-v2 − Hecate| moyen ; entropie binaire moyenne de reader-v2 ;
écart-type de reader-v2 sur la fenêtre de couches s ∈ {−1, 0, +1} (EXP-006).
Encre manquée = part des pixels d'encre étiquetée avec proba < 0,5, sur les tuiles à prévalence ≥ MIN_INK.
Statistiques : Spearman ρ par segment et tuiles poolées ; ρ partiel contrôlant la proba moyenne de reader-v2 et la
prévalence d'encre étiquetée (résidus de rangs) — l'erreur de Brier croît mécaniquement avec la prévalence ;
variante ajoutant le Brier attendu sous calibration E[p(1−p)], proche de l'entropie par construction.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from scipy.stats import rankdata, spearmanr

from vesres import eval_ink

TILE, MIN_COV, MIN_INK = 64, 0.5, 0.02
SEGS = {
    "20260220213127-w00": "EXP-001",
    "20260220214732-auto_grown_20260220144552896": "E1/20260220214732-auto_grown_20260220144552896",
    "20260221022814-auto_grown_20260220174252405": "E1/20260221022814-auto_grown_20260220174252405",
}


def prob(a: np.ndarray) -> np.ndarray:
    return a.astype(np.float32) / (np.iinfo(a.dtype).max if a.dtype.kind in "ui" else 1.0)


def partial_rho(x, y, covs) -> float:
    r = [rankdata(v) for v in (x, y, *covs)]
    C = np.column_stack([np.ones(len(x)), *r[2:]])
    res = [v - C @ np.linalg.lstsq(C, v, rcond=None)[0] for v in r[:2]]
    return float(np.corrcoef(*res)[0, 1])


def tiles(seg: str, rel: str, work: Path) -> dict[str, np.ndarray]:
    r2 = prob(tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif"))
    he = prob(tifffile.imread(work / "runs" / "E1.4" / seg / "pred_hecate.tif"))
    sh = np.stack([prob(tifffile.imread(work / "runs" / "EXP-006" / seg / f"pred_s{s}.tif")) for s in (-1, 0, 1)])
    assert np.array_equal(sh[1], r2)
    m = eval_ink.load_segment_masks(work / "cache" / "segments" / "PHerc0841" / seg, r2.shape)
    reg, ink = m["valid"] & m["supervision"], m["inklabels"].astype(np.float32)
    p = np.clip(r2, 1e-6, 1 - 1e-6)
    maps = {"brier": (r2 - ink) ** 2, "dis_hecate": np.abs(r2 - he),
            "entropy": -(p * np.log2(p) + (1 - p) * np.log2(1 - p)), "shift_std": sh.std(0),
            "mean_p": r2, "prevalence": ink, "exp_brier": r2 * (1 - r2),
            "miss": np.where(ink > 0, (r2 < 0.5).astype(np.float32), np.nan)}
    H, W = r2.shape
    out = {k: [] for k in maps}
    for y in range(0, H - TILE + 1, TILE):
        for x in range(0, W - TILE + 1, TILE):
            msk = reg[y:y + TILE, x:x + TILE]
            if msk.mean() < MIN_COV:
                continue
            for k, v in maps.items():
                w = v[y:y + TILE, x:x + TILE][msk]
                out[k].append(float(np.nanmean(w)) if np.isfinite(w).any() else np.nan)
    return {k: np.array(v) for k, v in out.items()}


def stats(t: dict[str, np.ndarray]) -> dict:
    r = {"n_tiles": int(len(t["brier"]))}
    for k in ("dis_hecate", "entropy", "shift_std"):
        r[k] = {"spearman": round(float(spearmanr(t[k], t["brier"])[0]), 3),
                "partial_vs_meanp_prev": round(partial_rho(t[k], t["brier"], [t["mean_p"], t["prevalence"]]), 3),
                "partial_vs_meanp_prev_expbrier": round(partial_rho(t[k], t["brier"],
                                                                    [t["mean_p"], t["prevalence"], t["exp_brier"]]), 3)}
        ok = t["prevalence"] >= MIN_INK
        r[k]["miss_rate_spearman"] = round(float(spearmanr(t[k][ok], t["miss"][ok])[0]), 3)
        r[k]["miss_rate_partial_vs_meanp"] = round(partial_rho(t[k][ok], t["miss"][ok], [t["mean_p"][ok]]), 3)
    r["n_tiles_ink"] = int((t["prevalence"] >= MIN_INK).sum())
    r["prevalence_vs_brier"] = round(float(spearmanr(t["prevalence"], t["brier"])[0]), 3)
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
