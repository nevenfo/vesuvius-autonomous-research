# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-3, B3, C, D1, E1.4, G1, G2.1 validés).

## Tâche actuelle
H-009 — reader-v2 / ink_9um / Hecate sur le segment étiqueté PHerc0009B (2e objet, 8,64 µm).

## Dernière tâche validée
E1.4 — EXP-003 : Hecate 9,6 µm sur PHerc0841 × 3 segments ; H-003 testée avec la paire reader-v2+Hecate.
Validation :
- 6/6 AUC Hecate publiées par reader-v2 reproduites (écart max 2e-4) — `experiments/EXP-003/results.json`.
- Fusion moyenne reader-v2+Hecate : AP sup. moyenne 0,765 vs 0,740 (Hecate seul), 2/3 segments ≥ +0,02 → H-003 soutenue, non confirmée (IC recouvrants, FP/ECE non mesurés, parenté Hecate↔0841 NV).
- Acquis antérieurs : EXP-001 (12/12 AUC reader-v2/ink_9um), EXP-002, `pytest` 10 passed, veille planifiée opérationnelle (rapport 2026-11-16 trié).

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002).
- Fusion reader-v2+Hecate non intégrée tant qu'aucun 2e objet indépendant ne la confirme (aucun parmi les labels publiés → E1.5 ou nouveaux labels).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-00{1,2,3}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-009 — Récupérer le segment étiqueté PHerc0009B (8,64 µm, labels 2,401 µm ; `docs/data/README.md`) avec `vesres.fetch_segment`, inférer reader-v2, ink_9um s43 et Hecate (`hecate_run.py` paramétré pour 8,64→9,6 µm), évaluer avec `vesres.eval_ink` + fusion reader-v2+Hecate ; consigner en EXP-004 avec la parenté (reader-v2 intra-objet, ink_9um non vu, Hecate NV) ; échec H-009 si AUC sup. reader-v2 < 0,75.
