# Audit et refonte stratégique (2026-11-27)

Remplace les priorités de `docs/research-review-2026-11-26.md` (conservé pour l'historique).
Base : HEAD `110c831` + travaux du 2026-11-27, `experiments/registry.csv` (EXP-001…018 terminées, 019/020 préparées,
021 en cours), `docs/hypotheses.md`, `docs/data/splits.md`, veille `watch/reports/` et recherche ciblée du jour (§3),
Second Brain (`wiki/concepts/envie-contribution-vesuvius-challenge.md`). Tests du dépôt réexécutés : 16 verts.

Statuts de preuve : **V** vérifié par nous (recalcul/reproduction) · **R** rapporté par une source, non reproduit ·
**I** inféré.

## 1. Audit des acquis historiques

Classes d'indépendance des références (définies dans `docs/protocols/independence.md`) : R0 accord avec un autre
modèle · R1 labels humains affinés par pseudo-labeling d'une famille de modèles possiblement parente · R2 annotation
humaine indépendante des modèles évalués · R3 référence physique indépendante (IR) ou lecture papyrologique ·
R4 validation papyrologique indépendante d'une lecture nouvelle.

| EXP | Objectif initial | Démontré (statut) | Limites / indépendance | Intérêt pour la lecture | Réutilisable | Réévaluer ? |
|---|---|---|---|---|---|---|
| 001/001b | reproduire reader-v2, ink_9um sur 0841 | 12/12 valeurs publiées reproduites (V) | réf. R1 (pseudo-labeling, modèle inconnu) ; 3 segments, 1 objet | faible direct ; base de toute mesure | chaîne d'évaluation `eval_ink` | non |
| 002 | fusion rv2+ink_9um ; FP de validation | fusion dégrade (V) ; détections hors labels en validation (R0) | accord inter-modèles = R0 | moyen : la région `validation` n'est pas une référence | choix région supervision | non |
| 003 | reproduire Hecate ; fusion | 6/6 AUC (V) ; fusion +0,025 AP (V, non robuste) | Hecate : rouleaux d'entraînement non publiés | faible (pixel) | fusion de référence | au niveau glyphe (EXP-022) |
| 004 | 2e objet, 116 keV | rv2 0,927 sur 0009B (V) | objet vu par rv2 | moyen : robustesse énergie | — | non |
| 005 | encre non étiquetée ? | test non discriminant (V) | R0 inutilisable comme juge | **leçon de méthode** : l'accord de modèles ne prouve rien | — | non |
| 006 | décalage de couches | défaut déjà centré (V, négatif) | 0841 seulement | faible | — | non |
| 007 | incertitude sans label | entropie ≈ confiance, pas mieux (V, négatif) | 0841 | **couverture** : l'incertitude d'un modèle ne suffit pas à classer « incertain » | — | non |
| 008 | circularité au niveau objet | DiD −0,001 (V) | circularité des pseudo-labels eux-mêmes non testée | moyen | DiD | non |
| 009 | géométrie vs erreurs | ρ < 0,2 (V, négatif) | surfaces quasi isométriques ; sauts de feuillet non testés | géométrie non limitante **sur ces surfaces faciles** | métriques de surface | sur surfaces difficiles (W2) |
| 010 | puissance du protocole | ρ min. détectable 0,12–0,26 (V) | — | méthode | contrôle positif | non |
| 011 | fusion sur 0500P2 | +0,023 AP (V, IC chevauche 0) | R1 ; objet vu par rv2 | faible | — | non |
| 012 | calibration | ECE 0,12–0,18 (V, négatif) | — | seuils fixes non fiables → métriques sans seuil | ECE | non |
| 013 | fusion calibrée | pas de gain AP ; ECE transférable (V) | — | faible | calibration LOO | non |
| 014 | bords de labels | erreurs surtout intérieures (V) | — | faible | — | non |
| 015/016 | TTA | gain sur objet non vu seulement, non cumulable (V) | — | faible | — | non |
| 017 | prédictions officielles 2,4 µm | canon +0,042 AUC sur 0841 (V sur prédictions publiées) | **R1 probablement circulaire** : labels pseudo-labelés, famille canon possible | **résolution** : gain non attribuable | comparateurs | oui (Y1, référence R2+) |
| 018 | reader-v2 sans objets de test | H-017 soutenue (V) | LO distillé de la carte canon 2,4 µm d'autres objets ; références R1 | permet ≥ 3 objets « non vus » au sens objet | checkpoints / 1000 | non (mais statut R1) |
| 019/020 | durée, WSD | préparées, non exécutées | — | coût seulement | scripts | suspendues (K) |
| 021 | texture 3D sans entraînement | reproduction en cours | masques R0, MCC in-sample | faible direct | — | priorité abaissée |

**Constats transverses** (V sauf mention) :
1. 18/18 expériences mesurent la détection d'encre au pixel ; aucune ne mesure un caractère, un mot, une couverture.
2. Les labels des 5 segments ne contiennent que **6 à 12 composantes de taille glyphe** chacun (≈ 3 × 3,5 mm), sur
   1,4–3,0 cm² de région supervisée par segment de 10–27 cm² : toutes les AUC reposent sur ≈ 45 unités de 3 objets.
3. Toutes les références sont R0 ou R1 : aucune n'est démontrée indépendante des familles de modèles évaluées.
4. Toute la chaîne commence à une surface déjà segmentée par la communauté et s'arrête à une carte d'encre.
5. Résolution : 9 µm partout ; la seule comparaison 2,4 µm (EXP-017) est probablement biaisée par la référence.
6. Les objets de test ont été consultés par 18 expériences : ils restent des comparateurs rétrospectifs, plus une
   validation finale scellée (`docs/protocols/independence.md` §4).

## 2. Les douze défauts et leur traitement

| # | Défaut | Traitement dans le plan refondu |
|---|---|---|
| 1 | Optimisation d'un composant | priorité au chemin de lecture (V) ; leviers d'encre seulement si l'analyse d'obstacles V3 les désigne |
| 2 | Géométrie peu évaluée | W2 : évaluer VC3D/autoseg/fibres existants par leur contribution à la couverture ; développement propre seulement si obstacle démontré |
| 3 | Pas de bout en bout | V1 (EXP-022) : chemin v0 assemblé et mesuré ; V2 : étage reconnaissance ; V3 : bilan d'obstacles |
| 4 | Métriques loin de la lecture | `docs/protocols/reading-evaluation.md` : niveaux 1–6, UGR, CER/WER, abstention, hallucinations |
| 5 | Circularité | `docs/protocols/independence.md` : graphe de provenance, classes R0–R4, requalification (P1–P2) |
| 6 | Généralisation | H1 refondu : objets représentatifs, résultats par objet, test scellé (P3) |
| 7 | Reconnaissance du texte | Phase T : caractères → mots → phrases → traduction, statuts Observé…Validé |
| 8 | Résolution | Phase Y : gain réel 2,4 vs 9 µm au niveau glyphe et sur référence R2+, calcul progressif |
| 9 | Découvertes éloignées | R1 découplé de N : exploration PHerc0800 après audit de provenance, dès maintenant |
| 10 | Optimisation prématurée | K4/K5 suspendus tant qu'aucune recette neuronale n'est retenue dans le système de lecture |
| 11 | Couverture | `docs/protocols/coverage.md` ; W1 inventaire de couverture du corpus ; cartes par segment |
| 12 | Validation externe / conformité | L1 actualisée (§3) ; procédure de validation externe (T6) ; questions écrites préparées (L1.3) |

## 3. Connaissances communautaires actualisées (recherche ciblée du 2026-11-27)

| Fait | Source | Statut | Conséquence |
|---|---|---|---|
| Aucune transcription alignée publique pour PHerc. 1667 (preprint arXiv:2606.29085, 9 papyrologues) ; PDF non lu | <https://arxiv.org/abs/2606.29085>, <https://scrollprize.org/data_browser/PHerc1667> | V (page) / NV (PDF) | référence caractère indisponible ; lire le PDF (T1.1) puis question écrite aux auteurs (L1.3) |
| Paris 4 : transcriptions/traductions interdites sans permission jusqu'au 2027-06-25 | <https://scrollprize.org/data_browser/PHercParis4> | V | pas de référence Paris 4 |
| PHerc. 172 : 25 « glyph slabs », masques dérivés d'une prédiction (CC BY-NC) | Zenodo 10.5281/zenodo.24392114 | V | R0 ; ne sert pas de vérité caractère |
| ICDAR 2023 lettres grecques sur papyrus : 150 images, boîtes + classes, CC BY-NC (images : licences variables) | <https://zenodo.org/records/13825619> | V | jeu de fond pour un classifieur de glyphes (écart de domaine photo → CT à mesurer) |
| AL-PUB (Oxyrhynque) ≈ 205 k vignettes de lettres | <https://arxiv.org/abs/2401.12513> | NV (licence) | candidat de pré-entraînement de glyphes |
| Aucun OCR communautaire sur cartes d'encre | recherche du jour | V (absence constatée, recherche limitée) | contribution ouverte possible |
| First Letters 2026 attribués : 306B, 343 (oct.), 846A, 846B, 211 partiel (nov.) ; reader-v3 majoritairement utilisé | <https://scrollprize.org/winners> | V | la méthode « bon modèle 9,6 µm + segments » suffit à trouver des lettres ; R1 réaliste |
| Premier First Letters 2023 : panel papyrologique avec confiance par lettre (> 80 / 50–80 / < 50 %) | <https://scrollprize.org/firstletters> | V | modèle de statut « reconnu/probable » pour T |
| PHerc0800 : ESRF 8,64 µm 116 keV, 6 segments avec prédiction d'encre officielle, aucune lettre annoncée, éligible | <https://scrollprize.org/data_browser/PHerc0800> | V | cible R1 plausible |
| Grand Prize 2027 : 100 % du recto (fragments détachés inclus, morceaux externes < 10 % omissibles), ≥ 70 % des caractères conservés lisibles par colonne sans interpolation ; ≤ 8 h d'intervention humaine | <https://scrollprize.org/prizes>, substack 2026-07-15 | V (résumé) | métrique glyphe et couverture alignées sur ces critères |
| First Letters : préentraînés/données externes autorisés si licence ; scans plus résolus du même rouleau interdits ; données d'entraînement publiées CC BY-NC ; aucune règle IA générative explicite | <https://scrollprize.org/prizes> | V (résumé, formulation exacte à relire) | matrice L1 actualisée |
| Géométrie : « no method yet traces a complete, correct surface automatically » ; sheet switches corrigés à la main ; aucune métrique publique de couverture par rouleau ; 172 « ~70 % » déroulé | <https://scrollprize.org/2026_open_problems>, <https://scrollprize.substack.com/p/the-hard-parts-are-getting-clearer> | V | une métrique de couverture ouverte est une contribution utile (W1) |
| Résolution : couches séparables à 2,4 µm, fondues à 7,91 µm (Paris 4) ; aucune comparaison quantitative 9 vs 2,4 µm publiée | open problems | V | Y1 a une valeur propre |
| Nouveaux modèles : `ink_canonical_2um`, `ink_3d_dino_guided`, `domenicor046/ink9um-dense`, `evilaliv3/rectina` (+0,01 AUC vs reader-v3, au niveau du bruit) | Hugging Face | V | comparateurs ; pas de nouveau levier pixel prioritaire |

## 4. Obstacles prioritaires à la lecture (classement argumenté)

1. **Absence de référence indépendante au niveau caractère** : bloque toute mesure CER/WER, toute validation de
   reconnaissance et rend circulaires les comparaisons d'encre (R1). Levier : références R2/R3 (IR des fragments,
   lectures publiées First Letters, demande écrite 1667), redondance de surfaces, annotation propre documentée.
