# Références de lecture et outils géométriques (T1.1, W2.1 — 2026-11-27)

Statuts : V vérifié sur la source · A auto-déclaré · NV non vérifié. Fiches au format de l'invariant « apprentissage
collectif » (problème, méthode, preuve, données, limites, reproductibilité, licence, intérêt, expérience comparative).

## 1. Références au niveau caractère/mot (T1.1)

### PHerc. 1667 — Angelotti et al., arXiv:2606.29085 (PDF lu localement, sha256 3f8cfecc…)
- **Transcription papyrologique complète colonne par colonne (Col. 1–22, lignes numérotées, points souscrits,
  crochets de restitution)** dans les Methods ; « transcription artifacts » annoncés sur le data browser (CC BY-NC) — V.
- Couverture publiée : 31 spires, **1231 cm²** déroulés, ≈ **860 cm²** de surface écrite (bas de 22 colonnes, ≤ 12
  lignes), **33 cm²** de traces indéchiffrables ; déroulement semi-automatique avec ≈ **25 h d'annotation manuelle par
  spire** (≈ 775 h) — V. Lecture d'une région à 1,1 µm qui rend lisibles des passages illisibles à 2,4 µm — A.
- Critères d'acceptation des lectures : surface géométriquement ajustée au feuillet, **formes de lettres stables à
  travers rendus ou passes d'inférence répétés**, consensus de 9 papyrologues — V.
- Classe : **R3 avec dépendance aux modèles** (lecture humaine de rendus ink-enhanced, modèles de la famille ResNet3D
  à pseudo-labels itératifs) → indépendante de nos chaînes 9 µm, pas de la famille canon.
- Catalogue : 20 segments `w011…w041` (tifxyz aplatis), 76 `ink-detection`, 6 `ink-labels`, `layers-zarr` — V.
- Code : villa commit `e583fb67` ; poids sur Hugging Face `scrollprize` (collection d'ablation 1667) — V.
- Intérêt : **seule référence textuelle complète disponible** → permet CER/WER par alignement de séquences par colonne
  (sans coordonnées par lettre) et l'alignement colonne ↔ segment par les figures/ordre des spires.
- Licence/usage : texte savant publié ; conservé **privé** (`vesuvius-work/refs/PHerc1667/`), jamais republié dans le dépôt.
- Expérience comparative : V3/V2 sur 1667 (chemin v0 → glyphes → reconnaissance) avec CER par colonne.

### Autres
| Source | Contenu | Classe | Licence | Usage |
|---|---|---|---|---|
| ICDAR 2023 lettres grecques sur papyrus (Zenodo 13825619) | 150 images, boîtes + classes | R2 (photos, autre domaine) | CC BY-NC (images variables) | pré-entraînement/évaluation d'un classifieur de glyphes ; écart photo→CT à mesurer |
| AL-PUB (arXiv:2401.12513) | ≈ 205 k vignettes de lettres d'Oxyrhynque | R2 (autre domaine) | NV | idem |
| Lectures First Letters 2026 (306B, 343…) | phrases publiées sans coordonnées | R3 partielle | page publique | contrôles qualitatifs |
| PHerc. 172 (Korotetskyi) | masques dérivés d'une prédiction | R0 | CC BY-NC | non utilisable comme vérité |
| Paris 4 | embargo jusqu'au 2027-06-25 | — | — | aucun |

## 2. Outils géométriques existants (W2.1)
| Outil | Rôle | Entrées / sorties | Coût / matériel | Licence | Statut |
|---|---|---|---|---|---|
| VC3D (villa `volume-cartographer`), AppImage `VC3D-*-linux-x86_64.AppImage` (release `latest` / `vc3d-archive-latest-*`) ; Docker `ghcr.io/scrollprize/villa/volume-cartographer:edge` (build 2026-05) | GUI + outils `vc_*` en CLI | zarr local ou distant → tifxyz | CPU (OpenMP) ; libs graphiques requises | **GPL-3.0** (sous-dossier ; racine MIT) : utilisation sans redistribution | V |
| `vc_grow_seg_from_seed` (GrowPatch, modes `default`/`projection`/`streamline`) | croissance d'un patch depuis une graine | `-v` volume, `-p` JSON (`generations`, `thread_limit`…), `--seed x y z` → `auto_grown_*/{x,y,z}.tif, meta.json` | non documenté | GPL-3.0 | V |
| `vc_render_tifxyz` | rendu du surface-volume | `-v` volume `-s` segment `--scale` `-g` niveau → `render/NN.tif` | lecture distante à la volée | GPL-3.0 | V |
| Spiral fitting (`villa/spiral-fitting`) | spirale par spire sur tout le rouleau | prédiction de surface seuillée, `umbilicus.json`, normales lasagna → `wNNN/` tifxyz | GPU NVIDIA, Python ≥ 3.14, torch < 2.13 | NV | V |
| Lasagna (`villa/lasagna`) | normales/aplatissement | OME-Zarr → modèle → tifxyz (`fit2tifxyz.py`) | GPU (repli CPU), Python 3.14 | NV | V |
| windcheck (tiers, bêta) | auto-intersections | tifxyz | — | NV | A |
Pratique des lauréats 2026 (A) : GrowPatch sur prédiction de surface « m7 » (306B), spiral-fitter + raccords manuels
(211, 343), traceur + modèle de fibres (846A) ; correction manuelle dans tous les cas ; temps humain non publié.
Pièges : sheet switches (principal échec, correction manuelle), compression, dérive ; aucune méthode n'assure une
surface complète correcte sans vérification humaine (open problems 2026, V).

## 3. Décisions
- T : PHerc. 1667 devient le manuscrit de référence de V3/V2 (transcription R3*, segments et prédictions publiés).
- W2.3 : essayer d'abord l'AppImage VC3D sous WSL (`list`, puis `vc_grow_seg_from_seed` sur un rouleau éligible avec
  graine choisie dans la prédiction de surface), mesurer surface, temps machine, temps humain ; spiral fitting ensuite
  si GrowPatch ne suffit pas. Aucun développement géométrique propre à ce stade.
