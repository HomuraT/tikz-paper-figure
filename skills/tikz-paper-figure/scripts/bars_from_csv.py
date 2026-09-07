"""Write a benchmark bar-panel figure (cardfig.sty, barpanel/barrow) from a results table.

Usage:
    python bars_from_csv.py results.csv --ours "Ours" [--cols 2] [--decimals 1] [--max auto] [--out figures/bench.tex]
                            [--lower-better "Latency"] [--body-only]

CSV layout (wide, one row per system):
    system,icon,Bench A,Bench B,...
    Ours,letter:O:kept,70.0,88.3
    Sol 3,fa:sun:addc,73.0,88.8
The first column is the system name, a column named "icon" is optional, every other column is a benchmark
and becomes one panel, in column order, filled left to right then top to bottom. Empty cells are skipped.

Icon cell: a shorthand or raw LaTeX.
    letter:K            \\iconletter{K}            letter:K:kept   \\iconletter[kept]{K}
    fa:sun              \\iconfa{sun}              fa:sun:addc     \\iconfa[addc]{sun}
    img:logos/x.pdf     \\iconimg{logos/x.pdf}     anything else is inserted as written

Rows are sorted best first (descending; ascending for --lower-better benchmarks). --max auto picks 1 when every
value is <= 1, 100 when every value is <= 100, else the largest value; the same maximum is used in every panel so
bar lengths compare across panels. The output sets \\barnamew from the longest name and \\barpanelpitch from the
largest number of rows; build it with build_figure.py and adjust the lengths by hand if needed.
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

TEXT_WIDTH_CM: float = 13.8       # usable width for a 5.5in text width
COL_GAP_CM: float = 0.6
TITLE_GAP_CM: float = 0.45
ROW_PITCH_CM: float = 0.3
PANEL_GAP_CM: float = 0.5
NAME_CM_PER_CHAR: float = 0.115
NAME_MIN_CM: float = 1.2

LATEX_SPECIALS: dict[str, str] = {"&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}"}


def escape(text: str) -> str:
    return "".join(LATEX_SPECIALS.get(ch, ch) for ch in text)


def icon_code(cell: str) -> str:
    cell = cell.strip()
    if not cell:
        return ""
    parts: list[str] = cell.split(":")
    kind: str = parts[0]
    if kind == "letter" and len(parts) in (2, 3):
        colour: str = f"[{parts[2]}]" if len(parts) == 3 else ""
        return f"\\iconletter{colour}{{{parts[1]}}}"
    if kind == "fa" and len(parts) in (2, 3):
        colour = f"[{parts[2]}]" if len(parts) == 3 else ""
        return f"\\iconfa{colour}{{{parts[1]}}}"
    if kind == "img" and len(parts) == 2:
        return f"\\iconimg{{{parts[1]}}}"
    return cell


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header: list[str] = [h.strip() for h in (reader.fieldnames or [])]
        rows: list[dict[str, str]] = [{k.strip(): (v or "").strip() for k, v in row.items() if k is not None} for row in reader]
    if len(header) < 2:
        sys.exit("the CSV needs a system column and at least one benchmark column")
    return header, rows


def pick_max(values: list[float], requested: str) -> float:
    if requested != "auto":
        return float(requested)
    top: float = max(values)
    if top <= 1.0:
        return 1.0
    if top <= 100.0:
        return 100.0
    return float(math.ceil(top))


def panel_body(title: str, entries: list[tuple[str, str, float]], ours: set[str], decimals: int, col: int, row: int) -> str:
    lines: list[str] = [f"\\begin{{barpanel}}{{{col}}}{{{row}}}{{{escape(title)}}}"]
    for name, icon, value in entries:
        style: str = "[ours]" if name in ours else ""
        lines.append(f"  \\barrow{style}{{{escape(name)}}}{{{icon}}}{{{value:.{decimals}f}}}")
    lines.append("\\end{barpanel}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--ours", action="append", default=[], help="system name to paint blue; may be repeated")
    parser.add_argument("--cols", type=int, default=2, help="panels per row (default 2)")
    parser.add_argument("--decimals", type=int, default=1)
    parser.add_argument("--max", default="auto", help="value that fills the track: auto (default), or a number")
    parser.add_argument("--lower-better", action="append", default=[], help="benchmark column sorted ascending; may be repeated")
    parser.add_argument("--keep-order", action="store_true",
                        help="keep the CSV row order in every panel instead of sorting by value: for rows that are an ordered "
                             "variable (model sizes, difficulty tiers, years), whose own order carries meaning")
    parser.add_argument("--out", type=Path, default=None, help="write here instead of stdout")
    parser.add_argument("--body-only", action="store_true", help="emit only the barpanel blocks")
    args = parser.parse_args()

    header, rows = read_table(args.csv)
    system_col: str = header[0]
    has_icon: bool = "icon" in header
    benchmarks: list[str] = [h for h in header[1:] if h != "icon"]
    ours: set[str] = set(args.ours)
    lower_better: set[str] = set(args.lower_better)

    panels: list[tuple[str, list[tuple[str, str, float]]]] = []
    all_values: list[float] = []
    for bench in benchmarks:
        entries: list[tuple[str, str, float]] = []
        for row in rows:
            cell: str = row.get(bench, "")
            if not cell:
                continue
            value: float = float(cell)
            entries.append((row[system_col], icon_code(row.get("icon", "")) if has_icon else "", value))
            all_values.append(value)
        if not args.keep_order:
            entries.sort(key=lambda e: e[2], reverse=bench not in lower_better)
        panels.append((bench, entries))
    if not all_values:
        sys.exit("no numeric cells found")

    track_max: float = pick_max(all_values, args.max)
    max_rows: int = max(len(entries) for _, entries in panels)
    longest_name: int = max(len(row[system_col]) for row in rows)
    name_w: float = max(NAME_MIN_CM, round(NAME_CM_PER_CHAR * longest_name + 0.15, 2))
    panel_w: float = round((TEXT_WIDTH_CM - (args.cols - 1) * COL_GAP_CM) / args.cols, 2)
    pitch: float = round(TITLE_GAP_CM + max_rows * ROW_PITCH_CM + PANEL_GAP_CM, 2)

    bodies: list[str] = [panel_body(title, entries, ours, args.decimals, i % args.cols, i // args.cols) for i, (title, entries) in enumerate(panels)]
    body: str = "\n".join(bodies)
    if args.body_only:
        text: str = body + "\n"
    else:
        max_text: str = f"{track_max:g}"
        text = "\n".join([
            f"% Generated by bars_from_csv.py from {args.csv.name}; edit freely, or change the CSV and regenerate.",
            "% One panel per benchmark, rows sorted best first, our system in blue. Build with build_figure.py.",
            "\\documentclass[10pt,tikz,border=1pt]{standalone}",
            "\\usepackage{cardfig}",
            f"\\setlength{{\\barpanelw}}{{{panel_w}cm}}        % cols*\\barpanelw + (cols-1)*\\barcolgap <= 13.8cm",
            f"\\setlength{{\\barcolgap}}{{{COL_GAP_CM}cm}}",
            f"\\setlength{{\\barnamew}}{{{name_w}cm}}          % longest name: {longest_name} characters",
            f"\\setlength{{\\barpanelpitch}}{{{pitch}cm}}      % \\bartitlegap + {max_rows} rows * \\barrowpitch + 0.5cm",
            f"\\renewcommand{{\\barmax}}{{{max_text}}}",
            "\\begin{document}",
            "\\begin{tikzpicture}",
            body,
            "\\end{tikzpicture}",
            "\\end{document}",
            "",
        ])
    if args.out is None:
        sys.stdout.write(text)
    else:
        args.out.write_text(text, encoding="utf-8")
        print(f"[bars] wrote {args.out} ({len(panels)} panels, {max_rows} rows max, track max {track_max:g})")


if __name__ == "__main__":
    main()
