# Data plots (pgfplots) with plotfig.sty

`assets/plotfig.sty` gives pgfplots the same fonts and palette as the card figures and bakes in the conventions
that make a plot read well in print: only the left and bottom axis lines, a light grid perpendicular to the
variable of interest, grey tick labels, digits in the text font, bars from zero, solid marks, series named at
the line ends instead of in a legend box, one colour per system across every figure of a paper. The reasons
behind these defaults, and the decision tables for choosing a chart, are in `principles.md` (a digest of
Wilke's *Fundamentals of Data Visualization*); read it first. Thirty-two finished plots with their renders sit in
`assets/examples/plots/` (all of them on one page in `gallery.md`); start from the one closest to the chart at hand.

## Which chart

The tables are grouped by the question the paragraph asks. Read the question column first; the data type alone
does not pick the chart.

**Amounts and comparisons**

| question the figure answers | chart | example |
|---|---|---|
| how do up to three systems compare on a few benchmarks, absolute values matter | grouped bars with the value on every bar, the compared variable on position | `grouped-bars.tex` |
| how do more than three systems compare on several benchmarks | bar panels, one per benchmark (`barpanel`, cardfig.sty) | `assets/examples/bench-bars.tex` |
| how do systems rank when every value lies in a narrow range | dot plot on an axis cut to the range, values printed | `dots.tex` |
| which component matters most when removed from the full system | ablation bars with the drop printed, a `ref` line at the full score | `ablation.tex` |
| how do the components add up from the baseline to our score | waterfall: two full bars from zero, floating deltas between them | `waterfall.tex` |
| how much of the raw collection survives each construction stage | funnel bars in process order with the retained share | `funnel.tex` |
| how many errors does each system make, and of what kind | stacked count bars with the total printed above each stack | `stacked-counts.tex` |

**Gains and paired data**

| question the figure answers | chart | example |
|---|---|---|
| how much did we gain over the baseline on about ten benchmarks or fewer | dumbbell; the whisker is the CI of the gain | `dumbbell.tex` |
| did we improve item by item over many items, or is the shift systematic | parity scatter with the x = y line and no grid | `parity.tex` |
| which systems gained and which lost between two conditions, and by how much | slopegraph, one line per system, names left, values right | `slope.tex` |
| how often do judges prefer ours over each opponent | centred win/tie/loss bars: ties on zero, wins to the right, losses to the left | `win-tie-loss.tex` |

**Trends over an ordered x**

| question the figure answers | chart | example |
|---|---|---|
| how does a score grow with data, compute or time, for several systems | lines with confidence bands, direct labels | `curves-bands.tex` |
| how do training runs converge, and how much do seeds scatter | loss curves on a log y axis, seeds as faint `runs` behind the mean | `training-curves.tex` |
| does a metric follow a power law, and does it predict the next point | log-log dots with a `trend` over the fitted range and a hollow held-out mark | `scaling-law.tex` |
| which systems are worth their cost | cost vs quality scatter with the Pareto frontier, both grids | `pareto.tex` |

**Classifier quality**

| question the figure answers | chart | example |
|---|---|---|
| how do classifiers trade false positives for recall; which is best when positives are rare | ROC beside precision-recall, AUC in the labels, chance as `ref` | `roc-pr.tex` |
| is the system's confidence honest | reliability diagram: accuracy per confidence bin against the x = y line, ECE printed | `calibration.tex` |

**Distributions**

| question the figure answers | chart | example |
|---|---|---|
| how is one statistic distributed (lengths, items per group) | histogram, one bar per integer for small counts | `histogram-ecdf.tex` (a) |
| how is a heavy-tailed statistic distributed per system | ECDF on a log x axis, direct labels | `histogram-ecdf.tex` (b) |
| how does one statistic differ between two or three groups | overlaid translucent densities labelled at the peaks, no y axis | `densities.tex` |
| how does a distribution shift along an ordered variable, four or more levels | ridgeline of densities, the groups on the y axis | `ridgeline.tex` |
| how do per-item scores or latencies spread, per system, with dozens of items | box plots, ours in blue | `boxplots.tex` |
| how do a handful of seeds or runs per system spread (n below about ten) | jittered strips with a quartile box and a median tick | `strips.tex` |
| how do two variables relate, and how is each distributed on its own | scatter with marginal histograms | `scatter-margins.tex` |

**Composition and shares**

| question the figure answers | chart | example |
|---|---|---|
| what is each group made of, in shares, when only the drift matters | 100% stacked bars with every value printed; two segments when one category is the message | `stacked-100.tex` |
| what is the dataset made of, one dimension per donut, at most four slices | donuts with the total in the hole | `donuts.tex` |
| how do two nested categorical variables split the whole (source, then domain) | treemap from a CSV: hue per group, lightness per item, numbers printed | `treemap.tex` via `scripts/treemap_from_csv.py` |
| how do three or more categorical variables relate (source, domain, split) | parallel sets from a records CSV, bands coloured by the leftmost variable | `flows.tex` via `scripts/flows_from_csv.py` |

**Matrices and many dimensions**

| question the figure answers | chart | example |
|---|---|---|
| how does every source transfer to every target; any table of more than about 30 values | annotated heat map, rows in a stated order; signed values on `paperdiv` | `heatmap.tex` |
| how do systems compare on many capabilities at once | radar; only when the text discusses the shape, three systems and six axes at most | `radar.tex` |

**Composite figures**

| question the figure answers | chart | example |
|---|---|---|
| how does one relation (score against size) hold across many benchmarks | small multiples: one panel per benchmark, shared ranges, one legend above the grid | `small-multiples.tex` |
| how do two quantities (accuracy and cost) move with the same x | two panels stacked on one shared x axis, never two y axes | `stacked-panels.tex` |
| how does a run look overall, and how do the curves end where they converge | line chart with an inset magnifying the end region | `inset-zoom.tex` |
| how good, how it scales and how it transfers, in one figure | three chart types in a row, aligned baselines, `\plab` letters | `mixed-panels.tex` |
| two panels that cannot share a groupplot (a linear histogram beside a log ECDF) | two axes placed with `name=`/`at=`, `\plab` letters | `histogram-ecdf.tex` |

A bar chart with values printed needs no y axis. A line chart with direct labels needs no legend. A heat map
needs its numbers printed when the reader is meant to quote them. A third quantitative variable on a scatter
goes into a printed label or a second panel, never into bubble size or a third axis. Lines join points only
when x orders them; between unordered categories draw bars or dots. Two quantities over one x are two stacked
panels, not two y axes.

## Styles in plotfig.sty

| style | what it does |
|---|---|
| `paper` (axis) | width 6cm, height 4cm, `scale only axis`, axes left and bottom only, grey ticks and labels, light y grid, `paper` cycle list, tick labels and values in the text font, `clip=false` |
| `log ticks x`, `log ticks y` | with `xmode=log` (which must stand in the axis options itself): ticks read as the values (10, 100, 1000; 1.5, 2, 2.5 on a loss axis) in the text font |
| `y label top` | y label horizontal above the axis instead of rotated beside it |
| `legend top` | legend as a row of squares above the plot, no frame, entries in the order the bars appear; put it **after** `ybar` or `xbar stacked` in the option list |
| `both grids`, `no grid` | grid in both directions with no axis lines (scatter); no grid at all (parity plot, which has the diagonal) |
| `bars labelled` | vertical bars with `nodes near coords`: `ymin=0`, no y axis, no grid, values at 5.8pt monospace with one decimal |
| `xbars labelled` | the same for horizontal bars: `xmin=0`, row names kept, no x axis; add `point meta=x` to the plot so the value, not the row index, is printed |
| `y axis hidden`, `x axis hidden` | keep the tick labels (row names), draw neither the axis line nor the ticks |
| `band` (plot) | translucent fill for `fill between`: `\addplot[band, fill=kept] fill between[of=u and l];` |
| `runs` (plot) | thin faint lines for individual seeds or draws behind the mean |
| `trend` (plot) | a fitted curve or smooth, dark grey, no marks; its form and parameters go in the caption |
| `ecdf` (plot) | `const plot, no marks` for a cumulative distribution |
| `boxes`, `box ours` (axis, plot) | horizontal box plots: grey quartile box, whiskers to 1.5 IQR, dark median; `box ours` on the blue one |
| `dl`, `dlc` (TikZ) | direct label right of a line end / above a point, 6.5pt |
| `note`, `notearrow` | grey annotation text and its thin arrow |
| `ref` | dashed grey reference line (human, chance, previous best, x = y); the only dashed line in a figure |
| `mono` | 6pt monospace for printed numbers; a node style (`\node[mono]`), inside running text use `\ttfamily` |
| `\plab{a}` | panel letter for a title: `title={\plab{a} accuracy (\%)}`, not bold, one case per paper |
| cycle list `paper` | kept blue, addc orange, dbA teal, dbB violet, gold, grey; solid marks *, square, triangle, diamond, pentagon, * |
| cycle list `paper accent` | kept blue, then three greys: for "ours against the field" |
| colormaps `paperblues`, `paperdiv` | white to blue for amounts (default); orange, white, blue for signed values with a symmetric `point meta min/max` |
| `setpink`, `setblue`, `setyellow`, `setgreen`, `setviolet`, `setorange`, `setgrey` | light colours for translucent overlapping fills (parallel sets, overlaid densities, treemap groups) at `opacity=0.5`; overlaps blend cleanly; `setgrey` for node bars |

Colours: `kept` and `barblue` for ours (the bright `barblue` in bar, dot, strip and box charts against grey, `kept` in
line and scatter charts), `addc` for a regression, a negative delta or a second system the text singles out,
`black!20`/`black!45` for two baselines in bar charts (the lighter grey is the older or weaker one, legend in that
order), `black!60`/`black!40` for two baseline lines, `bargrey` for a bar track. Text in orange is `addctext`.
Ordered groups (model sizes, tiers) take a lightness ladder of one hue (`kept!25` to `kept!85`), unordered
groups take the `set*` hues. Palette distances under colour-vision deficiency and in greyscale:
`python scripts/palette_check.py --sty plotfig.sty --only kept,addc,dbA,dbB,gold` (blue/violet and orange/gold
are the weak pairs; every series therefore has its own solid mark and a direct label).

## Sizes

| use | axis size | note |
|---|---|---|
| single plot in a two-column figure | width 6cm, height 4cm | fits `0.48\textwidth` with labels |
| two panels side by side (`groupplots`) | width 4.9cm, height 3.5cm, `horizontal sep=1.15cm` | 12.6cm total; 4.6cm and `1.4cm` when the right panel has a y label |
| bar chart across the text width | width 9.4cm, height 3.2cm | five groups of three bars at `bar width=0.3cm` |
| dot plot or dumbbell | 0.32cm per row, width 5.4 to 6.2cm | `ymin=0.4`, `ymax=rows+0.6` |
| ablation, funnel | 0.38cm per row, width 6cm | `xbar, bar width=0.25cm`; the value and its suffix need about 1.6cm after the longest bar |
| waterfall | 0.4cm per row, width 5.8cm | six rows are 2.7cm |
| win/tie/loss | 0.54cm per row, width 6.2cm | segments 0.32 above and below the row |
| stacked count bars | width 5.6cm, height 3.6cm | `bar width=0.46cm`; the totals need about 6% headroom |
| box plots | 0.5cm per row, width 6cm | `boxes` sets `box extend=0.52` |
| strips | 0.65cm per row, width 6cm | eight dots per row at `mark size=1.6pt` |
| densities | width 6cm, height 3.4cm | no y axis |
| ridgeline | width 6cm, height 4.6cm for six ridges | baselines 0.6 units apart, ridges 0.9 high |
| slopegraph | 4.6cm between the columns, height 4.4cm | ends in one column at least 0.3cm apart |
| parity scatter | width = height = 4.2cm, equal ranges | same unit on both axes, so equal scale |
| calibration | width = height = 4.2cm | `ybar interval`, ten bins |
| ROC and PR | two squares of 3.6cm, `horizontal sep=1.3cm` | 10.5cm total |
| scatter with marginals | main 5.3 x 3.4cm, marginals 1.1cm, gaps 0.15cm | 7.7 x 5.6cm in all |
| heat map | width = height = 4.6cm for 6 x 6 | 0.77cm per cell; colour bar adds 0.9cm |
| stacked bars | width 8.6cm, height 2.5cm for four rows | `bar width=0.34cm`, `enlarge y limits=0.18` |
| treemap | `--width 6.2 --height 4.2` | header strips 0.3cm; a cell needs about 1 x 0.55cm to carry name and value |
| radar | 4.6cm | labels add about 1cm on every side |
| parallel sets | `--height 5.4`, `--col-gap 3.7` | 12.1cm for four variables; three at `--col-gap 4.2` are 9.3cm; nodes 0.46cm wide |
| small multiples | panels 3.5 x 2.4cm, `horizontal sep=0.5cm`, `vertical sep=1.1cm` | a 3 x 2 grid is 12.1cm wide; the vertical sep holds the next row's titles |
| stacked panels | width 6cm, heights 2.6cm and 2.0cm, `vertical sep=0.65cm` | the sep holds the lower panel's `y label top` |
| inset | 2.3 x 1.5cm inside a 6 x 4cm axis | 5.5pt tick labels |
| mixed panels | heights 3.2cm, widths 3.8, 4.0 and 3.2cm, gaps 1.35cm | 13.8cm, the text-width maximum |

`width`/`height` are the axis box because of `scale only axis`; labels and legends come on top. Set them in
the figure and include the PDF at natural size; scaling with `width=` in `\includegraphics` shrinks the fonts.

## Recipes

**Direct labels.** `\addplot ... coordinates {...} node[dl, text=kept] {Ours};` puts the name at the last
point. With `clip=false` (set by `paper`) the label may hang past the axis end and the standalone page grows to
fit it. To keep it inside the axis instead, give an explicit `xmax` with room: `enlarge x limits` acts only on
automatic limits, and its amount is written `enlarge x limits={upper, value=0.4}` (`upper=0.4` is silently
ignored, and a second `enlarge x limits` replaces the first). When two lines end within about 4 points of
each other, add `yshift=3pt` to one label and `yshift=-3pt` to the other. Marks stay on sparse series (they
show where the measurements are) and go (`no marks`) on dense ones; with labels present, shapes are not
identifiers.

**Confidence bands.** Two invisible paths and a translucent fill, drawn before the line so the line sits on top:
```latex
\addplot[name path=u, draw=none, forget plot] coordinates {...upper...};
\addplot[name path=l, draw=none, forget plot] coordinates {...lower...};
\addplot[band, fill=kept] fill between[of=u and l];
```
The caption says what the band is: "95% CI over 5 seeds at every x", or "95% confidence band of the fit"
(which is hourglass shaped). Two nested bands (`fill opacity` 0.24 inside 0.10) only with one or two series.

**Seeds behind the mean.** Every seed as `\addplot[runs, kept] coordinates {...}` first (the style carries
`forget plot`, opacity 0.3 and a 0.45pt line), then the mean as `no marks, line width=0.9pt` with a `dl` at its
end (`training-curves.tex`). Loss goes on `ymode=log, log ticks y`. A vertical `ref` (end of warm-up) carries its
`note` at the top with `anchor=north west`, inside the axis, so it does not meet `y label top`. Up to about a
dozen runs per series; beyond that, bands.

**Reference line and annotation.** `\addplot[ref, forget plot] coordinates {(xmin,86) (xmax,86)} node[dl, text=black!55] {human};`
and one `note` with a `notearrow` for the finding the paragraph is about. One annotation, not three. A line
chart without a grid needs at least one reference line.

**Trend or smooth.** `\addplot[trend] coordinates {...}` over the visible raw points, never beyond the data;
the caption names the method and its window or the fitted form with its parameters. A power law is a straight
`trend` on `xmode=log, ymode=log, log ticks x, log ticks y`. A moving average is plotted at the centre of its window.

**Scaling law.** Measured models as `only marks` dots, the fit as a two-point `trend` from the first to the
last model it was fitted on and no further, the form once as a `note` beside the line (`$L = 4.2\,C^{-0.09}$`;
math digits are Computer Modern, acceptable in a formula). A held-out model is a hollow `mark=o` with
`mark options={line width=0.7pt}` and a `dl` shifted `xshift=1.5pt` so the text clears the ring
(`scaling-law.tex`). If `log ticks y` still prints an odd decimal for a tick, set `yticklabels` by hand.

**Values on bars.** `bars labelled` (vertical) or `xbars labelled` (horizontal, for labels longer than about
eight characters) plus `nodes near coords`; values are read from the y (or x) coordinate and the baseline is
pinned at zero. Horizontal bars need `point meta=x` on the plot, or the row index is printed. Numbers come out
in the text font because the style sets `assume math mode=true`. Three series per group at most; more systems
go to bar panels.

**Ablation.** `xbars labelled` with `xbar, bar width=0.25cm, point meta=x`; the full model as its own
`\addplot` in `barblue`, the variants in one `black!30` plot, both with `bar shift=0pt`. The drop is a text
column read with `visualization depends on={value \thisrow{d} \as \dropv}` and appended to the score in
`nodes near coords={\pgfmathprintnumber{\pgfplotspointmeta}\hspace{2pt}\textcolor{addctext}{\textminus\dropv}}`.
A `\draw[ref]` at the full score goes first; the number nodes carry `fill=white, inner xsep=1.5pt` so the dashed
line stops where a number crosses it (`ablation.tex`). Rows are sorted by score below the full model.

**Waterfall.** Rectangles in `axis cs` after an invisible `\addplot` fixes the limits: two full bars from zero
(baseline grey, ours `barblue`), the deltas as floating bars from the previous running total (`barblue!65`,
`addc` when negative), a thin `black!40` connector from each bar end to the next row, the amounts printed on the
full bars and the signed deltas (`$-$0.8`) on the floating ones (`waterfall.tex`). Rows stay in the order the
components were added.

**Funnel.** `xbars labelled` plus `xbar, bar width=0.25cm, point meta=x`, then
`/pgf/number format/precision=0` after the style so counts print as `48,200`. Stages keep their process order
top to bottom; the retained share is a text column (`64\%`, an empty `{}` cell for the first row) read with
`visualization depends on={value \thisrow{s} \as \share}` and printed after the count at 5.2pt in `black!55`.
The last stage is a second plot in `barblue` with `bar shift=0pt` (`funnel.tex`).

**Stacked counts.** `ybar stacked, bar width=0.46cm`, then `legend top`, one `\addplot coordinates` per
category in the `stacked-100.tex` colour order (`kept`, `dbA`, `addc`, `black!25`) with `symbolic x coords`
and `xtick=data`. The y axis, `ylabel={errors (count)}` and the light grid stay because the totals differ; the
total sits above each stack as `\node[mono, text=black!70, anchor=south, yshift=1.5pt] at (axis cs:Ours,86)`.
The rotated y label is used because `y label top` would meet the legend (`stacked-counts.tex`).

**Win/tie/loss.** No bar plot: one invisible `\addplot` fixes the limits, then every segment is a rectangle in
`axis cs` with its share printed at `($(axis cs:x0,y)!0.5!(axis cs:x1,y)$)` (the local `\seg` macro in
`win-tie-loss.tex`). Per row: tie from −t/2 to t/2 in `black!12`, loss from −t/2−l to −t/2 in `black!45`, win
from t/2 to t/2+w in `barblue`. The headers are `\addlegendimage{fill=...}\addlegendentry{...}` under
`legend top`, in the left-to-right order of the segments; `xticklabel={\pgfmathparse{abs(\tick)}\pgfmathprintnumber{\pgfmathresult}}`
prints unsigned ticks. Drop a label when its segment is under about 6%.

**Dot plot.** One `only marks` plot for the field in `black!45` and one for ours in `barblue`, `xmajorgrids`,
`y axis hidden`, rows sorted by value (ordered variables keep their order), `xmin`/`xmax` at the data range,
and a `\node[dl, mono, xshift=2.5pt]` with the value after every dot, so the truncated axis cannot mislead.

**Strips (small n).** The dot plot's frame (`xmajorgrids, y axis hidden`, rows named by `yticklabels`, x cut
to the data). Per row: a `\fill[black!10]` rectangle from Q1 to Q3 (0.24 row heights above and below) first,
then one `only marks` plot with `mark size=1.6pt, fill opacity=0.75, draw opacity=0` at (score, row + a fixed
jitter within 0.14), then a `\draw[ink, line width=1.2pt]` tick at the median, after the dots or it disappears
under them. Ours in `barblue` with a `barblue!18` box, the field `black!45`. Jitter is precomputed so the render
is deterministic; the caption states n and that the jitter runs along the row only (`strips.tex`).

