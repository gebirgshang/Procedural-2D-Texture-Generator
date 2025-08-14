
from __future__ import annotations
import numpy as np
from PIL import Image

def to_uint8_img(h: np.ndarray) -> Image.Image:
    h = np.clip(h, 0.0, 1.0)
    arr = (h * 255.0 + 0.5).astype("uint8")
    return Image.fromarray(arr, mode="L")

def rgb_from_array(arr: np.ndarray) -> Image.Image:
    arr = np.clip(arr, 0, 255).astype("uint8")
    return Image.fromarray(arr, mode="RGB")

def save_png(img: Image.Image, path: str):
    img.save(path, format="PNG", optimize=True)

def normal_from_height(h: np.ndarray, strength: float = 2.0) -> np.ndarray:
    sx = np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)
    sy = np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)
    nx = -sx * strength
    ny = -sy * strength
    nz = np.ones_like(h)
    length = np.sqrt(nx*nx + ny*ny + nz*nz) + 1e-8
    nx /= length; ny /= length; nz /= length
    rgb = np.stack([(nx*0.5+0.5), (ny*0.5+0.5), (nz*0.5+0.5)], axis=-1)
    return (rgb * 255.0).astype("uint8")
