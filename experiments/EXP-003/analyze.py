"""EXP-003 — E1.4 : Hecate 9,6 µm sur PHerc0841 (3 segments) et H-003 (fusion reader-v2 + Hecate).

Usage : PYTHONPATH=src python experiments/EXP-003/analyze.py <work_dir> <out.json>
Prédictions Hecate produites par `hecate_run.py` (runs/E1.4/<seg>/pred_hecate.tif), reader-v2 par EXP-001/E1.
Fusions testées : moyenne brute (échelles 0-255) et moyenne des rangs (insensible à la calibration).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from scipy.stats import rankdata

from vesres import eval_ink

SEGS = {
    "20260220213127-w00": "EXP-001",
    "20260220214732-auto_grown_20260220144552896": "E1/20260220214732-auto_grown_20260220144552896",
    "20260221022814-auto_grown_20260220174252405": "E1/20260221022814-auto_grown_20260220174252405",
}


def ranks(x: np.ndarray, valid: np.ndarray) -> np.ndarray:
    r = np.zeros(x.shape, np.float32)
    r[valid] = rankdata(x[valid]) / valid.sum()
    return r


def summary(m: dict) -> dict:
    return {k: {"auc_protocol": v.get("auc_protocol"), "auc_exact": v.get("auc_exact"), "ap": v.get("ap"),
                "best_f1": v.get("best_f1"), "ci95": v.get("bootstrap", {}).get("ci95")} for k, v in m.items()}


def main(work: Path, out: Path) -> None:
    res = {}
    for seg, rel in SEGS.items():
        a = tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif").astype(np.float32)
        h = tifffile.imread(work / "runs" / "E1.4" / seg / "pred_hecate.tif").astype(np.float32)
        assert a.shape == h.shape, (a.shape, h.shape)
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / "PHerc0841" / seg, a.shape)
        v = m["valid"]
        r = {"hecate": summary(eval_ink.evaluate(h, m)),
             "reader-v2": summary(eval_ink.evaluate(a, m)),
             "fusion_mean": summary(eval_ink.evaluate((a + h) / 2, m)),
             "fusion_rank": summary(eval_ink.evaluate((ranks(a, v) + ranks(h, v)) / 2, m)),
             "pearson_valid": round(float(np.corrcoef(a[v], h[v])[0, 1]), 4)}
        res[seg] = r
        print(seg, json.dumps({k: {kk: vv["auc_protocol"] for kk, vv in x.items()} if isinstance(x, dict) else x
                               for k, x in r.items()}), flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
