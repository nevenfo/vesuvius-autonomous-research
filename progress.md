# PROGRESS

## Phase actuelle
Phase D — premier chemin vertical (A, B1.1, B2.1-2, B3, C1.1, C2.1 faits).

## Tâche actuelle
A2.2 — remote GitHub privé, puis D1.1.

## Dernière tâche validée
C2.1 — lecture par région de couches TIFF distantes.
Validation :
- `python -m pytest -q` → 4 passed (2026-11-12).
- Crop réel Frag1 `surface_volume/32.tif` (8181×6330 uint16) lu par HTTP Range : 64×64, sans téléchargement complet.
- Inventaire régénérable : 45 échantillons (35 rouleaux, 10 fragments), `docs/data/corpus_inventory.md`.

## Décisions actives
- Dépôt sur le NAS (`Y:\VESUVIUS AUTONOMOUS RESEARCH`) ; venv + cache sur `C:\Users\FlowUP\vesuvius-work` (hors Git).
- Python natif Windows 3.12 + torch 2.11.0+cu128 (sm_120 OK) ; WSL Ubuntu (GPU OK) en repli pour outils Linux (VC3D…).
- Pas d'orchestrateur propre : boucle autonome = Claude Code + `experiments/` + `docs/hypotheses.md`.
- Premier chemin vertical = H-001 : reader-v2 (MIT) zéro-shot sur PHerc0841 (9,366 µm) vs ink-labels 2,403 µm.
- Veille : script déterministe + tâche planifiée Windows utilisateur (G1/G2), analyse par Claude.
- Licence données : aucune image d'encre/transcription publiée ; `.gitignore` les exclut.

## Blocage actif
Aucun.

## Fichiers / zones utiles
- `src/vesres/remote_tiff.py`, `src/vesres/catalog.py`, `tests/test_core.py`
- `docs/state-of-the-art/2026-11-12.md`, `docs/data/README.md`, `docs/hypotheses.md`
- Catalogue local : `C:\Users\FlowUP\vesuvius-work\cache\catalog\metadata.min.json`

## NEXT ACTION
A2.2 — Créer le dépôt GitHub privé `nevenfo/vesuvius-autonomous-research`, pousser `main`, vérifier visibilité PRIVATE.
