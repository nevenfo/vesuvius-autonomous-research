# EXP-027 — X2 / I-003 → H-032 : auto-cohérence de rendus redondants du même papyrus (faisabilité)

**Statut : en cours** (hypothèse et critères fixés le 2026-11-27 avant calcul).

## Origine (anomalie → idée)
EXP-023 : sur PHerc. 1667, la somme des aires des segments publiés (2 525 cm²) vaut ≈ 2× la surface réellement
déroulée (1 231 cm², arXiv:2606.29085) → une grande partie du papyrus est rendue par **plusieurs segments distincts**.
Les papyrologues de 1667 n'acceptaient une lecture que si les lettres restaient stables « à travers rendus ou passes
d'inférence répétés ». Idée I-003 : formaliser cette stabilité comme mesure de fiabilité **sans label**, locale, utilisable
sur des rouleaux inédits (pas de référence humaine) et comme détecteur de zones douteuses (géométrie ou hallucination).

## Obstacle visé
Absence de référence indépendante (obstacle n° 1) et classement « lisible / incertain » de la couverture (obstacle n° 2).

## Méthode (fixée avant)
- Segments publiés de PHerc1667 ayant tifxyz + prédiction d'encre officielle du **même modèle** (le plus fréquent).
- Correspondance 3D : nœuds tifxyz (coordonnées niveau 0) de deux segments à ≤ 2 voxels l'un de l'autre (KD-tree) et
  normales compatibles (|cos| ≥ 0,9) = même point physique ; une paire de segments est « chevauchante » si ≥ 2 000 nœuds
  appariés.
- Valeur d'encre d'un nœud = moyenne de la prédiction sur la cellule de rendu correspondant au nœud.
- Mesure : corrélation de Spearman ρ entre les deux segments sur les nœuds appariés, par paire.
- Contrôle négatif : même calcul après décalage circulaire des valeurs d'un segment le long de la grille (≥ 3 mm), 20
  décalages → distribution nulle.
- Coût : lecture de tifxyz (petits) et des prédictions officielles déjà publiées ; aucune inférence ; CPU.

## Hypothèse et critères
**H-032** : sur les paires chevauchantes, la médiane de ρ est ≥ 0,5 et dépasse le 95ᵉ centile de la distribution nulle
pour ≥ 80 % des paires. Soutenue → la redondance fournit une mesure de fiabilité exploitable (étape suivante : carte
locale de stabilité et lien avec la lisibilité glyphe). Réfutée si médiane ρ < 0,5 ou < 80 % des paires au-dessus du
nul ; dans ce cas attribuer : géométrie (rendus non superposables), modèle (prédictions instables), appariement.
Indéterminée si < 3 paires chevauchantes.

## Limites connues
Même modèle sur des rendus différents : mesure la stabilité géométrie + inférence, pas l'exactitude (classe R0) ;
segments dérivés les uns des autres (versions « merged », « straightened ») ne sont pas des rendus indépendants → à
distinguer par nom/date et rapporter séparément ; 1667 est vu par les modèles d'encre (fuite sans effet sur la
stabilité mais à rappeler).
