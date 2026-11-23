# EXP-017 — H-016 : prédictions officielles publiées (canon 2,4 µm, reader-v3, argus-v3) vs nos modèles

- **Date** : 2026-11-23 · aucune inférence. TIF officiels de `<scroll>/segments/<seg>/ink-detection/` (liste exacte :
  `sources.txt`, ≈ 250 Mio, hors Git dans `vesuvius-work/runs/EXP-017/`). Cadrage : `docs/data/scoping-2.4um.md`.
- **Grille** : cartes 9 µm déjà sur la grille du surface-volume local ; carte canon (grille des labels 2,4 µm) ramenée par
  cv2.INTER_AREA. Alignement vérifié (corrélation officiel/notre ink9um 0,53 contre 0,11 avec un miroir).
- **Critère fixé avant** : H-016 réfutée si AUC sup.(canon) − AUC sup.(fusion reader-v2+Hecate) < 0,02 en moyenne sur 0841.

## Résultats (région supervision ; AUC / AP)
| Segment | reader-v2 | Hecate | fusion | canon 2,4 µm | reader-v3 | argus-v3 | ink9um officiel | ink9um s43 (nous) |
|---|---|---|---|---|---|---|---|---|
| 0841 w00 | 0,876 / 0,742 | 0,912 / 0,800 | 0,926 / 0,824 | **0,971 / 0,917** | 0,916 / 0,807 | 0,922 / 0,804 | 0,779 / 0,563 | 0,740 / 0,483 |
| 0841 …144552 | 0,826 / 0,690 | 0,784 / 0,676 | 0,824 / 0,720 | **0,920 / 0,820** | 0,834 / 0,728 | 0,852 / 0,746 | 0,721 / 0,579 | 0,701 / 0,539 |
| 0841 …174252 | 0,819 / 0,657 | 0,894 / 0,745 | **0,887 / 0,752** | 0,870 / 0,703 | 0,854 / 0,715 | 0,848 / 0,719 | 0,719 / 0,518 | 0,747 / 0,537 |
| 0009B | 0,927 / 0,826 | 0,884 / 0,780 | 0,935 / 0,845 | **0,955 / 0,893** | 0,949 / 0,856 | 0,951 / 0,858 | 0,801 / 0,622 | 0,813 / 0,610 |
| 0500P2 | 0,873 / 0,721 | 0,910 / 0,781 | 0,923 / 0,804 | **0,974 / 0,924** | — | — | — | 0,767 / 0,521 |

Gain AUC canon − fusion sur 0841 : +0,046 / +0,096 / −0,018 → **moyenne +0,042**. IC appariés : `results.json`.

## Conclusions
- **H-016 soutenue au critère, mais indicative seulement.** Les labels de rouleaux sont des traits manuels **affinés par
  pseudo-labeling itératif** (README officiel `ink-labels-README.md`) ; les prédictions canon (2026-04-17, grille des
  labels) précèdent les labels `20260918` et ont pu servir à les amorcer. L'avantage de canon est donc possiblement
  circulaire : il mesure en partie l'accord avec le modèle qui a produit les labels. Indice compatible : canon domine
  surtout là où l'AP est très élevée (0500P2 0,924, w00 0,917) et perd sur …174252.
- **reader-v3 / argus-v3** (9 µm, postérieurs aux labels, parenté non publiée) : ≈ fusion reader-v2+Hecate sur 0841
  (AUC moyenne 0,868 / 0,874 contre 0,879), légèrement au-dessus sur 0009B. Aucun gain net démontré sur notre chaîne.
- **ink9um officiel ≠ notre run s43** (autre checkpoint « 20k », tuile 128) : AUC +0,01 à +0,04 sur 0841 ; nos
  conclusions sur ink_9um (EXP-001…008) portent sur notre run, à ne pas confondre avec la carte publiée.
- Conséquence : sans labels indépendants des pseudo-labels (ou ré-entraînement LOSO, E1.5), le gain 2,4 µm ne peut pas
  être séparé de la circularité. B1.2 (nature des labels) reste prioritaire pour interpréter toute comparaison.
