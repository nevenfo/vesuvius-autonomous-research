# PLAN — VESUVIUS AUTONOMOUS RESEARCH

Refonte stratégique du 2026-11-27 (audit : `docs/research-review-2026-11-27.md`). Plan précédent archivé à
l'identique : `docs/plan-archive-2026-11-27.md` (IDs, cases et preuves inchangés).

# PARTIE STABLE

## Objectif final
Parvenir à lire intégralement, fidèlement et de manière généralisable l'ensemble des manuscrits du Vesuvius
Challenge, en récupérant autant d'informations que physiquement possible, indépendamment de la méthode, de la
technologie ou de l'architecture : retrouver les caractères, identifier les mots, reconstruire les phrases, lire
et comprendre les passages, produire des transcriptions fiables, traduire quand c'est possible, retrouver des textes
inconnus, traiter de nouveaux manuscrits sans tout reconstruire, et cartographier précisément ce qui est récupéré,
incertain, non examiné ou potentiellement irrécupérable.
L'ambition de tout lire n'est pas une preuve que toute l'information subsiste dans les scans : on distingue
impossibilité physique démontrée, limite des données, du matériel, des connaissances, de notre méthode, et région
simplement non examinée. L'objectif n'est jamais réduit parce que les méthodes actuelles sont insuffisantes.

## Invariants
- **Neutralité** : aucune technologie obligatoire (IA, géométrie, physique, signal, statistiques, linguistique,
  hybrides…) ; à résultat comparable, la plus simple gagne ; aucune architecture conservée pour coût englouti.
  L'objectif est fixe, le plan évolutif, l'architecture révisable, la technologie remplaçable, les preuves décident.
- **Résultat réel** : toute optimisation importante est reliée à une hypothèse sur la quantité, la fidélité ou la
  couverture du texte lu, ou sur un coût réduit sans perte scientifique. AUC/AP/loss = diagnostics.
- **Rigueur avant apparence** : texte détecté ≠ caractère reconnu ≠ lecture validée ; statuts Observé / Reconnu /
  Probable / Restitué / Inconnu / Validé (`docs/protocols/reading-evaluation.md`) ; une restitution linguistique
  n'est jamais présentée comme observation ; aucune vérité terrain fabriquée ; résultats négatifs consignés.
- **Indépendance** : chaque métrique porte la classe de sa référence (R0–R4, `docs/protocols/independence.md`) ;
  évaluation par objet tenu à l'écart, jamais par patch ; objets de test jamais utilisés pour choisir durée,
  checkpoint, seuil ou hyperparamètre ; test scellé ouvert une fois par conclusion majeure.
- **Couverture** : jamais « 100 % » sans surface totale connue ; non examiné ≠ vide ; sans encre détectée ≠ sans
  texte ; inaccessible ≠ irrécupérable (`docs/protocols/coverage.md`).
- **Généralisation** : résultats par manuscrit et par région ; un échec n'est jamais masqué par une moyenne.
- **Apprentissage collectif** : veille consultée avant toute expérience importante ; réutiliser avant d'innover ;
  chaque nouveauté retenue évaluée (problème, méthode, preuve, données, limites, reproductibilité, négatifs,
  compatibilité, licence, intérêt lecture, expérience comparative).
- **Boucle autonome** : sélection, arrêt et audit selon `docs/protocols/research-loop.md` ; critères écrits avant
  mesure ; échec attribué avant conclusion.
- **Efficacité** : coût total mesuré ; ne jamais dépenser du calcul inutilement ni sacrifier un gain scientifique
  réel pour une durée ; PC personnel préservé (VRAM ≤ ~12 Go, pas de job CPU lourd pendant un entraînement, calculs
  interruptibles avec reprise sans corruption).
- **Compatibilité Vesuvius Challenge** : formats officiels (OME-Zarr, Zarr, tifxyz, meshes), outils officiels
  réutilisés, matrice `docs/compliance/vesuvius-challenge-matrix.md` sourcée ; jamais d'éligibilité déclarée sans
  preuve ; une échéance de prix n'est pas une date de fin scientifique.
- **Open source et licences** : code original MIT ; tiers sous leur licence ; dépôt public sans secret, donnée,
  poids non redistribuable, label, image d'encre, transcription ou découverte (licence données : rien de révélé hors
  Discord officiel sans accord écrit) ; `main` présentable, aucune fusion sans accord humain.
- **Stockage** : accès par régions ; cache reproductible évictable (`vesuvius-work/cache`) ; artefacts uniques
  copiés sur le NAS avec manifeste sha256 ; GitHub n'est pas un stockage de données.
