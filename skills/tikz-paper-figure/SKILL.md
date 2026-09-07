---
name: tikz-paper-figure
description: Paper figures as standalone TikZ/pgfplots files in one house style (Source Sans Pro, Inconsolata, fixed palette, blue = ours), with Wilke's chart-choice rules digested in a reference. Three templates: card-style teaser and method figures; benchmark bar panels generated from a CSV; data plots (curves with bands, training curves, scaling laws, grouped bars, ablations, waterfalls, funnels, dumbbells, slopegraphs, win/tie/loss, parity, Pareto, ROC/PR, calibration, heat maps, histograms, ECDFs, densities, ridgelines, box plots, strips, stacked shares, donuts, treemaps, Sankey flows, radar, small multiples, insets). Use whenever the user asks for any paper figure or chart or which chart to use: teaser, Figure 1, overview, pipeline, method figure, results or leaderboard figure, experiment plot, dataset statistics, redrawing a slide figure in TikZ, beautifying a TikZ figure, or says 画图, 先导图, 示意图, 方法图, 流程图, 美化这张图, 卡片风格, 柱状图, 折线图, 热力图, 散点图, 箱线图, 雷达图, 桑基图, 饼图, 实验图, 消融图, 组合图, 用什么图, even when TikZ is not mentioned.
license: MIT for SKILL.md, references and scripts; CC0-1.0 for everything under assets (see LICENSE-ASSETS in the repository)
compatibility: Needs TeX Live or MiKTeX with latexmk, pgfplots 1.18+, tikzmark, fontawesome5, sourcesanspro and inconsolata, poppler (pdfinfo, pdftoppm) and Python 3.9+ on PATH; scripts/check_env.py verifies all of it.
---

# Paper figures in TikZ and pgfplots

The card style comes from the Figure 1 of SWE-bench, Spider 2.0 and BIRD: a row of cards, one point per card, a single concrete example running through all of them, text large enough to read at 100% zoom. What makes those figures work is restraint, a handful of big elements per card, and colour that carries the same meaning everywhere. The cards, bands and shadows are decoration around that; they make the figure look finished, but they cannot rescue a crowded one.

Everything visual lives in `assets/cardfig.sty` (palette, geometry, TikZ styles, macros). A figure file only places elements. Finished figures with their renders sit in `assets/examples/`; `references/gallery.md` shows all thirty-six on one page with the question each answers. Open the render closest to the figure at hand before drawing; it is the target.

The same package holds a second template, **benchmark bar panels**, for results figures: a grid of small panels, one benchmark each, horizontal bars sorted best first with our system in blue. A sibling package, `assets/plotfig.sty`, styles **pgfplots data plots** (curves, bars, dots, heat maps, scatter, distributions, stacked shares, donuts, flows, radar) with the same fonts and palette, so every figure of one paper sits together without a seam. The rules for choosing a chart and for colour, axes, grids and captions come from Wilke's *Fundamentals of Data Visualization*, digested in `references/principles.md`; read it whenever a figure shows numbers. The card workflow is sections 1 to 5 below; bar panels and data plots have their own sections after it; revising and delivering apply to all three.

## Workflow

### 1. Decide the content before writing any TikZ

Write down, in a few lines, the answers to these questions. The figure fails or succeeds here.

- **How many cards, and what is the one message of each.** The title is that message in one to three words. Cards are either *parallel points* (numbered badges that match an enumeration in the text, an orange pill per card) or *stages of a process* (plain titles, stage arrows in the gaps, footer bands that read as one sentence left to right).
- **The running example.** Take it from a listing, table or example already in the paper, so the reader meets the same names twice. Keep it tiny: two tables of two or three rows, two or three classes, one sentence of document.
- **What is orange.** Exactly the thing the paper claims is hard or new: the link the inputs do not state, the value no field holds, the element a step adds, the cell that changed. Everything else stays blue (target side, accepted result), teal/violet (two sources or two kinds of input) or grey (present but not in play). If two things want to be orange in one card, the card has two messages; split or cut.
- **The footer band.** What the card is contrasted with: the assumption of earlier work, the input, the previous stage. One short clause, lowercase, no period, under about 45 characters at 6.3pt.

