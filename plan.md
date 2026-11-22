# PLAN — VESUVIUS AUTONOMOUS RESEARCH

## Objectif final
Construire, valider et faire progresser une chaîne informatique ouverte de bout en bout
(scan → feuilles → déroulement → encre → localisation → transcription assistée → incertitudes)
capable de lire virtuellement, aussi exhaustivement et fiablement que physiquement possible,
de nouveaux manuscrits du Vesuvius Challenge, sans dépendre d'un rouleau particulier.
« Lecture intégrale » = toute la surface récupérable reconstruite et examinée, observations,
lectures incertaines, restaurations hypothétiques et zones irrécupérables explicitement distinguées.

## Invariants
- Science avant spectacle : texte détecté par modèle ≠ texte déchiffré ≠ lecture papyrologique validée.
- État de l'art et réutilisation avant toute innovation ; une nouvelle méthode exige un besoin démontré
  et un gain mesuré contre une référence, sur données séparées.
- Évaluation par rouleau tenu à l'écart : jamais de split naïf de patches d'un même rouleau/zone ;
  parentés données/labels/pseudo-labels/modèles tracées (`docs/data/splits.md`).
- Licence données (dl.ash2txt.org/LICENSE.txt + CC BY-NC 4.0 + EduceLab) : aucune révélation de
  texte caché (transcription, image d'encre, label) publiée hors Discord officiel sans accord écrit
  de Vesuvius Challenge ; aucune redistribution de données ; citation EduceLab-Scrolls pour Scrolls 1-4/Frag 1-6.
  Les images d'encre restent hors Git (`.gitignore`) et hors dépôt public.
- Code original sous MIT (`LICENSE`) ; code/poids tiers gardent leur licence ; jamais d'imposition MIT à du tiers.
- Stockage : aucun volume complet sans justification écrite ; accès par régions (HTTP Range, OME-Zarr) ;
  cache évictable local `C:\Users\FlowUP\vesuvius-work\cache` (budget ≤ 150 Go) ; dépôt Git léger sur le NAS ;
  artefacts uniques jamais supprimés par politique automatique.
- PC personnel : calculs interruptibles, reprise sans corruption (écritures atomiques), VRAM ≤ ~12 Go
  par défaut pour laisser l'usage normal ; pas de service système nouveau sans bénéfice démontré.
- Confirmation humaine requise : dépense, action destructive/irréversible, modification système/réseau
  importante, exposition de secret, publication externe, annonce de découverte, PR upstream, dépôt public.
- Chaque résultat porte un identifiant stable `EXP-NNN` et un manifeste (données, coordonnées, code, modèle,
  paramètres, date, matériel, métriques, limites, niveau de validation) dans `experiments/`.

## Critères globaux de réussite (jalons, sur preuve uniquement)
- J1 État de l'art comparé et vérifiable (`docs/state-of-the-art/`).
- J2 Une baseline réelle reproduite et évaluée sur notre matériel.
- J3 Pipeline de bout en bout produisant des sorties traçables.
- J4 Nouvelle lecture intégrale de la portion récupérable d'un rouleau confirmée par des spécialistes.
- J5 Performances reproductibles sur ≥ 3 rouleaux indépendants.
- J6 Traitement systématique des manuscrits éligibles avec lectures ou diagnostics.
- J7 Recherche et veille périodiques actives alimentant les expériences.

# Phase A — Inspection et fondations

## A1 — Inspection de l'existant
### Objectif
Connaître matériel, outils, projets existants et contexte antérieur avant toute création.
### Dépendances
Aucune.
### Tâches
- [x] A1.1 Vérifier identité/capacités PC (DESKTOP-0JR01AG, RTX 5080 16 Go, 31 Go RAM, C: 475 Go libres, WSL Ubuntu GPU OK).
- [x] A1.2 Vérifier stockage NAS via partage `Y:` (278 Go libres) ; aucun projet Vesuvius préexistant (fd, gh repo list).
- [x] A1.3 Lire le Second Brain ciblé (`wiki/concepts/envie-contribution-vesuvius-challenge.md`).
### Validation
Relevés `nvidia-smi`, `Get-PSDrive`, `wsl nvidia-smi -L`, `gh repo list | rg vesuv` vide, 2026-11-12.

## A2 — Dépôt et continuité
### Objectif
Dépôt Git versionné, poussé sur un remote GitHub privé, avec plan/progress conformes.
### Dépendances
A1.
### Tâches
- [x] A2.1 `git init`, `.gitignore` (données/poids/images d'encre exclus), `LICENSE` MIT, structure `src/ tests/ docs/ experiments/ watch/`.
- [x] A2.2 Créer le remote GitHub privé `nevenfo/vesuvius-autonomous-research`, pousser `main` puis travailler sur `ai/<phase>`.
### Validation
`bash ~/.agents/continuity-check.sh .` PASS ; `gh repo view --json visibility` = PRIVATE ; `git status` propre après push.

# Phase B — Audit scientifique

## B1 — État de l'art
### Objectif
Synthèse traçable des méthodes, modèles, résultats, limites et inconnues, sources datées.
### Dépendances
A1.
### Tâches
- [x] B1.1 Revue initiale (villa, VC3D, Lasagna, spiral fitting, ScrollFiesta, modèles d'encre, autoresearch, PHerc. 1667, problèmes ouverts 2026) → `docs/state-of-the-art/2026-11-12.md`.
- [ ] B1.2 Vérifier sur sources primaires les points marqués « non vérifié » utiles à la décision courante (licences VC3D/lasagna, données d'entraînement de reader-v2, nature humaine/pseudo des ink-labels 20260918).
### Validation
Chaque affirmation du document porte une URL et un statut (vérifié / auto-déclaré / non vérifié).

## B2 — Inventaire du corpus
### Objectif
Catalogue déterministe et régénérable des 45 échantillons, répondant : références, généralisation, opportunités.
### Dépendances
A1.
### Tâches
- [x] B2.1 `src/vesres/catalog.py` génère `docs/data/corpus_inventory.{csv,md}` depuis `metadata.min.json` officiel.
- [x] B2.2 Lister les segments avec `ink-labels` (PHerc0139, 0814, 0841, 1667, Paris4, 0500P2, 0009B) → `docs/data/README.md`.
- [x] B2.3 Politique de splits par rouleau et matrice de parenté modèles↔données (`docs/data/splits.md`) : seul PHerc0841 est un rouleau étiqueté tenu à l'écart des modèles 9 µm publiés.
### Validation
`python -m vesres.catalog` reproduit les fichiers à l'identique ; test `tests/test_catalog.py` PASS.

## B3 — Hypothèses classées
### Objectif
Liste priorisée d'hypothèses falsifiables (impact, coût, incertitude).
### Dépendances
B1, B2.
### Tâches
- [x] B3.1 Rédiger `docs/hypotheses.md` (H-001…).
### Validation
Chaque hypothèse a référence, données, métrique, critère d'échec, coût estimé.

# Phase C — Environnement reproductible

## C1 — Environnement Python/CUDA
### Objectif
Environnement isolé, réversible, versionné, compatible sm_120.
### Dépendances
A1.
### Tâches
- [x] C1.1 venv uv Python 3.12 hors NAS (`C:\Users\FlowUP\vesuvius-work\.venv`), torch 2.11.0+cu128, matmul GPU OK.
- [x] C1.2 `pyproject.toml` + `requirements.lock` ; env d'inférence séparé `.venv-koine` (torch 2.10.0+cu128, koine_machines + vesuvius 0.2.4 en --no-deps) figé dans `experiments/EXP-001/env-koine.lock`.
### Validation
`python -c "import torch; torch.cuda.is_available()"` True ; `pytest` PASS ; lockfile commité.

## C2 — Accès aux données par région
### Objectif
Lire des crops de surface-volumes distants (TIFF Range / OME-Zarr) avec cache atomique et provenance.
### Dépendances
C1.
### Tâches
- [x] C2.1 `src/vesres/remote_tiff.py` (bandes de lignes via HTTP Range sur TIFF non compressés).
- [x] C2.2 Lecteur OME-Zarr distant (zarr/fsspec, S3 anonyme) pour `layers-zarr` et `ink-labels`.
- [x] C2.3 Tests unitaires (TIFF synthétique local, cache, bornes) ; test réseau manuel validé (crop Frag1).
### Validation
`pytest -m "not network"` PASS ; lecture d'un crop réel identique à la lecture complète sur une petite zone.

# Phase D — Premier chemin vertical

## D1 — Inférence zéro-shot d'un modèle d'encre publié sur un crop étiqueté tenu à l'écart
### Objectif
Petit échantillon réel → chargement vérifié → modèle existant → carte de probabilité → métriques contre labels → manifeste EXP-001.
### Dépendances
C1, C2.
### Tâches
- [x] D1.1 Choisir le crop (PHerc0841, rouleau déclaré non vu par reader-v2 ; layers-zarr 9.366 µm + ink-labels 2.403 µm rééchantillonnés) et figer les coordonnées.
- [x] D1.2 Télécharger le checkpoint (reader-v2 et/ou scrollprize/ink_9um), vérifier licence et empreinte.
- [x] D1.3 Inférence locale (VRAM/temps mesurés), AUC/AP/F1 vs labels, manifeste `experiments/EXP-001/`.
### Validation
Manifeste complet ; métriques recalculables par `python -m vesres.eval` ; comparaison chiffrée à la valeur auto-déclarée (AUC 0,824 vs labels humains sur PHerc0841).

# Phase E — Baseline scientifique

## E1 — Reproduction contrôlée
### Objectif
Reproduire une méthode officielle et comparer aux résultats connus, limites matérielles identifiées.
### Dépendances
D1.
### Tâches
- [ ] E1.1 Étendre D1 à plusieurs segments/rouleaux étiquetés (0139, 0814, 1667, Paris4) en respectant les parentés d'entraînement. (0841 × 3 segments fait : EXP-001b ; 0009B segment étiqueté fait : EXP-004.)
- [ ] E1.2 Comparer ink_9um vs reader-v2 vs pipeline 2,4 µm (`vesuvius.ink_detection`) sur mêmes crops.
- [x] E1.4 Hecate 9,6 µm (MIT) sur les 3 segments 0841 (rééchantillonnage 9,366→9,6 µm exigé par la model card) ; tester H-003 avec ce partenaire. (EXP-003 : 6/6 AUC reproduites ; H-003 soutenue.)
- [ ] E1.5 Ré-entraînement leave-one-scroll-out (recette `aligned21_hybrid_3d2d.json`) si nécessaire pour disposer de ≥ 3 rouleaux de test indépendants (J5).
- [ ] E1.3 Reproduction partielle PHerc. 1667 (crop représentatif, 2,4 µm) vs prédictions publiées.
### Validation
Tableau comparatif avec seeds, coûts, variance ; baseline déclarée validée seulement si sorties et métriques contrôlées.

# Phase F — Expérimentation autonome

## F1 — Boucle expérimentale
### Objectif
Enchaîner hypothèse → protocole → expérience → comparaison → décision, sans boucle improductive.
### Dépendances
E1, B3.
### Tâches
- [ ] F1.1 Registre `experiments/registry.csv` + gabarit de manifeste + règle d'arrêt (3 essais sans gain → audit métrique/protocole).
- [ ] F1.2 Exécuter l'hypothèse la mieux classée de `docs/hypotheses.md`.
### Validation
Chaque EXP a manifeste, conclusion (intégrer/rejeter/suspendre) et lien vers hypothèse.

# Phase G — Veille scientifique

## G1 — Détection incrémentale des changements
### Objectif
Script déterministe idempotent qui détecte les nouveautés (villa, HF scrollprize, catalogue S3, arXiv, pages scrollprize).
### Dépendances
C1.
### Tâches
- [x] G1.1 `src/vesres/watch.py` : état `watch/state.json`, rapport `watch/reports/YYYY-MM-DD.md`, erreurs réseau tolérées, verrou anti-concurrence.
- [x] G1.2 Tests (idempotence : deux passages successifs → aucun doublon).
### Validation
Deux exécutions consécutives : la seconde ne rapporte aucune nouveauté ; rapport écrit atomiquement.

## G2 — Planification et analyse
### Objectif
Déclenchement hebdomadaire réel, rattrapage des exécutions manquées, transformation en hypothèses.
### Dépendances
G1.
### Tâches
- [x] G2.1 Tâche planifiée utilisateur Windows `VesuviusResearchWatch` (lundi 09:00, StartWhenAvailable, IgnoreNew) → `watch/run_watch.ps1` ; déclenchement planifié vérifié 2026-11-12 23:37:36, LastTaskResult 0.
- [ ] G2.2 Vérifier un déclenchement réel et son rapport ; synthèse mensuelle `docs/state-of-the-art/` + mise à jour `docs/hypotheses.md`.
### Validation
`schtasks /query /tn` montre Last Result 0 et un rapport daté produit par le déclenchement planifié.

# Phase H — Généralisation

## H1 — Évaluation inter-rouleaux
### Objectif
Mesurer la robustesse sur ≥ 3 rouleaux indépendants aux conditions différentes.
### Dépendances
E1, B2.3.
### Tâches
- [ ] H1.1 Réserver des rouleaux de test (jamais utilisés pour décider d'un entraînement).
- [ ] H1.2 Évaluer la meilleure chaîne sur ces rouleaux ; rapport par rouleau, résolution, énergie.
### Validation
Résultats par rouleau avec intervalles (bootstrap par région), sans fuite documentée.

# Phase I — Contribution scientifique

## I1 — Consolidation et diffusion
### Objectif
Rendre publiables code, protocoles et résultats démontrés, dans le respect des licences.
### Dépendances
H1 ou résultat original démontré.
### Tâches
- [ ] I1.1 Reproduire les résultats clés depuis zéro, vérifier licences de chaque composant.
- [ ] I1.2 Préparer contribution (upstream villa / Discord / prix) — soumise à confirmation humaine.
### Validation
Reproduction indépendante réussie ; confirmation humaine explicite avant toute publication.
