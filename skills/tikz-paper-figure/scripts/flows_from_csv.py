"""Write a parallel-sets (alluvial, Sankey-like) diagram as a standalone TikZ file.

The form follows Wilke, Fundamentals of Data Visualization, "Nested proportions": every node is a grey bar
with its name set vertically inside it, each column carries the variable name beneath it, every band keeps
the colour of the leftmost variable across all hops, and within a node the bands are grouped by that colour
first, so the same colour stays together and the bands cross as little as possible. No numbers are printed
unless asked for.

Usage:
    python flows_from_csv.py records.csv --out flows.tex [--columns "source,domain,split"] [--height 4.2]
    python flows_from_csv.py edges.csv --edges --out flows.tex [--columns ...]

Input, default (records): a header row naming the categorical variables in column order, one row per record
or per group of records, and an optional `count` column (default 1). Nodes of a column are its distinct
values, ordered by first appearance; bands between adjacent columns are exact.

Input, --edges: source,target,quantity with one row per flow. Columns are inferred (a node is placed in
column k when its longest incoming chain has k edges). A flow out of a middle node is split among the
leftmost-column origins in proportion to the node's inflow, because an edge list does not say which records
went where; give records when the exact composition matters.

Options: --columns names the variables under the columns (records mode reads them from the header);
--totals appends the total to each node name; --label-min N prints the quantity on bands of at least N;
--palette house uses the paper's hues instead of the light set colours (they blend worse); --colour-by-source
colours each hop by its source node and the nodes themselves (the older form).
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

# band colours: the light `set*` colours of plotfig.sty, which blend cleanly at opacity 0.5 (Wilke's figure uses
# pink, blue, yellow in this order); --palette house switches to the paper's semantic hues
PALETTE_SETS: list[str] = ["setpink", "setblue", "setyellow", "setgreen", "setviolet", "setorange"]
PALETTE_HOUSE: list[str] = ["kept", "dbA", "addc", "dbB", "gold", "black!45"]
Part = tuple[str, str, str, float]  # origin, source, target, quantity


def read_records(path: Path) -> tuple[list[str], list[list[str]], list[Part]]:
    """Return variable names, nodes per column (first appearance), and the parts between adjacent columns."""
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")]
    header = [h.strip() for h in rows[0]]
    count_idx: int | None = next((i for i, h in enumerate(header) if h.lower() == "count"), None)
    var_idx: list[int] = [i for i in range(len(header)) if i != count_idx]
    variables: list[str] = [header[i] for i in var_idx]
    columns: list[list[str]] = [[] for _ in variables]
    agg: dict[tuple[int, str, str, str], float] = {}
    for row in rows[1:]:
        values: list[str] = [row[i].strip() for i in var_idx]
        count: float = float(row[count_idx]) if count_idx is not None and row[count_idx].strip() else 1.0
        for k, v in enumerate(values):
            if v not in columns[k]:
                columns[k].append(v)
        for k in range(len(values) - 1):
            key = (k, values[0], values[k], values[k + 1])
            agg[key] = agg.get(key, 0.0) + count
    parts: list[Part] = [(o, s, t, q) for (_, o, s, t), q in agg.items()]
    return variables, columns, parts


def read_edges(path: Path) -> list[tuple[str, str, float]]:
    flows: list[tuple[str, str, float]] = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.reader(fh):
            if not row or row[0].startswith("#") or row[0].strip().lower() in ("source", "src"):
                continue
            flows.append((row[0].strip(), row[1].strip(), float(row[2])))
    return flows


def edges_to_parts(flows: list[tuple[str, str, float]], by_source: bool) -> tuple[list[list[str]], list[Part]]:
    """Infer columns from the longest chain and split every flow by origin in proportion to the inflow."""
    nodes: list[str] = []
    for s, t, _ in flows:
        for n in (s, t):
            if n not in nodes:
                nodes.append(n)
    col: dict[str, int] = {n: 0 for n in nodes}
    changed: bool = True
    while changed:
        changed = False
        for s, t, _ in flows:
            if col[t] < col[s] + 1:
                col[t] = col[s] + 1
                changed = True
    ncols: int = max(col.values()) + 1
    columns: list[list[str]] = [[n for n in nodes if col[n] == k] for k in range(ncols)]
    if by_source:
        return columns, [(s, s, t, q) for s, t, q in flows]
    comp: dict[str, dict[str, float]] = {n: {} for n in nodes}
    for o in columns[0]:
        comp[o] = {o: sum(q for s, _, q in flows if s == o)}
    parts: list[Part] = []
    for s, t, q in sorted(flows, key=lambda f: col[f[0]]):
        base: float = sum(comp[s].values())
        for o, v in comp[s].items():
            share: float = q * v / base
            parts.append((o, s, t, share))
            comp[t][o] = comp[t].get(o, 0.0) + share
    return columns, parts


def esc(text: str) -> str:
    return text.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--edges", action="store_true", help="input is a source,target,quantity edge list")
    parser.add_argument("--columns", default=None, help="comma-separated variable names set beneath the columns")
    parser.add_argument("--height", type=float, default=4.2, help="height of the tallest column in cm")
    parser.add_argument("--col-gap", type=float, default=3.4, help="distance between column left edges in cm")
    parser.add_argument("--node-gap", type=float, default=0.3, help="gap between nodes of one column in cm")
    parser.add_argument("--node-width", type=float, default=0.46, help="node bar width in cm (holds the vertical name)")
    parser.add_argument("--node-border", type=float, default=1.6,
                        help="white outline of the node bars in pt, drawn over the band ends so a thin white gap separates bars from bands (0 for none)")
    parser.add_argument("--opacity", type=float, default=0.5, help="band opacity; overlaps blend")
    parser.add_argument("--palette", choices=["sets", "house"], default="sets",
                        help="sets (default): light pink, blue, yellow ... that blend cleanly; house: the paper's kept, dbA, addc ...")
    parser.add_argument("--totals", action="store_true", help="append the node total to its name")
    parser.add_argument("--label-min", type=float, default=None, help="print the quantity on bands at least this large")
    parser.add_argument("--colour-by-source", action="store_true",
                        help="colour each hop by its source node, and the nodes themselves, instead of by the leftmost variable")
    args = parser.parse_args()

    titles: list[str] = []
    if args.edges:
        columns, parts = edges_to_parts(read_edges(args.csv), args.colour_by_source)
    else:
        titles, columns, parts = read_records(args.csv)
    if args.columns:
        titles = [t.strip() for t in args.columns.split(",")]
    ncols: int = len(columns)
    order: list[str] = [n for c in columns for n in c]
    col: dict[str, int] = {n: k for k, c in enumerate(columns) for n in c}
    idx: dict[str, int] = {n: i for c in columns for i, n in enumerate(c)}
    origins: list[str] = columns[0]
    palette: list[str] = PALETTE_SETS if args.palette == "sets" else PALETTE_HOUSE
    colour_key: dict[str, str] = {n: palette[i % len(palette)] for i, n in enumerate(order if args.colour_by_source else origins)}

    total: dict[str, float] = {}
    for n in order:
        out_q: float = sum(q for _, s, _, q in parts if s == n)
        in_q: float = sum(q for _, _, t, q in parts if t == n)
        total[n] = max(in_q, out_q)
    max_rows: int = max(len(c) for c in columns)
    col_total: float = max(sum(total[n] for n in c) for c in columns)
    unit: float = (args.height - (max_rows - 1) * args.node_gap) / col_total  # cm per quantity unit

    # vertical placement: each column centred on the tallest one
    top: dict[str, float] = {}
    for c in columns:
        h: float = sum(total[n] * unit for n in c) + (len(c) - 1) * args.node_gap
        y: float = h / 2
        for n in c:
            top[n] = y
            y -= total[n] * unit + args.node_gap
    w: float = args.node_width
    x_of: dict[str, float] = {n: col[n] * args.col_gap for n in order}

    # slot order within a node: by colour (origin) first, then by the other end in its column order, so that
    # bands of one colour stay together and cross least (the parallel-sets layout)
    o_idx: dict[str, int] = {o: i for i, o in enumerate(origins)} if not args.colour_by_source else {n: i for i, n in enumerate(order)}
    out_off: dict[tuple[str, str, str], float] = {}
    in_off: dict[tuple[str, str, str], float] = {}
    for n in order:
        y = 0.0
        for o, s, t, q in sorted((p for p in parts if p[1] == n), key=lambda p: (o_idx[p[0]], idx[p[2]])):
            out_off[(o, s, t)] = y
            y += q * unit
        y = 0.0
        for o, s, t, q in sorted((p for p in parts if p[2] == n), key=lambda p: (o_idx[p[0]], idx[p[1]])):
            in_off[(o, s, t)] = y
            y += q * unit

    lines: list[str] = [
        f"% Generated by flows_from_csv.py from {args.csv.name}: parallel sets after Wilke. Grey node bars with vertical",
        "% names, bands coloured by the leftmost variable and grouped by colour inside every node, variable names beneath.",
        "\\documentclass[10pt,tikz,border=2pt]{standalone}",
        "\\usepackage{plotfig}",
        "\\begin{document}",
        "\\begin{tikzpicture}",
    ]
    for o, s, t, q in parts:
        h = q * unit
        x1: float = x_of[s] + w
        x2: float = x_of[t]
        y1: float = top[s] - out_off[(o, s, t)]
        y2: float = top[t] - in_off[(o, s, t)]
        cx: float = (x2 - x1) * 0.5
        lines.append(
            f"\\fill[{colour_key[o]}, opacity={args.opacity}] ({x1:.3f},{y1:.3f}) .. controls ({x1 + cx:.3f},{y1:.3f}) and ({x2 - cx:.3f},{y2:.3f}) .. ({x2:.3f},{y2:.3f})"
            f" -- ({x2:.3f},{y2 - h:.3f}) .. controls ({x2 - cx:.3f},{y2 - h:.3f}) and ({x1 + cx:.3f},{y1 - h:.3f}) .. ({x1:.3f},{y1 - h:.3f}) -- cycle;"
        )
        if args.label_min is not None and q >= args.label_min:
            tt: float = 0.8
            bx: float = (1 - tt) ** 3 * x1 + 3 * (1 - tt) ** 2 * tt * (x1 + cx) + 3 * (1 - tt) * tt ** 2 * (x2 - cx) + tt ** 3 * x2
            by: float = (1 - tt) ** 3 * y1 + 3 * (1 - tt) ** 2 * tt * y1 + 3 * (1 - tt) * tt ** 2 * y2 + tt ** 3 * y2 - h / 2
            lines.append(f"\\node[mono, text=black!60] at ({bx:.3f},{by:.3f}) {{{q:g}}};")
    for n in order:
        x: float = x_of[n]
        h = total[n] * unit
        fill: str = colour_key[n] if args.colour_by_source else "setgrey"
        # the bars are drawn after the bands with a white outline, so the band ends are trimmed by a thin white
        # gap on both sides of every bar, as in the book's figure
        border: str = f", draw=white, line width={args.node_border}pt" if args.node_border > 0 else ""
        lines.append(f"\\filldraw[fill={fill}{border}] ({x:.3f},{top[n]:.3f}) rectangle ({x + w:.3f},{top[n] - h:.3f});")
        label: str = esc(n) + (f" {total[n]:g}" if args.totals else "")
        text: str = "white" if args.colour_by_source else "black!80"
        lines.append(f"\\node[rotate=90, font=\\fontsize{{7}}{{8}}\\selectfont, text={text}, inner sep=0pt] at ({x + w / 2:.3f},{top[n] - h / 2:.3f}) {{{label}}};")
    if titles:
        y_bottom: float = min(top[n] - total[n] * unit for n in order)
        for k, title in enumerate(titles[:ncols]):
            lines.append(f"\\node[font=\\fontsize{{8.5}}{{9.5}}\\selectfont, text=ink, anchor=north] at ({k * args.col_gap + w / 2:.3f},{y_bottom - 0.25:.3f}) {{{esc(title)}}};")
    lines += ["\\end{tikzpicture}", "\\end{document}", ""]
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[flows] wrote {args.out}: {len(order)} nodes in {ncols} columns, {len(parts)} bands, unit {unit:.4f} cm")


if __name__ == "__main__":
    main()
