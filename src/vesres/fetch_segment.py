"""Copie locale (cache évictable) d'un surface-volume et de ses ink-labels depuis le bucket public.

Usage : python -m vesres.fetch_segment <scroll> <segment_long_id> <sv_name.zarr> <labels_rel_dir> <dest_dir>
Exemple : python -m vesres.fetch_segment PHerc0841 20260220213127-w00 \
    9.366um-1.2m-113keV-volume-20250821151531.zarr 2.403um-volume-20260319124803/20260918 \
    C:/Users/FlowUP/vesuvius-work/cache/segments/PHerc0841/20260220213127-w00

- Surface-volume : niveau 0 seulement, copié chunk par chunk dans un zarr v2 local (mêmes attributs).
- Labels : inklabels / supervision / validation, niveau 0, copiés en zarr v2 local.
- Idempotent : un marqueur `done.json` (avec provenance) évite de refaire ; écriture dans un dossier .partial puis renommage.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import zarr

BUCKET = "https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com"


def _copy_array(src: zarr.Array, dst_group: zarr.Group, name: str, attrs: dict, step: int = 1024) -> dict:
    dst = dst_group.create_array(name, shape=src.shape, chunks=src.chunks, dtype=src.dtype, fill_value=0,
                                 chunk_key_encoding={"name": "v2", "separator": "."}, compressors=None)
    h = src.shape[-2]
    for y0 in range(0, h, step):
        sl = (slice(None),) * (src.ndim - 2) + (slice(y0, min(h, y0 + step)), slice(None))
        dst[sl] = np.asarray(src[sl])
    return {"shape": list(src.shape), "dtype": str(src.dtype), "chunks": list(src.chunks)}


def fetch(scroll: str, seg: str, sv_name: str, labels_rel: str, dest: Path) -> dict:
    done = dest / "done.json"
    if done.exists():
        return json.loads(done.read_text())
    part = dest.with_name(dest.name + ".partial")
    if part.exists():
        shutil.rmtree(part)
    part.mkdir(parents=True)
    base = f"{BUCKET}/{scroll}/segments/{seg}"
    t0 = time.time()
    prov = {"scroll": scroll, "segment": seg, "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "items": {}}

    sv_url = f"{base}/surface-volumes/{sv_name}"
    sv_grp = zarr.open_group(sv_url, mode="r")
    out = zarr.open_group(str(part / "sv.zarr"), mode="w", zarr_format=2)
    out.attrs.update(dict(sv_grp.attrs))
    prov["items"]["sv"] = {"url": sv_url + "/0", **_copy_array(zarr.open_array(sv_url + "/0", mode="r"), out, "0", {})}

    for nm in ("inklabels", "supervision", "validation"):
        url = f"{base}/ink-labels/{labels_rel}/{nm}.zarr"
        try:
            src = zarr.open_array(url + "/0", mode="r")
        except Exception as e:  # masque optionnel absent
            prov["items"][nm] = {"url": url, "missing": repr(e)[:200]}
            continue
        g = zarr.open_group(str(part / f"{nm}.zarr"), mode="w", zarr_format=2)
        prov["items"][nm] = {"url": url + "/0", **_copy_array(src, g, "0", {})}

    prov["seconds"] = round(time.time() - t0, 1)
    (part / "done.json").write_text(json.dumps(prov, indent=1))
    if dest.exists():
        shutil.rmtree(dest)
    os.replace(part, dest)
    return prov


if __name__ == "__main__":
    a = sys.argv[1:]
    print(json.dumps(fetch(a[0], a[1], a[2], a[3], Path(a[4])), indent=1))
