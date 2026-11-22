# PROGRESS

## Phase actuelle
Phase E/F — baseline scientifique et boucle expérimentale (A, B1.1, B2.1-3, B3.1, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
B3.2 — audit du protocole après 4 hypothèses réfutées d'affilée (H-004, H-006, H-002, H-007), puis nouvelles hypothèses.

## Dernière tâche validée
H-007 — EXP-009 : métriques géométriques des tifxyz 9,366 µm (étirement, cisaillement, variation des normales) vs erreur locale de reader-v2 sur 0841 → H-007 réfutée.
Validation :
- 938 tuiles : |ρ| < 0,2 pour toutes les métriques, brut et partiel, sur chaque segment — `experiments/EXP-009/results.json`.
- EXP-008 (H-002 réfutée, DiD −0,001) ; EXP-007 (H-006) ; EXP-006 (H-004) ; `pytest` 10 passed.

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
- `experiments/registry.csv`, `experiments/EXP-00{1..9}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006,EXP-008}` ; modèles : `...\models\`
- Tifxyz 9,366 µm 0841 : `vesuvius-work/cache/segments/PHerc0841/<seg>/tifxyz_9.366/`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
B3.2 — Écrire `docs/audit-2026-11-22.md` : contrôle positif de la chaîne tuiles/Brier/ρ partiel d'EXP-007/009 (indicateur synthétique = Brier bruité à niveaux connus, ρ retrouvé ?) et puissance (ρ minimal détectable avec ~300 tuiles autocorrélées), puis ajouter ≥ 3 nouvelles hypothèses classées dans `docs/hypotheses.md` ; validation : contrôle positif retrouve ρ attendu à ±0,05.
