# EXP-021 — Reproduction de Korotetskyi & Haindl 2026 (H-022, N1.1)

**Statut : en cours** (recalcul section 6 reporté après EXP-018, voir ci-dessous).

## Objet
Reproduire la chaîne de texture 3D sans entraînement (10 descripteurs + fusion) sur les 25 glyphes de PHerc. 172
(article Zenodo 10.5281/zenodo.24391747 ; paquet code+données 10.5281/zenodo.24392114, `code_data_v2.zip`,
sha256 7db284ab…). Critère H-022 : MCC moyen de la fusion publiée 0,457 reproduit à ± 0,02.

## Exécution
- Le paquet compile des bibliothèques C (`cc`) et fige un environnement Linux : exécution sous **WSL Ubuntu**
  (Python 3.12.3, `uv` 0.9.30, `requirements-linux.lock.txt` des auteurs), copie locale `~/korotetskyi2026/code`.
- `reproduce_glyphs.sh` : `out/` fourni mis de côté (`out_supplied/`), recalcul `glyphs run` → `glyphs analyse` →
  `tables per_op`, puis `sections/compare.py out_supplied out` (tolérance relative 1e-6).
- Code des auteurs sous CC BY-NC 4.0 : non copié dans ce dépôt.
- Contention mesurée : 6 workers CPU sous WSL font tomber l'entraînement EXP-018 de 2,3 à ~0,5 it/s (chargeurs
  de données privés de CPU) ; même suspendu (SIGSTOP), il garde ~8 Go de RAM et le débit reste dégradé : recalcul arrêté, WSL éteint, relance après EXP-018.

## Lecture critique préalable (avant résultats)
- Les **masques de référence** sont dérivés de la prédiction publique `20241108111522_prediction.png`
  (`make_masks.py`), donc d'un modèle neuronal : le MCC mesure l'accord avec cette prédiction, pas avec une
  vérité terrain manuelle.
- Le 0,457 est le **meilleur des 1 023 sous-ensembles** (ACF+WAV+LRE) choisi sur les mêmes 25 glyphes : biais de
  sélection ; l'intensité brute (RAW) seule donne 0,373 [IC 0,334-0,410] et LRE seul 0,388.
- Conséquence pour H-023 (N1.2) : appliquer la configuration **figée** (ACF+WAV+LRE, paramètres
  `data/descriptor_config.json`) à nos segments, sans nouvelle sélection, et comparer à RAW et à reader-v2.

## Résultats
À compléter (comparaison recalcul / fourni).
