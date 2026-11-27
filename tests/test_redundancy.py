import importlib.util
from pathlib import Path

import numpy as np

_p = Path(__file__).resolve().parents[1] / "experiments" / "EXP-027" / "redundancy.py"
_s = importlib.util.spec_from_file_location("redundancy", _p)
R = importlib.util.module_from_spec(_s)
_s.loader.exec_module(R)


def _plane(rows, cols, step=20.0, off=(0.0, 0.0, 0.0), tilt=0.0):
    i, j = np.meshgrid(np.arange(rows), np.arange(cols), indexing="ij")
    X = j * step + off[0]
    Y = i * step + off[1]
    Z = np.full(X.shape, off[2], float) + tilt * X
    return X.astype(np.float32), Y.astype(np.float32), Z.astype(np.float32)


def _flat(X, Y, Z):
    N = R.grid_normals(X, Y, Z)
    ok = R.valid_mask(X, Y, Z) & np.isfinite(N[..., 0])
    idx = np.flatnonzero(ok.reshape(-1))
    return idx, np.stack([X, Y, Z], -1).reshape(-1, 3)[idx].astype(float), N.reshape(-1, 3)[idx]


def test_normals_plane_and_invalid():
    X, Y, Z = _plane(6, 7)
    X[0, 0] = Y[0, 0] = Z[0, 0] = -1
    N = R.grid_normals(X, Y, Z)
    assert np.allclose(np.abs(N[2:-2, 2:-2, 2]), 1.0)
    assert np.isnan(N[0, 0]).all() and np.isnan(N[0, :, 0]).all()  # bord : pas de normale


def test_match_nodes_tolerance_and_normals():
    A = _flat(*_plane(20, 20))
    ia, ib, d = R.match_nodes(A[1], A[2], *_flat(*_plane(20, 20, off=(1.0, 0.0, 0.0)))[1:])
    assert len(ia) == len(A[0]) and np.allclose(d, 1.0)  # décalage 1 voxel <= tol 2
    far = _flat(*_plane(20, 20, off=(5.0, 0.0, 0.0)))
    assert len(R.match_nodes(A[1], A[2], far[1], far[2])[0]) == 0  # > 2 voxels
    tilted = _flat(*_plane(20, 20, tilt=1.0))  # normale à 45 deg : cos ~ 0,71 < 0,9
    assert len(R.match_nodes(A[1], A[2], tilted[1], tilted[2])[0]) == 0
    flip = _flat(*_plane(20, 20, tilt=0.0))
    assert len(R.match_nodes(A[1], A[2], flip[1], -flip[2])[0]) == len(A[0])  # |cos|
    # appariement 1-1 : chaque B une fois
    ia, ib, _ = R.match_nodes(A[1], A[2], A[1][:50], A[2][:50])
    assert len(set(ib.tolist())) == len(ib)


def test_spearman_and_circular_null():
    rng = np.random.default_rng(0)
    g = rng.random((300, 120)).astype(np.float32)
    idx = np.arange(g.size)
    assert abs(R.spearman(g.reshape(-1), g.reshape(-1)) - 1.0) < 1e-9
    assert abs(R.spearman(g.reshape(-1), (g ** 3).reshape(-1)) - 1.0) < 1e-9  # monotone
    null = R.circular_null(g, idx, idx, g, axis=0, min_shift=63)
    assert len(null) == 20 and np.all(np.abs(null) < 0.05) and abs(np.nanmean(null)) < 0.02


def test_classify_and_verdict():
    assert R.classify_pair("w029_xx_flatboi", "w029_yy_flatboi") == "derivee"
    assert R.classify_pair("w011_a_flatboi", "w011_a_merged_v4_flatboi_straightened_v4") == "derivee"
    assert R.classify_pair("w029_x", "w030_y") == "independante"
    assert R.verdict([0.9, 0.8], [0.1, 0.1])["verdict"] == "indeterminee"
    assert R.verdict([0.9, 0.8, 0.7, 0.6, 0.5], [0.1] * 5)["verdict"] == "soutenue"
    assert R.verdict([0.4, 0.3, 0.7], [0.1] * 3)["verdict"] == "refutee"
    assert R.verdict([0.9, 0.9, 0.9], [0.95, 0.95, 0.1])["verdict"] == "refutee"  # < 80 % > nul


def test_node_ink_mapping():
    ds = np.zeros((40, 40), np.uint8)
    ds[:, 20:] = 200  # moitié droite
    v = R.node_ink(ds, (10, 15), 0.05)  # pas 2,5 px : colonnes de nœud 0..14 -> 0..35 px
    assert v.shape == (10, 15) and v[:, 0].max() < 1 and v[:, 14].min() > 190
