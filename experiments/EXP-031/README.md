# EXP-031 — R1.5 / H-036 : étendre la surface propre sur PHerc1218 et y appliquer la chaîne d'encre orientée

**Statut : préenregistré le 2026-11-27** (critères écrits avant toute croissance).

## Question
Un seul patch de 4,11 cm² sans lettre (EXP-029) ne dit rien du rouleau. La chaîne automatique (EXP-025) passe-t-elle
à l'échelle — plusieurs spires, plusieurs hauteurs — sans intervention, et la chaîne d'encre orientée (EXP-030) y
trouve-t-elle des lettres candidates ?

## Protocole
1. Graines : `seeds.py` (déterministe, rng 0) dans la fenêtre des normal-grids déjà locales (centre = graine EXP-025
   4324 5292 11620, demi-côté 1 300, marge 500) ; 3 tranches z = 11020, 11620, 12220 ; 3 graines par tranche ;
   rayon 40–70 % ; support local ≥ p90 ; séparation ≥ 700 voxels ; graine dans le CT érodé.
2. Croissance : `vc_grow_seg_from_seed` avec `experiments/EXP-025/params4.json` inchangé (mode `default`,
   60 générations, normal-grids locales), volume masqué distant, une graine à la fois, limite 20 min par graine.
3. Par patch : surface (`meta.json`), temps, fidélité (`EXP-025/fidelity.py`, 1 000 sommets, 2 voxels) ; orientation
   (`EXP-030/orientation.py`, axe = centroïde de la prédiction) ; rendu 31 couches (`--flip-normals` si normale
   sortante) ; inférence reader-v2-LO et ink_9um ; `EXP-029/analyze.py` (zones candidates, accord, contrôles).
4. Surface unique cumulée : union des sommets valides voxélisés à 20 voxels (pas de la grille), patch `out4` inclus ;
   aire = Σ aires × (cellules uniques / cellules totales).

## Amendement avant toute croissance (2026-11-27)
La fenêtre locale (±800 voxels utiles) ne laissait que 2 graines admissibles (bande de rayon × séparation). Un fichier
`.grid` couvrant un plan entier, toutes les normal-grids de 1218 sont téléchargées (cache évictable, ≈ 38 000 fichiers) ;
la fenêtre devient le volume entier (`seeds.py … 3800 3800 11623 11700 6000,11620,17200 3 0 700`), tranches z = 6000,
11620, 17200 (≈ 25/50/75 % de la hauteur). Graines obtenues : 9 (rayon 0,43–0,70), `vesuvius-work/runs/EXP-031/seeds.json`.
Aucun résultat de croissance n'était connu lors de l'amendement.

## Hypothèse et critères
**H-036** : sans intervention, ces 9 graines + `out4` donnent ≥ 40 cm² de surface **unique** cumulée, avec une fidélité
médiane ≥ 85 % à 2 voxels, en ≤ 3 h machine au total.
Réfutée si l'une des trois conditions échoue ; attribuer (graines, données, outil, chevauchements).

Lecture (descriptif, pas une hypothèse) : nombre de zones candidates par patch, accord inter-modèles par patch ;
**R1.3 déclenché** seulement si l'inspection privée trouve ≥ 10 formes de lettres candidates dans 4 cm² d'un même
patch (critère du plan).

## Limites connues
Fenêtre unique (≈ 2 600³ voxels, un quadrant du rouleau) ; graines sur la prédiction m7 (peut sauter de feuillet) ;
pas de détection de saut de feuillet dédiée (W2.2) ; deux patchs peuvent couvrir le même feuillet (comptés une fois).

## Confidentialité
Rendus, cartes, zones : `vesuvius-work/runs/EXP-031/` (hors dépôt) ; agrégats seuls versionnés.
