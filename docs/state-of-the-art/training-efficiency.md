# Efficacité d'entraînement — état de l'art (K1.1, 2026-11-26)

Niveaux de preuve : **A** article évalué · **D** documentation officielle · **C** code de référence lu localement ·
**R** dépôt communautaire · **N** pratique usuelle non sourcée (à traiter comme hypothèse).

## 1. Choisir une durée sans contaminer le test
- **N** Durée, checkpoint et arrêt se décident sur une validation disjointe ; le test est évalué une fois, configuration figée.
- **A** WSD (warmup-stable-decay) — Hägele et al., NeurIPS 2024, <https://arxiv.org/abs/2405.18392> : un seul run à LR
  constant permet de brancher des *cooldowns* à plusieurs durées ; cooldown ≈ 10–20 % des pas suffit pour égaler le
  cosine ; forme `1-sqrt` meilleure que linéaire. Moyenne de poids (SWA/LAWA, fenêtre ≤ 2 500 pas) réduit l'écart
  sans remplacer un vrai cooldown.
- **A** Schedule-Free AdamW — Defazio et al., NeurIPS 2024, <https://arxiv.org/abs/2405.15682>
  (code `facebookresearch/schedule_free`) : aucun horizon fixe ; évaluer les poids moyennés (à vérifier dans le README).
- **A** Budgeted Training — Li et al., ICLR 2020, <https://arxiv.org/abs/1905.04753> : le schedule doit être ajusté au
  budget ; décroissance linéaire jusqu'à 0 robuste, y compris en segmentation.
- **N** Non-infériorité : aucune référence ML formelle trouvée. Méthode retenue : bootstrap apparié par région/segment de
  la différence (court − référence), borne basse de l'IC 95 % unilatéral > −δ, δ fixé avant mesure.
  Bootstrap apparié en segmentation : <https://arxiv.org/abs/2307.10926>, <https://arxiv.org/abs/2210.14677>.

## 2. Conséquence pour EXP-018 (cosine 40k)
- **A** Un checkpoint intermédiaire d'un run cosine **sous-estime** un run court recuit à la même durée
  (Hägele et al. v3, <https://arxiv.org/html/2405.18392v3>). Les courbes K3 sur checkpoints EXP-018 donnent donc une
  borne basse, pas la durée minimale.
- Rattrapage : cooldown court depuis un checkpoint intermédiaire. **Limite** : la source branche depuis un plateau
  constant, pas depuis un cosine à mi-décroissance → extrapolation à valider empiriquement (K2.2).
- Recommandation : pour K4, un run **WSD** unique avec cooldowns branchés à plusieurs durées est le moyen le moins coûteux
  de mesurer la courbe durée/performance (un seul entraînement + cooldowns de 10–20 %).

## 3. Débit par itération
- **D** PyTorch tuning guide, <https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html> :
  `cudnn.benchmark=True` (tailles fixes), `pin_memory`, réglage `num_workers`, `zero_grad(set_to_none=True)`,
  dimensions multiples de 8 en AMP, `torch.compile` (`reduce-overhead`/`max-autotune`), `channels_last` expérimental
  (2D ; `channels_last_3d` à mesurer).
- **R** `torch.compile` sous Windows : `triton-windows` (<https://github.com/woct0rdho/triton-windows>) ; PyTorch 2.10 →
  `triton-windows<3.7` ; Blackwell sm120 supporté (Triton ≥ 3.3, CUDA ≥ 12.8). Communautaire → essai isolé.
- **N** bf16 vs fp16 (RTX 5080) : pas de source ; bf16 supprime le `GradScaler` et les débordements AMP
  (`max_amp_overflow_events` de la recette) — à mesurer.
- **D** Zarr, <https://zarr.readthedocs.io/en/stable/user-guide/performance/> : chunks ≥ ~1 Mo alignés sur le patch,
  sharding, réduire la concurrence par processus quand plusieurs workers. Sur-souscription de threads Blosc × workers :
  hypothèse non sourcée.
- **C** `koine_machines/training/train.py` (villa `merge-ink-pipelines`) possède un mode `benchmark` (mesure du temps
  d'attente des données, `warmup_steps`) et une **EMA** native (`ema.enabled/decay/start_step`, validée et sauvegardée) :
  à utiliser avant tout outillage propre.
- **Observé** (EXP-018, 2026-11-26) : recherche de patches ≈ 34 min par lancement, cache JSON 1,5 Go dans `out_dir`
  (réutilisé à la reprise) ; débit 1,6 → 3,6 it/s après chauffe ; ~57/59 Go de mémoire engagée (cause probable de
  l'OOM du 1er run) ; utilisation GPU basse pendant la recherche de patches.

## 4. Écosystème Vesuvius / références
- **C** Recette officielle `configs/aligned21_hybrid_3d2d.json` : 78 125 itérations, fp16, `val_every` 5 000 ; reader-v2 : 40k.
  Aucun arrêt anticipé dans `train.py` ; seul `best_checkpoint_metric` (`val_balanced_accuracy`) sélectionne — et
  exige un `validation_mask` par segment (découvert à côté des labels), absent de notre corpus LO.
- **R** nnU-Net v2 : 1 000 époques par défaut, variantes `nnUNetTrainer_Xepochs`, pas d'early stopping
  (<https://github.com/MIC-DKFZ/nnUNet/issues/2179>).
- Non résolu : durées/critères de reader-v2 au-delà de son `train_config.json` (déjà lu en E1.5).

## 5. Leviers classés (→ `docs/hypotheses.md`, H-018…H-021)
| Levier | Gain attendu | Effort | Risque scientifique | Priorité |
|---|---|---|---|---|
| Courbe durée/perf via WSD + cooldowns branchés (H-018) | ×2–4 sur la durée si plateau | moyen | faible si validation séparée | 1 |
| Débit : profil `benchmark` puis workers/zarr/bf16 (H-019) | 10–50 % temps/itération | faible | nul si métriques dans δ | 1 |
| Coût fixe recherche de patches : cache réutilisé entre runs de même corpus (H-020) | −34 min/run | faible | nul | 2 |
| EMA native (H-021) | gain qualité à durée égale → durée plus courte | faible | faible | 2 |
| `torch.compile` via triton-windows | 10–30 % (non mesuré) | moyen | dépendance communautaire | 3 |
| Schedule-Free AdamW | pas d'horizon à choisir | moyen | change l'optimiseur de la recette | 3 |
