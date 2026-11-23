#!/bin/bash
# EXP-018 : inférence reader-v2-LO (checkpoint $1, étiquette $2) sur les 5 segments étiquetés, options d'EXP-001.
cd /c/Users/FlowUP/vesuvius-work
CK=$1; TAG=${2:-lo}
for OS in PHerc0841/20260220213127-w00 PHerc0841/20260220214732-auto_grown_20260220144552896 \
          PHerc0841/20260221022814-auto_grown_20260220174252405 \
          PHerc0009B/20250919125754-auto_grown_20250919055754487_inp_hr PHerc0500P2/20250825181859--1; do
  SEG=${OS#*/}; O=runs/EXP-018/eval/$SEG; mkdir -p $O
  [ -f $O/pred_$TAG.tif ] && continue
  .venv-koine/Scripts/python.exe -m koine_machines.inference.infer cache/segments/$OS/sv.zarr $CK $O/pred_$TAG.tif \
    --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward > $O/$TAG.log 2>&1
  echo "$SEG $TAG exit=$?" >> runs/EXP-018/eval/meta.txt
done
