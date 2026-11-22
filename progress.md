# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-3, B3, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-002 — circularité labels/modèles : différence de différences sur 0500P2.

## Dernière tâche validée
H-006 — EXP-007 : indicateurs sans label (désaccord Hecate, entropie, instabilité ±1 couche) vs erreur locale de reader-v2 sur 0841 → H-006 réfutée dans sa forme informative.
Validation :
- 938 tuiles supervision : entropie ρ 0,74 brut vs Brier, mais |ρ| ≤ 0,25 sur tout segment une fois E[p(1−p)] contrôlé ; désaccord Hecate 0,14 brut poolé — `experiments/EXP-007/results.json` (contrôles ajoutés a posteriori, déclarés).
- EXP-006 (H-004 réfutée) : fenêtre par défaut optimale sur 2/3 segments, oracle +0,005 AUC.
- `pytest` 10 passed.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002) ; l'accord inter-modèles n'est pas une preuve d'encre non étiquetée (EXP-005).
- Fenêtre de couches par défaut de reader-v2 conservée (EXP-006) ; pas de recentrage par segment.
- Fusion reader-v2+Hecate non intégrée tant qu'aucun 2e objet indépendant ne la confirme (aucun parmi les labels publiés → E1.5 ou nouveaux labels).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-00{1..7}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-002 — Récupérer le segment étiqueté PHerc0500P2 `20250825181859--1` en 9,362 µm (`vesres.fetch_segment`, comme 0009B en EXP-004), inférer reader-v2 et ink_9um, évaluer AUC/AP avec `vesres.eval_ink`, consigner en EXP-008 ; écart d'AUC (reader-v2 − ink_9um) sur 0500P2 moins le même écart sur 0841 (EXP-001) = avantage « vu » ; H-002 réfutée si < 0,03.
