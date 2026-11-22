# EXP-010 — B3.2 : audit du protocole tuiles / Brier / ρ partiel (EXP-007, EXP-009)

- **Date** : 2026-11-22 · déclencheur : règle d'arrêt F1.1, 4 hypothèses réfutées d'affilée (H-004, H-006, H-002, H-007).
- **Code** : `audit.py` → `results.json` (réutilise `partial_rho`/`prob` d'EXP-007 et `geometry` d'EXP-009 ; tuilage
  vectorisé, mêmes règles : 64 px, supervision ≥ 50 % ; graine 0).
- H-004 (balayage direct d'AUC, contrôle s=0 bit à bit) et H-002 (DiD sur AUC publiées reproduites) ne passent pas par
  cette chaîne ; leur protocole est déjà contrôlé par la reproduction d'EXP-001.

## 1. Contrôle positif
Indicateur synthétique = résidu de rang du Brier (contrôles p̄, prévalence, E[p(1−p)]) + k·bruit ; 50 tirages.
| k | ρ attendu | w00 | …144552 | …174252 |
|---|---|---|---|---|
| 0 | 1,000 | 0,935 | 0,909 | 0,900 |
| 0,5 | 0,894 | 0,808 | 0,797 | 0,781 |
| 1 | 0,707 | 0,644 | 0,645 | 0,637 |
| 2 | 0,447 | 0,420 | 0,419 | 0,428 |
| 3 | 0,316 | 0,307 | 0,317 | 0,313 |

La chaîne retrouve ρ à ±0,03 dans la zone de décision (ρ ≤ 0,45, seuil 0,3) ; au-delà elle sous-estime de 0,06 à
0,11 (re-classement en rangs puis double résidualisation) — biais conservateur, sans effet sur les verdicts à 0,3.

## 2. Seuil nul (puissance)
Cartes d'indicateurs décalées toroïdalement (≥ 8 tuiles) avant tuilage, 200 décalages : quantile 95 % de |ρ partiel|.
| Indicateur | w00 (389 tuiles) | …144552 (239) | …174252 (310) | observé (w00 / 144552 / 174252) |
|---|---|---|---|---|
| entropie | 0,13 | 0,17 | 0,14 | 0,02 / −0,14 / −0,09 |
| désaccord Hecate | 0,12 | 0,21 | 0,13 | 0,08 / **0,25** / 0,08 |
| variation des normales | 0,13 | 0,26 | 0,20 | −0,01 / 0,06 / 0,05 |

- ρ minimal détectable à α = 5 % : 0,12–0,26 selon segment et indicateur → le critère |ρ| < 0,3 était testable.
- 1 dépassement sur 9 (désaccord Hecate, …144552 : 0,25 > 0,21), compatible avec le hasard (0,45 attendu sur 9) ;
  non répliqué sur les deux autres segments.

## Conclusion de l'audit
Protocole sain : la chaîne détecte un effet connu, sans biais dans la zone de décision, et a la puissance pour un effet
de 0,3. Les réfutations H-006/H-007 traduisent une absence réelle d'effet ≥ 0,3 sur 0841 ; des effets faibles
(0,1–0,25) ne sont pas exclus. Les 4 réfutations sont des résultats, pas un défaut de métrique : la boucle continue
avec de nouvelles hypothèses (`docs/hypotheses.md`, H-010…H-013).
