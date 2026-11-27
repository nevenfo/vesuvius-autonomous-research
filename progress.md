# PROGRESS

## Phase actuelle
Refonte du 2026-11-27 faite (S1, J1) + créativité intégrée (X1). Faits aujourd'hui : V1 (EXP-022), W1.1 (EXP-023), W2.1, W2.3 (EXP-025), P1, P2.1, P3.1, R1.1 (EXP-024), T1.1, Y1.1, E1.6, G3.4, K3.1 (EXP-026), X1.1–X1.2, X2.1 (EXP-027), X2.2 (EXP-028), R1.2 (EXP-029).

## Tâche actuelle
R1.4 — contrôle positif de notre chaîne de rendu VC3D tifxyz → surface-volume sur un segment publié à encre connue (PHerc0841 `20260220213127-w00`, tifxyz + inklabels en cache).

## Dernière tâche validée
R1.2 / EXP-029 — chaîne figée sur le patch propre PHerc1218 (4,11 cm²) : H-034 soutenue (ρ inter-modèles 0,278 vs nul p95 0,041 ; ρ intensité ≤ 0,04) mais 0 zone candidate et aucun trait à l'inspection privée ; rendu net (fibres visibles). Absence ininterprétable tant que le rendu propre n'est pas contrôlé positivement.
Validation :
- `experiments/EXP-029/results.json` ; `pytest tests -m "not network"` ; `continuity-check.sh` OK.

## Décisions actives
- Objectif = tout lire, technologie neutre ; métriques pixel = diagnostics ; mesures glyphe (`src/vesres/reading.py`), couverture (`src/vesres/coverage.py`).
- Toute métrique porte sa classe de référence (R0–R4, `ref_class` du registre) ; provenance `docs/data/provenance.csv`.
- 5 segments historiques = rétrospectifs ; test scellé T-1667-READ (`docs/data/sealed_test.md`) ; 1667 est vu par nos modèles (P3.2 si nécessaire).
- Goulot des découvertes = segmentation (EXP-024) ; VC3D `a7d4f88` (Windows natif, GPL-3.0, non redistribué) sous `vesuvius-work/third_party/vc3d/`.
- Rendu propre : `vc_render_tifxyz --scale 1 -g 0 -n 31` → `tifs_to_sv.py` (zarr 2/3) → infer ; ink_9um a un artefact de cadre en bord de rendu (marge 1 mm).
- Exploration sans quota, arbitrée à chaque revue ; génératif = statut max `Probable` ; I-002 suspendue.
- Suspendus : K4/K5 ; opportuniste : N1.1 EXP-021.
- Aucune image d'encre, coordonnée de texte, transcription ou label publié. Prix : aucune éligibilité déclarée ; questions écrites prêtes (matrice §6).

## Blocage actif
Aucun. Décisions humaines (non bloquantes) : M1.4 e-mail des commits ; envoi des questions L1.3/T1.2 ; annotateur P4.2.

## Fichiers / zones utiles
- `plan.md` (phases X, V, W, P, T, R, Y), `docs/research-review-2026-11-27.md` (§4–7), `docs/hypotheses.md`, `experiments/registry.csv`
- `experiments/EXP-02{2..9}/`, `src/vesres/{reading,coverage,eval_ink,watch}.py`
- Runs `vesuvius-work/runs/EXP-02{5,9}/` (EXP-029 : `private/` cartes et zones) (graines, params, logs) ; références privées `vesuvius-work/refs/PHerc1667/`

## NEXT ACTION
R1.4 — préenregistrer EXP-030 (critère : ρ par blocs rendu-propre vs SV publié ≥ 0,7 et AUC sur inklabels à ≤ 0,03 de celle du SV publié), puis `vc_render_tifxyz -v <volume 0841 de done.json> -s cache/segments/PHerc0841/20260220213127-w00/tifxyz_9.366 --scale 1 -g 0 -n 31`, `tifs_to_sv.py`, infer reader-v2-LO, comparaison.
