# Pitfalls and fixes

Each of these cost at least one full rebuild cycle the first time.

## Layout

**Positions taken from `\tikzmarknode` never settle.** The mark coordinates come from the `.aux` of the previous pass. If a node placed from `m1.center` counts towards the bounding box, pass 1 puts it at a wrong place, the page grows, pass 2 moves the mark, and so on. Fix: every node and path positioned from a mark gets `overlay`, and the picture has `remember picture`. If the render still looks stale, `latexmk -C name.tex` and rebuild from nothing; `build_figure.py` runs latexmk, which reruns as often as needed.

**`|-` inside a calc expression with a mark coordinate resolves wrongly.** `($(P3.north east)+(-0.3cm,0)$ |- m1.center)` puts the node in the wrong place with no error. Fix: `\coordinate (bx) at ($(P3.north east)+(-0.3cm,0)$);` then `(bx |- m1.center)`.

**Figure is 0.5pt too wide, only the paper log says so.** pdftex sees an included PDF about 1.5pt wider than `pdfinfo` reports. With three 4.35cm cards (391pt) the standalone `border` may add at most 4pt left+right: `border={1pt 3.5pt 3pt 1.5pt}` (left bottom right top). Check `grep -c Overfull main.log` after rebuilding the paper. Never scale with `width=` to compensate; it shrinks the fonts.

**Shadows cut off at the right or bottom.** Shadows are not in the bounding box; that is what the 3pt/3.5pt right and bottom borders are for. Keep them.

**`minimum height` on a node leaks into a `\tikzmarknode` inside its text.** Setting `minimum height` (for example to match a neighbouring box via `let`) on a `doc` or `code` node also stretches every `hl` node in its text, and the outer node then grows around the stretched line. Reset it on the inner node: `\tikzmarknode[hl, minimum height=0pt]{m1}{phrase}`. `text width` does not leak; the nested picture resets it.

**A word in the document page hyphenates.** The `doc` style sets `execute at begin node={\hyphenpenalty=10000\relax}` (the braces are needed). If a word then overflows, shorten the sentence or widen `text width`; do not re-enable hyphenation.

**Table rows have different widths.** Give every column a `text width` in the matrix options. Header and data rows are measured separately otherwise.

**A footer text nearly touches the card edges.** Footer is 6.3pt; about 45 characters fit in a 4.35cm card, 40 in a 3.95cm card. Shorten the text; do not shrink the font below 6pt.

**Dotted table-to-class arrows pass through the table name.** Start them from the name node (`ben.north`), not from the matrix (`bemp2.north`).

**Cross-card alignment leaves one card half empty.** Place each card's content relative to its own card and accept different y positions across cards. Same-height pills and group labels are what the eye checks.

**The legend overhangs the cards and nothing warns.** The width verdict measures the page, and the legend is part of it, so a legend wider than the card row still passes as long as the page fits the text width. Budget it (0.11cm per character at 7pt, 0.46cm per swatch, `\legsep` between items) and, when it runs wide, shorten an item or `\renewcommand{\legsep}{\hspace{0.3cm}}`. For two cards use `\cardlegendspan{P1}{P2}{...}`.

**Straight quotes come out curly.** In the monospace font `'` is a right quote. Use `\textquotesingle` for SQL string literals and code.

**Indentation inside a code box disappears.** Leading spaces after `\\` are dropped. Indent with `~~` or reflow the line.

## Bar panels

**A system name runs into its icon.** `\barnamew` is a fixed column; the script sets it from the longest name, a hand-written file must. Budget 0.115cm per character at 7pt plus 0.15cm.

**The value label of the top bar is clipped or pokes past the other column.** `\barvaluew` reserves the space after a full-length bar. Four-digit values or a dagger need 0.85cm.

**Panels in the second row overlap the first.** `\barpanelpitch` is the distance between panel tops, not the gap: `\bartitlegap + rows*\barrowpitch + 0.5cm`. Recompute it when a panel gains a row.

**Bars in one panel look wrong compared with another.** `\barmax` is global on purpose. If one benchmark is on another scale, give that panel its own maximum (`\begin{barpanel}[10]...`) and put the unit in the title; do not change `\barmax` between panels.

**`\barrow` fails with `Missing number` or `Illegal unit`.** The value argument must be a plain number; a dagger, a percent sign or `--` belongs in the trailing optional label: `\barrow{Name}{}{88.3}[88.3$^\dagger$]`. A missing score is a missing row, not a zero bar.

**`\iconimg` cannot find the logo.** Paths are relative to the figure source; keep the logo files in `figures/` (or set `\graphicspath` in the figure file) and commit them with the source.

## Data plots (pgfplots)

**`Illegal parameter number in definition of \tikz@scan@point@coordinate` at `\end{axis}`, or a `\foreach` that draws all its paths at one place.** Paths inside an axis are executed at `\end{axis}`, when the `\foreach` variable is gone. Use `\pgfplotsinvokeforeach{0,1,2}{\draw ... (axis cs:#1,0) ...;}`, which substitutes `#1` textually, for `\draw` as well as for `\addplot`.

