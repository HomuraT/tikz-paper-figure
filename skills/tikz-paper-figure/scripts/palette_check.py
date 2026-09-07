r"""Check a figure palette for colour-vision deficiency and greyscale print.

Usage:
    python palette_check.py 2B6CB0 DD6B20 2C7A7B 6B46C1          # hex values
    python palette_check.py --sty assets/plotfig.sty              # every \definecolor{..}{HTML}{..}
    python palette_check.py --sty assets/plotfig.sty --only kept,addc,dbA,dbB,gold

For every pair of colours it prints the CIE76 distance as seen by a normal observer and under simulated
protanopia, deuteranopia and tritanopia (Machado, Oliveira & Fernandes 2009, severity 1), plus the L*
lightness of each colour, which is what survives a black-and-white print. Pairs below --min (default 20)
are flagged: two series drawn in such colours cannot be told apart by that reader.
"""
from __future__ import annotations

import argparse
import itertools
import math
import re
import sys
from typing import Dict, List, Sequence, Tuple

RGB = Tuple[float, float, float]

MACHADO: Dict[str, Sequence[Sequence[float]]] = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def hex_to_rgb(h: str) -> RGB:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[return-value]


def to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(c: float) -> float:
    c = min(max(c, 0.0), 1.0)
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def simulate(rgb: RGB, kind: str) -> RGB:
    lin = [to_linear(c) for c in rgb]
    m = MACHADO[kind]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return tuple(to_srgb(c) for c in out)  # type: ignore[return-value]


def rgb_to_lab(rgb: RGB) -> Tuple[float, float, float]:
    r, g, b = (to_linear(c) for c in rgb)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.00000
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t: float) -> float:
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a: RGB, b: RGB) -> float:
    la, lb = rgb_to_lab(a), rgb_to_lab(b)
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(la, lb)))


def read_sty(path: str) -> List[Tuple[str, str]]:
    pat = re.compile(r"definecolor[{](\w+)[}][{]HTML[}][{]([0-9A-Fa-f]{6})[}]")
    found: List[Tuple[str, str]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.lstrip().startswith("%"):
                continue
            for name, hexv in pat.findall(line):
                found.append((name, hexv))
    return found


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("colours", nargs="*", help="hex values, optionally name=HEX")
    ap.add_argument("--sty", help="read every definecolor HTML from this .sty file")
    ap.add_argument("--only", help="comma-separated names to keep from the .sty")
    ap.add_argument("--min", type=float, default=20.0, help="flag pairs whose distance falls below this")
    args = ap.parse_args(argv)

    items: List[Tuple[str, str]] = []
    if args.sty:
        items = read_sty(args.sty)
        if args.only:
            keep = set(args.only.split(","))
            items = [it for it in items if it[0] in keep]
    for c in args.colours:
        name, _, hexv = c.rpartition("=")
        items.append((name or hexv.lstrip("#"), hexv))
    if len(items) < 2:
        ap.error("need at least two colours")

    rgbs = {name: hex_to_rgb(h) for name, h in items}
    width = max(len(n) for n in rgbs)
    print(f"{'colour':<{width}}  hex     L*    protan-L*  deutan-L*")
    for name, h in items:
        rgb = rgbs[name]
        lstar = rgb_to_lab(rgb)[0]
        lp = rgb_to_lab(simulate(rgb, "protan"))[0]
        ld = rgb_to_lab(simulate(rgb, "deutan"))[0]
        print(f"{name:<{width}}  {h}  {lstar:5.1f}  {lp:8.1f}  {ld:9.1f}")

    print()
    print(f"{'pair':<{2 * width + 3}}  normal  protan  deutan  tritan  greyscale(dL*)")
    flagged = 0
    for (na, ha), (nb, hb) in itertools.combinations(items, 2):
        a, b = rgbs[na], rgbs[nb]
        d_norm = delta_e(a, b)
        sims = {k: delta_e(simulate(a, k), simulate(b, k)) for k in MACHADO}
        d_grey = abs(rgb_to_lab(a)[0] - rgb_to_lab(b)[0])
        bad = min(d_norm, *sims.values()) < args.min
        mark = "  <-- low" if bad else ""
        flagged += bad
        print(f"{na + ' / ' + nb:<{2 * width + 3}}  {d_norm:6.1f}  {sims['protan']:6.1f}  {sims['deutan']:6.1f}  {sims['tritan']:6.1f}  {d_grey:8.1f}{mark}")
    print()
    print(f"{flagged} pair(s) below {args.min:g}. Greyscale column: below about 15 the two read the same in a black-and-white print.")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
