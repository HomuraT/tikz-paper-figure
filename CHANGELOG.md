# Changelog

## 0.2.0 (unreleased)

A second style next to the house style.

- `classicfig.sty`: the classic style, Matplotlib's default rcParams in pgfplots (DejaVu Sans with math in the same font, the four-sided frame, tab10, the rounded legend frame), plus one key or macro per finishing touch: light grid, minor ticks, white marker edges, halos, spans and reference lines, text boxes, significance brackets, hatched and white-edged bars, stepfilled histograms, aligned y labels, broken axes, a legend for a whole composite, spines over the data.
- 18 classic examples with renders: 13 plots (kinetics, spectrum, error bars with a derived axis, twin axes, waterfall, histogram, box plot, raincloud, bars, heat map, radar, contour, 3D surface) and 5 composite figures (fit with residuals, scatter with marginals and ellipses, XRD with an inset zoom and reference patterns, broken axis, mosaic with one legend); `data/make_data.py` computes every number they show (numpy only, seeded).
- References: `classic.md` (when to use the style, the workflow for new data, the example for each question, every key, the craft collected from Rougier's *Scientific Visualization: Python + Matplotlib*, his ten simple rules and the Matplotlib gallery, layout arithmetic, checklist); a classic section in `pitfalls.md`; `gallery.md` grouped by style.
- `SKILL.md`: choosing the style (one paper, one style) and the classic workflow.
- Scripts: `build_figure.py` switches to LuaLaTeX when a figure starts with `% !TEX program = lualatex`; `gallery_sheet.py` writes one contact sheet per style (`--style`); `check_env.py` also checks dejavu, mathastext, contour and numpy.

## 0.1.0 (2026-09-07)

First public version.

- Two style files sharing fonts and palette: `cardfig.sty` (card figures, benchmark bar panels) and `plotfig.sty` (pgfplots data plots).
- Three templates and 36 built examples with renders: 3 card figures, 1 bar-panel grid, 28 data plots, 4 composite figures.
- Scripts: build with width check and PNG render, bar panels from CSV, parallel-sets flows from CSV, treemap from CSV, palette check under simulated colour-vision deficiency, before/after sheet, gallery sheet, environment check.
- References: digest of Wilke's *Fundamentals of Data Visualization* with decision tables, element catalogue, one recipe per chart, pitfalls, gallery.
- Skill workflow: environment check before the first figure, a revision contract (change list and keep list, edit only the lines that carry the change), delivery rules (state which checks ran; never describe a render that was not produced). Each template carries its revision contract as a comment.
- Repository: two reproducible examples with commands and outputs, three test tasks with acceptance criteria, MIT for code and text, CC0 for the assets.