**A printed value comes out as `91.000000000`.** `visualization depends on={\thisrow{v} \as \cellv}` runs the cell through pgfmath. Write `visualization depends on={value \thisrow{v} \as \cellv}`; `value` keeps the text as written, and `\pgfmathtruncatemacro` can still test it.

**Digits in tick labels or printed values are in Computer Modern while the labels are sans.** pgfplots' default tick template is `$\pgfmathprintnumber{\tick}$`. The `paper` style replaces it with the text-mode template and sets `assume math mode=true`; a hand-written preamble must do the same, and a colour bar needs it in `colorbar style` because it is its own axis. Log axes take `xmode=log, log ticks x` (or `y`), whose ticks read 10, 100, 1000 in the text font; `xmode=log` alone prints the exponents. The `xmode` key itself must stand in the axis options: pgfplots scans them for it before any style runs, so an `xmode` hidden inside a style fails with "you can't change xmode in this context".

**A zero, a failure or a timeout vanishes on a log axis.** log(0) is minus infinity; pgfplots drops the point with a warning and nothing shows. Use a linear axis, or place the item outside the axis with a note and say so in the caption. Bars never go on a log axis (their length would depend on an arbitrary start); ratios may, starting at 1 with a `ref` line at 1.

**Blue and violet, or orange and gold, look alike to a red-green colour-blind reader, and all five hues print as one grey.** Measured with `scripts/palette_check.py` (deuteranopia: kept/dbB 15; protanopia: addc/gold 2). The palette is not changed, because the cards depend on it; the series survive through their solid marks and direct labels. Check any figure with more than three hues in greyscale, and prefer `cycle list name=paper accent` (ours blue, the field grey) or two panels.

**A bar chart with a raised `ymin` draws bars below the axis, or misstates every value.** `bars labelled` and `xbars labelled` pin the baseline at zero; do not override it. When the differences are invisible from zero, the chart is a dot plot (`dots.tex`), not a shortened bar chart.

**Two separate confidence whiskers, one per system, compared by eye.** Overlap says nothing reliable about the difference. Put the CI of the gain at the blue dot (`dumbbell.tex`), so the question "does the whisker reach the baseline dot" is the significance test.

**`Sorry, you can't change /pgfplots/xmode in this context` at `\end{groupplot}`, or `I do not know the key /tikz/xmode`.** A `\nextgroupplot` cannot switch its axis to log, and its options are processed with `/tikz` as the default path, so a style with bare pgfplots keys fails there. Panels that differ in axis mode are two `axis` environments placed with `name=` and `at={($(name.east)+(1.3cm,0)$)}, anchor=west`; styles meant for `\nextgroupplot` write their keys with the full `/pgfplots/` path (the ones in `plotfig.sty` do).

**A `.cd` inside a style changes the path for the keys that follow the style.** `/pgf/number format/.cd, precision=1` in a style body leaves the default path at `/pgf/number format/` for the rest of the option list that used the style, and the next key fails as `/pgf/number format/xmode`. Write `/pgf/number format/precision=1` with the full path instead.

**`\plab` inside a title comes out bold.** The title style is bold; `\plab` resets to `\mdseries` inside its own group and only for the letter. If the letter is still bold, the title text was wrapped in an extra `\textbf`.

**`File ended while scanning use of \pgfplotstableread@loop@next`.** An inline table must start on the line after `{` and the closing `}` must stand on its own line: `table {` newline `x y` newline rows newline `};`.

**The legend shows the default bar image, not the squares from `legend top`.** `ybar` and `xbar stacked` set their own `legend image code`. Put `legend top` after them in the option list.

**Row names vanish when the y axis is hidden.** `axis y line=none` removes the tick labels too. Use `y axis hidden` (axis line and ticks invisible, labels kept).

**Two direct labels overlap at the right edge.** Lines that end within about 4 points of each other need `yshift=3pt` on one label and `yshift=-3pt` on the other; there is no automatic repel.

**The flow diagram's quantity labels sit on a crossing.** `flows_from_csv.py` prints none by default (Wilke's parallel sets carry no numbers); `--label-min N` prints the bands of at least N at 80% of the way to the target, where bands have fanned apart. Move a node by reordering rows in the CSV.

**The bands of a parallel-sets diagram look grey and muddy where they overlap.** They were drawn in the house hues (`--palette house`, or an old file). The default `set*` colours are light bases whose 50% overlays blend into violet, green and orange; use them, and keep the opacity at 0.5.

**A node name in the flow diagram is longer than its bar.** Names are set vertically inside the grey bars, and a small category (a 10-record split) overflows above and below, as in the book. Shorten the name, raise `--height`, or merge the category; do not shrink the font.