- **Confirmation humaine** : dépense, action destructive/irréversible, modification système/réseau importante,
  exposition de secret, publication externe, annonce de découverte, contact de tiers, PR upstream, soumission à un
  prix, réécriture d'historique public.
- Chaque résultat porte un `EXP-NNN` et un manifeste (données, coordonnées, code, modèle, paramètres, date,
  matériel, métriques, coût, classe de référence, limites) dans `experiments/`.

## Critères globaux de réussite (jalons, cochés sur preuve uniquement)
Non séquentiels ; dépendances réelles dans les unités ci-dessous.
- [x] J1 État de l'art et acquis historiques audités (S1 : `docs/research-review-2026-11-27.md`).
- [ ] J2 Référence de lecture de bout en bout reproductible (V1–V3).
- [ ] J3 Mesures de couverture et de lisibilité opérationnelles (V1, W1, W3).
- [ ] J4 Protocole d'évaluation indépendant et contrôle de circularité appliqués (P1–P3).
- [ ] J5 Principaux obstacles identifiés expérimentalement (V3).
- [ ] J6 Amélioration réelle et mesurable de la capacité de lecture (niveau glyphe ou caractère, référence R2+).
- [ ] J7 Premières lettres inédites avec preuves (R1).
- [ ] J8 Passage inédit transcrit et validé indépendamment (R2, T5).
- [ ] J9 Généralisation sur plusieurs rouleaux indépendants (H1 ; 3 = minimum intermédiaire).
- [ ] J10 Première lecture intégrale d'un nouveau manuscrit dans les limites physiques démontrées.
- [ ] J11 Extension progressive au corpus accessible.
- [ ] J12 Optimisation, reproductibilité externe et contribution continue (K, M2, I1).
Anciens jalons (archive) : J1→J1, J2 (baseline reproduite, atteint par EXP-001)→S0, J3→J2, J4→J8/J10, J5→J9,
J6→J11, J7→G, J8→K (suspendu), J9→N/J6, J10→L/M2.

# PARTIE ÉVOLUTIVE

## Architecture de référence (révisable, 2026-11-27)
Chemin v0 : segments communautaires (tifxyz, autoseg VC) → surface-volume officiel 8,6–9,4 µm → encre (fusion
reader-v2(-LO) + Hecate ; comparateurs reader-v3, canon 2,4 µm) → unités graphiques et lisibilité locale
(`src/vesres/reading.py`) → **[manquant] identification de caractères** → [manquant] mots/phrases → statuts et
couverture. Toute brique est remplaçable sur preuve ; contournements de la géométrie (détection 3D sur volume non
aplati) admis comme hypothèses.

## Obstacles prioritaires et priorités courantes
Détail argumenté : `docs/research-review-2026-11-27.md` §4–6. Exploration (X) menée en parallèle, sans quota, arbitrée à chaque revue. Ordre courant : W1 → W2.3 (segments propres sur rouleau éligible, condition de R1) → T1 → R1.2 → Y1 → V2/T2 → H1 ; N1/N2 opportunistes ; K4/K5 suspendus. Faits : V1, P1, P2.1, R1.1.

## Traçabilité ancien → nouveau
Validés conservés en S0. Ouverts repris sous leur ID : B1.2, E1.1, E1.3, G2.2, G3.2, G3.3, H1.1, H1.2, I1.1, I1.2,
K3.1, K3.2, K4.1–K4.3, K5.1–K5.3, K6.1, K6.2, L1.2, L2.1, L2.2, M1.4, M2.1–M2.3, N1.1, N1.2, N2.1, R1.1–R1.3.
K6.3 (cascade) → Y2.1. F1.2 → absorbé par la boucle (`research-loop.md`).

# Phase X — Créativité et exploration

## X1 — Cycles créatifs
### Objectif
Générer, critiquer et sélectionner sans sollicitation humaine des idées capables de changer la façon de lire (audit d'hypothèses implicites, anomalies, suppression d'étapes, transferts interdisciplinaires vérifiés).
### Dépendances
Aucune.
### Tâches
- [x] X1.1 Intégrer la créativité à la boucle (`docs/protocols/research-loop.md` §6) et au registre (`docs/hypotheses.md`, idées I-NNN).
- [x] X1.2 Cycle n° 1 : idées I-001…I-008, nouveauté vérifiée, avis critique sur la piste utilisateur (`docs/research-review-2026-11-27.md` §7).
- [ ] X1.3 Cycle n° 2 à chaque revue d'obstacles (après V3 ou trois résultats nouveaux) : réexamen des idées suspendues, nouvelles idées.
### Validation
Chaque idée a fiche, statut et expérience minimale ; les idées retenues deviennent des H-NNN avec critères écrits.

