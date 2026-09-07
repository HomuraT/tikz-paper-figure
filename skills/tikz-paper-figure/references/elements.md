# Building blocks

All code assumes `\usepackage{cardfig}` and a `tikzpicture` after `\cardpanels{n}`, so the cards `P1..Pn` exist. Coordinates are written relative to a card corner with the `calc` syntax `($(P1.north west)+(x,-y)$)`. The snippets are taken from the three examples in `assets/examples/`.

Contents: palette, geometry and budgets, cards, stage arrows and legend, tables, chips, question badge, document page, code block, class boxes, free remarks, icons, benchmark bar panels. Data plots (pgfplots, `plotfig.sty`) are in `plots.md`.

## Palette

| name | hex | fill | meaning |
|---|---|---|---|
| `hdr` | 2D3748 | | title bar, stage arrows |
| `kept` | 2B6CB0 | `keptfill` EBF4FF | target side; what is kept, accepted, extracted or produced (`prop` chips, `cls` boxes, `code`, `tblK`) |
| `addc` | DD6B20 | `addfill` FFF1E4 | the difficulty; what the input leaves open; what a step adds; the cell that changed (`pill`, `qb`, `hi`, `hl`, `added`) |
| `dbA` | 2C7A7B | `dbAfill` E6FFFA | source A, or the only source (`colA`, `tblA`, `\dbicon{..}{dbA}`) |
| `dbB` | 6B46C1 | `dbBfill` F3EBFF | source B, or a second kind of input such as candidates (`colB`, `tblB`) |
| `ink` | 1A202C | | body text |
| grey | `black!35` line, `black!7` fill, `black!50` text | | present but not in play (`faint`, `faintcls`) |
| `barblue` | 007DFF | | bar panels only: our system's bar (`ours`); the card blue is too dark beside a grey bar |
| `bargrey` | E7E7E7 | | bar panels only: every other bar (`bar`) |

## Geometry and budgets

| length | default | note |
|---|---|---|
| `\cardw` | 4.35cm | 3.95cm when stage arrows need a wider gap; 4.8cm for two cards |
| `\cardh` | 4.45cm | raise it when a card stacks two tables (4.8cm); set it once for the tallest card |
| `\cardgap` | 0.35cm | 0.95cm with stage arrows |
| `\cardhh` | 0.6cm | title bar |
| `\cardfh` | 0.5cm | footer band; `0pt` removes it |

**Horizontal.** Width budget for a 5.5in text width: `n*\cardw + (n-1)*\cardgap <= 13.8cm`. Both three-card configurations give 13.75cm; two 4.8cm cards with a 0.95cm gap give 10.55cm and do not fill the line, which is fine.

**Vertical.** The body runs from `-\cardhh` to `-\cardh+\cardfh`. With pills, content must end above `-\cardh+\cardfh+0.55cm` (the pill centre is `\cardfh+0.34cm` above the bottom and the pill is about 0.4cm tall). Without pills, leave 0.25cm above the footer band.

**Element sizes**, to plan a card on paper before writing coordinates:

| element | size |
|---|---|
| table row | 0.28cm per row (`cell` minimum height), header included |
| table column | 0.105cm per monospace character at 6.5pt + 0.2cm; `New York City` needs 1.55cm |
| document page | 0.35cm (inner sep) + 0.25cm (label line) + 0.28cm per text line |
| `\dbicon` | 0.3 x 0.45cm at scale 1, 0.22 x 0.32cm at 0.72; the position is its bottom-left corner |
| chip, pill | about 0.42cm tall; a pill holds about 28 characters in a 4.35cm card |
| class box | 0.4cm header + 0.26cm per property row |
| question badge | 0.32cm |
| title | about 17 characters at 8.5pt bold in a 4.35cm bar next to badge and icon |
| footer | about 10 characters per cm of card width at 6.3pt |
| legend | 0.11cm per character at 7pt + 0.46cm per swatch + `\legsep` (0.4cm); must fit the width of the card row |

