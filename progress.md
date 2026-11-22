# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-3, B3, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-008b — test discriminant de l'incomplétude des labels `validation` PHerc0841 avec Hecate (architecture distincte).

## Dernière tâche validée
H-009 — EXP-004 : reader-v2 / ink_9um / Hecate sur le segment étiqueté PHerc0009B (8,64 µm, 116 keV).
Validation :
- AUC sup. reader-v2 0,927 [0,887–0,948] (segment tenu à l'écart, objet vu), Hecate 0,884, ink_9um 0,813 (objet non vu) — `experiments/EXP-004/results.json`.
- Fusion reader-v2+Hecate 0,935 / AP +0,0195 (sous le seuil H-003 de 0,02) ; EXP-003 : Hecate reproduit 6/6 sur 0841, fusion AP +0,025.
- `pytest` 10 passed ; veille planifiée opérationnelle.

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
- `experiments/registry.csv`, `experiments/EXP-00{1,2,3,4}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-008b — Rejouer le test d'accord H-008 d'EXP-002 (`experiments/EXP-002/analyze.py`) avec Hecate (`runs/E1.4/<seg>/pred_hecate.tif`) comme 2e modèle à la place d'ink_9um sur les 3 segments 0841 ; consigner en EXP-005 ; H-008 renforcée si l'accord en zone `validation \ supervision` reste ≫ taux de base (≥ 5×) avec cette architecture distincte.
