# PROGRESS

## Phase actuelle
Refonte du 2026-11-27 faite (S1, J1) + créativité intégrée (X1). Faits aujourd'hui : V1 (EXP-022), W1.1 (EXP-023), W2.1, W2.3 (EXP-025), P1, P2.1, P3.1, R1.1 (EXP-024), T1.1, Y1.1, E1.6, G3.4, K3.1 (EXP-026), X1.1–X1.2, X2.1 (EXP-027), X2.2 (EXP-028).

## Tâche actuelle
R1.2 — rendre le surface-volume du patch propre de PHerc1218 (EXP-025 `out4`, 4,11 cm²) et y appliquer la chaîne d'encre figée n'ayant pas vu 1218 (reader-v2-LO, ink_9um), inspection privée des zones candidates.

## Dernière tâche validée
W2.3 / EXP-025 — premier segment propre sur un rouleau éligible sans segment publié (PHerc1218) : 4,11 cm² en 475 s sans intervention (VC3D `default` + normal-grids locales) ; H-031 réfutée de justesse (fidélité à m7 86,7 % < 90 %). X2.1 / EXP-027 — H-032 soutenue (auto-cohérence de rendus redondants, ρ 0,78–0,89).
Validation :
- `pytest tests -m "not network"` 31 verts ; `continuity-check.sh` OK ; `experiments/EXP-025/fidelity4.json`, `experiments/EXP-027/results.json`.

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
R1.2 — `vc_render_tifxyz.exe -v <volume 1218 masqué> -s runs/EXP-025/out4 --scale 1 -g 0 -n 31 --tif-output runs/EXP-029/render`, puis `experiments/EXP-025/tifs_to_sv.py` → `runs/EXP-029/sv.zarr` et inférence `koine_machines.inference.infer` avec `runs/EXP-018/train/ckpt_040000.pth` (reader-v2-LO) ; README EXP-029 (critères écrits avant) ; inspection privée, aucune publication.
