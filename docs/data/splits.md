# Parentés modèles ↔ données et politique de splits (B2.3)

Vérifié le 2026-11-12 sur les sources citées. « vu » = au moins un segment de l'objet dans l'entraînement
(labels ou pseudo-labels) ; un segment non vu d'un objet vu n'est **pas** une évaluation inter-rouleaux.

## Matrice
| Objet (type) | Segments étiquetés publiés | ink_9um | reader-v2 | Hecate | Utilisable comme test indépendant |
|---|---|---|---|---|---|
| PHerc0841 (rouleau) | 3 | non vu | non vu (déclaré, absent du `train_config.json`) | NV (« weak 3D supervision on other scrolls », liste non publiée) | **oui pour ink_9um, reader-v2** ; NV pour Hecate |
| PHerc0139 (rouleau) | 8 | vu (9 + 5 natifs) | vu | NV (probable) | non |
| PHerc1667 (rouleau) | 6 | vu (6) | vu | NV (probable) | non |
| PHercParis4 (rouleau) | 8 | vu (8) | vu | vu (3D Paris4) | non |
| PHerc0814 (rouleau) | 1 | vu (1) | vu | NV | non |
| PHerc0009B (fragment) | 1 (+ labels reader-v2) | non vu | vu (segments hors 4 tenus à l'écart) | NV | intra-objet seulement pour reader-v2 |
| PHerc0500P2 (fragment) | 1 | non vu | vu (`data/v2/0500P2`, 17 segments ; le segment étiqueté `20250825181859--1` est tenu à l'écart) | NV | oui pour ink_9um ; intra-objet seulement pour reader-v2 (EXP-008) |
| PHerc0343P (fragment) | 0 publié | non vu | vu | NV | — |
| PHerc0172 (rouleau) | 0 publié (prédictions seulement) | non vu | vu (`data/v2/0172`, cartes d'équipe) | NV | — |

Sources : ink_9um model card (`huggingface.co/scrollprize/ink_9um`, section *Training data*) ; reader-v2
`train_config.json` (13 jeux : 0139×4, 1667×2, Paris4, 0814×2, 0009B, 0500P2, 0343P, 0172) et `scripts/v2_run.py` ;
Hecate model card (`huggingface.co/scrollprize/hecate`, liste exacte des rouleaux non publiée).

## Conséquences
1. **Un seul rouleau étiqueté publié est réellement tenu à l'écart des modèles 9 µm actuels : PHerc0841.**
   Toute affirmation de généralisation inter-rouleaux (J5, ≥ 3 rouleaux) est aujourd'hui impossible sans
   (a) nouveaux labels indépendants, ou (b) ré-entraînement en *leave-one-scroll-out* sur nos propres splits.
2. Les labels des rouleaux sont des pseudo-labels raffinés par des modèles de la même famille → circularité possible
   sur les objets vus (H-002) ; seul un label issu d'IR (fragments DLS 2023) est indépendant des modèles.
3. Politique : (i) tout résultat porte la colonne de parenté ci-dessus ; (ii) un rouleau de test n'influence jamais
   un choix d'entraînement ou d'hyperparamètre ; (iii) les splits intra-rouleau se font par segment entier, jamais par patch.

## Rouleaux réservés au test (H1.1, provisoire)
- PHerc0841 (3 segments étiquetés, ESRF 113 keV 9,366 µm / 77 keV 2,403 µm).
- Candidats après ré-entraînement LOSO : 0814, 0500P2 (peu de segments → bon test de transfert), Frag1 DLS (labels IR).

## Provenance des ink-labels `20260918` (B1.2, vérifié le 2026-11-23)
Source primaire : `s3://vesuvius-challenge-open-data/metadata/history/20261119T152337Z/metadata.json` (entrées
`type: ink-labels`) et `scrollprize.org/data/datasets/ink-labels-README.md`.
- **Vérifié** : labels « reviewed » (`ink-labels-reviewed-20260918`), republiés le 2026-09-22 (schéma `ink-republish/1`)
  depuis un jeu antérieur `s3://philodemos/datasets/ink/ink_030927/<objet>/<segment>/` (`*_inklabels_v2.tif`,
  `*_supervision_mask_v2.tif`, `*_validation_mask_v2.tif`, aperçu `*_max_22_42.tif`) ; `registration: transferred` :
  reportés par maillage sur le rendu canonique 2,4 µm (couverture 0,993, distance p50 0,29 px, p95 1,75 px).
- **Vérifié** : décalage de canevas « measured … against the canonical render + ink-prediction alignment » ; résidu
  0,005–0,015 px (2,4 µm) → biais d'alignement en faveur du modèle de prédiction utilisé **négligeable** sur la grille
  9 µm, faible même à 2,4 µm.
- **Vérifié (README)** : labels de rouleaux = traits annotés à la main puis affinés par pseudo-labeling itératif.
- **Non vérifié** : modèle(s) utilisé(s) pour le pseudo-labeling (`annotated_on: unknown`, `ink_models_allow/deny: null`),
  parenté de reader-v3 / argus-v3 / `ink_canonical_2um`. → l'avantage du canon 2,4 µm (EXP-017) reste indicatif.
