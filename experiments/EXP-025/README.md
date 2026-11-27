# EXP-025 — W2.3 / H-031 : premier segment propre sur un rouleau éligible sans segment publié

**Statut : terminé** — H-031 réfutée de justesse (surface et temps atteints, fidélité 86,7 % < 90 %) ; premier segment propre obtenu sur un rouleau éligible sans segment publié (protocole fixé le 2026-11-27 avant exécution).

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

## Exécution et résultats
- Essai 1 (graine 4132 5644 11620) : échec en 4 s, valeur CT = 0 à la graine. Diagnostic : sur la tranche médiane
  (niveau 3), **seuls 51 % des voxels de la prédiction de surface m7 tombent dans la zone non nulle du CT masqué**
  (bbox CT y 396–674 contre prédiction 360–719) → la graine était dans la prédiction mais hors masque.
- Écart documenté (bug de protocole, pas réglage) : graine contrainte au CT érodé (`seed.py <pred> <out> <ct>`) →
  graine 4324 5292 11620 (CT 106, prédiction 255, 40 % du rayon).
- Essai 2 (`streamline`, 60 générations, 8 threads, volume distant) : **échec après 483 s**, ≈ 36 % des sommets de
  la grille 121 × 121 placés, « No usable CT sheet normal during seed growth ». Attribution probable : **données**
  (la croissance atteint des zones à CT nul — masque plus étroit que le papyrus prédit — ou des normales CT non
  estimables) et **mode** (`streamline` n'utilise pas les normal-grids). Aucune surface publiée par l'outil.
- Constat secondaire important pour la couverture : si le masque du volume officiel exclut du papyrus, toute chaîne
  lisant le volume masqué perd cette surface → à vérifier (W1.2/W2.2) en comparant volume masqué et non masqué.

## Suite (dans le protocole)
Second et dernier essai argumenté : GrowPatch `default` avec les normal-grids officielles (téléchargées localement),
même graine, puis, si échec, réduction à 30 générations pour mesurer au moins une surface ; conclusion H-031 ensuite.
- Essai 3 (`default`, `normal_grid_path` = URL HTTPS publique, `params3.json`) : échec immédiat « normal-grid file not
  found » — l'outil attend un magasin **local** ; structure publique = `metadata.json` + un fichier `.grid` par tranche
  et par plan (`xy/000000.grid`, ≈ 0,6 Mo). Échec d'**entrée d'outil**, pas de méthode : l'essai `default` reste à faire.
- Suite : télécharger une fenêtre des normal-grids autour de la graine (≈ ± 1 500 tranches par plan, ≈ 5 Go, cache
  évictable) et relancer `default` avec le chemin local ; H-031 conclue ensuite.
- Essai 4 (`default`, normal-grids locales, `params4.json`, fenêtre ± 1 300 tranches téléchargée, 4,0 Go, cache
  évictable `vesuvius-work/cache/normal_grids/PHerc1218`) : **succès de l'outil**, patch 122 × 122 nœuds,
  **4,11 cm²** en **475 s** mur (8 threads CPU, volume lu à distance), **0 intervention humaine**.
- Fidélité (1 000 sommets, prédiction de surface niveau 0) : **86,7 %** à ≤ 2 voxels (`fidelity4.json`) ;
  descriptif hors critère : 96,3 % à ≤ 4 voxels (≈ 35 µm, `fidelity4_tol4_descriptif.json`).

## Conclusion
- **H-031 réfutée de justesse** au critère fixé (fidélité < 90 %) ; surface (≥ 4 cm²) et temps (≤ 2 h) atteints.
- Faisabilité démontrée : la chaîne officielle VC3D produit sans intervention, en 8 min sur notre PC, un patch de la
  taille du critère First Letters sur un rouleau éligible sans segment publié. Le mode `streamline` (CT seul) échoue ;
  le mode `default` exige les normal-grids **locales**.
- Limites : fidélité mesurée contre m7 (pas contre le feuillet réel) ; ≈ 13 % des sommets à plus de 2 voxels de m7
  (lissage, trous de m7 ou dérive) ; pas de contrôle de saut de feuillet ; un seul patch, une seule graine.
- Suite (R1.2) : rendre le surface-volume (`vc_render_tifxyz`, 31 couches, `tifs_to_sv.py`), appliquer la chaîne
  d'encre figée propre (reader-v2-LO / ink_9um, n'ayant pas vu 1218), inspection privée ; en parallèle, mesurer
  l'auto-cohérence (H-032) entre deux patchs chevauchants issus de graines voisines.
