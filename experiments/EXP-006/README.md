# EXP-006 — H-004 : sensibilité de reader-v2 au décalage de la fenêtre de couches (PHerc0841)

- **Date** : 2026-11-22 · 3 segments PHerc0841 (w00, auto_grown_…144552, auto_grown_…174252), masques d'EXP-001.
- **Modèle** : reader-v2 `reader-v2-step040000.pth`, `koine_machines.inference.infer` (villa @ 47a9c37f, sans patch),
  fenêtre de 17 couches `--layer-start 6+s --layer-end 23+s`, s ∈ [−6, +5] (28 couches disponibles ; s=0 = défaut 6–22).
- **Code** : `run_sweep.sh` (36 inférences, toutes exit=0, ≈ 25 s mur chacune, RTX 5080), `analyze.py` → `results.json`.
- **Contrôle** : la prédiction s=0 est identique bit à bit à celle d'EXP-001/E1 sur les 3 segments.
- **Critère fixé avant l'expérience** : H-004 réfutée si l'AUC optimale par segment dépasse celle de s=0 de moins de 0,01.

## AUC supervision (protocole reader-v2) par décalage
| s | −6 | −5 | −4 | −3 | −2 | −1 | **0** | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w00 | 0,746 | 0,796 | 0,825 | 0,839 | 0,843 | 0,862 | 0,876 | 0,881 | 0,888 | **0,890** | 0,874 | 0,846 |
| …144552 | 0,749 | 0,781 | 0,800 | 0,811 | 0,815 | 0,818 | **0,826** | 0,825 | 0,812 | 0,804 | 0,798 | 0,778 |
| …174252 | 0,733 | 0,757 | 0,767 | 0,782 | 0,810 | 0,819 | **0,819** | 0,816 | 0,805 | 0,798 | 0,787 | 0,778 |
| moyenne | 0,743 | 0,778 | 0,797 | 0,811 | 0,822 | 0,833 | **0,840** | **0,840** | 0,835 | 0,831 | 0,820 | 0,801 |

- Optimum par segment : s=+3 pour w00 (gain +0,015 ; AP 0,742 → 0,763 ; IC95 AUC [0,779–0,901] → [0,803–0,921],
  recouvrants), s=0 pour les deux autres (gain 0).
- Moyenne de l'oracle par segment : 0,845 vs 0,840 (+0,005) — plafond d'un recentrage parfait, choisi sur les labels de test.
- Aucun décalage global unique ne bat le défaut (s=+1 ex æquo).
- Sensibilité réelle mais asymétrique : −0,09 à −0,13 AUC à s=−6, −0,03 à −0,05 à s=+5.

## Conclusion
**H-004 réfutée sur 0841** (2/3 segments au-dessous du seuil ; gain du 3e choisi par oracle, non significatif, plafond
moyen +0,005). La fenêtre par défaut de reader-v2 est déjà quasi optimale ; le décalage en profondeur n'explique pas
les échecs résiduels à 9 µm sur ce rouleau. Décision : **rejeter** le recentrage automatique par segment. Limite :
un seul rouleau, surfaces déjà bien centrées par la segmentation ; à revérifier seulement si un segment présente un
optimum décalé hors IC.
