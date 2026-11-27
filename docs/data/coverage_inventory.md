# Couverture par rouleau : surface identifiée vs surface physique estimée (généré, EXP-023 / W1.1)

Source : metadata.min.json

Méthode : `experiments/EXP-023/README.md` (`src/vesres/coverage.py`). Surface identifiée = somme des `area_cm2` des segments publiés (borne haute, chevauchements non dédupliqués) ; surface estimée = Σ_z aire(enveloppe) / pas × Δz (une face), intervalle [p75, p25] du pas. Le ratio n'a de sens qu'avec son intervalle [identifiée/estimée_haute – identifiée/estimée_basse].

Rouleaux : 35 ; estimés : 0 ; H-028 (rouleaux estimés) : 0 avec ratio_haut < 0,5, 0 avec ratio_bas ≥ 0,5 → **indéterminée**. Sous-ensemble avec ≥ 1 segment publié : 0 estimés, 0 / 0 → indéterminée.

## Limites
- Segments publiés ≠ tout le travail de segmentation existant (non publié, en cours).
- Chevauchements non dédupliqués ; pas variable avec le rayon et la compression ; enveloppe incluant d'éventuels vides.
- Estimation d'une seule face ; fragments détachés et morceaux externes non distingués ; fragments (type `fragment`) exclus.
- Écarts d'implémentation : quand `tifxyz_original` (ou son `area_cm2`) est absent, secours = `area_vx2` × pixel² du `tifxyz-transformed` sur le volume utilisé (colonne `n_segments_area_secours` ; écart de ≈ 8 % mesuré sur PHerc0800 : 2,45 vs 2,28 cm²) ; volume limité aux masqués ≤ 10 µm dont le niveau 5 ≤ 300 M voxels (budget réseau), le plus de segments d'abord ; bande valide = pic d'autocorrélation ≥ 0.15, tronçon radial ≥ 64 échantillons ; directions ±x, ±y (axes du volume) ; centroïde de l'enveloppe remplie.
- Rouleaux sans segment publié : identifiée = 0, donc ratio = 0 (trivial) ; voir le sous-ensemble ci-dessus.

| id | volume_utilise | pixel_um | n_segments | n_segments_sans_area | surface_identifiee_cm2 | hauteur_mm | pas_um_median | n_bandes_valides | statut | surface_estimee_cm2 [bas–haut] | ratio [bas–haut] | raison |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PHercParis4 |  |  | 82 | 54 | 11390.6 |  |  | 0 | inconnue | — | — | niveau 5 > 300 M voxels pour tous les volumes candidats |
| PHerc0172 | 20241024131839 | 7.91 | 53 | 0 | 7069.89 | 164.78 | 120.3 | 1 | inconnue | — | — | 1 bandes valides < 6 |
| PHerc0139 | 20250728140407 | 9.362 | 39 | 1 | 1548.25 | 195.93 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc1667 | 20251217075048 | 2.399 | 20 | 0 | 2524.82 | 85.67 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0814 | 20250804134230 | 9.362 | 19 | 0 | 643.8 | 174.06 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc1447 | 20250521151220 | 8.64 | 15 | 1 | 58.27 | 210.12 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0800 | 20250521135224 | 8.64 | 6 | 0 | 9.2 | 210.12 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0841 | 20250821151531 | 9.366 | 3 | 0 | 49.43 | 181.93 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0332 | 20251211183505 | 2.399 | 2 | 2 | 0.0 | 74.08 | 121.2 | 1 | inconnue | — | — | 1 bandes valides < 6 |
| PHercMAN5 | 20260311104824 | 2.399 | 1 | 1 | 0.0 | 70.01 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0125 | 20250821151825 | 9.362 | 0 | 0 | 0.0 | 188.44 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0175A | 20250521115057 | 8.64 | 0 | 0 | 0.0 | 110.32 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0175B | 20250521125822 | 8.64 | 0 | 0 | 0.0 | 137.41 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0191 | 20250821151635 | 9.362 | 0 | 0 | 0.0 | 171.06 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0211 | 20250821151803 | 9.362 | 0 | 0 | 0.0 | 176.16 | 184.4 | 1 | inconnue | — | — | 1 bandes valides < 6 |
| PHerc0257 | 20250821151750 | 9.362 | 0 | 0 | 0.0 | 169.86 | 175.1 | 1 | inconnue | — | — | 1 bandes valides < 6 |
| PHerc0268 | 20251110183117 | 8.64 | 0 | 0 | 0.0 | 126.63 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0306B | 20250521133212 | 8.64 | 0 | 0 | 0.0 | 137.41 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0343 | 20250521140437 | 8.64 | 0 | 0 | 0.0 | 155.66 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0358 | 20250821151737 | 9.362 | 0 | 0 | 0.0 | 134.81 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0483A | 20250521140913 | 8.64 | 0 | 0 | 0.0 | 137.41 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0483B | 20251124083638 | 8.64 | 0 | 0 | 0.0 | 95.39 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0490A | 20250521151210 | 8.64 | 0 | 0 | 0.0 | 101.19 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0490B | 20250521151215 | 8.64 | 0 | 0 | 0.0 | 92.07 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0813 | 20250821151723 | 9.362 | 0 | 0 | 0.0 | 145.6 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0826 | 20250821151701 | 9.362 | 0 | 0 | 0.0 | 158.48 | 106.9 | 3 | inconnue | — | — | 3 bandes valides < 6 |
| PHerc0846A | 20250728152254 | 9.362 | 0 | 0 | 0.0 | 131.52 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc0846B | 20250804142305 | 9.362 | 0 | 0 | 0.0 | 125.23 | 101.7 | 1 | inconnue | — | — | 1 bandes valides < 6 |
| PHerc1203 | 20250820131727 | 9.362 | 0 | 0 | 0.0 | 171.06 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc1218 | 20250521120456 | 8.64 | 0 | 0 | 0.0 | 201.0 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc1299 |  |  | 0 | 0 | 0.0 |  |  | 0 | inconnue | — | — | niveau 5 > 300 M voxels pour tous les volumes candidats |
| PHerc1451 | 20250521151225 | 8.64 | 0 | 0 | 0.0 | 155.66 |  | 0 | inconnue | — | — | 0 bandes valides < 6 |
| PHerc1545 | 20250821151648 | 9.362 | 0 | 0 | 0.0 | 189.64 | 180.1 | 1 | inconnue | — | — | 1 bandes valides < 6 |
| PHercMANB |  |  | 0 | 0 | 0.0 |  |  | 0 | inconnue | — | — | niveau 5 > 300 M voxels pour tous les volumes candidats |
| PHercParis3 |  |  | 0 | 0 | 0.0 |  |  | 0 | inconnue | — | — | niveau 5 > 300 M voxels pour tous les volumes candidats |
