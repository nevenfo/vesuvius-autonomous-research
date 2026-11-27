"""Mesures orientées lecture : unités graphiques, lisibilité locale, couverture des références.

Premier étage « au-delà du pixel » du protocole `docs/protocols/reading-evaluation.md` (niveaux 1-2) :
- unité graphique de référence (UGR) = composante connexe des ink-labels sur la grille de prédiction,
  principalement en région `supervision` (la région `validation` contient de l'encre non étiquetée, EXP-002/005) ;
- lisibilité locale d'une UGR = AUC entre les scores de ses pixels et ceux d'un anneau de fond voisin
  (même région revue, hors encre étiquetée) : indépendante du seuil et de la calibration (EXP-012) ;
- candidats glyphes en fond = composantes prédites de taille glyphe loin de toute encre étiquetée
  (proxy de faux glyphes, « hallucinations » au niveau détection) ;
- couverture = surfaces (cm²) du segment, revues avec référence fiable, revues sans référence fiable, non revues.

Une UGR n'est PAS une lettre identifiée : c'est un objet de taille glyphe (souvent une lettre ou un groupe de
lettres jointes). Aucune identité de caractère n'est mesurée ici (niveau 2 complet = phase T).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi


def dilate(mask: np.ndarray, r: float) -> np.ndarray:
    """Dilatation par un disque euclidien de rayon r (≡ structure x²+y² ≤ r²), via transformée de distance."""
    if not mask.any():
        return np.zeros_like(mask, dtype=bool)
    return ndi.distance_transform_edt(~mask) <= r


def auc_fast(pos: np.ndarray, neg: np.ndarray) -> float:
    from scipy.stats import rankdata

    s = np.concatenate([pos, neg]).astype(np.float64)
    r = rankdata(s)
    n1, n0 = len(pos), len(neg)
    return float((r[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def reference_units(ink: np.ndarray, valid: np.ndarray, supervision: np.ndarray, min_px: int = 200,
                    min_sup_frac: float = 0.5) -> tuple[np.ndarray, list[int]]:
    """Étiquette les composantes connexes de l'encre étiquetée ; garde celles ≥ min_px et ≥ min_sup_frac en supervision."""
    lab, n = ndi.label(ink & valid)
    if n == 0:
        return lab, []
    idx = np.arange(1, n + 1)
    area = ndi.sum(np.ones_like(lab, dtype=np.float64), lab, idx)
    insup = ndi.sum(supervision.astype(np.float64), lab, idx)
    keep = [int(i) for i, a, s in zip(idx, area, insup) if a >= min_px and s / a >= min_sup_frac]
    return lab, keep


def unit_geometry(lab: np.ndarray, units: list[int], ink: np.ndarray, region: np.ndarray,
                  ring_px: int = 48, gap_px: int = 3) -> list[dict]:
    """Pour chaque unité : fenêtre, masque de l'unité et anneau de fond (région revue, hors encre dilatée de gap_px).
    Indépendant de la prédiction : à calculer une fois par segment."""
    far = region & ~dilate(ink, gap_px)
    keep = set(units)
    out = []
    for sl_i, sl in enumerate(ndi.find_objects(lab)):
        u = sl_i + 1
        if u not in keep or sl is None:
            continue
        y0, y1 = max(sl[0].start - ring_px, 0), min(sl[0].stop + ring_px, lab.shape[0])
        x0, x1 = max(sl[1].start - ring_px, 0), min(sl[1].stop + ring_px, lab.shape[1])
        m = lab[y0:y1, x0:x1] == u
        ring = dilate(m, ring_px) & far[y0:y1, x0:x1]
        out.append({"unit": u, "win": (slice(y0, y1), slice(x0, x1)), "mask": m, "ring": ring,
                    "bbox": [int(sl[0].start), int(sl[1].start), int(sl[0].stop), int(sl[1].stop)]})
    return out


