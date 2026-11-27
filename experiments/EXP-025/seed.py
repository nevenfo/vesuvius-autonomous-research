"""EXP-025 — graine automatique dans la prédiction de surface officielle (protocole du README, étape 1).

Usage : python experiments/EXP-025/seed.py <surface_pred_zarr_url> <out.json> [<ct_zarr_url>]
Avec <ct_zarr_url> (écart documenté, essai 2) : la graine doit aussi être dans le CT (> 0) aux niveaux 3 et 0.
Sortie : graine niveau 0 (x, y, z) + traces du choix.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import zarr
from scipy import ndimage as ndi


def main(url: str, out: str, ct: str | None = None) -> None:
    l3 = zarr.open_array(url.rstrip("/") + "/3", mode="r")
    zc = l3.shape[0] // 2
    sl = np.asarray(l3[zc]).astype(np.float32)
    surf = sl > 0
    ct3 = None
    if ct:
        ct3 = np.asarray(zarr.open_array(ct.rstrip("/") + "/3", mode="r")[zc]) > 0
        sl = sl * ndi.binary_erosion(ct3, iterations=2)
        surf = sl > 0
    ys, xs = np.nonzero(surf)
    cy, cx = ys.mean(), xs.mean()
    r = np.hypot(ys - cy, xs - cx)
    rmax = np.percentile(r, 99)
    support = ndi.uniform_filter(sl, 5)
    cand = np.flatnonzero((r >= 0.4 * rmax) & (r <= 0.7 * rmax))
    sc = support[ys[cand], xs[cand]]
    best = cand[sc >= np.percentile(sc, 99)]
    pick = int(np.random.default_rng(0).choice(best))
    y3, x3 = int(ys[pick]), int(xs[pick])
    z0, y0, x0 = zc * 8 + 4, y3 * 8 + 4, x3 * 8 + 4
    l0 = zarr.open_array(url.rstrip("/") + "/0", mode="r")
    w = 8
    sub = np.asarray(l0[z0 - w:z0 + w + 1, y0 - w:y0 + w + 1, x0 - w:x0 + w + 1]).astype(np.float32)
    ctv = None
    if ct:
        c0 = np.asarray(zarr.open_array(ct.rstrip("/") + "/0", mode="r")[z0 - w:z0 + w + 1, y0 - w:y0 + w + 1, x0 - w:x0 + w + 1])
        sub = sub * (c0 > 0)
        ctv = c0
    dz, dy, dx = np.unravel_index(int(np.argmax(sub)), sub.shape)
    seed = {"x": x0 - w + int(dx), "y": y0 - w + int(dy), "z": z0 - w + int(dz)}
    res = {"seed_level0_xyz": [seed["x"], seed["y"], seed["z"]], "seed_pred_value": float(sub.max()),
           "seed_ct_value": None if ctv is None else int(ctv[dz, dy, dx]),
           "pred_in_ct_frac_level3": None if ct3 is None else round(float(((l3_raw := np.asarray(l3[zc])) > 0)[ct3].sum() / max((l3_raw > 0).sum(), 1)), 4),
           "level3_slice_z": int(zc), "center_level3_yx": [round(float(cy), 1), round(float(cx), 1)],
           "rmax_level3": round(float(rmax), 1), "radius_frac": round(float(r[pick] / rmax), 3),
           "n_candidates": int(len(cand)), "n_best": int(len(best))}
    print(res)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
