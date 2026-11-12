# Hypothèses classées (révisées après chaque expérience ou veille)

Score = impact sur la lecture intégrale × information attendue / coût. Statut : ouverte · en cours · confirmée · réfutée · suspendue.

| ID | Hypothèse | Référence | Données | Métrique | Échec si | Coût | Statut |
|---|---|---|---|---|---|---|---|
| H-001 | Un modèle d'encre 9 µm publié (reader-v2) reproduit sur notre matériel sa performance auto-déclarée sur un rouleau tenu à l'écart | AUC 0,824 vs labels (A) | PHerc0841, layers 9,366 µm + labels 2,403 µm | AUC, AP, F1@seuil, FP sur papyrus vierge | AUC < 0,75 ou écart > 0,05 inexpliqué | faible (inférence, < 1 h GPU) | ouverte |
| H-002 | Les labels `ink-labels/20260918` des rouleaux sont corrélés aux sorties des modèles qui les ont produits (circularité) au point de biaiser les métriques | — | 0139 (labels 9 µm) vs ink_9um (entraîné sur 0139) | écart AUC rouleaux vus/non vus | écart négligeable | faible | ouverte |
| H-003 | La fusion calibrée de deux modèles 9 µm indépendants (ink_9um, reader-v2) améliore AP sur rouleaux non vus sans hausse des FP | meilleur modèle seul | 0841 (+ 1 autre non vu) | AP, FP vierge, ECE | gain AP < 0,02 | faible | ouverte |
| H-004 | Le décalage en profondeur de la fenêtre de couches explique une part majeure des échecs à 9 µm ; un recentrage automatique par segment améliore AUC | fenêtre par défaut | segments 9 µm étiquetés | AUC par décalage −6…+6 | aucune sensibilité | faible | ouverte |
| H-005 | Le 2,4 µm (pipeline officiel) apporte un gain mesurable sur la lisibilité vs 9 µm à coût calcul acceptable sur RTX 5080 | 9 µm | 1667 crop | AUC, temps, VRAM | gain nul ou VRAM > 14 Go | moyen | ouverte |
| H-006 | Un indicateur sans label (cohérence inter-modèles, entropie) prédit les zones « non récupérées » vs « sans encre » | — | 0841/0139 | corrélation avec erreurs | corr < 0,3 | moyen | ouverte |
| H-007 | Les métriques de qualité de surface (windcheck/TIFXYZ Doctor) prédisent les zones où l'encre échoue | — | segments étiquetés | AUC locale vs score géométrique | aucune relation | moyen | ouverte |

Prochaine : H-001 (premier chemin vertical D1, cheap, falsifiable, base de toutes les comparaisons).