### 2. Set up the files

- Once per machine, run `python <skill>/scripts/check_env.py`. It lists the TeX and poppler tools the scripts need and says what each missing one breaks. When it fails, tell the user before drawing anything and do not promise a render (see Delivering).
- Copy `assets/cardfig.sty` next to the figure sources (usually `figures/`) if it is not there yet. The paper repository must contain its own copy; Overleaf compiles from the repository alone.
- Copy `assets/template.tex` to `figures/<name>.tex`. It has the class line with the right `border`, the geometry lengths, and commented placeholders for each element.
- Read `references/elements.md` for the building blocks and their code, and open the example source closest to the figure at hand (`teaser-points.tex` for parallel points, `pipeline-stages.tex` for stages, `io-two-cards.tex` for an input/output pair with a code block).

### 3. Place the elements

Plan each card on paper first with the size table in `references/elements.md` (row heights, characters per cm, legend width). The longest cell value and the legend decide the layout more often than anything else: a 13-character cell does not fit beside a document page, and a four-item legend does not fit under two narrow cards.

Place everything relative to its own card: `($(P1.north west)+(0.3cm,-1.2cm)$)`. The body area runs from `-\cardhh` (below the title bar) to `-\cardh+\cardfh` (above the footer); with pills, content ends above `-\cardh+\cardfh+0.55cm`. Keep 0.25 to 0.3cm from the card edges, and 0.9cm on the left when a connector runs down that side. Set `\cardh` once, for the tallest card.

Do not force elements in different cards onto the same coordinates when that leaves a large empty region in one card. Same *kind* of alignment matters more: pills at the same height (the macro does this), group labels on one line across a card, a result chip level with the row it comes from.

### 4. Build and look

```
python <skill>/scripts/build_figure.py figures/<name>.tex --png-dir /tmp/cardfig
```

The script compiles with latexmk from the figure's directory, cleans the aux files, prints the page size with a width verdict, and renders a PNG into `--png-dir` (default: the system temp directory; use `.` to deliver the PNG next to the source). On a compile error it prints the `!` lines with the `l.NN` line that locates them. Read the PNG with the Read tool every time; the log does not show overlaps, hyphenation or misalignment. Check:

- nothing touches or crosses a card edge; footer text has air on both sides
- no hyphenated word in a document page or a pill (the `doc` style forbids hyphenation; shorten the text instead of widening the page)
- table rows even (every column has a `text width`), highlighted cell border not clipped by its neighbour
- arrows leave from and arrive at the right anchors, none passes through a label or another cell
- shadows visible at the right and bottom (the standalone `border` leaves room; do not reduce it)
- width verdict `ok`; three 4.35cm cards with 0.35cm gaps are the maximum for a 5.5in text width
- a legend stays within the outer edges of the card row (the width verdict does not check this)

Iterate until the render is clean. Two or three rounds are normal.

### 5. Put it in the paper

- `\includegraphics{<name>.pdf}` with no width option; the figure is designed at text width and scaling changes the font sizes. `\graphicspath{{figures/}}` in the main file.
- The caption's first sentence is the figure's title and states its point ("The mapping the inputs do not state"), never "This figure shows". Then the reading key (what the colours mean, what the footer bands are) and what the figure cannot show on its own. It does not repeat the pills or the titles.
- Above the `figure` environment, add the project's usual comment block (in the paper's working language) recording what each card shows, the colour semantics, which listing the example comes from, and any decision a later editor should know.
- Rebuild the paper and check `grep -c Overfull <main>.log`; a figure 0.5pt too wide shows up there and nowhere else.
- Commit the PDF together with the source.

## Benchmark bar panels (results figures)

