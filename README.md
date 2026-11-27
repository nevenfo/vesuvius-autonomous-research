# VESUVIUS AUTONOMOUS RESEARCH

Recherche ouverte et largement autonome visant la lecture virtuelle intégrale et vérifiable des manuscrits
carbonisés du [Vesuvius Challenge](https://scrollprize.org), en réutilisant d'abord l'état de l'art
(`ScrollPrize/villa`, modèles publiés) et en n'innovant que sur besoin démontré.

- Objectif, invariants, phases : [`plan.md`](plan.md) · état courant et prochaine action : [`progress.md`](progress.md)
- État de l'art daté : [`docs/state-of-the-art/`](docs/state-of-the-art/) · données/licences : [`docs/data/`](docs/data/)
- Hypothèses classées : [`docs/hypotheses.md`](docs/hypotheses.md) · expériences : `experiments/EXP-NNN/`

## Environnement
Le dépôt vit sur le NAS ; l'environnement et le cache de données vivent sur le disque local du PC :

```bash
uv venv --python 3.12 $VESRES_WORK/.venv
uv pip install --python $VESRES_WORK/.venv/Scripts/python.exe torch torchvision --index-url https://download.pytorch.org/whl/cu128
uv pip install --python $VESRES_WORK/.venv/Scripts/python.exe -r requirements.lock
$VESRES_WORK/.venv/Scripts/python.exe -m pytest -q
```

Cache évictable : `VESRES_CACHE` (défaut `~/vesuvius-work/cache`).

## Licences
Code original : MIT ([`LICENSE`](LICENSE)). Données Vesuvius Challenge : CC BY-NC 4.0 / EduceLab Data License,
**non redistribuées ici** ; aucune image d'encre ni transcription issue de ces données n'est publiée sans accord
de Vesuvius Challenge (voir `docs/data/README.md`). Data used: EduceLab-Scrolls (Parsons et al., 2023, arXiv:2304.02084).
