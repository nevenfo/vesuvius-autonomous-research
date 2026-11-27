# Boucle de recherche autonome, sélection, arrêt et continuité (2026-11-27)

Remplace la règle fixe « 3 essais sans gain → audit » (F1.1) par une règle proportionnée.

## 1. Cycle
1 veille depuis la dernière décision (`watch/reports/`, recherche ciblée si l'expérience est coûteuse) →
2 relire résultats → 3 identifier l'obstacle principal (`docs/research-review-*.md` §4) → 4 solutions existantes ? →
5 ≥ 2 hypothèses concurrentes → 6 comparer intérêt/coût → 7 choisir la plus informative → 8 critères de réussite,
réfutation, arrêt, ressources max **écrits avant** → 9 exécuter → 10 mesurer → 11 erreurs et incertitudes →
12 reproduire si important → 13 conserver/améliorer/abandonner/suspendre → 14 mettre à jour hypothèses, plan,
registre, progress → 15 prochaine action.

## 2. Questions obligatoires avant une expérience importante (README de l'EXP)
Obstacle visé et pourquoi prioritaire · preuves en faveur · solution communautaire existante ? · gain de lecture
attendu et comment le vérifier · connaissance obtenue même en échec · coût (h GPU/CPU, Go, temps humain) ·
expérience moins chère pour la même question ? · risques de circularité/fuite/biais (`independence.md`) · autres
pistes à meilleur bénéfice ? · ce qui justifie de continuer ou d'arrêter · « veille consultée : <date>, impact ».
Pas de score universel : l'argumentation écrite est la trace reproductible.

## 3. Échecs, audit, abandon
- Attribuer l'échec : hypothèse, protocole, données, modèle, résolution, implémentation, métrique, matériel ou
  puissance statistique ; un échec non attribué n'est pas une réfutation.
- Audit de protocole/métrique déclenché quand le coût cumulé des essais sans progrès sur un même obstacle dépasse
  ≈ 1 jour-machine **ou** 3 essais peu coûteux, selon le premier atteint, ou dès qu'un contrôle positif échoue.
- Abandon/suspension sur preuve ; résultat négatif consigné avec ses limites ; pas de répétition sans information
  nouvelle ; réouverture quand une découverte change une hypothèse sous-jacente (noter laquelle).
- Ne pas s'acharner pour coût englouti ; ne pas abandonner une piste après un seul essai mal contrôlé.

## 4. Ressources (relevé 2026-11-27)
PC : RTX 5080 16 Go, 31 Go RAM, 16 threads, C: ≈ 229 Gio libres (baisse depuis 442 Gio le 2026-11-12 ; travail
`vesuvius-work` ≈ 98 Gio) ; NAS `Y:` ≈ 202 Gio libres. Règles : VRAM ≤ ~12 Go, pas de job CPU lourd (WSL inclus)
pendant un entraînement (débit ÷ 5 mesuré), calculs interruptibles avec reprise, aucune dépense externe autonome.
Budget cache local ≤ 150 Go (à réviser : travail actuel ≈ 98 Gio, espace libre en baisse → nettoyage du cache
reproductible avant tout téléchargement > 20 Go).

## 5. Artefacts, sauvegarde et reprise
| Classe | Exemples | Où | Sauvegarde |
|---|---|---|---|
| Code, protocoles, résultats agrégés publiables | `src/`, `docs/`, `experiments/*/results.json` | Git → GitHub | historique Git (durable) |
| Cache reproductible | segments téléchargés, prédictions recalculables | `vesuvius-work/cache`, `runs/` | aucune (régénérable, manifeste suffit) |
| Artefacts uniques coûteux | checkpoints EXP-018 (≈ 2–4 h GPU), sorties privées par UGR, futures zones candidates | `vesuvius-work/runs/` (PC) | **copie sur le NAS** + manifeste sha256 ; le NAS seul n'est pas une sauvegarde indépendante des originaux qui y résident |
| Preuves privées (images d'encre, coordonnées de texte) | dossiers R1 | PC + NAS, hors Git | jamais publiées sans accord écrit (licence) |
Chaque EXP longue écrit : configuration, commit, données, checkpoints valides, résultats partiels, prochaine étape
(dans son README) ; reprise par checkpoint ; journaux bruts hors du contexte permanent.

## 6. Créativité et exploration (intégré le 2026-11-27)
Le plan n'est pas une frontière intellectuelle. À chaque cycle (étapes 3–5 du §1), en plus des hypothèses issues des
obstacles :
- **Audit d'hypothèses implicites** : quelle croyance non testée limite la recherche (ex. « il faut aplatir avant de
  lire », « le masque officiel contient tout le papyrus », « l'accord de modèles signifie quelque chose ») ?
- **Anomalies → opportunités** : tout résultat inattendu (échec, écart, contradiction) reçoit une idée ou une hypothèse.
- **Suppression d'étape** : quelle étape de la chaîne pourrait être supprimée plutôt qu'optimisée ?
- **Transfert interdisciplinaire** : méthode d'un autre domaine, avec vérification écrite de la compatibilité de ses
  hypothèses physiques/mathématiques avec des papyrus carbonisés (encre carbonée quasi iso-atténuante, relief de
  quelques µm, compression, voxels 2,4–9 µm).

**Cycle de vie et statuts** (registre unique `docs/hypotheses.md`, section « Idées exploratoires ») :
`idée exploratoire (I-NNN)` → `hypothèse (H-NNN, critères écrits)` → `faisabilité démontrée` → `résultat expérimental`
→ `résultat reproduit` → `méthode validée` ; ou `suspendue` / `abandonnée` avec raison et condition de réexamen.
Fiche minimale d'une idée : problème visé, principe, différence avec l'existant (veille), hypothèses nécessaires,
potentiel pour la lecture, risques/coûts, **expérience minimale discriminante**, critères de réussite/réfutation.

**Équilibre exploration / exploitation** : pas de quota. À chaque revue, justifier par écrit la part d'effort : plus
d'exploration quand l'exploitation plafonne (essais sans progrès, obstacle sans solution connue) ou qu'une idée a un
fort potentiel pour une expérience courte ; plus d'exploitation quand une piste produit des gains mesurés. Préférer
les expériences courtes et discriminantes ; une idée originale n'est pas une bonne idée par défaut, une idée
improbable n'est pas mauvaise par défaut.

**Garde-fou génératif** : toute méthode générative (diffusion, restauration, modèle de langue) produit au mieux des
statuts `Probable`/`Restitué` ; aucune lecture n'est revendiquée sans traçabilité vers des observations physiques
indépendantes ; contrôles obligatoires sur fond vierge, entrées permutées et données synthétiques à vérité connue.
