#!/usr/bin/env bash
# EXP-021 / H-022 — reproduction de Korotetskyi & Haindl 2026 (section 6 : 25 glyphes PHerc. 172, Table 2, fusion).
# À exécuter sous Linux x86_64 (ici WSL Ubuntu, Python 3.12, cc) : le paquet compile des bibliothèques C.
# Le code des auteurs (CC BY-NC 4.0) n'est pas redistribué ici : paquet Zenodo 10.5281/zenodo.24392114
# (code_data_v2.zip, sha256 7db284ab…), décompressé dans $KH/code.
# usage : KH=~/korotetskyi2026 WORKERS=6 bash reproduce_glyphs.sh
set -euo pipefail
KH=${KH:-$HOME/korotetskyi2026}; cd "$KH/code"
UV=${UV:-$HOME/.local/bin/uv}
[ -x .venv/bin/python ] || { "$UV" venv -q --python python3.12 .venv && "$UV" pip install -q --python .venv/bin/python -r requirements-linux.lock.txt; }
# --fresh partiel : résultats fournis mis de côté, recalcul depuis un out/ vide
[ -e out_supplied ] || { mv out out_supplied && mkdir out; }
export PY=.venv/bin/python WORKERS=${WORKERS:-6}
source sections/common.sh
step glyphs_run "$W" glyphs run
step glyphs_analyse 1 glyphs analyse
step tables_per_op 1 tables per_op
"$PY" sections/compare.py out_supplied out | tee logs/compare.txt
