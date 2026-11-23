# PROGRESS

## Phase actuelle
Phase E/F — baseline scientifique et boucle expérimentale (A, B1.1, B2.1-3, B3.1-2, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-015 — TTA reader-v2 répliquée (0009B, 0500P2) et cumulée à la fusion Hecate.

## Dernière tâche validée
H-012 — EXP-015 : soutenue ; `--tta-mirror` (4 variantes) de reader-v2 sur 0841 × 3 : AUC sup. +0,013, AP +0,029, IC apparié AP > 0 sur 3/3, temps inchangé.
Validation :
- `experiments/EXP-015/results.json` ; EXP-014 (H-013 réfutée), EXP-013 (H-014 réfutée), EXP-012 (H-011 réfutée).
- `pytest` 10 passed.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002) ; l'accord inter-modèles n'est pas une preuve d'encre non étiquetée (EXP-005).
- Fenêtre de couches par défaut de reader-v2 conservée (EXP-006) ; indicateurs sans label rejetés (EXP-007).
- Segments étiquetés tenus à l'écart d'objets vus (0009B, 0500P2) = tests indicatifs pour reader-v2, pas inter-rouleaux (EXP-008).
- Probabilités brutes non calibrées (EXP-012) ; cartes en probabilité = fusion calibrée isotone LOO objet (EXP-013), classement/AP = moyenne brute.
- Fusion reader-v2+Hecate = candidate par défaut pour les cartes (gain ≈ +0,02 AP, même signe sur 0841/0009B/0500P2, EXP-003/004/011) ; pas de revendication inter-rouleaux (aucun objet indépendant des deux modèles → E1.5 ou nouveaux labels).
- Leviers post-hoc sans inférence épuisés (EXP-012…014) ; prochains gains via inférence/modèle/données (H-012 TTA soutenue ; H-005, E1.5) ; baseline rapportée = passe unique, TTA = amélioration de chaîne rapportée à part.
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-0{01..15}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006,EXP-008,EXP-015}` ; modèles : `...\models\`
- Tifxyz 9,366 µm 0841 : `vesuvius-work/cache/segments/PHerc0841/<seg>/tifxyz_9.366/`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-015 — Inférer reader-v2 `--tta-mirror` sur 0009B (8,64 µm) et 0500P2 dans `runs/EXP-016/` (lanceur d'EXP-015), puis dans `experiments/EXP-016/` comparer sur les 5 segments rv2 vs rv2-TTA et fusion(rv2, Hecate) vs fusion(rv2-TTA, Hecate) (AP/AUC sup., IC appariés) ; H-015 réfutée si gain AP moyen de la fusion < 0,01.
