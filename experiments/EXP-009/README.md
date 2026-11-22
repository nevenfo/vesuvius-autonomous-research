# EXP-009 — H-007 : la qualité géométrique de la surface prédit-elle les erreurs locales de reader-v2 ? (PHerc0841)

- **Date** : 2026-11-22 · 3 segments PHerc0841, région `supervision` ; aucune inférence nouvelle.
- **Surface** : tifxyz officiels `*-on-20250821151531-9.366um.tifxyz` (même volume que le surface-volume ; scale 0,05 →
  1 sommet / 20 px ; forme × 20 = forme des prédictions, vérifié), copiés hors Git dans
  `vesuvius-work/cache/segments/PHerc0841/<seg>/tifxyz_9.366/`.
- **Métriques sans label** (par sommet, moyenne et max par tuile) : `stretch` (écart log à l'isométrie en u et v),
  `shear` (écart à 90° entre ∂P/∂u et ∂P/∂v), `normal_var` (angle moyen aux normales voisines : courbure/plis).
- **Erreur, tuilage, contrôles** : identiques à EXP-007 (Brier de reader-v2, tuiles 64 px, ρ partiel sur rangs avec
  proba moyenne, prévalence, E[p(1−p)]). Code : `analyze.py` (réutilise `partial_rho`/`prob` d'EXP-007) → `results.json`.
- **Critère fixé avant** : H-007 réfutée si |ρ partiel| < 0,3 pour toutes les métriques.

## Résultats (938 tuiles poolées ; plage par segment)
| Métrique | médiane | ρ brut vs Brier | partiel (p̄, prévalence) | + E[p(1−p)] |
|---|---|---|---|---|
| stretch | 0,023 | −0,02 [−0,06–0,08] | −0,01 [−0,09–0,05] | −0,01 [−0,02 – −0,01] |
| shear (°) | 0,76 | −0,09 [−0,13–0,01] | −0,08 [−0,18–0,01] | −0,10 [−0,17–0,03] |
| normal_var (°) | 5,3 | −0,07 [−0,07–0,11] | 0,07 [0,03–0,18] | 0,01 [−0,01–0,06] |
| max par tuile (3 métriques) | — | ≤ 0,09 en valeur absolue | ≤ 0,15 | ≤ 0,16 |

## Conclusion
**H-007 réfutée sur 0841** : aucune métrique géométrique locale n'atteint |ρ| = 0,2 avec l'erreur de reader-v2, sur
aucun segment ni en poolé. Lecture : sur ces segments étiquetés, la surface est quasi isométrique (étirement médian
≈ 2 %, cisaillement < 1°) ; la variabilité géométrique restante n'explique pas où l'encre échoue. Limites : plage
restreinte (segments choisis pour l'étiquetage, donc de bonne qualité), grille de 20 px ≈ 190 µm qui ne voit pas les
défauts plus fins, et ces métriques intrinsèques ne détectent pas les sauts de feuillet (erreur de segmentation la
plus grave), qui demanderaient le volume. Décision : **rejeter** ces métriques comme prédicteurs d'échec d'encre sur
des segments de qualité étiquetage ; non testé sur des segments automatiques bruts.
