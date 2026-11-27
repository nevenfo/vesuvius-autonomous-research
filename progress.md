# PROGRESS

## Phase actuelle
Refonte du 2026-11-27 faite (S1, J1). Recherche organisée autour de la lecture : V chemin bout en bout, W couverture/géométrie, P indépendance, T reconnaissance, Y résolution, R découvertes, H généralisation. Faits aujourd'hui : V1 (EXP-022), P1, P2.1, R1.1, T1.1, W2.1, Y1.1, E1.6, G3.4, EXP-024.

## Tâche actuelle
W2.3 / H-031 — EXP-025 : segment propre sur PHerc1218 (éligible, aucun segment publié) avec VC3D `vc_grow_seg_from_seed` (streamline, graine automatique 4132 5644 11620), en cours ; W1.1 / EXP-023 (inventaire de couverture) en cours en parallèle.

## Dernière tâche validée
T1.1 / W2.1 — preprint 1667 lu (transcription Col. 1–22 = référence R3*, 1231 cm² déroulés, 860 cm² écrits, ≈ 25 h d'annotation/spire) ; fiches outils géométriques (VC3D GPL-3.0, archive Windows native).
Validation :
- `pytest tests -m "not network"` 20 verts ; `continuity-check.sh` OK ; commit `881591d` poussé.

## Décisions actives
- Objectif = tout lire, technologie neutre ; métriques pixel = diagnostics ; mesures glyphe (`src/vesres/reading.py`) et couverture d'abord.
- Protocoles `docs/protocols/{reading-evaluation,coverage,independence,research-loop}.md` ; classes de référence R0–R4 dans `experiments/registry.csv` (`ref_class`) ; provenance `docs/data/provenance.csv`.
- 5 segments historiques = rétrospectifs ; test scellé à créer (P3) ; aucun réglage sur eux.
- Goulot des découvertes = segmentation (EXP-024) → W2.3 avant toute inférence R1.2 ; PHerc0800 audité (17 cm², rien de lisible).
- Manuscrit de référence de lecture = PHerc. 1667 (transcription privée `vesuvius-work/refs/PHerc1667/`, jamais publiée).
- Résolution : canon 2,4 µm ≫ 9 µm au niveau glyphe mais référence R1 → H-029 (Y1) sur référence indépendante.
- Suspendus : K4/K5 ; opportuniste : N1.1 EXP-021 (WSL, contention CPU).
- Outils : VC3D `a7d4f88` sous `vesuvius-work/third_party/vc3d/` (non redistribué) ; venvs `.venv`, `.venv-koine`, `.venv-tex`.
- Aucune image d'encre, coordonnée de texte, transcription ou label publié. Prix : aucune éligibilité déclarée ; questions écrites prêtes (matrice §6).

## Blocage actif
Aucun. Décisions humaines (non bloquantes) : M1.4 e-mail des commits ; envoi des questions L1.3/T1.2 ; annotateur P4.2.

## Fichiers / zones utiles
- `plan.md`, `docs/research-review-2026-11-27.md` (§4–6), `docs/hypotheses.md`, `experiments/registry.csv`
- `experiments/EXP-02{2,3,4,5}/`, `src/vesres/{reading,eval_ink,watch,catalog}.py`
- Catalogue courant `vesuvius-work/cache/catalog/metadata.min.2026-11-27.json` ; runs `vesuvius-work/runs/EXP-025/` (graine, params, log, sortie)

## NEXT ACTION
W2.3 — À la fin de `vc_grow_seg_from_seed` (`runs/EXP-025/grow.log`) : lire surface et temps dans `out/pherc1218_seed0/meta.json`, mesurer la fidélité (1 000 sommets vs prédiction de surface niveau 0), conclure H-031 dans `experiments/EXP-025/README.md`.
