# EXP-023 — W1.1 / H-028 : inventaire de couverture du corpus

**Statut : en cours** (méthode et critère fixés le 2026-11-27 avant calcul).

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
