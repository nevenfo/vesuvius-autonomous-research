# EXP-013 — H-014 : fusion reader-v2+Hecate calibrée (isotone LOO objet) ou par rangs

- **Date** : 2026-11-23 · aucune inférence ; prédictions et masques d'EXP-012 (0841 × 3, 0009B, 0500P2).
- **Variantes** : `raw` = moyenne brute (EXP-011) ; `iso` = moyenne après calibration isotone de chaque modèle apprise
  sur les pixels supervision des **autres objets** (1 M px/segment, l'objet testé n'entre jamais dans l'ajustement) ;
  `rank` = moyenne des rangs normalisés par segment (sans label).
- **Code** : `analyze.py` → `results.json`. **Critère fixé avant** : H-014 réfutée si le gain AP moyen (meilleure variante
  − raw, moyenne des 3 objets) < 0,01. IC95 appariés par bootstrap de blocs 256 px.

## Résultats (région supervision ; AUC / AP / ECE)
| Segment | raw | iso (LOO) | rank | gain AP iso [IC95] | gain AP rank [IC95] |
|---|---|---|---|---|---|
| 0841 w00 | 0,926 / 0,824 / 0,122 | 0,925 / 0,822 / 0,058 | 0,917 / 0,807 / 0,303 | −0,002 [−0,016 ; 0,005] | −0,017 [−0,045 ; −0,004] |
| 0841 …144552 | 0,824 / 0,720 / 0,080 | 0,827 / 0,727 / 0,031 | 0,826 / 0,729 / 0,288 | +0,007 [−0,001 ; 0,014] | +0,009 [−0,005 ; 0,027] |
| 0841 …174252 | 0,887 / 0,752 / 0,095 | 0,885 / 0,747 / 0,033 | 0,882 / 0,738 / 0,319 | −0,005 [−0,025 ; 0,001] | −0,014 [−0,057 ; 0,000] |
| 0009B | 0,935 / 0,845 / 0,113 | 0,935 / 0,847 / 0,039 | 0,930 / 0,839 / 0,285 | +0,002 [−0,007 ; 0,009] | −0,006 [−0,021 ; 0,003] |
| 0500P2 | 0,923 / 0,804 / 0,111 | 0,923 / 0,801 / 0,055 | 0,918 / 0,792 / 0,336 | −0,003 [−0,020 ; 0,002] | −0,013 [−0,037 ; 0,001] |

Gain AP moyen par objet (0841 moyenné) : iso −0,0006 · rank −0,0086. ECE des modèles seuls calibrés LOO :
reader-v2 0,022–0,050, Hecate 0,015–0,077 (contre 0,12–0,18 et 0,06–0,16 bruts, EXP-012).

## Conclusions
- **H-014 réfutée** : calibrer avant de moyenner ne change pas l'AP (|gain| ≤ 0,007, IC contenant 0) ; la fusion par rangs
  est légèrement pire (−0,009). Les biais opposés de reader-v2 et Hecate ne nuisent donc pas au classement de la fusion
  brute.
- **Résultat utile** : la calibration isotone **se transfère entre objets** (apprise sans l'objet testé) : ECE de la
  fusion 0,03–0,06 au lieu de 0,08–0,12, à AP égale. Décision : pour toute carte exprimée en probabilité, utiliser la
  fusion `iso` ; pour le classement/AP, `raw` suffit.
- Limite : 5 segments / 3 objets ; la calibration dépend de la prévalence (0,21–0,32 ici) et de la définition des labels.
