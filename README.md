# VESUVIUS AUTONOMOUS RESEARCH

Open, largely autonomous research towards the complete and verifiable virtual reading of the carbonised
Herculaneum scrolls of the [Vesuvius Challenge](https://scrollprize.org). The project reuses the state of the
art first (`ScrollPrize/villa`, published models) and only innovates where a measured need is shown.
Internal working documents (plan, progress, experiment reports) are written in French; this page is the
English entry point.

## What is here
- **Plan and state**: [`plan.md`](plan.md) (goal, invariants, phases with stable IDs) · [`progress.md`](progress.md)
  (current snapshot and single next action).
- **Hypotheses**: [`docs/hypotheses.md`](docs/hypotheses.md) — each with a test, a refutation criterion and a status.
- **Experiments**: [`experiments/registry.csv`](experiments/registry.csv) and `experiments/EXP-NNN/` (scripts,
  metrics, README with positive *and* negative results). Ink maps themselves are never published (data licence).
- **Protocols**: [`docs/protocols/`](docs/protocols/), data and splits [`docs/data/`](docs/data/), dated state of
  the art [`docs/state-of-the-art/`](docs/state-of-the-art/), compliance [`docs/compliance/`](docs/compliance/).
- **Library**: `src/vesres/` — segment fetching, ink evaluation (`eval_ink`: AUC/AP on the `supervision` region
  with block-bootstrap confidence intervals), literature/repository watch.

## Results so far (9 µm ink detection, held-out PHerc. 0841 segments)
- Official inference (`koine_machines`, reader-v2) and Hecate reproduce their published numbers (EXP-001, EXP-003).
- A mean fusion of reader-v2 and Hecate is the current reference chain (EXP-003/004/011: AP +0.023 over the
  best single model, CI not fully above zero).
- Negative results: calibration, calibrated fusion, border handling (EXP-012…014) and test-time mirroring
  inside the fusion (EXP-016) bring no robust gain; several hypotheses (H-002, H-004, H-006, H-007) are refuted.
- Official 2.4 µm predictions score higher but are only indicative comparators (possible label circularity, EXP-017).
- In progress: reader-v2 retrained without the test objects (EXP-018, H-017); reproduction of the training-free
  3-D texture method of Korotetskyi & Haindl 2026 (EXP-021, H-022).

## Environment
The working tree (data cache, models, runs, virtual environments) lives outside the repository, under
`VESRES_WORK` (default `~/vesuvius-work`):

```bash
uv venv --python 3.12 $VESRES_WORK/.venv
uv pip install --python $VESRES_WORK/.venv/Scripts/python.exe torch torchvision --index-url https://download.pytorch.org/whl/cu128
uv pip install --python $VESRES_WORK/.venv/Scripts/python.exe -r requirements.lock
$VESRES_WORK/.venv/Scripts/python.exe -m pytest -q
```

Evictable cache: `VESRES_CACHE` (default `~/vesuvius-work/cache`).

## Licences and citations
Original code: MIT ([`LICENSE`](LICENSE)). Vesuvius Challenge data: CC BY-NC 4.0 / EduceLab Data License,
**not redistributed here**; no ink image or transcription derived from these data is published without the
agreement of Vesuvius Challenge (see `docs/data/README.md`). Third-party code (e.g. Korotetskyi & Haindl 2026,
CC BY-NC 4.0) is used from its original archive and never copied into this repository.
Data used: EduceLab-Scrolls (Parsons et al., 2023, arXiv:2304.02084).

---

*Français* — Recherche ouverte visant la lecture virtuelle intégrale et vérifiable des rouleaux du Vesuvius
Challenge ; documents de travail (plan, progression, rapports d'expérience) en français, voir les liens ci-dessus.
