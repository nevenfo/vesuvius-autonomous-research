"""EXP-019 (K3.2) — courbe performance/durée des checkpoints EXP-018 sur la validation K (protocole K2).

Usage : PYTHONPATH=src python experiments/EXP-019/analyze.py <work_dir> <ref_step> <out.json> <step> [<step>...]
Prédictions : <work>/runs/EXP-019/<seg>/pred_<step>.tif (`run_val.sh`). Labels : `build.py` role=holdout
(<work>/data/v2lo_val/<obj>/labels/<id>/<id>_{inklabels,supervision_mask}.zarr, tranche centrale).
Région = valide & supervision. Métriques par segment : AUC exacte, AP. Non-infériorité (docs/protocols/training-duration.md) :
bootstrap apparié par blocs de 256 px (mêmes blocs pour toutes les étapes), moyenne des 4 segments,
Δ = AUC(step) − AUC(ref) ; non inférieure si borne basse IC 95 % unilatéral (5e centile) > −δ, δ = 0,01.
Courbe descriptive d'un run cosine : un checkpoint intermédiaire n'est pas un run court recuit (borne basse).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
import zarr
from sklearn.metrics import average_precision_score

from vesres import eval_ink

VAL = [("0343P", "20250904233748-0_b2"), ("0343P", "20250905172054-1_b2"),
       ("0172", "20250926122938-w082_20250926122938619_fl"), ("0172", "20250926132117-w083_20250926132117595_fl")]
DELTA, BLOCK, PER_BLOCK, N_BOOT = 0.01, 256, 2000, 1000


def masks(work: Path, obj: str, sid: str):
    d = work / "data" / "v2lo_val" / obj
    sv = zarr.open_array(str(d / sid / "sv.zarr" / "0"), mode="r")
    z = sv.shape[0] // 2
    valid = np.asarray(sv[z]) > 0
    lab = {n: np.asarray(zarr.open_array(str(d / "labels" / sid / f"{sid}_{n}.zarr" / "0"), mode="r")[z]) > 0
           for n in ("inklabels", "supervision_mask")}
    return lab["inklabels"], valid & lab["supervision_mask"]


def blocks_of(preds: dict, ink, reg, rng):
    h, w = reg.shape
    out = []
    for y in range(0, h, BLOCK):
        for x in range(0, w, BLOCK):
            idx = np.flatnonzero(reg[y:y + BLOCK, x:x + BLOCK])
            if len(idx) < 50:
                continue
            if len(idx) > PER_BLOCK:
                idx = rng.choice(idx, PER_BLOCK, replace=False)
            b = {k: v[y:y + BLOCK, x:x + BLOCK].ravel()[idx] for k, v in preds.items()}
            b["_y"] = ink[y:y + BLOCK, x:x + BLOCK].ravel()[idx]
            out.append(b)
    return out


def main(work: Path, ref: int, out: Path, steps: list[int]) -> None:
    rng = np.random.default_rng(0)
    steps = sorted(set(steps) | {ref})
    per_seg, seg_blocks = {}, []
    for obj, sid in VAL:
        ink, reg = masks(work, obj, sid)
        preds = {s: tifffile.imread(work / "runs" / "EXP-019" / sid / f"pred_{s}.tif").astype(np.float32) for s in steps}
        if next(iter(preds.values())).shape != reg.shape:
            raise ValueError(f"{sid} : grille prédiction ≠ labels")
        r = {}
        for s, p in preds.items():
            pos, neg = p[reg & ink], p[reg & ~ink]
            r[s] = {"auc": round(eval_ink.auc_exact(pos, neg), 4),
                    "ap": round(float(average_precision_score(ink[reg], p[reg])), 4),
                    "n_pos": int(len(pos)), "n_neg": int(len(neg))}
        per_seg[sid] = r
        seg_blocks.append(blocks_of(preds, ink, reg, rng))
    diffs = {s: [] for s in steps if s != ref}
    for _ in range(N_BOOT):
        aucs = {s: [] for s in steps}
        for bl in seg_blocks:
            pick = rng.integers(0, len(bl), len(bl))
            y = np.concatenate([bl[i]["_y"] for i in pick])
            if y.all() or not y.any():
                break
            for s in steps:
                p = np.concatenate([bl[i][s] for i in pick])
                aucs[s].append(eval_ink.auc_exact(p[y], p[~y]))
        else:
            for s in diffs:
                diffs[s].append(np.mean(aucs[s]) - np.mean(aucs[ref]))
    mean = {s: {m: round(float(np.mean([per_seg[k][s][m] for k in per_seg])), 4) for m in ("auc", "ap")} for s in steps}
    ni = {}
    for s, d in diffs.items():
        lo5, lo25, hi = np.percentile(d, [5, 2.5, 97.5])
        ni[s] = {"delta_auc": round(mean[s]["auc"] - mean[ref]["auc"], 4), "lb95_one_sided": round(float(lo5), 4),
                 "ci95": [round(float(lo25), 4), round(float(hi), 4)], "n_boot": len(d),
                 "non_inferior": bool(lo5 > -DELTA)}
    res = {"ref_step": ref, "delta": DELTA, "mean": mean, "non_inferiority": ni, "per_segment": per_seg,
           "status": "descriptif (checkpoints d'un run cosine 40k, borne basse d'un run court recuit)"}
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    for s in steps:
        print(s, mean[s], ni.get(s, "ref"))


if __name__ == "__main__":
    main(Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]), [int(x) for x in sys.argv[4:]])
