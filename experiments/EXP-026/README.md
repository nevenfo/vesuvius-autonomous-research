# EXP-026 — K3.1 : perte d'entraînement et débit de la référence EXP-018 (descriptif)

**Statut : terminé** (2026-11-27). Aucune décision de durée tirée ici (perte d'entraînement ≠ validation, protocole K2).

## Données
`runs/EXP-018/train/train_0.log` : seule la reprise 13 000 → 40 000 est journalisée (le journal de 0 → 13 212 du
2026-11-26 a été écrasé par la reprise). Script : extraction des barres tqdm (`results.json`).

## Résultats
- Perte moyenne par tranche de 2 000 it. : 0,5688 (12–14 k) → 0,5605 (38–40 k), décroissance quasi linéaire et très
  faible (−1,5 % sur 27 000 it.) ; dernière valeur 0,555 (fin de cosine).
- Débit de la reprise : 27 000 it. en 16 005 s = **1,69 it/s** (4,4 h), contre ≈ 5,7 it/s mesuré sur tenseurs
  synthétiques (EXP-018) → entraînement limité par le chargement des données (cohérent avec EXP-018).

## Interprétation et limites
Rendement décroissant probable au-delà de ~15–20 k sur la perte d'entraînement, mais seule la validation K (K3.2) peut
fonder une durée. Phase K suspendue (aucune recette neuronale retenue dans le système de lecture, `plan.md`) :
résultat conservé pour le jour où un ré-entraînement (ex. P3.2 sans 1667) sera justifié — y viser 20 k au plus en
premier essai, avec validation K.
