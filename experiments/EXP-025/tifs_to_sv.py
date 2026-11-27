"""EXP-025 — convertit le rendu `vc_render_tifxyz --tif-output` (NN.tif, une couche par fichier) en `sv.zarr/0`
(zarr v2, uint8, [couches, H, W], blocs [n, 128, 128]) au format des surface-volumes publiés et de notre chaîne
d'inférence (`koine_machines.inference.infer <seg>/sv.zarr`).

Usage : python experiments/EXP-025/tifs_to_sv.py <render_dir> <segment_out_dir>
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import tifffile
import zarr


def main(render: Path, out: Path) -> None:
    files = sorted(render.glob("*.tif"), key=lambda p: int(p.stem) if p.stem.isdigit() else p.stem)
    if not files:
        raise SystemExit(f"aucun tif dans {render}")
    first = tifffile.imread(files[0])
    stack = np.zeros((len(files), *first.shape), np.uint8)
    for i, f in enumerate(files):
        a = tifffile.imread(f)
        stack[i] = (a >> 8).astype(np.uint8) if a.dtype == np.uint16 else a.astype(np.uint8)
    g = zarr.open_group(str(out / "sv.zarr"), mode="w", zarr_format=2)
    arr = g.create_array("0", shape=stack.shape, chunks=(len(files), 128, 128), dtype="uint8", compressors=None,
                         fill_value=0)
    arr[:] = stack
    print({"layers": len(files), "shape": list(stack.shape), "nonzero_frac_mid": round(float((stack[len(files) // 2] > 0).mean()), 4)})


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
