# Cadrage H-005 / E1.2 — détection d'encre 2,4 µm (2026-11-23)

## Faits vérifiés (bucket `vesuvius-challenge-open-data`, listés le 2026-11-23)
- Surface-volume 2,403 µm de 0841 w00 : `surface-volumes/2.403um-0.22m-77keV-volume-20260319124803.zarr/0`,
  (109, 16460, 18560) uint8 non compressé → **≈ 33 Go par segment** (critère « go » d'inférence ≤ 20 Go : dépassé).
- **Prédictions officielles déjà publiées** dans `<scroll>/segments/<seg>/ink-detection/` :
  | Modèle (suffixe du fichier) | Grille | date run | 0841 × 3 | 0009B | 0500P2 |
  |---|---|---|---|---|---|
  | `new_canon_autoresearch_recipe-tile256-stride128` | 2,4 µm (labels) | 2026-04-17 | oui | oui | oui |
  | `ink9um-hybrid3d2d-s43-20k-tile128-stride64` | 9 µm | 2026-08-14 | oui | oui | non |
  | `reader-v3-tile384-stride192` | 9 µm | 2026-10-19 | oui | oui | non |
  | `argus-v3-tile384-stride192` | 9 µm | 2026-11-17 | oui | oui | non |
  Taille 5–47 Mio par fichier (≈ 250 Mio au total).

## Faits externes (recherche web, à revérifier sur les pages)
- Seul modèle ~2 µm du registre HF `scrollprize` : `scrollprize/ink_canonical_2um` (ResNet-152 3D + décodeur 3D,
  recette `new_canon_autoresearch_recipe`, fenêtre 62 couches, tuile 256, MIT ; données sous CC BY-NC 4.0) ;
  **données d'entraînement non déclarées**. Inférence officielle : `villa/ink-detection/optimized_inference`
  (`entrypoint.py`, variables `MODEL`, `S3_PATH`, `START_LAYER`, `END_LAYER`…), VRAM non documentée.
- Famille `scrollprize/PHerc.1667-iteration-*` (ResNet3D-50 + U-Net 2D) : 0500P2 dans l'entraînement.
- Aucune comparaison contrôlée 2,4 vs 9 µm publiée trouvée.

## Décision
- Pas d'inférence 2,4 µm locale à ce stade (33 Go/segment, VRAM inconnue) : on **évalue les prédictions officielles
  publiées** avec notre protocole (EXP-017), ce qui teste H-005 sur la qualité, pas sur le coût.
- Risque de circularité : les labels `20260918` sont postérieurs aux prédictions canon (2026-04-17) et ont pu être
  amorcés par elles (B1.2 non résolu) ; reader-v3 / argus-v3 (postérieurs aux labels) ont pu être entraînés sur 0841.
  → toute comparaison favorable à ces modèles reste « indicative » tant que la parenté n'est pas établie.
