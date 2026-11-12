"""Lecture par région de couches TIFF distantes (HTTP Range), avec cache local évictable.

Les couches de surface publiées sur dl.ash2txt.org sont des TIFF uint16 non compressés
à une seule strip : une bande de lignes [y0, y1) correspond à une plage d'octets contiguë.
On ne télécharge donc que les lignes utiles, jamais le fichier complet.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import requests

DEFAULT_CACHE = Path(os.environ.get("VESRES_CACHE", Path.home() / "vesuvius-work" / "cache"))
_SESSION = requests.Session()
_SESSION.headers["User-Agent"] = "vesres-research/0.1"


@dataclass(frozen=True)
class TiffLayout:
    url: str
    height: int
    width: int
    dtype: str
    data_offset: int
    content_length: int
    last_modified: str | None
    etag: str | None


def _get_range(url: str, start: int, end_inclusive: int, timeout: float = 120.0) -> bytes:
    r = _SESSION.get(url, headers={"Range": f"bytes={start}-{end_inclusive}"}, timeout=timeout)
    r.raise_for_status()
    if r.status_code != 206:
        raise RuntimeError(f"Range non honoré ({r.status_code}) pour {url}")
    data = r.content
    expected = end_inclusive - start + 1
    if len(data) != expected:
        raise RuntimeError(f"Réponse tronquée {len(data)}/{expected} octets pour {url}")
    return data


def probe_layout(url: str) -> TiffLayout:
    """Lit l'en-tête TIFF (quelques Ko) et vérifie que la couche est lisible par bandes."""
    import io

    import tifffile

    head = _SESSION.head(url, timeout=60, allow_redirects=True)
    head.raise_for_status()
    size = int(head.headers["Content-Length"])
    # L'IFD des TIFF classiques est en général au début ; on lit 64 Kio puis on élargit si besoin.
    n = 1 << 16
    while True:
        buf = _get_range(url, 0, min(n, size) - 1)
        try:
            with tifffile.TiffFile(io.BytesIO(buf)) as t:
                if t.byteorder != "<":
                    raise ValueError("TIFF big-endian non supporté")
                p = t.pages[0]
                shape, dtype = p.shape, p.dtype
                offsets, counts = p.dataoffsets, p.databytecounts
                compression = int(p.compression)
            break
        except ValueError:
            raise
        except Exception:  # en-tête tronqué : élargir la fenêtre lue
            if n >= size:
                raise
            n *= 4
    if compression != 1 or len(offsets) != 1 or len(shape) != 2:
        raise ValueError(f"Format non supporté par la lecture par bandes: comp={compression} strips={len(offsets)} shape={shape}")
    h, w = shape
    if counts[0] != h * w * np.dtype(dtype).itemsize:
        raise ValueError("Taille de strip incohérente")
    return TiffLayout(url, h, w, str(np.dtype(dtype)), int(offsets[0]), size,
                      head.headers.get("Last-Modified"), head.headers.get("ETag"))


def _cache_path(layout: TiffLayout, y0: int, y1: int, cache: Path) -> Path:
    key = hashlib.sha256(f"{layout.url}|{layout.etag}|{y0}|{y1}".encode()).hexdigest()[:24]
    return cache / "bands" / f"{key}.npy"


def read_rows(layout: TiffLayout, y0: int, y1: int, cache: Path | None = DEFAULT_CACHE) -> np.ndarray:
    """Retourne les lignes [y0, y1) de la couche (toute la largeur)."""
    if not (0 <= y0 < y1 <= layout.height):
        raise ValueError(f"bande hors limites {y0}:{y1} pour hauteur {layout.height}")
    if cache is not None:
        cp = _cache_path(layout, y0, y1, cache)
        if cp.exists():
            return np.load(cp)
    itemsize = np.dtype(layout.dtype).itemsize
    rowbytes = layout.width * itemsize
    start = layout.data_offset + y0 * rowbytes
    end = layout.data_offset + y1 * rowbytes - 1
    # Ordre d'octets : les TIFF Vesuvius sont little-endian ("II") ; vérifié par probe via tifffile.
    arr = np.frombuffer(_get_range(url=layout.url, start=start, end_inclusive=end), dtype=np.dtype(layout.dtype).newbyteorder("<"))
    arr = arr.reshape(y1 - y0, layout.width).copy()
    if cache is not None:
        cp.parent.mkdir(parents=True, exist_ok=True)
        tmp = cp.with_suffix(".tmp.npy")
        np.save(tmp, arr)
        os.replace(tmp, cp)  # écriture atomique : reprise sûre après interruption
        meta = cp.with_suffix(".json")
        meta.write_text(json.dumps({"layout": asdict(layout), "y0": y0, "y1": y1}, indent=1))
    return arr


def read_region(layout: TiffLayout, y0: int, y1: int, x0: int, x1: int, cache: Path | None = DEFAULT_CACHE) -> np.ndarray:
    return read_rows(layout, y0, y1, cache)[:, x0:x1]
