# EXP-024 — R1 : tri des rouleaux First Letters par surface publiée et signal officiel

**Statut : terminé** — critère de tri non concluant ; constat structurant sur la surface publiée (méthode fixée le 2026-11-27 avant calcul).

## Obstacle visé
Découvertes réelles (J7). L'audit de PHerc0800 (`docs/compliance/target-PHerc0800.md`) montre ≈ 17 cm² publiés et
aucune lettre lisible dans les prédictions officielles : choisir la cible R1 sur la surface disponible et le signal,
pas sur un a priori. Alternative moins chère : aucune (prédictions officielles déjà publiées, ≈ 1 Mo/segment).

## Veille consultée
2026-11-27 (`docs/research-review-2026-11-27.md` §3) : First Letters 2026 attribués sur 306B, 343, 846A, 846B, 211
(partiel), surtout avec reader-v3 → reader-v3 sur segments publiés suffit à révéler des lettres quand le signal existe.

## Méthode
- Rouleaux : liste First Letters de `docs/compliance/vesuvius-challenge-matrix.md` §1 (à revérifier contre la page
  `prizes` : les lauréats 2026 n'y figuraient pas, liste possiblement obsolète) + lauréats 2026 comme **contrôles
  positifs** (lettres lisibles connues publiquement).
- Pour chaque segment ayant une prédiction officielle reader-v3 (catalogue du 2026-11-26) : surface valide (cm²),
  fraction > 0,5, densité de composantes `p ≥ 0,5` de taille glyphe (aire 0,5–15 mm²) par cm².
- Par rouleau : surface publiée totale, surface avec prédiction, densité médiane (segments ≥ 1 cm²).
- Classe de référence R0 (sortie de modèle) : sert **uniquement** à ordonner les cibles ; aucune conclusion de texte.

## Critère d'utilité (fixé avant)
Le tri est jugé informatif si les rouleaux lauréats (contrôles positifs) ont une densité médiane supérieure à la
médiane des rouleaux non lus ; sinon le signal officiel n'est pas un bon critère de tri (résultat négatif consigné).

## Limites
R0 ; densité sensible au bruit et aux fibres ; surfaces publiées ≠ surfaces existantes ; éligibilité à revérifier.

## Exécution
`python experiments/EXP-024/triage.py <catalogue 2026-11-26> <VESRES_WORK> experiments/EXP-024/results.json`
(prédictions reader-v3 officielles, < 10 Mo, privées sous `runs/EXP-024/`).

## Résultats
- **16 des 17 rouleaux éligibles n'ont aucun segment publié** ; seul PHerc0800 en a (6 segments, 17,3 cm² prédits).
  Les lauréats 846A/846B n'ont pas non plus de segment au catalogue ; 306B, 343, 211 en ont un chacun (9–25 cm²).
- Tous les rouleaux éligibles ont en revanche des **représentations géométriques officielles** : prédiction de surface
  (`surface-prediction-zarr`), `normal-grids`, volume VC3D (`ome-zarr-vcd3d`) et, pour 10 d'entre eux, `lasagna`.
- Densité de blobs de taille glyphe (reader-v3, médiane par rouleau) : 0800 2,19/cm² ; lauréats 306B 1,58, 343 3,25,
  211 4,98. Critère « lauréats > éligibles » formellement vrai (3,25 > 2,19) mais **non concluant** : 1 seul rouleau
  éligible mesurable, et un lauréat (306B) sous 0800 → ce signal R0 ne permet pas de trier les cibles.

## Conclusions
- Le goulot des découvertes n'est ni le modèle d'encre ni le tri : c'est la **surface segmentée** des rouleaux
  éligibles. Les lauréats 2026 ont produit leurs propres segments.
- Décision : R1 passe par W2 — produire des segments sur un rouleau éligible à partir des représentations officielles
  (prédiction de surface, normal-grids, lasagna) avec les outils existants (VC3D/villa), puis rendre le
  surface-volume et appliquer la chaîne d'encre figée.
