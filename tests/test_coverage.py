import math

import numpy as np
import pytest

from vesres import coverage as cv


def _spiral_image(n=1600, pitch_px=10.0, noise=0.15, seed=0):
    yy, xx = np.mgrid[:n, :n].astype(float)
    cy = cx = n / 2
    r = np.hypot(yy - cy, xx - cx)
    th = np.arctan2(yy - cy, xx - cx)
    img = 130 + 70 * np.cos(2 * math.pi * r / pitch_px - th)  # spirale d'Archimède : pas radial = pitch_px
    img += np.random.default_rng(seed).normal(0, noise * 70, img.shape)
    img = np.clip(img, 1, 255)
    img[r > n / 2 - 5] = 0
    return img.astype(np.uint8), cy, cx


@pytest.mark.parametrize("pitch_um", [160.0, 300.0, 450.0])
def test_estimate_pitch_spiral(pitch_um):
    px_um = 30.0
    img, cy, cx = _spiral_image(pitch_px=pitch_um / px_um)
    patch = img[int(cy) - 64:int(cy) + 64, int(cx):]
    prof = cv.band_profile(patch)
    assert prof is not None
    est = cv.estimate_pitch(prof, px_um)
    assert est is not None and abs(est - pitch_um) / pitch_um < 0.10


def test_estimate_pitch_rejects_noise():
    rng = np.random.default_rng(1)
    assert cv.estimate_pitch(rng.normal(size=400), 30.0, min_corr=0.5) is None


def test_surface_cylinder():
    R, H, v, pitch = 40, 30, 50.0, 250.0
    yy, xx = np.mgrid[:101, :101]
    disk = (np.hypot(yy - 50, xx - 50) <= R).astype(np.uint8)
    vol = np.stack([disk] * H)
    vol[:, 45:55, 45:55] = 0  # trou central : doit être rempli
    areas = cv.envelope_areas(vol)
    assert cv.height_extent(areas) == (0, H - 1)
    s = cv.surface_cm2(areas, v, pitch)
    expected = math.pi * (R * v) ** 2 / pitch * (H * v) / 1e8  # longueur de spirale πR²/pas × hauteur
    assert abs(s - expected) / expected < 0.02


def test_inventory_row_and_verdict():
    areas = np.full(20, 1000.0)
    row = cv.inventory_row("X", "v", 8.0, 2, 1, 0, 10.0, 12.0, [200, 210, 220, 190, 205, 215, 200], areas, 256.0)
    assert row["statut"] == "estimée" and row["ratio_bas"] <= row["ratio_median"] <= row["ratio_haut"]
    short = cv.inventory_row("Y", "v", 8.0, 0, 0, 0, 0.0, 1.0, [200, 210], areas, 256.0)
    assert short["statut"] == "inconnue" and "bandes" in short["raison"]
    assert cv.verdict([row, short])["n_estimes"] == 1
