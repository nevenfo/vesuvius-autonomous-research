"""EXP-022 — chemin de lecture v0 : lisibilité au niveau glyphe (UGR) et couverture des références.

Usage : PYTHONPATH=src python experiments/EXP-022/analyze.py <work_dir> <out_public.json> <out_private.json>
Public = agrégats par segment/objet ; privé (hors Git) = enregistrements par UGR avec boîtes (positions de texte).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import tifffile

from vesres import reading

_spec = importlib.util.spec_from_file_location("exp013", Path(__file__).parents[1] / "EXP-013" / "analyze.py")
exp013 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exp013)
SEGS, OBJ, load = exp013.SEGS, exp013.OBJ, exp013.load
THR_MAIN, THR_ALT = 0.90, 0.80


def chains(work: Path, k: str, p: dict, shape) -> dict:
    seg = SEGS[k][1]
    q = {"reader-v2": p["rv2"], "hecate": p["h"], "fusion_rv2_h": (p["rv2"] + p["h"]) / 2}
    lo = work / "runs" / "EXP-018" / "eval" / seg / "pred_lo.tif"
    if lo.exists():
        q["lo"] = tifffile.imread(lo).astype(np.float32) / 255
        q["fusion_lo_h"] = (q["lo"] + p["h"]) / 2
    for nm in ("canon", "reader-v3", "argus-v3"):
        f = work / "runs" / "EXP-017" / seg / f"pred_{nm}.tif"
        if f.exists():
            a = tifffile.imread(f)
            a = a.astype(np.float32) / (65535 if a.dtype == np.uint16 else 255)
            if a.shape != shape:
                a = cv2.resize(a, (shape[1], shape[0]), interpolation=cv2.INTER_AREA)
            q[nm] = a
    return q


def main(work: Path, out_pub: Path, out_priv: Path) -> None:
    pub, priv = {}, {}
    for k in SEGS:
        p, m = load(work, k)
        valid, ink, sup = m["valid"], m["inklabels"], m["supervision"]
        region = valid & sup
        lab, units = reading.reference_units(ink, valid, sup)
        geoms = reading.unit_geometry(lab, units, ink, region)
        bg = region & ~reading.dilate(ink, 48)
        areas = [int(g["mask"].sum()) for g in geoms]
        amed = float(np.median(areas)) if areas else 0.0
        r = {"object": OBJ[k], "n_units": len(units), "unit_area_px_median": amed,
             "coverage": reading.coverage(valid, sup, m["validation"])}
        q = chains(work, k, p, valid.shape)
        q["control_positive"] = reading.positive_control(ink)
        best = "fusion_lo_h" if "fusion_lo_h" in q else "fusion_rv2_h"
        q["control_negative"] = reading.negative_control(q[best])
        priv[k] = {}
        for n, x in q.items():
            recs = reading.score_units(x, geoms)
            aucs = [a["local_auc"] for a in recs if a["local_auc"] is not None]
            r[n] = {"legible_090": reading.legible_fraction(recs, THR_MAIN),
                    "legible_080": reading.legible_fraction(recs, THR_ALT),
                    "local_auc_median": round(float(np.median(aucs)), 4) if aucs else None,
                    "n_scored": len(aucs)}
            if not n.startswith("control"):
                r[n]["bg_candidates"] = reading.background_candidates(x, ink, region, 0.5,
                                                                      (int(0.25 * amed), int(4 * amed)), bg=bg)
            priv[k][n] = recs
        pub[k] = r
        print(k, len(units), {n: (r[n]["legible_090"], r[n]["local_auc_median"]) for n in q}, flush=True)
    agg = {}
    for obj in sorted({OBJ[k] for k in SEGS}):
        ks = [k for k in SEGS if OBJ[k] == obj]
        names = set.intersection(*[set(priv[k]) for k in ks])
        agg[obj] = {}
        for n in sorted(names):
            a = [u["local_auc"] for k in ks for u in priv[k][n] if u["local_auc"] is not None]
            agg[obj][n] = {"n_units": len(a),
                           "legible_090": round(float(np.mean([x >= THR_MAIN for x in a])), 4) if a else None,
                           "legible_080": round(float(np.mean([x >= THR_ALT for x in a])), 4) if a else None}
    pub["by_object"] = agg

    def allu(n):
        return [u["local_auc"] for k in SEGS for u in priv[k].get(n, []) if u["local_auc"] is not None]

    pos, neg = allu("control_positive"), allu("control_negative")
    h026 = {"positive_legible": round(float(np.mean([x >= THR_MAIN for x in pos])), 4),
            "negative_legible": round(float(np.mean([x >= THR_MAIN for x in neg])), 4)}
    h026["verdict"] = "soutenue" if h026["positive_legible"] >= 0.95 and h026["negative_legible"] <= 0.20 else "réfutée"
    pub["H026"] = h026
    v = agg["0841"].get("fusion_lo_h", {}).get("legible_090")
    pub["H027"] = {"fusion_lo_h_0841_legible_090": v,
                   "verdict": None if v is None else ("soutenue" if v >= 0.70 else "réfutée")}
    print(pub["H026"], pub["H027"])
    out_pub.parent.mkdir(parents=True, exist_ok=True)
    out_pub.write_text(json.dumps(pub, indent=1, ensure_ascii=False), encoding="utf-8")
    out_priv.parent.mkdir(parents=True, exist_ok=True)
    out_priv.write_text(json.dumps(priv, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
