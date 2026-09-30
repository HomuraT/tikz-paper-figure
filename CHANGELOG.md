# Changelog

## 0.2.2 (2026-09-30)

Soft ontology diagrams with a reusable visual style.

- Add `softontology.sty`: font-neutral, namespaced TikZ styles for class boxes, instance capsules, white values and text excerpts, references, attributes, type links, regions and legends. White value boxes share the nodes' black outlines, small corners, monospace type and subtle hard shadows.
- Add six compiled examples with editable TeX, PDF and PNG: `soft-schema`, `soft-lineage`, `soft-graph-text`, `soft-dense-schema` (28 nodes), `soft-dense-lineage` (26 nodes), and `soft-dense-catalogue` (27 nodes). The repository now contains 63 examples, including nine ontology/RDF diagrams.
- Expand the ontology guide and skill workflow to separate notation, appearance and layout. Colours and grouping remain content-dependent; no fixed domain, topology, lane structure or panel arrangement is required. Retain the original RDF, VOWL and TBox/ABox examples.
- Update the ontology contact sheet, English/Chinese READMEs, gallery, example index, banner count (63 examples) and full-width build instructions. Correct the skill description's YAML format and include the new ontology use cases.
- Ignore the local `draft/` review copies; the six approved examples are shipped under the skill's assets.
- Validation: all six new examples compile at their intended width, packaged renders match the approved drafts pixel-for-pixel, and local documentation links resolve.

## 0.2.1 (2026-09-29)

Ontology and RDF diagrams.

- Three examples in `assets/examples/ontology/`, each in a published notation: `rdf-triples` (the W3C convention for RDF graphs: IRIs in ovals, literals in rectangles, a blank node, a prefixes box) and `vowl-schema` (VOWL 2 as WebVOWL draws it, in VOWL's own colours) in the classic style, `tbox-abox` (name-only class boxes, datatype properties as arrows to datatypes, individuals under their classes with rdf:type links) in the house style.
- `classicfig.sty`: styles `rdf iri`, `rdf focus`, `rdf literal`, `rdf blank`, `rdf edge`, `rdf pred`, `rdf prefixes`, the `vowl ...` styles with VOWL's colours, `graph key` and `\graphkey`; loads DejaVu Sans Mono and `shapes.geometric`. `cardfig.sty`: the `onto ...` styles (black outlines on tab20's light shades). No existing style changed; every other example renders pixel for pixel as before.
- Fix: `\legswatch` sets `anchor=center`; under `\cardlegend` the swatch had inherited `anchor=north` and sat half its height below the text (`io-two-cards` and `pipeline-stages` re-rendered).
- References: `ontology.md` (which notation for which figure, the notations and their sources, layout rules, styles, checklist); an ontology section in `pitfalls.md` and `gallery.md`; `SKILL.md` section. `gallery_sheet.py` writes a third contact sheet, `assets/examples/ontology/gallery.png` (`--style ontology`). The READMEs show the contact sheets directly instead of folding them.

## 0.2.0 (2026-09-29)

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
