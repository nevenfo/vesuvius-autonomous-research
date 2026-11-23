"""EXP-011 — H-010 : fusion moyenne reader-v2+Hecate sur un 3e objet (PHerc0500P2, segment tenu à l'écart).

Usage : PYTHONPATH=src python experiments/EXP-011/analyze.py <work_dir> <out.json>
Prédictions : runs/EXP-008/pred_{reader-v2,ink9um_s43}.tif (koine infer, EXP-008) et
runs/EXP-008/<seg>/pred_hecate.tif (experiments/EXP-003/hecate_run.py <seg> PHerc0500P2 9.362 runs/EXP-008).
Critère : H-010 réfutée si AP_sup(fusion) − max(AP_sup reader-v2, AP_sup Hecate) < 0,02.
IC95 apparié du gain d'AP par bootstrap de blocs 256 px (mêmes blocs/pixels pour tous les modèles).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from sklearn.metrics import average_precision_score

from vesres import eval_ink

OBJ, SEG = "PHerc0500P2", "20250825181859--1"


def summary(m: dict) -> dict:
    return {k: {"n_pos": v["n_pos"], "auc_protocol": v.get("auc_protocol"), "auc_exact": v.get("auc_exact"),
                "ap": v.get("ap"), "best_f1": v.get("best_f1"), "prevalence": v.get("prevalence"),
                "ci95": v.get("bootstrap", {}).get("ci95")} for k, v in m.items()}


def paired_gain_ci(p: dict, ink: np.ndarray, reg: np.ndarray, block: int = 256, per_block: int = 2000,
                   n_boot: int = 200, seed: int = 0) -> dict:
    """Gain AP fusion − meilleur seul (choisi sur l'estimation ponctuelle), bootstrap apparié par blocs."""
    rng = np.random.default_rng(seed)
    h, w = reg.shape
    blocks = []
    for y in range(0, h, block):
        for x in range(0, w, block):
            m = reg[y:y + block, x:x + block]
            if m.sum() < 50:
                continue
            idx = np.flatnonzero(m)
            if len(idx) > per_block:
                idx = rng.choice(idx, per_block, replace=False)
            blocks.append({k: v[y:y + block, x:x + block].ravel()[idx] for k, v in {**p, "_ink": ink}.items()})
    gains, best = [], None
    for _ in range(n_boot):
        pick = rng.integers(0, len(blocks), len(blocks))
        l = np.concatenate([blocks[i]["_ink"] for i in pick])
        if l.all() or not l.any():
            continue
        ap = {k: average_precision_score(l, np.concatenate([blocks[i][k] for i in pick])) for k in p}
        gains.append(ap["fusion_rv2_hecate"] - max(ap["reader-v2"], ap["hecate"]))
    lo, hi = np.percentile(gains, [2.5, 97.5])
    return {"n_blocks": len(blocks), "n_boot": len(gains), "ci95": [round(float(lo), 4), round(float(hi), 4)],
            "frac_ge_0.02": round(float(np.mean(np.array(gains) >= 0.02)), 3)}


def main(work: Path, out: Path) -> None:
    run = work / "runs" / "EXP-008"
    p = {"reader-v2": tifffile.imread(run / "pred_reader-v2.tif"),
         "ink9um_s43": tifffile.imread(run / "pred_ink9um_s43.tif"),
         "hecate": tifffile.imread(run / SEG / "pred_hecate.tif")}
    dt = {k: str(v.dtype) for k, v in p.items()}
    p = {k: v.astype(np.float32) for k, v in p.items()}
    shape = p["reader-v2"].shape
    assert all(v.shape == shape for v in p.values()), {k: v.shape for k, v in p.items()}
    m = eval_ink.load_segment_masks(work / "cache" / "segments" / OBJ / SEG, shape)
    p["fusion_rv2_hecate"] = (p["reader-v2"] + p["hecate"]) / 2
    p["fusion_all3"] = (p["reader-v2"] + p["hecate"] + p["ink9um_s43"]) / 3
    v = m["valid"]
    sup = v & m["supervision"]
    res = {"object": OBJ, "segment": SEG, "shape": list(shape), "dtypes": dt,
           "pearson_rv2_hecate": round(float(np.corrcoef(p["reader-v2"][v], p["hecate"][v])[0, 1]), 4),
           "models": {k: summary(eval_ink.evaluate(x, m)) for k, x in p.items()}}
    ap = {k: res["models"][k]["in_supervision"]["ap"] for k in ("reader-v2", "hecate", "fusion_rv2_hecate")}
    auc = {k: res["models"][k]["in_supervision"]["auc_protocol"] for k in ap}
    res["gain_ap_sup"] = round(ap["fusion_rv2_hecate"] - max(ap["reader-v2"], ap["hecate"]), 4)
    res["gain_auc_sup"] = round(auc["fusion_rv2_hecate"] - max(auc["reader-v2"], auc["hecate"]), 4)
    res["gain_ap_sup_paired_bootstrap"] = paired_gain_ci(
        {k: p[k] for k in ap}, m["inklabels"], sup)
    res["verdict_H010"] = "soutenue" if res["gain_ap_sup"] >= 0.02 else "réfutée"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    for k, r in res["models"].items():
        print(k, {g: (x["auc_protocol"], x["ap"], x["ci95"]) for g, x in r.items()})
    print("gain AP", res["gain_ap_sup"], "AUC", res["gain_auc_sup"], res["gain_ap_sup_paired_bootstrap"],
          "pearson", res["pearson_rv2_hecate"], res["verdict_H010"])


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
