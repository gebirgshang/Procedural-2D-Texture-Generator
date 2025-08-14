
from __future__ import annotations
import numpy as np

def worley_tileable(size: int, cells: int, seed: int = 0, metric: str = "euclidean"):
    rng = np.random.default_rng(seed)
    pts = rng.random((cells, cells, 2))  # in cell-local [0,1)
    y = np.linspace(0, cells, size, endpoint=False)
    x = np.linspace(0, cells, size, endpoint=False)
    X, Y = np.meshgrid(x, y)
    xi = np.floor(X).astype(int)
    yi = np.floor(Y).astype(int)
    xf = X - xi
    yf = Y - yi

    offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
    dmin = np.full((size, size), 1e9, dtype=np.float32)
    for oy, ox in offsets:
        cx = (xi + ox) % cells
        cy = (yi + oy) % cells
        feat = pts[cy, cx]
        dx = (feat[...,0] + ox) - xf
        dy = (feat[...,1] + oy) - yf
        if metric == "manhattan":
            d = np.abs(dx) + np.abs(dy)
        else:
            d = np.sqrt(dx*dx + dy*dy)
        dmin = np.minimum(dmin, d.astype(np.float32))

    dmin = dmin / np.sqrt(2.0)
    dmin = np.clip(dmin, 0.0, 1.0)
    return dmin
