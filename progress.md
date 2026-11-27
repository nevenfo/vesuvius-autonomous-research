# PROGRESS

## Phase actuelle
Phases E/F/K/N — baseline et boucle expérimentale ; quatre exigences permanentes intégrées le 2026-11-26 (lecture intégrale, état de l'art vivant, efficacité de la chaîne, compatibilité Vesuvius Challenge). Validés : A, B1.1, B2.1-3, B3.1-2, C, D1, E1.2, E1.4, G1, G2.1, G3.1, K1, K2, K3.0, L1.1, M1.1-M1.3 ; E1.1 partiel.

## Tâche actuelle
- E1.5 / H-017 — EXP-018 : entraînement interrompu le 2026-11-26 à 13212 it. (processus tué), relancé le 2026-11-27 10:58 depuis `ckpt_013000` via la tâche planifiée Windows `VESRES_EXP018` (`vesuvius-work/runs/EXP-018/launch.cmd`, survit à la session) ; ~2,3 it/s, fin estimée ~14:30.
- N1.1 / H-022 — EXP-021 : reproduction sous WSL Ubuntu (`~/korotetskyi2026/code`, venv lock Linux des auteurs) ; recalcul `glyphs run` lancé puis **suspendu (SIGSTOP, PID 1881-1886)** car il divise par 5 le débit d'EXP-018. Reprendre après EXP-018 : `wsl -d Ubuntu --cd "~" -- pkill -CONT -f "glyphs run"` (lancer depuis un cwd local, pas UNC).

## Dernière tâche validée
M1.2 (README anglais) et M1.3 (chemins configurables `VESRES_WORK`, commit `cf4e472`).
Validation :
- `pytest tests/` 12 verts ; `rg "FlowUP|100\.90\.138"` sur *.py/*.sh/*.ps1/*.md hors plan/progress : 0 occurrence ; `bash -n` des scripts OK.

## Décisions actives
- Dépôt public MIT sur NAS ; venvs `.venv` (outils, torch 2.11), `.venv-koine` (inférence/entraînement officiels, torch 2.10), `.venv-tex` (N1) + cache, modèles, runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (région `supervision`, IC par blocs).
- Chaîne de référence = fusion moyenne reader-v2+Hecate (EXP-003/004/011) ; leviers post-hoc épuisés (EXP-012…016) ; prédictions officielles 2,4 µm = comparateurs indicatifs (EXP-017).
- Objets de test 0841 × 3, 0009B, 0500P2 : jamais utilisés pour choisir durée, checkpoint, hyperparamètre ou configuration (N1.2 : configuration figée).
- Phase K : validation K = 4 holdouts reader-v2 (0343P ×2, 0172 ×2, `vesuvius-work/data/v2lo_val/`), R = EXP-018, δ = 0,01 AUC sup., candidat WSD (`experiments/EXP-020/train_wsd.py`, test GPU 200 it. à faire) ; EXP-019 prêt ; aucune inférence pendant l'entraînement (mesure de débit K3.1).
- Priorités : `docs/research-review-2026-11-26.md` (E1.5 → N1 → N2 → R1 PHerc0800 → K → cascade).
- Prix : aucune éligibilité déclarée ; contradiction licence ↔ open source documentée (`docs/compliance/vesuvius-challenge-matrix.md`) ; permissions et Discord = actions humaines.
- Veille : tâche planifiée → `watch/run_watch.ps1` (sans commit) ; rapports analysés et committés en session ; consulter avant toute expérience importante (G3.2).
- Aucune image d'encre / transcription / label publié (licence données).

## Blocage actif
Aucun. Décision humaine attendue (non bloquante) : M1.4, e-mail personnel dans les métadonnées des commits publics.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-0{01..20}/`, `docs/hypotheses.md`, `docs/data/splits.md`, `docs/protocols/training-duration.md`
- `docs/research-review-2026-11-26.md`, `docs/compliance/vesuvius-challenge-matrix.md`, `docs/open-source/audit-2026-11-26.md`, `docs/state-of-the-art/`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Runs : `vesuvius-work/runs/EXP-018/train/` (runner.log, ckpt_*.pth), prédictions antérieures `vesuvius-work/runs/EXP-0*` ; segments étiquetés `vesuvius-work/cache/segments/`

## NEXT ACTION
E1.5 — À `DONE` dans `vesuvius-work/runs/EXP-018/train/runner.log` : `bash experiments/EXP-018/run_eval.sh C:/Users/FlowUP/vesuvius-work/runs/EXP-018/train/ckpt_040000.pth lo` puis `PYTHONPATH=src python experiments/EXP-018/analyze.py C:/Users/FlowUP/vesuvius-work lo experiments/EXP-018/results.json` ; conclure H-017 ; puis reprendre EXP-021 (SIGCONT).