**Histogram.** `ybar` with numeric x, one bar per integer (`xtick={1,...,8}`, `bar width` a little under the
tick spacing), a single `fill=kept, draw=none`, `ymin=0`, the count axis kept, x titled with the statistic and
its unit. Try two or three bin widths before choosing; equal widths only.

**ECDF.** `\addplot[kept, ecdf] coordinates {(x0,0) ... (xmax,1)} node[dl] {Ours};` on `xmode=log, log ticks x` when the
statistic is heavy tailed, `ymin=0, ymax=1`, `ylabel={cumulative fraction}`. One colour per system, no legend.
Every ECDF ends at 1, so line-end labels collide: place the names where the curves are apart, with `\node[dl]`
above-left of the leftmost curve's step and below-right of the rightmost one's (`histogram-ecdf.tex`).

**Overlaid densities.** Two or three groups of one statistic as closed-form curves
(`\addplot[density] {1000/(x*s*2.5066)*exp(-(ln(x)-mu)^2/(2*s^2))}` with a local
`density/.style={domain=5:600, samples=120, no marks, line width=0.7pt}`), each drawn twice: once with
`draw=none, fill=setblue, fill opacity=0.5` and `\closedcycle`, then once as the outline in `setblue!70!black`.
All fills before all outlines, the tallest fill first, so the overlaps blend and no outline is dimmed
(`\closedcycle` strokes the baseline, which is why fill and outline are separate plots). `axis y line=none,
ytick=\empty, ymajorgrids=false`: a density carries no numbers. Name each curve with `\node[dlc]` at its peak
in the outline colour. The domain starts above 0 for a lognormal (`ln(0)` fails) (`densities.tex`).

