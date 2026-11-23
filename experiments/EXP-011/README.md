# EXP-011 — H-010 : fusion moyenne reader-v2+Hecate sur un 3e objet (PHerc0500P2)

- **Date** : 2026-11-23 · segment PHerc0500P2 `20250825181859--1` (même données/masques qu'EXP-008, grille 9,362 µm,
  (5880, 3300)).
- **Parenté** (`docs/data/splits.md`) : reader-v2 = objet vu, segment tenu à l'écart ; Hecate = NV ; ink_9um = non vu.
- **Inférence** : reader-v2 et ink_9um repris d'EXP-008 ; Hecate via `experiments/EXP-003/hecate_run.py
  20250825181859--1 PHerc0500P2 9.362 runs/EXP-008` (9,362→9,6 µm puis retour, 132 s). Prédiction hors Git
  `vesuvius-work/runs/EXP-008/20250825181859--1/pred_hecate.tif`, sha256 `bb6a4cf9…`. Toutes en uint8 0–255 →
  fusion = moyenne arithmétique directe.
- **Code** : `analyze.py` → `results.json`. **Critère fixé avant** (EXP-010) : H-010 réfutée si
  AP_sup(fusion) − max(AP_sup reader-v2, AP_sup Hecate) < 0,02. Ajout : IC95 apparié du gain par bootstrap de blocs
  256 px (72 blocs, 200 tirages, ≤ 2000 px/bloc).

## Résultats (région supervision ; prévalence 21 %, 544 501 px positifs)
| Modèle | AUC protocole | AP | IC95 AUC (blocs) |
|---|---|---|---|
| reader-v2 | 0,873 | 0,721 | 0,833–0,907 |
| ink_9um s43 | 0,767 | 0,521 | 0,740–0,809 |
| Hecate | 0,910 | 0,781 | 0,889–0,939 |
| **fusion reader-v2+Hecate** | **0,923** | **0,804** | 0,902–0,946 |
| fusion des 3 | 0,905 | 0,784 | 0,886–0,930 |

Gain fusion − meilleur seul (Hecate) : **AP +0,023**, AUC +0,013. IC95 apparié du gain d'AP : **[−0,002 ; 0,036]** ;
34 % des tirages ≥ 0,02. Pearson reader-v2/Hecate (pixels valides) : 0,718.

## Conclusions
- **H-010 soutenue au critère pré-enregistré** (gain ponctuel 0,023 ≥ 0,02), **mais non robuste** : l'IC apparié inclut
  0 et le seuil n'est atteint que dans un tiers des rééchantillonnages. Lecture honnête : gain positif probable,
  ampleur ≈ seuil.
- Ici **Hecate est le meilleur modèle seul** (0,910 vs 0,873), à l'inverse de 0009B ; la fusion bat pourtant les deux →
  le gain ne vient pas d'un modèle dominant, il est cohérent avec une complémentarité (Pearson 0,72).
- Bilan H-003 reader-v2+Hecate sur 3 objets : 0841 +0,025 (moy. 3 segments), 0009B +0,0195, 0500P2 +0,023 → même signe
  partout, ampleur ≈ 0,02. Ajouter ink_9um dégrade (comme EXP-004).
- Limite : 0500P2 et 0009B sont des objets vus par reader-v2 (segments tenus à l'écart) et la parenté de Hecate est NV ;
  aucun des 3 objets n'est indépendant des deux modèles à la fois. Décision : la fusion devient la **candidate par
  défaut** pour les cartes de démonstration, avec l'incertitude affichée ; pas de revendication de gain inter-rouleaux.
