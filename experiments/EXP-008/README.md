# EXP-008 — H-002 : avantage « objet vu » de reader-v2 sur ink_9um (différence de différences)

- **Date** : 2026-11-22 · nouveau segment : PHerc0500P2 `20250825181859--1` (seul segment 0500P2 portant des
  `ink-labels`), surface-volume `9.362um-1.2m-113keV-volume-20250820143440.zarr/0` (28, 5880, 3300), labels
  `ink-labels/2.215um-volume-20250526151718/20260918` (24760×13880 → grille 9,362 µm, `vesres.fetch_segment`, 39 s).
- **Parenté** : reader-v2 = objet vu (17 segments `z_dbg_gen_*` de 0500P2 dans `train_config.json`), **segment tenu à
  l'écart** (absent du fichier, vérifié le 2026-11-22) ; ink_9um = objet non vu. Même situation que 0009B (EXP-004).
  Les segments d'entraînement peuvent recouvrir physiquement la même surface du fragment : non vérifié.
- **Inférence** : comme EXP-001 (`koine_machines.inference.infer --overlap 0.5 --blend-mode hann --batch-size 8
  --no-compile --direction forward`, couches 6–22) ; reader-v2 32 s, ink_9um 24 s ; prédictions hors Git
  `vesuvius-work/runs/EXP-008/`, sha256 reader-v2 `6bdf1bc1…`, ink_9um `ac849966…`.
- **Code** : `analyze.py` → `results.json`. **Critère fixé avant** : H-002 réfutée si DiD < 0,03 AUC.

## Résultats (région supervision, AUC protocole reader-v2 [IC95 blocs] / AP)
| Segment | groupe | reader-v2 | ink_9um s43 | Δ AUC | Δ AP |
|---|---|---|---|---|---|
| 0500P2 `…181859--1` | vu par reader-v2 | 0,873 [0,833–0,907] / 0,721 | 0,767 [0,740–0,809] / 0,521 | 0,106 | 0,200 |
| 0009B (EXP-004) | vu par reader-v2 | 0,927 [0,887–0,948] / 0,826 | 0,813 [0,774–0,843] / 0,610 | 0,114 | 0,216 |
| 0841 w00 | non vu | 0,876 / 0,742 | 0,740 / 0,483 | 0,136 | 0,258 |
| 0841 …144552 | non vu | 0,826 / 0,690 | 0,701 / 0,539 | 0,126 | 0,151 |
| 0841 …174252 | non vu | 0,819 / 0,657 | 0,747 / 0,537 | 0,072 | 0,120 |

- **DiD AUC = −0,001** (vus 0,110 vs 0841 0,111) ; 0500P2 seul : −0,005 ; pire cas (min vus − max non vus) : −0,029.
- 0500P2 : prévalence d'encre 21 % en supervision ; région `validation` non incluse dans `supervision`.
- reader-v2 atteint 0,873 sur 0500P2, dans l'intervalle de 0841 (0,82–0,88) : aucune prime visible à l'objet vu.

## Conclusion
**H-002 réfutée au niveau « objet vu, segment tenu à l'écart » pour reader-v2** : l'écart reader-v2 − ink_9um est le
même sur les objets vus par reader-v2 et sur l'objet vu par aucun. Pas de prime mesurable à la familiarité de l'objet
à cette résolution. Limites : 2 segments vus contre 3 non vus, Δ variable entre segments 0841 (0,07–0,14), donc la
résolution du test est d'environ ±0,03 ; ne teste pas l'évaluation sur un segment d'entraînement lui-même, ni la
circularité de labels produits par la même famille de modèles (origine des pseudo-labels 20260918 : B1.2). Décision :
les segments tenus à l'écart d'objets vus (0009B, 0500P2) sont **utilisables comme objets de test supplémentaires pour
reader-v2 à titre indicatif**, sans valoir une évaluation inter-rouleaux.
