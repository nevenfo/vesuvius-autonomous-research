# EXP-029 — R1.2 : chaîne d'encre figée sur le patch propre de PHerc1218 (EXP-025 `out4`)

**Statut : terminé** — rendu valide = `--flip-normals` (EXP-030) : H-034 soutenue (ρ 0,372 vs nul 0,068) ; 3 zones au critère (0,96 mm²), taches rondes sans trait → **aucune lettre candidate**. Préenregistré le 2026-11-27 avant tout rendu ou inférence.

## Question
La chaîne d'encre figée n'ayant vu aucune région de PHerc1218 produit-elle, sur le premier patch propre obtenu sans
intervention (4,11 cm², EXP-025), des zones candidates d'encre distinguables des faux positifs (fond, fibres, bords) ?

## Entrées (aucune modifiée)
- Patch : `vesuvius-work/runs/EXP-025/out4` (tifxyz, uuid `f3cc00bb…`, VC3D `a7d4f88`).
- Volume : PHerc1218 `20250521120456-8.640um-1.2m-116keV-masked.zarr` (S3 public, niveau 0, lecture distante).
- Rendu : `vc_render_tifxyz --scale 1 -g 0 -n 31 --tif-output` → `experiments/EXP-025/tifs_to_sv.py` → `sv.zarr`.
- Modèles figés : reader-v2-LO (`runs/EXP-018/train/ckpt_040000.pth`, notre ré-entraînement) et ink_9um s43 ; inférence
  `koine_machines.inference.infer` (villa @ 47a9c37f, sans patch) `--overlap 0.5 --blend-mode hann --batch-size 8
  --no-compile --direction forward` ; recadrage central des couches par l'outil. Parentés : aucun n'a vu 1218
  (`docs/data/provenance.csv`).

## Mesures (classe de référence R0 : aucun label sur 1218)
1. Contrôle d'orientation : la couche centrale du rendu doit être la surface (intensité médiane maximale au centre
   ± 3 couches) ; sinon rendu avec `--flip-normals` (seul écart autorisé, documenté).
2. Fraction de pixels valides ; distribution des probabilités (p50, p95, p99) par modèle.
3. Accord inter-modèles : Spearman ρ par blocs 64 × 64 entre reader-v2-LO et ink_9um ; nul = ρ entre cartes décalées
   circulairement (≥ 200 px, 100 tirages, p95).
4. Faux positifs : corrélation (ρ par blocs) de chaque carte avec l'intensité CT moyenne de la couche centrale et avec la
   distance au bord du masque valide ; une carte qui suit l'intensité (|ρ| ≥ 0,5) est jugée dominée par le fond/fibres.
5. Zones candidates : composantes connexes au-dessus du p99 de la carte moyenne, ≥ 0,25 mm², hors 1 mm du bord,
   présentes dans les deux modèles ; inspection visuelle privée (traits, largeur ≈ 0,3–1 mm, orientation cohérente).

## Hypothèse et critères
**H-034** : sur ce patch, les deux modèles figés concordent au-delà du hasard (ρ > p95 du nul) **et** leur accord n'est
pas expliqué par l'intensité CT (|ρ carte–intensité| < 0,5 pour les deux).
Soutenue si les deux conditions tiennent ; réfutée sinon (attribution : rendu/orientation, domaine, absence d'encre
sur la zone, faux positifs). Le comptage de lettres candidates relève de R1.3 (seuil ≥ 10 dans 4 cm²), sans conclusion
de lecture ici.

## Confidentialité
Cartes, rendus, coordonnées des zones et images restent dans `vesuvius-work/runs/EXP-029/` (hors dépôt) ; seuls des
agrégats numériques sont versionnés.

## Exécution (2026-11-27)
- Rendu `vc_render_tifxyz` (volume distant) : 31 × 2440 × 2440, 92 % de pixels valides ; `tifs_to_sv.py` rendu
  compatible zarr 2 (venv koine) sans changement de format. Inférences : 21 s (reader-v2-LO) et 17 s (ink_9um), 181 blocs.
