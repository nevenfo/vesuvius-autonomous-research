# EXP-018 — E1.5 / H-017 : reader-v2-LO, recette reader-v2 ré-entraînée sans les objets de test

## Cadrage (2026-11-23)
- **Constat** : ink_9um (corpus 0139, 1667, Paris4, 0814 — `villa/ink-detection/configs/aligned21_hybrid_3d2d.json`)
  n'a vu **aucun** objet de test (0841, 0009B, 0500P2) : il est déjà « leave-out ». La parenté gênante est celle de
  reader-v2 (0009B : 14 segments + init `ft12k` affinée à 116 keV ; 0500P2 : 18 segments).
- **Recette reader-v2** (`github.com/DomRusso2/reader-v2`, `scripts/v2_run.py`, `train_config.json`) : labels natifs
  denses = **carte canon 2,4 µm publiée** ramenée sur la grille 9 µm (encre ≥ 128 ; supervisé si ≥ 128 ou ≤ 64) →
  reader-v2 est distillé du modèle canon.
- **Coût mesuré** : 0,174 s/itération (batch 64, 17×128×128, fp16, tenseurs synthétiques), 5,4 Gio VRAM → 40k itérations
  ≈ 1,9 h de GPU pur (+ chargement des données). Données : 38 segments d'entraînement (≈ 85 Go non compressés,
  `selection.json`), identiques segment pour segment aux jeux natifs v2 de reader-v2 (vérifié 38/38).
- **Écarts assumés** (`make_config.py`) : sans 0009B/0500P2, sans le corpus aligné 21 tranches de l'auteur (non publié
  tel quel), quotas proportionnels (22/13/9/20), init `scrollprize/ink_9um` s43 60k au lieu de `ft12k`.

## Hypothèse et critère (fixés avant l'entraînement)
H-017 : l'avantage de reader-v2 sur 0009B/0500P2 ne vient pas d'avoir vu ces objets : reader-v2-LO perd < 0,03 d'AUC
sup. par rapport à reader-v2 en moyenne sur 0009B et 0500P2, et sa perte n'y dépasse pas de plus de 0,02 sa perte
sur 0841 (DiD, comme EXP-008). Réfutée sinon. Secondaire : fusion(reader-v2-LO, Hecate) sur 3 objets.

## Fichiers
`select_segments.py` → `selection.json` ; `build.py` (SV + carte canon + labels denses) ; `make_config.py` → `train_config.json`.

## Exécution
Entraînement 40k (`run_train.py`, `train_config.json`) : 0 → 13 212 it. le 2026-11-26 (processus tué), reprise
depuis `ckpt_013000` le 2026-11-27 (tâche planifiée Windows), fin à 15:27 (rc 0, perte finale ≈ 0,555). Débit
1,6–2,4 it/s, limité par le chargement des données (GPU peu occupé) ; un job CPU concurrent (WSL, 6 workers) le
divise par ~5. Inférence `run_eval.sh ckpt_040000.pth lo` (options d'EXP-001), 5/5 exit 0 ; `analyze.py` → `results.json`.

## Résultats (région supervision ; AUC [IC95 blocs], AP)
| Segment | reader-v2 | reader-v2-LO | perte AUC | IC95 Δ AP (LO − rv2) | fusion LO+Hecate | gain AP fusion LO vs meilleur seul |
|---|---|---|---|---|---|---|
| 0841 w00 | 0,876 / 0,742 | 0,854 [0,757-0,874] / 0,678 | 0,022 | [−0,137 ; −0,043] | 0,918 / 0,806 | +0,006 |
| 0841 144552 | 0,826 / 0,690 | 0,767 [0,689-0,850] / 0,650 | 0,059 | [−0,087 ; 0,044] | 0,792 / 0,693 | +0,017 |
| 0841 174252 | 0,819 / 0,657 | 0,820 [0,713-0,852] / 0,654 | −0,001 | [−0,039 ; 0,048] | 0,887 / 0,753 | +0,008 |
| 0009B (vu par rv2) | 0,927 / 0,826 | 0,911 [0,867-0,940] / 0,805 | 0,016 | [−0,041 ; 0,034] | 0,927 / 0,836 | +0,032 |
| 0500P2 (vu par rv2) | 0,873 / 0,721 | 0,873 [0,834-0,910] / 0,715 | 0,000 | [−0,047 ; 0,032] | 0,924 / 0,805 | +0,024 |

Perte moyenne sur les objets vus par reader-v2 : **0,008** (< 0,03) ; sur 0841 (vu par aucun) : 0,027 ;
DiD = **−0,019** (≤ 0,02) → **H-017 soutenue** : l'avantage de reader-v2 sur 0009B/0500P2 ne s'explique pas par
le fait d'avoir vu ces objets. La perte de LO est au contraire plus forte sur 0841, ce qui pointe vers des écarts de
recette (init ink_9um, absence du corpus aligné, quotas) plutôt que vers une fuite par objet.
Secondaire : la fusion LO+Hecate reste au-dessus du meilleur seul en AP sur 5/5 segments, mais sous la fusion
reader-v2+Hecate sur 0841 (−0,007 à −0,032 d'AUC) ; elle l'égale sur 0009B/0500P2.

## Conséquences
- reader-v2 publié peut rester dans la chaîne de référence pour 0009B/0500P2 sans biais de fuite mesurable ;
  reader-v2-LO (`runs/EXP-018/train/ckpt_040000.pth`) est la variante propre pour toute évaluation exigeant un
  modèle n'ayant vu aucun objet de test (≥ 3 rouleaux indépendants, J5).
- Référence R de la phase K (durée d'entraînement) : cet entraînement 40k.
