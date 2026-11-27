"""EXP-030 — règle d'orientation sans label d'un tifxyz : signe de cross(du, dv) (normale de la grille) par rapport à la
direction radiale sortante depuis l'axe approximatif du rouleau (cy, cx en voxels niveau 0).

Usage : python orientation.py <tifxyz_dir> <cy> <cx>
Règle (EXP-030, 3/3 segments publiés PHerc0841) : normale sortante (médiane > 0) → `vc_render_tifxyz --flip-normals`
pour retrouver l'ordre des couches des surface-volumes publiés.
"""
import sys,tifffile,numpy as np
d=sys.argv[1]; cy,cx=float(sys.argv[2]),float(sys.argv[3])
x,y,z=(tifffile.imread(f'{d}/{c}.tif').astype(np.float64) for c in 'xyz')
P=np.stack([x,y,z],-1); ok=(x>0)
du=np.gradient(P,axis=1); dv=np.gradient(P,axis=0)
n=np.cross(du,dv); n/=np.linalg.norm(n,axis=-1,keepdims=True)+1e-9
r=np.stack([x-cx,y-cy,np.zeros_like(x)],-1); r/=np.linalg.norm(r,axis=-1,keepdims=True)+1e-9
dot=(n*r).sum(-1)[ok&np.isfinite((n*r).sum(-1))]
print(d.split('/')[-2], 'cross(du,dv).radial_out: median',round(float(np.median(dot)),3),'frac>0',round(float((dot>0).mean()),3))
