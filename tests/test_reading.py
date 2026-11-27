import numpy as np

from vesres import reading


def _scene(seed=0):
    rng = np.random.default_rng(seed)
    h, w = 300, 400
    ink = np.zeros((h, w), bool)
    for y, x in ((60, 60), (60, 200), (200, 120), (200, 300)):
        ink[y:y + 30, x:x + 8] = True  # trait vertical
        ink[y:y + 8, x:x + 30] = True  # trait horizontal
    valid = np.ones((h, w), bool)
    sup = np.zeros((h, w), bool)
    sup[:, :350] = True
    val = np.ones((h, w), bool)
    return rng, ink, valid, sup, val


def test_reference_units_and_controls():
    rng, ink, valid, sup, val = _scene()
    lab, units = reading.reference_units(ink, valid, sup, min_px=50)
    assert len(units) == 4
    pos = reading.positive_control(ink)
    recs = reading.unit_legibility(pos, lab, units, ink, valid & sup, ring_px=12)
    assert reading.legible_fraction(recs, 0.9) == 1.0
    noise = rng.random(ink.shape).astype(np.float32)
    recs_n = reading.unit_legibility(noise, lab, units, ink, valid & sup, ring_px=12)
    assert all(0.35 < r["local_auc"] < 0.65 for r in recs_n)


def test_unit_outside_supervision_excluded():
    _, ink, valid, sup, _ = _scene()
    sup[:, 280:] = False  # la 4e unité (x 300..330) sort de la supervision
    _, units = reading.reference_units(ink, valid, sup, min_px=50)
    assert len(units) == 3


def test_background_candidates_counts_false_glyph():
    _, ink, valid, sup, _ = _scene()
    pred = reading.positive_control(ink, noise=0.0)
    pred[250:280, 20:50] = 1.0  # faux glyphe loin de l'encre
    r = reading.background_candidates(pred, ink, valid & sup, thr=0.5, area_range=(100, 5000), margin_px=10)
    assert r["n_candidates"] == 1


def test_dilate_matches_disk_structure():
    from scipy import ndimage as ndi

    rng = np.random.default_rng(1)
    m = rng.random((80, 90)) > 0.995
    r = 6
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    ref = ndi.binary_dilation(m, structure=(x * x + y * y <= r * r))
    assert np.array_equal(reading.dilate(m, r), ref)


def test_coverage_partitions_segment():
    _, ink, valid, sup, val = _scene()
    val[:, 380:] = False
    c = reading.coverage(valid, sup, val, px_um=10.0)
    tot = c["reliable_reference_cm2"] + c["reviewed_unreliable_cm2"] + c["unreviewed_cm2"]
    assert abs(tot - c["segment_cm2"]) < 1e-3
    assert c["unreviewed_cm2"] > 0
