> Archive verbatim de plan.md au commit 110c831 (2026-11-27), remplacé par la refonte stratégique. IDs, cases et preuves conservés ; correspondance ancien → nouveau dans plan.md, section « Traçabilité ».

# PLAN — VESUVIUS AUTONOMOUS RESEARCH

## Objectif final
Construire, valider et faire progresser une chaîne informatique ouverte de bout en bout
(scan → feuilles → déroulement → encre → localisation → transcription assistée → incertitudes)
capable de lire virtuellement, aussi exhaustivement et fiablement que physiquement possible,
de nouveaux manuscrits du Vesuvius Challenge, sans dépendre d'un rouleau particulier.
« Lecture intégrale » = toute la surface récupérable reconstruite et examinée, observations,
lectures incertaines, restaurations hypothétiques et zones irrécupérables explicitement distinguées.

Quatre exigences permanentes (2026-11-26), au service de l'objectif ci-dessus, qui reste inchangé :
1. **Lecture intégrale généralisable** (objectif principal).
2. **État de l'art vivant** : veille opérationnelle (Phase G) consultée avant chaque expérience importante ;
   chaque nouveauté pertinente évaluée (apport, preuve, reproductibilité, limites, intérêt, expérience comparative).
3. **Efficacité optimale de toute la chaîne** (Phase K) : coût total minimal — préparation, géométrie, encre,
   entraînement, inférence, CPU/GPU/RAM/VRAM/stockage/réseau — sans perte significative de qualité,
   reproductibilité ou généralisation.
4. **Compatibilité Vesuvius Challenge** (Phases L, M) : formats et outils officiels, licences, matrice de
   conformité aux prix sourcée (`docs/compliance/vesuvius-challenge-matrix.md`) ; jamais d'éligibilité déclarée sans preuve.
Principe directeur : construire le meilleur système scientifique ouvert, évolutif, efficace et compatible pour
lire les manuscrits, pas la meilleure IA. Priorités courantes : `docs/research-review-2026-11-26.md`.

## Invariants
- Neutralité de méthode : l'IA n'est jamais la solution présumée. Pour chaque problème, considérer
  géométrie/topologie/optimisation, physique des matériaux et interaction rayons X, traitement du signal,
  statistiques et méthodes non supervisées, apprentissage, et hybrides ; choisir sur performance démontrée,
  généralisation, coût, fiabilité et contribution à la lecture ; à qualité comparable, la plus simple gagne.
  Une piste prometteuse n'est jamais écartée parce qu'elle n'est pas neuronale.