2. **Couverture inconnue** : on ne sait ni quelle part de chaque rouleau est segmentée, ni ce qui est examiné ;
   condition de toute « lecture intégrale ». Levier : W1 (catalogue + méta des segments), cartes par segment.
3. **Étage de reconnaissance inexistant** : aucune sortie au-delà de la carte d'encre. Levier : T2–T3.
4. **Généralisation non démontrée** : 3 objets, références R1. Levier : P3 + H1 + R1 sur rouleau inédit.
5. **Résolution** : gain 2,4 µm non attribuable. Levier : Y1 au niveau glyphe sur références R2+.
Les leviers d'encre au pixel (calibration, fusion, TTA, durée d'entraînement) ne sont pas des obstacles prioritaires.

## 5. Sélection des prochaines expériences (questions de `docs/protocols/research-loop.md`)

| Expérience | Obstacle | Pourquoi maintenant | Gain attendu / vérification | Info même en échec | Coût | Alternative moins chère |
|---|---|---|---|---|---|---|
| EXP-022 (V1) | métriques loin de la lecture | données et prédictions locales | métrique glyphe validée par contrôles (H-026) ; niveau atteint (H-027) | savoir si nos références permettent une mesure glyphe | < 1 h CPU | aucune |
| EXP-023 (W1) inventaire de couverture du corpus | couverture inconnue | métadonnées publiques, sans GPU | surface segmentée par rouleau vs estimation physique, bornes | quantifier l'inconnu | réseau léger, < 1 h | aucune |
| EXP-024 (R1) exploration PHerc0800 | découvertes, généralisation | First Letters attribués avec méthodes équivalentes | zones/lettres candidates privées, examen faux positifs | taux de faux glyphes sur rouleau inédit | téléchargements Go + inférence h | prédictions officielles 0800 (déjà publiques) d'abord |
| T1 références caractère | référence indépendante | bloquant principal | inventaire R2/R3 exploitable, question écrite | — | faible | — |
| EXP-021 (N1.1) | méthode non neuronale | engagée, CPU | reproduction | — | CPU < 1 j, contention | opportuniste quand la machine est libre |

Écartés pour l'instant (révisables) : K4/K5 (optimisation d'entraînement), nouveaux leviers d'encre au pixel,
développement géométrique propre, super-résolution.
