"""EXP-010 — B3.2 : audit de la chaîne tuiles / Brier / ρ partiel d'EXP-007 et EXP-009 (PHerc0841).

Usage : PYTHONPATH=src python experiments/EXP-010/audit.py <work_dir> <out.json>
1. Contrôle positif : indicateur synthétique I = résidu de rang du Brier (contrôles p̄, prévalence, E[p(1−p)]) normalisé
   + k·N(0,1) ; ρ partiel attendu ≈ 1/√(1+k²). La chaîne doit le retrouver à ±0,05.
2. Seuil nul / puissance : les cartes d'indicateurs (entropie, désaccord Hecate, variation des normales) sont décalées
   toroïdalement (≥ 8 tuiles en y et x) avant tuilage → paires indicateur/erreur rompues, autocorrélation spatiale
   conservée ; quantile 95 % de |ρ partiel| sur N_NULL décalages = ρ minimal détectable à α = 5 % par segment.
Tuilage vectorisé, mêmes règles qu'EXP-007 (64 px, supervision ≥ 50 %).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
import tifffile
from scipy.stats import rankdata

import importlib.util

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, exp: str):
    sys.path.insert(0, str(ROOT / exp))  # EXP-009 importe `analyze` d'EXP-007 par ce chemin
    spec = importlib.util.spec_from_file_location(name, ROOT / exp / "analyze.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_e7 = _load("analyze", "EXP-007")
sys.modules["analyze"] = _e7
_e9 = _load("exp009_analyze", "EXP-009")
SEGS, partial_rho, prob, geometry = _e7.SEGS, _e7.partial_rho, _e7.prob, _e9.geometry

from vesres import eval_ink  # noqa: E402

TILE, MIN_COV, STEP, N_NULL, MIN_SHIFT = 64, 0.5, 20, 200, 8
KS = (0.0, 0.5, 1.0, 2.0, 3.0)


def tile_means(v: np.ndarray, reg: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    H, W = (s // TILE * TILE for s in v.shape)
    sh = (H // TILE, TILE, W // TILE, TILE)
    r, vv = reg[:H, :W].reshape(sh), v[:H, :W].reshape(sh)
    ok = r & np.isfinite(vv)
    n = ok.sum((1, 3))
    x = np.where(ok, vv, 0).sum((1, 3)) / np.maximum(n, 1)
    return np.where(n > 0, x, np.nan), r.mean((1, 3))


def rank_resid(y, covs):
    C = np.column_stack([np.ones(len(y)), *[rankdata(c) for c in covs]])
    ry = rankdata(y)
    return ry - C @ np.linalg.lstsq(C, ry, rcond=None)[0]


def main(work: Path, out: Path) -> None:
    rng = np.random.default_rng(0)
    res = {}
    for seg, rel in SEGS.items():
        sd = work / "cache" / "segments" / "PHerc0841" / seg
        r2 = prob(tifffile.imread(work / "runs" / rel / "pred_reader-v2.tif"))
        he = prob(tifffile.imread(work / "runs" / "E1.4" / seg / "pred_hecate.tif"))
        H, W = r2.shape
        m = eval_ink.load_segment_masks(sd, r2.shape)
        reg, ink = m["valid"] & m["supervision"], m["inklabels"].astype(np.float32)
        p = np.clip(r2, 1e-6, 1 - 1e-6)
        nv = cv2.resize(geometry(sd / "tifxyz_9.366")["normal_var"].astype(np.float32), (W, H),
                        interpolation=cv2.INTER_NEAREST)
        base = {"brier": (r2 - ink) ** 2, "mean_p": r2, "prevalence": ink, "exp_brier": r2 * (1 - r2)}
        ind = {"entropy": -(p * np.log2(p) + (1 - p) * np.log2(1 - p)), "dis_hecate": np.abs(r2 - he),
               "normal_var": nv}
        cov, keep = tile_means(base["brier"], reg)
        keep = keep >= MIN_COV
        t = {k: tile_means(v, reg)[0][keep] for k, v in base.items()}
        covs = [t["mean_p"], t["prevalence"], t["exp_brier"]]
        r = {"n_tiles": int(keep.sum()), "positive_control": {}, "null_q95_abs_partial": {}, "observed_partial": {}}
        # 1. contrôle positif
        e = rank_resid(t["brier"], covs)
        e /= e.std()
        for k in KS:
            vals = [partial_rho(e + k * rng.standard_normal(len(e)), t["brier"], covs) for _ in range(50)]
            r["positive_control"][str(k)] = {"expected": round(1 / np.sqrt(1 + k * k), 3),
                                             "mean": round(float(np.mean(vals)), 3), "sd": round(float(np.std(vals)), 3)}
        # 2. seuil nul par décalages toroïdaux
        gy, gx = keep.shape
        for name, v in ind.items():
            r["observed_partial"][name] = round(partial_rho(tile_means(v, reg)[0][keep], t["brier"], covs), 3)
            null = []
            for _ in range(N_NULL):
                dy = int(rng.integers(MIN_SHIFT, gy - MIN_SHIFT)) * TILE
                dx = int(rng.integers(MIN_SHIFT, gx - MIN_SHIFT)) * TILE
                vs = np.roll(v, (dy, dx), (0, 1))
                x = tile_means(vs, reg)[0][keep]
                ok = np.isfinite(x)
                if ok.sum() > 30:
                    null.append(abs(partial_rho(x[ok], t["brier"][ok], [c[ok] for c in covs])))
            r["null_q95_abs_partial"][name] = round(float(np.quantile(null, 0.95)), 3)
        res[seg] = r
        print(seg[:14], json.dumps(r), flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
