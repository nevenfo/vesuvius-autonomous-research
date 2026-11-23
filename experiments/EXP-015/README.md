# EXP-015 — H-012 : TTA miroir de reader-v2 sur PHerc0841 × 3

- **Date** : 2026-11-23 · option officielle `--tta-mirror` de `koine_machines.inference.infer` (villa @ 47a9c37f, sans
  patch) : 4 variantes (miroirs des axes de patch 1, 2), moyenne des probabilités. Autres options identiques à EXP-001
  (`--overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward`), `--tta-batch-size 2`.
  Lanceur `run_tta.sh`.
- **Temps mur** (chargement inclus) : 38 / 32 / 30 s, contre 42 s pour la passe unique d'EXP-001 sur w00 → surcoût non
  mesurable à cette échelle (chaîne dominée par les E/S et la préparation).
- **Prédictions** hors Git `vesuvius-work/runs/EXP-015/<seg>/pred_reader-v2_tta.tif`, sha256 w00 `a0ec8140…`,
  …144552 `a115f56e…`, …174252 `d4cdc2d5…`.
- **Critère fixé avant** (EXP-010) : H-012 réfutée si gain AUC sup. moyen < 0,01.

## Résultats (région supervision)
| Segment | AUC passe unique → TTA | AP passe unique → TTA | gain AP [IC95 apparié blocs] | Pearson |
|---|---|---|---|---|
| w00 | 0,876 → **0,894** | 0,742 → 0,765 | +0,023 [0,010 ; 0,051] | 0,969 |
| …144552 | 0,826 → **0,837** | 0,690 → 0,737 | +0,047 [0,008 ; 0,109] | 0,973 |
| …174252 | 0,819 → **0,829** | 0,657 → 0,673 | +0,016 [0,001 ; 0,047] | 0,971 |

Gain moyen : **AUC +0,013**, **AP +0,029**.

## Conclusions
- **H-012 soutenue** : le gain est positif sur les 3 segments (IC apparié de l'AP > 0 partout) pour un coût négligeable.
  C'est le premier levier qui améliore reader-v2 lui-même sur l'objet tenu à l'écart.
- La TTA ne figure pas dans le protocole auto-déclaré de reader-v2 (AUC 0,824) : notre baseline reste la passe unique ;
  la TTA est une amélioration de la chaîne, à rapporter séparément.
- Suite : répliquer sur 0009B/0500P2 et combiner avec la fusion Hecate (H-015).
