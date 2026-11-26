# Revue scientifique et repriorisation (2026-11-26)

Base : `experiments/registry.csv` (EXP-001…018), `docs/hypotheses.md` (H-001…H-021), veille 2026-11-12/16/23,
recherches K1 (`docs/state-of-the-art/training-efficiency.md`), conformité (`docs/compliance/vesuvius-challenge-matrix.md`),
recherche « détection non neuronale » du 2026-11-26 (sources ci-dessous).

## 1. Acquis (preuves)
- Chaîne d'évaluation sans fuite, reproduite et auditée : reader-v2 reproduit à 12/12 valeurs publiées (EXP-001),
  protocole sain (EXP-010), métrique primaire = région `supervision` (EXP-002).
- Référence d'encre 9 µm : fusion moyenne reader-v2 + Hecate, gain ≈ +0,02 AP de même signe sur 3 objets
  (EXP-003/004/011), non robuste statistiquement.
- Résultats négatifs utiles : leviers post-hoc épuisés (calibration, fusion par rangs, bords des labels, fenêtre de
  couches, indicateurs sans label, géométrie de surface : EXP-006/007/009/012/013/014/016) ; TTA utile seulement sur
  objet non vu (EXP-015/016).
- Les prédictions officielles 2,4 µm dépassent la fusion 9 µm (EXP-017, indicatif : labels en partie pseudo-labels).

## 2. Diagnostic
1. **Biais de méthode** : 18/18 expériences évaluent des réseaux publiés ; aucune méthode non neuronale, physique
   ou géométrique n'a été testée. L'invariant « méthode la plus simple à qualité comparable » n'a jamais été exercé.
2. **Biais de stade** : tout porte sur la détection d'encre sur 5 segments déjà lus ; rien sur segmentation,
   déroulement, localisation de lettres, ni sur des rouleaux non lus.
3. **Circularité des labels** : la plupart des labels publiés sont dérivés de modèles (canon, timesformer,
   pseudo-labeling itératif, EXP-017/018) → nos métriques mesurent souvent l'accord avec un autre modèle.
4. **Généralisation** : un seul objet étiqueté réellement indépendant des modèles 9 µm (0841) ; E1.5 (EXP-018) en cours pour 0009B/0500P2.
5. **Lecture réelle** : aucune lettre candidate, aucune zone nouvelle ; nos objets de test ne sont éligibles à aucun prix.

## 3. Problèmes ouverts (sources)
- Physique : encre carbonée quasi iso-atténuante ; signal surtout morphologique (relief 3–5 µm, Parker 2019,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6505748/>) ; contraste de phase du relief (Mocella 2015,
  <https://www.nature.com/articles/ncomms6895>) ; morphologie quasi perdue au-delà de ~1–3 µm en profilométrie
  (Angelotti et al. 2026, <https://arxiv.org/abs/2603.27698>) → la résolution 9 µm limite toute méthode.
- Problèmes officiels 2026 (<https://scrollprize.org/2026_open_problems>) : généralisation inter-rouleaux, plateau
  des pseudo-labels, labels de surface approximatifs, régions compressées, ambiguïté de profondeur ;
  détection 3D sur volume non aplati comparable à la 2,5D (<https://scrollprize.substack.com/p/we-are-cooking>).
- Non neuronal : quasi vierge publiquement, sauf **Korotetskyi & Haindl 2026** (Zenodo 10.5281/zenodo.24391747,
  code 10.5281/zenodo.24392114, trouvé par la veille Zenodo le 2026-11-26) : 10 descripteurs de texture 3D,
  sans entraînement, MCC 0,457 sur 25 glyphes de PHerc. 172 **in-sample** (configuration choisie sur ces glyphes),
  référence = prédiction communautaire neuronale, pas de transfert utile démontré sur 5 autres rouleaux.

## 4. Priorités (information attendue × impact lecture / coût)
| Rang | Piste | Pourquoi | Coût | ID |
|---|---|---|---|---|
| 1 | Conclure H-017 (EXP-018) | engagé ; donne 2 objets de test indépendants de plus (J5) | ~1 h après fin d'entraînement | E1.5 |
| 2 | Reproduire puis tester hors échantillon la détection par texture 3D sans entraînement sur nos 5 segments (config figée), seule et comme entrée/fusion avec reader-v2 | seule référence non neuronale reproductible ; teste l'invariant « méthode simple » ; explicable | CPU, ~0,5–1 j | N1, H-022/H-023 |
| 3 | Baseline physique simple : profils d'intensité le long de la normale (différences de couches, gradient) + petit classifieur évalué en leave-one-object-out | quantifie ce que la physique seule apporte à 9 µm, borne inférieure de toute méthode | faible | N2, H-024 |
| 4 | Recherche de lettres candidates sur un rouleau éligible First Letters (PHerc0800 : 12 segments au catalogue) avec la meilleure chaîne n'ayant vu aucune région de ce rouleau | premier pas vers une découverte réelle ; teste la généralisation sans label | moyen (téléchargements, inférence) | R1 |
| 5 | Durée d'entraînement / débit (Phase K, déjà protocolée) | réduit le coût de toutes les pistes neuronales futures | après E1.5 | K3–K5 |
| 6 | Cascade adaptative (rapide → coûteux) | gain de calcul potentiel ; risque d'encre manquée → hypothèse à mesurer, rappel étage 1 ≥ 99 % | après N1/N2 | K6, H-025 |
| 7 | Open source : README anglais, chemins configurables, Docker | reproductibilité externe, Progress Prizes | faible | M1–M2 |

Écartées pour l'instant : nouveaux leviers post-hoc (épuisés), ré-entraînements neuronaux sans protocole K,
segmentation/déroulement propres (VC3D/villa couvrent le besoin ; réutilisation d'abord).

## 5. Garde-fous
Aucune lettre ou zone « découverte » sans preuves visuelles privées, coordonnées, provenance, méthode et
incertitudes ; pas de publication hors Discord officiel sans accord écrit (licence) ; pas de caractère restauré présenté comme observé.
