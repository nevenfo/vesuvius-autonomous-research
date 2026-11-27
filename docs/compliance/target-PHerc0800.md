# Audit de rouleau cible — PHerc0800 (R1.1 / L2.2, 2026-11-27)

Aucune image, coordonnée de texte ni lecture publiée ici (licence données). Aperçus privés : `vesuvius-work/runs/R1/PHerc0800/`.

## Données (catalogue `metadata.min.json` du 2026-11-26, ETag 2f0d7504…)
- Un scan ESRF 8,64 µm / 116 keV (`20250521135224`, masqué, CC BY-NC 4.0) ; représentations publiées : prédiction de
  surface, normal-grids, lasagna.
- 6 segments `auto_grown` (2025-10-28/29), surfaces valides ≈ 3,2 / 2,9 / 2,9 / 4,2 / 3,4 / 0,7 cm² → **≈ 17 cm² au
  total** (estimation physique du rouleau : EXP-023).
- Prédictions officielles sur les 6 segments : ink_9um s43, reader-v3, argus-v3 (téléchargées, 22 Mo).

## Parentés des modèles (règle « pas de recouvrement entraînement / prédiction »)
| Modèle | A vu PHerc0800 ? | Statut |
|---|---|---|
| ink_9um | non (0139, 1667, Paris4, 0814) | V |
| reader-v2 / reader-v2-LO | non (`train_config.json`, `selection.json`) | V |
| Hecate | inconnu (liste non publiée) | NV |
| reader-v3, argus-v3, canon 2,4 µm | inconnu | NV |
Règle « scan plus résolu du même rouleau » : aucun scan de 0800 autre que 8,64 µm au catalogue → sans objet à ce jour.

## Inspection préalable des prédictions officielles (privée)
Fraction de pixels > 0,5 : reader-v3 2–10 %, argus-v3 4–16 %, ink_9um 1–4 % selon le segment. Inspection visuelle
d'un aperçu reader-v3 réduit : taches diffuses de taille sub-glyphe, au plus un alignement évoquant une ligne,
**aucune lettre lisible**. Cohérent avec l'absence de First Letters annoncé sur 0800.

## Décision
- 0800 reste éligible et admissible pour nos modèles propres (reader-v2/LO, ink_9um) ; Hecate et reader-v3 exclus
  de toute soumission tant que leurs parentés sont inconnues.
- Valeur attendue d'une inférence de notre chaîne 9 µm sur ces 17 cm² : **faible** (au niveau glyphe, reader-v3 ≈
  notre fusion, EXP-022). Le facteur limitant probable est la **surface segmentée** et la résolution, pas le modèle
  d'encre → R1 réorienté vers un tri des rouleaux First Letters par surface publiée et signal des prédictions
  officielles (EXP-024), et vers W2 (segmentation supplémentaire par les outils existants).
