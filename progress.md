# PROGRESS

## Phase actuelle
Phase E/F — baseline scientifique et boucle expérimentale (A, B1.1, B2.1-3, B3.1-2, C, D1, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
H-014 — fusion reader-v2+Hecate après calibration croisée (LOO objet) ou par rangs.

## Dernière tâche validée
H-011 — EXP-012 : réfutée ; reader-v2 surestime (ECE sup. 0,12–0,18 sur 0841/0009B/0500P2, p moyen ≈ 0,34 vs prévalence 0,21–0,32), Hecate sous-estime ; isotone CV ≤ 0,035. H-014 ajoutée.
Validation :
- `experiments/EXP-012/results.json` (+ courbes de fiabilité) ; EXP-011 (H-010 +0,023 AP, non robuste).
- `pytest` 10 passed.

## Décisions actives
- Dépôt sur NAS ; venvs `.venv` (outils, torch 2.11) et `.venv-koine` (inférence officielle, torch 2.10) + cache + modèles + runs sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Inférence d'encre = `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f) sans patch ; Hecate = `hecate.py` officiel via `experiments/EXP-003/hecate_run.py` ; évaluation = `vesres.eval_ink` (protocole reader-v2 + AP/F1/IC blocs).
- Métrique primaire pour ces labels : région `supervision` (EXP-002) ; l'accord inter-modèles n'est pas une preuve d'encre non étiquetée (EXP-005).
- Fenêtre de couches par défaut de reader-v2 conservée (EXP-006) ; indicateurs sans label rejetés (EXP-007).
- Segments étiquetés tenus à l'écart d'objets vus (0009B, 0500P2) = tests indicatifs pour reader-v2, pas inter-rouleaux (EXP-008).
- Probabilités brutes non calibrées (EXP-012) : aucun seuil fixe interprété comme probabilité.
- Fusion reader-v2+Hecate = candidate par défaut pour les cartes (gain ≈ +0,02 AP, même signe sur 0841/0009B/0500P2, EXP-003/004/011) ; pas de revendication inter-rouleaux (aucun objet indépendant des deux modèles → E1.5 ou nouveaux labels).
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-0{01..12}/`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006,EXP-008}` ; modèles : `...\models\`
- Tifxyz 9,366 µm 0841 : `vesuvius-work/cache/segments/PHerc0841/<seg>/tifxyz_9.366/`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
H-014 — Dans `experiments/EXP-013/`, comparer sur 0841/0009B/0500P2 (LOO par objet) la fusion moyenne brute à la fusion après calibration isotone de chaque modèle apprise sur les autres objets et à la fusion par rangs (AP/AUC sup. + IC blocs) ; H-014 réfutée si gain AP moyen < 0,01.
