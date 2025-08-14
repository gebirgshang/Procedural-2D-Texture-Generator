
from __future__ import annotations
import numpy as np

def _fade(t):
    return t*t*t*(t*(t*6 - 15) + 10)

def _gradients(gx, gy, rng):
    # Unit vectors on the circle
    theta = rng.random((gy+1, gx+1)) * 2*np.pi
    return np.stack([np.cos(theta), np.sin(theta)], axis=-1)

def perlin_tileable(size: int, freq: int, seed: int = 0, octaves: int = 1, persistence: float = 0.5, lacunarity: float = 2.0):
    """
    Generate tileable Perlin fractal noise.
    size: output is size x size
    freq: number of gradient cells per axis (period)
    """
    rng = np.random.default_rng(seed)
    h = np.zeros((size, size), dtype=np.float32)
    amp = 1.0
    per = 0.0
    for o in range(octaves):
        period = int(round(freq * (lacunarity ** o)))
        period = max(1, period)
        grid = _gradients(period, period, rng)
        # Map pixel coordinates to grid space [0, period)
        y = np.linspace(0, period, size, endpoint=False)
        x = np.linspace(0, period, size, endpoint=False)
        X, Y = np.meshgrid(x, y)
        x0 = np.floor(X).astype(int)
        y0 = np.floor(Y).astype(int)
        xf = X - x0
        yf = Y - y0
        # Wrap indices for tileability
        x1 = (x0 + 1) % period
        y1 = (y0 + 1) % period
        x0 = x0 % period
        y0 = y0 % period

        # Fetch gradients
        g00 = grid[y0, x0]
        g10 = grid[y0, x1]
        g01 = grid[y1, x0]
        g11 = grid[y1, x1]

        # Compute distance vectors
        d00 = np.stack([xf    , yf    ], axis=-1)
        d10 = np.stack([xf-1.0, yf    ], axis=-1)
        d01 = np.stack([xf    , yf-1.0], axis=-1)
        d11 = np.stack([xf-1.0, yf-1.0], axis=-1)

        # Dot products
        n00 = np.sum(g00 * d00, axis=-1)
        n10 = np.sum(g10 * d10, axis=-1)
        n01 = np.sum(g01 * d01, axis=-1)
        n11 = np.sum(g11 * d11, axis=-1)

        u = _fade(xf); v = _fade(yf)
        nx0 = n00*(1-u) + n10*u
        nx1 = n01*(1-u) + n11*u
        nxy = nx0*(1-v) + nx1*v

        h += nxy * amp
        per += amp
        amp *= persistence

    # Normalize to 0..1
    h = (h - h.min()) / (h.max() - h.min() + 1e-8)
    return h
