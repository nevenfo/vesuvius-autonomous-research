# EXP-018 — E1.5 / H-017 : reader-v2-LO, recette reader-v2 ré-entraînée sans les objets de test

## Cadrage (2026-11-23)
- **Constat** : ink_9um (corpus 0139, 1667, Paris4, 0814 — `villa/ink-detection/configs/aligned21_hybrid_3d2d.json`)
  n'a vu **aucun** objet de test (0841, 0009B, 0500P2) : il est déjà « leave-out ». La parenté gênante est celle de
  reader-v2 (0009B : 14 segments + init `ft12k` affinée à 116 keV ; 0500P2 : 18 segments).
- **Recette reader-v2** (`github.com/DomRusso2/reader-v2`, `scripts/v2_run.py`, `train_config.json`) : labels natifs
  denses = **carte canon 2,4 µm publiée** ramenée sur la grille 9 µm (encre ≥ 128 ; supervisé si ≥ 128 ou ≤ 64) →
  reader-v2 est distillé du modèle canon.
- **Coût mesuré** : 0,174 s/itération (batch 64, 17×128×128, fp16, tenseurs synthétiques), 5,4 Gio VRAM → 40k itérations
  ≈ 1,9 h de GPU pur (+ chargement des données). Données : 38 segments d'entraînement (≈ 85 Go non compressés,
  `selection.json`), identiques segment pour segment aux jeux natifs v2 de reader-v2 (vérifié 38/38).
- **Écarts assumés** (`make_config.py`) : sans 0009B/0500P2, sans le corpus aligné 21 tranches de l'auteur (non publié
  tel quel), quotas proportionnels (22/13/9/20), init `scrollprize/ink_9um` s43 60k au lieu de `ft12k`.

## Hypothèse et critère (fixés avant l'entraînement)
H-017 : l'avantage de reader-v2 sur 0009B/0500P2 ne vient pas d'avoir vu ces objets : reader-v2-LO perd < 0,03 d'AUC
sup. par rapport à reader-v2 en moyenne sur 0009B et 0500P2, et sa perte n'y dépasse pas de plus de 0,02 sa perte
sur 0841 (DiD, comme EXP-008). Réfutée sinon. Secondaire : fusion(reader-v2-LO, Hecate) sur 3 objets.

## Fichiers
`select.py` → `selection.json` ; `build.py` (SV + carte canon + labels denses) ; `make_config.py` → `train_config.json`.
