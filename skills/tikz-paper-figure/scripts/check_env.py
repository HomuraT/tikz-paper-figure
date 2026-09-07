"""Check that the tools the skill's scripts rely on are present, and say what each missing one is needed for.

Usage:
    python check_env.py

Prints one line per tool or package: `ok` with the path found, or `MISSING` with what breaks without it and where
to get it. Exit status 1 when something required is missing, so an agent can stop before promising a render.
Optional items (Pillow, lualatex) are reported but do not fail the check. Run it once per machine, before the
first figure; afterwards build_figure.py reports the same tools when they disappear.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    kind: str  # "tool" (on PATH), "tex" (found by kpsewhich) or "python" (importable module)
    needed_for: str
    source: str
    required: bool = True


ITEMS: list[Item] = [
    Item("latexmk", "tool", "build_figure.py (compiles every figure)", "TeX Live or MiKTeX"),
    Item("pdflatex", "tool", "build_figure.py and compare_sheet.py", "TeX Live or MiKTeX"),
    Item("kpsewhich", "tool", "this check (locates TeX packages)", "TeX Live or MiKTeX"),
    Item("pdfinfo", "tool", "build_figure.py (page size, width verdict)", "poppler-utils; TeX Live on Windows ships it"),
    Item("pdftoppm", "tool", "build_figure.py and compare_sheet.py (PNG renders)", "poppler-utils; TeX Live on Windows ships it"),
    Item("standalone.cls", "tex", "every figure (document class)", "TeX Live package standalone"),
    Item("pgfplots.sty", "tex", "plotfig.sty (data plots); 1.18 or later", "TeX Live package pgfplots"),
    Item("tikzlibrarytikzmark.code.tex", "tex", "cardfig.sty (highlights inside document pages)", "TeX Live package tikzmark"),
    Item("sourcesanspro.sty", "tex", "both style files (text font)", "TeX Live package sourcesanspro"),
    Item("inconsolata.sty", "tex", "both style files (monospace font)", "TeX Live package inconsolata"),
    Item("fontawesome5.sty", "tex", "both style files (icons)", "TeX Live package fontawesome5"),
    Item("PIL", "python", "gallery_sheet.py (contact sheet)", "pip install pillow", required=False),
    Item("lualatex", "tool", "build_figure.py --lualatex (pgfplots contour plots only)", "TeX Live or MiKTeX", required=False),
]


def locate(item: Item) -> str | None:
    if item.kind == "tool":
        return shutil.which(item.name)
    if item.kind == "tex":
        if shutil.which("kpsewhich") is None:
            return None
        result = subprocess.run(["kpsewhich", item.name], capture_output=True, text=True)
        path: str = result.stdout.strip()
        return path or None
    spec = importlib.util.find_spec(item.name)
    return spec.origin if spec is not None and spec.origin else None


def main() -> int:
    width: int = max(len(item.name) for item in ITEMS)
    missing_required: int = 0
    version: str = sys.version.split()[0]
    if sys.version_info < (3, 9):
        print(f"MISSING  python {version}: the scripts use 3.9 syntax; install Python 3.9 or later")
        missing_required += 1
    else:
        print(f"ok       python {version}  ({sys.executable})")
    for item in ITEMS:
        found: str | None = locate(item)
        if found:
            print(f"ok       {item.name:<{width}}  {found}")
            continue
        tag: str = "MISSING" if item.required else "absent "
        print(f"{tag}  {item.name:<{width}}  needed for {item.needed_for}; source: {item.source}")
        if item.required:
            missing_required += 1
    if missing_required:
        print(f"\n{missing_required} required item(s) missing: figures cannot be built or rendered on this machine."
              " Report that instead of describing a render.")
        return 1
    print("\nall required tools present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
