r"""EXP-005 — H-008b : l'accord inter-modèles sur les détections non étiquetées de la zone `validation \ supervision`
(PHerc0841) persiste-t-il avec Hecate (pipeline et tête 3D distincts) comme 2e modèle ?

Usage : PYTHONPATH=src python experiments/EXP-005/analyze.py <work_dir> <out.json>
Même statistique qu'EXP-002 (top 5 % des pixels valides par modèle) ; paires : reader-v2→Hecate, Hecate→reader-v2,
reader-v2→ink_9um (rappel EXP-002) et accord triple.
Contrôle d'effet de bord : régions `*_far` = pixels à plus de FAR_PX px (grille 9,366 µm) de toute encre étiquetée.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile

import cv2

from vesres import eval_ink

FAR_PX = 8  # ≈ 75 µm

SEGS = {
    "20260220213127-w00": "EXP-001",
    "20260220214732-auto_grown_20260220144552896": "E1/20260220214732-auto_grown_20260220144552896",
    "20260221022814-auto_grown_20260220174252405": "E1/20260221022814-auto_grown_20260220174252405",
}


def agree(a: np.ndarray, b: np.ndarray, valid, ink, reg) -> dict:
    hi_a, hi_b = a >= np.percentile(a[valid], 95), b >= np.percentile(b[valid], 95)
    unl = reg & ~ink
    ha = unl & hi_a
    base = float((unl & hi_b).sum() / max(unl.sum(), 1))
    g = float((ha & hi_b).sum() / max(ha.sum(), 1))
    return {"unlabeled_hi_a_frac": round(float(ha.sum() / max(unl.sum(), 1)), 4), "agree_b_given_hi_a": round(g, 4),
            "agree_b_base_rate": round(base, 4), "lift": round(g / base, 2) if base else None,
            "agree_b_given_labeled_ink": round(float((reg & ink & hi_b).sum() / max((reg & ink).sum(), 1)), 4)}


def main(work: Path, out: Path) -> None:
    res = {}
    for seg, rel in SEGS.items():
        r2 = tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif").astype(np.float32)
        i9 = tifffile.imread(work / "runs" / rel / "pred_ink9um_s43.tif").astype(np.float32)
        he = tifffile.imread(work / "runs" / "E1.4" / seg / "pred_hecate.tif").astype(np.float32)
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / "PHerc0841" / seg, r2.shape)
        valid, ink = m["valid"], m["inklabels"]
        far = cv2.distanceTransform((~ink).astype(np.uint8), cv2.DIST_L2, 5) > FAR_PX
        sup, val = valid & m["supervision"], valid & m["validation"] & ~m["supervision"]
        regs = {"supervision": sup, "validation_only": val, "supervision_far": sup & far, "validation_only_far": val & far}
        r = {}
        for name, reg in regs.items():
            hi = {k: x >= np.percentile(x[valid], 95) for k, x in (("r2", r2), ("he", he), ("i9", i9))}
            unl = reg & ~ink
            trip = unl & hi["r2"] & hi["he"] & hi["i9"]
            r[name] = {"rv2_to_hecate": agree(r2, he, valid, ink, reg), "hecate_to_rv2": agree(he, r2, valid, ink, reg),
                       "rv2_to_ink9um": agree(r2, i9, valid, ink, reg),
                       "triple_frac_of_unlabeled": round(float(trip.sum() / max(unl.sum(), 1)), 5),
                       "triple_expected_indep": round(0.05 ** 3, 5), "n_unlabeled": int(unl.sum())}
        res[seg] = r
        print(seg[:14], json.dumps({n: {k: (v["agree_b_given_hi_a"], v["agree_b_base_rate"], v["lift"])
                                        for k, v in x.items() if isinstance(v, dict)} | {"triple": x["triple_frac_of_unlabeled"]}
                                    for n, x in r.items()}), flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
