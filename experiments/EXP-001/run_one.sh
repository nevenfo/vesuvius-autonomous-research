#!/bin/bash
# usage: run_one.sh <ckpt> <out.tif> <log>
W=${VESRES_WORK:-$HOME/vesuvius-work}; cd "$W"
S=cache/segments/PHerc0841/20260220213127-w00/sv.zarr
( while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits >> "$3.vram"; sleep 2; done ) &
SP=$!
start=$(date +%s)
.venv-koine/Scripts/python.exe -m koine_machines.inference.infer $S "$1" "$2" --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward > "$3" 2>&1
echo "exit=$? wall_s=$(( $(date +%s)-start ))" >> "$3.meta"
kill $SP
