# PROGRESS

## Phase actuelle
Refonte du 2026-11-27 faite (S1, J1) + créativité intégrée (X1 : `docs/protocols/research-loop.md` §6, idées I-001…I-008 dans `docs/hypotheses.md`). Faits aujourd'hui : V1 (EXP-022), W1.1 (EXP-023, H-028 indéterminée), P1, P2.1, P3.1, R1.1 (EXP-024), T1.1, W2.1, Y1.1, E1.6, G3.4, K3.1 (EXP-026), X1.1–X1.2.

## Tâche actuelle
Deux unités en parallèle (CPU, pas de contention GPU) : X2.1 / H-032 — EXP-027 (auto-cohérence de rendus redondants de 1667, sous-agent en cours) ; W2.3 / H-031 — EXP-025 (segment propre sur PHerc1218 : streamline échoué, `default` à relancer avec normal-grids locales).

## Dernière tâche validée
W1.1 / EXP-023 — inventaire de couverture déterministe (35 rouleaux) ; estimateur de pas inopérant (H-028 indéterminée) ; somme des segments de 1667 = 2× la surface déroulée publiée.
Validation :
- `pytest tests -m "not network"` 26 verts ; deux exécutions → sha256 identiques ; commit `d95f22f` poussé.

## Décisions actives
- Objectif = tout lire, technologie neutre ; métriques pixel = diagnostics ; mesures glyphe (`src/vesres/reading.py`), couverture (`src/vesres/coverage.py`).
- Toute métrique porte sa classe de référence (R0–R4, `ref_class` du registre) ; provenance `docs/data/provenance.csv`.
- 5 segments historiques = rétrospectifs ; test scellé T-1667-READ (`docs/data/sealed_test.md`) ; 1667 est vu par nos modèles (P3.2 si nécessaire).
- Goulot des découvertes = segmentation (EXP-024) ; VC3D `a7d4f88` (Windows natif, GPL-3.0, non redistribué) sous `vesuvius-work/third_party/vc3d/`.
- Anomalie EXP-025 : 49 % de la prédiction de surface hors CT masqué sur 1218 → I-008 (X2.2).
- Exploration sans quota, arbitrée à chaque revue ; génératif = statut max `Probable` ; I-002 suspendue.
- Suspendus : K4/K5 ; opportuniste : N1.1 EXP-021.
- Aucune image d'encre, coordonnée de texte, transcription ou label publié. Prix : aucune éligibilité déclarée ; questions écrites prêtes (matrice §6).

## Blocage actif
Aucun. Décisions humaines (non bloquantes) : M1.4 e-mail des commits ; envoi des questions L1.3/T1.2 ; annotateur P4.2.

## Fichiers / zones utiles
- `plan.md` (phases X, V, W, P, T, R, Y), `docs/research-review-2026-11-27.md` (§4–7), `docs/hypotheses.md`, `experiments/registry.csv`
- `experiments/EXP-02{2..7}/`, `src/vesres/{reading,coverage,eval_ink,watch}.py`
- Runs `vesuvius-work/runs/EXP-025/` (graines, params, logs) ; références privées `vesuvius-work/refs/PHerc1667/`

## NEXT ACTION
X2.1 — À la fin du sous-agent EXP-027 : vérifier tests, `experiments/EXP-027/results.json` et le verdict H-032, puis consigner (registre, hypothèses, plan) ; ensuite W2.3 : télécharger la fenêtre de normal-grids de PHerc1218 autour de z 11620 et relancer `vc_grow_seg_from_seed` en mode `default` avec le chemin local.
