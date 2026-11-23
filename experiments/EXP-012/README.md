# EXP-012 — H-011 : calibration de reader-v2, Hecate et fusion (région supervision)

- **Date** : 2026-11-23 · aucune inférence : prédictions existantes (EXP-001/E1, E1.4, EXP-004, EXP-008), uint8 → p = x/255.
- **Segments** : 0841 × 3, 0009B, 0500P2 (mêmes masques `vesres.eval_ink.load_segment_masks`).
- **Mesures** : ECE 15 bins égaux pixel-pondérée, courbe de fiabilité (`results.json`), p moyen vs prévalence, ECE après
  recalibration isotone en validation croisée 2 plis (damier de blocs 256 px, même segment → borne optimiste).
- **Critère fixé avant** (EXP-010) : H-011 réfutée si ECE reader-v2 > 0,10 sur ≥ 2 objets.

## Résultats (ECE / p moyen ; prévalence entre parenthèses)
| Segment | prév. | reader-v2 | Hecate | fusion | ECE isotone CV rv2 / Hecate / fusion |
|---|---|---|---|---|---|
| 0841 w00 | 0,222 | 0,182 / 0,345 | 0,077 / 0,145 | 0,122 / 0,245 | 0,015 / 0,007 / 0,007 |
| 0841 …144552 | 0,324 | 0,117 / 0,401 | 0,164 / 0,163 | 0,080 / 0,282 | 0,024 / 0,035 / 0,030 |
| 0841 …174252 | 0,227 | 0,145 / 0,354 | 0,083 / 0,148 | 0,095 / 0,251 | 0,007 / 0,017 / 0,014 |
| 0009B | 0,223 | 0,181 / 0,351 | 0,087 / 0,136 | 0,113 / 0,244 | 0,011 / 0,015 / 0,006 |
| 0500P2 | 0,213 | 0,169 / 0,334 | 0,058 / 0,155 | 0,111 / 0,245 | 0,016 / 0,004 / 0,009 |

ECE reader-v2 par objet : 0841 0,148 · 0009B 0,181 · 0500P2 0,169.

## Conclusions
- **H-011 réfutée** (3/3 objets > 0,10) : reader-v2 **surestime** systématiquement (p moyen 0,33–0,40 pour 0,21–0,32
  d'encre) ; Hecate **sous-estime** (0,14–0,16). Les erreurs se compensent en partie dans la fusion (ECE 0,08–0,12),
  ce qui ne la rend pas calibrée.
- Le biais est **stable entre objets** (p moyen reader-v2 ≈ 0,34 ± 0,03) et monotone : une recalibration isotone ramène
  l'ECE à ≤ 0,035 partout → corrigible, mais à apprendre hors du segment évalué.
- Conséquences : (1) aucun seuil fixe 0,5 n'est interprétable comme probabilité pour ces modèles ; (2) la fusion par
  moyenne mélange deux échelles biaisées en sens opposé → H-014 : fusion après calibration croisée (apprise sur les autres
  objets) ou par rangs. AUC/AP d'un modèle seul sont invariantes à toute recalibration monotone ; celles de la fusion non.
