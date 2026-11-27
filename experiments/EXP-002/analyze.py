"""EXP-002 — H-003 (fusion moyenne reader-v2 + ink_9um) et H-008 (région validation des labels PHerc0841).

Usage : PYTHONPATH=src python experiments/EXP-002/analyze.py <work_dir> <out.json>
<work_dir> = $VESRES_WORK (prédictions de EXP-001/E1 et segments en cache).

H-008, test : dans la zone « validation \\ supervision », les pixels non étiquetés à score élevé (top 5 % reader-v2)
sont-ils aussi élevés pour ink_9um (modèle indépendant, entraîné sans 0841) plus souvent que dans la zone
supervision, où les labels sont réputés complets ? Un taux d'accord nettement supérieur suggère de l'encre non
étiquetée (labels incomplets) plutôt que des faux positifs propres à un modèle.
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


def main(work: Path, out: Path) -> None:
    res = {}
    for seg, rel in SEGS.items():
        a = tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif").astype(np.float32)
        b = tifffile.imread(work / "runs" / rel / "pred_ink9um_s43.tif").astype(np.float32)
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / "PHerc0841" / seg, a.shape)
        valid, ink = m["valid"], m["inklabels"]
        sup = valid & m["supervision"]
        valonly = valid & m["validation"] & ~m["supervision"]
        fused = (a + b) / 2
        r = {"fusion_mean": {k: v.get("auc_protocol") for k, v in eval_ink.evaluate(fused, m).items()},
             "fusion_mean_ap": {k: v.get("ap") for k, v in eval_ink.evaluate(fused, m).items()}}
        # H-008
        thr_a = np.percentile(a[valid], 95)
        thr_b = np.percentile(b[valid], 95)
        stats = {}
        for name, reg in (("supervision", sup), ("validation_only", valonly)):
            unl = reg & ~ink
            hi_a = unl & (a >= thr_a)
            stats[name] = {
                "ink_prevalence": round(float(ink[reg].mean()), 4) if reg.any() else None,
                "unlabeled_hi_a_frac": round(float(hi_a.sum() / max(unl.sum(), 1)), 4),
                "agree_b_given_hi_a": round(float((hi_a & (b >= thr_b)).sum() / max(hi_a.sum(), 1)), 4),
                "agree_b_base_rate": round(float((unl & (b >= thr_b)).sum() / max(unl.sum(), 1)), 4),
                "agree_b_given_labeled_ink": round(float(((reg & ink) & (b >= thr_b)).sum() / max((reg & ink).sum(), 1)), 4),
            }
        r["h008"] = stats
        res[seg] = r
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
