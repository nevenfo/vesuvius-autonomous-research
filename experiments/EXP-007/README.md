# EXP-007 — H-006 : un indicateur sans label prédit-il les erreurs locales de reader-v2 ? (PHerc0841)

- **Date** : 2026-11-22 · 3 segments PHerc0841, région `supervision`, masques d'EXP-001 ; aucune inférence nouvelle
  (prédictions reader-v2 d'EXP-001/E1, Hecate d'EXP-003, décalages s ∈ {−1, 0, +1} d'EXP-006).
- **Code** : `analyze.py` → `results.json` (< 2 min CPU).
- **Unité** : tuiles 64×64 px (≈ 0,6 mm) couvertes à ≥ 50 % par la supervision (938 tuiles ; 448 avec ≥ 2 % d'encre).
- **Erreur** : Brier de reader-v2 vs labels ; et taux d'encre manquée (pixels d'encre étiquetée à proba < 0,5).
- **Indicateurs sans label** : désaccord |reader-v2 − Hecate|, entropie de reader-v2, écart-type de reader-v2 sous
  décalage de la fenêtre de ±1 couche.
- **Critère fixé avant** : H-006 réfutée si |ρ| < 0,3 pour tous les indicateurs. **Contrôles ajoutés après le premier
  passage** (à déclarer) : ρ partiel sur rangs contrôlant la proba moyenne et la prévalence, puis le Brier attendu
  sous calibration E[p(1−p)], car l'entropie et le Brier sont liés par construction.

## Résultats (Spearman ρ, tuiles poolées ; plage par segment entre crochets)
| Indicateur | ρ brut vs Brier | partiel (p̄, prévalence) | + E[p(1−p)] | ρ vs encre manquée | partiel (p̄) |
|---|---|---|---|---|---|
| désaccord Hecate | 0,14 [0,07–0,32] | 0,34 [0,29–0,41] | 0,13 [0,08–0,25] | 0,15 [0,11–0,22] | 0,17 [0,17–0,18] |
| entropie reader-v2 | **0,74** [0,63–0,80] | 0,64 [0,53–0,68] | −0,06 [−0,14–0,02] | −0,05 [−0,16–0,09] | 0,38 [0,37–0,41] |
| instabilité ±1 couche | 0,69 [0,52–0,77] | 0,39 [0,34–0,46] | 0,11 [0,04–0,20] | −0,18 [−0,26 – −0,13] | 0,21 [0,14–0,32] |

Prévalence d'encre étiquetée ↔ Brier : ρ 0,72.

## Conclusion
**H-006 réfutée dans sa forme informative sur 0841.** Les indicateurs dépassent 0,3 en brut, mais uniquement par
la confiance propre du modèle : une fois le Brier attendu sous calibration contrôlé, aucun ne dépasse |ρ| = 0,25 (max atteint) sur
aucun segment. Le seul indicateur externe (désaccord avec Hecate) reste < 0,3 en brut poolé et sur l'encre manquée.
La corrélation entropie ↔ encre manquée à p̄ fixé (0,38) est en partie mécanique (pixels d'encre juste sous 0,5).
Lecture utile : l'entropie de reader-v2 classe correctement les tuiles par erreur attendue (ρ 0,74), cohérent avec
une calibration correcte — ECE non mesurée. Décision : **rejeter** ces indicateurs comme détecteurs de zones « non
récupérées » ; aucun ne distingue l'encre manquée du papyrus vierge mieux que la confiance du modèle elle-même.
Limites : un rouleau, 3 segments corrélés, tuiles non indépendantes (pas d'IC par blocs), contrôles choisis a posteriori.
