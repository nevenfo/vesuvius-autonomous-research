# Hypothèses classées (révisées après chaque expérience ou veille)

Score = impact sur la lecture intégrale × information attendue / coût. Statut : ouverte · en cours · confirmée · réfutée · suspendue.

| ID | Hypothèse | Référence | Données | Métrique | Échec si | Coût | Statut |
|---|---|---|---|---|---|---|---|
| H-001 | Un modèle d'encre 9 µm publié (reader-v2) reproduit sur notre matériel sa performance auto-déclarée sur un rouleau tenu à l'écart | AUC 0,824 vs labels (A) | PHerc0841, layers 9,366 µm + labels 2,403 µm | AUC, AP, F1@seuil, FP sur papyrus vierge | AUC < 0,75 ou écart > 0,05 inexpliqué | faible (inférence, < 1 h GPU) | **confirmée** (EXP-001 : 12/12 valeurs publiées reproduites sur 3 segments) |
| H-002 | Les labels `ink-labels/20260918` des rouleaux sont corrélés aux sorties des modèles qui les ont produits (circularité) au point de biaiser les métriques | — | 0139 (labels 9 µm) vs ink_9um (entraîné sur 0139) | écart AUC rouleaux vus/non vus | écart négligeable | faible | ouverte |
| H-003 | La fusion calibrée de deux modèles 9 µm indépendants (ink_9um, reader-v2) améliore AP sur rouleaux non vus sans hausse des FP | meilleur modèle seul | 0841 (+ 1 autre non vu) | AP, FP vierge, ECE | gain AP < 0,02 | faible | rejetée pour reader-v2+ink_9um (EXP-002) ; **soutenue** pour reader-v2+Hecate (EXP-003 : AP sup. +0,025 en moyenne vs Hecate seul, 2/3 segments ≥ 0,02 ; 0009B : +0,0195, EXP-004 ; FP/ECE non mesurés) → à confirmer sur un objet indépendant |
| H-004 | Le décalage en profondeur de la fenêtre de couches explique une part majeure des échecs à 9 µm ; un recentrage automatique par segment améliore AUC | fenêtre par défaut | segments 9 µm étiquetés | AUC par décalage −6…+6 | aucune sensibilité | faible | ouverte |
| H-005 | Le 2,4 µm (pipeline officiel) apporte un gain mesurable sur la lisibilité vs 9 µm à coût calcul acceptable sur RTX 5080 | 9 µm | 1667 crop | AUC, temps, VRAM | gain nul ou VRAM > 14 Go | moyen | ouverte |
| H-006 | Un indicateur sans label (cohérence inter-modèles, entropie) prédit les zones « non récupérées » vs « sans encre » | — | 0841/0139 | corrélation avec erreurs | corr < 0,3 | moyen | ouverte |
| H-007 | Les métriques de qualité de surface (windcheck/TIFXYZ Doctor) prédisent les zones où l'encre échoue | — | segments étiquetés | AUC locale vs score géométrique | aucune relation | moyen | ouverte |
| H-008 | Dans la région `validation` des labels 0841, l'AP faible (0,18 vs 0,74 en supervision, EXP-001) vient surtout d'encre non étiquetée plutôt que de faux positifs des modèles | AP par région | 0841 (3 segments), 2 modèles | AP/prévalence par région ; accord inter-modèles sur les « FP » | les « FP » de validation ne sont pas plus cohérents entre modèles que du bruit | faible | **soutenue** (EXP-002 : accord 2e modèle 0,39–0,45 vs base 0,05) ; test discriminant H-008b ouvert |
| H-009 | Un modèle 9 µm (reader-v2) conserve AUC supervision ≥ 0,80 sur un 2e objet et une autre énergie (116 keV / 8,64 µm) | EXP-001 | PHerc0009B segment étiqueté (8,64 µm + labels 2,401 µm) — attention : autres segments 0009B dans l'entraînement de reader-v2 | AUC sup., IC blocs | AUC < 0,75 | faible | **soutenue** (EXP-004 : reader-v2 0,927, segment tenu à l'écart d'un objet vu ; ink_9um, objet non vu, 0,813) |

Contrainte de généralisation constatée : les objets étiquetés publiés (0139, 0814, 1667, Paris4, 0009B, 0500P2) sont presque tous dans l'entraînement des modèles 9 µm ; seul 0841 est déclaré entièrement tenu à l'écart → établir la matrice de parenté (B2.3) avant toute affirmation inter-rouleaux.

Prioritaire : H-008b (test discriminant labels incomplets) → H-004 ; métrique primaire = région supervision. B2.3, E1.4, H-009 faits.
