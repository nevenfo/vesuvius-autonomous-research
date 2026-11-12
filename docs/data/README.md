# Données — accès, licences, cibles d'évaluation

## Accès
- Catalogue officiel : `https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/metadata.min.json`
  (servi gzip ; schéma `metadata.schema.json`). Arborescence `{ID}/volumes|segments/…`, S3 anonyme.
- Legacy : `https://dl.ash2txt.org/` (`full-scrolls/Scroll1..5`, `fragments/Frag1..6`, `datasets/`, `ml-models/`).
  TIFF de couches uint16 non compressés à une strip → bandes lisibles par HTTP Range (`vesres.remote_tiff`).
- Régénérer l'inventaire : `PYTHONPATH=src python -m vesres.catalog <metadata.min.json> docs/data/corpus_inventory.csv docs/data/corpus_inventory.md "<note source>"`.

## Licences (à respecter strictement)
- Volumes récents : CC BY-NC 4.0. Scrolls 1-4 / Frag 1-6 (DLS 2023) : EduceLab Data License + citation
  Parsons et al. 2023 (arXiv:2304.02084).
- `dl.ash2txt.org/LICENSE.txt` : pas de publication hors Discord officiel de révélations de texte (transcriptions,
  images d'encre, labels) sans accord écrit ; pas de redistribution. → images d'encre jamais dans Git.

## Segments portant des `ink-labels` (catalogue du 2026-11-05)
| Rouleau | Segments | Résolutions de layers | Labels |
|---|---|---|---|
| PHerc0139 | w030, w035, w039, w040, w041, w043, w044, w045 | 1,129 / 2,399 / 9,362 µm | 2,399 µm (+ 9,362 µm pour w035/w039/w040/w041/w044) |
| PHerc0841 | w00, 2 auto_grown | 2,403 / 9,366 µm | 2,403 µm |
| PHerc0814 | 46527_2um_try2 | 1,129 / 2,399 / 9,362 µm | 2,399 µm |
| PHerc1667 | w013, w018, w023, w028, w029, w031 | 1,129 / 2,399 µm | 2,399 µm |
| PHercParis4 | 8 segments 2023 | 2,4 / 45,5 (/1,129) µm | 2,4 µm |
| PHerc0500P2 (fragment) | 20250825181859--1 | 2,215 / 4,317 / 9,362 µm | 2,215 µm |
| PHerc0009B (fragment) | auto_grown_…_inp_hr | 2,401 / 8,64 µm | 2,401 µm |

Fragment DLS avec label IR humain : Frag1 `PHercParis2Fr47` (`working/54keV_exposed_surface/`, 65 couches × 98,8 Mio, `inklabels.png`, `mask.png`).

## Parentés connues (fuites potentielles)
- `scrollprize/ink_9um` entraîné sur 0139, 1667, Paris4, 0814 → ne pas l'évaluer comme « zéro-shot » sur ces rouleaux.
- reader-v2 déclare PHerc0841 non vu (**A**) ; données exactes d'entraînement à vérifier (B1.2).
- Labels de rouleaux = pseudo-labels itératifs issus de modèles (README ink-labels) → circularité possible.
