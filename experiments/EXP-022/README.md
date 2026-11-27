# EXP-022 — V1 / H-026, H-027 : chemin de lecture v0 et lisibilité au niveau glyphe

**Statut : terminé** — H-026 soutenue, H-027 réfutée (hypothèses et critères fixés le 2026-11-27 avant toute mesure).

## Obstacle visé
Les 18 expériences précédentes mesurent des pixels (AUC/AP). La lecture se juge au niveau du caractère
(Grand Prize 2027 : ≥ 70 % des caractères lisibles par colonne). Il manque (i) une mesure au niveau glyphe,
(ii) une mesure de ce que couvrent réellement nos références. EXP-022 assemble le chemin v0
« surface communautaire → surface-volume officiel → encre (chaînes existantes) → unités graphiques →
lisibilité locale + couverture » et nomme l'étage manquant (identification des caractères, phase T).

## Veille consultée
Rapport `watch/reports/2026-11-23.md` + recherche ciblée du 2026-11-27 (`docs/research-review-2026-11-27.md` §3) :
aucune référence publique au niveau caractère alignée sur des coordonnées (1667 : non publiée ; Paris 4 : embargo
jusqu'au 2027-06-25 ; 172 : masques dérivés d'un modèle) ; aucun OCR communautaire sur cartes d'encre.
→ la seule référence localisée disponible est la forme des ink-labels ; d'où des unités graphiques (UGR), pas des lettres.

## Constat préalable (prototype, avant hypothèses)
Les ink-labels des 5 segments ne contiennent que **6 à 12 composantes de taille glyphe** chacun (≈ 3 × 3,5 mm,
à 2,4 µm natif comme sur la grille 9 µm) ; la région `supervision` couvre 1,4–3,0 cm² sur 10–27 cm² de segment.
Toutes les AUC historiques (EXP-001…018) reposent donc sur ≈ 45 unités de référence de 3 objets.

## Définitions (`src/vesres/reading.py`)
- UGR : composante connexe des ink-labels (grille de prédiction), ≥ 200 px, ≥ 50 % en supervision.
- Lisibilité locale : AUC des scores des pixels de l'UGR contre un anneau de 48 px (≈ 0,45 mm) de fond revu,
  hors encre dilatée de 3 px. « Lisible » si AUC locale ≥ 0,90 (seuil principal), 0,80 rapporté.
- Contrôle positif : labels flous (σ = 2 px) + bruit 0,05. Contrôle négatif : prédiction tournée de 180°.
- Candidats glyphes en fond : composantes `p ≥ 0,5` d'aire comprise entre 0,25× et 4× l'aire médiane des UGR,
  ≥ 95 % dans le fond revu à plus de 48 px de toute encre étiquetée ; par cm² de fond.
- Couverture : segment / référence fiable (supervision) / revu sans référence fiable (validation seule) / non revu.

## Hypothèses et critères (fixés avant mesure)
- **H-026 (validité de la mesure)** : sur les 5 segments, le contrôle positif est lisible pour ≥ 95 % des UGR et le
  contrôle négatif (rotation, meilleure chaîne 9 µm propre) pour ≤ 20 %. Réfutée sinon (métrique non discriminante).
- **H-027 (niveau atteint)** : la chaîne 9 µm la plus propre vis-à-vis des objets de test (fusion reader-v2-LO +
  Hecate) rend lisibles (AUC locale ≥ 0,90) ≥ 70 % des UGR de 0841 (objet vu par aucun modèle d'encre évalué ;
  Hecate : liste non publiée). Réfutée si < 70 %. Descriptif : toutes les chaînes et les 3 objets.
- Aucune décision de configuration n'est prise sur ces objets : seuils et tailles ci-dessus sont figés a priori.

## Limites connues (avant résultats)
- UGR ≠ lettre identifiée ; les labels de rouleaux sont en partie des pseudo-labels (circularité possible avec les
  modèles de la famille canon, `docs/protocols/independence.md`) → référence de classe R2 au mieux.
