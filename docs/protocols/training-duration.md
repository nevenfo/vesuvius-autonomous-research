# Protocole — durée d'entraînement optimale (K2, fixé le 2026-11-26 avant toute mesure)

Sources : `docs/state-of-the-art/training-efficiency.md` (K1.1) ; partitions : `docs/data/splits.md`.

## 1. Rôles des données (invariant)
| Rôle | Contenu | Usage autorisé |
|---|---|---|
| Entraînement | 38 segments `role == train` de `experiments/EXP-018/selection.json` (corpus EXP-018 inchangé) | gradients |
| **Validation K** | les 4 segments `role == holdout` de `selection.json`, hérités de `n_holdout` de reader-v2 (`v2_run.py`) et jamais vus par reader-v2-LO : PHerc0343P `20250904233748-0_b2`, `20250905172054-1_b2` ; PHerc0172 `20250926122938-w082_…`, `20250926132117-w083_…`. Liste figée le 2026-11-26 | choix de durée, checkpoint, arrêt, hyperparamètres |
| Test | 0841 × 3, 0009B, 0500P2 (+ rouleaux réservés H1.1) | une seule évaluation par configuration figée ; courbes = descriptives |

Les segments de validation sont construits comme ceux d'entraînement (`build.py`, mêmes seuils sur la carte publiée)
et évalués hors ligne avec `vesres.eval_ink` (même chaîne que les tests), et non par la validation interne en patches
de `train.py` (absente : aucun `validation_mask` dans le corpus). Avantage : EXP-018 est directement la référence R
et ses checkpoints sont évaluables sur la validation.

Limites assumées : (i) validation in-distribution (rouleaux 0343P et 0172 vus à l'entraînement, segments disjoints) ;
(ii) ses labels sont des cartes de modèles publiées (0343P : canon 2,4 µm ; 0172 : timesformer), comme les labels
d'entraînement → elle mesure la convergence de la distillation, pas la vérité terrain ; (iii) 0139 et 0814 n'y
figurent pas. Elle sert à choisir une durée, pas à mesurer la généralisation (rôle des tests et de H1).

## 2. Métriques et marge
- Primaire : AUC région `supervision` moyenne par segment de validation ; secondaire : AP sup.
- **δ = 0,01 AUC sup.** (≈ un tiers de la marge H-017 et du même ordre que les gains jugés utiles en EXP-011…016).
  Révision avant K4.2 seulement si l'écart-type inter-seeds mesuré en K4.1 dépasse δ/2 (alors δ = 2 σ, consigné).
- Non-infériorité d'une durée T vs référence R : bootstrap apparié par **blocs spatiaux** de 256 px (mêmes blocs
  tirés pour T et R, comme `eval_ink.block_bootstrap_auc`, ≥ 1 000 tirages, seed 0) de Δ = AUC(T) − AUC(R) ; non inférieure si borne basse IC 95 % unilatéral > −δ.
- Durée minimale = plus petite T non inférieure ; en cas d'égalité de coût, préférer la meilleure AUC moyenne.

## 3. Coût total (manifeste de chaque run)
Heures murales et GPU de : construction/cache des données, recherche de patches, entraînement (it/s médian,
attente données via le mode `benchmark` de `train.py`), validation/inférence, évaluation. Matériel et charge concurrente notés.

## 4. Schedule et plan d'expérience (K2.2)
- Un checkpoint intermédiaire d'un run cosine **n'est pas** un run court (LR non recuit) : les courbes K3 sur EXP-018
  sont une borne basse descriptive, jamais la base d'une décision.
- **R (référence)** : EXP-018 lui-même (recette reader-v2-LO, cosine 40k, warmup 500, seed 42, 38 segments).
- **W (candidat)** : même recette, schedule **WSD** (warmup 500, LR constant, cooldown `1-sqrt` sur 15 % de la durée
  cible) ; un run stable jusqu'à 34k avec checkpoints, cooldowns branchés depuis 8,5k → 10k, 17k → 20k, 34k → 40k.
  Coût ≈ 1,2 run. WSD n'existe pas dans `train.py` (cosine/cosine_annealing/one_cycle) : enrobage `LambdaLR` dans le
  lanceur, sans patch de villa, testé sur 200 itérations (courbe de LR attendue) avant le run.
- Le cooldown depuis un checkpoint cosine intermédiaire (non validé par la littérature) n'est pas utilisé.
- Ordre : R et W évalués sur validation K → décision de T → confirmation unique sur test de T vs R (et vs EXP-018).
- Arrêt anticipé (K4.3) : seulement si la courbe de validation de W montre un plateau ; règle = arrêt quand l'AUC de
  validation (évaluée tous les 5k) ne progresse pas de > δ/2 sur 2 évaluations consécutives, puis cooldown.

## 5. Débit (K5)
Chaque levier est mesuré isolément sur 1 000 itérations après chauffe, même seed ; conservé si le temps/itération
baisse d'au moins 10 % et si la perte moyenne sur la fenêtre reste dans ±1 % ; validé en fin de chaîne par l'AUC de validation dans δ.

## 6. Interdits
- Évaluer un checkpoint non final sur test pour **choisir** quoi que ce soit.
- Modifier ou interrompre EXP-018 (référence historique, 38 segments).
- Modifier δ ou la liste de validation après avoir vu un résultat de validation.
