# EXP-005 — H-008b : l'accord inter-modèles discrimine-t-il des labels incomplets ? (PHerc0841)

- **Date** : 2026-11-22 · entrées : prédictions reader-v2, ink_9um s43 (EXP-001/E1) et Hecate (EXP-003), 3 segments 0841.
- **Code** : `analyze.py` → `results.json` ; < 3 min CPU, aucune inférence.
- **Statistique** (celle d'EXP-002) : parmi les pixels non étiquetés du top 5 % du modèle A, part également dans le top 5 %
  du modèle B ; `lift` = cette part / part de B dans le top 5 % sur tout le non-étiqueté de la région.
- **Contrôle ajouté** : régions `*_far` = pixels à > 8 px (≈ 75 µm) de toute encre étiquetée, pour écarter un effet de bord
  des labels.

## Résultats (lift reader-v2 → Hecate / reader-v2 → ink_9um)
| Segment | supervision | supervision loin de l'encre | validation \ supervision |
|---|---|---|---|
| w00 | 22,1 / 2,1 | 36,9 / 0,2 | 12,5 / 8,0 |
| auto_grown_…144552 | 9,0 / 6,7 | 10,9 / 7,4 | 13,2 / 9,4 |
| auto_grown_…174252 | 12,8 / 7,7 | 13,1 / 8,3 | 12,0 / 9,2 |

Accord triple (top 5 % des 3 modèles) sur le non-étiqueté : 1,2–1,4 % en validation vs 0,004–0,56 % en supervision loin
de l'encre (attendu sous indépendance : 0,0125 %).

## Conclusion
- Critère pré-déclaré (lift ≥ 5× en validation avec Hecate) **atteint** : 12–13×.
- Mais le contrôle montre qu'il **ne discrimine pas** : l'accord est du même ordre en supervision loin de toute encre
  étiquetée (lift 11–37× avec Hecate), zone réputée complètement annotée ; l'effet de bord n'explique rien (les régions
  `_far` gardent les mêmes lifts).
- Deux lectures restent ouvertes : (a) labels incomplets y compris en supervision ; (b) biais partagé — Hecate « préserve
  l'architecture et les poids pré-entraînés du modèle canonique » (model card) et reader-v2/ink_9um partagent la famille
  hybride 3D→2D : ce ne sont pas des juges indépendants. Seul l'accord triple, plus élevé en validation, penche vers (a).
- **H-008 : rétrogradée de « soutenue » à « suspendue »** — l'accord inter-modèles n'est pas une preuve d'encre non
  étiquetée. Trancher exige un juge indépendant des modèles (fragment à label IR, inspection experte de crops) ; aucun
  signalement à l'équipe sur cette base.
- Conséquence inchangée : métrique primaire = région `supervision`.
