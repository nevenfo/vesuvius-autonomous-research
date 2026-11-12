# EXP-002 — Fusion simple (H-003) et fiabilité de la région `validation` des labels (H-008), PHerc0841

- **Date** : 2026-11-12 · entrées : les 6 prédictions d'EXP-001 (reader-v2, ink_9um s43 × 3 segments), mêmes masques.
- **Code** : `analyze.py` (ce dossier) ; résultats bruts `results.json`. Coût : < 2 min CPU, aucune inférence.

## H-003 — moyenne reader-v2 + ink_9um
| Segment | reader-v2 seul (revue / sup.) | Fusion (revue / sup.) |
|---|---|---|
| w00 | 0,832 / 0,876 | 0,825 / 0,838 |
| auto_grown_…144552 | 0,839 / 0,826 | 0,807 / 0,793 |
| auto_grown_…174252 | 0,801 / 0,819 | 0,786 / 0,804 |

**Rejetée pour cette paire** : la fusion dégrade reader-v2 sur 3/3 segments (AUC et AP). Une moyenne naïve avec un
modèle nettement plus faible n'aide pas ; reste à tester avec un partenaire de niveau comparable (Hecate, publié 0,866 par
reader-v2, auto-déclaré) — hypothèse maintenue sous cette forme.

## H-008 — la région `validation \ supervision` est-elle étiquetée de façon complète ?
Dans cette région la prévalence d'encre étiquetée est ≈ 0 (0,4 %, 0,0 %, 0,03 %). Parmi les pixels non étiquetés
du top 5 % reader-v2, part également dans le top 5 % ink_9um (modèle indépendant, jamais entraîné sur 0841) :

| Segment | validation : accord | taux de base | supervision : accord sur non-étiqueté | accord sur encre étiquetée |
|---|---|---|---|---|
| w00 | 0,388 | 0,049 | 0,075 | 0,208 (sup.) |
| auto_grown_…144552 | 0,445 | 0,048 | 0,300 | 0,194 (sup.) |
| auto_grown_…174252 | 0,431 | 0,047 | 0,301 | 0,281 (sup.) |

**Soutenue, non confirmée** : les détections non étiquetées de la zone validation sont reproduites par un second modèle
8–9× plus souvent que par hasard, et plus souvent que l'encre effectivement étiquetée. Interprétation la plus probable :
encre non annotée (labels incomplets hors supervision) → l'AUC « revue » (sup ∪ val, appelée « vs human labels » par
reader-v2) compte probablement de l'encre comme négatif et sous-estime les modèles ; l'AP en souffre fortement (0,14–0,18).
Explication concurrente non exclue : biais partagé des deux modèles (même architecture hybride 3D→2D, même pipeline
`koine`) sur des structures non-encre.

## Conséquences
- Pour comparer des modèles sur ces labels : métrique primaire = région `supervision` ; la région revue est rapportée
  à titre secondaire avec cet avertissement.
- Test discriminant suivant (H-008b) : inspection visuelle locale (non publiée) de crops validation à fort accord, et
  accord avec un modèle d'architecture différente (ex. Hecate ou TimeSformer 2023) ; si l'accord persiste → signaler
  l'incomplétude des labels à l'équipe (via Discord, après confirmation humaine).
