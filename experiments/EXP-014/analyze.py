"""EXP-014 — H-013 : part de l'erreur due aux bords des labels (bande d'exclusion autour des frontières encre/fond).

Usage : PYTHONPATH=src python experiments/EXP-014/analyze.py <work_dir> <out.json>
Segments/prédictions d'EXP-012 (0841 × 3, 0009B, 0500P2). Bande de largeur r px = dilate(ink, r) & ~erode(ink, r)
(élément structurant carré 3×3 itéré r fois) ; la bande est retirée de la région supervision.
Contrôle : retrait d'un même nombre de pixels tirés au hasard dans la région (ΔAUC attendu ≈ 0).
Critère fixé avant (EXP-010) : H-013 réfutée si ΔAUC sup. à r = 2 < 0,03 pour reader-v2 ou Hecate (moyenne des objets,
0841 moyenné sur ses 3 segments).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

from vesres import eval_ink

_spec = importlib.util.spec_from_file_location("exp013", Path(__file__).parents[1] / "EXP-013" / "analyze.py")
exp013 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exp013)
SEGS, OBJ, load = exp013.SEGS, exp013.OBJ, exp013.load
RADII = (0, 1, 2, 3)
ST = np.ones((3, 3), bool)


def metrics(x: np.ndarray, y: np.ndarray, reg: np.ndarray) -> dict:
    pos, neg = x[reg & y], x[reg & ~y]
    return {"auc": eval_ink.auc_protocol(pos, neg), "ap": eval_ink.pr_metrics(x[reg], y[reg])["ap"]}


def main(work: Path, out: Path) -> None:
    rng = np.random.default_rng(0)
    res = {}
    for k in SEGS:
        p, m = load(work, k)
        q = {"reader-v2": p["rv2"], "hecate": p["h"], "fusion": (p["rv2"] + p["h"]) / 2}
        y, sup = m["inklabels"].astype(bool), m["valid"] & m["supervision"]
        r_out = {"object": OBJ[k]}
        for r in RADII:
            band = (ndimage.binary_dilation(y, ST, r) & ~ndimage.binary_erosion(y, ST, r)) if r else np.zeros_like(y)
            reg = sup & ~band
            e = {"frac_removed": round(float((sup & band).sum() / sup.sum()), 4),
                 "frac_pos_removed": round(float((sup & band & y).sum() / (sup & y).sum()), 4)}
            for n, x in q.items():
                e[n] = metrics(x, y, reg)
            if r:  # contrôle aléatoire de même taille
                idx = np.flatnonzero(sup)
                drop = rng.choice(idx, int((sup & band).sum()), replace=False)
                ctrl = sup.copy()
                ctrl.ravel()[drop] = False
                e["random_ctrl"] = {n: metrics(x, y, ctrl) for n, x in q.items()}
            r_out[f"r{r}"] = e
        for r in RADII[1:]:
            r_out[f"r{r}"]["delta_auc"] = {n: round(r_out[f"r{r}"][n]["auc"] - r_out["r0"][n]["auc"], 4) for n in q}
            r_out[f"r{r}"]["delta_ap"] = {n: round(r_out[f"r{r}"][n]["ap"] - r_out["r0"][n]["ap"], 4) for n in q}
            r_out[f"r{r}"]["delta_auc_ctrl"] = {
                n: round(r_out[f"r{r}"]["random_ctrl"][n]["auc"] - r_out["r0"][n]["auc"], 4) for n in q}
        res[k] = r_out
        print(k, {f"r{r}": (r_out[f"r{r}"]["frac_removed"], r_out[f"r{r}"]["delta_auc"],
                            r_out[f"r{r}"]["delta_auc_ctrl"]["reader-v2"]) for r in RADII[1:]}, flush=True)
    summ = {}
    for r in RADII[1:]:
        per_obj = {}
        for o in ("0841", "0009B", "0500P2"):
            ks = [k for k in SEGS if OBJ[k] == o]
            per_obj[o] = {n: round(float(np.mean([res[k][f"r{r}"]["delta_auc"][n] for k in ks])), 4)
                          for n in ("reader-v2", "hecate", "fusion")}
        summ[f"r{r}"] = {"per_object": per_obj, "mean": {n: round(float(np.mean([v[n] for v in per_obj.values()])), 4)
                                                        for n in ("reader-v2", "hecate", "fusion")}}
    res["delta_auc_summary"] = summ
    m2 = summ["r2"]["mean"]
    res["verdict_H013"] = "soutenue" if min(m2["reader-v2"], m2["hecate"]) >= 0.03 else "réfutée"
    print(json.dumps(summ), res["verdict_H013"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
