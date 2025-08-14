
from __future__ import annotations
import numpy as np
from math import cos, sin, pi

def checker(size: int, squares: int = 8):
    y = np.arange(size)[:,None]
    x = np.arange(size)[None,:]
    sq = size // max(1, squares)
    return (((x//sq) + (y//sq)) % 2).astype("float32")

def stripes(size: int, bands: int = 16, angle_deg: float = 0.0):
    y = np.arange(size)[:,None]
    x = np.arange(size)[None,:]
    theta = angle_deg * pi/180.0
    xr =  cos(theta)*x + sin(theta)*y
    period = max(1, size // max(1, bands))
    v = (np.sin(2*pi*xr/period) * 0.5 + 0.5).astype("float32")
    return v
