"""EXP-025 — fidélité d'un patch tifxyz à la prédiction de surface (protocole, étape 3).

Usage : python experiments/EXP-025/fidelity.py <segment_dir> <surface_pred_zarr_url> <out.json> [n=1000] [tol=2]
Fraction de n sommets valides (tirage rng 0) ayant un voxel de prédiction > 0 à ≤ tol voxels (niveau 0, cube).
Lecture groupée : chaque bloc de la prédiction touché n'est lu qu'une fois.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import tifffile
import zarr


def main(seg: Path, url: str, out: Path, n: int = 1000, tol: int = 2) -> None:
    x, y, z = (tifffile.imread(seg / f"{c}.tif").astype(np.float64) for c in "xyz")
    valid = (x > 0) & (y > 0) & (z > 0) & np.isfinite(x)
    idx = np.flatnonzero(valid)
    pick = np.random.default_rng(0).choice(idx, min(n, len(idx)), replace=False)
    pts = np.stack([z.ravel()[pick], y.ravel()[pick], x.ravel()[pick]], 1).round().astype(int)
    arr = zarr.open_array(url.rstrip("/") + "/0", mode="r")
    cz, cy, cx = arr.chunks
    groups = defaultdict(list)
    for i, (pz, py, px) in enumerate(pts):
        groups[(pz // cz, py // cy, px // cx)].append(i)
    hit = np.zeros(len(pts), bool)
    for (bz, by, bx), ii in groups.items():
        z0, y0, x0 = bz * cz - tol, by * cy - tol, bx * cx - tol
        blk = np.asarray(arr[max(z0, 0):(bz + 1) * cz + tol, max(y0, 0):(by + 1) * cy + tol,
                             max(x0, 0):(bx + 1) * cx + tol]) > 0
        oz, oy, ox = max(z0, 0), max(y0, 0), max(x0, 0)
        for i in ii:
            pz, py, px = pts[i] - (oz, oy, ox)
            w = blk[max(pz - tol, 0):pz + tol + 1, max(py - tol, 0):py + tol + 1, max(px - tol, 0):px + tol + 1]
            hit[i] = bool(w.any())
    res = {"n_points": int(len(pts)), "tol_voxels": tol, "fidelity": round(float(hit.mean()), 4),
           "n_chunks_read": len(groups), "valid_vertices": int(valid.sum()), "grid": list(x.shape)}
    print(res)
    out.write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    a = sys.argv
    main(Path(a[1]), a[2], Path(a[3]), int(a[4]) if len(a) > 4 else 1000, int(a[5]) if len(a) > 5 else 2)
