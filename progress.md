# PROGRESS

## Phase actuelle
Refonte du 2026-11-27 faite (S1, J1) + créativité intégrée (X1). Faits aujourd'hui : V1 (EXP-022), W1.1 (EXP-023), W2.1, W2.3 (EXP-025), P1, P2.1, P3.1, R1.1 (EXP-024), T1.1, Y1.1, E1.6, G3.4, K3.1 (EXP-026), X1.1–X1.2, X2.1 (EXP-027), X2.2 (EXP-028), R1.2 (EXP-029), R1.4 (EXP-030).

## Tâche actuelle
R1.5 — étendre la surface propre sur PHerc1218 (≥ 40 cm², graines sur plusieurs spires et hauteurs) et y appliquer la chaîne d'encre validée.

## Dernière tâche validée
R1.4 / EXP-030 — contrôle positif du rendu propre sur PHerc0841 w00 : rendu VC3D par défaut = couches inversées (AUC 0,49) ; `--flip-normals` : ρ 0,948, AUC revue 0,825 vs 0,832 (SV publié) → H-035 soutenue (2e essai). R1.2 / EXP-029 refait avec flip : H-034 soutenue (ρ 0,372 vs nul 0,068), 3 taches sans trait, **aucune lettre candidate** sur 4,11 cm².
Validation :
- `experiments/EXP-030/results_flip.json`, `experiments/EXP-029/results_flip.json` ; `pytest tests -m "not network"` 31 verts ; `continuity-check.sh` OK.

## Décisions actives
- Objectif = tout lire, technologie neutre ; métriques pixel = diagnostics ; mesures glyphe (`src/vesres/reading.py`), couverture (`src/vesres/coverage.py`).
- Toute métrique porte sa classe de référence (R0–R4, `ref_class` du registre) ; provenance `docs/data/provenance.csv`.
- 5 segments historiques = rétrospectifs ; test scellé T-1667-READ (`docs/data/sealed_test.md`) ; 1667 est vu par nos modèles (P3.2 si nécessaire).
- Goulot des découvertes = segmentation (EXP-024) ; VC3D `a7d4f88` (Windows natif, GPL-3.0, non redistribué) sous `vesuvius-work/third_party/vc3d/`.
- Rendu propre : `vc_render_tifxyz --scale 1 -g 0 -n 31` **+ `--flip-normals` si normale de grille sortante** (`experiments/EXP-030/orientation.py <tifxyz> <cy> <cx>`) → `tifs_to_sv.py` → infer ; sans flip la chaîne est aveugle. ink_9um : artefact de cadre en bord de rendu (marge 1 mm).
- Tests : `vesuvius-work/.venv` (pytest) ; inférence : `.venv-koine` (zarr 2).
- Exploration sans quota, arbitrée à chaque revue ; génératif = statut max `Probable` ; I-002 suspendue.
- Suspendus : K4/K5 ; opportuniste : N1.1 EXP-021.
- Aucune image d'encre, coordonnée de texte, transcription ou label publié. Prix : aucune éligibilité déclarée ; questions écrites prêtes (matrice §6).

## Blocage actif
Aucun. Décisions humaines (non bloquantes) : M1.4 e-mail des commits ; envoi des questions L1.3/T1.2 ; annotateur P4.2.

## Fichiers / zones utiles
- `plan.md` (phases X, V, W, P, T, R, Y), `docs/research-review-2026-11-27.md` (§4–7), `docs/hypotheses.md`, `experiments/registry.csv`
- `experiments/EXP-02{2..9}/`, `experiments/EXP-030/`, `src/vesres/{reading,coverage,eval_ink,watch}.py`
- Runs `vesuvius-work/runs/EXP-0{25,29,30}/` (EXP-029 valide : `flip/private/`) (graines, params, logs) ; références privées `vesuvius-work/refs/PHerc1667/`

## NEXT ACTION
R1.5 — préenregistrer EXP-031 (H-036 : ≥ 40 cm² propres cumulés sur 1218 sans intervention, fidélité ≥ 85 % à 2 vx ; puis chaîne d'encre orientée) : ~10 graines via `experiments/EXP-025/seed.py` sur 3 hauteurs z et rayons 40–70 %, normal-grids locales étendues aux fenêtres z nécessaires (cache évictable), `vc_grow_seg_from_seed` `params4.json` ; rendu orienté et inférence par patch.