**Ridgeline.** Ridge k sits on baseline 0.6k: `{0.6*k + c*exp(-(x-m)^2/(2*s^2))}` with c chosen so every
ridge has the same area, closed along its own baseline with the trailing path
`-- (axis cs:100,b) -- (axis cs:0,b) -- cycle` (`\closedcycle` would close to y = 0). Draw the top ridge
first; each lower ridge covers the one above and is separated by `draw=white, line width=0.8pt` (a dark outline
adds a rule under every ridge and competes with the curves). Fills are a lightness ladder `kept!25` to
`kept!85` because the groups are ordered. `ytick` at the baselines with the group names, `y axis hidden`,
`axis on top` so the x axis line survives the bottom ridge's white edge (`ridgeline.tex`). More ridges lower
the spacing; keep about 0.9 units of ridge height for 0.6 of spacing.

**Box plots.** Axis options `boxes` (adds `boxplot/draw direction=x`), one
`\addplot[boxplot prepared={draw position=k, lower whisker=, lower quartile=, median=, upper quartile=, upper whisker=}] coordinates {};`
per row, `box ours` on our system; items beyond the whiskers as a separate `only marks` plot at (value, k).
Caption: box = quartiles, whiskers to the last value within 1.5 IQR, n per box. Fewer than about ten items per
group: strips instead of boxes.