- ≈ 45 unités : puissance faible ; résultats par objet, sans agrégation masquant un échec.
- Sorties privées (coordonnées d'UGR = positions de texte caché) : `results.json` ne publie que des agrégats.

## Exécution
`PYTHONPATH=src python experiments/EXP-022/analyze.py <VESRES_WORK> experiments/EXP-022/results.json <VESRES_WORK>/runs/EXP-022/units_private.json`
— 50 s CPU (commit de ce README) ; prédictions existantes (EXP-001/004/008, E1, E1.4, EXP-017, EXP-018), aucune inférence.

## Résultats (UGR lisibles à AUC locale ≥ 0,90 ; IC 95 % de Wilson ; ≥ 0,80 entre parenthèses)
| Chaîne | 0841 (17 UGR, non vu*) | 0009B (10 UGR) | 0500P2 (12 UGR) |
|---|---|---|---|
| reader-v2 | 3/17 = 0,18 (0,47) | 0,50 (1,00) | 0,17 (0,67) |
| reader-v2-LO | 2/17 = 0,12 (0,41) | 0,30 (1,00) | 0,17 (0,67) |
| Hecate | 3/17 = 0,18 (0,65) | 0,20 (1,00) | 0,25 (0,92) |
| fusion reader-v2 + Hecate | 5/17 = 0,29 [0,13-0,53] (0,65) | 0,60 (1,00) | 0,42 (1,00) |
| **fusion LO + Hecate** (H-027) | **5/17 = 0,29 [0,13-0,53]** (0,65) | 0,50 (1,00) | 0,42 (0,92) |
| reader-v3 (officiel) | 4/17 = 0,24 (0,65) | 0,70 (1,00) | — |
| argus-v3 (officiel) | 6/17 = 0,35 (0,71) | 0,70 (1,00) | — |
| canon 2,4 µm (officiel) | **11/17 = 0,65 [0,41-0,83]** (0,88) | 0,70 (1,00) | **12/12 = 1,00 [0,76-1,00]** |
| contrôle positif / négatif | 1,00 / 0,00 | 1,00 / 0,00 | 1,00 / 0,00 |
\* 0841 n'a été vu par aucun modèle 9 µm évalué (Hecate : liste non publiée) ; canon 2,4 µm : parenté inconnue.

Par segment, 0841 : canon 1,00 / 0,67 / 0,20 ; fusion LO+Hecate 0,33 / 0,17 / 0,40 → forte hétérogénéité.
Tests appariés (McNemar exact, UGR discordantes) : canon > fusion reader-v2+Hecate sur 0841 (6/0, p = 0,031) et
0500P2 (7/0, p = 0,016) ; canon vs fusion LO+Hecate sur 0841 p = 0,070 ; reader-v3 ≈ fusion (0/1, p = 1) ;
LO ≈ reader-v2 dans la fusion (1/1).
Couverture des références : la région fiable (supervision) ne représente que **6,8–22 %** des segments
(0841 : 0,86–1,40 cm² sur ≈ 12,5 cm² ; 0009B 3,0 / 26,9 cm², 23,9 cm² non revus ; 0500P2 2,2 / 10,2 cm²).
Candidats glyphes en fond : 0 partout sauf argus-v3 (1 sur 0841_174252) — **non informatif** : le fond revu à
plus de 0,45 mm de l'encre ne couvre que ≈ 0,5 cm² par segment.

## Conclusions
- **H-026 soutenue** : la métrique sépare parfaitement contrôles positif (100 %) et négatif (0 %, AUC locale
  médiane 0,47–0,52) → mesure glyphe utilisable.
- **H-027 réfutée** : la meilleure chaîne 9 µm propre rend fortement lisibles 29 % [13-53 %] des UGR de 0841 (65 % au
  seuil 0,80). À 9 µm, environ un glyphe de référence sur trois atteint un contraste local élevé sur l'objet non vu.
- Le passage du pixel au glyphe **amplifie** l'écart de résolution : +0,042 d'AUC pixel (EXP-017) devient +35 points
  d'UGR lisibles (0841) et +58 (0500P2) pour canon 2,4 µm. Mais la référence est R1 et l'alignement des labels a été
  calé sur le rendu canonique : la circularité est **maximale précisément pour canon** → Y1 (référence R2/R3)
  devient la question décisionnelle prioritaire sur la résolution.
- Les leviers 9 µm récents n'apportent rien au niveau glyphe (reader-v3 ≈ fusion ; LO ≈ reader-v2).
- Limites : 39 UGR, 3 objets, référence R1 ; AUC locale ≠ lisibilité humaine (calibration par jugement humain à
  faire, P4) ; proxy d'hallucination non mesurable avec ces régions.