The target is `assets/examples/bench-bars.png`: a 2 x 3 grid of panels, each a bold benchmark name over six rows, each row a system name, a small logo, a grey bar and the score in monospace at the bar's end. Our system's bar is blue. There are no axes, ticks or grid lines; every bar in the figure is drawn on the same scale (`\barmax`, 100 for percentages), so a short bar in one panel means a low score, not a different axis.

1. **Put the numbers in a CSV**, one row per system, one column per benchmark, an optional `icon` column (`letter:K`, `letter:K:kept`, `fa:sun:addc`, `img:logos/x.pdf`, or raw LaTeX). Take the numbers from the paper's results table so figure and table agree to the decimal.
2. **Generate the figure file:**
   ```
   python <skill>/scripts/bars_from_csv.py results.csv --ours "Ours" --cols 2 --out figures/<name>.tex
   ```
   The script sorts every panel best first (`--lower-better "Latency"` for metrics where less is better; `--keep-order` when the rows are an ordered variable such as model sizes or difficulty tiers, whose own order carries meaning), paints the `--ours` system blue, sets `\barnamew` from the longest name, `\barpanelpitch` from the largest row count and `\barmax` from the value range (`--max` to force it). Panels fill the grid left to right, then down, in CSV column order; put the columns in the results table's order. Titles come from the CSV headers, so a header carries its unit (`Latency (s)`). When every value in a panel lies in a narrow band (the shortest bar longer than about 70% of the longest), bars from zero all look alike; that panel is a dot plot on an axis cut to the range (`assets/examples/plots/dots.tex`).
3. **Build and look** with `build_figure.py` as for cards. Check that no name touches its icon (raise `\barnamew`), that the longest value label stays inside the panel width (raise `\barvaluew`), that the panels have the same air between them vertically and horizontally, and that the title is not wider than the panel.
4. **Include** with `\includegraphics{<name>.pdf}` and no width option. The caption names the metric of each panel when the titles do not, states that the blue bar is our system, that bars share one scale and that rows are sorted within each panel, and does not repeat the winners. Panels get no (a)/(b) letters; their titles identify them.

Hand-written panels use the same macros (see `assets/template-bars.tex`): `\begin{barpanel}{col}{row}{Title}` with zero-based grid positions, and one `\barrow[ours]{name}{icon}{value}` per system, best first. A panel on another scale takes `\begin{barpanel}[10]{...}`; a printed label that differs from the number goes in a trailing optional argument, `{88.3}[88.3$^\dagger$]`. Three columns fit at `\barpanelw` 4.2cm; a single panel at text width is a bar chart with very long bars, so use one or two columns.

Rules that differ from the card template: no shadows, no frames, black text, and its own two colours, the bright `barblue` (007DFF) for ours against `bargrey` (E7E7E7) for everyone else (orange `ours2` for one more system that the text singles out, such as an ablation). Do not swap in the card blue; it reads as dull beside grey bars. Logos are decoration; when a system has none, leave the icon empty rather than inventing one. Sort by the value shown, or keep the variable's own order when the rows are ordered; never alphabetically.

## Data plots (pgfplots)

`assets/plotfig.sty` is loaded instead of `cardfig.sty` (copy it into `figures/` too). Its `paper` axis style bakes in what Wilke, Tufte and the PGF manual ask for: axis lines left and bottom only, a light grid perpendicular to the variable of interest, grey tick labels, digits in the text font, the y label horizontal above the axis, bars from zero, solid marks, series named at their line ends, one colour per system reused across all figures. The thirty-two renders in `assets/examples/plots/` are the target (all on one page in `references/gallery.md`); `references/principles.md` says why each rule exists and which chart answers which question; `references/plots.md` lists every style and gives the recipe for each chart.