Beside a document page of text width 1.55cm in a 4.35cm card, about 1.5cm remain for chips; a table wider than that goes under the page instead of beside it. Long cell values (a city name, a file path) decide between a horizontal and a vertical card layout; check them first.

## Cards, title bar, footer, pill

```latex
\cardpanels{3}                       % P1 P2 P3, gradient title bars, footer bands, borders
\cardheadn{P1}{1}{Issue}             % badge with the number of the point in the text + title
\cardhead{P2}{Entities}              % title without badge (stages of a process)
\cardicon{P1}{bug}                   % faint white icon, right end of the title bar
\cardfoot{P1}{earlier work: the file to edit is given}
\cardpill{P1}{the issue names no file}   % orange, at \cardfh+0.34cm above the bottom in every card
```

Why a footer band: the card body shows the situation of this paper, the footer names the baseline it differs from, so the contrast is inside the card and needs no arrow. Why a pill instead of a loose orange sentence: three loose sentences land at three heights; pills with a fixed offset line up without thought.

When one card ends up with more air than the others, balance the gaps above and below its elements and leave it; do not enlarge an element to fill space. Lower `\cardh` only if every card has air.

## Stage arrows and legend (process figures)

```latex
\setlength{\cardgap}{0.95cm}          % before \cardpanels
\cardstage{P1}{P2}{extract}           % arrow across the gap at the middle of the body area, small-caps label above
\cardlegend{P2}{%                     % one node centred under the middle card (odd card counts)
  \legswatch{draw=kept, fill=keptfill} extracted entity\legsep
  \legswatch{faint, fill=black!7} not used\legsep
  \legswatch{added, fill=addfill} added by the merge\legsep
  \legline{pop} derived from\legsep
  {\color{kept}\faIcon{key}}\, key}
\cardlegendspan{P1}{P2}{...}          % centred between the outer edges of two cards (even card counts)
\renewcommand{\legsep}{\hspace{0.3cm}}   % before \begin{document}, when the legend runs wide
```

The legend is one node so its width is measured once and it centres itself. Size it with the budget above before building; the width verdict of the build script does not see a legend that overhangs the cards. With a legend in the figure, the caption does not explain the colours again.

## Tables

```latex
\dbicon[0.72]{$(P1.north west)+(0.25cm,-1.2cm)$}{dbA}                                 % cylinder, bottom-left corner at the position
\node[tname, text=dbA, anchor=south west] at ($(P1.north west)+(0.53cm,-1.16cm)$) {emp};
\matrix[tblA, anchor=north west,
  column 1/.style={nodes={text width=0.3cm}}, column 2/.style={nodes={text width=0.55cm}}, column 3/.style={nodes={text width=0.45cm}}]
  at ($(P1.north west)+(0.25cm,-1.24cm)$) (aemp) {
  id & name & unit \\
  7 & Ada & 2 \\
  9 & Bob & 2 \\
};
\boxshadow[]{aemp}                   % square-cornered shadow; drop shadow does not work on a matrix
\draw[fk] (aemp-1-3.east) -- (aunit-1-1.west);                                        % foreign key to another table
\matrix[tbl, anchor=north west, nodes={cell, faint, fill=black!3}, ...] at (...) (alog) {...};   % a table not in play
\matrix[tblK, anchor=north, column 1/.style={nodes={text width=0.7cm}}] at (...) (r) { name \\ Ada \\ Bob \\ };   % result table, blue header
\node[tnote] at ($(aemp.south west)+(0,-0.12cm)$) {$\dagger$ in miles, \tikzmarknode[hl]{u1}{1 mi = 1.609 km}};   % table footnote
```

