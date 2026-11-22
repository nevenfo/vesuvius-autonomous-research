# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-3, B3, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-007 — qualité géométrique de surface vs erreurs locales de reader-v2 (PHerc0841).

## Dernière tâche validée
H-002 — EXP-008 : différence de différences reader-v2 − ink_9um entre objets vus par reader-v2 (0500P2 nouveau, 0009B) et 0841 → H-002 réfutée au niveau objet vu / segment tenu à l'écart.
Validation :
- DiD AUC sup. −0,001 (critère < 0,03) ; reader-v2 0,873 [0,833–0,907] sur 0500P2 `20250825181859--1` (absent de `train_config.json`) — `experiments/EXP-008/results.json`.
- EXP-007 (H-006 réfutée) ; EXP-006 (H-004 réfutée) ; `pytest` 10 passed.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002) ; l'accord inter-modèles n'est pas une preuve d'encre non étiquetée (EXP-005).
- Fenêtre de couches par défaut de reader-v2 conservée (EXP-006) ; indicateurs sans label rejetés (EXP-007).
- Segments étiquetés tenus à l'écart d'objets vus (0009B, 0500P2) = tests indicatifs pour reader-v2, pas inter-rouleaux (EXP-008).
- Fusion reader-v2+Hecate non intégrée tant qu'aucun 2e objet indépendant ne la confirme (aucun parmi les labels publiés → E1.5 ou nouveaux labels).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-00{1..8}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006,EXP-008}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-007 — Récupérer les tifxyz (x/y/z.tif) des 3 segments 0841 depuis le bucket, calculer par tuile 64 px (grille EXP-007) des métriques géométriques sans label (distorsion d'aire/étirement local vs pas nominal, variation angulaire des normales), Spearman vs Brier de reader-v2 avec contrôle E[p(1−p)] (`experiments/EXP-009/`) ; H-007 réfutée si |ρ partiel| < 0,3 pour toutes les métriques.
