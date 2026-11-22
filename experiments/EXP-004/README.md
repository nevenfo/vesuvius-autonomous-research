# EXP-004 — H-009 : modèles 9 µm sur le segment étiqueté PHerc0009B (8,64 µm, 116 keV) et fusion (H-003)

- **Date** : 2026-11-22 · segment `20250919125754-auto_grown_20250919055754487_inp_hr` (seul segment 0009B portant des
  `ink-labels`, catalogue officiel), surface-volume `8.64um-1.2m-116keV-volume-20250521125136.zarr/0` (31, 7040, 5700),
  labels `ink-labels/2.401um-volume-20250820154339/20260918` (25360×20520 → grille 8,64 µm, INTER_AREA ≥ 128).
- **Parenté** (`docs/data/splits.md`) : reader-v2 = objet vu, **segment tenu à l'écart** (absent des 14 segments 0009B de
  `train_config.json`, entraînés en natif 8,64 µm) ; ink_9um = objet non vu ; Hecate = NV.
- **Inférence** : reader-v2 et ink_9um s43 comme EXP-001 (`koine_machines.inference.infer`, grille native 8,64 µm, sans
  rééchantillonnage) ; Hecate via `experiments/EXP-003/hecate_run.py <seg> PHerc0009B 8.64 runs/EXP-004` (8,64→9,6 µm).
- **Coût** : reader-v2 66 s, ink_9um 43 s, Hecate 4 min 47 s mur (rééchantillonnage inclus) ; téléchargement 57 s.
- **Prédictions** (hors Git, `vesuvius-work/runs/EXP-004/`) sha256 : reader-v2 `c1fe3dcb…`, ink_9um `7e3262b0…`, Hecate `c61951da…`.
- Région `validation` ⊂ `supervision` sur ce segment → « revue » = « supervision » (pas de zone à labels incomplets type H-008).

## Résultats (région supervision ; prévalence encre 22 %, 763 301 px positifs)
| Modèle | AUC protocole | AP | IC95 AUC (blocs) |
|---|---|---|---|
| reader-v2 | **0,927** | 0,826 | 0,887–0,948 |
| ink_9um s43 | 0,813 | 0,610 | 0,774–0,843 |
| Hecate | 0,884 | 0,780 | 0,840–0,916 |
| fusion moyenne reader-v2+Hecate | **0,935** | **0,845** | 0,901–0,956 |
| fusion moyenne des 3 | 0,927 | 0,831 | 0,892–0,950 |

Corrélation de Pearson reader-v2/Hecate sur pixels valides : 0,615.

## Conclusions
- **H-009 soutenue** : reader-v2 garde AUC sup. 0,927 (≥ 0,80) à 8,64 µm / 116 keV — mais sur un objet vu à
  l'entraînement (même fragment, même scan) : ce n'est **pas** une généralisation inter-objets. ink_9um, objet réellement non
  vu, tient 0,813 à une résolution différente de son entraînement (≈ 9,36 µm), sans rééchantillonnage.
- **H-003** (reader-v2+Hecate) : AP +0,0195 vs meilleur modèle seul (reader-v2) — juste sous le seuil de 0,02 ; AUC +0,009.
  Même signe que sur 0841 (EXP-003, +0,025 en moyenne) ; ajouter ink_9um n'apporte rien. Statut inchangé : soutenue,
  non confirmée (pas d'objet indépendant pour reader-v2 ici).
