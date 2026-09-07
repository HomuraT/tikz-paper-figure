"""Stack several figure PDFs with labels into one PNG, for before/after comparison.

Usage:
    python compare_sheet.py --out sheet.png "Figure 1, before=figures/teaser.pdf" "Figure 1, after=figures/teaser2.pdf" ...

Each positional argument is LABEL=PATH. The PDFs are placed at their natural size, one below the other,
in a standalone document set in Source Sans Pro, then rendered at --dpi (default 220).
Requires pdflatex and pdftoppm on PATH.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def tex_path(p: Path) -> str:
    return p.resolve().as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("items", nargs="+", help="LABEL=PATH pairs, top to bottom")
    parser.add_argument("--out", type=Path, required=True, help="output PNG")
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()

    blocks: list[str] = []
    for item in args.items:
        label, _, path = item.partition("=")
        if not path:
            print(f"[compare] expected LABEL=PATH, got: {item}")
            return 1
        blocks.append(
            "{\\large\\bfseries\\color{black!60} " + label + "}\\par\\vspace{4pt}\n"
            "\\includegraphics{" + tex_path(Path(path)) + "}\\par\\vspace{18pt}\n"
        )
    doc: str = (
        "\\documentclass[border=12pt]{standalone}\n"
        "\\usepackage{graphicx}\n\\usepackage[default]{sourcesanspro}\n\\usepackage{xcolor}\n"
        "\\begin{document}\n\\begin{minipage}{14.5cm}\\centering\n" + "".join(blocks) + "\\end{minipage}\n\\end{document}\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir: Path = Path(tmp)
        (tmpdir / "sheet.tex").write_text(doc, encoding="utf-8")
        result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "sheet.tex"], cwd=tmp, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stdout[-2000:])
            return 1
        args.out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", str(args.dpi), "-png", "-singlefile", "sheet.pdf", str(args.out.resolve().with_suffix(""))], cwd=tmp, check=True)
    print(f"[compare] wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
