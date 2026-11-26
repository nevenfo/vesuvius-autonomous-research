"""EXP-020 (K4.1, H-018) — entraînement koine_machines avec schedule WSD (warmup-stable-decay), sans patch de villa.

Usage : <python venv-koine> experiments/EXP-020/train_wsd.py <train_config.json>
La config garde `scheduler.name = diffusers_cosine_warmup` (seul nom accepté par train.py) et ajoute une clé
`wsd` : {"decay_start": int, "decay_steps": int}. Ce module remplace `get_scheduler` dans
`koine_machines.training.train` par un LambdaLR :
  pas < warmup        : s / warmup                                    (identique à la recette)
  warmup ≤ s < D      : 1                                             (plateau)
  D ≤ s < D + C       : 1 - sqrt((s - D) / C)                         (cooldown `1-sqrt`, Hägele et al. 2024)
  s ≥ D + C           : 0
Branche de cooldown : relancer depuis un checkpoint du plateau (`checkpoint`, `weights_only: false`) avec
`decay_start` = pas du checkpoint, `num_iterations` = D + C et un `out_dir` distinct ; l'état LambdaLR restauré
(`last_epoch`) reste valide car la fonction ne dépend que du pas.
`--dry-run` : affiche le multiplicateur aux pas clés sans entraîner (test K2.2).
"""
import json
import math
import sys

import torch


def wsd_lambda(warmup: int, decay_start: int, decay_steps: int):
    def f(s: int) -> float:
        if s < warmup:
            return s / max(1, warmup)
        if s < decay_start:
            return 1.0
        if s < decay_start + decay_steps:
            return 1.0 - math.sqrt((s - decay_start) / decay_steps)
        return 0.0
    return f


def main(cfg_path: str, dry: bool = False) -> None:
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    w = cfg['wsd']
    warm, D, C = int(cfg.get('warmup_steps', 1000)), int(w['decay_start']), int(w['decay_steps'])
    if D + C != int(cfg['num_iterations']):
        raise ValueError(f"decay_start + decay_steps ({D + C}) ≠ num_iterations ({cfg['num_iterations']})")
    f = wsd_lambda(warm, D, C)
    if dry:
        for s in sorted({0, warm // 2, warm, D - 1, D, D + C // 4, D + C // 2, D + C - 1, D + C}):
            print(s, round(f(s), 4))
        return
    import koine_machines.training.train as T

    def get_scheduler(name, optimizer, initial_lr=None, max_steps=None, warmup_steps=None, **_):
        return torch.optim.lr_scheduler.LambdaLR(optimizer, f)

    T.get_scheduler = get_scheduler
    T.train.main(args=[cfg_path], standalone_mode=True)


if __name__ == '__main__':
    main(sys.argv[1], '--dry-run' in sys.argv[2:])
