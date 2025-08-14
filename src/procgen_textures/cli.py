
from __future__ import annotations
import argparse, os, json
import numpy as np
from . import __version__
from .palette import PALETTES, list_palettes, map_height_to_rgb
from .imgutil import to_uint8_img, rgb_from_array, save_png, normal_from_height
from .perlin import perlin_tileable
from .worley import worley_tileable
from .patterns import checker, stripes

def ensure_out(path: str):
    os.makedirs(os.path.dirname(path) if os.path.splitext(path)[1] else path, exist_ok=True)

def cmd_list_palettes(_):
    for name in list_palettes():
        print(name)

def cmd_list_patterns(_):
    print("perlin, worley, checker, stripes")

def build_height(pattern: str, size: int, seed: int, **kwargs):
    if pattern == "perlin":
        freq = int(kwargs.get("freq", 8))
        octaves = int(kwargs.get("octaves", 4))
        persistence = float(kwargs.get("persistence", 0.5))
        lacunarity = float(kwargs.get("lacunarity", 2.0))
        return perlin_tileable(size=size, freq=freq, seed=seed, octaves=octaves, persistence=persistence, lacunarity=lacunarity)
    if pattern == "worley":
        cells = int(kwargs.get("cells", 12))
        metric = str(kwargs.get("metric", "euclidean"))
        return worley_tileable(size=size, cells=cells, seed=seed, metric=metric)
    if pattern == "checker":
        squares = int(kwargs.get("squares", 8))
        return checker(size=size, squares=squares)
    if pattern == "stripes":
        bands = int(kwargs.get("bands", 16))
        angle_deg = float(kwargs.get("angle", 0.0))
        return stripes(size=size, bands=bands, angle_deg=angle_deg)
    raise SystemExit(f"Unknown pattern: {pattern}")

def cmd_gen(args):
    h = build_height(args.pattern, args.size, args.seed, **vars(args))
    if args.normalize:
        h = (h - h.min()) / (h.max() - h.min() + 1e-8)
    if args.palette:
        pal = PALETTES.get(args.palette)
        if pal is None:
            raise SystemExit(f"Unknown palette: {args.palette}")
        rgb = map_height_to_rgb(h, pal)
        img = rgb_from_array(rgb)
    else:
        img = to_uint8_img(h)

    out = args.out or f"out/{args.pattern}.png"
    ensure_out(out)
    save_png(img, out)
    print(f"Saved {out}")

def cmd_gen_pack(args):
    h = build_height(args.pattern, args.size, args.seed, **vars(args))
    h = (h - h.min()) / (h.max() - h.min() + 1e-8)
    pal = PALETTES.get(args.palette, PALETTES["stone"])
    rgb = map_height_to_rgb(h, pal)
    nrm = normal_from_height(h, strength=args.normal_strength)

    base = args.out or f"out/{args.pattern}"
    os.makedirs(base, exist_ok=True)
    save_png(to_uint8_img(h), os.path.join(base, "height.png"))
    save_png(rgb_from_array(rgb), os.path.join(base, "albedo.png"))
    save_png(rgb_from_array(nrm), os.path.join(base, "normal.png"))
    meta = {
        "pattern": args.pattern,
        "size": args.size,
        "seed": args.seed,
        "params": {
            "perlin": {k:getattr(args,k) for k in ["freq","octaves","persistence","lacunarity"] if hasattr(args,k)},
            "worley": {k:getattr(args,k) for k in ["cells","metric"] if hasattr(args,k)},
        },
        "palette": args.palette,
    }
    with open(os.path.join(base, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
    print(f"Saved pack -> {base}/(albedo|height|normal).png")

def main(argv=None):
    p = argparse.ArgumentParser(prog="procgen_textures", description="Procedural 2D asset generator (tileable)")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(required=True)

    # list-palettes
    sp = sub.add_parser("list-palettes", help="List built-in palettes")
    sp.set_defaults(func=cmd_list_palettes)

    # list-patterns
    sp = sub.add_parser("list-patterns", help="List available patterns")
    sp.set_defaults(func=cmd_list_patterns)

    # gen
    g = sub.add_parser("gen", help="Generate a single PNG (albedo if --palette, else heightmap)")
    g.add_argument("pattern", choices=["perlin","worley","checker","stripes"])
    g.add_argument("--size", type=int, default=512)
    g.add_argument("--seed", type=int, default=1337)
    g.add_argument("--normalize", action="store_true")
    g.add_argument("--out", type=str, default=None)
    # perlin params
    g.add_argument("--freq", type=int, default=8)
    g.add_argument("--octaves", type=int, default=4)
    g.add_argument("--persistence", type=float, default=0.5)
    g.add_argument("--lacunarity", type=float, default=2.0)
    # worley params
    g.add_argument("--cells", type=int, default=12)
    g.add_argument("--metric", type=str, default="euclidean", choices=["euclidean","manhattan"])
    # style
    g.add_argument("--palette", type=str, default=None, help="If set, maps height to color")
    g.set_defaults(func=cmd_gen)

    # gen-pack
    gp = sub.add_parser("gen-pack", help="Generate albedo/height/normal into a folder")
    gp.add_argument("pattern", choices=["perlin","worley","checker","stripes"])
    gp.add_argument("--size", type=int, default=512)
    gp.add_argument("--seed", type=int, default=1337)
    gp.add_argument("--out", type=str, default=None)
    # perlin params
    gp.add_argument("--freq", type=int, default=8)
    gp.add_argument("--octaves", type=int, default=4)
    gp.add_argument("--persistence", type=float, default=0.5)
    gp.add_argument("--lacunarity", type=float, default=2.0)
    # worley params
    gp.add_argument("--cells", type=int, default=12)
    gp.add_argument("--metric", type=str, default="euclidean", choices=["euclidean","manhattan"])
    gp.add_argument("--palette", type=str, default="stone")
    gp.add_argument("--normal-strength", type=float, default=2.0)
    gp.set_defaults(func=cmd_gen_pack)

    args = p.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