1. **Pick the chart from the question the paragraph asks**, with the decision tables in `references/principles.md` and the grouped tables in `references/plots.md`, which map every question to an example file. Growth over data or time: lines with bands; training runs: seeds behind the mean; a power law: log-log dots with a trend. Up to three systems on a few benchmarks: grouped bars with printed values; more systems: bar panels (previous section). Values all in a narrow range: dot plot. Removing components: ablation bars; adding them up: waterfall; a pipeline's yield: funnel; errors by kind: stacked counts. Gains over a baseline on few rows: dumbbell; over many items: parity scatter; two conditions: slopegraph; judge preferences: win/tie/loss bars. Cost against quality: Pareto scatter. Classifiers: ROC beside precision-recall, a reliability diagram for calibration. A large table or a transfer matrix: heat map. How a statistic is distributed: histogram, ECDF for heavy tails, densities for two or three groups, a ridgeline along an ordered variable, box plots per system, strips below ten items, a scatter with marginals for two variables at once. Shares: two-segment stacked bars, donuts with at most four slices, a treemap for two nested variables. Where data goes: flows coloured by origin. Several panels: small multiples with shared ranges, two panels on one x instead of two y axes, an inset where curves converge, mixed chart types with `\plab` letters.
2. **Copy the closest example** from `assets/examples/plots/` (or `assets/template-plot.tex` for a plain line chart) to `figures/<name>.tex`, replace the data, keep the sizes unless the figure has a different slot. Flow diagrams (parallel sets) are generated from a records CSV whose header names the variables: `python <skill>/scripts/flows_from_csv.py records.csv --out figures/<name>.tex`. Treemaps likewise from a `group,item,value` CSV: `python <skill>/scripts/treemap_from_csv.py data.csv --out figures/<name>.tex`.
3. **Name every series on the plot** (`node[dl] {Ours}` at the line end, `legend top` for bars, in the order of the data), print values where the reader will quote them, add at most one annotation, and one reference line if the text compares against one (human, chance, previous best, x = y). More than three hues in one plot means two panels, or `cycle list name=paper accent` (ours in blue, the field in greys).
4. **Build with `build_figure.py`**, read the PNG at 100%, and check the list at the end of `references/plots.md`: no two labels touch, no Computer Modern digits, lines above bands and grids, every series still told apart in greyscale by its mark or label.
5. **Include** at natural size. The caption's first sentence states the point; it then names the metric and the colour meaning once (ours is blue in every figure), says what every band or whisker is (quantity, level, n), and notes a log axis, jitter, a smooth, or a panel on its own scale. It does not repeat what the direct labels already say.

## Revising an existing figure

A revision request names one change; everything it does not name is a constraint. Before touching the file, write two lists in the reply: what changes (the legend position, one added reference line, a renamed series, a fourth card) and what stays (the data, the palette and the meaning of each colour, fonts and type sizes, axis ranges, the page width, the position of every element not named). Then edit only the lines that carry the change. Do not regenerate the figure from a template, and do not re-tune the rest of the layout while there; a revision that also improves three other things cannot be reviewed. For a generated figure (bar panels, flows, treemap) the change goes into the CSV and the generator runs again; numbers are never edited in the `.tex`.

Rebuild, read the render, and put both versions on one sheet:

```
python <skill>/scripts/compare_sheet.py --out /tmp/before-after.png "before=figures/<name>.pdf" "after=figures/<name>2.pdf"
```

When the user wants to compare, write the new version to `<name>2.tex`, leave the old files untouched, switch the `\includegraphics` to the new file and deliver the sheet. Otherwise edit in place; version control keeps the old one. The reply says which elements were added, moved or removed and shows that the keep list held; `diff` of the two sources (or of the two CSVs) is the evidence.

## Delivering

Hand over the source, the PDF and the PNG render, and the include line for the paper (`\includegraphics{<name>.pdf}`, no width). State which checks ran: compile clean, width verdict, render read at 100%, the `Overfull` grep when the paper itself was rebuilt. When latexmk or pdftoppm is missing (`scripts/check_env.py` says so), say that the figure was not compiled or not rendered and stop at the source; do not describe a render nobody has seen, and do not report a check that did not run.

## Design rules