**`enlarge x limits={upper=0.4}` does nothing, or not what it says.** `upper` is a flag, so the number is ignored and the default 0.1 applies; a second `enlarge x limits` in the same option list replaces the first; and the key acts only on automatic limits, so with an explicit `xmin`/`xmax` it is dead. Write `enlarge x limits={upper, value=0.4}` on an axis without explicit limits, or set `xmax` with room. Direct labels do not need it: `paper` sets `clip=false`, so a label hangs past the axis end and the standalone page grows around it.

**A horizontal bar chart prints 1, 2, 3 instead of the values.** `nodes near coords` reads the y coordinate, which on an `xbar` is the row index. Add `point meta=x` to the plot (`ablation.tex`, `funnel.tex`).

**`\closedcycle` closes to y = 0 and strokes the baseline.** A filled density with an outline therefore needs two plots, the fill with `draw=none` and `\closedcycle`, the outline without it (`densities.tex`); a ridge on its own baseline is closed by hand with `-- (axis cs:xmax,b) -- (axis cs:xmin,b) -- cycle` (`ridgeline.tex`).

**`log ticks y` prints 2.4998 for a tick at 2.5.** pgfmath's `10^x` is accurate to about four digits; the styles now print with `precision=3`, which rounds it away (1.5, 2, 2.5, 4 and 0.001 all print as written). If a tick still comes out odd, set `yticklabels` by hand for that axis.

**`\mono` is undefined.** `mono` is a node style (`\node[mono] {91.8}`), not a macro; inside running text (a node label that mixes words and a number) use `\ttfamily` for the number.

**The median tick of a strip vanishes.** It was drawn before the dots. In `strips.tex` the order is quartile box, dots, median tick.

**Two legends in a groupplot, or none.** For one legend over a grid, put `legend to name=<name>` and the `\addlegendentry` calls on the first `\nextgroupplot` only, and place `\pgfplotslegendfromname{<name>}` in a node after `\end{groupplot}` (`small-multiples.tex`); panels without entries create no legend of their own.

**The inset shows the whole curve, or has no frame.** An inset axis needs `clip=true` (`paper` sets `clip=false`), `axis lines*=box` (the starred form keeps the `paper` tick settings), `axis background/.style={fill=white}`, and its connector drawn after both axes from a saved `\coordinate` (`inset-zoom.tex`).

**`y label top` lands on a title, a legend or a top marginal.** All three own the top-left corner. Keep the rotated y label in a panel with a title (`roc-pr.tex`), with a `legend top` that would meet it (`stacked-counts.tex`), or under a marginal histogram (`scatter-margins.tex`).

**A direct label of one panel runs into the next panel's row labels.** In a row of separately placed axes the labels hang outside their own axis. Give the panel an explicit `xmax` with room, or shorten the label (`mixed-panels.tex`).

**`/tmp/...` paths in a Python heredoc on Windows.** Git Bash translates `/tmp/x` to the Windows temp directory only in command arguments; inside a Python script the string stays `/tmp/x` and the file is not found. Use the path the build script printed (`C:\Users\...\Temp\...`).

## Compile errors

**`Missing number, treated as zero ... \pgf@layerboxsaved@background`.** `\pgfsetlayers{background,shadow,main}` needs the `backgrounds` TikZ library. `cardfig.sty` loads it; a hand-written preamble must too.

**`Undefined control sequence \faFileAlt`.** Some fontawesome5 icons have an empty macro name. Use `\faIcon{file-alt}`; same for `share-alt`, `network-wired`, `book-open`, `project-diagram`.

**`drop shadow` does nothing on a matrix or a `rectangle split` node.** Both are drawn in pieces. Use `\boxshadow[]{name}` (square corners, for matrices) or `\boxshadow{name}` (2.5pt rounded, for class boxes); `\classbox` and `\classtag` already do it.

**`shadow opacity=0.45` makes the blur shadow invisible.** In `shadows.blur`, `shadow opacity` is a percentage (45). In `drop shadow`, `opacity` is a fraction (0.22).

**Nested `\tikz` inside a node.** Used by the legend helpers `\legswatch` and `\legline`. Works for a single node or path; do not put named nodes or `remember picture` inside them.

## Tooling

**Aux files land in the wrong directory.** Compile from the figure's directory (the build script does). Run `latexmk -c` afterwards; only `.tex` and `.pdf` are committed.

**Writing LaTeX through a Bash heredoc on Windows mangles backslashes** (`\\` collapses, `\f` becomes a form feed). Write and edit `.tex` files with the file tools, not with `cat <<EOF` or `sed`.

**The paper compiles but shows the old figure.** The PDF viewer is stale, or the figure PDF was not rebuilt, or the change is not pushed to Overleaf. Check the paper log for the figure's reported size (`<figures/name.pdf, id=..., 397pt x ...>`), then reopen the viewer.

**Reference figures to compare against.** SWE-bench Figure 1 (teaser.svg in the repository), Spider 2.0 Figure 1 and 2, BIRD Figure 1. Render an SVG with headless Chrome (`chrome --headless=new --screenshot`) via a small HTML wrapper when no other renderer is at hand.
