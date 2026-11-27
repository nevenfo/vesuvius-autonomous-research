# Protocole d'indépendance, de provenance et de contrôle des fuites (2026-11-27)

Complète `docs/data/splits.md` (matrice de parenté B2.3, provenance des ink-labels B1.2).

## 1. Graphe de provenance
Nœuds : manuscrit → scan (résolution, énergie) → volume → segment → région → label / pseudo-label → modèle →
checkpoint → prédiction → métrique ; plus transcriptions humaines et prédictions communautaires.
Arêtes à tracer : « entraîné sur », « initialisé depuis », « distillé de », « pseudo-étiqueté par », « aligné sur »,
« même volume physique à une autre résolution », « sélectionné à l'aide de ».
Fichier machine-lisible : `docs/data/provenance.csv` (P1) — colonnes `source,relation,cible,statut,preuve`.

## 2. Classes de référence
| Classe | Définition | Exemples actuels | Ce qu'on peut conclure |
|---|---|---|---|
| R0 | sortie d'un autre modèle | accord inter-modèles (EXP-002/005), masques Korotetskyi (172) | accord, jamais exactitude |
| R1 | labels humains affinés par pseudo-labeling d'une famille de modèles possiblement parente du modèle évalué | ink-labels `20260918` des rouleaux (0841…) ; canon/reader-v2/LO évalués dessus | accord avec une référence en partie modèle ; comparaison **entre familles** suspecte |
| R2 | annotation humaine sans assistance d'un modèle parent (assistance documentée) | aucune disponible à ce jour | exactitude de détection/lecture sur cette zone |
| R3 | référence physique indépendante (photo IR de fragment) ou lecture papyrologique publiée | IR fragments (à localiser), lectures First Letters publiées (texte sans coordonnées) | exactitude, sous réserve d'alignement |
| R4 | validation papyrologique aveugle d'une lecture nouvelle | — | découverte confirmée |
Toute métrique publiée porte sa classe. Une référence humaine corrigée avec un modèle est R1, pas R2.

## 3. Contrôles de fuite (avant toute conclusion inter-rouleaux ou toute prédiction sur rouleau cible)
1. Même région physique dans plusieurs jeux (segments chevauchants, autres résolutions du même volume).
2. Modèle dérivé d'un autre (init, distillation) : hériter des parentés du parent.
3. Pseudo-labels produits par un modèle évalué ou de sa famille.
4. Données ayant servi à choisir des hyperparamètres, seuils, checkpoints.
5. Données consultées à répétition pendant la conception des hypothèses (contamination du chercheur).
6. Règles des prix : pas de scan plus résolu du même rouleau ; pas de recouvrement entraînement/prédiction.

## 4. Jeux de test scellés
- Les 5 segments historiques (0841 × 3, 0009B, 0500P2) sont **rétrospectifs** : consultés par 18 expériences, ils
  servent aux comparaisons et au développement de métriques, plus à une validation finale.
- Test scellé (P3) : objets/segments choisis par une règle écrite (diversité : rouleau/fragment, énergie,
  résolution, état), enregistrés par empreinte (`docs/data/sealed_test.md`, liste et sha256 des identifiants) avant
  toute consultation ; ouverts une seule fois par conclusion majeure, ouverture consignée.
- Rouleaux cibles de découverte (R1) : aucun label n'existe ; ils ne servent jamais à un choix de configuration
  avant le gel de la chaîne utilisée pour l'exploration.

## 5. Annotation indépendante (quand aucune référence R2 n'existe)
Protocole d'annotation propre (P4) : annotateur humain identifié, sans affichage de prédictions de la famille
évaluée (images brutes/rendus physiques seulement), consignes écrites, double annotation sur un sous-ensemble,
accord inter-annotateurs rapporté, temps humain compté (≤ 8 h exigé par le Grand Prize pour une soumission). Aucune
vérité terrain fabriquée par un modèle ; l'annotation reste privée si elle révèle du texte (licence).
