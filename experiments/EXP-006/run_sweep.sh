#!/bin/bash
# EXP-006 / H-004 : reader-v2, fenêtre de 17 couches décalée de s ∈ [-6, +5] (défaut s=0 → couches 6..22 sur 28).
# usage : bash run_sweep.sh   (écrit dans $VESRES_WORK/runs/EXP-006/<seg>/pred_s<s>.tif)
W=${VESRES_WORK:-$HOME/vesuvius-work}; cd "$W"
CK=models/domenicor046_reader-v2/reader-v2-step040000.pth
for seg in 20260220213127-w00 20260220214732-auto_grown_20260220144552896 20260221022814-auto_grown_20260220174252405; do
  O=runs/EXP-006/$seg; mkdir -p $O
  for s in -6 -5 -4 -3 -2 -1 0 1 2 3 4 5; do
    [ -f $O/pred_s$s.tif ] && continue
    t=$(date +%s)
    .venv-koine/Scripts/python.exe -m koine_machines.inference.infer cache/segments/PHerc0841/$seg/sv.zarr $CK $O/pred_s$s.tif \
      --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward \
      --layer-start $((6+s)) --layer-end $((23+s)) > $O/s$s.log 2>&1
    echo "$seg s=$s exit=$? wall_s=$(( $(date +%s)-t )) $(grep -o 'indices=\[[0-9, ]*\]' $O/s$s.log | head -1)"
  done
done
echo SWEEP_DONE
