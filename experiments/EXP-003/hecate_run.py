"""E1.4: Hecate 9.6um maps on native 9.366um grid (method of reader-v2 infer_with_hecate.py).
Run with .venv python (cv2, tifffile, zarr); hecate.py is run by .venv-koine python (torch cu128).
Resample: XY cv2.INTER_AREA to round(n*um/9.6), Z linear (zs=(k+.5)/f-.5), uint8 round. Back: cv2.INTER_LINEAR to (W,H).
"""
import os, subprocess, sys, time
import cv2, numpy as np, tifffile, zarr
W0 = 'C:/Users/FlowUP/vesuvius-work'
HD = W0 + '/models/scrollprize_hecate'
KPY = W0 + '/.venv-koine/Scripts/python.exe'
UM = 9.366

def resample_96(vol, um):
    f = um / 9.6
    nz, ny, nx = vol.shape
    oy, ox, oz = int(round(ny * f)), int(round(nx * f)), int(round(nz * f))
    xy = np.stack([cv2.resize(np.asarray(vol[k]), (ox, oy), interpolation=cv2.INTER_AREA) for k in range(nz)])
    zs = (np.arange(oz) + 0.5) / f - 0.5
    z0 = np.clip(np.floor(zs).astype(int), 0, nz - 1); z1 = np.clip(z0 + 1, 0, nz - 1); w = np.clip(zs - z0, 0, 1)
    return np.stack([np.round((1 - w[k]) * xy[z0[k]] + w[k] * xy[z1[k]]).astype(np.uint8) for k in range(oz)])

seg = sys.argv[1]
d = f'{W0}/runs/E1.4/{seg}'; os.makedirs(d, exist_ok=True)
root = zarr.open(f'{W0}/cache/segments/PHerc0841/{seg}/sv.zarr', mode='r')
vol = root['0']
H, W = vol.shape[1:]
t = time.time()
v96 = resample_96(vol, UM)
print(seg, 'native', vol.shape, '-> 9.6', v96.shape, flush=True)
npy, png = d + '/sv96.npy', d + '/hecate96.png'
np.save(npy, v96)
subprocess.run([KPY, HD + '/hecate.py', '--checkpoint', HD + '/hecate_9.6um.pth', '--input', npy, '--spacing-um', '9.6',
                '--output', png, '--precision', 'bf16', '--batch-size', '8'], check=True)
h = cv2.imread(png, cv2.IMREAD_UNCHANGED)
h = (h[..., 0] if h.ndim == 3 else h).astype(np.float32)
h = cv2.resize(h, (W, H), interpolation=cv2.INTER_LINEAR)
out = np.round(h).clip(0, 255).astype(np.uint8)
assert out.shape == (H, W)
tifffile.imwrite(d + '/pred_hecate.tif', out, tile=(128, 128), compression='zlib')
print('done', out.shape, f'{time.time()-t:.1f}s')
