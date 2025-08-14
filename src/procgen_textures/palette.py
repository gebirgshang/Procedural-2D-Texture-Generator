
from __future__ import annotations
from typing import List, Tuple
import numpy as np

PALETTES = {
    "grass": [
        (0.00, (30, 40, 20)),
        (0.25, (46, 77, 27)),
        (0.50, (71, 122, 53)),
        (0.75, (120, 170, 80)),
        (1.00, (190, 220, 120)),
    ],
    "sand": [
        (0.00, (40, 30, 10)),
        (0.30, (120, 90, 40)),
        (0.60, (180, 150, 80)),
        (1.00, (230, 210, 150)),
    ],
    "stone": [
        (0.00, (20, 20, 24)),
        (0.40, (64, 64, 70)),
        (0.70, (120, 120, 128)),
        (1.00, (200, 200, 205)),
    ],
    "lava": [
        (0.00, (10, 0, 0)),
        (0.30, (90, 10, 0)),
        (0.60, (200, 40, 0)),
        (0.80, (255, 120, 0)),
        (1.00, (255, 220, 120)),
    ],
    "ocean": [
        (0.00, (2, 6, 20)),
        (0.25, (10, 40, 90)),
        (0.50, (20, 90, 150)),
        (0.75, (30, 140, 200)),
        (1.00, (160, 220, 250)),
    ],
}

def list_palettes() -> list[str]:
    return sorted(PALETTES.keys())

def map_height_to_rgb(h, palette: List[Tuple[float, tuple]]):
    out = np.zeros((h.shape[0], h.shape[1], 3), dtype=np.uint8)
    stops = [p for p,_ in palette]
    cols  = [c for _,c in palette]
    idx = np.searchsorted(stops, h, side="right") - 1
    idx = np.clip(idx, 0, len(stops)-2)
    left = np.take(stops, idx)
    right = np.take(stops, idx+1)
    denom = (right - left)
    denom[denom == 0] = 1e-6
    t = (h - left) / denom
    c0 = np.stack([np.take([c[0] for c in cols], idx),
                   np.take([c[1] for c in cols], idx),
                   np.take([c[2] for c in cols], idx)], axis=-1)
    c1 = np.stack([np.take([c[0] for c in cols], idx+1),
                   np.take([c[1] for c in cols], idx+1),
                   np.take([c[2] for c in cols], idx+1)], axis=-1)
    out = (c0 + (c1 - c0) * t[...,None]).astype("uint8")
    return out