- Orientation lecture : une métrique intermédiaire n'est poursuivie que si elle sert la lecture réelle
  (zones d'encre nouvelles, lettres candidates, passages reconstruits, validation papyrologique, généralisation).
  Aucun caractère inventé ; restauration linguistique ≠ observation physique ; toute découverte potentielle
  porte preuves visuelles (privées), coordonnées, provenance, méthode et incertitudes.
- Compatibilité Vesuvius Challenge : formats/coordonnées/métadonnées officiels (OME-Zarr, Zarr, tifxyz, meshes),
  outils officiels réutilisés quand ils suffisent, briques réutilisables hors de notre infrastructure, pas de
  format propriétaire ; provenance des labels, pseudo-labels et modèles auditée avant toute prédiction sur un
  rouleau cible ; l'objectif scientifique n'est jamais modifié pour un prix.
- Dépôt public (MIT, `github.com/nevenfo/vesuvius-autonomous-research`, public depuis 2026-11) : aucun secret,
  donnée, poids, label, image d'encre ou transcription non autorisée ; `main` présentable et scientifiquement
  fiable, aucune fusion sans autorisation humaine ; résultats positifs et négatifs documentés.
- Efficacité de calcul : ne jamais dépenser du calcul inutilement, mais ne jamais sacrifier un gain
  scientifique réel pour réduire une durée. Aucun nombre d'itérations n'est optimal par défaut :
  la durée se choisit sur un jeu de **validation** distinct de l'entraînement et des tests ; les
  objets de test (0841, 0009B, 0500P2 et futurs rouleaux réservés H1.1) ne servent jamais à choisir
  une durée, un checkpoint ou un hyperparamètre (courbes sur test = descriptives uniquement).
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
  importante, exposition de secret, publication externe, annonce de découverte, PR upstream, soumission à un prix,
  réécriture d'historique Git public.
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
- J8 Recette d'entraînement de référence ramenée à une durée et un coût minimaux mesurés, non
  inférieure à la référence 40k (marge et protocole K2), appliquée par défaut aux entraînements futurs.
- J9 Au moins une méthode non neuronale ou hybride évaluée hors échantillon contre la référence neuronale sur ≥ 3 objets.
- J10 Matrice de conformité Vesuvius Challenge à jour (≤ 1 mois) et dépôt public reproductible depuis zéro par un tiers.

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
- [ ] B1.2 Vérifier sur sources primaires les points marqués « non vérifié » utiles à la décision courante (licences VC3D/lasagna, données d'entraînement de reader-v2, nature humaine/pseudo des ink-labels 20260918). (Labels : provenance/alignement établis, modèle de pseudo-labeling non publié — `docs/data/splits.md` ; reste : licences VC3D/lasagna.)
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
- [x] B3.2 Réviser `docs/hypotheses.md` après EXP-006…009 (4 hypothèses réfutées d'affilée → audit protocole/métrique selon la règle d'arrêt F1.1) : audit écrit du protocole (contrôle positif de la chaîne tuiles/Brier, puissance du test), puis ≥ 3 nouvelles hypothèses falsifiables classées. (EXP-010 ; H-010…H-013.)
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
- [x] E1.2 Comparer ink_9um vs reader-v2 vs pipeline 2,4 µm (`vesuvius.ink_detection`) sur mêmes crops. (EXP-017 : prédictions officielles canon 2,4 µm publiées vs nos modèles sur les 5 segments étiquetés ; inférence 2,4 µm locale écartée, 33 Go/segment — `docs/data/scoping-2.4um.md`.)
- [x] E1.4 Hecate 9,6 µm (MIT) sur les 3 segments 0841 (rééchantillonnage 9,366→9,6 µm exigé par la model card) ; tester H-003 avec ce partenaire. (EXP-003 : 6/6 AUC reproduites ; H-003 soutenue.)
- [x] E1.5 Ré-entraînement leave-one-scroll-out (recette `aligned21_hybrid_3d2d.json`) si nécessaire pour disposer de ≥ 3 rouleaux de test indépendants (J5). (Cadrage EXP-018 : ink_9um déjà leave-out de 0841/0009B/0500P2 ; ré-entraînement retenu = recette reader-v2 sans 0009B/0500P2 → reader-v2-LO, validé par entraînement complet 40k + évaluation sur les 5 segments : EXP-018, H-017 soutenue.)
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

## G3 — Veille renforcée et décisionnelle
### Objectif
Veille fiable (sans trou ni défaillance silencieuse) couvrant toutes les sources pertinentes, et branchée sur les décisions expérimentales.
### Dépendances
G1, G2.1.
### Tâches
- [x] G3.1 Réessais HTTP avec backoff, arXiv 200 résultats / 120 s (rattrapage des passages manqués), sources Zenodo et pages règlement/licence (`rules_pages`), défaillances ≥ 2 passages signalées (commit `e35201f`, 12 tests verts ; Zenodo a trouvé Korotetskyi & Haindl 2026 dès le premier essai).
- [ ] G3.2 Règle d'expérience : avant toute expérience importante, consulter les rapports de veille depuis la dernière décision et noter dans le README de l'EXP « veille consultée : <date>, impact : … ».
- [ ] G3.3 Chaque nouveauté retenue reçoit une fiche (apport, niveau de preuve, reproductibilité, limites, intérêt, expérience comparative) dans l'analyse du rapport, et une hypothèse si une comparaison est pertinente.
### Validation
Passage planifié suivant sans erreur persistante ; une expérience au moins dont le README cite la veille consultée.

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

# Phase K — Efficacité d'entraînement (objectif secondaire permanent)

## K1 — État de l'art de l'efficacité d'entraînement
### Objectif
Recenser les méthodes établies (choix de durée, arrêt anticipé, schedules sans horizon fixe, débit GPU/données) avant tout développement propre.
### Dépendances
Aucune.
### Tâches
- [x] K1.1 Synthèse sourcée `docs/state-of-the-art/training-efficiency.md` : early stopping, WSD / schedule-free, moyenne de poids (EMA/SWA), non-infériorité, débit PyTorch (précision, compile, channels_last, DataLoader, zarr), pratiques villa/reader-v2/nnU-Net.
- [x] K1.2 Classer les leviers en hypothèses `H-NNN` (gain attendu, effort, risque, impact scientifique) dans `docs/hypotheses.md`.
### Validation
Document avec URL et niveau de preuve par point ; hypothèses K inscrites avec critère de réfutation fixé avant mesure.

## K2 — Protocole de durée optimale
### Objectif
Définir, avant toute mesure, comment déterminer la durée minimale non inférieure à une référence sans contaminer les tests.
### Dépendances
K1.1.
### Tâches
- [x] K2.1 `docs/protocols/training-duration.md` : jeu de validation tenu à l'écart (segments entiers des rouleaux d'entraînement, jamais un objet de test), métriques (AUC/AP sup. sur validation), marge de non-infériorité δ (par défaut 0,01 AUC sup., révisée si la variance inter-seeds mesurée l'exige) testée par bootstrap par région (IC 95 % unilatéral), coût total mesuré (préparation, recherche de patches, entraînement, validation, en heures GPU et murales), règle d'arrêt anticipé.
- [x] K2.2 Préciser l'effet du schedule : un checkpoint intermédiaire d'un run cosine 40k n'équivaut pas à un run court recuit ; protocole de rattrapage (décroissance courte depuis checkpoint, ou schedule sans horizon) défini avant mesure.
### Validation
Protocole relu contre `docs/data/splits.md` (aucun objet de test dans validation ou sélection) et commité avant la première mesure K3.

## K3 — Courbes performance/temps sur la référence EXP-018
### Objectif
Exploiter les 40 checkpoints de la référence reader-v2-LO 40k (EXP-018, non modifiée) pour situer le rendement décroissant.
### Dépendances
E1.5 (entraînement terminé et évalué), K2.1.
### Tâches
- [x] K3.0 Construire les 4 segments de validation K (`role == holdout` de `selection.json`, 0343P ×2, 0172 ×2) avec `build.py`, mêmes seuils ; vérifier labels non vides. (4/4, `data/v2lo_val_build.log` : encre 4–17 %, supervision 67–94 %.)
- [ ] K3.1 Courbe perte d'entraînement et débit (it/s, utilisation GPU) par itération depuis les journaux EXP-018 ; coût réel de chaque phase.
- [ ] K3.2 Inférence de checkpoints échantillonnés (5k, 10k, 20k, 30k, 40k) sur la validation K ; sur objets de test uniquement en descriptif, après la conclusion H-017, sans en tirer de durée.
### Validation
`experiments/EXP-NNN/` avec courbes, coûts et mention explicite du statut descriptif des courbes sur test.

## K4 — Durée minimale validée et arrêt anticipé
### Objectif
Démontrer une recette plus courte non inférieure à la référence, et un arrêt anticipé adaptatif si pertinent.
### Dépendances
K2, K3.
### Tâches
- [ ] K4.1 Entraînements courts recuits (durées choisies d'après K3 et K1), même données, même seed puis ≥ 2 seeds sur la durée retenue ; non-infériorité sur validation K2.1.
- [ ] K4.2 Confirmation unique sur les objets de test de la durée retenue (après décision sur validation) vs référence 40k.
- [ ] K4.3 Arrêt anticipé (patience sur validation périodique) intégré au lanceur si K4.1 montre un plateau exploitable.
### Validation
Non-infériorité démontrée (borne IC 95 % < δ) sur validation, confirmée sur test, gain de temps total chiffré ; sinon recette 40k conservée et résultat négatif consigné.

## K5 — Débit par itération et coût des données
### Objectif
Réduire le temps par itération et le coût de préparation sans changer les résultats au-delà de δ.
### Dépendances
K1.1.
### Tâches
- [ ] K5.1 Profilage d'une fenêtre d'entraînement (GPU vs DataLoader vs I/O zarr) ; coût de la recherche de patches (≈ 40 min par lancement observé 2026-11-26) et réutilisation de son cache.
- [ ] K5.2 Leviers mesurés un à un (précision bf16/fp16, `torch.compile`, channels_last, workers/prefetch, taille de lot + LR, cache des données) ; chacun gardé seulement si gain de temps ≥ 10 % et métriques validation dans δ.
- [ ] K5.3 Intégrer les leviers démontrés à la recette par défaut (lanceur, `make_config.py`) et au manifeste des expériences (coût total).
### Validation
Tableau avant/après (it/s, heures totales, métriques validation) par levier, reproductible depuis les scripts commités.

## K6 — Efficacité de toute la chaîne et calcul adaptatif
### Objectif
Mesurer et réduire le coût total de la chaîne (données, géométrie, encre, inférence, ressources), et tester une cascade rapide → coûteuse.
### Dépendances
K1.1 ; N1/N2 pour l'étage rapide de la cascade.
### Tâches
- [ ] K6.1 Manifeste de coût standard pour chaque EXP (heures murales/GPU, pic RAM/VRAM, stockage, volume réseau) ; tableau de coût de la chaîne de référence (téléchargement, recherche de patches, inférence par cm², évaluation).
- [ ] K6.2 Réutilisation : inventaire des artefacts intermédiaires réutilisables (prédictions, caches de patches, surfaces) avec règles de compatibilité de protocole.
- [ ] K6.3 H-025 cascade : étage rapide (descripteurs N1/N2 ou modèle léger) calibré pour un rappel ≥ 99 % de l'encre sur validation, étage coûteux sur les zones restantes ; mesurer économie de calcul et perte de rappel/AP vs modèle seul sur objets de test (config figée).
### Validation
Tableau de coûts reproductible ; cascade adoptée seulement si rappel ≥ 99 % et AP dans δ, sinon résultat négatif consigné.

# Phase L — Compatibilité Vesuvius Challenge

## L1 — Matrice de conformité aux prix
### Objectif
Maintenir une matrice sourcée exigences × état × preuves × actions pour chaque prix actif.
### Dépendances
Aucune.
### Tâches
- [x] L1.1 Matrice initiale `docs/compliance/vesuvius-challenge-matrix.md` (Grand Prize 2027, First Letters, Paris 4 Title, Progress ; licence ↔ open source ; sources officielles lues le 2026-11-26).
- [ ] L1.2 Revue mensuelle et à chaque alerte `rules_pages` de la veille ; points ❔ (agents IA, pays, préentraînés, délai open source) à poser par écrit aux organisateurs — action humaine.
### Validation
Date de vérification ≤ 1 mois ; chaque ligne cite sa source.

## L2 — Interopérabilité technique
### Objectif
Sorties directement utilisables par VC3D/villa et briques réutilisables hors de notre infrastructure.
### Dépendances
L1.1.
### Tâches
- [ ] L2.1 Export d'une carte d'encre en OME-Zarr/TIFF aligné sur la grille tifxyz du segment + image programmatique (barre 1 cm, sans retouche) conforme aux prix, sorties privées (licence).
- [ ] L2.2 Audit de provenance par rouleau cible (modèles, labels, résolution source) avant toute prédiction sur un rouleau éligible (règles « pas de chevauchement » et « pas de scan plus résolu du même volume »).
### Validation
Fichier ouvert dans VC3D ou chargé par les outils villa sans conversion manuelle ; audit écrit pour chaque rouleau cible.

# Phase M — Open source et reproductibilité externe

## M1 — Sécurité et présentation du dépôt public
### Objectif
Dépôt public sûr, conforme aux licences et lisible par la communauté.
### Dépendances
Aucune.
### Tâches
- [x] M1.1 Audit sécurité/licences de tout l'historique (`docs/open-source/audit-2026-11-26.md`) : aucun secret, aucune donnée/label/image/poids ; écarts listés.
- [x] M1.2 README et documentation d'entrée en anglais (objectif, résultats positifs et négatifs, protocoles, licences, citations), français conservé pour le travail interne.
- [x] M1.3 Chemins configurables (`VESRES_WORK` ; dépôt déduit de `$PSScriptRoot`) au lieu de `C:/Users/...` et de l'IP du NAS codés en dur.
- [ ] M1.4 Décision humaine : adresse e-mail des commits (noreply GitHub pour l'avenir ; réécriture d'historique seulement sur demande).
### Validation
`rg` ne trouve plus de chemin personnel dans le code ; README anglais présent ; décision M1.4 consignée.

## M2 — Reproductibilité sur une autre machine
### Objectif
Installer et rejouer une expérience clé depuis zéro sans notre infrastructure.
### Dépendances
M1.3.
### Tâches
- [ ] M2.1 Environnements verrouillés documentés (`.venv`, `.venv-koine`, `.venv-tex`) + `Dockerfile` CPU/GPU.
- [ ] M2.2 Rejouer EXP-001 depuis un clone propre dans un dossier neuf (données publiques téléchargées par script).
- [ ] M2.3 Liste des contributions communautaires candidates (évaluation sans fuite, détecteur explicable, export programmatique) avec preuve d'intérêt — soumission/PR seulement sur autorisation humaine.
### Validation
Rejeu EXP-001 identique (12/12) depuis un clone propre.

# Phase N — Méthodes non neuronales et hybrides

## N1 — Détection d'encre par texture 3D sans entraînement
### Objectif
Reproduire Korotetskyi & Haindl 2026 puis l'évaluer hors échantillon contre notre référence neuronale.
### Dépendances
B2 (segments étiquetés), C1.
### Tâches
- [ ] N1.1 EXP-021 / H-022 : reproduction de leurs résultats (MCC fusion 0,457 in-sample, 25 glyphes PHerc. 172) depuis le paquet Zenodo, CPU.
- [ ] N1.2 H-023 : configuration figée appliquée à nos 5 segments étiquetés (0841 × 3, 0009B, 0500P2) ; AUC/AP sup. vs reader-v2, Hecate, intensité brute ; fusion avec reader-v2 ; coût CPU.
### Validation
Tableau publié/reproduit ; évaluation `eval_ink` avec IC par blocs, sans réglage sur les objets de test.

## N2 — Baseline physique simple
### Objectif
Mesurer ce que la physique seule (profil d'intensité le long de la normale) apporte à 9 µm.
### Dépendances
B2.
### Tâches
- [ ] N2.1 H-024 : features par pixel du surface-volume (profil 65 couches, différences, gradient, variance locale) + classifieur léger (régression logistique / gradient boosting) en leave-one-object-out ; comparer à reader-v2 et N1.
### Validation
AUC sup. par objet tenu à l'écart avec IC ; coût mesuré.

# Phase R — Orientation vers des découvertes réelles

## R1 — Lettres candidates sur un rouleau non lu
### Objectif
Rechercher des zones d'encre et lettres candidates sur un rouleau éligible First Letters, avec une chaîne n'ayant vu aucune région de ce rouleau.
### Dépendances
E1.5 (modèles LO), L2.2 (provenance), N1/N2 (signal complémentaire).
### Tâches
- [ ] R1.1 Choisir le rouleau (candidat : PHerc0800, 12 segments au catalogue) et des segments selon qualité de surface et couverture ; audit L2.2.
- [ ] R1.2 Inférence de la meilleure chaîne, cartes privées, inspection ; toute zone candidate documentée (coordonnées, méthode, incertitudes) sans publication.
- [ ] R1.3 Si ≥ 10 lettres candidates dans 4 cm² : dossier de preuve privé et décision humaine (Discord / soumission).
### Validation
Rapport privé par segment (zones, scores, faux positifs plausibles) ; aucune image publiée ; décision humaine consignée.
