# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-2, B3, C, D1, G1, G2.1 validés).

## Tâche actuelle
E1.4 — Hecate 9,6 µm sur PHerc0841.

## Dernière tâche validée
B2.3 — `docs/data/splits.md` : seul PHerc0841 est un rouleau étiqueté tenu à l'écart des modèles 9 µm publiés (recoupé avec ink_9um model card, reader-v2 `train_config.json`, Hecate model card).
Validation (dernières preuves techniques) :
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
E1.4 — Télécharger `scrollprize/hecate` (checkpoint 9,6 µm), rééchantillonner les 3 surface-volumes 0841 de 9,366 à 9,6 µm (XY et Z, comme reader-v2 `scripts/infer_with_hecate.py`), inférer, ramener sur la grille 9,366 µm, évaluer avec `vesres.eval_ink` ; valider contre les AUC publiées par reader-v2 pour Hecate (revue 0,8887/0,8013/0,8752 ; supervision 0,9119/0,7841/0,8936), puis fusion reader-v2+Hecate (H-003).
