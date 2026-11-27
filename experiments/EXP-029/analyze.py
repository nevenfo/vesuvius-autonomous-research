"""EXP-029 — analyse préenregistrée (README) des cartes d'encre figées sur le patch PHerc1218.

Usage : python analyze.py <run_dir> <results.json>
Lit <run_dir>/seg/sv.zarr, pred_lo.tif, pred_i9.tif ; écrit les agrégats dans results.json (versionné) et les zones
candidates + aperçus dans <run_dir>/private/ (jamais versionné).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
import zarr
from scipy import ndimage
from scipy.stats import spearmanr

B = 64            # bloc (px) pour les corrélations
PX_MM = 0.00864   # mm par pixel (scale 1, niveau 0)


def load_pred(p: Path, shape) -> np.ndarray:
    a = tifffile.imread(p).astype(np.float32)
    a = np.squeeze(a)
    if a.max() > 1.5:
        a /= 255.0 if a.max() <= 255 else 65535.0
    if a.shape != shape:  # sortie sous-échantillonnée éventuelle : remise à l'échelle au plus proche
        zy, zx = shape[0] / a.shape[0], shape[1] / a.shape[1]
        a = ndimage.zoom(a, (zy, zx), order=0)[: shape[0], : shape[1]]
    return a


def blocks(a: np.ndarray, valid: np.ndarray) -> np.ndarray:
    h, w = (a.shape[0] // B) * B, (a.shape[1] // B) * B
    av = a[:h, :w].reshape(h // B, B, w // B, B).mean((1, 3))
    vv = valid[:h, :w].reshape(h // B, B, w // B, B).mean((1, 3))
    return np.where(vv >= 0.99, av, np.nan)


def rho(x: np.ndarray, y: np.ndarray) -> float:
    m = np.isfinite(x) & np.isfinite(y)
    return float(spearmanr(x[m], y[m]).statistic)


def main(run: Path, out: Path) -> None:
    sv = np.asarray(zarr.open(str(run / "seg" / "sv.zarr"), mode="r")["0"])
    n = sv.shape[0]
    valid = sv.max(0) > 0
    inten = sv[n // 2 - 3 : n // 2 + 4].astype(np.float32).mean(0)
    med = [float(np.median(sv[i][valid])) for i in range(n)]
    orient_ok = abs(int(np.argmax(med)) - n // 2) <= 3

    preds = {k: load_pred(run / f"pred_{k}.tif", valid.shape) for k in ("lo", "i9")}
    edge = ndimage.distance_transform_edt(valid) * PX_MM  # mm au bord du masque valide
    res: dict = {"layers": n, "shape": list(valid.shape), "valid_frac": round(float(valid.mean()), 4),
                 "orientation": {"median_by_layer_argmax": int(np.argmax(med)), "center": n // 2, "ok": orient_ok}}

    bi, be = blocks(inten, valid), blocks(edge, valid)
    bp = {k: blocks(v, valid) for k, v in preds.items()}
    for k, v in preds.items():
        q = np.percentile(v[valid], [50, 95, 99])
        res[k] = {"p50": round(float(q[0]), 4), "p95": round(float(q[1]), 4), "p99": round(float(q[2]), 4),
                  "rho_intensity": round(rho(bp[k], bi), 3), "rho_edge": round(rho(bp[k], be), 3)}

    r_obs = rho(bp["lo"], bp["i9"])
    rng = np.random.default_rng(0)
    nb = bp["i9"].shape
    min_sh = int(np.ceil(200 / B))
    null = []
    for _ in range(100):
        sy, sx = (int(rng.integers(min_sh, s - min_sh)) for s in nb)
        null.append(rho(bp["lo"], np.roll(bp["i9"], (sy, sx), (0, 1))))
    p95 = float(np.percentile(null, 95))
    res["agreement"] = {"rho_lo_i9": round(r_obs, 3), "null_p95": round(p95, 3), "null_median": round(float(np.median(null)), 3)}

    # zones candidates : p99 de la carte moyenne, >= 0,25 mm², hors 1 mm du bord, présentes dans les deux modèles
    mean = (preds["lo"] + preds["i9"]) / 2
    thr = np.percentile(mean[valid], 99)
    core = valid & (edge > 1.0)
    lab, nl = ndimage.label((mean > thr) & core)
    min_px = 0.25 / PX_MM**2
    t_lo, t_i9 = (np.percentile(preds[k][valid], 95) for k in ("lo", "i9"))
    zones = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i
        if m.sum() < min_px:
            continue
        both = bool(np.median(preds["lo"][sl][m]) > t_lo and np.median(preds["i9"][sl][m]) > t_i9)
        if both:
            zones.append({"y0": sl[0].start, "y1": sl[0].stop, "x0": sl[1].start, "x1": sl[1].stop,
                          "area_mm2": round(float(m.sum() * PX_MM**2), 3),
                          "mean_prob": round(float(mean[sl][m].mean()), 3)})
    priv = run / "private"
    priv.mkdir(exist_ok=True)
    (priv / "zones.json").write_text(json.dumps(zones, indent=1))
    for k, v in {**preds, "mean": mean}.items():
        tifffile.imwrite(priv / f"{k}_u8.tif", (np.clip(v, 0, 1) * 255).astype(np.uint8))
    tifffile.imwrite(priv / "intensity_u8.tif", np.clip(inten, 0, 255).astype(np.uint8))
    res["candidates"] = {"n_zones": len(zones), "total_area_mm2": round(sum(z["area_mm2"] for z in zones), 3),
                         "threshold_mean_p99": round(float(thr), 4)}

    sup = r_obs > p95 and all(abs(res[k]["rho_intensity"]) < 0.5 for k in ("lo", "i9"))
    res["H-034"] = "soutenue" if sup else "réfutée"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
