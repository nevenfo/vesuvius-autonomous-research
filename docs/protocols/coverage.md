# Protocole de mesure de la couverture (2026-11-27)

But : savoir à tout moment ce qui, dans chaque manuscrit, est identifié, reconstruit, examiné, lu, incertain,
non traité ou inaccessible — sans jamais déclarer 100 % quand la surface totale est inconnue.

## 1. Catégories (surfaces en cm², avec bornes)
| Catégorie | Définition opérationnelle actuelle | Source |
|---|---|---|
| Volume disponible | scans publiés (résolution, énergie, emprise) | catalogue `metadata.min.json` |
| Surface estimée du manuscrit | estimation physique avec intervalle (ex. aire de section annulaire × hauteur / pas des spires ; ou longueur déroulée publiée) | W1 (méthode et hypothèses écrites) |
| Surface identifiée | union des segments publiés (tifxyz), chevauchements non dédupliqués ⇒ borne haute | méta des segments |
| Surface reconstruite | segments rendus en surface-volume | catalogue (`layers*`) |
| Surface examinée | pixels valides passés par une chaîne d'encre avec trace | manifestes EXP |
| Référence fiable | région `supervision` (labels revus) | ink-labels |
| Revue sans référence fiable | `validation` seule (encre non étiquetée possible, EXP-002/005) | ink-labels |
| Encre potentielle / sans encre détectée | carte d'encre seuillée **avec** classe d'incertitude | chaîne |
| Lisible / partiellement / incertain | UGR lisibles (AUC locale ≥ 0,90), 0,80–0,90, < 0,80 | `reading.py` |
| Non traitée | identifiée mais non examinée | différence |
| Inaccessible actuellement | zones sans segment (compression, cassures) | W2 |
| Perte potentielle d'information | uniquement sur preuve physique (ex. lacune visible dans le volume), jamais par défaut | — |

Règles : non examiné ≠ vide ; sans encre détectée ≠ sans texte ; inaccessible ≠ irrécupérable.

## 2. Défauts à détecter
Trous entre segments, doublons/chevauchements (même papyrus rendu deux fois), changements de feuillet (sheet
switches), zones exclues par un filtre de sélection, pertes de transformation (rééchantillonnage, aplatissement).
Outils existants d'abord (windcheck, TIFXYZ Doctor, vérification de cohérence des enroulements primée en 2026) ;
outil propre seulement si leur insuffisance est démontrée.

## 3. Sorties
- Par segment : tableau `reading.coverage` (segment / référence fiable / revue non fiable / non revue) + catégories
  de lisibilité (EXP-022).
- Par manuscrit : `docs/data/coverage_inventory.{csv,md}` (W1) — surface identifiée (borne haute), reconstruite,
  examinée par nous, estimation physique avec intervalle, ratio avec intervalle, inconnues.
- Toute couverture se lit « surface examinée / surface estimée [intervalle] », jamais en pourcentage seul.
