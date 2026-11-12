"""Inventaire déterministe du corpus à partir du catalogue officiel `metadata.min.json`.

Usage : python -m vesres.catalog <metadata.min.json> <sortie.csv> <sortie.md>
Le catalogue est récupéré depuis le bucket public vesuvius-challenge-open-data (voir docs/data/README.md).
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path


def _data_types(entry: dict) -> list[str]:
    return [d.get("type", "?") for d in entry.get("data", [])]


def summarize(meta: dict) -> list[dict]:
    rows = []
    for sid, s in meta["samples"].items():
        props = s.get("sample", {}).get("properties", {})
        scans = s.get("scans", {}) or {}
        vols = s.get("volumes", {}) or {}
        segs = s.get("segments", {}) or {}
        seg_types = Counter(t for e in segs.values() for t in _data_types(e))
        scan_desc = sorted(
            f"{sc.get('properties', {}).get('pixel_size_um')}um/{sc.get('properties', {}).get('energy_keV')}keV"
            f"@{(sc.get('creation', {}).get('metadata', {}).get('location') or '?').split(' ')[0]}"
            for sc in scans.values()
        )
        licenses = sorted({v.get("properties", {}).get("license", {}).get("name", "?") for v in vols.values()})
        best_um = min((sc.get("properties", {}).get("pixel_size_um") or 99) for sc in scans.values()) if scans else None
        rows.append({
            "id": sid,
            "type": props.get("type", "?"),
            "n_scans": len(scans),
            "best_um": best_um,
            "scans": "; ".join(scan_desc),
            "n_volumes": len(vols),
            "volume_licenses": "; ".join(licenses),
            "n_segments": len(segs),
            "n_seg_ink_detection": seg_types.get("ink-detection", 0),
            "n_seg_layers": sum(v for k, v in seg_types.items() if k.startswith("layers")),
            "segment_data_types": "; ".join(f"{k}:{v}" for k, v in sorted(seg_types.items())),
            "volume_formats": "; ".join(sorted({t for e in vols.values() for t in _data_types(e)})),
            "legacy_data_url": props.get("legacy_data_url", ""),
        })
    rows.sort(key=lambda r: (r["type"], -r["n_segments"], r["id"]))
    return rows


def write_outputs(rows: list[dict], csv_path: Path, md_path: Path, source_note: str) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cols = ["id", "type", "best_um", "n_scans", "n_segments", "n_seg_layers", "n_seg_ink_detection", "volume_licenses"]
    lines = [
        "# Inventaire du corpus (généré)",
        "",
        source_note,
        "",
        f"Échantillons : {len(rows)} — rouleaux : {sum(r['type'] == 'scroll' for r in rows)}, "
        f"fragments : {sum(r['type'] == 'fragment' for r in rows)}.",
        "",
        "`n_seg_ink_detection` = segments portant une prédiction d'encre publiée (sortie de modèle, pas un label humain).",
        "",
        "| " + " | ".join(cols) + " |",
        "|" + "---|" * len(cols),
    ]
    lines += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    src, out_csv, out_md = map(Path, argv[1:4])
    meta = json.loads(src.read_text(encoding="utf-8"))
    rows = summarize(meta)
    note = argv[4] if len(argv) > 4 else f"Source : {src.name}"
    write_outputs(rows, out_csv, out_md, note)
    print(f"{len(rows)} échantillons -> {out_csv}, {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