**Parity scatter.** `width = height`, equal `xmin/xmax` and `ymin/ymax`, `ymajorgrids=false`, the diagonal as
`\addplot[ref] coordinates {(0,0) (100,100)};` first, points with `fill opacity=0.55, draw opacity=0` because
rounded scores tie, two `note`s naming the half-planes, one annotated point at most.

**Scatter with marginals.** Main axis `name=main, no grid`, points `fill opacity=0.55, draw opacity=0`, y
range cut to the data (dots need no zero). Top marginal: a second axis `at={(main.north west)}, anchor=south west,
yshift=0.15cm`, the same `width` and `xmin/xmax`, `axis lines=none, xtick=\empty, ytick=\empty,
ymajorgrids=false, ymin=0, ybar interval=0.9`, one `\addplot[fill=barblue!60, draw=none]` over the bin edges
(the last coordinate closes the last bin). Right marginal likewise at `(main.south east)` with `xshift`, the
same `height` and `ymin/ymax`, `xbar interval=0.9` with coordinates (count, edge). The plot areas align by
themselves because `paper` sets `scale only axis` and the anchors are the axis rectangle. The y label stays
rotated: `y label top` would sit inside the top marginal (`scatter-margins.tex`).

**Slopegraph.** `xmin=0, xmax=1`, the two condition names as x tick labels set at the top
(`axis x line*=top, x axis line style={draw=none}, xtick style={draw=none}`), `axis y line=none, ytick=\empty,
ymajorgrids=false`. One `\addplot[colour, mark=*, mark size=1.5pt, line width=0.7pt] coordinates {(0,l) (1,r)}`
per system with `node[pos=0, dl, anchor=east] {Name\enspace\lv{l}}` and `node[pos=1, dl, mono] {r}` (`pos=`
works on pgfplots paths; `\lv` is a local 6pt grey `\ttfamily` macro for the left value). Ours `kept` at 1pt,
systems that got worse in `addc`, the rest `black!45`. Keep the ends in each column at least 0.3cm apart, or
`yshift` a label (`slope.tex`).

