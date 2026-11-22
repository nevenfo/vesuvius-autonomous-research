"""EXP-004 — H-009 : reader-v2, ink_9um s43, Hecate sur le segment étiqueté PHerc0009B (8,64 µm, 116 keV) + fusions.

Usage : PYTHONPATH=src python experiments/EXP-004/analyze.py <work_dir> <out.json>
Prédictions : runs/EXP-004/pred_{reader-v2,ink9um_s43}.tif (koine infer) et runs/EXP-004/<seg>/pred_hecate.tif
(experiments/EXP-003/hecate_run.py <seg> PHerc0009B 8.64 runs/EXP-004).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile

from vesres import eval_ink

SEG = "20250919125754-auto_grown_20250919055754487_inp_hr"


def summary(m: dict) -> dict:
    return {k: {"n_pos": v["n_pos"], "auc_protocol": v.get("auc_protocol"), "auc_exact": v.get("auc_exact"),
                "ap": v.get("ap"), "best_f1": v.get("best_f1"), "prevalence": v.get("prevalence"),
                "ci95": v.get("bootstrap", {}).get("ci95")} for k, v in m.items()}


def main(work: Path, out: Path) -> None:
    run = work / "runs" / "EXP-004"
    p = {"reader-v2": tifffile.imread(run / "pred_reader-v2.tif"),
         "ink9um_s43": tifffile.imread(run / "pred_ink9um_s43.tif"),
         "hecate": tifffile.imread(run / SEG / "pred_hecate.tif")}
    p = {k: v.astype(np.float32) for k, v in p.items()}
    shape = p["reader-v2"].shape
    assert all(v.shape == shape for v in p.values()), {k: v.shape for k, v in p.items()}
    m = eval_ink.load_segment_masks(work / "cache" / "segments" / "PHerc0009B" / SEG, shape)
    p["fusion_rv2_hecate"] = (p["reader-v2"] + p["hecate"]) / 2
    p["fusion_all3"] = (p["reader-v2"] + p["hecate"] + p["ink9um_s43"]) / 3
    v = m["valid"]
    res = {"segment": SEG, "shape": list(shape),
           "pearson_rv2_hecate": round(float(np.corrcoef(p["reader-v2"][v], p["hecate"][v])[0, 1]), 4),
           "models": {k: summary(eval_ink.evaluate(x, m)) for k, x in p.items()}}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    for k, r in res["models"].items():
        print(k, {g: (x["auc_protocol"], x["ap"], x["ci95"]) for g, x in r.items()})
    print("n_pos", {g: x["n_pos"] for g, x in res["models"]["hecate"].items()}, "pearson", res["pearson_rv2_hecate"])


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
