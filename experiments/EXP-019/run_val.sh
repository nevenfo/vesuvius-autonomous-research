#!/bin/bash
# EXP-019 (K3.2) : inférence de checkpoints EXP-018 sur les 4 segments de validation K (holdouts reader-v2).
# Usage : bash experiments/EXP-019/run_val.sh <run_dir> <step> [<step>...]   (ex. runs/EXP-018/train 5000 10000)
# Options d'inférence identiques à EXP-018/run_eval.sh (EXP-001). Temps par segment journalisé (coût K).
cd /c/Users/FlowUP/vesuvius-work
RUN=$1; shift
for STEP in "$@"; do
  CK=$RUN/ckpt_$(printf %06d $STEP).pth
  [ -f $CK ] || { echo "absent : $CK"; continue; }
  for OS in 0343P/20250904233748-0_b2 0343P/20250905172054-1_b2 \
            0172/20250926122938-w082_20250926122938619_fl 0172/20250926132117-w083_20250926132117595_fl; do
    SEG=${OS#*/}; O=runs/EXP-019/$SEG; mkdir -p $O
    [ -f $O/pred_$STEP.tif ] && continue
    T0=$(date +%s)
    .venv-koine/Scripts/python.exe -m koine_machines.inference.infer data/v2lo_val/$OS/sv.zarr $CK $O/pred_$STEP.tif.part.tif \
      --overlap 0.5 --blend-mode hann --batch-size 8 --no-compile --direction forward > $O/$STEP.log 2>&1
    RC=$?
    [ $RC -eq 0 ] && mv $O/pred_$STEP.tif.part.tif $O/pred_$STEP.tif
    echo "$SEG $STEP exit=$RC sec=$(( $(date +%s) - T0 ))" >> runs/EXP-019/meta.txt
  done
done
