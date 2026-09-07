# Figure principles, from Wilke's *Fundamentals of Data Visualization*

Claus O. Wilke, *Fundamentals of Data Visualization* (O'Reilly, 2019; free at https://clauswilke.com/dataviz/) is
the source of most defaults in `plotfig.sty` and of the chart choices in `plots.md`. This file is the digest:
what the book asks for, why, and what that means in this skill. Each heading links to the chapter; read it when
a rule needs its argument. Read this file before choosing a chart; `plots.md` then gives the code.

The book's vocabulary for a failed figure: **ugly** (aesthetic problems only, still readable), **bad** (perception
problems: unclear, confusing, misleading), **wrong** (mathematically incorrect: a bar whose length does not
match its value). A figure that is none of the three is acceptable: informative, clear, printable as is.
[introduction](https://clauswilke.com/dataviz/introduction.html)

## Which chart answers which question

The paragraph asks a question; the chart is chosen for that question, never for the data type alone.
[directory-of-visualizations](https://clauswilke.com/dataviz/directory-of-visualizations.html)

**Amounts.** [visualizing-amounts](https://clauswilke.com/dataviz/visualizing-amounts.html)

| situation | chart | why |
|---|---|---|
| one categorical variable, values differ widely | bars from zero; horizontal when labels are longer than a short word; sorted by value unless the categories are ordered | a bar encodes its value by length, so its baseline is zero and its labels must stay horizontal |
| values all lie close together (every system between 85 and 92) | dots on an axis cut to the data range, values printed (`dots.tex`) | bars from zero would all be the same length and the eye would go to their middles |
| two categorical variables, few levels, one compared within groups | grouped bars, the compared variable on position, the other in colour; three series at most (`grouped-bars.tex`) | position is read directly, colour is matched against a legend |
| two categorical variables, no wish to encode colour | one small bar chart per group (bar panels) | the book's own preference over grouped bars |
| the sum of the parts is itself a quantity (counts, totals, 100%) | stacked bars with the total printed above each stack (`stacked-counts.tex`) | the top of a stack reads as a total; scores and means are never stacked |
| a table of more than about 30 values, or a transfer matrix | heat map with the rows ordered by a stated criterion, cells printed when they will be quoted (`heatmap.tex`) | colour is worse than position for single values and better for patterns over many cells |
| ordered categories (model sizes, difficulty tiers, years, data budgets) | any of the above in the variable's own order | sorting an ordered variable by value scrambles what the reader is tracking |
| one system with its components removed one at a time | horizontal bars from zero, the full model first, the drop printed after each score (`ablation.tex`); the additive reading is a waterfall from the baseline to the full score (`waterfall.tex`) | the absolute scores stay honest from zero, and the drop, which is the message, is printed rather than read off |
| the stages of a pipeline (collected, filtered, annotated, released) | bars in process order with the count and the retained share printed (`funnel.tex`) | a process order is an ordered variable |

**Proportions.** [visualizing-proportions](https://clauswilke.com/dataviz/visualizing-proportions.html),
[nested-proportions](https://clauswilke.com/dataviz/nested-proportions.html),
[proportional-ink](https://clauswilke.com/dataviz/proportional-ink.html)

| situation | chart | why |
|---|---|---|
| one whole, at most four parts, the message is a fraction or a majority | donut with the percentages printed (`donuts.tex`) | a pie shows that the parts make a whole; pieces cannot be compared precisely |
| the parts must be compared with each other, or there are five or more | sorted bars with values printed | bars share a baseline; areas are judged worse than lengths |
| the same categories across several groups or years | stacked bars with two segments (the category of interest against a grey remainder), or grouped bars, or small multiples; never a row of pies | middle segments of a stack sit on different baselines in every bar |
| several groups, many categories, only the overall drift matters | 100% stacked bars with every percentage printed (`stacked-100.tex`) | accepted by the book only with the numbers on the segments |
| three shares per row with a neutral middle (win, tie, loss against each opponent) | centred stacked bars, the tie on zero, wins to the right, losses to the left, percentages printed (`win-tie-loss.tex`) | the right ends compare wins and the left ends losses across rows; in a 100% stack only the first segment is comparable |
| a share along a continuous variable | one panel per part with the total in grey behind it; stacked densities only when the total is roughly constant | percent-of-total hides a changing whole |
| two nested categorical variables | treemap or mosaic with the count in every rectangle, hue for the outer level and lightness for the inner (`treemap.tex`, generated); never two rings | areas need the numbers to be verified; a double ring counts every item twice |
| three or more categorical variables | parallel sets: grey node bars, bands coloured by the leftmost variable and grouped by colour in every node, variables ordered so bands cross least (`flows.tex`, generated) | the reader follows one colour from left to right |

The slices of one donut or the segments of one stack partition the whole: they sum to 100 and no item is in two
of them. Overlapping categories go into side-by-side bars with the overlap shown.

**Distributions.** [histograms-density-plots](https://clauswilke.com/dataviz/histograms-density-plots.html),
[ecdf-qq](https://clauswilke.com/dataviz/ecdf-qq.html), [boxplots-violins](https://clauswilke.com/dataviz/boxplots-violins.html)

| situation | chart | why |
|---|---|---|
| one statistic (query length, tables per schema) | histogram with equal bins, one bar per integer for small counts, bars touching, one fill, y from zero (`histogram-ecdf.tex`) | bin width changes the picture; try several before choosing |
| the same statistic for two or three groups | overlaid translucent densities with outlines and labels at the peaks (`densities.tex`); for exactly two, a back-to-back histogram | stacked histograms have no baseline; overlapped bars read as a third colour |
| a heavy-tailed statistic, or quantiles matter, or the groups differ in size | ECDF on a log x axis, y = cumulative fraction, direct labels (`histogram-ecdf.tex`) | no bin width to choose and all the data shown; a linear axis makes a spike at zero |
| per-item scores or latencies for several systems | box plots (grey, ours in blue), violins only when every group has dozens of points, jittered dots with a quartile box when a group has fewer than about ten (`boxplots.tex`, `strips.tex`) | mean with symmetric error bars hides spread and skew |
| four or more distributions along an ordered variable | ridgeline of densities in the variable's order, no density axis (`ridgeline.tex`) | staggered histograms turn their bar edges into noise |

A density curve is an estimate: clip it at the domain bounds (no negative lengths), scale it to counts when the
groups differ in size, and do not draw one for a small sample or an integer statistic.

**Paired data and gains.** [visualizing-associations](https://clauswilke.com/dataviz/visualizing-associations.html),
[visualizing-uncertainty](https://clauswilke.com/dataviz/visualizing-uncertainty.html)

| situation | chart | why |
|---|---|---|
| about ten items or fewer, the value of each matters | dumbbell (`dumbbell.tex`) | per-item slopes show direction and size for a handful of rows |
| many items, or the message is a systematic shift | parity scatter with the x = y line and no grid (`parity.tex`) | under no effect the points scatter symmetrically around the diagonal |
| each item measured under two conditions (before and after, zero-shot and fine-tuned) | slopegraph, one line per item from the first value to the second, names and values at the ends (`slope.tex`) | the slope shows direction and size per item; a dumbbell shows the gap, a slopegraph the change |
| two quantitative variables, and how each is distributed on its own | scatter with marginal histograms (`scatter-margins.tex`) | the dense middle of a scatter hides both marginals |
| the claim is "ours beats the baseline" | the CI of the difference against a zero line | two separate intervals compared by eye are unreliable; the interval of the gain says whether it excludes zero |
| three or four quantitative variables | scatter matrix, coloured by group | position beats bubble size; beyond four, a correlogram with a diverging scale |
| a third quantitative variable on a scatter | a printed label or a second panel, never bubble area or a third axis | size is perceived far worse than position |

**Trends.** [visualizing-trends](https://clauswilke.com/dataviz/visualizing-trends.html),
[time-series](https://clauswilke.com/dataviz/time-series.html)

- Lines join points only when x orders them (time, data size, compute, a dose). Between unordered categories
  draw bars or dots; a line there asserts values that were never observed.
- Keep the marks when the series is sparse or unevenly spaced, and say "lines guide the eye" in the caption;
  drop them (`no marks`) when the series is dense. With direct labels, mark shapes are not identifiers.
- A handful of runs is shown as the runs themselves, thin and faint behind the mean (`training-curves.tex`);
  a power law is a straight `trend` on log-log axes fitted over the observed range only, with a held-out point
  as a hollow mark to show whether it would have predicted (`scaling-law.tex`).
- Fill under a curve only when y starts at zero. Bands between two paths are fine at any range.
- A smooth (moving average, LOESS, spline) is drawn in a distinct style (`trend`), over the visible raw points,
  never beyond the data, and the caption names the method and its window. A moving average sits at the centre of
  its window. Prefer a fit with a defined form and print its parameters in the caption; a power law is a
  straight line on log-log axes, an exponential on a log y axis.
- When the paragraph is about departures from a trend or a baseline, plot the difference or the ratio against a
  reference line at 0 or 1, not the two raw curves.
- Two response variables over the same x: two stacked panels sharing x. The book does not use dual y axes.

**Overlapping points.** [overlapping-points](https://clauswilke.com/dataviz/overlapping-points.html)
In order of severity: `fill opacity` about 0.5; then a small jitter (at most half the rounding step) stated in
the caption; then 2D bins coloured by count (reuse the heat map machinery) when no opacity serves both the dense
blob and the sparse tail; then density contours with small transparent points, one panel per group when groups
overlap.

## Colour

[color-basics](https://clauswilke.com/dataviz/color-basics.html), [color-pitfalls](https://clauswilke.com/dataviz/color-pitfalls.html),
[redundant-coding](https://clauswilke.com/dataviz/redundant-coding.html), [aesthetic-mapping](https://clauswilke.com/dataviz/aesthetic-mapping.html)

- Every colour has exactly one job: series identity, a data value, or a highlight. A colour with no job is grey.
- Identity: three to five hues, of equal weight (no lightness ladder among peers); from the sixth series on,
  merge into grey or split into panels, and name series with direct labels. Cycle list `paper`.
- Highlight: hue for ours (and orange for the one system the text singles out), greys of decreasing weight for
  the rest, so the accent does not compete with saturated baselines. Cycle list `paper accent`; bar panels and
  dot plots already do this with `barblue` on grey.
- Values: a single-hue map with monotonic lightness (`paperblues`); a diverging map (`paperdiv`) only around a
  meaningful midpoint (0, 50%, ratio 1) with `point meta min/max` symmetric about it. Never rainbow.
- Two shades of each hue: the light one for fills, the dark one for lines and text. Orange text at 6.5pt is
  `addctext`, not `addc`. Large saturated areas make neighbouring text hard to read.
- Translucent fills that overlap (parallel sets, overlaid densities) take the light `set*` colours at opacity
  0.5, recovered from the book's own bands: pink over blue reads as violet, blue over yellow as green. The house
  hues are too dark for this and their overlaps turn grey. Nothing in such a figure is "ours", so blue carries
  no claim there.
- Colour is never the only difference between series. Every series has a solid mark of its own shape and a
  direct label; dash patterns are not used on data lines (they look porous and are hard to match to a name).
  Solid shapes throughout: filled bars without dark outlines, filled marks, filled boxes; overlapping fills are
  translucent rather than tinted (`band`).
- Check the figure in greyscale and under a colour-vision-deficiency simulation:
  `python scripts/palette_check.py --sty figures/plotfig.sty --only kept,addc,dbA,dbB,gold`. Measured for this
  palette: blue/orange is safe for every observer; blue/violet is 15 under deuteranopia; gold/orange is 2 to 6
  under red-green deficiency; all five hues sit between L* 40 and 58, so a black-and-white print shows one grey.
  The marks and labels are what make a five-series line chart survive that; a chart that needs more than three
  hues is usually two panels.
- Legend entries follow the order the reader sees: highest line first, bars in the order they appear in a group.
  Better, no legend at all; and never a legend moved into the caption ("blue dots are X").

## Axes and scales

[proportional-ink](https://clauswilke.com/dataviz/proportional-ink.html), [coordinate-systems-axes](https://clauswilke.com/dataviz/coordinate-systems-axes.html),
[no-3d](https://clauswilke.com/dataviz/no-3d.html)

- Bars and any fill down to the axis start at zero on a linear scale (`bars labelled` and `xbars labelled` pin
  it). If the differences vanish from zero, switch to dots, or plot the difference; never shorten the axis.
- Dots and lines may use a truncated range, since a dot encodes position only, but the axis line and ticks stay
  visible and the range must not exaggerate a change relative to the whole. The book has no broken axes.
- Log axes for ratios and for values spanning orders of magnitude (`xmode=log, log ticks x`). Ticks read as the values
  (0.1, 1, 10), the axis title names the variable, never "log cost". No bars on a log axis, except ratios
  starting at 1 with a reference line at 1. A zero (failure, timeout, zero cost) cannot be shown on a log axis:
  use a linear axis, or mark it outside the axis and say so in the caption.
- Categories on a discrete axis are ordered deliberately: by the value shown, or by the paper's enumeration, or
  by the variable's own order; never alphabetically.
- With the same unit on both axes, equal scale: a square parity plot with width = height and equal ranges.
- No third position axis and no depth on data marks: no 3D bars, no tilted donuts, no shadows on plot elements.
  Card shadows stay on cards, which are schematics.

## Grids, frames, and the amount of context

[balance-data-context](https://clauswilke.com/dataviz/balance-data-context.html), [small-axis-labels](https://clauswilke.com/dataviz/small-axis-labels.html),
[avoid-line-drawings](https://clauswilke.com/dataviz/avoid-line-drawings.html)

- No frame around the figure, the plot area or the legend. Grid lines only perpendicular to the variable of
  interest: horizontal for values over x, vertical for horizontal bars and dot rows, both directions with no
  axis lines for a scatter with no primary axis (`both grids`), none for a parity plot, which has the diagonal.
  Major ticks only, light grey. A gridless line chart needs at least one reference line (`ref`).
- Both extremes are ugly: the data must dominate, and the tick labels, titles and a light grid must remain
  clearly visible. Text that carries a value or a name is never lighter than `black!60`.
- Check the render at print size (100% zoom, or a 3 to 5 inch wide PNG), not zoomed in; default label sizes
  are almost always too small. Marks, line widths and bar widths scale together with the text.
- In a grid of small panels, every panel needs a visible extent (a baseline or a light background) so bars do
  not float and panels do not merge.

## Labels, legends, and captions

[figure-titles-captions](https://clauswilke.com/dataviz/figure-titles-captions.html),
[redundant-coding](https://clauswilke.com/dataviz/redundant-coding.html)

- Every axis has a title with its unit in parentheses; drop the title only when the tick labels explain
  themselves (years, system names). A legend never has a title. Remove a whole axis only when the values are
  printed on the marks.
- The figure's one title is the first sentence of the caption, and it states the point, not the contents:
  "Ours gains most on the long-tail joins", never "This figure shows". Then the reading key: what the colours
  and marks mean, what a band or whisker is (quantity, level, n), that an axis is logarithmic, that points are
  jittered, what a smooth is, how the rows are ordered, and any panel whose scale differs. A panel title inside
  the drawing names a metric or a benchmark, not the point.
- Compound figures label their panels (a), (b), (c) at the top left in the figure's own font at body size, not
  bold, one case for the whole paper (`\plab`); the caption keys one clause to each letter. Small multiples get
  no letters; their row and column labels identify them.

## Uncertainty

[visualizing-uncertainty](https://clauswilke.com/dataviz/visualizing-uncertainty.html)

| display | use when | never |
|---|---|---|
| one error bar per estimate, caps optional | many estimates, expert readers | without saying what it is: SD, SE or CI, and the level |
| graded bars (80/95/99%, thicker and darker for lower confidence) | few estimates, to stop the reader taking the bar as min and max | in a dense figure |
| CI of the difference against a zero line (`dumbbell.tex` whisker) | the claim is "A beats B" | two separate CIs compared by overlap |
| one flat translucent band (`band`) | uncertainty of a curve at every x, or of a fit (hourglass shaped) | a fading gradient strip; readers cannot integrate shading |
| two nested bands | one or two series | three or more overlapping series |
| individual runs as thin faint lines (`runs`) | a handful of seeds, or a nonlinear fit whose band hides its wiggle | more than about fifteen lines |
| the raw observations as a jittered strip | small n, when spread matters more than the precision of the mean | hundreds of points per group (bin them) |
| bar with SE whisker | only when convention forces it | when spread or precision is the point; it shows neither |

The caption always states the quantity, the level and n for every bar or band, and whether a band is a fit band
or a per-x interval over runs.

## Multi-panel figures and the paper as a whole

[multi-panel-figures](https://clauswilke.com/dataviz/multi-panel-figures.html), [telling-a-story](https://clauswilke.com/dataviz/telling-a-story.html)

- Small multiples share axis ranges; when one panel must differ, the caption says so. Panels are ordered by a
  stated principle (results-table order, our margin), left to right then top to bottom (`small-multiples.tex`:
  one legend above the grid, tick labels only on the outer edges).
- Two quantities over the same x are two panels stacked on one shared x axis (`stacked-panels.tex`); an
  inset magnifies where curves converge and keeps their colours (`inset-zoom.tex`); panels of different chart
  types stand in one standalone with aligned baselines and `\plab` letters (`mixed-panels.tex`).
- Across panels and across figures, the same system keeps its colour, mark and position, and no colour is
  reused for another meaning. One legend per compound figure. Panels are built in one standalone so their axes
  and baselines align.
- The opening figure is "for the generals": one point readable in seconds, every dimension not serving it cut.
  Show one instance before the grid: the teaser carries a single running example, and a results grid never
  appears in Figure 1. Order the paper's figures from closest to raw (the example, score curves) to most derived
  (gains, ratios). Three to six figures in the main text; each answers a different question with a different
  chart type while fonts and palette stay identical.
- Icons and logos are decoration; in a technical paper clarity outranks memorability.
- Figures enter the paper as vector PDF (what the standalone build produces), never as a raster of the
  same drawing; PNG is for previews and for photographs or screenshots only, and every re-encoding of a
  raster blurs its text. [image-file-formats](https://clauswilke.com/dataviz/image-file-formats.html)

## Where this skill deviates from the book, on purpose

- **Values past the bar ends in bar panels.** The book says outside labels elongate the bars. The leaderboard
  genre (SWE-bench, Spider 2.0) puts the score at the bar end, and every bar in the figure shares one scale, so
  the panels stay in that form. Do not add this to other bar charts; `bars labelled` prints values above bars of
  a zero-based axis, which the book accepts.
- **Logos in bar panels and icons in card title bars.** Decoration, as the book says. Kept for genre
  recognition; never a substitute for a label, and empty when a system has none.
- **Shadows and frames on cards.** Cards are schematics, not data plots; the shadow is the card's edge. No
  shadow ever touches a data mark, a bar or a line.
- **Per-panel sorting in bar panels.** The book keeps one order across panels of a figure. Bar panels answer
  "how does ours rank", so each panel sorts by its own values and the caption says so. When the rows are an
  ordered variable, or the figure tracks one system across benchmarks, use `--keep-order`.
- **Four-segment 100% stacked bars.** Accepted by the book only with every percentage printed, which the
  example does; prefer two segments when one category is the message.
- **Charts the book does not cover.** ROC and precision-recall curves (`roc-pr.tex`), reliability diagrams
  (`calibration.tex`), win/tie/loss bars, waterfalls, insets and radar charts are common in machine-learning
  papers and have examples here. They follow the book's rules all the same: the reference line (chance, the
  diagonal) is the only dashed line, series are labelled on the plot, ours is blue, one annotation at most.
