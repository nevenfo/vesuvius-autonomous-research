"""EXP-024 — tri des rouleaux First Letters par surface publiée et signal reader-v3 officiel (référence R0).

Usage : python experiments/EXP-024/triage.py <metadata.min.json> <work_dir> <out.json>
Télécharge les prédictions reader-v3 officielles (≈ 1 Mo/segment) dans <work_dir>/runs/EXP-024/ (privé).
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
import tifffile
from scipy import ndimage as ndi

BASE = "https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/"
ELIGIBLE = ["PHerc0125", "PHerc0175A", "PHerc0175B", "PHerc0191", "PHerc0257", "PHerc0268", "PHerc0358", "PHerc0483A",
            "PHerc0483B", "PHerc0490A", "PHerc0490B", "PHerc0800", "PHerc0813", "PHerc0826", "PHerc1203", "PHerc1218",
            "PHerc1545"]
WINNERS = ["PHerc0306B", "PHerc0343", "PHerc0846A", "PHerc0846B", "PHerc0211"]


def seg_stats(a: np.ndarray, px_um: float) -> dict:
    a = a.astype(np.float32) / (65535 if a.dtype == np.uint16 else 255)
    valid = a > 0
    c = (px_um * 1e-4) ** 2
    cm2 = float(valid.sum()) * c
    lab, n = ndi.label(a >= 0.5)
    dens = None
    if n:
        area_mm2 = ndi.sum(np.ones_like(lab, dtype=np.float64), lab, np.arange(1, n + 1)) * (px_um * 1e-3) ** 2
        k = int(np.sum((area_mm2 >= 0.5) & (area_mm2 <= 15)))
    else:
        k = 0
    if cm2 > 0:
        dens = k / cm2
    return {"valid_cm2": round(cm2, 3), "frac_gt05": round(float((a[valid] >= 0.5).mean()), 4) if valid.any() else None,
            "glyph_blobs": k, "glyph_blobs_per_cm2": round(dens, 3) if dens is not None else None}


def main(meta_path: Path, work: Path, out: Path) -> None:
    samples = json.loads(meta_path.read_text(encoding="utf-8"))["samples"]
    res = {}
    for sid in ELIGIBLE + WINNERS:
        s = samples.get(sid)
        if s is None:
            res[sid] = {"status": "absent du catalogue"}
            continue
        px = {vid: v["properties"].get("pixel_size_um") for vid, v in (s.get("volumes") or {}).items()}
        segs = []
        for gid, g in (s.get("segments") or {}).items():
            rv3 = [d for d in g["data"] if d["type"] == "ink-detection" and "reader-v3" in d["origins"][0]["path"]]
            if not rv3:
                continue
            path = rv3[0]["origins"][0]["path"]
            m = re.search(r"-(\d+(?:\.\d+)?)um-", path.rsplit("/", 1)[-1])
            um = next((p for k, p in px.items() if k in path and p), None) or (float(m.group(1)) if m else None)
            if um is None:
                continue
            dst = work / "runs" / "EXP-024" / sid / f"{gid}_reader-v3.tif"
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                tmp = dst.with_suffix(".part")
                urllib.request.urlretrieve(BASE + path, tmp)
                os.replace(tmp, dst)
            st = seg_stats(tifffile.imread(dst).squeeze(), float(um))
            segs.append({"segment": gid, "px_um": um, **st})
        big = [x["glyph_blobs_per_cm2"] for x in segs if x["valid_cm2"] >= 1 and x["glyph_blobs_per_cm2"] is not None]
        res[sid] = {"role": "winner_control" if sid in WINNERS else "eligible",
                    "n_segments_catalog": len(s.get("segments") or {}), "n_segments_reader_v3": len(segs),
                    "pred_cm2": round(sum(x["valid_cm2"] for x in segs), 2),
                    "median_glyph_blobs_per_cm2": round(float(np.median(big)), 3) if big else None,
                    "median_frac_gt05": round(float(np.median([x["frac_gt05"] for x in segs if x["frac_gt05"] is not None])), 4) if segs else None}
        print(sid, res[sid], flush=True)
    w = [res[k]["median_glyph_blobs_per_cm2"] for k in WINNERS if res.get(k, {}).get("median_glyph_blobs_per_cm2") is not None]
    e = [res[k]["median_glyph_blobs_per_cm2"] for k in ELIGIBLE if res.get(k, {}).get("median_glyph_blobs_per_cm2") is not None]
    res["criterion"] = {"winners_median": float(np.median(w)) if w else None, "eligible_median": float(np.median(e)) if e else None,
                        "n_winners": len(w), "n_eligible": len(e)}
    res["criterion"]["informative"] = bool(w and e and np.median(w) > np.median(e))
    print(res["criterion"])
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
