"""EXP-013 — H-014 : fusion reader-v2+Hecate calibrée (isotone LOO objet) ou par rangs vs fusion moyenne brute.

Usage : PYTHONPATH=src python experiments/EXP-013/analyze.py <work_dir> <out.json>
Prédictions et segments : ceux d'EXP-012 (0841 × 3, 0009B, 0500P2), uint8 → p = x/255.
- raw    : (p_rv2 + p_h) / 2 (EXP-011).
- iso    : moyenne de f_rv2(p_rv2) et f_h(p_h), f isotone apprise sur les pixels supervision des AUTRES objets
           (1 M px tirés par segment ; l'objet testé n'intervient jamais dans l'ajustement).
- rank   : moyenne des rangs normalisés de chaque modèle sur les pixels valides du segment (sans label).
Critère fixé avant : H-014 réfutée si le gain AP moyen (meilleure variante − raw, moyenne des 3 objets, 0841 moyenné
sur ses 3 segments) < 0,01. IC95 apparié du gain par bootstrap de blocs 256 px par segment.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from scipy.stats import rankdata
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import average_precision_score

from vesres import eval_ink

_spec = importlib.util.spec_from_file_location("exp012", Path(__file__).parents[1] / "EXP-012" / "analyze.py")
exp012 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exp012)
SEGS, ece = exp012.SEGS, exp012.ece
OBJ = {k: k.split("_")[0] for k in SEGS}
N_FIT = 1_000_000


def load(work: Path, k: str):
    obj, seg, rrv, rh = SEGS[k]
    p = {"rv2": tifffile.imread(work / "runs" / rrv / "pred_reader-v2.tif").astype(np.float32) / 255,
         "h": tifffile.imread(work / "runs" / rh / "pred_hecate.tif").astype(np.float32) / 255}
    m = eval_ink.load_segment_masks(work / "cache" / "segments" / obj / seg, p["rv2"].shape)
    return p, m


def paired_ci(p: dict, base: str, ink, reg, rng, block=256, per_block=2000, n_boot=200) -> dict:
    h, w = reg.shape
    blocks = []
    for y in range(0, h, block):
        for x in range(0, w, block):
            idx = np.flatnonzero(reg[y:y + block, x:x + block])
            if len(idx) < 50:
                continue
            if len(idx) > per_block:
                idx = rng.choice(idx, per_block, replace=False)
            blocks.append({k: v[y:y + block, x:x + block].ravel()[idx] for k, v in {**p, "_y": ink}.items()})
    g = {k: [] for k in p if k != base}
    for _ in range(n_boot):
        pick = rng.integers(0, len(blocks), len(blocks))
        l = np.concatenate([blocks[i]["_y"] for i in pick])
        if l.all() or not l.any():
            continue
        ap = {k: average_precision_score(l, np.concatenate([blocks[i][k] for i in pick])) for k in p}
        for k in g:
            g[k].append(ap[k] - ap[base])
    return {k: [round(float(x), 4) for x in np.percentile(v, [2.5, 97.5])] for k, v in g.items()}


def main(work: Path, out: Path) -> None:
    rng = np.random.default_rng(0)
    fit = {}  # segment -> (p_rv2, p_h, y) échantillon supervision
    for k in SEGS:
        p, m = load(work, k)
        reg = np.flatnonzero(m["valid"] & m["supervision"])
        idx = rng.choice(reg, min(N_FIT, len(reg)), replace=False)
        fit[k] = (p["rv2"].ravel()[idx], p["h"].ravel()[idx], m["inklabels"].ravel()[idx].astype(np.float32))
        print("fit sample", k, len(idx), flush=True)
    res = {}
    for k in SEGS:
        others = [s for s in SEGS if OBJ[s] != OBJ[k]]
        y_o = np.concatenate([fit[s][2] for s in others])
        f = {n: IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip").fit(
            np.concatenate([fit[s][j] for s in others]), y_o) for j, n in ((0, "rv2"), (1, "h"))}
        p, m = load(work, k)
        v, reg, ink = m["valid"], m["valid"] & m["supervision"], m["inklabels"]
        cal = {n: f[n].predict(p[n].ravel()).reshape(p[n].shape).astype(np.float32) for n in p}
        rk = {}
        for n in p:
            r = np.zeros(p[n].shape, np.float32)
            r[v] = rankdata(p[n][v]) / v.sum()
            rk[n] = r
        q = {"raw": (p["rv2"] + p["h"]) / 2, "iso": (cal["rv2"] + cal["h"]) / 2, "rank": (rk["rv2"] + rk["h"]) / 2}
        r = {"object": OBJ[k], "fit_on": others}
        for n, x in q.items():
            ev = eval_ink.evaluate(x, m)["in_supervision"]
            r[n] = {"auc": ev["auc_protocol"], "ap": ev["ap"], "ece": ece(x[reg], ink[reg].astype(np.float32))[0]}
        r["ece_iso_single"] = {n: ece(cal[n][reg], ink[reg].astype(np.float32))[0] for n in cal}
        r["gain_ap"] = {n: round(r[n]["ap"] - r["raw"]["ap"], 4) for n in ("iso", "rank")}
        r["gain_ap_ci95"] = paired_ci(q, "raw", ink, reg, rng)
        res[k] = r
        print(k, {n: (r[n]["auc"], r[n]["ap"], r[n]["ece"]) for n in q}, r["gain_ap"], r["gain_ap_ci95"], flush=True)
    per_obj = {}
    for o in ("0841", "0009B", "0500P2"):
        ks = [k for k in SEGS if OBJ[k] == o]
        per_obj[o] = {n: round(float(np.mean([res[k]["gain_ap"][n] for k in ks])), 4) for n in ("iso", "rank")}
    mean_gain = {n: round(float(np.mean([per_obj[o][n] for o in per_obj])), 4) for n in ("iso", "rank")}
    res["gain_ap_per_object"], res["gain_ap_mean"] = per_obj, mean_gain
    res["verdict_H014"] = "soutenue" if max(mean_gain.values()) >= 0.01 else "réfutée"
    print(per_obj, mean_gain, res["verdict_H014"])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
