# EXP-023 — W1.1 / H-028 : inventaire de couverture du corpus

**Statut : terminé** — H-028 indéterminée (estimateur de pas inopérant) ; inventaire de surface identifiée produit (méthode et critère fixés le 2026-11-27 avant calcul).

## Obstacle visé
« Lecture intégrale » est invérifiable tant qu'on ignore, par manuscrit, la surface totale et la part déjà
identifiée/reconstruite. Aucune métrique publique de couverture par rouleau n'existe (`docs/research-review-2026-11-27.md` §3).
Alternative moins chère : aucune (méta-données publiques + quelques blocs basse résolution).

## Veille consultée
Recherche ciblée du 2026-11-27 : « ~70 % » de PHerc. 172 déroulé (2025) ; PHerc. 1667 ≈ 1,4 m lus (partie basse
des colonnes) ; Paris 4 « à estimer » ; aucune méthode publiée de mesure de couverture. Impact : ces chiffres servent
de contrôles de vraisemblance, pas de référence.

## Méthode (fixée avant calcul)
Pour chaque rouleau du catalogue `metadata.min.json` (fragments exclus : surface ≈ surface de l'objet, traitée à part) :
1. **Surface identifiée (borne haute)** : somme des `area_cm2` des `meta.json` `tifxyz_original` des segments publiés
   (chevauchements non dédupliqués ⇒ borne haute) ; nombre de segments sans `area_cm2` rapporté.
2. **Volume** : volume OME-Zarr `*-masked.zarr` portant le plus de segments ; non masqué ⇒ estimation « inconnue ».
3. **Enveloppe** : niveau 5 de la pyramide ; par tranche z, aire de `vol > 0` après remplissage des trous ;
   hauteur = étendue z non vide.
4. **Pas des spires** : bandes radiales (largeur 1 bloc) au niveau 2, depuis le centroïde de l'enveloppe vers l'extérieur
   dans 4 directions, à 25/50/75 % de la hauteur ; profil moyenné sur la largeur, tendance retirée ; premier pic
   d'autocorrélation dans [80, 600] µm ; médiane et quartiles sur les bandes valides.
5. **Surface physique estimée** = Σ_z aire_enveloppe(z) / pas × Δz (une face du feuillet), intervalle [p75, p25]
   du pas ; < 6 bandes valides ⇒ « inconnue ».
6. Ratio couverture = identifiée / estimée, avec intervalle ; jamais exprimé sans son intervalle.
Validation de l'estimateur avant usage : test synthétique (spirale d'Archimède de pas connu, bruit) retrouvé à ± 10 %.

## Hypothèse et critère
**H-028** : la surface identifiée (borne haute) est < 50 % de la surface physique estimée pour la majorité des
rouleaux à estimation disponible. Soutenue si `identifiée / estimée_basse` < 0,5 pour > 50 % de ces rouleaux ;
réfutée si `identifiée / estimée_haute` ≥ 0,5 pour > 50 % ; indéterminée sinon.

## Limites connues (avant résultats)
- Segments publiés ≠ tout le travail de segmentation existant (non publié, en cours).
- Chevauchements non dédupliqués ; pas variable avec le rayon et la compression ; enveloppe incluant d'éventuels vides.
- Estimation d'une seule face ; fragments détachés et morceaux externes non distingués.

## Exécution
`python -m vesres.coverage <metadata.min.json> docs/data/coverage_inventory.csv docs/data/coverage_inventory.md experiments/EXP-023/results.json`
(`src/vesres/coverage.py`, `tests/test_coverage.py` 6 tests ; deux exécutions → sha256 identiques ; ≈ 1,9 Go lus et mis
en cache sous `vesuvius-work/cache/coverage`, 25 min la première fois). Écarts d'implémentation listés dans le `.md`
(secours `area_vx2` quand `area_cm2` manque, ≈ 8 % d'écart mesuré sur 0800 ; volumes > 300 M voxels au niveau 5 exclus).

## Résultats
- **Estimateur de pas inopérant** : 0/35 rouleaux estimés ; 28 rouleaux < 6 bandes radiales valides (pas de pic
  d'autocorrélation dans [80, 600] µm sur des profils moyennés de 128 voxels selon ±x/±y), 6 exclus par taille.
  Le test synthétique passait (± 10 %) : l'échec vient de l'hypothèse de spires quasi circulaires/axes x-y, pas du code.
- **H-028 : indéterminée** (aucun rouleau estimé).
- Surface identifiée (borne haute) : PHercParis4 11 391 cm² (54/82 segments sans aire), PHerc0172 7 070, PHerc1667 2 525,
  PHerc0139 1 548, PHerc0814 644, PHerc1447 58, PHerc0841 49, PHerc0800 9,2 ; 16/17 éligibles First Letters : 0.
- **Contrôle de vraisemblance** : 1667 = 2 525 cm² identifiés contre **1 231 cm² réellement déroulés** (arXiv:2606.29085)
  → la somme des segments surestime d'un facteur ≈ 2 (chevauchements) ; elle ne doit jamais être lue comme une couverture.

## Conclusions
- La surface identifiée par somme d'aires est une borne haute très lâche ; une couverture exige la déduplication
  géométrique des segments (union dans le volume) — à faire avant toute affirmation.
- Amendement nécessaire (W1.2) : pas des spires estimé le long des normales locales des segments/prédictions de surface
  (ou FFT 2D locale) au lieu de rayons x/y ; déduplication par union voxélisée des segments.