**Text in nodes near coords.** To print a table column as written (and to test it with `\ifnum`), read it with
`visualization depends on={value \thisrow{v} \as \cellv}` and use `\cellv`; without `value` the number is
printed as `91.000000000`. Skip small labels: `nodes near coords={\pgfmathtruncatemacro{\vv}{\cellv}\ifnum\vv>7 \cellv\fi}`.

**Heat map.** `matrix plot*` with `mesh/cols=N`, `point meta=explicit`, `y dir=reverse`, `enlargelimits=false`,
the default `paperblues` colormap with fixed `point meta min/max`, white text on cells above the midpoint,
white 1pt grid lines and the diagonal outline drawn with `\pgfplotsinvokeforeach`. Rows and columns in one
deliberate order (by the last column, by row total), named in the caption. Signed cells (gain over a baseline):
`colormap name=paperdiv` with `point meta min=-M, point meta max=M`. With the values printed the colour bar can
go (`colorbar=false`, as in `mixed-panels.tex`).

**Dumbbell.** Connectors as `\draw` in `axis cs` first, then one `only marks` plot per colour; the whisker at
the blue dot is the CI of the gain, `error bars/.cd, x dir=both, x explicit` with `+- (ci,0)` after each
coordinate, so a whisker that reaches the grey dot means the gain does not exclude zero; gains as
`\node[dl, mono]`. Drop the caps (`error mark=none`) beyond about eight rows. Speed-ups or x-fold gains go on
`xmode=log, log ticks x` with a `ref` line at 1.

