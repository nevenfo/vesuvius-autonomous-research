# Jeux de test scellés (P3.1, 2026-11-27)

Règle générale (`docs/protocols/independence.md` §4) : choisis par règle écrite **avant** consultation, enregistrés par
empreinte, ouverts une fois par conclusion majeure ; chaque ouverture est consignée ci-dessous.

## T-1667-READ — lecture au niveau texte (référence R3*)
- Source : transcription papyrologique de PHerc. 1667, arXiv:2606.29085 (PDF sha256 `3f8cfecc…`), extraite localement.
- Règle : colonnes dont le numéro est multiple de 3 → **scellées** ; les autres → développement. Fixée avant toute
  lecture du contenu des colonnes (seuls les en-têtes ont été affichés lors de la vérification d'extraction ; la
  colonne 5, de développement, a été affichée partiellement).
- Extraction : Col. 5–22 (Col. 1–4 absentes de l'extraction texte, à vérifier dans le PDF sans consulter de colonne scellée).
- Scellées : Col. 6, 9, 12, 15, 18, 21 — `vesuvius-work/refs/PHerc1667/sealed/cols_sealed.txt`, sha256 `3aed5363190e02ca…`.
- Développement : Col. 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22 — `vesuvius-work/refs/PHerc1667/cols_dev.txt`.
- Privé (texte savant sous licence de diffusion non vérifiée) : jamais copié dans le dépôt.
- **Fuite connue** : PHerc. 1667 est dans l'entraînement d'ink_9um, reader-v2 et reader-v2-LO (`docs/data/provenance.csv`).
  Une lecture évaluée sur T-1667-READ avec ces modèles est optimiste ; une évaluation propre exige un modèle entraîné
  sans 1667 (recette EXP-018 sans 1667, à justifier par V3) ou un modèle dont la parenté exclut 1667.

## T-INK-RETRO — encre au pixel/glyphe (référence R1)
- 0841 × 3, 0009B, 0500P2 : **rétrospectifs** (consultés par EXP-001…022) ; plus une validation finale.
- Aucun objet étiqueté publié n'est à la fois inédit pour nos modèles et non consulté : pas de test scellé d'encre R1/R2
  possible aujourd'hui → dépend de P4 (références R2/R3, IR des fragments).

## Journal des ouvertures
Aucune.
