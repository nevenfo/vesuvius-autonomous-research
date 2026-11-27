"""EXP-031 — graines multiples déterministes dans la prédiction de surface m7, restreintes au CT érodé et à la fenêtre
des normal-grids locales (protocole du README).

Usage : python seeds.py <surface_pred_url> <ct_url> <out.json> <cx> <cy> <cz> <half> <z1,z2,...> <n_per_z> [margin=500] [min_sep=700]
- Fenêtre locale : |x-cx|, |y-cy|, |z-cz| <= half - margin (la croissance reste dans les normal-grids téléchargées).
- Par tranche z (niveau 0) : candidats du niveau 3 dans la prédiction × CT érodé, rayon 40–70 % du rayon max (centre =
  centroïde de la prédiction sur la tranche), support local au p90 ; tirage glouton rng 0 avec séparation >= min_sep
  voxels (niveau 0) entre graines ; recalage niveau 0 sur le maximum de prédiction à ± 8 voxels dans le CT.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import zarr
from scipy import ndimage as ndi


def main(a: list[str]) -> None:
    pred_url, ct_url, out = a[1].rstrip("/"), a[2].rstrip("/"), a[3]
    cx, cy, cz, half = (int(v) for v in a[4:8])
    zs = [int(v) for v in a[8].split(",")]
    n_per = int(a[9])
    margin = int(a[10]) if len(a) > 10 else 500
    min_sep = int(a[11]) if len(a) > 11 else 700
    lim = half - margin
    p3, c3 = zarr.open_array(pred_url + "/3", mode="r"), zarr.open_array(ct_url + "/3", mode="r")
    p0, c0 = zarr.open_array(pred_url + "/0", mode="r"), zarr.open_array(ct_url + "/0", mode="r")
    rng = np.random.default_rng(0)
    seeds: list[dict] = []
    for z in zs:
        assert abs(z - cz) <= lim, (z, cz, lim)
        z3 = z // 8
        sl = np.asarray(p3[z3]).astype(np.float32)
        allsurf = sl > 0
        sl = sl * ndi.binary_erosion(np.asarray(c3[z3]) > 0, iterations=2)
        ys, xs = np.nonzero(allsurf)
        ccy, ccx = ys.mean(), xs.mean()
        ys, xs = np.nonzero(sl > 0)
        r = np.hypot(ys - ccy, xs - ccx)
        rmax = np.percentile(np.hypot(*(np.nonzero(allsurf) - np.array([[ccy], [ccx]]))), 99)
        inwin = (np.abs(xs * 8 + 4 - cx) <= lim) & (np.abs(ys * 8 + 4 - cy) <= lim)
        cand = np.flatnonzero((r >= 0.4 * rmax) & (r <= 0.7 * rmax) & inwin)
        sup = ndi.uniform_filter(sl, 5)[ys[cand], xs[cand]]
        cand = cand[sup >= np.percentile(sup, 90)]
        order = rng.permutation(cand)
        got = 0
        for k in order:
            if got >= n_per:
                break
            y0, x0 = int(ys[k]) * 8 + 4, int(xs[k]) * 8 + 4
            if any(np.hypot(y0 - s["y"], x0 - s["x"]) < min_sep and abs(z - s["z"]) < min_sep for s in seeds):
                continue
            w = 8
            sub = np.asarray(p0[z - w:z + w + 1, y0 - w:y0 + w + 1, x0 - w:x0 + w + 1]).astype(np.float32)
            cc = np.asarray(c0[z - w:z + w + 1, y0 - w:y0 + w + 1, x0 - w:x0 + w + 1])
            sub *= cc > 0
            if sub.max() <= 0:
                continue
            dz, dy, dx = np.unravel_index(int(np.argmax(sub)), sub.shape)
            seeds.append({"x": x0 - w + int(dx), "y": y0 - w + int(dy), "z": z - w + int(dz),
                          "ct": int(cc[dz, dy, dx]), "pred": float(sub.max()),
                          "radius_frac": round(float(r[k] / rmax), 3), "z_slice": z})
            got += 1
    res = {"window": {"cx": cx, "cy": cy, "cz": cz, "half": half, "margin": margin}, "min_sep": min_sep, "seeds": seeds}
    print(json.dumps(res))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main(sys.argv)