- Analyse : `analyze.py <run> results.json` (agrégats seuls ; cartes et zones dans `vesuvius-work/runs/EXP-029/private/`).

## Résultats (`results.json`, R0)
| Mesure | reader-v2-LO | ink_9um |
|---|---|---|
| p50 / p95 / p99 | 0,27 / 0,32 / 0,39 | 0,32 / 0,58 / 0,70 |
| ρ carte–intensité CT (blocs 64²) | 0,04 | 0,03 |
| ρ carte–distance au bord | −0,03 | −0,10 |

- Orientation : médiane maximale à la couche 16 (centre 15) → OK, pas de `--flip-normals`.
- Accord inter-modèles ρ = **0,278** vs nul p95 = 0,041 (médiane −0,009) → au-delà du hasard, mais faible.
- Zones candidates au critère (p99 de la moyenne, ≥ 0,25 mm², hors 1 mm du bord, au-dessus du p95 de chaque modèle) :
  **0**.
- Inspection visuelle privée : rendu net (fibres horizontales et verticales du papyrus bien visibles → patch sur une
  vraie surface de feuillet) ; cartes = taches isolées sans structure de trait ; ink_9um montre un artefact de cadre
  le long des bords du rendu (non compté : exclu par la marge de 1 mm).

## Conclusion
- **H-034 soutenue** au critère préenregistré, mais l'accord (ρ 0,28) n'indique pas d'encre : il peut venir d'une
  texture commune non CT-intensité (fibres, bruit structuré). **Aucune lettre candidate** sur ces 4,11 cm² → R1.3 non
  déclenché.
- Interprétation non tranchée : (a) zone sans encre (marge, verso, lacune), (b) encre sous le seuil du domaine 1218,
  (c) chaîne de rendu propre (VC3D tifxyz → 31 couches, scale 1) non équivalente aux surface-volumes publiés sur
  lesquels les modèles ont été validés. **(c) n'a jamais été contrôlé** : sans contrôle positif, l'absence de zone est
  ininterprétable → R1.4.

## Correction d'orientation (2026-11-27, après EXP-030)
EXP-030 a montré que le rendu VC3D par défaut d'un tifxyz à normale sortante inverse l'ordre des couches (chaîne d'encre
aveugle : AUC 0,49 sur 0841). Le patch `out4` a une normale sortante → le rendu valide est `--flip-normals`
(`vesuvius-work/runs/EXP-029/flip/`, `results_flip.json`) ; les résultats ci-dessus (premier rendu) sont **invalides**
pour la question de l'encre et conservés pour traçabilité.

| Mesure (`--flip-normals`) | reader-v2-LO | ink_9um |
|---|---|---|
| p50 / p95 / p99 | 0,27 / 0,34 / 0,44 | 0,33 / 0,60 / 0,71 |
| ρ carte–intensité CT | 0,04 | 0,02 |
| ρ carte–distance au bord | −0,01 | −0,04 |

- Orientation : médiane maximale couche 14 (centre 15) ; accord inter-modèles ρ = **0,372** vs nul p95 0,068.
- Zones au critère : **3** (0,27–0,36 mm², 0,96 mm² au total, probabilité moyenne 0,58–0,64), coordonnées dans
  `private/zones.json`.
- Inspection privée : les trois zones sont des taches rondes ≈ 0,6 mm sans structure de trait ; dans le rendu, elles
  tombent sur des croisements de fibres et des taches sombres, pas sur des formes de lettres. Artefact de cadre
  d'ink_9um inchangé.

## Conclusion révisée
- **H-034 soutenue** (orientation valide), accord plus fort qu'avec la mauvaise face (0,372 vs 0,278).
- **Aucune lettre candidate** sur ces 4,11 cm² → R1.3 non déclenché. Le rendu étant contrôlé (EXP-030), l'absence est
  informative mais pas concluante : (a) zone sans encre (marge, lacune, verso), (b) encre sous le seuil dans le domaine
  1218. Un patch de 4 cm² ne permet pas de trancher → R1.5 (surface ≥ 40 cm²).