**Pareto frontier.** `both grids`; `const plot` through the non-dominated points, sorted by x, with the last
point repeated at `xmax`; the dominated region as a `\fill[barblue!7]` rectangle drawn before the plots. A zero
cost or a failed run cannot sit on the log axis; the caption says where it went.

**ROC and precision-recall.** `groupplots`, `group size=2 by 1`, shared 0 to 1 ranges and ticks `{0,0.5,1}`
with explicit labels, titles `\plab{a} ROC` and `\plab{b} precision--recall`, rotated `xlabel`/`ylabel` per
panel (a `y label top` would meet the title). Curves `no marks`, the weakest drawn first; the diagonal as `ref`
in (a); in (b) a horizontal `ref` at the positive rate with `node[dl] {chance}`. Labels carry the AUC. At
3.6cm a label is about half the axis wide and every tangent placement is crossed by a curve, so the three
labels stand stacked in the empty lower right of (a), in curve order and colour; set them along the curves in
wider panels (`roc-pr.tex`).

**Reliability diagram.** Square `paper` axis with 0 to 1 on both axes, `y label top`, one
`\addplot[ybar interval, fill=barblue!75, draw=white, line width=0.4pt]` over the bin edges (the last y is
ignored; `ybar interval` goes on the plot, not the axis, so the `ref` diagonal drawn after it stays a line), a
`note` with the ECE in the upper left and one rotated 45 degrees above the diagonal reading "perfect
calibration". Per-bin counts are stated in the caption, not printed: in the low bins the bars touch the diagonal
(`calibration.tex`).

