# Changelog

## 0.1.0 (2026-09-07)

First public version.

- Two style files sharing fonts and palette: `cardfig.sty` (card figures, benchmark bar panels) and `plotfig.sty` (pgfplots data plots).
- Three templates and 36 built examples with renders: 3 card figures, 1 bar-panel grid, 28 data plots, 4 composite figures.
- Scripts: build with width check and PNG render, bar panels from CSV, parallel-sets flows from CSV, treemap from CSV, palette check under simulated colour-vision deficiency, before/after sheet, gallery sheet, environment check.
- References: digest of Wilke's *Fundamentals of Data Visualization* with decision tables, element catalogue, one recipe per chart, pitfalls, gallery.
- Skill workflow: environment check before the first figure, a revision contract (change list and keep list, edit only the lines that carry the change), delivery rules (state which checks ran; never describe a render that was not produced). Each template carries its revision contract as a comment.
- Repository: two reproducible examples with commands and outputs, three test tasks with acceptance criteria, MIT for code and text, CC0 for the assets.