def score_units(pred: np.ndarray, geoms: list[dict], min_ring: int = 200) -> list[dict]:
    out = []
    for g in geoms:
        p = pred[g["win"]]
        pos, neg = p[g["mask"]], p[g["ring"]]
        rec = {"unit": g["unit"], "area_px": int(len(pos)), "ring_px": int(len(neg)), "bbox": g["bbox"]}
        rec["local_auc"] = round(auc_fast(pos, neg), 4) if len(neg) >= min_ring else None
        out.append(rec)
    return out


def unit_legibility(pred: np.ndarray, lab: np.ndarray, units: list[int], ink: np.ndarray, region: np.ndarray,
                    ring_px: int = 48, gap_px: int = 3, min_ring: int = 200) -> list[dict]:
    """AUC locale par unité : pixels de l'unité vs anneau de fond (région revue, hors encre dilatée de gap_px)."""
    return score_units(pred, unit_geometry(lab, units, ink, region, ring_px, gap_px), min_ring)


def legible_fraction(recs: list[dict], thr: float) -> float | None:
    v = [r["local_auc"] for r in recs if r["local_auc"] is not None]
    return round(float(np.mean([a >= thr for a in v])), 4) if v else None


def background_candidates(pred: np.ndarray, ink: np.ndarray, region: np.ndarray, thr: float, area_range: tuple[int, int],
                          margin_px: int = 48, px_um: float = 9.366, bg: np.ndarray | None = None) -> dict:
    """Composantes prédites (pred ≥ thr) de taille glyphe ≥ 95 % dans le fond revu, loin de l'encre étiquetée.
    `bg` (fond pré-calculé) évite de recalculer la dilatation pour chaque chaîne."""
    if bg is None:
        bg = region & ~dilate(ink, margin_px)
    lab, n = ndi.label((pred >= thr) & region)
    if n:
        idx = np.arange(1, n + 1)
        area = ndi.sum(np.ones_like(lab, dtype=np.float64), lab, idx)
        inbg = ndi.sum(bg.astype(np.float64), lab, idx)
        cand = int(np.sum((area >= area_range[0]) & (area <= area_range[1]) & (inbg >= 0.95 * area)))
    else:
        cand = 0
    bg_cm2 = float(bg.sum()) * (px_um * 1e-4) ** 2
    return {"threshold": round(float(thr), 4), "n_candidates": cand, "background_cm2": round(bg_cm2, 3),
            "per_cm2": round(cand / bg_cm2, 3) if bg_cm2 > 0 else None}


def coverage(valid: np.ndarray, supervision: np.ndarray, validation: np.ndarray, px_um: float = 9.366) -> dict:
    """Surfaces (cm²) : segment, revue avec référence fiable (supervision), revue sans référence fiable
    (validation seule : encre non étiquetée possible), non revue."""
    c = (px_um * 1e-4) ** 2
    sup = valid & supervision
    val_only = valid & validation & ~supervision
    unrev = valid & ~supervision & ~validation
    tot = float(valid.sum())
    r = {"segment_cm2": tot * c, "reliable_reference_cm2": float(sup.sum()) * c,
         "reviewed_unreliable_cm2": float(val_only.sum()) * c, "unreviewed_cm2": float(unrev.sum()) * c}
    r = {k: round(v, 3) for k, v in r.items()}
    r["reliable_reference_frac"] = round(float(sup.sum()) / tot, 4) if tot else None
    return r


def positive_control(ink: np.ndarray, sigma: float = 2.0, noise: float = 0.05, seed: int = 0) -> np.ndarray:
    """Prédiction quasi parfaite : labels flous + bruit faible (la métrique doit la juger lisible)."""
    rng = np.random.default_rng(seed)
    return np.clip(ndi.gaussian_filter(ink.astype(np.float32), sigma) + rng.normal(0, noise, ink.shape), 0, 1).astype(np.float32)


def negative_control(pred: np.ndarray) -> np.ndarray:
    """Prédiction réelle découplée des labels par rotation de 180° (garde la texture, détruit l'alignement)."""
    return np.ascontiguousarray(pred[::-1, ::-1])
