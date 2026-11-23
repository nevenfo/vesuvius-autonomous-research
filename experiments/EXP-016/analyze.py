"""EXP-016 — H-015 : TTA reader-v2 répliquée (0009B, 0500P2) et cumulée à la fusion Hecate, 5 segments.

Usage : PYTHONPATH=src python experiments/EXP-016/analyze.py <work_dir> <out.json>
reader-v2 TTA : runs/EXP-015/<seg> (0841) et runs/EXP-016/<seg> (0009B, 0500P2, `run_tta.sh`) ; le reste comme EXP-012.
Variantes : rv2, rv2_tta, hecate, fusion = (rv2 + h)/2, fusion_tta = (rv2_tta + h)/2.
Critère fixé avant : H-015 réfutée si gain AP moyen (fusion_tta − fusion, 3 objets, 0841 moyenné) < 0,01.
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


def main(work: Path, out: Path) -> None:
    rng = np.random.default_rng(0)
    res = {}
    for k, (obj, seg, _, _) in SEGS.items():
        p, m = load(work, k)
        run = "EXP-015" if obj == "PHerc0841" else "EXP-016"
        tta = tifffile.imread(work / "runs" / run / seg / "pred_reader-v2_tta.tif").astype(np.float32) / 255
        q = {"rv2": p["rv2"], "rv2_tta": tta, "hecate": p["h"], "fusion": (p["rv2"] + p["h"]) / 2,
             "fusion_tta": (tta + p["h"]) / 2}
        reg = m["valid"] & m["supervision"]
        r = {"object": OBJ[k]}
        for n, x in q.items():
            ev = eval_ink.evaluate(x, m)["in_supervision"]
            r[n] = {"auc": ev["auc_protocol"], "ap": ev["ap"]}
        r["gain_ap"] = {"tta_single": round(r["rv2_tta"]["ap"] - r["rv2"]["ap"], 4),
                        "tta_fusion": round(r["fusion_tta"]["ap"] - r["fusion"]["ap"], 4),
                        "fusion_tta_vs_best_single": round(r["fusion_tta"]["ap"] - max(r["rv2_tta"]["ap"], r["hecate"]["ap"]), 4)}
        r["gain_auc"] = {"tta_single": round(r["rv2_tta"]["auc"] - r["rv2"]["auc"], 4),
                         "tta_fusion": round(r["fusion_tta"]["auc"] - r["fusion"]["auc"], 4)}
        ci1 = exp013.paired_ci({"rv2": q["rv2"], "rv2_tta": q["rv2_tta"]}, "rv2", m["inklabels"], reg, rng)
        ci2 = exp013.paired_ci({"fusion": q["fusion"], "fusion_tta": q["fusion_tta"]}, "fusion", m["inklabels"], reg, rng)
        r["gain_ap_ci95"] = {"tta_single": ci1["rv2_tta"], "tta_fusion": ci2["fusion_tta"]}
        res[k] = r
        print(k, {n: (r[n]["auc"], r[n]["ap"]) for n in q}, r["gain_ap"], r["gain_ap_ci95"], flush=True)
    keys = ("tta_single", "tta_fusion", "fusion_tta_vs_best_single")
    per_obj = {o: {g: round(float(np.mean([res[k]["gain_ap"][g] for k in SEGS if OBJ[k] == o])), 4) for g in keys}
               for o in ("0841", "0009B", "0500P2")}
    res["gain_ap_per_object"] = per_obj
    res["gain_ap_mean"] = {g: round(float(np.mean([v[g] for v in per_obj.values()])), 4) for g in keys}
    res["verdict_H015"] = "soutenue" if res["gain_ap_mean"]["tta_fusion"] >= 0.01 else "réfutée"
    print(per_obj, res["gain_ap_mean"], res["verdict_H015"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
