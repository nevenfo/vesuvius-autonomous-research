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

## Exécution / Résultats (2026-11-27)
Code : `experiments/EXP-027/redundancy.py` (tests `tests/test_redundancy.py`). Agrégats : `results.json` (règle du README, tol 2 voxels) et `results_sensibilite_tol10.json` (analyse complémentaire, tol 10 voxels, **hors critère**). Cache `<VESRES_WORK>/cache/exp027/` (868 Mo téléchargés, 387 s ; aucune image d'encre dans le dépôt).

**Données.** Repère unique : `tifxyz-transformed` sur le volume `20251217075048` (2,399 µm), commun aux 20 segments. Modèle : `new_canon_autoresearch_recipe` (versions `-t2` écartées), prédiction `-ds8.jpg` présente sur 19 segments ; le segment `20260612121456` (w011 merged/straightened) n'a pas de prédiction ds8 → exclu (19 segments, 171 paires, 111 avec ≥ 1 nœud apparié après filtre bbox).
**Correspondance grille ↔ prédiction** (vérifiée sur les 19 segments) : `scale = 0,05` ; prédiction pleine résolution = grille × 20 (ex. 1969×785 nœuds ↔ 39380×15700 px, même orientation lignes/colonnes) ; `ds8` = ⌈plein/8⌉ → 2,5 px par nœud.
**Valeur d'encre d'un nœud** : `cv2.blur` 3×3 de la `ds8` échantillonnée en bilinéaire au pixel (i·2,5 ; j·2,5). Normales : différences finies centrales sur la grille (NaN sur bords/trous). Appariement : nœud A → plus proche nœud B (cKDTree, k=4) à ≤ 2 voxels avec |cos| ≥ 0,9, 1-1 (chaque nœud B conservé une fois, le plus proche). Nul : 20 décalages circulaires uniformes de la grille de valeurs de B le long de son axe le plus long, entre 63 nœuds (3 mm = 1 250 voxels × 0,05) et n−63 ; p95 des 20 ρ.

**Paires chevauchantes (≥ 2 000 nœuds, tol 2 vox)** — toutes « indépendantes » (numéros wNNN distincts, aucune paire dérivée chevauchante ; la seule paire w011 est merged/straightened et exclue) :
| Segments (suffixe wNNN) | n nœuds | ρ | nul p95 |
|---|---|---|---|
| 20240304144031 (w018) – 20240304161941 (w023) | 3 428 | 0,814 | 0,246 |
| 20240304161941 (w023) – 20251208130119 (w028) | 2 508 | 0,833 | 0,093 |
| 20251208130119 (w028) – 20251212185248 (w029) | 2 907 | 0,892 | 0,125 |
| 20251212185248 (w029) – 20251220020000 (w030) | 3 340 | 0,781 | 0,119 |

Quasi-chevauchantes sous le seuil : w013–w018 1 992, w030–w031 1 582, w031–w032 1 601.
**Verdict H-032 (règle exacte) : SOUTENUE** — 4 paires (≥ 3), médiane ρ = 0,823 ≥ 0,5, 4/4 (100 %) au-dessus du nul p95 (nul min/max par paire dans [−0,24 ; 0,26]). Paires dérivées : 0 (indéterminée).
**Analyse complémentaire tol 10 voxels** (non critère) : 76 paires chevauchantes, médiane ρ = 0,939 (min 0,625), 76/76 > nul p95 (marge min 0,243 ; nul p95 jusqu'à 0,73) ; n médian 11 161 nœuds. Même verdict.

**Écarts / anomalies.**
- La tolérance de 2 voxels est de l'ordre du dixième du pas de grille (20 voxels) : un appariement n'a lieu que si les grilles tombent à ≤ 2 voxels (distance médiane des appariés 1,5 vox, aucun nœud exact commun) → n sous-estime le recouvrement réel d'un facteur ≈ 30 (un nœud sur ~33 en moyenne) ; seulement 4 paires franchissent le seuil de 2 000 contre 76 à tol 10. Verdict inchangé, mais le critère « ≥ 2 000 nœuds » est dépendant de la tolérance (à réviser côté protocole si H-032 est repris).
- Les numéros wNNN ne sont pas des spires adjacentes : des paires à |Δw| jusqu'à 10 se recouvrent (tol 10) ; classification dérivée/indépendante fondée uniquement sur nom (wNNN, merged, straightened), sans test de dérivation géométrique (aucun appariement à distance < 0,05 vox).
- Nuls élevés (p95 jusqu'à 0,73) sur certaines paires : forte autocorrélation spatiale des prédictions ; ρ ne mesure ni l'exactitude (classe R0) ni l'indépendance d'inférence (même modèle, même volume).
- Valeur d'encre issue d'une prédiction JPEG 8 bits réduite ×8 (cellule ≈ 2,5 px, approximée par blur 3×3), pas de la pleine résolution.
