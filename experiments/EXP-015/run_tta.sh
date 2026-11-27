#!/bin/bash
# EXP-015 : reader-v2 + --tta-mirror (sinon options identiques à EXP-001) sur 0841 × 3
W=${VESRES_WORK:-$HOME/vesuvius-work}; cd "$W"
CK=models/domenicor046_reader-v2/reader-v2-step040000.pth
for SEG in 20260220213127-w00 20260220214732-auto_grown_20260220144552896 20260221022814-auto_grown_20260220174252405; do
  O=runs/EXP-015/$SEG; mkdir -p $O
  start=$(date +%s)
  .venv-koine/Scripts/python.exe -m koine_machines.inference.infer cache/segments/PHerc0841/$SEG/sv.zarr $CK $O/pred_reader-v2_tta.tif \
    --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward --tta-mirror --tta-batch-size 2 > $O/tta.log 2>&1
  echo "$SEG exit=$? wall_s=$(( $(date +%s)-start ))" >> runs/EXP-015/meta.txt
done
