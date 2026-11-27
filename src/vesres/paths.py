"""Racine de travail hors dépôt (données, modèles, runs, venv), configurable par `VESRES_WORK`."""
import os
from pathlib import Path

WORK = Path(os.environ.get("VESRES_WORK", Path.home() / "vesuvius-work"))
