# Classic style (classicfig.sty): Matplotlib's look, finished by hand

`assets/classicfig.sty` makes pgfplots look like Matplotlib's default output (version 2 and later) and adds the
touches a careful Matplotlib user puts on top: a light grid, markers with a white edge, direct labels, text
boxes, annotated key numbers, composite layouts. The eighteen examples in `assets/examples/classic/` are the
target; `references/gallery.md` shows them all, and `assets/examples/classic/gallery.png` tiles them on one sheet.
This file says when to use the style, how to turn new data into a figure, what each example teaches, which key
does what, and the craft collected while building the examples, each rule with its source.

Contents: [When](#when-to-use-it) · [Workflow](#workflow-for-new-data) · [Examples](#which-example-to-open) ·
[Keys](#the-keys-of-classicfigsty) · [Craft](#craft-what-makes-a-classic-figure-look-finished) ·
[Budget](#layout-arithmetic) · [Checklist](#checklist-before-delivering) · [Sources](#sources)

## When to use it

- The paper's other figures come out of Python, or the field reads Matplotlib as the default (chemistry,
  materials, physics, most of the natural sciences: spectra, diffractograms, kinetics, calibration lines).
- The user asks for the classic, Matplotlib or 经典 look, or sends a Matplotlib figure to match.
- Otherwise use the house style (`plotfig.sty`, `cardfig.sty`): it follows Wilke and suits ML papers, whose
  Figure 1 is a card figure anyway.
- RDF graphs and VOWL ontology schemas in this style are plain TikZ on `classicfig.sty`, with no axis; their
  notations, styles and layout rules are in `references/ontology.md`.

One style per paper. The two families differ in font (DejaVu Sans against Source Sans Pro), palette (tab10
against the house hues), frame (four spines and a legend box against two spines and direct labels) and in who
owns blue. `classicfig.sty` shares no colour name with `plotfig.sty`; never load both in one figure.

What the style keeps from Matplotlib's rcParams, and why a classic figure is recognisable at a glance: DejaVu
Sans 10pt with math in the same font (`mathastext`, true minus signs), title 12pt, a black frame of 0.8pt on all
four sides, ticks outside on the bottom and left only (3.5pt, minor 2pt), lines 1.5pt, the tab10 cycle, 5 %
margins around the data, and the legend in a rounded light grey frame on 80 % white. Polish goes on top of
these; it never replaces them. A classic figure with the top and right spines removed is no longer classic.

## Workflow for new data

1. **State the message and pick the chart.** One sentence the figure proves ("Pt₁/CeO₂ is 13 times more active
   than any nanoparticle catalyst"). The chart follows from the question, with the tables in
   `references/principles.md`; the table below maps each chart to the example that already solves it.
2. **Compute every number in Python, never in pgfmath.** Keep a small numpy script next to the figure, as
   `assets/examples/classic/data/make_data.py` does, and reuse its helpers: least-squares fits with confidence
   and prediction bands (`calibration`), Welch's t-test with the t distribution done by hand (`welch`,
   `t_quantile`), Gaussian KDE with Scott's bandwidth (`kde`), box statistics as `matplotlib.cbook.boxplot_stats`
   computes them (`boxstats`), covariance ellipses (`ellipse`), histograms on fixed edges. Series longer than
   about thirty points go into `data/<figure>.dat` (one header line, space separated) and are read with
   `table[x=..., y=...]`; short lists and the statistics are printed and pasted. pgfmath only draws curves whose
   parameters Python fitted (`declare function`). Figure and a Python check then agree to the last digit.
3. **Copy the nearest example**, keep its sizes (7.4 × 4.7 cm axis for one column, 14 cm total for a
   composite) and replace the data. Keep the comment block at the top and rewrite it: what the figure shows,
   where the numbers come from, which Matplotlib calls it imitates.
4. **Find the free space before placing any text.** Print the data extents per region (min and max of each
   series in the corners and bands you intend to use); do not judge empty space by eye on a render that still
   changes. Legends, text boxes, notes and labels go into regions the data leave empty; convert their size
   from points into data units first (see [Layout arithmetic](#layout-arithmetic)).
5. **Build and read the render.** `python <skill>/scripts/build_figure.py <name>.tex --png-dir .` compiles with
   pdflatex, or LuaLaTeX when the file starts with `% !TEX program = lualatex` (needed for `contour lua`). Read
   the PNG; then crop the crowded parts and read them at two to three times the size (a Pillow crop and
   resize). Thumbnails hide collisions and invent others.
6. **Iterate on collisions only.** Every round moves labels, shortens texts or changes one size; three to six
   rounds are normal for a composite. Recompute every rotated label after an axis changes size.
7. **Deliver** as in `SKILL.md` (source, PDF, PNG, the checks that ran), with the Python script and the data
   files beside the figure.

## Which example to open

Sources are `assets/examples/classic/<name>.tex`, renders beside them; data in `assets/examples/classic/data/`.

| Question or chart | Example | Techniques it shows |
|---|---|---|
| Data against a fitted model over time | `kinetics` | markers with white edges over fit lines, error bars drawn as a separate plot, half-lives as open circles on a dotted guide, halo labels with arrows, the model in the title note |
| A spectrum with weak and strong bands | `spectrum` | Gaussian model in `declare function`, fill coloured by wavelength, weak region redrawn ×10, a brace over a group of bands, conditions in a light box |
| Rates with uncertainty, one derived axis | `errorbars` | 95 % confidence bands with `fill between`, activation energies written along the curves, a secondary kelvin axis on top from an empty overlaid axis |
| Two quantities on one time axis | `twin-axes` | `twin right` and `twin color` (axis coloured like its series), process phases as spans with labels, a set-point line, no legend |
| A series of curves along an ordered variable | `waterfall` | offset traces coloured by plasma, reversed wavenumber axis, labels at the line ends, bands marked above the traces, a scale bar in place of y ticks |
| A distribution of one variable, two groups | `histogram` | stepfilled bars plus step outlines, normal fits scaled to counts, a wheat text box that is table and legend at once, `mpl spines on top` |
| Replicates per group, with a test | `boxplot` | light boxes over jittered points, medians redrawn on top, white diamond means, a target line, significance brackets with the test named in a note |
| Distributions whose shape matters | `raincloud` | half-violin KDE, slim box and raw points per group, a curved arrow to the bimodality the box hides |
| A few groups on a few conditions | `bars` | white bar edges, a hatched control, values inside tall bars and above short ones, fold-change bridges, one-row legend |
| A value on a grid of two factors | `heatmap` | annotated cells with the text colour chosen per value, a white cell grid, the best cell outlined, no spines |
| Several profiles over several criteria | `radar` | polar axis as a radar chart, the reference in grey and dashed drawn first, `reverse legend`, radial labels with halos |
| A scalar field in two dimensions | `contour` | filled contours plus contour lines (LuaLaTeX), a path cased white over dark, minima and saddles marked and labelled |
| A response surface | `surface3d` | mplot3d look rebuilt (panes, grid, view), contours projected on the floor, design points on stems, the optimum starred |
| A calibration line and its residuals | `calibration` | two panels 3 : 1, confidence and prediction bands, statistics box with LOD, residual stems with the ±2s band, aligned y labels |
| Two variables and both marginals | `joint` | scatter with 1σ and 2σ ellipses, marginal histograms with KDE, iso-yield curves, labels and legend in the empty corners |
| A pattern with one small feature | `xrd` | rotated peak labels with fanned leaders, an inset with a peak decomposition, zoom box and connectors that miss the labels, a mirrored reference panel |
| One value far above the rest | `broken-axis` | `mpl break upper` and `mpl break lower`, one bar across the break, a two-level category axis, one y label centred on both panels |
| Several views of one study | `subplots` | a mosaic (one tall panel, two short), one figure legend, panel letters on the title baseline, a semilog panel, a regeneration event |

## The keys of classicfig.sty

Axis styles (in the axis options):

| Key | Does |
|---|---|
| `classic` | the complete Matplotlib axis: frame, fonts, 7.4 × 4.7 cm, tab10, 5 % margins, legend frame, `clip mode=individual` so annotations are not clipped |
| `classic frame` | fonts, frame and ticks only, for polar, 3D, colour bars and secondary axes |
| `classic legend` | the legend frame alone, for axes built from `classic frame` |
| `legend upper left`, `legend upper right`, `legend lower left`, `legend lower right` | Matplotlib's `loc`, 5pt inside the frame |
| `mpl grid`, `mpl grid light`, `mpl ygrid light`, `mpl xgrid light` | the rc grid (grey, 0.8pt) or the light dashed grid of the polished examples |
| `mpl minor={x}{y}` | minor ticks per major step: Matplotlib's AutoMinorLocator puts 4 in a step of 1, 2.5 or 5 (times 10^k) and 3 otherwise; fewer on a short axis where they would crowd |
| `sticky ymin` | no margin at a limit the data stand on (bars, histograms) |
| `mpl log x`, `mpl log y` | 10^k tick labels; `xmode=log` itself must stand in the axis options |
| `twin right`, `twin color=C3` | the second axis of `twinx()`, and colouring its ticks and label |
| `classic colorbar={label}` | `fig.colorbar`: as tall as the axis, 1/20 as wide |
| `mpl imshow` | cells centred on integers, first row on top, axis on top |
| `mpl title left` + `\mpltitleright{note}` | title flush left and a grey note on the same baseline at the right |
| `mpl align ylabel=26pt` | the y labels of a column of panels at one distance from their spines |
| `mpl break upper`, `mpl break lower` | the two axes of a broken y axis, spine at the break hidden, cut marks drawn |
| `mpl figure legend={(point)}{anchor}` | an empty axis whose legend serves the whole composite |
| `mpl spines on top` | spines and ticks over the data; single axes at the origin only (pitfalls) |

Plot styles (in `\addplot` options): `mpl dashed`, `mpl dotted` (Matplotlib's dash patterns at 1.5pt);
`mpl scatter` (plt.scatter, s = 20, alpha 0.8); markers `mpl o`, `mpl s`, `mpl D`, `mpl ^` and `mpl edge` (white
marker edge, 0.8pt default); `mpl patch`, `mpl bar=<width>`, `mpl hist`, `mpl bar edge` (white edges),
`mpl hatch=<colour>`; `mpl stepfill` plus `mpl step` (stepfilled histogram and its outline); `mpl band`
(fill_between at 0.2 without legend entry); `mpl yerr`, `mpl yerr black`, `mpl yerr thin` (error bars with
caps); `mpl box`, `mpl fliers` (plt.boxplot with `boxplot prepared`).

TikZ styles (on `\node` and `\draw`): `mpl text` (10pt), `mpl small` (8pt), `mpl arrow`, `mpl arrow filled`,
`mpl arrow both` (annotate arrows, shortened 2pt), `mpl box`, `mpl box wheat`, `mpl box light` (text boxes),
`mpl gap` (a white casing under a line), `panel label` (bold panel letter). Note that `mpl box` on an
`\addplot` is the box plot and on a `\node` the text box; the two live in different key families.

Macros (inside an axis): `\axhline[opts]{y}`, `\axvline[opts]{x}`, `\axhspan[opts]{y0}{y1}`,
`\axvspan[opts]{x0}{x1}`, `\sigbracket[opts]{x1}{x2}{y}{label}`, `\halo[colour]{text}`; after an axis:
`\panellabel[opts]{name}{a}`; for broken axes: `\mplbreakmark{coordinate}`.

Colours: `C0` to `C9` (tab10, the names Matplotlib accepts), `C0L` to `C9L` (the light halves of tab20),
`mplframe` (the legend edge, CCCCCC), `wheat`.

## Craft: what makes a classic figure look finished

Each rule names where it is shown and where it comes from: Rougier's *Scientific Visualization: Python +
Matplotlib* (chapter and example), his *Ten simple rules for better figures*, or an example of the Matplotlib
gallery. Links are in [Sources](#sources).

### The message first

- One figure, one message, stated in the caption's first sentence; everything that does not serve it goes
  (Ten simple rules 2 and 9). The raincloud exists because the box plot alone hides the bimodal route; the
  broken axis exists because the single-atom catalyst is thirteen times higher than the rest.
- Defaults are a starting point, not a design (rule 5): the classic frame stays, but grids, marker edges,
  label positions and text sizes are decided for each figure.
- Draw the numbers the text quotes where they live: half-lives on the curves (`kinetics`), T₅₀ at the 50 %
  line (`subplots`), the LOD on the concentration axis (`calibration`), the optimum on the surface
  (`surface3d`), fold changes between the bars (`bars`). A number the reader has to read off an axis is a
  number the figure does not give.

### Frame, grid and background

- The grid is a reading aid and stays below the data: `mpl grid light` (0.5pt, dashed, alpha 0.3, the grid of
  the Stock prices showcase) on continuous axes, `mpl ygrid light` for bars, none on heat maps, images, polar,
  3D and on panels that carry printed values. Source: Matplotlib gallery, Stock prices.
- Minor ticks on continuous axes (`mpl minor`), none on category axes (`x tick style={draw=none}` there).
- Regimes and regions go behind the data as spans at alpha 0.05 to 0.1, drawn before any plot, labelled
  inside at the top (`twin-axes` phases, `waterfall` bands). Source: gallery, Shade regions (span_regions).
- A reference line (target, set point, zero, 50 %) is thin, dashed or dotted, grey, labelled once at its end.
- The title names the figure; conditions, n and the model go into the grey note at the right
  (`\mpltitleright`), which keeps text boxes out of the plot. Source: gallery, Stock prices (`loc="left"`).
- Background colour only when it means something: the fill under the absorption spectrum is coloured by
  wavelength (`spectrum`); a decorative gradient is chart junk (Ten simple rules 8).

### Lines, markers, bars

- Measurements as markers, models as lines, never the other way round (`kinetics`, `calibration`, `errorbars`).
- Markers get a white edge (`mpl edge`), so a point on its fit line and points that overlap stay apart; with
  many points, lower the alpha and keep the edge. Source: Rougier, Ornaments (elegant scatter: black edge,
  white body, translucent colour on top); gallery, Scatter with histograms.
- A line crossing other lines or a dark field gets a casing: a wider white line under it (`mpl gap`), or a
  white line over a dark one (`contour` minimum energy path). Source: Rougier, Ornaments (Bessel functions,
  each curve drawn white and wide first).
- Error bars thin (`mpl yerr thin`, 1pt, caps 2.5pt) when they sit on markers, and drawn as their own plot:
  `mpl edge` would turn their caps white.
- Highlight by contrast, not by quantity: the subject in a saturated colour, the context in greys or lighter
  shades (`broken-axis` red against blue; `radar` reference grey and dashed). Source: Rougier, Bessel
  functions (J₀ in orange, the others in greys).
- Bars: white edges between neighbours (`mpl bar edge`), the control hatched in its edge colour (`mpl hatch`),
  values in white bold inside tall bars and in colour above short ones, the spine redrawn over the bars
  (`mpl spines on top`). Source: gallery, Bar label demo; Rougier, book gallery (hatched bars).
- Histograms: `mpl stepfill` at alpha 0.35 plus the outline in the full colour; all fills first, then all
  outlines, so no outline runs under the other group's fill; a fitted density scaled to counts
  (n × bin width × pdf). Source: Matplotlib's `histtype="stepfilled"` and `histtype="step"`.
- Two kinds of uncertainty, two kinds of mark: the confidence band of a fit as a translucent fill, the
  prediction band for a new sample as dashed lines (`calibration`). Source: gallery, Curve with error band;
  Fill between with transparency.
- Box plots with their data: light fill (`C0L` and friends), jittered raw points, the median redrawn after the
  points, the mean as a white diamond, n in the title note, brackets with stars and the test named in a
  corner. Source: gallery, Customized violin plot.

### Text and annotation

- Label series directly when they are few and apart: at the line end (`waterfall` temperatures, one label
  per trace in its colour), at a maximum (Rougier, Bessel functions), or along the line. Source: Rougier,
  Ornaments (legend alternatives).
- A label along a line takes the line's angle on screen, not in data:
  angle = atan(slope × (cm per y unit) / (cm per x unit)); on a log y axis the slope is in decades per x unit
  (`subplots`: −10.9°, −13.3°, −15.9° for three activation energies). Recompute it whenever the axis changes
  size.
- Text that crosses data gets a halo, a 1pt white outline (`\halo`, the `contour` package). Colour the label
  like its series, one step darker (`C0!85!black`) so thin text keeps its contrast. Source: Rougier,
  Ornaments (annotation with path effects).
- Close features whose labels collide: fan the labels out to at least the text height apart and join them to
  their features with thin leaders in the label colour (`xrd` (105)/(211), (116)/(220)); label only what the
  field labels (the nine anatase reflections, not the weak shoulders). Source: Rougier, Ornaments (side
  annotation).
- Arrows start at the text node and end 2pt short of the point (`mpl arrow`); curve one with
  `.. controls ..` to pass through a gap instead of over data (`raincloud`). Source: Matplotlib's `annotate`
  (`shrinkA`, `shrinkB`, `connectionstyle`).
- A statistics box sits in an empty corner (`mpl box light`, or `mpl box wheat` as in the gallery's Placing
  text boxes); it can be the legend too, a small tabular with colour patches (`histogram`).
- Group labels for a two-level category axis: brackets under the tick labels with the group name below
  (`broken-axis`: supports on the ticks, nanoparticles and single atoms on the brackets).
- Text size: 10pt for labels that carry the story, 8 or 9pt for notes, leaders and secondary labels, never
  below 8pt at the final size. Greek letters in math come from Computer Modern under `mathastext`; that is
  acceptable, Latin letters and digits are DejaVu.

### Legends

- A legend goes where the data are not. Check the region with the data extents; `legend upper left` and its
  siblings place it 5pt inside the frame, as Matplotlib's `loc` does.
- Short labels keep the frame small ("95 % CI", "95 % PI", "linear fit"); the caption says the rest.
- Order the entries by reading, not by drawing: `\addlegendimage{...}` handles first, every `\addplot`
  `forget plot` (the equivalent of `ax.legend(handles=[...])`, `calibration`).
- One legend for a composite, above the panels (`mpl figure legend`, `subplots`), or in the empty corner cell
  of a joint plot (`joint`). Colours then mean the same in every panel.
- No legend at all when the series are labelled directly, the axes are coloured like their series
  (`twin-axes`), or a text box carries the patches.

### Colour

- tab10 in its order (C0 blue, C1 orange, C2 green, C3 red ...), as the reader expects from Matplotlib; the
  same entity keeps the same colour in every panel and figure of the paper (`subplots`, `joint`).
- Light shades (`C0L` ... `C9L`) for fills behind points; tab10 at alpha 0.16 to 0.45 for areas; darker mixes
  (`C0!65!black`) for fitted curves over a light fill of the same hue.
- Sequential maps for magnitudes: viridis for fields and matrices (`heatmap`, `contour`, `surface3d`), plasma
  sampled from 0 to 0.82 for an ordered series of lines (`waterfall`), stopped before the pale end so the last
  line still shows on white. Text on cells: white on dark, black on light, chosen per value. Source: Rougier,
  Colors.
- Overlapping translucent fills sum towards grey; keep at most three layers (`radar`), or separate them.

### Composite figures

- Build every panel as its own `axis` with `name=`, placed with `at={(a.north east)}, anchor=north west,
  xshift=...`; the anchors are the axis rectangles, the `outer` anchors include labels. Recipes:
  - fit and residuals, heights 3 : 1, 0.22cm apart, x tick labels only on the lower panel, the ±2s band on the
    residuals (`calibration`);
  - scatter with marginals, 4 : 1, 0.22cm gaps, the marginals' zero labels dropped where two panels meet, or
    "80" and "0" read as "800" (`joint`; gallery, Scatter plot with histograms);
  - inset zoom in the emptiest region, a thin rectangle on the zoomed range and two connectors chosen so they
    miss every label, the inset's tick labels on its free side (`xrd`; gallery, Zoom region inset axes;
    Rougier, Ornaments (annotation zoom));
  - broken axis with heights in proportion to the ranges shown and one y label centred on both
    (`broken-axis`; gallery, Broken axis);
  - mosaic of a tall panel and two short ones, with one legend above all (`subplots`; Matplotlib's
    `subplot_mosaic`; Rougier, Layout);
  - a reference panel under a pattern, sharing its x (`xrd` stick patterns, mirrored up and down).
- Align what the eye compares: y labels of a column with `mpl align ylabel` (`fig.align_ylabels()`), panel
  letters on the title baseline at the outer left edge (gallery, Labelling subplots).
- Spacing budget between panels: x tick labels plus x label about 0.85cm, a title about 0.55cm, y tick labels
  plus y label 1.2 to 1.3cm. Total width at most 14cm (5.5in), which `build_figure.py` checks.
- Use the empty cells: the corner of a joint plot holds the legend, the corners of a panel hold the key
  numbers (`subplots` T₅₀ key) and the conditions.

### Fields, 3D and polar

- Filled contours with `contour filled` (pdflatex); contour lines need `contour lua` and LuaLaTeX, and time:
  81 × 73 samples build in about 45s, twice that samples in minutes. Source: gallery, Contourf demo, Contour
  label demo.
- mplot3d has to be rebuilt: the three back panes in its greys on the `axis background` layer, grid on them,
  `view={30}{30}` for elev 30 and azim −60, axis lines on the front edges, every plot but the legend entries
  `forget plot`. Source: gallery, 3D surface.
- A radar chart is a `polaraxis` with the first criterion at the top, angles within `xmin..xmax`, the
  reference drawn first and listed last (`reverse legend`). Source: gallery, Radar chart.

## Layout arithmetic

Numbers for planning a figure before the first build; all at the final size.

| Quantity | Value |
|---|---|
| DejaVu Sans digit width | 6.36pt at 10pt, 5.73pt at 9pt, 5.09pt at 8pt |
| Average character width, mixed text | about 0.55em: 5.6pt at 10pt, 5.0pt at 9pt, 4.5pt at 8pt (measured on labels and legend entries) |
| Line height | 12pt at 10pt, 11pt at 9pt, 9.6pt at 8pt |
| Rotated label (8pt) seen across | about 9pt, so rotated neighbours need 9 to 10pt of axis between them |
| Tick label to spine | 3.5pt tick plus about 4pt gap, then the label |
| Title baseline | axis top + 9pt; `\mpltitleright` uses the same baseline |
| Legend of four 9pt entries | about 50pt high; about 42pt wide plus the longest entry (frame padding, 20pt handle, cell padding) |
| 1cm | 28.45pt |

Data units per point = (axis max − axis min) / axis length in pt. A label 30pt wide on an axis of 7.4cm
(210pt) spanning 60 units covers 8.6 units. The build script's width verdict is the page; it does not say
whether a legend or label covers data.

## Checklist before delivering

- No label touches another label, a marker, a line or a spine (checked on 2 to 3 times enlarged crops of the
  crowded parts).
- The legend frame and every text box sit on empty space.
- No two tick labels meet where panels join; y labels of a column aligned; letters on one baseline.
- Series stay apart without colour: marker shape, dash pattern or a direct label.
- Every number printed in the figure matches the Python output; units in every axis label.
- The same entity has the same colour in every panel.
- Width verdict ok; a LuaLaTeX figure builds from its magic comment.
- The comment block at the top of the file says what the figure shows and where the numbers come from.

## Sources

- Nicolas P. Rougier, *Scientific Visualization: Python + Matplotlib*, 2021, open access:
  [PDF on HAL](https://hal.inria.fr/hal-03427242/document), code (BSD) in
  [rougier/scientific-visualization-book](https://github.com/rougier/scientific-visualization-book): chapters
  Defaults, Layout, Colors, Ornaments (annotation-direct, annotation-side, annotation-zoom,
  legend-alternatives, elegant-scatter, bessel-functions), Showcases.
- Nicolas P. Rougier, Michael Droettboom, Philip E. Bourne, Ten simple rules for better figures, *PLoS
  Computational Biology* 10(9): e1003833, 2014, [doi:10.1371/journal.pcbi.1003833](https://doi.org/10.1371/journal.pcbi.1003833).
- Matplotlib gallery: [Stock prices](https://matplotlib.org/stable/gallery/showcase/stock_prices.html),
  [Confidence ellipse](https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html),
  [Scatter plot with histograms](https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html),
  [Broken axis](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html),
  [Zoom region inset axes](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/zoom_inset_axes.html),
  [Placing text boxes](https://matplotlib.org/stable/gallery/text_labels_and_annotations/placing_text_boxes.html),
  [Labelling subplots](https://matplotlib.org/stable/gallery/text_labels_and_annotations/label_subplots.html),
  [Bar label demo](https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html),
  [Shade regions](https://matplotlib.org/stable/gallery/lines_bars_and_markers/span_regions.html),
  [Fill between with transparency](https://matplotlib.org/stable/gallery/lines_bars_and_markers/fill_between_alpha.html),
  [Curve with error band](https://matplotlib.org/stable/gallery/statistics/curve_error_band.html),
  [Customized violin plot](https://matplotlib.org/stable/gallery/statistics/customized_violin.html),
  [Radar chart](https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html),
  [3D surface](https://matplotlib.org/stable/gallery/mplot3d/surface3d.html),
  [Contourf demo](https://matplotlib.org/stable/gallery/images_contours_and_fields/contourf_demo.html),
  [Contour label demo](https://matplotlib.org/stable/gallery/images_contours_and_fields/contour_label_demo.html).
- Matplotlib's `matplotlibrc` defaults (rcParams) for every size, width and colour of the frame; the values in
  `classicfig.sty` are converted to points.

These sources are paraphrased and linked; no text, code or figure of them is copied into this repository.
