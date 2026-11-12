import json
from pathlib import Path

import numpy as np
import pytest
import tifffile

from vesres import catalog, remote_tiff


def _fake_meta():
    return {"samples": {
        "S1": {"sample": {"properties": {"type": "scroll", "legacy_data_url": ""}},
               "scans": {"a": {"properties": {"pixel_size_um": 2.4, "energy_keV": 78.0},
                               "creation": {"metadata": {"location": "ESRF Grenoble"}}}},
               "volumes": {"v": {"properties": {"license": {"name": "CC BY-NC 4.0"}}, "data": [{"type": "ome-zarr"}]}},
               "segments": {"g": {"data": [{"type": "ink-detection"}, {"type": "layers-zarr"}, {"type": "ink-labels"}]}}},
        "F1": {"sample": {"properties": {"type": "fragment"}}, "scans": {}, "volumes": {}, "segments": {}},
    }}


def test_catalog_summary_and_outputs(tmp_path):
    rows = catalog.summarize(_fake_meta())
    s1 = next(r for r in rows if r["id"] == "S1")
    assert s1["n_segments"] == 1 and s1["n_seg_ink_detection"] == 1 and s1["n_seg_layers"] == 1
    assert s1["best_um"] == 2.4 and "ESRF" in s1["scans"]
    src = tmp_path / "m.json"
    src.write_text(json.dumps(_fake_meta()), encoding="utf-8")
    a, b = tmp_path / "o.csv", tmp_path / "o.md"
    catalog.main(["x", str(src), str(a), str(b), "note"])
    first = (a.read_bytes(), b.read_bytes())
    catalog.main(["x", str(src), str(a), str(b), "note"])
    assert (a.read_bytes(), b.read_bytes()) == first  # déterministe


@pytest.fixture
def local_tiff(tmp_path, monkeypatch):
    arr = (np.arange(37 * 53, dtype=np.uint16).reshape(37, 53) * 7)
    p = tmp_path / "layer.tif"
    tifffile.imwrite(p, arr, rowsperstrip=37)  # non compressé, une strip
    raw = p.read_bytes()

    def fake_range(url, start, end_inclusive, timeout=0):
        return raw[start:end_inclusive + 1]

    monkeypatch.setattr(remote_tiff, "_get_range", fake_range)
    with tifffile.TiffFile(p) as t:
        pg = t.pages[0]
        lay = remote_tiff.TiffLayout("file://x", 37, 53, "uint16", int(pg.dataoffsets[0]), len(raw), None, "e1")
    return arr, lay


def test_read_rows_matches_full_read(local_tiff, tmp_path):
    arr, lay = local_tiff
    np.testing.assert_array_equal(remote_tiff.read_rows(lay, 5, 19, cache=None), arr[5:19])
    np.testing.assert_array_equal(remote_tiff.read_region(lay, 0, 37, 10, 20, cache=None), arr[:, 10:20])


def test_read_rows_cache_roundtrip(local_tiff, tmp_path):
    arr, lay = local_tiff
    a = remote_tiff.read_rows(lay, 3, 9, cache=tmp_path)
    b = remote_tiff.read_rows(lay, 3, 9, cache=tmp_path)  # depuis le cache
    np.testing.assert_array_equal(a, b)
    assert list((tmp_path / "bands").glob("*.npy"))


def test_read_rows_bounds(local_tiff):
    _, lay = local_tiff
    with pytest.raises(ValueError):
        remote_tiff.read_rows(lay, 30, 40, cache=None)
