# EXP-001 — Reproduction zéro-shot de reader-v2 et ink_9um sur PHerc0841 w00

- **Hypothèse** : H-001 — reader-v2 reproduit sur notre matériel sa performance auto-déclarée sur un rouleau tenu à l'écart.
- **Date** : 2026-11-12 · **Matériel** : RTX 5080 16 Go (sm_120), Windows 11, pilote 617.42 / CUDA 13.4.
- **Niveau de validation** : reproduction numérique d'un résultat publié (pas une nouvelle lecture).

## Entrées
| Élément | Valeur |
|---|---|
| Rouleau / segment | PHerc0841 / `20260220213127-w00` (catalogue officiel, ETag 9e782ff1…) |
| Surface-volume | `surface-volumes/9.366um-1.2m-113keV-volume-20250821151531.zarr/0`, (28, 4220, 4760) uint8, ESRF 113 keV |
| Labels | `ink-labels/2.403um-volume-20260319124803/20260918/{inklabels,supervision,validation}.zarr/0`, 16460×18560 → grille 9,366 µm par INTER_AREA ≥ 128 |
| Provenance | `data_provenance.json` (URLs exactes, date de copie) |

## Code et modèles
- Inférence : `koine_machines.inference.infer` (villa `merge-ink-pipelines` @ 47a9c37f, non modifié), `--overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward` ; env `env-koine.lock` (torch 2.10.0+cu128) ; lanceur `run_one.sh`.
- reader-v2 : `domenicor046/reader-v2/reader-v2-step040000.pth`, sha256 `654ec5ac…d5a6`, MIT.
- ink_9um : `scrollprize/ink_9um/hybrid_3d2d-seed43/step-060000.pth`, sha256 `bf229faf…d270`, MIT.
- Évaluation : `python -m vesres.eval_ink <pred.tif> <segment_dir> <out.json>` (protocole reader-v2 répliqué + AP, F1, IC bootstrap de blocs 256 px).
- Empreintes des prédictions : `predictions.sha256` (cartes conservées hors dépôt, `C:\Users\FlowUP\vesuvius-work\runs\EXP-001`, non publiables — licence données).

## Résultats
| Modèle | Région | AUC (protocole) | Publié | AUC exacte | IC 95 % blocs | AP | F1 max | Prévalence |
|---|---|---|---|---|---|---|---|---|
| reader-v2 | revue (sup ∪ val) | **0,8320** | 0,832 | 0,8322 | [0,793 ; 0,870] | 0,181 | 0,283 | 2,85 % |
| reader-v2 | supervision | **0,8755** | 0,8755 | 0,8757 | [0,779 ; 0,901] | 0,742 | 0,673 | 22,2 % |
| ink_9um s43 60k | revue | **0,7555** | 0,7555 | 0,7557 | [0,712 ; 0,803] | 0,096 | 0,166 | 2,85 % |
| ink_9um s43 60k | supervision | **0,7399** | 0,7399 | 0,7406 | [0,687 ; 0,811] | 0,483 | 0,475 | 22,2 % |

Coût : reader-v2 42 s mur (≈ 30 s d'inférence), ink_9um 33 s ; pic VRAM +1,06 Go au-dessus de la base (6,2 Go occupés par d'autres applications).

## Conclusions
1. **H-001 confirmée sur ce segment** : valeurs publiées reproduites à 4 décimales pour les deux modèles → environnement, données, alignement des labels et métrique sont correctement interprétés (base fiable pour la suite).
2. L'écart reader-v2 − ink_9um (+0,077 AUC revue) est supérieur à la largeur des IC, mais les IC par blocs (~±0,04) montrent qu'**une AUC sur un seul segment ne suffit pas** à départager des modèles proches (ex. reader-v2 vs Hecate, Δ ≈ 0,02).
3. L'AUC masque une précision faible dans la région « revue » (AP 0,18 pour 2,85 % d'encre) alors que l'AP vaut 0,74 en supervision : soit la région de validation contient de l'encre non étiquetée, soit les modèles y produisent beaucoup de faux positifs → nouvelle hypothèse H-008.

## Extension E1.1 — les 3 segments 0841 étiquetés
Mêmes code/paramètres ; sous-dossiers `20260220214732-…/`, `20260221022814-…/` (métriques + provenance) ; ~30 s par inférence.

| Modèle | Région | w00 | auto_grown_…144552 | auto_grown_…174252 | Moyenne | Publié (moyenne) |
|---|---|---|---|---|---|---|
| reader-v2 | revue | 0,8320 | 0,8387 | 0,8005 | **0,8237** | 0,8237 |
| reader-v2 | supervision | 0,8755 | 0,8263 | 0,8193 | **0,8404** | 0,8404 |
| ink_9um s43 | revue | 0,7555 | 0,7095 | 0,7326 | **0,7325** | 0,7325 |
| ink_9um s43 | supervision | 0,7399 | 0,7006 | 0,7470 | **0,7292** | 0,7291 |

12/12 valeurs reproduites (écart max 1e-4). IC 95 % par blocs par segment : largeur 0,08–0,17 → les écarts < ~0,05 entre modèles ne sont pas résolus par ces 3 segments.

## Limites
- 3 segments d'un seul rouleau ; labels = pseudo-labels raffinés (qualifiés « human » par reader-v2) ; pas d'évaluation papyrologique.
- Les IC par blocs supposent l'indépendance entre blocs de 256 px (≈ 2,4 mm), approximation.
