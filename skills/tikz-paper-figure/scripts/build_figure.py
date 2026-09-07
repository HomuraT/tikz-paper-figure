"""Build a standalone TikZ figure, clean up, check its width and render a PNG to look at.

Usage:
    python build_figure.py FIG.tex [FIG2.tex ...] [--max-width 397.5] [--dpi 300] [--png-dir DIR] [--keep-aux]

For every FIG.tex this runs latexmk in the file's directory (so aux files stay there), removes the aux files,
reads the page size of the PDF, warns when the figure would overflow the text width, and renders page 1 to a PNG.
Read the PNG afterwards; the compile log alone does not show overlaps, hyphenation or misaligned elements.

Requires latexmk, pdfinfo and pdftoppm (TeX Live + poppler) on PATH.
The skill's assets directory is appended to TEXINPUTS so the bundled examples find cardfig.sty and plotfig.sty;
a copy next to the figure always wins, and that copy is what a paper repository should contain.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# pdftex reports an included PDF about 1.5pt wider than pdfinfo does (the MediaBox is rounded up).
PDFTEX_SLACK_PT: float = 1.5
DEFAULT_MAX_WIDTH_PT: float = 397.5  # 5.5in, the ICLR / NeurIPS text width
ASSETS_DIR: Path = Path(__file__).resolve().parent.parent / "assets"


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")


def texinputs_env() -> dict[str, str]:
    env: dict[str, str] = dict(os.environ)
    current: str = env.get("TEXINPUTS", "")
    # trailing separator keeps the default search path
    env["TEXINPUTS"] = f".{os.pathsep}{ASSETS_DIR}{os.pathsep}{current}" if current else f".{os.pathsep}{ASSETS_DIR}{os.pathsep}"
    return env


def compile_figure(tex: Path, keep_aux: bool, lualatex: bool = False) -> bool:
    env: dict[str, str] = texinputs_env()
    engine: str = "-lualatex" if lualatex else "-pdf"
    result = run(["latexmk", engine, "-interaction=nonstopmode", "-halt-on-error", tex.name], cwd=tex.parent, env=env)
    log: Path = tex.with_suffix(".log")
    if result.returncode != 0:
        print(f"[build] FAILED: {tex.name}")
        if log.exists():
            text: str = log.read_text(encoding="utf-8", errors="replace")
            # the "!" line plus enough context to reach the "l.NN" line that locates the error in the source
            for m in re.finditer(r"^!.*(?:\n.*){0,9}", text, flags=re.M):
                print(m.group(0))
                print("-" * 40)
        else:
            print(result.stdout[-3000:])
        return False
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
        for pattern in (r"Overfull \\hbox.*", r"LaTeX Warning: Label\(s\) may have changed.*"):
            for m in re.finditer(pattern, text):
                print(f"[build] {tex.name}: {m.group(0).strip()}")
    if not keep_aux:
        run(["latexmk", "-c", tex.name], cwd=tex.parent, env=env)
    return True


def page_size_pt(pdf: Path) -> tuple[float, float] | None:
    result = run(["pdfinfo", pdf.name], cwd=pdf.parent)
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", result.stdout)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def render_png(pdf: Path, png_dir: Path, dpi: int) -> Path:
    png_dir = png_dir.resolve()  # pdftoppm runs in the figure's directory, so a relative --png-dir must be made absolute first
    png_dir.mkdir(parents=True, exist_ok=True)
    stem: Path = png_dir / pdf.stem
    run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", str(pdf), str(stem)], cwd=pdf.parent)
    return stem.with_suffix(".png")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tex", nargs="+", type=Path, help="standalone figure sources")
    parser.add_argument("--max-width", type=float, default=DEFAULT_MAX_WIDTH_PT, help="text width in pt (default 397.5 = 5.5in)")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--png-dir", type=Path, default=Path(tempfile.gettempdir()) / "cardfig", help="where to put the PNG renders")
    parser.add_argument("--keep-aux", action="store_true", help="do not run latexmk -c afterwards")
    parser.add_argument("--lualatex", action="store_true", help="compile with lualatex (needed for pgfplots contour lua)")
    args = parser.parse_args()

    ok: bool = True
    for tex in args.tex:
        tex = tex.resolve()
        if not tex.exists():
            print(f"[build] no such file: {tex}")
            ok = False
            continue
        if not compile_figure(tex, args.keep_aux, args.lualatex):
            ok = False
            continue
        pdf: Path = tex.with_suffix(".pdf")
        size = page_size_pt(pdf)
        if size is None:
            print(f"[build] {pdf.name}: could not read page size (is pdfinfo on PATH?)")
        else:
            width, height = size
            limit: float = args.max_width - PDFTEX_SLACK_PT
            verdict: str = "ok" if width <= limit else f"TOO WIDE, pdftex will see about {width + PDFTEX_SLACK_PT:.1f}pt > {args.max_width}pt"
            print(f"[build] {pdf.name}: {width:.1f} x {height:.1f} pt  ({width / 28.4528:.2f} x {height / 28.4528:.2f} cm)  width {verdict}")
        png: Path = render_png(pdf, args.png_dir, args.dpi)
        print(f"[build] render: {png}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