- `tblA` / `tblB` tint the header row with the source colour, `tblK` with the target blue; plain `tbl` has no tint; `nodes={cell, faint, fill=black!3}` greys a whole table.
- Every column gets a `text width`, otherwise rows of different content come out uneven.
- `|[hi]|` before a cell gives it the orange border and fill: the cell the story is about (`test\_empty & fail & |[hi]| pass \\`).
- Cells are named `<matrix>-<row>-<col>`; connect to `aemp-1-3.east`, `tt-2-3.south`, etc. `(tt.south -| tt-2-3)` is the table bottom under a column.
- A daggered header cell: `length$^{\textcolor{addc}{\dagger}}$` when the footnote is in play, plain `$^{\dagger}$` otherwise; the footnote goes in a `tnote` node under the table.
- String values as the source would show them. `\textquotesingle` gives a straight quote in the monospace font; `\textvisiblespace` shows a trailing blank; escape `_`, `&`, `#`.

## Chips

```latex
\node[grp, anchor=west] at ($(P2.north west)+(0.3cm,-0.92cm)$) {\faIcon{layer-group}\ candidates};   % group label
\node[grp, anchor=east] at ($(P2.north east)+(-0.3cm,-0.92cm)$) {{\color{kept}\faIcon{check}}\ accepted};
\node[colA, anchor=east] at ($(P1.north east)+(-0.3cm,-1.5cm)$) (f1) {parse.py};        % teal chip: source A
\node[colB, anchor=west] at ($(P2.north west)+(0.3cm,-1.4cm)$) (c1) {patch A};          % violet chip: source B / candidates
\node[prop, anchor=east] at ($(P2.north east)+(-0.3cm,-1.95cm)$) (a1) {patch};          % blue chip: target side, result
\dbchip{$(P2.north west)+(0.3cm,-1.4cm)$}{colA}{c1}{dbA}{first}                          % chip with a small cylinder inside its left end
```

Group labels (`grp`) are small caps at 6pt and sit on one line across the card; they tell the reader which side is which without a box around each side. Chips read as tags; use them for things that have a name and no internal structure (columns, files, candidates, a result value).

## Question badge and orange connectors

```latex
\node[qb] at ($(P2.north)+(0,-1.95cm)$) (q2) {?};    % orange disc, the open decision
\node[qb] at (...) (q3) {$\Sigma$};                   % other glyphs: $\Sigma$ for a sum, $\times$ for a conversion, + for a union
\draw[wire] (c1.east) -- (q2);                        % plain orange line into the badge
\draw[wire] (c2.east) -- (q2);
\draw[arr] (q2) -- (a1.west);                         % orange arrow out of it
\draw[fed] (ta-2-1.west) -- (ta-2-1.west -| jx) -- (tb-2-1.west -| jx) -- (tb-2-1.west);   % dashed link with rounded corners
```

The badge sits at the point where the system has to decide or compute something the inputs do not state. Put it on the connector, not beside it. Inputs come in with `wire`, the result goes out with `arr`. Math glyphs in the badge come out in Computer Modern bold and match the sans well enough at this size.

## Document page with highlighted phrases

```latex
\begin{tikzpicture}[remember picture]                 % required for \tikzmarknode
\docpage[text width=1.55cm]{d}{$(P1.north west)+(0.28cm,-0.95cm)$}{ISSUE}{%
  Empty input makes \tikzmarknode[hl]{m1}{parse()} raise KeyError. Seen since \tikzmarknode[hl]{m2}{v2.3}.}
\docpage[text width=3.85cm][comment-dots]{q}{...}{QUESTION}{Which \tikzmarknode[hl]{m1}{employees} work in \tikzmarknode[hl]{m2}{R\&D}?}
\coordinate (qx) at ($(P1.north west)+(2.55cm,0)$);
\node[qb, overlay] at (qx |- m1.center) (q1) {?};     % x fixed, y from the mark
\draw[wire, overlay] (d.east |- m1.center) -- (q1);   % leave the page edge at the height of the phrase
\draw[arr, overlay] (d.south -| m1.center) -- (t.north);   % leave the page bottom under the phrase
```

