"""EXP-031 — synthèse : surface unique cumulée, fidélité, temps, zones candidates (critères H-036 du README).

Usage : python summarize.py <run_dir> <out4_dir> <out4_fidelity.json> <results.json>
Surface unique : sommets valides voxélisés à 20 voxels ; aire unique = Σ aires × cellules uniques / Σ cellules par patch.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import tifffile

CELL = 20


def cells(seg: Path) -> set:
    x, y, z = (tifffile.imread(seg / f"{c}.tif").astype(np.float64) for c in "xyz")
    ok = (x > 0) & (y > 0) & (z > 0) & np.isfinite(x)
    q = np.stack([z[ok], y[ok], x[ok]], 1) // CELL
    return set(map(tuple, np.unique(q.astype(np.int64), axis=0)))


def main(run: Path, out4: Path, fid4: Path, out: Path) -> None:
    rows, allc, tot = [], set(), 0
    entries = [("out4", out4, json.loads(fid4.read_text()), None, None, 474.2)]
    for p in sorted(run.glob("p[0-9]*"), key=lambda q: int(q.name[1:])):
        meta = p / "grow.meta"
        wall = int(re.search(r"wall=(\d+)", meta.read_text()).group(1)) if meta.exists() else None
        seg = p / "seg"
        if not (seg / "meta.json").exists():
            rows.append({"patch": p.name, "area_cm2": 0.0, "wall_s": wall, "status": meta.read_text().strip() if meta.exists() else "absent"})
            continue
        fid = json.loads((p / "fidelity.json").read_text()) if (p / "fidelity.json").exists() else {}
        an = json.loads((p / "analysis.json").read_text(encoding="utf-8")) if (p / "analysis.json").exists() else None
        ori = (p / "orientation.txt").read_text(encoding="utf-8", errors="replace").strip().replace("\n", " ") if (p / "orientation.txt").exists() else None
        entries.append((p.name, seg, fid, an, ori, wall))
    for name, seg, fid, an, ori, wall in entries:
        area = json.loads((seg / "meta.json").read_text())["area_cm2"]
        c = cells(seg)
        tot += len(c)
        allc |= c
        f = fid.get("fidelity", fid.get("frac_within_tol", fid.get("frac")))
        row = {"patch": name, "area_cm2": round(area, 3), "cells": len(c), "fidelity_2vx": f, "wall_s": wall, "orientation": ori}
        if an:
            row.update({"rho_lo_i9": an["agreement"]["rho_lo_i9"], "null_p95": an["agreement"]["null_p95"],
                        "rho_int_lo": an["lo"]["rho_intensity"], "rho_int_i9": an["i9"]["rho_intensity"],
                        "n_zones": an["candidates"]["n_zones"], "zones_mm2": an["candidates"]["total_area_mm2"]})
        rows.append(row)
    s_area = sum(r["area_cm2"] for r in rows)
    uniq = s_area * len(allc) / tot if tot else 0.0
    fids = [r["fidelity_2vx"] for r in rows if r.get("fidelity_2vx") is not None]
    walls = [r["wall_s"] for r in rows if r.get("wall_s")]
    res = {"patches": rows, "sum_area_cm2": round(s_area, 2), "unique_area_cm2": round(uniq, 2),
           "unique_frac": round(len(allc) / tot, 3) if tot else None, "median_fidelity": float(np.median(fids)) if fids else None,
           "total_wall_h": round(sum(walls) / 3600, 2)}
    res["H-036"] = "soutenue" if (uniq >= 40 and res["median_fidelity"] is not None and res["median_fidelity"] >= 0.85
                                  and res["total_wall_h"] <= 3) else "réfutée"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "patches"}, ensure_ascii=False))
    for r in rows:
        print(r)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
