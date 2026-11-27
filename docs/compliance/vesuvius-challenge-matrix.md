# Matrice de compatibilité Vesuvius Challenge (L1, vérifiée le 2026-11-26, actualisée le 2026-11-27 §5–6)

Sources : <https://scrollprize.org/prizes> (non datée, échéance Progress 2026-11-30 affichée),
<https://scrollprize.substack.com/p/a-new-1m-grand-prize-for-2027> (2026-07-15), <https://scrollprize.org/data#licenses>,
<https://dl.ash2txt.org/LICENSE.txt>. Pages suivies par la veille (`rules_pages`, empreinte du texte) : toute
modification déclenche une revue de cette matrice. **Le projet n'est déclaré éligible à aucun prix à ce jour.**

Légende : ✅ satisfait (preuve citée) · 🟡 partiel · ❌ non satisfait · ❔ exigence non confirmée.

## 1. Prix actifs
| Prix | Objet / montant | Échéance | Manuscrits éligibles |
|---|---|---|---|
| Grand Prize 2027 | déroulement complet + lisibilité ≥ 70 % des caractères par colonne, 100 % recto ; 800/100/50/50 k$ | 2027-06-25 | PHerc0125, 0191, 0211, 0257, 0268, 0358, 0800, 0813, 0826, 1203, 1218, 1447, 1545 |
| First Letters | ≥ 10 lettres lisibles dans 4 cm² d'un rouleau jamais lu ; 50 k$/rouleau (5 × 50 k$ sur la page ; « 10 prizes » / 400 k$ ailleurs ❔) | 2027-06-25 | PHerc0125, 0175A, 0175B, 0191, 0257, 0268, 0358, 0483A, 0483B, 0490A, 0490B, 0800, 0813, 0826, 1203, 1218, 1545 |
| Paris 4 Title | titre de PHerc. Paris 4 ; 50 k$ | 2027-06-25 | PHerc. Paris 4 seulement |
| Progress (mensuel) | meilleure contribution du mois ; 20 k$ … 250 $ | 2026-11-30 puis mensuel | aucune restriction |

## 2. Exigences et état du projet
| Exigence (prix) | Source | État | Preuve / écart | Action |
|---|---|---|---|---|
| Aucun chevauchement régions d'entraînement / prédiction (GP, FL) | prizes | 🟡 | parentés tracées (`docs/data/splits.md`) ; aucun modèle évalué sur un rouleau éligible | vérifier pour chaque modèle les rouleaux vus avant toute prédiction sur un rouleau éligible (M3) |
| Pas de données dérivées d'un scan plus résolu du même volume (GP) | prizes | ❔ pour nos chaînes | reader-v2 distillé de la carte canon 2,4 µm (EXP-018 README) → **interdit si appliqué au même volume** | audit de provenance par rouleau cible |
| Datasets/pseudo-labels/checkpoints publiés CC-BY-NC 4.0 (GP) | prizes | ❌ | aucun poids publié ; données hors Git | après prix seulement, sous réserve licence |
| Seeds fixées et rapportées ; runs W&B publics (GP) | prizes | 🟡 | seeds dans manifestes (EXP-018 seed 42) ; W&B désactivé (`WANDB_MODE=disabled`) | activer un W&B public au moment d'un run candidat |
| Pipeline automatisé, ≤ 8 h d'annotation humaine documentée (GP) | prizes | ✅ (aucune annotation) | — | journaliser toute intervention humaine |
| Meshes `tifxyz` par colonne/zone + image programmatique (barre 1 cm, sans retouche) (GP, FL, Title) | prizes | ❌ | formats lus (tifxyz 9,366 µm 0841) mais aucune sortie de ce type | brique d'export d'image programmatique (M2) |
| Méthodologie + image Docker + section faux positifs + validation tenue à l'écart (GP, FL) | prizes | 🟡 | protocoles et validation K (`docs/protocols/`) ; pas de Docker | `Dockerfile` reproductible (M2) |
| Code open source permissif sur GitHub (GP, FL, Progress) | prizes | ✅ | dépôt public MIT depuis 2026-11 | garder `main` présentable (M1) |
| Formats standard OME-Zarr / Zarr / tifxyz / meshes (Progress) | prizes | ✅ | entrées/sorties Zarr/tifxyz/TIFF via outils villa | — |
| Découverte non publique avant annonce officielle (FL) ; texte révélé hors Discord interdit sans accord écrit | prizes, LICENSE | ✅ | invariant licence `plan.md` ; images d'encre hors Git | — |
| Inscription Discord au moment de la soumission ; chef d'équipe soumet | prizes | ❔ | décision et action humaines | à confirmer par l'utilisateur |
| Âge, pays, sanctions, agents IA autonomes | — | ❔ | pages muettes | question écrite aux organisateurs avant soumission |

