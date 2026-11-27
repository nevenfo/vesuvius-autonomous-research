"""EXP-018 — configuration d'entraînement de reader-v2-LO.

Usage : python experiments/EXP-018/make_config.py <selection.json> <data_dir> <out_dir> <config_out.json>
Base : `train_config.json` publié de reader-v2 (hyperparamètres inchangés : 40k itérations, batch 64, SGD 0,01,
warmup 500, patch 17×128×128, BCE lissée + Dice, robust-MAD, échantillonnage stratifié par rouleau).
Différences (seules) :
- datasets : uniquement les 4 jeux natifs v2 (0139, 0814, 0343P, 0172 ; mêmes 38 segments que reader-v2), sans
  0009B, 0500P2 (objets de test) ni le corpus aligné 21 tranches / pseudo de l'auteur (non publié tel quel) ;
- quotas : ceux de reader-v2 pour ces 4 rouleaux (12, 7, 5, 11) mis à l'échelle proportionnellement à 64
  (22, 13, 9, 20) — la règle de v2_run.py (reste ajouté à 0139) donnerait 41/64 à 0139 ;
- init : `scrollprize/ink_9um` hybrid_3d2d-seed43 step-060000 (corpus 0139/1667/Paris4/0814) au lieu de
  `reader-v2-init-ft12k` (affiné à 116 keV, a vu 0009B).
"""
import json, os, sys
from pathlib import Path

W = os.environ.get('VESRES_WORK', str(Path.home() / 'vesuvius-work')).replace('\\', '/')
RV2_CFG = W + '/models/domenicor046_reader-v2/train_config.json'
INIT = W + '/models/scrollprize_ink_9um/hybrid_3d2d-seed43/step-060000.pth'
QUOTAS = {'0139': 12, '0814': 7, '0343P': 5, '0172': 11}


def main(sel, data, out_dir, cfg_out):
    cfg = json.load(open(RV2_CFG))
    rows = [r for r in json.load(open(sel)) if r['role'] == 'train']
    data = Path(data).as_posix()
    cfg['datasets'] = []
    for obj in QUOTAS:
        segs = sorted(r['id'] for r in rows if r['obj'] == obj)
        cfg['datasets'].append({
            'segments_path': f'{data}/{obj}/labels', 'segments': segs,
            'surface_volume_paths': {s: f'{data}/{obj}/{s}/sv.zarr' for s in segs},
            'volume_scale': 0, 'source_family': f'native_v2_{obj}', 'sampling_scroll': obj,
            'sampling_physical_segment_keys': {s: f'{obj}:{s}' for s in segs},
            'sampling_representation_keys': {s: f'native_v2_{obj}:{s}' for s in segs}})
    tot = sum(QUOTAS.values())
    q = {k: round(v * 64 / tot) for k, v in QUOTAS.items()}
    q['0139'] += 64 - sum(q.values())
    cfg['fixed_scroll_prior']['target_batch_counts'] = q
    cfg['checkpoint'] = INIT
    cfg['weights_only'] = True
    cfg['out_dir'] = Path(out_dir).as_posix()
    cfg['description'] = 'reader-v2-LO (EXP-018) : recette reader-v2 sans 0009B/0500P2/0841, init ink_9um s43 60k.'
    json.dump(cfg, open(cfg_out, 'w'), indent=1)
    print(len(cfg['datasets']), 'jeux', sum(len(d['segments']) for d in cfg['datasets']), 'segments', q)


if __name__ == '__main__':
    main(*sys.argv[1:5])