- `\docpage` draws the page, its folded corner, the cut-corner shadow and the small label (icon + LABEL). The second optional argument is the icon (`file-alt` default, `comment-dots` for a question, `book` for a manual). The first line of the body is a blank line under the label.
- `hl` boxes a phrase in orange. The connector leaves the page at the height of that phrase, which is what ties the text to the element on the right.
- Three ways to use a mark: `(bx |- m1.center)` takes the y, `(m1.center |- qy)` takes the x, `(d.south -| m1.center)` puts a node edge under it. All work outside `$...$` and need `overlay` on the node or path; see pitfalls.
- Hyphenation is off inside `doc`; if a word does not fit, shorten the text or widen `text width`, never let it break.

## Code block

```latex
\node[grp, anchor=south west] at ($(P2.north west)+(0.3cm,-0.97cm)$) {{\color{kept}\faIcon{code}}\ sql};
\node[code, anchor=north west, text width=3.85cm] at ($(P2.north west)+(0.3cm,-1.02cm)$) (s) {%
  \textbf{SELECT} \tikzmarknode[hl]{s1}{e.name}\\
  \textbf{FROM} emp e\\
  \textbf{JOIN} unit u \textbf{ON} e.unit = u.id\\
  \textbf{WHERE} u.name = \tikzmarknode[hl]{s2}{\textquotesingle R\&D\textquotesingle}};
\draw[obj] (s.south -| r.north) -- node[caplab, right] {execute} (r.north);   % blue arrow with a small-caps label
```

- `code` is a blue-bordered box in the monospace font with `align=left`; lines end with `\\`, keywords in `\textbf`. Leading spaces after `\\` are dropped, so indent with `~~` or reflow the line.
- `hl` inside the box inherits the monospace font, so the same style marks a span in the question and the token it becomes in the code.
- `caplab` is a small-caps arrow label in a colour: `node[caplab, right]` (blue) or `node[caplab=addc, above]`.

## Class boxes and edges

```latex
\classbox[cls, anchor=north west]{bemp}{$(P2.north west)+(0.25cm,-0.95cm)$}{Employee}{\keyic name\\ \nokey unit}
\classbox[cls, anchor=north east]{bun}{$(P2.north east)+(-0.25cm,-0.95cm)$}{Unit}{\keyic name}
\classbox[faintcls, anchor=north west][black!35]{alog}{...}{Log}{ts\\ message}       % grey box: give the divider colour too
\classtag[addedcls1, anchor=north]{cper}{$(P3.north west)+(1.1cm,-1.35cm)$}{Person}   % name only, orange dashed: added by a step
\classtag[faintcls1, anchor=north]{aarc}{...}{Archive}                                % name only, grey
% edges
\draw[obj] (bemp.east |- bun.text east) -- node[lab, above] {inUnit} (bun.west |- bun.text east);   % relation, filled arrow
\draw[sub, added] (cemp.north -| cper.south) -- (cper.south);                          % subclass, open triangle, orange dashed
\coordinate (pm) at ($(cper.south)+(0,-0.3cm)$);                                       % two children joining a bus to one parent:
\draw[added, line width=0.6pt] (cemp.north) |- (pm) -| (cun.north);  \draw[sub, added] (pm) -- (cper.south);
\draw[pop] (ben.north) to[bend left=12] (bemp.south);                                  % dotted: table name -> the class it yields
```

`\classbox` takes the style (with anchor) as the first optional argument and the divider colour as the second; grey boxes need `[black!35]` so the divider matches the border. `\keyic` puts the key icon before the key property, `\nokey` keeps the other rows aligned. A property greyed inside a blue box (`{\color{black!45}length}`) means the class is in play but that field is empty. `bun.text east` is the right end of the name part of a two-part box; use it to aim an edge at the header of the box.

## Free remarks

```latex
\node[note, anchor=west] at ($(fq.east)+(0.2cm,0)$) {same key? no link declared};   % orange text, no box
```

Use `note` only when a pill does not fit (inside a tight gap). In a row of cards the pills are preferred because they line up.

## Icons

