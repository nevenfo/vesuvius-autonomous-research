"""EXP-030 — compare l'inférence sur notre rendu propre et sur le surface-volume publié (README, critères H-035).

Usage : python compare.py <run_dir> <segment_dir> <results.json>
Attend <run_dir>/seg/sv.zarr, pred_own.tif, pred_pub.tif. Métriques d'encre via `vesres.eval_ink`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import tifffile
import zarr
from scipy.stats import spearmanr

from vesres.eval_ink import evaluate, load_segment_masks

B = 64


def blocks(a: np.ndarray, valid: np.ndarray) -> np.ndarray:
    h, w = (a.shape[0] // B) * B, (a.shape[1] // B) * B
    av = a[:h, :w].reshape(h // B, B, w // B, B).mean((1, 3))
    vv = valid[:h, :w].reshape(h // B, B, w // B, B).mean((1, 3))
    return np.where(vv >= 0.99, av, np.nan)


def main(run: Path, seg: Path, out: Path) -> None:
    own_sv = np.asarray(zarr.open(str(run / "seg" / "sv.zarr"), mode="r")["0"])
    pub_sv = np.asarray(zarr.open(str(seg / "sv.zarr"), mode="r")["0"])
    v_own, v_pub = own_sv.max(0) > 0, pub_sv.max(0) > 0
    n = own_sv.shape[0]
    med = [float(np.median(own_sv[i][v_own])) for i in range(n)]
    p_own = np.squeeze(tifffile.imread(run / "pred_own.tif"))
    p_pub = np.squeeze(tifffile.imread(run / "pred_pub.tif"))
    assert p_own.shape == p_pub.shape == v_own.shape == v_pub.shape, (p_own.shape, p_pub.shape, v_own.shape)
    valid = v_own & v_pub
    bo, bp = blocks(p_own.astype(np.float32), valid), blocks(p_pub.astype(np.float32), valid)
    m = np.isfinite(bo) & np.isfinite(bp)
    r = float(spearmanr(bo[m], bp[m]).statistic)
    # corrélation d'intensité (couche centrale) pour contrôler l'alignement des rendus
    ci = own_sv[n // 2].astype(np.float32), pub_sv[pub_sv.shape[0] // 2].astype(np.float32)
    bi = blocks(ci[0], valid), blocks(ci[1], valid)
    mi = np.isfinite(bi[0]) & np.isfinite(bi[1])
    masks = load_segment_masks(seg, p_own.shape)
    m_own, m_pub = evaluate(p_own, masks), evaluate(p_pub, masks)
    a_own, a_pub = m_own["reviewed"]["auc_protocol"], m_pub["reviewed"]["auc_protocol"]
    res = {"layers_own": n, "layers_pub": int(pub_sv.shape[0]), "shape": list(valid.shape),
           "valid_own": round(float(v_own.mean()), 4), "valid_pub": round(float(v_pub.mean()), 4),
           "valid_both": round(float(valid.mean()), 4),
           "orientation": {"argmax": int(np.argmax(med)), "center": n // 2, "ok": abs(int(np.argmax(med)) - n // 2) <= 3},
           "rho_blocks_pred": round(r, 3), "n_blocks": int(m.sum()),
           "rho_blocks_intensity_center": round(float(spearmanr(bi[0][mi], bi[1][mi]).statistic), 3),
           "auc_reviewed_own": a_own, "auc_reviewed_pub": a_pub,
           "ap_reviewed_own": m_own["reviewed"].get("ap"), "ap_reviewed_pub": m_pub["reviewed"].get("ap"),
           "metrics_own": m_own, "metrics_pub": m_pub}
    res["H-035"] = "soutenue" if (r >= 0.7 and a_own >= a_pub - 0.03) else "réfutée"
    out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if not k.startswith("metrics")}, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
