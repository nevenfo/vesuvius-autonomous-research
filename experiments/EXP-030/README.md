# EXP-030 — R1.4 : contrôle positif de notre chaîne de rendu (VC3D tifxyz → surface-volume) sur un segment à encre connue

**Statut : terminé** — H-035 réfutée au premier essai (AUC 0,49 : ordre des couches inversé), **soutenue au second essai argumenté** `--flip-normals` (ρ 0,948, AUC 0,825 vs 0,832). Préenregistré le 2026-11-27 avant tout rendu.

## Question
L'absence de zone candidate sur 1218 (EXP-029) est ininterprétable si notre rendu propre (`vc_render_tifxyz --scale 1
-g 0 -n 31` → `tifs_to_sv.py`) n'est pas équivalent, pour la chaîne d'encre, aux surface-volumes publiés sur lesquels
elle a été validée. On le contrôle sur un segment publié à encre étiquetée.

## Objet
PHerc0841 `20260220213127-w00` (référence EXP-001 ; tifxyz publié `tifxyz_9.366`, 211 × 238 nœuds, scale 0,05 →
4220 × 4760 = grille du surface-volume publié 28 × 4220 × 4760) ; volume `20250821151531-9.366um-1.2m-113keV-masked.zarr`
(S3 public). Labels : `inklabels` / `supervision` / `validation` (revue, R2), métriques `src/vesres/eval_ink.py`.
Parenté : reader-v2-LO (EXP-018) a été entraîné avec 0841 — ce contrôle mesure l'**équivalence de rendu**, pas la
généralisation ; la même carte de référence (SV publié) est inférée par le même modèle.

## Protocole
1. Rendu propre comme EXP-029 (31 couches, scale 1, groupe 0, volume distant), `tifs_to_sv.py`.
2. Inférence reader-v2-LO (`ckpt_040000`) sur le rendu propre **et** sur le SV publié en cache, mêmes options qu'EXP-029.
3. Mesures : ρ de Spearman par blocs 64² (blocs ≥ 99 % valides dans les deux) entre les deux cartes ; AUC (revue) de
   chaque carte par `eval_ink.py` ; contrôle d'orientation (médiane d'intensité maximale à ± 3 couches du centre).

## Hypothèse et critères
**H-035** : notre rendu propre est équivalent pour la chaîne d'encre : ρ par blocs ≥ 0,7 **et** AUC revue du rendu
propre ≥ AUC revue du SV publié − 0,03.
Réfutée sinon → attribuer (orientation/`--flip-normals`, nombre de couches, interpolation, décalage de grille) ; un seul
second essai argumenté autorisé (p. ex. `--flip-normals` si l'orientation échoue, ou 28 couches).
Conséquence : soutenue → l'absence de zone sur 1218 (EXP-029) devient informative (domaine ou zone sans encre) ;
réfutée → EXP-029 à refaire avec le rendu corrigé.

## Résultats (`results.json`, `results_flip.json`)
| Rendu | ρ blocs cartes | ρ blocs intensité (centre) | AUC revue | AP revue |
|---|---|---|---|---|
| SV publié (28 couches) | — | — | **0,8318** | 0,155 |
| Essai 1 : propre, 31 couches | 0,215 | 0,967 | 0,4928 | 0,030 |
| Essai 2 : propre, `--flip-normals` | **0,948** | 0,967 | **0,8252** | 0,154 |

- Essai 1 : grilles alignées dans le plan (ρ intensité 0,967) mais AUC au hasard. Diagnostic (corrélation couche à
  couche sur 800 × 800 px) : couche publiée j ↔ couche propre ≈ 28 − j (r 0,89–0,95) → **ordre des couches inversé**.
- Essai 2 (seul écart autorisé, argumenté par ce diagnostic) : équivalence atteinte (Δ AUC −0,007, ρ 0,948).
- **Règle d'orientation sans label** (`orientation.py`) : sur les 3 segments publiés de 0841, la normale de grille
  `cross(du, dv)` pointe vers l'extérieur (médiane du cosinus avec le rayon sortant 0,42–0,44 ; 83–85 % > 0) **et** le
  rendu VC3D par défaut est inversé par rapport au SV publié (3/3, corrélation couche à couche). Le patch 1218 `out4`
  a une normale sortante (0,956 ; 99 %) → `--flip-normals`.

## Conclusion
- **H-035 soutenue (second essai)** : notre chaîne de rendu est équivalente aux SV publiés pour l'encre **à condition**
  d'appliquer `--flip-normals` aux tifxyz à normale sortante. Sans cette correction, la chaîne d'encre est aveugle
  (AUC 0,49) sans aucun signe visible dans le rendu ni dans les distributions.
- Conséquence : EXP-029 (premier rendu) a lu la mauvaise face ; refait avec `--flip-normals` (`results_flip.json`).
- Limites : axe du rouleau approché par le centre du volume (0841) ou du masque de prédiction (1218) ; 3 segments d'un
  seul rouleau, tous issus du même outil de croissance.
