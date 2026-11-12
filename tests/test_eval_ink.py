import numpy as np
from sklearn.metrics import roc_auc_score

from vesres import eval_ink


def test_auc_exact_matches_sklearn_with_ties():
    rng = np.random.default_rng(1)
    pos = rng.integers(0, 20, 500).astype(float) + 3
    neg = rng.integers(0, 20, 700).astype(float)
    y = np.r_[np.ones(500), np.zeros(700)]
    assert abs(eval_ink.auc_exact(pos, neg) - roc_auc_score(y, np.r_[pos, neg])) < 1e-12


def test_mask_on_canvas_area_threshold():
    a = np.zeros((40, 40), np.uint8)
    a[:20, :] = 255
    m = eval_ink.mask_on_canvas(a, (10, 10))
    assert m[:5].all() and not m[5:].any()


def test_evaluate_perfect_and_random():
    rng = np.random.default_rng(0)
    h, w = 1024, 1024
    ink = np.zeros((h, w), bool)
    ink[::8, :] = True
    ink[1::8, :] = True
    masks = {"valid": np.ones((h, w), bool), "inklabels": ink,
             "supervision": np.ones((h, w), bool), "validation": np.zeros((h, w), bool)}
    perfect = eval_ink.evaluate(ink.astype(np.float32), masks)
    assert perfect["reviewed"]["auc_exact"] == 1.0 and perfect["reviewed"]["ap"] == 1.0
    rnd = eval_ink.evaluate(rng.random((h, w)).astype(np.float32), masks)
    assert abs(rnd["reviewed"]["auc_exact"] - 0.5) < 0.02
    lo, hi = rnd["reviewed"]["bootstrap"]["ci95"]
    assert lo < 0.5 < hi
