"""EXP-018 — lanceur reprenable de l'entraînement reader-v2-LO (inspiré du watchdog de reader-v2 `v2_run.py train`).

Usage : <python venv-koine> experiments/EXP-018/run_train.py <train_config.json>
Relance `koine_machines.training.train` jusqu'à ce que ckpt_040000.pth existe (≤ 6 relances) ; chaque relance reprend
l'état complet du dernier `ckpt_*.pth` (`weights_only: false`). Journal : <out_dir>/train_<n>.log, état : <out_dir>/runner.log.
"""
import glob, json, os, subprocess, sys, time
from pathlib import Path

W = os.environ.get('VESRES_WORK', str(Path.home() / 'vesuvius-work')).replace('\\', '/')
ENV = dict(os.environ, WANDB_MODE='disabled', PYTHONIOENCODING='utf-8',
           PYTHONPATH=os.pathsep.join([f'{W}/third_party/villa/ink-detection', f'{W}/third_party/villa/vesuvius/src']))
cfg_path = sys.argv[1]
base = json.load(open(cfg_path, encoding='utf-8'))
out = base['out_dir']
os.makedirs(out, exist_ok=True)
final = os.path.join(out, f"ckpt_{base['num_iterations']:06d}.pth")
log = lambda m: open(os.path.join(out, 'runner.log'), 'a', encoding='utf-8').write(time.strftime('%F %T ') + m + '\n')
for n in range(7):
    if os.path.exists(final):
        log('DONE ' + final)
        break
    cks = sorted(glob.glob(os.path.join(out, 'ckpt_*.pth')))
    cfg, path = dict(base), cfg_path
    if cks:
        cfg['checkpoint'] = cks[-1].replace(os.sep, '/')
        cfg['weights_only'] = False
        path = os.path.join(out, 'train_config_resume.json')
        json.dump(cfg, open(path, 'w'), indent=1)
    log(f'launch {n} from {cfg["checkpoint"]}')
    rc = subprocess.run([sys.executable, '-u', '-m', 'koine_machines.training.train', path], cwd=W, env=ENV,
                        stdout=open(os.path.join(out, f'train_{n}.log'), 'w'), stderr=subprocess.STDOUT).returncode
    log(f'exit {n} rc={rc}')
    time.sleep(30)
else:
    log('GAVE UP')
