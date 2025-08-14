# 🌀 ProcGen Textures  
**Tileable procedural 2D textures for game developers — in Python**  

<p align="center">
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue.svg"></a>
  <a href="https://github.com/gebirgshang/procgen-textures/actions"><img alt="CI" src="https://github.com/gebirgshang/procgen-textures/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://pypi.org/project/procgen-textures/"><img alt="PyPI" src="https://img.shields.io/pypi/v/procgen-textures.svg"></a>
  <a href="./LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <a href="#"><img alt="Made with" src="https://img.shields.io/badge/made%20with-NumPy%20%26%20Pillow-informational"></a>
</p>

---

## 🎯 What is this?  
**ProcGen Textures** is a lightweight Python toolkit for generating **seamless, tileable textures** with ready-to-use **Albedo**, **Height**, and **Normal** maps.  
It’s perfect for **game developers**, **environment artists**, and **technical designers** who need quick, engine-ready textures for **Unity**, **Unreal**, **Godot**, or custom engines.

---

## ✨ Features
- 🎨 **Tileable** — perfect loops for any material.
- ⚙ **Multiple algorithms** — Perlin noise, Worley noise, patterns.
- 🖼 **Three maps per texture** — Albedo, Height, Normal.
- 🌈 **Built-in palettes** — grass, stone, lava, ocean, sand.
- 🎯 **Deterministic** — same seed = same result, every time.
- 📦 **Plug-and-play** — works with Unity, Unreal, Godot.
- 🪶 **Lightweight** — only `numpy` and `Pillow`.

---

## 🖥 Preview  

<p align="center">
  <img src="_preview/perlin_albedo.png" width="30%" />
  <img src="_preview/perlin_height.png" width="30%" />
  <img src="_preview/perlin_normal.png" width="30%" />
</p>

<p align="center">
  <img src="_preview/worley_albedo.png" width="30%" />
  <img src="_preview/worley_height.png" width="30%" />
  <img src="_preview/worley_normal.png" width="30%" />
</p>

---

## 🚀 Quick Start

```bash
# 1️⃣ Install
pip install procgen-textures

# 2️⃣ Generate a grass texture pack
procgen-textures gen-pack perlin     --size 512 --octaves 4 --freq 8     --palette grass --out out/grass --seed 1337
```

**Output:**
```
out/grass/albedo.png
out/grass/height.png
out/grass/normal.png
```

---

## 🛠 CLI Commands

List available palettes:
```bash
procgen-textures list-palettes
```

Generate with Worley noise:
```bash
procgen-textures gen-pack worley     --size 512 --cells 12 --palette stone     --out out/rock --seed 7
```

---

## 📦 Installation (from source)

```bash
git clone https://github.com/gebirgshang/procgen-textures.git
cd procgen_textures
pip install -e .
```

---

## 🧑‍💻 For Game Engines
1. Import **albedo.png** as your base color.
2. Use **normal.png** in your normal map slot.
3. Use **height.png** for displacement or parallax mapping.

---

## 📜 License  
MIT — free for commercial & personal use.  
