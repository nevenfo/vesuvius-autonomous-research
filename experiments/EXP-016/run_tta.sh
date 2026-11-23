#!/bin/bash
# EXP-016 : reader-v2 + --tta-mirror (options EXP-015) sur 0009B et 0500P2
cd /c/Users/FlowUP/vesuvius-work
CK=models/domenicor046_reader-v2/reader-v2-step040000.pth
for OS in PHerc0009B/20250919125754-auto_grown_20250919055754487_inp_hr PHerc0500P2/20250825181859--1; do
  SEG=${OS#*/}; O=runs/EXP-016/$SEG; mkdir -p $O
  start=$(date +%s)
  .venv-koine/Scripts/python.exe -m koine_machines.inference.infer cache/segments/$OS/sv.zarr $CK $O/pred_reader-v2_tta.tif \
    --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward --tta-mirror --tta-batch-size 2 > $O/tta.log 2>&1
  echo "$SEG exit=$? wall_s=$(( $(date +%s)-start ))" >> runs/EXP-016/meta.txt
done
