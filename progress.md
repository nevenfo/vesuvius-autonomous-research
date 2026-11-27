# PROGRESS

## Phase actuelle
Phases E/F/K/N — baseline et boucle expérimentale ; quatre exigences permanentes intégrées le 2026-11-26 (lecture intégrale, état de l'art vivant, efficacité de la chaîne, compatibilité Vesuvius Challenge). Validés : A, B1.1, B2.1-3, B3.1-2, C, D1, E1.2, E1.4, G1, G2.1, G3.1, K1, K2, K3.0, L1.1, M1.1-M1.3, E1.5 ; E1.1 partiel.

## Tâche actuelle
N1.1 / H-022 — EXP-021 : reproduction Korotetskyi & Haindl 2026 sous WSL Ubuntu (`~/korotetskyi2026/code`, venv lock Linux des auteurs, `out_supplied/` = résultats fournis, `out/` vide) ; recalcul section 6 à lancer (machine libre, EXP-018 terminé).

## Dernière tâche validée
E1.5 / H-017 — EXP-018 reader-v2-LO entraîné 40k (`vesuvius-work/runs/EXP-018/train/ckpt_040000.pth`) et évalué : H-017 soutenue (perte AUC sup. 0,008 sur objets vus, 0,027 sur 0841, DiD −0,019).
Validation :
- `run_eval.sh` 5/5 exit 0 ; `analyze.py` → `experiments/EXP-018/results.json` ; `pytest tests/` 12 verts.

## Décisions actives
- Dépôt public MIT sur NAS ; venvs `.venv` (outils, torch 2.11), `.venv-koine` (inférence/entraînement officiels, torch 2.10), `.venv-tex` (N1) + cache, modèles, runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (région `supervision`, IC par blocs).
- Chaîne de référence = fusion moyenne reader-v2+Hecate (EXP-003/004/011) ; leviers post-hoc épuisés (EXP-012…016) ; prédictions officielles 2,4 µm = comparateurs indicatifs (EXP-017).
- Objets de test 0841 × 3, 0009B, 0500P2 : jamais utilisés pour choisir durée, checkpoint, hyperparamètre ou configuration (N1.2 : configuration figée).
- Phase K : validation K = 4 holdouts reader-v2 (0343P ×2, 0172 ×2, `vesuvius-work/data/v2lo_val/`), R = EXP-018 (terminé, checkpoints / 1000 disponibles), δ = 0,01 AUC sup., candidat WSD (`experiments/EXP-020/train_wsd.py`, test GPU 200 it. à faire) ; EXP-019 prêt ; aucune inférence pendant l'entraînement (mesure de débit K3.1).
- Priorités : `docs/research-review-2026-11-26.md` (N1 → N2 → R1 PHerc0800 → K → cascade ; E1.5 fait).
- Pas de job CPU lourd (WSL inclus) pendant un entraînement : débit EXP-018 divisé par ~5 (mesuré).
- `experiments/EXP-018/select.py` renommé `select_segments.py` (masquait le module standard `select`).
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
N1.1 — Sous WSL (cwd local) : `KH=~/korotetskyi2026 WORKERS=12 bash experiments/EXP-021/reproduce_glyphs.sh` (copie du script dans WSL), puis lire `logs/compare.txt` et le MCC moyen ACF+WAV+LRE de `out/fusion_subsets10/report.txt` ; conclure H-022 (± 0,02 de 0,457).
