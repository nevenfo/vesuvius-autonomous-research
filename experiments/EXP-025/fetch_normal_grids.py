"""EXP-025 — télécharge une fenêtre des normal-grids officielles (un fichier .grid par tranche et par plan) autour
d'une graine, dans un magasin local utilisable par `vc_grow_seg_from_seed` (`normal_grid_path`).

Usage : python experiments/EXP-025/fetch_normal_grids.py <normal_grids_url> <dest_dir> <x> <y> <z> [half=1300] [workers=16]
Plans : xy indexé par z, xz par y, yz par x (vérifié : xy/023246 existe, 023247 non, pour un volume de 23247 tranches).
"""
from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def fetch(url: str, dst: Path) -> int:
    if dst.exists():
        return 0
    tmp = dst.with_suffix(".part")
    try:
        urllib.request.urlretrieve(url, tmp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return -1
        raise
    os.replace(tmp, dst)
    return dst.stat().st_size


def main(url: str, dest: Path, x: int, y: int, z: int, half: int = 1300, workers: int = 16) -> None:
    url = url.rstrip("/")
    dest.mkdir(parents=True, exist_ok=True)
    fetch(url + "/metadata.json", dest / "metadata.json")
    jobs = []
    for plane, c in (("xy", z), ("xz", y), ("yz", x)):
        (dest / plane).mkdir(exist_ok=True)
        for i in range(max(c - half, 0), c + half + 1):
            jobs.append((f"{url}/{plane}/{i:06d}.grid", dest / plane / f"{i:06d}.grid"))
    with ThreadPoolExecutor(workers) as ex:
        sizes = list(ex.map(lambda j: fetch(*j), jobs))
    print({"files": len(jobs), "downloaded_bytes": sum(s for s in sizes if s > 0), "missing_404": sum(s < 0 for s in sizes)})


if __name__ == "__main__":
    a = sys.argv
    main(a[1], Path(a[2]), int(a[3]), int(a[4]), int(a[5]), *(int(v) for v in a[6:8]))
