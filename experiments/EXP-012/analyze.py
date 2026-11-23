"""EXP-012 — H-011 : calibration (ECE 15 bins, fiabilité) de reader-v2, Hecate et fusion en région supervision.

Usage : PYTHONPATH=src python experiments/EXP-012/analyze.py <work_dir> <out.json>
Prédictions existantes (uint8 0–255 → p = x/255) : reader-v2 (koine infer), Hecate (hecate_run.py), fusion moyenne.
Critère fixé avant (EXP-010) : H-011 réfutée si ECE(reader-v2) > 0,10 sur ≥ 2 objets ; soutenue si ≤ 0,05 partout.
Échelle : ECE pixel-pondérée, 15 bins de largeur égale sur [0, 1] ; on rapporte aussi la prévalence vs p moyen
(biais global) et l'ECE après recalibration isotone en validation croisée 2 plis en damier de blocs 256 px (borne
de ce qu'une simple recalibration monotone pourrait corriger).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from sklearn.isotonic import IsotonicRegression

from vesres import eval_ink

SEGS = {  # objet, segment, chemin reader-v2 relatif à runs/, chemin Hecate relatif à runs/
    "0841_w00": ("PHerc0841", "20260220213127-w00", "EXP-001", "E1.4/20260220213127-w00"),
    "0841_144552": ("PHerc0841", "20260220214732-auto_grown_20260220144552896",
                    "E1/20260220214732-auto_grown_20260220144552896", "E1.4/20260220214732-auto_grown_20260220144552896"),
    "0841_174252": ("PHerc0841", "20260221022814-auto_grown_20260220174252405",
                    "E1/20260221022814-auto_grown_20260220174252405", "E1.4/20260221022814-auto_grown_20260220174252405"),
    "0009B": ("PHerc0009B", "20250919125754-auto_grown_20250919055754487_inp_hr", "EXP-004",
              "EXP-004/20250919125754-auto_grown_20250919055754487_inp_hr"),
    "0500P2": ("PHerc0500P2", "20250825181859--1", "EXP-008", "EXP-008/20250825181859--1"),
}
NB = 15


def ece(p: np.ndarray, y: np.ndarray) -> tuple[float, list]:
    b = np.minimum((p * NB).astype(int), NB - 1)
    n = np.bincount(b, minlength=NB)
    sp = np.bincount(b, weights=p, minlength=NB)
    sy = np.bincount(b, weights=y, minlength=NB)
    nz = n > 0
    e = float(np.sum(np.abs(sp[nz] - sy[nz])) / len(p))
    curve = [[i, int(n[i]), round(float(sp[i] / n[i]), 4), round(float(sy[i] / n[i]), 4)] for i in range(NB) if n[i]]
    return round(e, 4), curve


def iso_cv_ece(p2d: np.ndarray, y2d: np.ndarray, reg: np.ndarray) -> float:
    yy, xx = np.indices(reg.shape)
    chk = ((yy // 256 + xx // 256) % 2).astype(bool)
    halves = [~chk, chk]
    ps, ys = [], []
    for tr, te in ((0, 1), (1, 0)):
        a, b = reg & halves[tr], reg & halves[te]
        iso = IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip").fit(p2d[a], y2d[a])
        ps.append(iso.predict(p2d[b]))
        ys.append(y2d[b])
    return ece(np.concatenate(ps), np.concatenate(ys))[0]


def main(work: Path, out: Path) -> None:
    res = {}
    for k, (obj, seg, rrv, rh) in SEGS.items():
        p = {"reader-v2": tifffile.imread(work / "runs" / rrv / "pred_reader-v2.tif"),
             "hecate": tifffile.imread(work / "runs" / rh / "pred_hecate.tif")}
        assert all(v.dtype == np.uint8 for v in p.values()), {n: v.dtype for n, v in p.items()}
        p = {n: v.astype(np.float32) / 255 for n, v in p.items()}
        p["fusion_rv2_hecate"] = (p["reader-v2"] + p["hecate"]) / 2
        m = eval_ink.load_segment_masks(work / "cache" / "segments" / obj / seg, p["reader-v2"].shape)
        reg = m["valid"] & m["supervision"]
        y = m["inklabels"].astype(np.float32)
        r = {"prevalence": round(float(y[reg].mean()), 4), "n": int(reg.sum())}
        for n, x in p.items():
            e, curve = ece(x[reg], y[reg])
            r[n] = {"ece": e, "mean_p": round(float(x[reg].mean()), 4), "ece_isotonic_cv": iso_cv_ece(x, y, reg),
                    "reliability": curve}
        res[k] = r
        print(k, r["prevalence"], {n: (r[n]["ece"], r[n]["mean_p"], r[n]["ece_isotonic_cv"]) for n in p}, flush=True)
    objs = {"0841": [k for k in res if k.startswith("0841")], "0009B": ["0009B"], "0500P2": ["0500P2"]}
    per_obj = {o: round(float(np.mean([res[k]["reader-v2"]["ece"] for k in ks])), 4) for o, ks in objs.items()}
    res["reader-v2_ece_per_object"] = per_obj
    n_bad = sum(v > 0.10 for v in per_obj.values())
    res["verdict_H011"] = ("réfutée" if n_bad >= 2 else "soutenue" if all(v <= 0.05 for v in per_obj.values())
                           else "indéterminée (0,05 < ECE ≤ 0,10 ou 1 seul objet > 0,10)")
    print(per_obj, res["verdict_H011"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
