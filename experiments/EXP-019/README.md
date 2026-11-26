# EXP-019 — K3 : courbe performance/durée des checkpoints EXP-018 sur la validation K

Protocole : `docs/protocols/training-duration.md` (fixé avant mesure). Référence R = EXP-018 `ckpt_040000`.
Validation K = 4 holdouts reader-v2 (0343P ×2, 0172 ×2), construits par `EXP-018/build.py … holdout`
dans `vesuvius-work/data/v2lo_val/`. Objets de test non utilisés ici.

## Fichiers
`run_val.sh <run_dir> <step>…` (inférence, temps par segment dans `runs/EXP-019/meta.txt`) ;
`analyze.py <work> 40000 results.json <step>…` (AUC/AP sup. par segment, non-infériorité δ = 0,01 par bootstrap apparié par blocs).

## État
- Test de fumée 2026-11-26 : `ckpt_005000` sur 0343P `20250904233748-0_b2`, 32 s, grille 3620×2500 = labels, 113 blocs, AUC sup. 0,694 (pendant l'entraînement, non retenu).
- Mesures complètes après la fin d'EXP-018 (pas d'inférence concurrente, pour ne pas fausser le débit mesuré en K3.1).

## Limite
Checkpoints d'un run cosine 40k : borne basse d'un run court recuit, descriptif ; la décision de durée relève de K4.