- **Type sizes.** Title 8.5pt bold, body 6.5 to 7pt, footer 6.3pt, never below 6pt. Identifiers (table, column, class, file names) in the monospace font; prose in the sans.
- **One shadow system.** Cards get the blurred shadow, every inner element gets the 0.7pt hard shadow (`sh` style, or `\boxshadow` for matrices and class boxes). An element without a shadow looks pasted on; a second shadow style looks like two figures glued together.
- **Colour is semantic.** Blue `kept` for the target side and for what is kept, accepted or extracted; orange `addc` for the difficulty or for what a step adds; teal `dbA` and violet `dbB` for two sources or two kinds of input (teal alone when there is one); grey for present-but-not-in-play. Keep the same meaning across all figures of one paper, and give the meaning in the first caption or a legend. Colour is never the only difference between two things the reader must tell apart: blue and violet are alike to a deuteranope, and every hue of this palette prints as the same grey, so series also differ by a solid mark and a direct label, and cards also differ by position and name (`scripts/palette_check.py` measures any palette).
- **The paper as a whole.** Three to six figures in the main text, ordered from closest to raw (the running example, score curves) to most derived (gains, ratios); each answers a different question with a different chart type while fonts, palette and the meaning of every colour stay identical. A results grid never appears in Figure 1.
- **Names carry the story.** Source-side names look like the source (`id`, `unit`, `parse.py`), target-side names like the target (`Employee`, `inUnit`, `resolved`), so the reader sees the gap the system has to bridge without being told.
- **Icons.** fontawesome5 for abstract notions in title bars and group labels (`database`, `sitemap`, `cubes`, `bug`, `code`, `vial`, `key`, `file-alt`, `code-branch`); the drawn cylinder `\dbicon` for databases in the body, because it takes the source colour. Icons decorate; they never replace a label.
- **Text in the figure.** Sentence case for titles, lowercase for footers and pills, no terminal periods, no abbreviations the paper does not use. A pill is one clause; if it needs a comma, it is two messages.
- **Nothing the paper text does not say.** The figure shows the problem or the procedure; it does not explain a method or a score unless the surrounding section does.

## Pitfalls

The ones that cost the most time are listed with their fixes in `references/pitfalls.md`. The two that bite first: elements positioned from `\tikzmarknode` coordinates need `overlay`, or the page never converges; and the standalone `border` plus card widths must stay under the text width minus 1.5pt, because pdftex sees included PDFs slightly wider than `pdfinfo` reports.

## Files