**Stacked shares.** `xbar stacked`, one `\addplot table[x=v, y=row, meta=v]` per category, `point meta=explicit`;
the last (grey) category gets `every node near coord/.append style={text=black!70}` in its own options. Every
percentage printed, or two segments only. When a majority flips across rows, one `ref` line at 50.

**Donuts.** `\donut{position}{centre text}{title}{value/colour/label, ...}` from `donuts.tex`; values in
percent, drawn clockwise from the top, label anchor picked by the sign of `cos(mid angle)`. At most four
slices; slices under about 5% merge into "other"; each donut splits a different variable.

**Treemap.** `python <skill>/scripts/treemap_from_csv.py data.csv --out figures/treemap.tex --width 6.2 --height 4.2`
from a CSV `group,item,value`. Squarified layout, groups by total and items by value, one `set*` hue per group
and a lightness ladder (100% down to 55%) for its items, white separators (thin between items, 1.6pt between
groups), every cell carrying its name and number when they fit (about 1 x 0.55cm), the name alone in a
narrower cell, nothing below that. Each group's name and total stand in a white 0.3cm strip above its items
(`--header`), which is not part of the area; the total is dropped when the strip is too narrow. Merge items
that would fall below the label threshold into "other" before plotting (`treemap.tex`, `treemap.csv`).

**Flows (parallel sets).** `python <skill>/scripts/flows_from_csv.py records.csv --out figures/flows.tex` from
a CSV whose header names the categorical variables in column order, one row per record or per group with a
`count` column. The form is Wilke's bridges figure: every node a grey bar (`setgrey`) with a thin white
outline that trims the band ends (`--node-border`, 1.6pt), its name set vertically inside, the variable name
beneath each column (from the header, or `--columns`), every band in the
colour of the leftmost variable, and within a node the bands grouped by colour first, then by the other end,
which keeps one colour together and crosses least. The bands use the light `setpink`, `setblue`, `setyellow`
(then green, violet, orange) at 50% opacity: these are the bases of the book's own bands, and their overlaps
blend into clean violet, green and orange, where the house hues turn grey (`--palette house` if the paper's
colours must carry over). No numbers unless `--totals` (after the node name) or `--label-min N` (on bands of at
least N). Put the variable the reader should follow leftmost; reorder rows to reorder nodes; avoid categories
of one or two records, which become hairlines. An edge list `source,target,quantity` goes in with `--edges`
(columns inferred from the longest chain; a flow out of a middle node is split among origins in proportion,
which is exact only when records are given). Four variables at `--col-gap 3.7 --height 5.4` are 12.1cm wide
(`flows.tex`); three at `--col-gap 4.2` are 9.3cm.

**Radar.** `polaraxis` with `grid=none` and the polygon grid drawn by `\pgfplotsinvokeforeach`; close every
polygon by repeating the first point at 360; `fill opacity` 0.10 to 0.18; `legend image code` as squares.

