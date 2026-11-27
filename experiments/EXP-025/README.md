# EXP-025 — W2.3 / H-031 : premier segment propre sur un rouleau éligible sans segment publié

**Statut : en cours** (protocole fixé le 2026-11-27 avant exécution).

## Obstacle visé
EXP-024 : 16/17 rouleaux First Letters n'ont aucun segment publié ; les découvertes passent par la segmentation.
Question : les outils officiels permettent-ils, sur notre matériel et sans intervention manuelle, d'obtenir une surface
exploitable à partir des seules représentations publiées ? Solution communautaire existante : oui (VC3D GrowPatch,
spiral fitting) — on la réutilise, aucun développement propre (`docs/state-of-the-art/2026-11-27-reading-and-geometry.md` §2).

## Veille consultée
2026-11-27 : lauréats 2026 = GrowPatch sur prédiction de surface « m7 » ou spiral-fitter, **avec corrections
manuelles** ; sheet switches = échec principal. Impact : on mesure ce que donne la version **sans** correction.

## Cible et outils
- PHerc1218 (éligible First Letters, aucun segment publié, ESRF 8,64 µm / 116 keV comme 0009B et 0800, volume masqué
  `20250521120456`, prédiction de surface m7 `20260413222639` seuil 0,2, lasagna disponible). Parentés : aucun de nos
  modèles propres (reader-v2/LO, ink_9um) n'a vu 1218 (`docs/data/provenance.csv`).
- VC3D `a7d4f88` (release `latest` du 2026-11-27, archive Windows, GPL-3.0, sha256 zip 993cc32a…), non redistribué.

## Protocole (fixé avant)
1. Graine automatique : niveau 3 de la prédiction de surface, tranche médiane en z ; centre = centroïde des voxels de
   surface ; candidats à 40–70 % du rayon maximal ; choix déterministe (rng 0) du candidat au plus fort support local ;
   passage au niveau 0 et recalage sur le voxel de prédiction maximale à ± 8 voxels.
2. `vc_grow_seg_from_seed` mode `streamline` (estimateur de normales sur le CT, pas de normal-grids), `generations` 60
   (grille 121 × 121), `step_size` 20, `walk_step_size` 2, `thread_limit` 8, `min_area_cm` 0, `--rng-seed 0`, volume
   distant (lecture par blocs), limite 2 h.
3. Mesures : surface (cm², `meta.json`), temps mur et CPU, volume réseau, **fidélité** = fraction de 1 000 sommets
   tirés au hasard situés à ≤ 2 voxels d'un voxel de prédiction de surface (niveau 0) ; intervention humaine = 0.

## Hypothèse et critères
**H-031** : sans intervention manuelle, ce protocole produit sur PHerc1218 un patch ≥ 4 cm² (taille du critère First
Letters) en ≤ 2 h machine, dont ≥ 90 % des sommets sont à ≤ 2 voxels de la prédiction de surface.
Réfutée si l'une des trois conditions échoue ; en cas d'échec, l'attribuer (graine, mode, paramètres, données, outil).
Conditions d'arrêt : 2 h mur ou échec de l'outil ; pas de réglage itératif de paramètres au-delà d'un second essai
argumenté (mode `default` avec normal-grids si `streamline` échoue).

## Limites connues
Fidélité à la prédiction m7 ≠ fidélité au feuillet réel (m7 peut elle-même sauter de feuillet) ; aucune détection de
saut de feuillet dédiée à ce stade ; un patch n'est pas une couverture.
