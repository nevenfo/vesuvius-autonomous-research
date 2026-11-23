# EXP-016 — H-015 : TTA reader-v2 répliquée sur 0009B/0500P2 et cumulée à la fusion Hecate

- **Date** : 2026-11-23 · reader-v2 `--tta-mirror` (options d'EXP-015, `run_tta.sh`) sur 0009B (8,64 µm, 55 s) et 0500P2
  (28 s) ; prédictions hors Git `vesuvius-work/runs/EXP-016/<seg>/pred_reader-v2_tta.tif`, sha256 0009B `ec769e97…`,
  0500P2 `6b869620…`. 0841 : TTA d'EXP-015 ; Hecate et passe unique comme EXP-012.
- **Critère fixé avant** : H-015 réfutée si gain AP moyen (fusion(rv2-TTA, Hecate) − fusion(rv2, Hecate), 3 objets) < 0,01.

## Résultats (région supervision ; AUC / AP)
| Segment | rv2 | rv2-TTA | Hecate | fusion | fusion-TTA | gain AP TTA seul [IC95] | gain AP TTA fusion [IC95] |
|---|---|---|---|---|---|---|---|
| 0841 w00 | 0,876 / 0,742 | 0,894 / 0,765 | 0,912 / 0,800 | 0,926 / 0,824 | 0,927 / 0,826 | +0,023 [0,010 ; 0,051] | +0,002 [−0,002 ; 0,010] |
| 0841 …144552 | 0,826 / 0,690 | 0,837 / 0,737 | 0,784 / 0,676 | 0,824 / 0,720 | 0,828 / 0,731 | +0,047 [0,011 ; 0,105] | +0,011 [−0,002 ; 0,034] |
| 0841 …174252 | 0,819 / 0,657 | 0,829 / 0,673 | 0,894 / 0,745 | 0,887 / 0,752 | 0,889 / 0,755 | +0,016 [0,001 ; 0,043] | +0,003 [0,000 ; 0,014] |
| 0009B | 0,927 / 0,826 | 0,928 / 0,826 | 0,884 / 0,780 | 0,935 / 0,845 | 0,934 / 0,844 | +0,001 [−0,007 ; 0,009] | −0,001 [−0,006 ; 0,001] |
| 0500P2 | 0,873 / 0,721 | 0,876 / 0,722 | 0,910 / 0,781 | 0,923 / 0,804 | 0,922 / 0,803 | +0,001 [−0,010 ; 0,035] | −0,002 [−0,005 ; 0,009] |

Gain AP moyen par objet — TTA seul : 0841 +0,029 · 0009B +0,001 · 0500P2 +0,001 ; TTA dans la fusion : +0,005 · −0,001 ·
−0,002 (moyenne **+0,0008**). Fusion-TTA − meilleur modèle seul : +0,010 · +0,017 · +0,022.

## Conclusions
- **H-015 réfutée** : la TTA ne se cumule pas à la fusion (+0,001 AP en moyenne) ; Hecate apporte déjà la
  diversité que la TTA donne à reader-v2.
- **La TTA ne se réplique pas sur les objets vus** (0009B, 0500P2 : +0,001). Son gain se limite à 0841, seul objet non vu
  par reader-v2 → hypothèse compatible : la TTA compense un décalage de domaine, inutile en distribution. Non séparable
  ici d'un effet propre à 0841 (un seul objet non vu) ; H-012 reste soutenue sur 0841 seulement.
- Chaîne recommandée inchangée : fusion moyenne reader-v2+Hecate (passe unique) ; TTA reader-v2 seulement si Hecate est
  indisponible, sur un objet non vu.
