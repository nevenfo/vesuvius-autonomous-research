# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-3, B3, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-004 — sensibilité de reader-v2 au décalage de la fenêtre de couches (PHerc0841).

## Dernière tâche validée
H-008b — EXP-005 : l'accord inter-modèles (reader-v2/Hecate/ink_9um) sur le non-étiqueté ne discrimine pas des labels incomplets.
Validation :
- Lift reader-v2→Hecate 12–13× en `validation \ supervision` mais 11–37× en supervision à > 8 px de l'encre étiquetée — `experiments/EXP-005/results.json` ; H-008 rétrogradée « suspendue ».
- EXP-004 (H-009) : AUC sup. reader-v2 0,927 sur 0009B (segment tenu à l'écart) ; EXP-003 : Hecate reproduit 6/6 sur 0841.
- `pytest` 10 passed ; veille planifiée opérationnelle.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002) ; l'accord inter-modèles n'est pas une preuve d'encre non étiquetée (EXP-005).
- Fusion reader-v2+Hecate non intégrée tant qu'aucun 2e objet indépendant ne la confirme (aucun parmi les labels publiés → E1.5 ou nouveaux labels).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-00{1..5}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-004 — Inférer reader-v2 sur les 3 segments 0841 avec la fenêtre de 17 couches décalée de −6 à +5 (`koine_machines.inference.infer --layer-start 6+s --layer-end 23+s`, défaut s=0 = couches 6–22 sur 28), évaluer AUC/AP supervision par décalage avec `vesres.eval_ink`, consigner en EXP-006 ; H-004 réfutée si l'AUC optimale par segment dépasse celle de s=0 de moins de 0,01.
