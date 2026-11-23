"""EXP-017 — H-016 : prédictions officielles publiées (canon 2,4 µm, ink9um, reader-v3, argus-v3) vs nos modèles.

Usage : PYTHONPATH=src python experiments/EXP-017/analyze.py <work_dir> <out.json>
Prédictions officielles : `<scroll>/segments/<seg>/ink-detection/*.tif` du bucket public (liste exacte : `sources.txt`),
copiées dans runs/EXP-017/<seg>/pred_{canon,ink9um_off,reader-v3,argus-v3}.tif. La carte canon (grille des labels
2,4 µm) est ramenée sur la grille du surface-volume local par cv2.INTER_AREA (float32), comme les masques.
Nos modèles : reader-v2, Hecate, fusion (EXP-012/013) et ink_9um s43 (notre inférence) pour contrôle.
Critère fixé avant : H-016 réfutée si AUC sup.(canon) − AUC sup.(fusion) < 0,02 en moyenne sur 0841 × 3.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import cv2
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
    for k, (obj, seg, rrv, _) in SEGS.items():
        p, m = load(work, k)
        H, W = p["rv2"].shape
        q = {"reader-v2": p["rv2"], "hecate": p["h"], "fusion": (p["rv2"] + p["h"]) / 2}
        s43 = work / "runs" / rrv / "pred_ink9um_s43.tif"
        if s43.exists():
            q["ink9um_s43_ours"] = tifffile.imread(s43).astype(np.float32) / 255
        d = work / "runs" / "EXP-017" / seg
        for n in ("canon", "ink9um_off", "reader-v3", "argus-v3"):
            f = d / f"pred_{n}.tif"
            if not f.exists():
                continue
            a = tifffile.imread(f).astype(np.float32) / 255
            if a.shape != (H, W):
                a = cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA)
            q[n] = a
        reg = m["valid"] & m["supervision"]
        r = {"object": OBJ[k]}
        for n, x in q.items():
            ev = eval_ink.evaluate(x, m)["in_supervision"]
            r[n] = {"auc": ev["auc_protocol"], "ap": ev["ap"], "ci95_auc": ev["bootstrap"]["ci95"]}
        r["gain_auc_canon_vs_fusion"] = round(r["canon"]["auc"] - r["fusion"]["auc"], 4)
        r["gain_ap_ci95_vs_fusion"] = exp013.paired_ci({n: q[n] for n in q if n != "ink9um_s43_ours"}, "fusion",
                                                       m["inklabels"], reg, rng)
        if "ink9um_off" in q and "ink9um_s43_ours" in q:
            v = m["valid"]
            r["pearson_ink9um_off_vs_ours"] = round(float(np.corrcoef(q["ink9um_off"][v], q["ink9um_s43_ours"][v])[0, 1]), 4)
        res[k] = r
        print(k, {n: (r[n]["auc"], r[n]["ap"]) for n in q}, r.get("pearson_ink9um_off_vs_ours"), flush=True)
    k841 = [k for k in SEGS if OBJ[k] == "0841"]
    res["gain_auc_canon_vs_fusion_0841"] = round(float(np.mean([res[k]["gain_auc_canon_vs_fusion"] for k in k841])), 4)
    res["verdict_H016"] = "soutenue" if res["gain_auc_canon_vs_fusion_0841"] >= 0.02 else "réfutée"
    print(res["gain_auc_canon_vs_fusion_0841"], res["verdict_H016"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