Title bars and group labels use `\faIcon{name}` from fontawesome5. Names that have worked: `database`, `sitemap`, `cubes`, `project-diagram`, `network-wired`, `calculator`, `book-open`, `book`, `bug`, `code`, `code-branch`, `vial`, `check`, `layer-group`, `eye-slash`, `key`, `file-alt`, `comment-dots`, `sign-in-alt`, `sign-out-alt`, `link`, `ruler-horizontal`, `table`, `search`, `random`, `magic`, `sun`, `star`, `globe`, `robot`, `brain`, `bolt`, `cloud`, `leaf`. Some of these have no `\faXxx` macro, so always use the `\faIcon{...}` form. To check a name: `grep -c "{name}" "$(kpsewhich fontawesome5-mapping.def)"`.

## Benchmark bar panels

```latex
\setlength{\barpanelw}{6.6cm}  \setlength{\barcolgap}{0.6cm}   % two columns: 2*6.6 + 0.6 = 13.8cm
\setlength{\barnamew}{1.6cm}                                   % longest system name, 0.115cm per character at 7pt
\setlength{\barpanelpitch}{2.75cm}                             % \bartitlegap (0.45) + rows*\barrowpitch (0.3) + 0.5cm
\renewcommand{\barmax}{100}                                    % the value that fills the track, same in every panel
\begin{barpanel}{0}{0}{Code Repair}                            % {col}{row}, zero-based, then the title
  \barrow{Sol 3}{\iconfa[addc]{sun}}{73.0}                     % rows best first
  \barrow[ours]{Ours}{\iconletter{O}}{67.5}                    % blue bar
  \barrow[ours2]{Ours (no retrieval)}{}{61.0}                  % orange bar, no icon
  \barrow{Vega}{\iconletter[black!60]{V}}{46.2}[46.2$^\dagger$] % printed label differs from the number
\end{barpanel}
\begin{barpanel}[10]{1}{0}{Latency (s)} ... \end{barpanel}     % this panel fills the track at 10
```

| length | default | note |
|---|---|---|
| `\barpanelw` | 6.6cm | 4.2cm for three columns; the value labels of the longest bars end at this width |
| `\barcolgap` | 0.6cm | between panel columns |
| `\barpanelpitch` | 2.75cm | between panel rows; recompute when the row count changes |
| `\barnamew` | 1.6cm | name column; names longer than this run into the icon |
| `\bariconw` | 0.4cm | icon column; `0pt` when no system has one |
| `\barvaluew` | 0.7cm | reserved after a full-length bar for the value label; 0.85cm for four-digit values |
| `\barrowpitch`, `\barh` | 0.3cm, 0.17cm | row pitch and bar thickness |
| `\bartitlegap` | 0.45cm | top of the title to the centre of the first bar |

- The panel is a `scope` shifted to the grid cell; everything inside is positioned from the title's top-left corner, so panels never depend on each other's content.
- One scale for the whole figure is what makes the grid readable at a glance: a bar half as long is a score half as high, in any panel. Override `\barmax` per panel only for a metric on another scale, and say so in the title (`Latency (s)`).
- Colours: `barblue` (007DFF) for ours, `bargrey` (E7E7E7) for the rest, black text. These were sampled from the release charts the template imitates and are deliberately not the card palette; the card blue looks muddy next to a grey bar. `ours2` keeps the orange `addc`.
- Icons: `\iconletter[colour]{K}` is a rounded filled square with one white letter, the stand-in for a logo; `\iconfa[colour]{name}` a fontawesome5 glyph; `\iconimg{file}` a real logo at 0.24cm height (a PDF or PNG next to the figure source). Colours that sit well with the bars: `black`, `barblue`, `addc`, `dbA`, `dbB`, `black!60`.
- `scripts/bars_from_csv.py` writes a complete figure file from a wide CSV (`system,icon,Bench A,Bench B,...`), sorted per panel, with the lengths above computed from the data; `--body-only` gives just the `barpanel` blocks for pasting into an existing file.
