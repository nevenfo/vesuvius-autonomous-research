"""EXP-018 — H-017 : reader-v2-LO vs reader-v2 publié (et ink_9um s43, Hecate, fusions) sur les 5 segments étiquetés.

Usage : PYTHONPATH=src python experiments/EXP-018/analyze.py <work_dir> <tag> <out.json>
Prédictions LO : runs/EXP-018/eval/<seg>/pred_<tag>.tif (`run_eval.sh`). Le reste comme EXP-012/017.
Critère fixé avant (README) : H-017 réfutée si perte AUC sup. (reader-v2 − LO) moyenne sur 0009B et 0500P2 ≥ 0,03,
ou si cette perte dépasse de > 0,02 la perte moyenne sur 0841 (DiD).
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
SEGS, OBJ, load = exp013.SEGS, exp013.OBJ, exp013.load


def main(work: Path, tag: str, out: Path) -> None:
    rng = np.random.default_rng(0)
    res = {}
    for k, (obj, seg, rrv, _) in SEGS.items():
        p, m = load(work, k)
        lo = tifffile.imread(work / "runs" / "EXP-018" / "eval" / seg / f"pred_{tag}.tif").astype(np.float32) / 255
        q = {"reader-v2": p["rv2"], "lo": lo, "hecate": p["h"], "fusion_rv2_h": (p["rv2"] + p["h"]) / 2,
             "fusion_lo_h": (lo + p["h"]) / 2}
        s43 = work / "runs" / rrv / "pred_ink9um_s43.tif"
        if s43.exists():
            q["ink9um_s43"] = tifffile.imread(s43).astype(np.float32) / 255
        reg = m["valid"] & m["supervision"]
        r = {"object": OBJ[k]}
        for n, x in q.items():
            ev = eval_ink.evaluate(x, m)["in_supervision"]
            r[n] = {"auc": ev["auc_protocol"], "ap": ev["ap"], "ci95_auc": ev["bootstrap"]["ci95"]}
        r["loss_auc_rv2_minus_lo"] = round(r["reader-v2"]["auc"] - r["lo"]["auc"], 4)
        r["gain_ap_fusion_lo_h_vs_best_single"] = round(r["fusion_lo_h"]["ap"] - max(r["lo"]["ap"], r["hecate"]["ap"]), 4)
        r["ap_ci95_vs_reader-v2"] = exp013.paired_ci({"reader-v2": q["reader-v2"], "lo": q["lo"]}, "reader-v2",
                                                     m["inklabels"], reg, rng)["lo"]
        res[k] = r
        print(k, {n: (r[n]["auc"], r[n]["ap"]) for n in q}, r["loss_auc_rv2_minus_lo"], flush=True)
    seen = [res[k]["loss_auc_rv2_minus_lo"] for k in ("0009B", "0500P2")]
    unseen = [res[k]["loss_auc_rv2_minus_lo"] for k in SEGS if OBJ[k] == "0841"]
    res["loss_seen_mean"] = round(float(np.mean(seen)), 4)
    res["loss_0841_mean"] = round(float(np.mean(unseen)), 4)
    res["did"] = round(res["loss_seen_mean"] - res["loss_0841_mean"], 4)
    res["verdict_H017"] = "soutenue" if res["loss_seen_mean"] < 0.03 and res["did"] <= 0.02 else "réfutée"
    print(res["loss_seen_mean"], res["loss_0841_mean"], res["did"], res["verdict_H017"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
