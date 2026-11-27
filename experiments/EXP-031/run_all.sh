#!/bin/bash
# EXP-031 — croissance + fidélité + orientation + rendu + inférence + analyse, graine par graine (README).
# usage : run_all.sh [i_debut] [i_fin]   (indices dans seeds.json, défaut 0..8)
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"
W=${VESRES_WORK:-$HOME/vesuvius-work}
BIN=$W/third_party/vc3d/a7d4f88/x/VC3D-a7d4f88-2026-11-27-win64/bin
S3=https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/PHerc1218
VOL=$S3/volumes/20250521120456-8.640um-1.2m-116keV-masked.zarr/
PRED=$S3/representations/predictions/surfaces/20250521120456-surface-20260413222639-surface-m7-L0-th0.2.zarr
PY=$W/.venv/Scripts/python.exe
PK=$W/.venv-koine/Scripts/python.exe
RUN=$W/runs/EXP-031
AXIS_Y=4252; AXIS_X=3943   # centroïde de la prédiction (EXP-025 seed2.json, niveau 3 × 8)
cd "$RUN"
for i in $(seq "${1:-0}" "${2:-8}"); do
  read -r x y z < <($PY -c "import json;s=json.load(open('seeds.json'))['seeds'][$i];print(s['x'],s['y'],s['z'])")
  P=$RUN/p$i; mkdir -p "$P"
  if [ ! -f "$P/seg/meta.json" ]; then
    s=$(date +%s)
    timeout 1200 "$BIN/vc_grow_seg_from_seed.exe" -v "$VOL" -t "$P" --segment-name seg -p "$R/experiments/EXP-025/params4.json" -s $x $y $z --rng-seed 0 > "$P/grow.log" 2>&1
    echo "grow exit=$? wall=$(( $(date +%s)-s ))" > "$P/grow.meta"
  fi
  [ -f "$P/seg/meta.json" ] || { echo "p$i: pas de surface ($(cat "$P/grow.meta"))"; continue; }
  $PY -I "$R/experiments/EXP-025/fidelity.py" "$P/seg" "$PRED" "$P/fidelity.json" > /dev/null 2>&1
  o=$($PY -I "$R/experiments/EXP-030/orientation.py" "$P/seg" $AXIS_Y $AXIS_X 2>&1 | tail -1)
  echo "$o" > "$P/orientation.txt"
  med=$(echo "$o" | sed -n 's/.*median \(-\?[0-9.]*\).*/\1/p')
  FLIP=""; awk "BEGIN{exit !($med > 0)}" && FLIP="--flip-normals"
  echo "flip=${FLIP:-none}" >> "$P/orientation.txt"
  A=$P/an   # structure attendue par EXP-029/analyze.py : <A>/seg/sv.zarr, <A>/pred_{lo,i9}.tif
  if [ ! -f "$A/pred_i9.tif" ]; then
    "$BIN/vc_render_tifxyz.exe" -v "$VOL" -s "$P/seg" --scale 1 -g 0 -n 31 $FLIP --tif-output "$P/render" --timeout 60 > "$P/render.log" 2>&1
    $PK "$R/experiments/EXP-025/tifs_to_sv.py" "$P/render" "$A/seg" > /dev/null
    for m in "lo:$W/runs/EXP-018/train/ckpt_040000.pth" "i9:$W/models/scrollprize_ink_9um/hybrid_3d2d-seed43/step-060000.pth"; do
      $PK -m koine_machines.inference.infer "$A/seg/sv.zarr" "${m#*:}" "$A/pred_${m%%:*}.tif" --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward > "$P/infer_${m%%:*}.log" 2>&1
    done
  fi
  PYTHONIOENCODING=utf-8 $PK "$R/experiments/EXP-029/analyze.py" "$A" "$P/analysis.json" > /dev/null 2>&1
  echo "p$i done: $(cat "$P/grow.meta") $(tr '\n' ' ' < "$P/orientation.txt")"
done
