"""EXP-008 — H-002 : avantage « objet vu » de reader-v2 sur ink_9um (différence de différences).

Usage : PYTHONPATH=src python experiments/EXP-008/analyze.py <work_dir> <out.json>
Écart Δ = AUC_sup(reader-v2) − AUC_sup(ink_9um s43) par segment.
- Objets vus par reader-v2 seul (segments eux-mêmes tenus à l'écart) : PHerc0500P2 `20250825181859--1` (ce run),
  PHerc0009B (EXP-004).
- Objet vu par aucun des deux : PHerc0841 × 3 segments (EXP-001/E1).
DiD = moyenne Δ(vus) − moyenne Δ(0841). Mêmes masques, même protocole (`vesres.eval_ink`).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile

from vesres import eval_ink

SEGS = {  # (objet, segment, dossier des prédictions relatif à runs/, groupe)
    "0500P2": ("PHerc0500P2", "20250825181859--1", "EXP-008", "seen_rv2"),
    "0009B": ("PHerc0009B", "20250919125754-auto_grown_20250919055754487_inp_hr", "EXP-004", "seen_rv2"),
    "0841_w00": ("PHerc0841", "20260220213127-w00", "EXP-001", "unseen"),
    "0841_144552": ("PHerc0841", "20260220214732-auto_grown_20260220144552896",
                    "E1/20260220214732-auto_grown_20260220144552896", "unseen"),
    "0841_174252": ("PHerc0841", "20260221022814-auto_grown_20260220174252405",
                    "E1/20260221022814-auto_grown_20260220174252405", "unseen"),
}


def main(work: Path, out: Path) -> None:
    res = {}
    for k, (obj, seg, rel, grp) in SEGS.items():
        p = {n: tifffile.imread(work / "runs" / rel / f"pred_{n}.tif").astype(np.float32)
             for n in ("reader-v2", "ink9um_s43")}
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / obj / seg, p["reader-v2"].shape)
        sup = m["valid"] & m["supervision"]
        r = {"group": grp, "prevalence_sup": round(float(m["inklabels"][sup].mean()), 4),
             "validation_in_supervision": bool(not (m["validation"] & ~m["supervision"] & m["valid"]).any())}
        for n, x in p.items():
            ev = eval_ink.evaluate(x, m)["in_supervision"]
            r[n] = {"auc": ev["auc_protocol"], "ap": ev.get("ap"), "ci95": ev.get("bootstrap", {}).get("ci95")}
        r["delta_auc"] = round(r["reader-v2"]["auc"] - r["ink9um_s43"]["auc"], 4)
        r["delta_ap"] = round(r["reader-v2"]["ap"] - r["ink9um_s43"]["ap"], 4)
        res[k] = r
        print(k, json.dumps(r), flush=True)
    d = {g: [v["delta_auc"] for v in res.values() if v["group"] == g] for g in ("seen_rv2", "unseen")}
    res["did_auc"] = round(float(np.mean(d["seen_rv2"]) - np.mean(d["unseen"])), 4)
    res["did_auc_0500P2_only"] = round(res["0500P2"]["delta_auc"] - float(np.mean(d["unseen"])), 4)
    res["did_auc_min_seen_minus_max_unseen"] = round(min(d["seen_rv2"]) - max(d["unseen"]), 4)
    print("DiD", res["did_auc"], "0500P2 only", res["did_auc_0500P2_only"],
          "min-max", res["did_auc_min_seen_minus_max_unseen"], flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
