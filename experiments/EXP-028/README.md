# EXP-028 — X2.2 / I-008 → H-033 : le masque officiel exclut-il du papyrus ?

**Statut : terminé** — H-033 réfutée (critère fixé le 2026-11-27 avant mesure).

## Origine
Anomalie EXP-025 : sur PHerc1218 (tranche médiane, niveau 3), 49 % des voxels de la prédiction de surface m7 tombent
là où le CT masqué vaut 0. Si le masque ampute du papyrus, toute chaîne lisant le volume masqué perd cette surface
(couverture) ; si ce sont des faux positifs de la prédiction, la graine automatique doit les éviter.

## Méthode
Rouleaux : PHerc1218 et PHerc0800 (8,64 µm, masqués). Niveau 3 (69 µm), 5 tranches à 20/35/50/65/80 % de la hauteur.
Pour chaque voxel de prédiction > 0 hors CT > 0 : distance euclidienne (transformée de distance) au CT > 0 le plus proche.
Classes : « bordure » ≤ 3 voxels (≈ 0,2 mm, ambigu), « proche » 3–15 voxels (≈ 0,2–1 mm), « loin » > 15 voxels (> 1 mm).
Enveloppe : remplissage des trous de CT > 0 ; une prédiction hors masque mais **dans l'enveloppe remplie** indique un
masque troué à l'intérieur du rouleau.

## Hypothèse et critère
**H-033** : ≥ 25 % des voxels de prédiction hors masque sont dans l'enveloppe remplie ou à ≤ 15 voxels du CT masqué
(papyrus plausiblement exclu). Réfutée si < 25 % (prédictions surtout loin, dans l'air). Classe : R0 (prédiction) — une
confirmation visuelle sur le CT brut reste nécessaire avant de conclure à une perte de papyrus.

## Résultats (`results.json`, 5 tranches niveau 3 par rouleau, < 1 min, lecture distante)
| Rouleau | prédiction hors masque | dont ≤ 15 voxels du CT | dont dans l'enveloppe remplie | dont > 1 mm |
|---|---|---|---|---|
| PHerc1218 | 49,3 % | 0,07 % | 0,00 % | 99,9 % |
| PHerc0800 | 32,4 % | 0,05 % | 0,00 % | 99,95 % |

## Conclusions
- **H-033 réfutée** : le masque n'ampute pas le papyrus à sa périphérie ni à l'intérieur ; les voxels de prédiction hors
  masque sont tous loin (> 1 mm) du CT conservé.
- Deux explications restent ouvertes : faux positifs de la prédiction m7 hors du rouleau (support, boîtier, air) ou
  **fragments détachés** retirés par le masque (comptent pour le Grand Prize). Les départager exige le volume non masqué
  (absent du catalogue) → question à ajouter si des fragments détachés deviennent un enjeu de couverture.
- Conséquence pratique : toute graine automatique doit être contrainte au CT masqué (fait, EXP-025 essai 2) ; l'échec
  `streamline` d'EXP-025 n'est donc pas attribuable à une amputation du masque.