## X2 — Expériences de faisabilité
### Objectif
Tester par des expériences courtes et discriminantes les idées au meilleur rapport potentiel/coût.
### Dépendances
X1.
### Tâches
- [x] X2.1 I-003 → H-032, EXP-027 : auto-cohérence de rendus redondants de 1667. (H-032 soutenue : ρ 0,78–0,89 ; prochaine étape : carte locale de stabilité, tolérance d'appariement révisée.)
- [x] X2.2 I-008 : masque officiel vs papyrus (tranches, PHerc1218/0800), coût très faible. (EXP-028 : H-033 réfutée, masque non amputant ; fragments détachés non départageables.)
- [ ] X2.3 I-004 : encre 3D publiée vs rendus de surface, par glyphe, sur zone étiquetée.
- [ ] X2.4 I-001 minimal : seuil de détectabilité du relief d'encre selon voxel/bruit sur coupe 2D simulée.
### Validation
README d'EXP avec critères fixés avant ; verdict ; statut de l'idée mis à jour.

# Phase S — Audit et refonte stratégique

## S0 — Acquis historiques (2026-11-12 → 2026-11-27)
### Objectif
Conserver la trace des unités validées avant la refonte.
### Dépendances
Aucune.
### Tâches
- [x] S0.1 Validés : A1.1–A1.3, A2.1–A2.2, B1.1, B2.1–B2.3, B3.1–B3.2, C1.1–C1.2, C2.1–C2.3, D1.1–D1.3, E1.2, E1.4, E1.5, G1.1–G1.2, G2.1, G3.1, K1.1–K1.2, K2.1–K2.2, K3.0, L1.1, M1.1–M1.3 ; EXP-001…018 (preuves : `docs/plan-archive-2026-11-27.md`, `experiments/registry.csv`).
### Validation
Archive verbatim présente ; registre EXP-001…018 inchangé.

## S1 — Audit et refonte du 2026-11-27
### Objectif
Auditer acquis et limites, traiter les douze défauts, réorienter le plan vers la lecture.
### Dépendances
S0.
### Tâches
- [x] S1.1 Audit par expérience (objectif, démontré, limites, indépendance, intérêt lecture, réutilisable, réévaluation) et constats transverses → `docs/research-review-2026-11-27.md` §1.
- [x] S1.2 Veille ciblée sur les lacunes décisionnelles (références caractère, OCR, couverture, PHerc0800, résolution, nouveautés) → §3.
- [x] S1.3 Protocoles : `docs/protocols/{reading-evaluation,coverage,independence,research-loop}.md`.
- [x] S1.4 Refonte de `plan.md`, `docs/hypotheses.md`, `progress.md` ; capitalisation Second Brain.
### Validation
`bash ~/.agents/continuity-check.sh .` PASS ; `pytest` vert ; commit poussé.

# Phase V — Chemin de lecture de bout en bout

## V1 — Chemin v0 et lisibilité au niveau glyphe
### Objectif
Assembler la meilleure chaîne existante jusqu'aux unités graphiques et mesurer lisibilité et couverture des références.
### Dépendances
S1.
### Tâches
- [x] V1.1 Module `src/vesres/reading.py` (UGR, AUC locale, candidats en fond, couverture, contrôles) + tests.
- [x] V1.2 EXP-022 : H-026 (validité par contrôles) et H-027 (≥ 70 % d'UGR lisibles sur 0841, fusion LO+Hecate) ; toutes chaînes par objet. (H-026 soutenue 100 %/0 % ; H-027 réfutée 29 % [13-53].)
### Validation
`experiments/EXP-022/results.json` ; verdicts H-026/H-027 consignés ; sorties par UGR privées hors Git.

## V2 — Étage de reconnaissance v0
### Objectif
Prolonger le chemin jusqu'à des caractères avec statut et abstention.
### Dépendances
V1, T1, T2.
### Tâches
- [ ] V2.1 Brancher le meilleur classifieur T2 sur les UGR du chemin v0 ; sorties « Reconnu/Probable/Inconnu » avec probabilité et alternatives.
- [ ] V2.2 Mesurer CER/abstention sur la seule référence R2+ disponible ; contrôles fond vierge et fibres.
### Validation
Tableau CER/abstention/faux caractères par cm², classe de référence indiquée.

## V3 — Bilan d'obstacles mesurés
### Objectif
Décomposer les pertes de lecture par étage (couverture, géométrie, encre, glyphes, reconnaissance) sur une référence connue.
### Dépendances
V1, W1 ; V2 si disponible.
### Tâches
- [ ] V3.1 Pour le manuscrit de référence PHerc. 1667 (transcription complète R3*, segments et prédictions publiés ; 0841 en v0), attribuer les pertes de lecture à leur cause (hors segment, géométrie, encre faible, reconnaissance, référence douteuse) ; CER par colonne par alignement de séquences.
### Validation
Tableau des pertes par étage avec incertitudes ; obstacles reclassés dans la revue suivante.

# Phase W — Couverture et géométrie

## W1 — Inventaire de couverture du corpus
### Objectif
Pour chaque manuscrit : surface identifiée (borne haute), reconstruite, examinée, et estimation physique avec intervalle.
### Dépendances
B2.1.
### Tâches
- [x] W1.1 EXP-023 : lire les méta-données des segments publiés (aire, dimensions tifxyz) et des scans ; méthode d'estimation physique écrite avant calcul → `docs/data/coverage_inventory.{csv,md}` régénérable. (Inventaire déterministe, 26 tests ; H-028 indéterminée : estimateur de pas inopérant ; somme des segments 1667 = 2× la surface déroulée publiée.)
- [ ] W1.2 Amender l'estimation : pas des spires le long des normales locales (segments / prédiction de surface) ou FFT 2D locale ; surface identifiée dédupliquée par union voxélisée des segments ; contrôle sur 1667 (1 231 cm² publiés) ; comparer volume masqué et non masqué (papyrus exclu par le masque ?).
### Validation
Script déterministe ; deux exécutions identiques ; inconnues explicites par manuscrit.

## W2 — Outils géométriques existants
### Objectif
Évaluer VC3D, autosegmentation officielle, fibres, spiral fitting, contrôles de cohérence par leur contribution à la couverture et leur coût, avant tout développement propre.
### Dépendances
W1.
### Tâches
- [x] W2.1 Fiche par outil (capacités, limites, coût, licence, sorties) depuis sources primaires et dépôts. (`docs/state-of-the-art/2026-11-27-reading-and-geometry.md` §2 ; VC3D GPL-3.0, AppImage CLI.)
- [ ] W2.2 Tester sur une région d'un rouleau la détection de trous, doublons et sauts de feuillet par les outils existants ; décider si la géométrie est un obstacle significatif (H-009 sur surfaces difficiles).
- [x] W2.3 Produire avec les outils officiels (VC3D/villa, lasagna) au moins un segment tifxyz sur un rouleau éligible sans segment publié, depuis `surface-prediction-zarr`/`normal-grids` ; rendre son surface-volume ; mesurer surface obtenue, temps machine et humain, contrôles qualité. (EXP-025 : PHerc1218, 4,11 cm² en 475 s, 0 intervention, fidélité 86,7 % ; rendu du surface-volume reporté à R1.2.)
### Validation
Décision écrite « réutiliser / contourner / développer » avec preuves.

## W3 — Cartes de couverture par segment
### Objectif
Produire pour chaque segment traité les catégories de `coverage.md` (examiné, encre potentielle, lisible, incertain, non traité).
### Dépendances
V1, W1.
### Tâches
- [ ] W3.1 Étendre `reading.coverage` aux catégories de lisibilité et l'intégrer au manifeste de chaque EXP d'inférence.
### Validation
Carte (privée) et tableau (public, agrégé) pour les segments de R1.

# Phase P — Indépendance, provenance, fuites

## P1 — Graphe de provenance
### Objectif
Tracer données, labels, pseudo-labels, modèles, checkpoints et prédictions.
### Dépendances
B2.3.
### Tâches
- [x] P1.1 `docs/data/provenance.csv` (source, relation, cible, statut, preuve) depuis `splits.md`, model cards, EXP-017/018 ; test de cohérence. (`tests/test_provenance.py` 3 verts ; parentés NV : Hecate, canon, reader-v3, argus-v3, modèle de pseudo-labeling.)
### Validation
Chaque modèle évalué a ses parentés ; inconnues marquées.

## P2 — Requalification des métriques historiques
### Objectif
Attribuer une classe R0–R4 à chaque métrique historique et borner les conclusions.
### Dépendances
P1.
### Tâches
- [x] P2.1 Colonne « classe de référence » dans le registre et les résultats ; corriger toute conclusion qui dépasse sa classe (EXP-017 en priorité). (`registry.csv` colonne `ref_class` ; EXP-017 requalifiée dans `docs/hypotheses.md` et EXP-022.)
- [ ] B1.2 Licences VC3D/lasagna ; modèle de pseudo-labeling des ink-labels (reste non vérifié).
### Validation
Registre complété ; liste des conclusions révisées.

## P3 — Test scellé
### Objectif
Réserver des objets réellement protégés des décisions expérimentales.
### Dépendances
P1, W1.
### Tâches
- [x] P3.1 Règle de choix écrite (diversité rouleau/fragment, énergie, résolution, état) ; liste et empreintes dans `docs/data/sealed_test.md` avant consultation. (T-1667-READ : Col. multiples de 3 scellées, sha256 3aed5363… ; aucun test d'encre scellable sans P4 ; fuite 1667 ↔ nos modèles consignée.)
- [ ] P3.2 Modèle de lecture sans 1667 (recette EXP-018 sans 1667 ni objets de test) si V3 confirme que l'évaluation sur T-1667-READ est nécessaire ; coût ≈ 3–4 h GPU, entraînement seul sur la machine.
- [ ] H1.1 Réserver les rouleaux de test (jamais utilisés pour décider d'un entraînement).
### Validation
Fichier daté et commité avant toute ouverture ; journal des ouvertures.

## P4 — Références indépendantes
### Objectif
Obtenir des références R2/R3 au lieu de R1.
### Dépendances
T1.
### Tâches
- [ ] P4.1 Localiser et évaluer les photos IR des fragments alignées sur les surface-volumes (R3) et leur couverture de nos objets.
- [ ] P4.2 Protocole d'annotation indépendante (`independence.md` §5) prêt à l'emploi ; exécution = décision humaine (annotateur).
### Validation
Inventaire des références R2/R3 avec licence et emprise ; protocole relu.

# Phase T — Reconnaissance du texte

## T1 — Références et état de l'art de la reconnaissance
### Objectif
Identifier les références caractère/mot utilisables et les méthodes OCR/HTR pertinentes, sans imposer d'architecture.
### Dépendances
S1.
### Tâches
- [x] T1.1 Lire arXiv:2606.29085 (transcriptions, alignements, couverture 1667) ; ICDAR 2023 papyrus grecs, AL-PUB, lectures First Letters publiées : fiche (preuve, licence, intérêt, expérience comparative). (`docs/state-of-the-art/2026-11-27-reading-and-geometry.md` §1 : transcription complète 1667 Col. 1–22 = référence R3*, copie privée `vesuvius-work/refs/PHerc1667/`.)
- [ ] T1.2 Rédiger la question écrite aux auteurs/organisateurs (alignement colonne ↔ segment de la transcription 1667, « transcription artifacts » du data browser) — envoi = action humaine (L1.3). (Question 4 de la matrice §6, à préciser.)
### Validation
Fiches dans `docs/state-of-the-art/` ; décision sur la référence de V2.

## T2 — Identification de glyphes v0
### Objectif
Mesurer si des glyphes de cartes d'encre sont identifiables, avec abstention et contrôles.
### Dépendances
T1, V1.
### Tâches
- [ ] T2.1 Hypothèse et protocole (classifieur simple vs pré-entraîné sur lettres grecques ; écart de domaine photo→CT mesuré) ; contrôles fond vierge, fibres, glyphes tournés.
### Validation
Résultats par classe avec IC et classe de référence ; aucun caractère sans statut.

## T3 — Mots, phrases, langue
### Objectif
Utiliser la linguistique comme information complémentaire, jamais comme preuve d'encre.
### Dépendances
T2.
### Tâches
- [ ] T3.1 Lectures concurrentes, contradictions observation/lecture, tests texte permuté ; grec et latin sans présupposer la langue.
### Validation
Taux de restitutions présentées comme observations = 0 (audit) ; WER si référence.

## T4 — Transcription et traduction
### Objectif
Produire transcriptions diplomatique et normalisée distinctes, traduction et lacunes quand les preuves le permettent.
### Dépendances
T3.
### Tâches
- [ ] T4.1 Format de sortie (statuts, coordonnées, alternatives, lacunes) et exemple sur passage connu.
### Validation
Format relu contre `reading-evaluation.md` ; exemple sur référence publiée.

## T5 — Validation papyrologique externe
### Objectif
Procédure opérationnelle de validation indépendante des lectures nouvelles.
### Dépendances
R1.
### Tâches
- [ ] T5.1 Dossier de preuve type (images privées, coordonnées, méthode, incertitudes, statuts) et circuit (Discord officiel / organisateurs) — exécution = décision humaine.
### Validation
Modèle de dossier commité ; aucune publication sans accord.

# Phase R — Découvertes réelles

## R1 — Lettres candidates sur un rouleau non lu
### Objectif
Rechercher zones d'encre et lettres candidates sur un rouleau éligible avec une chaîne n'ayant vu aucune région de ce rouleau, sans attendre la fin des travaux intermédiaires.
### Dépendances
L2.2 (provenance), V1 (métriques), P1 ; W2.3 (segments propres sur rouleau éligible, EXP-024).
### Tâches
- [x] R1.1 Audit PHerc0800 (intérêt, segments, qualité, éligibilité, parentés des modèles : reader-v2/LO/ink_9um sans 0800, Hecate et reader-v3 à vérifier) ; inspecter d'abord les prédictions officielles publiées. (`docs/compliance/target-PHerc0800.md` : 17 cm² publiés, aucune lettre lisible ; EXP-024 : 16/17 rouleaux éligibles sans segment publié → goulot = segmentation.)
- [x] R1.2 Inférence de la chaîne figée, cartes privées, examen des faux positifs (fond, fibres) ; zones candidates documentées (coordonnées, méthode, incertitudes) sans publication. (EXP-029 : patch 1218 `out4`, 0 zone candidate, H-034 soutenue mais accord faible.)
- [ ] R1.4 Contrôle positif de notre chaîne de rendu : sur un segment publié à encre connue (PHerc0841 `20260220213127-w00` ou 1667), rendre son tifxyz avec `vc_render_tifxyz` (mêmes réglages qu'EXP-029), inférer reader-v2-LO, comparer à l'inférence sur le surface-volume publié (ρ par blocs, AUC sur labels si disponibles) ; critère écrit avant (EXP-030).
- [ ] R1.5 Étendre la surface propre sur 1218 (plusieurs graines ou croissance plus longue, objectif ≥ 40 cm²) puis appliquer la chaîne validée par R1.4.
- [ ] R1.3 Si ≥ 10 lettres candidates dans 4 cm² : dossier de preuve privé et décision humaine (Discord / soumission).
### Validation
Rapport privé par segment ; aucune image publiée ; décision humaine consignée.

## R2 — Passage inédit validé
### Objectif
Transcrire un passage inédit et le faire valider indépendamment.
### Dépendances
R1, T4, T5.
### Tâches
- [ ] R2.1 Transcription avec statuts et dossier T5.
### Validation
Validation R4 obtenue (humaine).

# Phase Y — Résolution et signal

## Y1 — Gain réel de résolution
### Objectif
Mesurer ce que 2,4 µm (ou plus) apporte vs 9 µm en lisibilité, couverture et coût, sur référence non circulaire.
### Dépendances
V1, P2.
### Tâches
- [x] Y1.1 Requalifier EXP-017 au niveau glyphe (EXP-022 inclut canon/reader-v3/argus-v3) et selon la classe de référence. (Canon +35 points d'UGR sur 0841, McNemar p = 0,03 vs fusion rv2+H ; référence R1, circularité maximale pour canon → H-029.)
- [ ] Y1.2 Comparaison sur une référence R2/R3 (P4) : 9 vs 2,4 µm, coût par cm².
- [ ] E1.3 Reproduction partielle PHerc. 1667 (crop 2,4 µm) vs prédictions publiées.
### Validation
Gain par objet avec IC et classe de référence ; aucune super-résolution comme preuve.

## Y2 — Calcul progressif
### Objectif
Tester analyse globale peu coûteuse → raffinement ciblé, avec contrôle du texte manqué.
### Dépendances
Y1, N1 ou N2.
### Tâches
- [ ] Y2.1 H-025 cascade (ex-K6.3) : rappel ≥ 99 % des UGR à l'étage rapide, économie ≥ 40 %.
### Validation
Adoptée seulement si rappel et lisibilité préservés.

# Phase H — Généralisation

## H1 — Évaluation représentative du corpus
### Objectif
Mesurer la lecture sur plusieurs manuscrits indépendants et différents, par objet, région et difficulté.
### Dépendances
P3, W1.
### Tâches
- [ ] H1.2 Évaluer la meilleure chaîne sur les objets scellés ; rapport par rouleau, résolution, énergie, difficulté ; coût des adaptations et interventions humaines.
- [ ] E1.1 Étendre l'évaluation aux autres segments étiquetés (0139, 0814, 1667, Paris4) en respectant les parentés (comparateurs, non indépendants).
### Validation
Résultats par objet avec IC, classe de référence et fuites documentées.

# Phase N — Méthodes non neuronales et hybrides

## N1 — Texture 3D sans entraînement
### Objectif
Reproduire Korotetskyi & Haindl 2026 puis l'évaluer hors échantillon (priorité abaissée : masques R0, faible intérêt lecture direct).
### Dépendances
B2, C1 ; machine libre (contention CPU).
### Tâches
- [ ] N1.1 EXP-021 / H-022 : reproduction (MCC 0,457 ± 0,02), opportuniste quand aucun calcul n'est en cours.
- [ ] N1.2 H-023 : configuration figée sur nos 5 segments ; mesure aussi au niveau glyphe.
### Validation
Tableau publié/reproduit ; évaluation avec IC, sans réglage sur les objets de test.

## N2 — Baseline physique simple
### Objectif
Mesurer ce que la physique seule apporte à 9 µm.
### Dépendances
B2.
### Tâches
- [ ] N2.1 H-024 : profil le long de la normale + classifieur léger en leave-one-object-out ; aussi au niveau glyphe.
### Validation
AUC sup. et lisibilité glyphe par objet tenu à l'écart ; coût.

# Phase E — Baseline d'encre (acquise, maintenue)

## E1 — Reproduction contrôlée
### Objectif
Maintenir les comparateurs d'encre publiés ; aucune optimisation pixel sans obstacle démontré par V3.
### Dépendances
D1.
### Tâches
- [x] E1.6 Évaluer reader-v3 (référence communautaire First Letters) sur nos 5 segments au niveau glyphe (prédictions officielles déjà locales, EXP-022). (0841 : 4/17 ≈ fusion ; 0009B 7/10 ; absent pour 0500P2.)
### Validation
Inclus dans EXP-022 ou EXP dédiée.

# Phase G — Veille décisionnelle

## G2 — Planification et synthèse
### Objectif
Déclenchement hebdomadaire réel et synthèse transformée en décisions.
### Dépendances
G1.
### Tâches
- [ ] G2.2 Vérifier un déclenchement réel et son rapport ; synthèse mensuelle `docs/state-of-the-art/` + mise à jour des hypothèses.
### Validation
`schtasks /query /tn VesuviusResearchWatch` Last Result 0 et rapport daté du déclenchement.

## G3 — Veille branchée sur les décisions
### Objectif
Aucune expérience importante sans veille consultée ; chaque nouveauté retenue a une fiche.
### Dépendances
G1, G2.1.
### Tâches
- [ ] G3.2 « Veille consultée : <date>, impact » dans chaque README d'EXP importante (première application : EXP-022).
- [ ] G3.3 Fiche par nouveauté retenue (12 questions de l'invariant) et hypothèse si comparaison pertinente.
- [x] G3.4 Sources de veille ajoutées : page `winners`, Hugging Face `scrollprize` + modèles communautaires cités (§3 de la revue). (`src/vesres/watch.py` : pages `winners`, `2026_open_problems`, source `hf_community` ; `tests/test_watch.py` 5 verts, appel réseau réel OK.)
### Validation
Deux EXP au moins citant la veille ; fiches présentes.

## G4 — Recherche interdisciplinaire
### Objectif
Importer des méthodes d'autres disciplines quand un obstacle le justifie, sous forme d'hypothèses falsifiables.
### Dépendances
V3.
### Tâches
- [ ] G4.1 Pour chaque obstacle V3 : recherche ciblée (physique, imagerie médicale, signal, graphique, statistiques, linguistique, papyrologie), compatibilité physique vérifiée, hypothèse `H-NNN`.
### Validation
Au moins une hypothèse issue d'une autre discipline testée ou écartée par argument écrit.

# Phase K — Efficacité

## K3 — Courbes performance/temps EXP-018
### Objectif
Situer le rendement décroissant de la référence 40k à coût faible (sans nouvel entraînement).
### Dépendances
E1.5, K2.1.
### Tâches
- [x] K3.1 Perte et débit depuis les journaux EXP-018 ; coût réel par phase. (EXP-026 : −1,5 % de perte entre 13 k et 40 k, 1,69 it/s limité par les données ; journal 0–13 k perdu.)
- [ ] K3.2 Inférence de checkpoints échantillonnés sur la validation K ; test en descriptif seulement.
### Validation
EXP avec courbes, coûts, statut descriptif des courbes sur test.

## K4 — Durée minimale (suspendue)
### Objectif
Recette plus courte non inférieure — suspendue tant qu'aucune recette neuronale n'est retenue dans le système de lecture.
### Dépendances
K3, V3.
### Tâches
- [ ] K4.1 Entraînements courts recuits, non-infériorité sur validation K2.1.
- [ ] K4.2 Confirmation unique sur test après décision.
- [ ] K4.3 Arrêt anticipé si plateau exploitable.
### Validation
Non-infériorité (IC 95 % < δ) ou résultat négatif consigné.

## K5 — Débit (suspendue)
### Objectif
Réduire le temps par itération — même condition que K4.
### Dépendances
K1.1, V3.
### Tâches
- [ ] K5.1 Profilage GPU / DataLoader / I/O ; cache de recherche de patches.
- [ ] K5.2 Leviers un à un (≥ 10 % de gain, métriques dans δ).
- [ ] K5.3 Intégration à la recette par défaut.
### Validation
Tableau avant/après par levier.

## K6 — Coût de la chaîne
### Objectif
Mesurer le coût total de la chaîne de lecture par cm² et réutiliser les artefacts.
### Dépendances
K1.1.
### Tâches
- [ ] K6.1 Manifeste de coût standard par EXP ; coût par cm² du chemin v0.
- [ ] K6.2 Inventaire des artefacts réutilisables et règles de compatibilité.
### Validation
Tableau de coûts reproductible.

# Phase L — Compatibilité Vesuvius Challenge

## L1 — Matrice de conformité
### Objectif
Matrice sourcée à jour (≤ 1 mois) ; inconnues explicites.
### Dépendances
Aucune.
### Tâches
- [x] L1.1 Matrice initiale (2026-11-26).
- [ ] L1.2 Revue mensuelle et à chaque alerte `rules_pages` (actualisée 2026-11-27 avec la veille ; relire la formulation exacte de `prizes`).
- [ ] L1.3 Questions écrites prêtes (agents IA, pays, licence ↔ open source, transcription 1667) dans la matrice ; envoi = action humaine.
### Validation
Date ≤ 1 mois ; chaque ligne sourcée ; questions rédigées.

## L2 — Interopérabilité
### Objectif
Sorties utilisables par VC3D/villa ; audit de provenance par rouleau cible.
### Dépendances
L1.1, P1.
### Tâches
- [ ] L2.1 Export carte d'encre OME-Zarr/TIFF sur grille tifxyz + image programmatique (barre 1 cm), privé.
- [ ] L2.2 Audit de provenance par rouleau cible (PHerc0800 d'abord) avant toute prédiction.
### Validation
Chargement VC3D/villa sans conversion manuelle ; audit écrit par rouleau.

# Phase M — Open source, reproductibilité, stockage

## M1 — Dépôt public
### Objectif
Dépôt public sûr et lisible.
### Dépendances
Aucune.
### Tâches
- [ ] M1.4 Décision humaine : e-mail des commits (noreply pour l'avenir ; réécriture d'historique seulement sur demande).
### Validation
Décision consignée.

## M2 — Reproductibilité externe
### Objectif
Rejouer une expérience clé depuis zéro sans notre infrastructure.
### Dépendances
M1.3.
### Tâches
- [ ] M2.1 Environnements verrouillés documentés + `Dockerfile`.
- [ ] M2.2 Rejouer EXP-001 depuis un clone propre.
- [ ] M2.3 Contributions communautaires candidates (métrique glyphe sans fuite, inventaire de couverture, évaluation par classe de référence) — soumission sur autorisation humaine.
### Validation
Rejeu EXP-001 identique (12/12).

## M3 — Stockage scientifique et sauvegarde
### Objectif
Distinguer cache et artefacts uniques ; sauvegarder et vérifier ces derniers.
### Dépendances
Aucune.
### Tâches
- [ ] M3.1 Manifeste sha256 des artefacts uniques (checkpoints EXP-018, sorties privées) et copie sur le NAS ; test de restauration d'un fichier.
- [ ] M3.2 Politique d'espace : C: libre en baisse (229 Gio) → éviction du cache reproductible avant tout téléchargement > 20 Go.
### Validation
Manifeste commité (sans données) ; restauration vérifiée par sha256.

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

# Phase F — Boucle expérimentale

## F1 — Règles de la boucle
### Objectif
Hypothèse → protocole → expérience → décision, sans boucle improductive.
### Dépendances
E1, B3.
### Tâches
- [x] F1.1 Registre `experiments/registry.csv`, manifestes par EXP, règle d'arrêt proportionnée (`docs/protocols/research-loop.md`).
### Validation
Chaque EXP a manifeste, conclusion et lien vers hypothèse.
