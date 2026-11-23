# PROGRESS

## Phase actuelle
Phase E/F — baseline scientifique et boucle expérimentale (A, B1.1, B2.1-3, B3.1-2, C, D1, E1.2, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
E1.5 / H-017 — reader-v2-LO (EXP-018) : entraînement 40k en cours (lancé 2026-11-23, ≈ 4 it/s, ≈ 2 h 45).

## Dernière tâche validée
EXP-018 préparation — corpus reader-v2-LO complet (38/38 segments, 60 Go, `vesuvius-work/data/v2lo/`), test de fumée 60 itérations OK (perte finie), entraînement complet lancé ; `.venv-koine` complété (wandb, accelerate, diffusers… — `experiments/EXP-018/env-koine-train.lock`).
Validation :
- `data/v2lo_build.log` (38 labels `done`) ; `runs/EXP-018/smoke/train.log` rc=0 ; `runs/EXP-018/train/train.log` itérations à 4 it/s.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002) ; l'accord inter-modèles n'est pas une preuve d'encre non étiquetée (EXP-005).
- Fenêtre de couches par défaut de reader-v2 conservée (EXP-006) ; indicateurs sans label rejetés (EXP-007).
- Segments étiquetés tenus à l'écart d'objets vus (0009B, 0500P2) = tests indicatifs pour reader-v2, pas inter-rouleaux (EXP-008).
- Probabilités brutes non calibrées (EXP-012) ; cartes en probabilité = fusion calibrée isotone LOO objet (EXP-013), classement/AP = moyenne brute.
- Fusion reader-v2+Hecate = candidate par défaut pour les cartes (gain ≈ +0,02 AP, même signe sur 0841/0009B/0500P2, EXP-003/004/011) ; pas de revendication inter-rouleaux (aucun objet indépendant des deux modèles → E1.5 ou nouveaux labels).
- Leviers post-hoc sans inférence épuisés (EXP-012…014) ; prochains gains via inférence/modèle/données (H-005, E1.5) ; TTA utile seulement sur objet non vu sans Hecate (EXP-015/016) ; chaîne de référence = fusion moyenne reader-v2+Hecate passe unique.
- Prédictions officielles publiées (canon 2,4 µm, reader-v3, argus-v3) = comparateurs indicatifs tant que la provenance des labels n'est pas établie (EXP-017).
- E1.5 approuvé par l'utilisateur (2026-11-23) : reader-v2-LO = recette reader-v2 sans 0009B/0500P2, init ink_9um s43 60k, quotas proportionnels (EXP-018/README).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-0{01..17}/`, `docs/data/scoping-2.4um.md` ; corpus LO `vesuvius-work/data/v2lo/` (log `data/v2lo_build.log`), `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006,EXP-008,EXP-015,EXP-016,EXP-017}` ; modèles : `...\models\`
- Tifxyz 9,366 µm 0841 : `vesuvius-work/cache/segments/PHerc0841/<seg>/tifxyz_9.366/`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
E1.5 — À la fin de `runs/EXP-018/train/train.log` (`rc=0`, checkpoint 40000 dans `runs/EXP-018/train/`), lancer `bash experiments/EXP-018/run_eval.sh <ckpt_40000> lo` puis `PYTHONPATH=src python experiments/EXP-018/analyze.py C:/Users/FlowUP/vesuvius-work lo experiments/EXP-018/results.json` et conclure H-017 ; si le run a planté, reprendre depuis le dernier checkpoint (`checkpoint` + `weights_only: false`).
