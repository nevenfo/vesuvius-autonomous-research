"""Évaluation d'une carte de probabilité d'encre contre des ink-labels publiés.

Réplique le protocole de reader-v2 (scripts/v2_run.py, `evaluate`) pour comparabilité :
- pixels valides : tranche centrale du surface-volume > 0 ;
- masques (inklabels, supervision, validation) rééchantillonnés sur la grille de prédiction par
  cv2.INTER_AREA puis seuil ≥ 128 (`mask_on_canvas`) ;
- région « revue » = supervision ∪ validation ; AUC = Mann-Whitney sur sous-échantillon de 300 000 pos/neg,
  rng seed 0 (`auc_protocol`).
Ajouts (non présents chez reader-v2) : AUC exacte sur tous les pixels, AP, meilleur F1, et IC 95 % par
bootstrap de blocs spatiaux (les pixels voisins ne sont pas indépendants).

Usage : python -m vesres.eval_ink <pred.tif> <segment_dir> <out.json>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


def mask_on_canvas(arr: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    import cv2

    a = (np.asarray(arr) > 0).astype(np.uint8) * 255
    return cv2.resize(a, (shape[1], shape[0]), interpolation=cv2.INTER_AREA) >= 128


def auc_exact(pos: np.ndarray, neg: np.ndarray) -> float:
    """AUC de Mann-Whitney avec rangs moyens pour les ex-aequo."""
    from scipy.stats import rankdata

    s = np.concatenate([pos, neg]).astype(np.float64)
    r = rankdata(s)
    n1, n0 = len(pos), len(neg)
    return float((r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def auc_protocol(pos: np.ndarray, neg: np.ndarray, n: int = 300_000) -> float | None:
    rng = np.random.default_rng(0)
    if len(pos) < 100 or len(neg) < 100:
        return None
    sub = lambda a: a[rng.choice(len(a), min(n, len(a)), replace=False)]
    return round(auc_exact(sub(pos), sub(neg)), 4)


def pr_metrics(score: np.ndarray, label: np.ndarray) -> dict:
    from sklearn.metrics import average_precision_score, precision_recall_curve

    ap = float(average_precision_score(label, score))
    p, r, t = precision_recall_curve(label, score)
    f1 = 2 * p * r / np.maximum(p + r, 1e-12)
    i = int(np.nanargmax(f1[:-1])) if len(t) else 0
    return {"ap": round(ap, 4), "best_f1": round(float(f1[i]), 4), "best_f1_threshold": float(t[i]) if len(t) else None,
            "prevalence": round(float(label.mean()), 4)}


def block_bootstrap_auc(pred: np.ndarray, ink: np.ndarray, region: np.ndarray, block: int = 256,
                        n_boot: int = 200, per_block: int = 2000, seed: int = 0) -> dict:
    """IC 95 % de l'AUC par rééchantillonnage de blocs spatiaux (avec remise)."""
    rng = np.random.default_rng(seed)
    h, w = pred.shape
    blocks = []
    for y in range(0, h, block):
        for x in range(0, w, block):
            m = region[y:y + block, x:x + block]
            if m.sum() < 50:
                continue
            p = pred[y:y + block, x:x + block][m]
            l = ink[y:y + block, x:x + block][m]
            if len(p) > per_block:
                idx = rng.choice(len(p), per_block, replace=False)
                p, l = p[idx], l[idx]
            blocks.append((p, l))
    if len(blocks) < 10:
        return {"n_blocks": len(blocks), "ci95": None}
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(blocks), len(blocks))
        p = np.concatenate([blocks[i][0] for i in pick])
        l = np.concatenate([blocks[i][1] for i in pick])
        if l.all() or (~l).all():
            continue
        vals.append(auc_exact(p[l], p[~l]))
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return {"n_blocks": len(blocks), "block_px": block, "n_boot": len(vals), "ci95": [round(float(lo), 4), round(float(hi), 4)]}


def load_segment_masks(seg_dir: Path, shape: tuple[int, int]) -> dict[str, np.ndarray]:
    import zarr

    sv = zarr.open_array(str(seg_dir / "sv.zarr" / "0"), mode="r")
    out = {"valid": np.asarray(sv[sv.shape[0] // 2]) > 0}
    if out["valid"].shape != shape:
        raise ValueError(f"grille prédiction {shape} ≠ surface-volume {out['valid'].shape}")
    for nm in ("inklabels", "supervision", "validation"):
        p = seg_dir / f"{nm}.zarr" / "0"
        out[nm] = mask_on_canvas(zarr.open_array(str(p), mode="r")[:], shape) if p.exists() else np.zeros(shape, bool)
    return out


def evaluate(pred: np.ndarray, masks: dict[str, np.ndarray]) -> dict:
    pred = pred.astype(np.float32)
    valid, ink = masks["valid"], masks["inklabels"]
    reviewed = valid & (masks["supervision"] | masks["validation"])
    insup = valid & masks["supervision"]
    res = {}
    for name, reg in (("reviewed", reviewed), ("in_supervision", insup)):
        pos, neg = pred[reg & ink], pred[reg & ~ink]
        r = {"n_pos": int(len(pos)), "n_neg": int(len(neg)), "auc_protocol": auc_protocol(pos, neg)}
        if len(pos) >= 100 and len(neg) >= 100:
            r["auc_exact"] = round(auc_exact(pos, neg), 4)
            r.update(pr_metrics(pred[reg], ink[reg]))
            r["bootstrap"] = block_bootstrap_auc(pred, ink, reg)
        res[name] = r
    return res


def main(argv: list[str]) -> int:
    import tifffile

    pred_path, seg_dir, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    pred = tifffile.imread(pred_path)
    pred = pred if pred.ndim == 2 else pred.squeeze()
    masks = load_segment_masks(seg_dir, pred.shape)
    res = {"pred": str(pred_path), "segment_dir": str(seg_dir), "pred_dtype": str(pred.dtype),
           "pred_shape": list(pred.shape), "metrics": evaluate(pred, masks)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res["metrics"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
