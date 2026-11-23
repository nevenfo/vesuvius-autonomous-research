# PROGRESS

## Phase actuelle
Phase E/F — baseline scientifique et boucle expérimentale (A, B1.1, B2.1-3, B3.1-2, C, D1, E1.2, E1.4, G1, G2.1 validés ; E1.1 partiel).

## Tâche actuelle
E1.5 — cadrage du ré-entraînement leave-one-scroll-out (seule voie vers un test indépendant).

## Dernière tâche validée
B1.2 (partiel, labels) — `metadata.json` officiel : labels 20260918 « reviewed », reportés (`transferred`) depuis `philodemos/datasets/ink/ink_030927`, alignement calé sur rendu canonique + prédiction (résidu 0,005–0,015 px, négligeable) ; modèle de pseudo-labeling non publié → EXP-017 indicatif. E1.2 cochée (EXP-017).
Validation :
- `docs/data/splits.md` § Provenance ; EXP-017 (`results.json`) ; `pytest` 10 passed.

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
- Veille : tâche planifiée → `watch/run_watch.ps1` (ASCII, PowerShell 5.1), sans commit ; rapports `watch/reports/` analysés et committés en session.
- Aucune image d'encre / transcription publiée (licence données).

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `experiments/registry.csv`, `experiments/EXP-0{01..17}/`, `docs/data/scoping-2.4um.md`, `docs/hypotheses.md`, `docs/data/splits.md`
- `src/vesres/{fetch_segment,eval_ink,watch,remote_tiff,catalog}.py`
- Prédictions locales : `C:\Users\FlowUP\vesuvius-work\runs\{EXP-001,E1,E1.4,EXP-004,EXP-006,EXP-008,EXP-015,EXP-016,EXP-017}` ; modèles : `...\models\`
- Tifxyz 9,366 µm 0841 : `vesuvius-work/cache/segments/PHerc0841/<seg>/tifxyz_9.366/`
- Code reader-v2 (référence protocole) : `github.com/DomRusso2/reader-v2` `scripts/v2_run.py`

## NEXT ACTION
E1.5 — Chiffrer dans `docs/` le ré-entraînement LOSO de la recette ink_9um (`aligned21_hybrid_3d2d.json`, villa) : données d'entraînement à télécharger (Go), durée GPU estimée sur RTX 5080 (mesurer quelques centaines d'itérations), rouleaux tenus à l'écart candidats (0841 + 0500P2/0009B) ; décision go/no-go à faire valider par l'utilisateur (coût ressources).
