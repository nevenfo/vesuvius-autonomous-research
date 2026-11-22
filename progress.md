# PROGRESS

## Phase actuelle
Phase E — baseline scientifique (A, B1.1, B2.1-3, B3, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-006 — indicateur sans label des erreurs locales de reader-v2 (PHerc0841, région supervision).

## Dernière tâche validée
H-004 — EXP-006 : fenêtre de 17 couches de reader-v2 décalée de −6 à +5 sur 3 segments 0841 → H-004 réfutée.
Validation :
- 36 inférences exit=0 ; s=0 identique bit à bit à EXP-001/E1 ; défaut optimal sur 2/3 segments, w00 +0,015 à s=+3 (IC recouvrants), oracle moyen +0,005 — `experiments/EXP-006/results.json`.
- EXP-005 (H-008b) : accord inter-modèles non discriminant → H-008 suspendue.
- EXP-004 (H-009) : AUC sup. reader-v2 0,927 sur 0009B (segment tenu à l'écart) ; EXP-003 : Hecate reproduit 6/6 sur 0841.
- `pytest` 10 passed ; veille planifiée opérationnelle.

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
- `experiments/registry.csv`, `experiments/EXP-00{1..6}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006}` ; modèles : `...\models\`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-006 — Créer `experiments/EXP-007/analyze.py` : sur les 3 segments 0841, région supervision, tuiles 64×64 px, erreur locale de reader-v2 = Brier vs labels ; indicateurs sans label = |reader-v2 − Hecate|, entropie reader-v2, écart-type reader-v2 sur s∈{−1,0,+1} (EXP-006) ; Spearman indicateur↔erreur par segment → `results.json` + README ; H-006 réfutée si |ρ| < 0,3 pour tous les indicateurs.