**Two panels.** `groupplots` with `group style={group size=2 by 1, horizontal sep=1.15cm}`; options shared by
both panels (including `ymin`/`ymax`, so the scales match) go on the `groupplot` environment, the title on each
`\nextgroupplot[title={\plab{a} ...}]`. One legend, on the first panel only. When one panel must have its own
scale, the caption says so. Panels of different kinds (a linear histogram beside a log ECDF, bars beside
lines) cannot share a groupplot, because `xmode` cannot change per panel: give the first axis `name=left` and
place the second with `at={($(left.east)+(1.3cm,0)$)}, anchor=west`, as `histogram-ecdf.tex` does. A panel
title and `y label top` both sit at the top left; use one of them, and let the title name the y quantity.

**Small multiples.** `groupplots` with `group style={group size=3 by 2, horizontal sep=0.5cm, vertical sep=1.1cm,
x descriptions at=edge bottom, y descriptions at=edge left}`; everything the panels share (`xmode=log`, ticks,
`ymin`/`ymax`, `xlabel`) goes on the `groupplot` environment, each `\nextgroupplot[title={...}]` carries only
its data. One legend for the grid: `legend to name=smlegend` on the first panel only, `\addlegendentry` after
each of its plots, then `\node[anchor=south] at ($(group c2r1.north)+(0,0.55cm)$) {\pgfplotslegendfromname{smlegend}};`
after the grid. The vertical sep must hold the next row's titles. Add a panel by changing `group size` and
appending a `\nextgroupplot`; titles identify the panels, no letters (`small-multiples.tex`).

**Stacked panels (shared x).** `group style={group size=1 by 2, vertical sep=0.65cm, x descriptions at=edge bottom}`
with `xmode=log`, ticks and `xlabel` on the `groupplot`, so x is set once at the bottom; each `\nextgroupplot`
sets its own `height`, `ylabel` (with `y label top`) and y range (groupplots accept different heights). Direct
labels at the line ends in both panels, one `note` in the panel the paragraph is about; explicit `xmin`/`xmax`
give the labels room. A third quantity is a third `\nextgroupplot` and `group size=1 by 3` (`stacked-panels.tex`).

**Inset.** The inset is a second `axis[paper]` placed with `at={(main.south east)}, anchor=south east,
xshift=-0.3cm, yshift=0.4cm`, with `clip=true` (`paper` sets `clip=false`), `axis background/.style={fill=white}`,
`axis lines*=box` in `black!30`, 5.5pt `tick label style`, and the window's `xmin/xmax/ymin/ymax`; the same
series in the same colours, from one point outside the window. The main axis draws the window as
`\draw[black!35, line width=0.4pt] (axis cs:80,76) rectangle (axis cs:100,86);` and saves `\coordinate (zoomcorner)`
at one corner; the connector `\draw[black!30] (zoomcorner) -- (inset.north west);` comes after both axes. Move
the inset to another corner if it covers a curve (`inset-zoom.tex`).

**Mixed panels.** Three `axis` environments named `a`, `b`, `c`, the second and third placed with
`at={($(a.south east)+(1.35cm,0)$)}, anchor=south west`; the anchors are the axis rectangles, so baselines and
tops coincide whatever the labels do. Each panel takes its own chart's options (`bars labelled` + `legend top`;
`xmode=log, log ticks x`; `matrix plot*` with `nodes near coords`) and a title `\plab{a} ...`. A middle
panel's direct labels must fit inside its own width (explicit `xmax`), or they run into the next panel's row
labels. Because the title owns the top-left corner, a legend goes inside the plot area at the top
(`legend style={at={(0.5,1)}, anchor=north}` after `legend top`, with `ymax` leaving headroom). Shrink the
widest panel first when the width verdict is not ok (`mixed-panels.tex`).

## Checklist before including

- the chart answers the paragraph's question (`principles.md`); no line joins unordered categories
- every series is named on the plot, or the legend sits above it as a row of squares in the order of the data
- every colour has one job; the same system has the same colour, mark and order in every panel and figure
- in a greyscale render every series is still told apart by its mark or label; only `ref` is dashed
- bars and fills to the axis start at zero; a truncated range is used only with dots or lines and keeps its axis
- log axes read as values, name the variable, carry no bars, and hold no zero
- every whisker and band is named in the caption with its quantity, level and n
- the y label is horizontal above the axis (`y label top`) or dropped when the title says it; axis titles carry units
- digits are in the text font (no Computer Modern in tick labels or printed values)
- lines and bars are on top of bands, grids and tinted regions; the grid runs perpendicular to the variable of interest
- nothing in the figure is a claim the text does not make; one annotation at most; no title states the point inside the drawing
- panels of one figure share their scales, or the caption says which does not; compound panels carry `\plab` letters, small multiples do not
- in a composite, the plot areas have the same top and bottom, one legend serves the whole figure, and no label of one panel reaches into the next
- `build_figure.py` says `width ok`, and the PNG read at 100% shows no label touching another
