"""EXP-015 — H-012 : TTA miroir (`--tta-mirror`, 4 variantes axes 1-2) de reader-v2 vs passe unique sur 0841 × 3.

Usage : PYTHONPATH=src python experiments/EXP-015/analyze.py <work_dir> <out.json>
Inférence : `run_tta.sh` (options d'EXP-001 + `--tta-mirror --tta-batch-size 2`) → runs/EXP-015/<seg>/pred_reader-v2_tta.tif.
Passe unique : prédictions d'EXP-001/E1 (chemins d'EXP-012). Critère fixé avant : H-012 réfutée si gain AUC sup. moyen
< 0,01. IC95 apparié du gain d'AP par bootstrap de blocs (fonction d'EXP-013).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import tifffile

from vesres import eval_ink

_spec = importlib.util.spec_from_file_location("exp013", Path(__file__).parents[1] / "EXP-013" / "analyze.py")
exp013 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exp013)
SEGS = {k: v for k, v in exp013.SEGS.items() if k.startswith("0841")}


def main(work: Path, out: Path) -> None:
    rng = np.random.default_rng(0)
    res = {}
    for k, (obj, seg, rrv, _) in SEGS.items():
        p = {"single": tifffile.imread(work / "runs" / rrv / "pred_reader-v2.tif").astype(np.float32),
             "tta": tifffile.imread(work / "runs" / "EXP-015" / seg / "pred_reader-v2_tta.tif").astype(np.float32)}
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / obj / seg, p["single"].shape)
        reg = m["valid"] & m["supervision"]
        r = {}
        for n, x in p.items():
            ev = eval_ink.evaluate(x, m)["in_supervision"]
            r[n] = {"auc": ev["auc_protocol"], "ap": ev["ap"], "ci95_auc": ev["bootstrap"]["ci95"]}
        r["gain_auc"] = round(r["tta"]["auc"] - r["single"]["auc"], 4)
        r["gain_ap"] = round(r["tta"]["ap"] - r["single"]["ap"], 4)
        r["gain_ap_ci95"] = exp013.paired_ci(p, "single", m["inklabels"], reg, rng)["tta"]
        r["pearson_single_tta"] = round(float(np.corrcoef(p["single"][m["valid"]], p["tta"][m["valid"]])[0, 1]), 4)
        res[k] = r
        print(k, json.dumps(r), flush=True)
    res["gain_auc_mean"] = round(float(np.mean([res[k]["gain_auc"] for k in SEGS])), 4)
    res["gain_ap_mean"] = round(float(np.mean([res[k]["gain_ap"] for k in SEGS])), 4)
    res["verdict_H012"] = "soutenue" if res["gain_auc_mean"] >= 0.01 else "réfutée"
    print(res["gain_auc_mean"], res["gain_ap_mean"], res["verdict_H012"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
