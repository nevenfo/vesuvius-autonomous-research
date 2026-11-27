# Protocole d'évaluation de la lecture (2026-11-27)

But : juger une chaîne sur ce qu'elle permet de **lire**, pas seulement sur des pixels. Indépendant de la méthode
(neuronale, physique, géométrique, hybride). Les métriques d'encre (AUC/AP/ECE) restent des diagnostics.

## 1. Niveaux et sorties exigées
| Niveau | Question | Sortie minimale | Métriques (définies avant usage) | Référence requise |
|---|---|---|---|---|
| 1 Observation physique | quelles structures sont dans les données ? | carte d'encre/structure + provenance (scan, résolution, segment, coordonnées, paramètres, commit) | AUC/AP/ECE région supervision ; couverture (`coverage.md`) | ink-labels (classe R ≥ 1) |
| 2a Unités graphiques | où sont les glyphes ? | liste d'UGR détectées (boîte, score) | **lisibilité locale par UGR** (AUC locale ≥ 0,90), fraction lisible par objet, candidats glyphes en fond / cm² | composantes des labels (`src/vesres/reading.py`) |
| 2b Caractères | quel caractère ? | caractère + probabilité + alternatives, ou abstention | précision/rappel par classe, CER, taux d'abstention, calibration (ECE) | identités de caractères localisées (R2+) |
| 3 Mots | quels mots ? | segmentation en mots, statut par mot | WER, exactitude sur mots attestés | transcription humaine alignée (R2+) |
| 4 Phrases | texte cohérent ? | lecture(s) concurrente(s) avec contradictions observées | fidélité de passage (CER/WER sur passages), continuité des lignes | transcription papyrologique (R3) |
| 5 Traduction | sens ? | transcription diplomatique, normalisée, traduction, lacunes | exactitude sémantique jugée par spécialiste | traduction publiée (R3) |
| 6 Validation | lecture confirmée ? | dossier de preuve | accord indépendant | papyrologue aveugle (R4) |

## 2. Statuts obligatoires (aucune sortie sans statut)
`Observé` structure présente · `Reconnu` caractère identifié avec preuve et incertitude · `Probable` plausible,
insuffisamment confirmé · `Restitué` proposition linguistique comblant une lacune · `Inconnu` · `Validé` confirmé
par preuve indépendante adaptée. Règles : une restitution n'est jamais promue en observation ; un modèle de langue
peut **ordonner** des alternatives ou signaler une contradiction, jamais servir de preuve de présence d'encre ;
diplomatique et normalisée sont deux fichiers distincts.

## 3. Contrôles obligatoires (anti-hallucination)
- Contrôle positif (labels flous + bruit) et contrôle négatif (prédiction tournée de 180° ou décalée) pour toute
  métrique nouvelle : la métrique doit séparer les deux (ex. H-026).
- Régions sans texte (papyrus vierge, fond revu loin de l'encre) : taux de caractères/glyphes produits par cm².
- Fibres et structures ressemblant à des lettres : échantillon dédié dès qu'un étage de reconnaissance existe.
- Texte inversé/permuté pour tout étage linguistique : la lecture doit se dégrader.
- Abstention mesurée : un système qui s'abstient sur l'incertain est préféré à un système qui invente.

## 4. Conventions
- Résultats **par objet et par segment** ; aucune moyenne inter-objets sans le détail ; un échec n'est pas masqué.
- Chaque métrique porte la classe d'indépendance de sa référence (`independence.md`) ; une conclusion ne dépasse
  jamais ce que la classe autorise (R1 ⇒ « accord avec une référence en partie pseudo-étiquetée »).
- Seuils fixés avant mesure ; aucun réglage sur les objets de test scellés.
- Pas de score global agrégé opaque ; en cas de compromis : fidélité et couverture d'abord.
- Coordonnées d'UGR et images d'encre = privées (licence) : seuls des agrégats sont publiés.

## 5. Limites actuelles (à lever)
Aucune référence R2+ au niveau caractère n'est disponible publiquement (`docs/research-review-2026-11-27.md` §3) :
les niveaux 2b–6 sont définis mais non mesurables à ce jour. Les UGR sont des glyphes ou groupes de glyphes, pas des
lettres identifiées.
