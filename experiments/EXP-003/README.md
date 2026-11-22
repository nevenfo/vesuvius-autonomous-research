# EXP-003 — Hecate 9,6 µm sur PHerc0841 (E1.4) et fusion reader-v2 + Hecate (H-003)

- **Date** : 2026-11-22 · 3 segments PHerc0841 (w00, auto_grown_…144552, auto_grown_…174252), mêmes masques qu'EXP-001.
- **Modèle** : `scrollprize/hecate` `hecate_9.6um.pth` (MIT), `hecate.py` officiel, bf16, batch 8, profondeur centrale 16.
- **Code** : `hecate_run.py` (rééchantillonnage 9,366→9,6 µm XY `INTER_AREA` + Z linéaire, inférence, retour grille native
  `INTER_LINEAR` ; méthode de reader-v2 `scripts/infer_with_hecate.py`), `analyze.py` → `results.json`.
- **Coût** : ≈ 2 min 45 s mur par segment (rééchantillonnage + inférence + retour), RTX 5080 ; pic GPU total observé 7,4 Go
  (autres applications incluses).
- **Prédictions** (hors Git, `vesuvius-work/runs/E1.4/<seg>/pred_hecate.tif`) sha256 : w00 `9ad74217…`, …144552 `b37b912d…`,
  …174252 `18691e63…`.

## Reproduction Hecate (AUC protocole reader-v2)
| Segment | revue (publié → obtenu) | supervision (publié → obtenu) |
|---|---|---|
| w00 | 0,8887 → 0,8888 | 0,9119 → 0,9120 |
| auto_grown_…144552 | 0,8013 → 0,8013 | 0,7841 → 0,7841 |
| auto_grown_…174252 | 0,8752 → 0,8753 | 0,8936 → 0,8938 |

**Reproduite** (6/6, écart max 2e-4). Hecate > reader-v2 sur 2/3 segments ; corrélation de Pearson reader-v2/Hecate 0,66–0,69.

## H-003 — fusion reader-v2 + Hecate (région supervision, métrique primaire)
| Segment | reader-v2 AUC / AP | Hecate AUC / AP | fusion moyenne AUC / AP [IC95 AUC] | fusion rangs AUC / AP |
|---|---|---|---|---|
| w00 | 0,876 / 0,742 | 0,912 / 0,800 | **0,926 / 0,824** [0,880–0,946] | 0,917 / 0,807 |
| …144552 | 0,826 / 0,690 | 0,784 / 0,676 | 0,824 / 0,720 [0,748–0,870] | 0,826 / **0,729** |
| …174252 | 0,819 / 0,657 | **0,894** / 0,745 | 0,887 / **0,751** [0,831–0,923] | 0,881 / 0,738 |
| **moyenne** | 0,840 / 0,696 | 0,863 / 0,740 | **0,879 / 0,765** | 0,875 / 0,758 |

- Gain AP moyen de la fusion moyenne sur le meilleur modèle seul (Hecate) : **+0,025** (seuil d'échec H-003 : < 0,02) ;
  par segment vs meilleur seul : +0,024, +0,030, +0,007 → 2/3 au-dessus du seuil. Pire cas AUC sup. : 0,824 vs 0,784 (Hecate).
- Région « revue » (labels incomplets, H-008) : AUC fusion 0,866 vs Hecate 0,855 en moyenne, mais AP en baisse sur 2/3.
- IC par blocs largement recouvrants : aucun écart individuel n'est significatif.

**Conclusion : H-003 soutenue pour la paire reader-v2+Hecate, non confirmée.** Gain d'AP au seuil sur la moyenne et
robustesse accrue (pas de choix de modèle a posteriori), mais parenté Hecate↔0841 non vérifiable (« weak 3D supervision
on other scrolls », liste non publiée — `docs/data/splits.md`), un seul rouleau, 3 segments corrélés, FP sur papyrus vierge
et calibration (ECE) non mesurés. Décision : **suspendre l'intégration** jusqu'à un 2e objet indépendant ; aucun n'existe pour cette paire parmi les labels publiés → passe par E1.5
(leave-one-scroll-out) ou de nouveaux labels.
