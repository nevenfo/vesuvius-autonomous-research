# PROGRESS

## Phase actuelle
Refonte stratégique du 2026-11-27 faite (S1) : plan réorganisé autour de la lecture (V chemin bout en bout, W couverture/géométrie, P indépendance, T reconnaissance du texte, Y résolution, R découvertes, H généralisation) ; ancien plan archivé (`docs/plan-archive-2026-11-27.md`). Jalon J1 atteint ; J2–J12 ouverts.

## Tâche actuelle
W1.1 / H-028 — EXP-023 : inventaire de couverture du corpus (surface identifiée par les segments publiés vs estimation physique avec intervalle).

## Dernière tâche validée
V1.2 / EXP-022 — chemin de lecture v0 et lisibilité par unité graphique : H-026 soutenue (contrôles 100 %/0 %), H-027 réfutée (fusion LO+Hecate 5/17 UGR lisibles sur 0841 = 29 % [13-53] ; canon 2,4 µm 11/17, réf. R1) ; références fiables = 7–22 % des segments.
Validation :
- `pytest tests -m "not network"` 17 verts ; `experiments/EXP-022/analyze.py` → `experiments/EXP-022/results.json` (50 s) ; `continuity-check.sh` OK.

## Décisions actives
- Objectif = tout lire, technologie neutre ; métriques pixel = diagnostics ; mesures glyphe (`src/vesres/reading.py`) et couverture d'abord.
- Protocoles : `docs/protocols/{reading-evaluation,coverage,independence,research-loop}.md` ; toute métrique porte sa classe de référence (R0–R4) ; toutes nos références actuelles sont R0/R1.
- Les 5 segments historiques (0841 × 3, 0009B, 0500P2) sont rétrospectifs, plus une validation finale ; test scellé à créer (P3) ; jamais de réglage sur eux.
- Chaîne de référence 9 µm = fusion reader-v2(-LO) + Hecate ; reader-v3 ≈ fusion au niveau glyphe ; canon 2,4 µm nettement supérieur mais circularité non exclue (H-029, Y1).
- Suspendus : K4/K5 (optimisation d'entraînement) ; opportuniste : N1.1 EXP-021 (WSL, seulement machine libre, contention CPU mesurée).
- R1 PHerc0800 découplé de N : après audit L2.2 ; inspecter d'abord les prédictions officielles publiées.
- Venvs `.venv` (outils), `.venv-koine` (inférence/entraînement officiels), `.venv-tex` ; travail hors Git dans `C:\Users\FlowUP\vesuvius-work` (≈ 98 Gio ; C: 229 Gio libres, en baisse).
- Aucune image d'encre, coordonnée de texte, transcription ou label publié ; sorties par UGR dans `vesuvius-work/runs/EXP-022/` (privé).
- Prix : aucune éligibilité déclarée ; questions écrites prêtes (`docs/compliance/vesuvius-challenge-matrix.md` §6), envoi = action humaine.

## Blocage actif
Aucun. Décisions humaines attendues (non bloquantes) : M1.4 (e-mail des commits) ; envoi des questions L1.3 ; annotateur pour P4.2.

## Fichiers / zones utiles
- `plan.md`, `docs/research-review-2026-11-27.md`, `docs/hypotheses.md`, `experiments/registry.csv`
- `src/vesres/{reading,eval_ink,catalog,fetch_segment,watch}.py`, `experiments/EXP-022/`, `experiments/EXP-013/analyze.py` (chargeur des 5 segments)
- Catalogue local `vesuvius-work/cache/catalog/metadata.min.json` ; segments `vesuvius-work/cache/segments/` ; prédictions `vesuvius-work/runs/`

## NEXT ACTION
W1.1 — Écrire `experiments/EXP-023/README.md` (méthode d'estimation physique et critère H-028 avant calcul), puis un script qui lit les méta-données tifxyz (`meta.json`) des segments publiés par rouleau (S3 anonyme) et produit `docs/data/coverage_inventory.{csv,md}` ; valider par deux exécutions identiques.
