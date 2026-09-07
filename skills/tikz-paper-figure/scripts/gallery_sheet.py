"""Tile every example render of the skill into one contact sheet, assets/examples/gallery.png.

Usage:
    python gallery_sheet.py [--out assets/examples/gallery.png] [--cols 4] [--cell-width 430] [--cell-height 300]

The order and grouping match references/gallery.md: card figures, bar panels, then the data plots by the
question they answer. Each render is scaled to fit its cell (aspect kept) and labelled with its file stem.
Run it after adding or re-rendering an example, so the sheet and the gallery page agree. Needs Pillow.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SKILL_ROOT: Path = Path(__file__).resolve().parent.parent
EXAMPLES: Path = SKILL_ROOT / "assets" / "examples"
GROUPS: list[tuple[str, list[str]]] = [
    ("Card figures (cardfig.sty)", ["teaser-points", "pipeline-stages", "io-two-cards"]),
    ("Benchmark bar panels (cardfig.sty)", ["bench-bars"]),
    ("Data plots (plotfig.sty), in the order of references/gallery.md",
     ["grouped-bars", "dots", "ablation", "waterfall", "funnel", "stacked-counts",
      "dumbbell", "parity", "slope", "win-tie-loss",
      "curves-bands", "training-curves", "scaling-law", "pareto", "roc-pr", "calibration",
      "histogram-ecdf", "densities", "ridgeline", "boxplots", "strips", "scatter-margins",
      "stacked-100", "donuts", "treemap", "flows", "heatmap", "radar"]),
    ("Composite figures (plotfig.sty)", ["small-multiples", "stacked-panels", "inset-zoom", "mixed-panels"]),
]
FONT_CANDIDATES: list[str] = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf",
                              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]


def find_png(stem: str) -> Path:
    for candidate in (EXAMPLES / f"{stem}.png", EXAMPLES / "plots" / f"{stem}.png"):
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"no render for example {stem!r} under {EXAMPLES}")


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=EXAMPLES / "gallery.png")
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--cell-width", type=int, default=430, help="image box width in px")
    parser.add_argument("--cell-height", type=int, default=300, help="image box height in px")
    args = parser.parse_args()

    margin, gap, label_h, head_h = 36, 30, 34, 60
    cols: int = args.cols
    cell_w, cell_h = args.cell_width, args.cell_height
    sheet_w: int = 2 * margin + cols * cell_w + (cols - 1) * gap
    rows_total: int = sum(-(-len(items) // cols) for _, items in GROUPS)
    sheet_h: int = 2 * margin + len(GROUPS) * head_h + rows_total * (label_h + cell_h + gap)
    sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
    draw = ImageDraw.Draw(sheet)
    head_font, label_font = load_font(26), load_font(21)

    y: int = margin
    for title, items in GROUPS:
        draw.text((margin, y + 10), title, fill=(45, 55, 72), font=head_font)
        draw.line([(margin, y + head_h - 8), (sheet_w - margin, y + head_h - 8)], fill=(200, 200, 200), width=2)
        y += head_h
        for i, stem in enumerate(items):
            col, row = i % cols, i // cols
            x0: int = margin + col * (cell_w + gap)
            y0: int = y + row * (label_h + cell_h + gap)
            draw.text((x0, y0 + 4), stem, fill=(26, 32, 44), font=label_font)
            im = Image.open(find_png(stem)).convert("RGB")
            scale: float = min(cell_w / im.width, cell_h / im.height, 1.0)
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
            box_y: int = y0 + label_h
            draw.rectangle([x0, box_y, x0 + cell_w, box_y + cell_h], outline=(232, 232, 232), width=1)
            sheet.paste(im, (x0 + (cell_w - im.width) // 2, box_y + (cell_h - im.height) // 2))
        y += -(-len(items) // cols) * (label_h + cell_h + gap)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.out, optimize=True)
    print(f"[gallery] wrote {args.out}: {sheet_w}x{sheet_h}, {sum(len(i) for _, i in GROUPS)} renders")


if __name__ == "__main__":
    main()