- `assets/cardfig.sty`: palette, geometry lengths, layers, all TikZ styles (tables `tblA/tblB/tblK`, chips, `code`, class boxes, edges, `caplab`), and the macros `\cardpanels`, `\cardhead`, `\cardheadn`, `\cardicon`, `\cardfoot`, `\cardpill`, `\cardstage`, `\cardlegend`, `\cardlegendspan`, `\boxshadow`, `\pageshadow`, `\foldcorner`, `\dbicon`, `\dbchip`, `\classbox`, `\classtag`, `\docpage`, `\keyic`; plus the bar-panel template: lengths `\barpanelw`, `\barcolgap`, `\barpanelpitch`, `\barnamew`, `\bariconw`, `\barvaluew`, `\barrowpitch`, `\barh`, `\bartitlegap`, macro `\barmax`, environment `barpanel`, command `\barrow`, icon helpers `\iconletter`, `\iconfa`, `\iconimg`.
- `assets/plotfig.sty`: pgfplots counterpart of cardfig (same fonts and palette): axis styles `paper`, `log ticks x`, `log ticks y`, `y label top`, `legend top`, `both grids`, `no grid`, `bars labelled`, `xbars labelled`, `y axis hidden`, `x axis hidden`, `boxes`; plot styles `band`, `runs`, `trend`, `ecdf`, `box ours`; cycle lists `paper` and `paper accent`; colormaps `paperblues` and `paperdiv`; `\plab` panel letters; TikZ styles `dl`, `dlc`, `note`, `notearrow`, `ref`, `mono`; text colours `addctext`, `goldtext`; light `setpink`, `setblue`, `setyellow`, `setgreen`, `setviolet`, `setorange`, `setgrey` for translucent overlapping fills.
- `assets/template.tex`: card skeleton to copy.
- `assets/template-bars.tex`: bar-panel skeleton to copy (or generate the file with `bars_from_csv.py`).
- `assets/template-plot.tex`: line-chart skeleton with direct labels and a reference line.
- `assets/examples/plots/` (+ `.png` each; all described in `references/gallery.md`): amounts `grouped-bars`, `dots`, `ablation`, `waterfall`, `funnel`, `stacked-counts`; gains `dumbbell`, `parity`, `slope`, `win-tie-loss`; trends `curves-bands`, `training-curves`, `scaling-law`, `pareto`; classifiers `roc-pr`, `calibration`; distributions `histogram-ecdf`, `densities`, `ridgeline`, `boxplots`, `strips`, `scatter-margins`; composition `stacked-100`, `donuts`, `treemap` (+ `treemap.csv`; generated), `flows` (+ `flows.csv`; generated); matrices `heatmap`, `radar`; composites `small-multiples`, `stacked-panels`, `inset-zoom`, `mixed-panels`.
- `assets/examples/teaser-points.tex` (+ `.png`): three parallel points with badges and pills; document page with highlighted phrases, chips, question badges, a table with a highlighted cell.
- `assets/examples/pipeline-stages.tex` (+ `.png`): three stages with stage arrows; tables with a foreign key and a greyed table, class boxes with key icons, dotted derivation arrows, an added superclass, legend.
- `assets/examples/io-two-cards.tex` (+ `.png`): two cards, input and output; question page, schema tables, code block with highlighted tokens, blue result table, legend spanning both cards.
- `assets/examples/bench-bars.csv`, `bench-bars.tex` (+ `.png`): six benchmarks in a 2 x 3 grid, six systems, letter and icon logos, generated from the CSV.
- `references/gallery.md`: every example render on one page, grouped by template and ordered by the question it answers, each with its source path and recipe pointer; `assets/examples/gallery.png` is the same as one contact sheet.
- `references/elements.md`: every card and bar-panel building block with its code and the reason for its shape.
- `references/principles.md`: digest of Wilke's *Fundamentals of Data Visualization* with chapter links: decision tables for choosing a chart (amounts, proportions, distributions, paired data, trends, uncertainty, overlapping points), the rules for colour, axes, grids, labels, captions and multi-panel figures, and the places where this skill deviates from the book on purpose. Read before choosing any data plot.
- `references/plots.md`: which chart for which question, the plotfig styles, sizes, one recipe per chart, checklist.
- `references/pitfalls.md`: compile and layout problems and their fixes, including the pgfplots ones.
- `scripts/check_env.py`: lists the TeX, poppler and Python pieces the other scripts need and what each missing one breaks; exit status 1 when a required one is absent.
- `scripts/build_figure.py`: compile, clean, width check, PNG render.
- `scripts/bars_from_csv.py`: results CSV to a sorted bar-panel figure file (`--keep-order` for ordered rows).
- `scripts/flows_from_csv.py`: parallel-sets diagram after Wilke from a records CSV (variables as columns, optional `count`), or from a source,target,quantity edge list with `--edges`: grey node bars with vertical names, translucent bands in the light set colours, coloured by the leftmost variable and grouped by colour in every node, variable names beneath the columns.
- `scripts/treemap_from_csv.py`: squarified treemap from a `group,item,value` CSV: one light hue per group, a lightness ladder for its items, numbers printed where they fit, group names in header strips.
- `scripts/palette_check.py`: pairwise colour distances under simulated colour-vision deficiency and in greyscale, for a list of hex values or a `.sty`.
- `scripts/compare_sheet.py`: stacked before/after image.
- `scripts/gallery_sheet.py`: tiles all example renders into `assets/examples/gallery.png`; run after adding or re-rendering an example.