## 3. Contradiction licence ↔ open source
Les prix exigent code, datasets d'entraînement, pseudo-labels et poids ouverts, alors que `LICENSE.txt` interdit
de publier, hors Discord et sans consentement écrit, texte révélé, transcriptions et **images d'ink labels**
associées, et toute redistribution de données. Aucune page officielle ne concilie les deux.
Position du projet : ne publier ni labels, ni images d'encre, ni données dérivées ; code et protocoles seulement.
Permission à demander (par l'utilisateur, via Discord / GitHub Issues de ScrollPrize) avant toute soumission
comportant des artefacts dérivés de données.

## 4. Implications pour la recherche (cf. `docs/research-review-2026-11-26.md`)
- Nos objets de test (0841, 0009B, 0500P2) ne sont éligibles à aucun prix ; la voie « découverte réelle » passe
  par les rouleaux First Letters / Grand Prize, avec modèles n'ayant vu aucune région de ces rouleaux.
- Progress Prizes : une brique réutilisable mesurée sur données réelles (ex. évaluation sans fuite, détecteur
  non neuronal explicable, export programmatique) est la contribution la plus accessible à court terme.

## 5. Actualisation du 2026-11-27 (recherche ciblée ; formulation exacte de `prizes` à relire, résumé outillé)
| Point | Source | Statut | Effet sur la matrice |
|---|---|---|---|
| First Letters 2026 attribués : 306B, 343 (oct.), 846A, 846B, 211 partiel (nov.) ; reader-v3 majoritaire | <https://scrollprize.org/winners> | V | 0800 reste sans lettre annoncée ; vérifier avant R1 que 0800 est toujours éligible (max 5 rouleaux ❔) |
| Préentraînés et données externes autorisés si licence ; scans plus résolus **du même rouleau** interdits | <https://scrollprize.org/prizes> | V (résumé) | reader-v2/LO distillés de cartes 2,4 µm d'**autres** objets : compatibles a priori pour 0800 ; audit L2.2 requis |
| Données d'entraînement/pseudo-labels publiés CC BY-NC 4.0 ; seeds et runs W&B partagés ; code permissif, publication non requise à la soumission ; divulgation interdite avant annonce | idem | V (résumé) | inchangé : contradiction licence ↔ open source toujours ouverte |
| Aucune règle explicite sur IA générative / agents ni sur recouvrement entraînement/prédiction pour First Letters | idem | V (absence constatée) | reste ❔ → question écrite |
| Grand Prize 2027 : 100 % du recto (fragments détachés inclus, morceaux externes < 10 % omissibles), ≥ 70 % des caractères conservés lisibles par colonne sans interpolation, ≤ 8 h d'intervention humaine | idem + substack 2026-07-15 | V (résumé) | aligne nos métriques : couverture (`docs/protocols/coverage.md`) et lisibilité glyphe (EXP-022) |

## 6. Questions écrites prêtes (L1.3) — envoi = action humaine (Discord officiel ou GitHub Issues ScrollPrize)
1. « Un projet open source (MIT) mené en grande partie par un agent IA supervisé par un humain est-il éligible aux
   First Letters / Grand Prize, l'humain étant le soumissionnaire ? »
2. « Les prix exigent la publication des datasets, pseudo-labels et poids, alors que LICENSE.txt interdit la
   redistribution et la publication d'images d'ink labels sans accord écrit : quelle procédure suivre pour publier
   ces artefacts au moment d'une soumission ? »
3. « Pour First Letters, un modèle entraîné sur des cartes 2,4 µm d'autres rouleaux (pas du rouleau cible) est-il
   conforme à la règle sur les scans plus résolus ? »
4. « La transcription de PHerc. 1667 (arXiv:2606.29085) existe-t-elle alignée sur les segments, et peut-elle être
   utilisée en interne, sans publication, comme référence d'évaluation de lecture ? »
5. « Y a-t-il des restrictions de pays de résidence ou d'âge pour recevoir un prix ? »
