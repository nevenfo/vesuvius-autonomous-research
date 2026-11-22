"""EXP-006 — H-004 : sensibilité de reader-v2 au décalage de la fenêtre de 17 couches (PHerc0841, 3 segments).

Usage : PYTHONPATH=src python experiments/EXP-006/analyze.py <work_dir> <out.json>
Prédictions : runs/EXP-006/<seg>/pred_s<s>.tif (run_sweep.sh). Contrôle : s=0 doit égaler la prédiction EXP-001/E1.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile

from vesres import eval_ink

SEGS = {
    "20260220213127-w00": "EXP-001",
    "20260220214732-auto_grown_20260220144552896": "E1/20260220214732-auto_grown_20260220144552896",
    "20260221022814-auto_grown_20260220174252405": "E1/20260221022814-auto_grown_20260220174252405",
}
SHIFTS = range(-6, 6)


def main(work: Path, out: Path) -> None:
    res = {}
    for seg, rel in SEGS.items():
        ref = tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif")
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / "PHerc0841" / seg, ref.shape)
        r = {"s0_identical_to_baseline": None, "shifts": {}}
        for s in SHIFTS:
            p = tifffile.imread(work / "runs" / "EXP-006" / seg / f"pred_s{s}.tif")
            if s == 0:
                r["s0_identical_to_baseline"] = bool(np.array_equal(p, ref))
                r["s0_max_abs_diff"] = int(np.abs(p.astype(np.int16) - ref.astype(np.int16)).max())
            ev = eval_ink.evaluate(p.astype(np.float32), m)
            r["shifts"][s] = {g: {"auc_protocol": v["auc_protocol"], "ap": v.get("ap"),
                                  "ci95": v.get("bootstrap", {}).get("ci95")} for g, v in ev.items()}
        sup = {s: v["in_supervision"]["auc_protocol"] for s, v in r["shifts"].items()}
        best = max(sup, key=sup.get)
        r["best_shift_supervision"] = best
        r["gain_vs_s0"] = round(sup[best] - sup[0], 4)
        res[seg] = r
        print(seg[:14], "s0==base", r["s0_identical_to_baseline"], "sup AUC", sup, "best", best, "gain", r["gain_vs_s0"], flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
