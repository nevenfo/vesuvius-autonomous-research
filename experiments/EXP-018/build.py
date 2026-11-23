"""EXP-018 — téléchargement et labels denses du corpus reader-v2-LO (règles reader-v2 `scripts/v2_run.py`).

Usage : PYTHONPATH=src python experiments/EXP-018/build.py <selection.json> <data_dir> [workers=4]
Pour chaque segment `role == train` : surface-volume niveau 0 (`vesres.fetch_segment`, idempotent) + carte d'encre
canon publiée (`map.tif`) ; labels denses sur la tranche centrale, identiques à v2_run.py `build_labels` :
  inklabels        = valide & (carte >= 128)
  supervision_mask = valide & (carte >= 128 | carte <= 64)     (carte ramenée sur la grille du SV par INTER_AREA)
Arborescence : <data_dir>/<obj>/<id>/{sv.zarr,map.tif}, <data_dir>/<obj>/labels/<id>/<id>_{inklabels,supervision_mask}.zarr
"""
import json, os, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import zarr

from vesres import fetch_segment

S3 = 'https://vesuvius-challenge-open-data.s3.amazonaws.com/'
T_HI, T_LO = 128, 64


def _rename_retry(src, dst, tries=30):
    for i in range(tries):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            time.sleep(2 + i)
    raise PermissionError(f'renommage impossible : {src}')


def one(r, data):
    import cv2, tifffile
    d = data / r['obj'] / r['id']
    ld = data / r['obj'] / 'labels' / r['id']
    if (ld / 'done').exists():
        return r['id'], 'déjà fait'
    t0 = time.time()
    part = d.with_name(d.name + '.partial')
    if not (d / 'done.json').exists() and (part / 'done.json').exists():
        _rename_retry(part, d)  # copie complète restée en .partial (renommage bloqué par l'antivirus)
    try:
        fetch_segment.fetch(r['scroll'], r['seg'], r['sv'].split('/surface-volumes/')[1], 'none/none', d)
    except PermissionError:
        _rename_retry(part, d)
    mp = d / 'map.tif'
    if not mp.exists() or mp.stat().st_size != r['map_size']:
        urllib.request.urlretrieve(S3 + urllib.parse.quote(r['map']), str(mp) + '.part')
        os.replace(str(mp) + '.part', mp)
    v = zarr.open_array(str(d / 'sv.zarr' / '0'), mode='r')
    z = v.shape[0] // 2
    valid = np.asarray(v[z]) > 0
    m = tifffile.imread(mp)
    m = m[..., 0] if m.ndim == 3 else m
    if m.shape != valid.shape:
        m = cv2.resize(m, (valid.shape[1], valid.shape[0]), interpolation=cv2.INTER_AREA)
    ld.mkdir(parents=True, exist_ok=True)
    fr = {}
    for name in ('inklabels', 'supervision_mask'):
        g = zarr.open_group(str(ld / f"{r['id']}_{name}.zarr"), mode='w', zarr_format=2)
        a = g.create_array('0', shape=v.shape, chunks=(v.shape[0], 128, 128), dtype=np.uint8, fill_value=0,
                           chunk_key_encoding={'name': 'v2', 'separator': '.'})
        lab = (valid & (m >= T_HI)) if name == 'inklabels' else (valid & ((m >= T_HI) | (m <= T_LO)))
        a[z] = lab.astype(np.uint8) * 255
        fr[name] = round(float(lab.sum() / max(valid.sum(), 1)), 3)
    (ld / 'done').write_text(json.dumps(fr))
    return r['id'], f"{fr} {time.time() - t0:.0f}s"


def main(sel, data, workers):
    rows = [r for r in json.load(open(sel)) if r['role'] == 'train']
    with ThreadPoolExecutor(workers) as ex:
        for i, (sid, msg) in enumerate(ex.map(lambda r: one(r, data), rows), 1):
            print(f'[{i}/{len(rows)}] {sid} {msg}', flush=True)


if __name__ == '__main__':
    main(sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 4)
