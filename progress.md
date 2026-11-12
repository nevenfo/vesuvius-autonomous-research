# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-2, B3, C, D1, G1, G2.1 validés).

## Tâche actuelle
B2.3 — matrice de parenté modèles↔données (préalable à E1.1 et H-009).

## Dernière tâche validée
D1 + E1.1 partiel (EXP-001/001b) et EXP-002, veille G1/G2.1.
Validation :
- `python -m pytest -q` → 10 passed (2026-11-12).
- EXP-001 : reader-v2 et ink_9um s43 sur PHerc0841 × 3 segments → 12/12 AUC publiées reproduites (écart max 1e-4) ; ~30 s/inférence, +1 Go VRAM.
- EXP-002 : fusion reader-v2+ink_9um rejetée (3/3 segments en baisse) ; H-008 soutenue (labels zone `validation` probablement incomplets).
- Tâche `VesuviusResearchWatch` : déclenchement planifié réel 23:37:36, LastTaskResult 0, état `watch/state.json` à jour.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-001/`, `experiments/EXP-002/`, `docs/hypotheses.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
B2.3 — Écrire `docs/data/splits.md` : pour reader-v2 (`train_config.json`), ink_9um (model card) et Hecate, lister rouleaux/segments d'entraînement ; en déduire les segments étiquetés réellement tenus à l'écart par modèle ; valider en recoupant chaque entrée avec sa source.
