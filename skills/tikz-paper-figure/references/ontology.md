# Ontology and RDF diagrams

Keep three decisions separate: notation gives symbols their meaning, visual style gives them their
appearance, and layout arranges them for the figure's message. `assets/examples/ontology/` contains three
notation examples and six soft-style examples, including graphs with 26–28 content nodes. Use the published
notation when it is requested or required by the paper; use the soft style for explanatory ontology,
mapping, provenance and resource diagrams whose visual vocabulary can be defined in a key.

Contents: [Which example](#which-example-to-open) · [Soft style](#soft-ontology-style) · [Notations](#the-notations) · [Layout](#layout-rules) ·
[Styles](#styles) · [Checklist](#checklist) · [Sources](#sources)

## Which example to open

| The figure shows | Example | Package | Style family |
|---|---|---|---|
| RDF data: the triples about one resource, literals and datatypes, a blank node | `rdf-triples.tex` | `classicfig.sty` | classic |
| An ontology's schema (TBox): classes, object and datatype properties, subclasses, external classes | `vowl-schema.tex` | `classicfig.sty` | classic |
| A schema and its individuals together (TBox over ABox), which fact instantiates which axiom | `tbox-abox.tex` | `cardfig.sty` | house |
| Soft class boxes, instance capsules and white values, in a small example | `soft-schema.tex` | `softontology.sty` | classic fonts |
| Sources, operations and a shared output | `soft-lineage.tex` | `softontology.sty` | classic fonts |
| A resource graph beside a text excerpt and a selected value | `soft-graph-text.tex` | `softontology.sty` | classic fonts |
| A larger schema/instance example, 28 nodes | `soft-dense-schema.tex` | `softontology.sty` | classic fonts |
| Four source branches converging into shared outputs, 26 nodes | `soft-dense-lineage.tex` | `softontology.sty` | classic fonts |
| A connected catalogue with shared affiliation and literal branches, 27 nodes | `soft-dense-catalogue.tex` | `softontology.sty` | classic fonts |

The package follows the paper, as for every other figure (one paper, one style; `SKILL.md`, Choosing a
style). `tbox-abox` belongs to the house style: Source Sans and Inconsolata, cardfig's class boxes and chips,
so it sits beside card figures in an ML paper; its fills are tab20's light shades, so it does not clash with
the classic figures of a paper either, but its fonts do. `rdf-triples` and `vowl-schema` are plain TikZ on
`classicfig.sty` (DejaVu Sans and DejaVu Sans Mono).

A general knowledge-graph neighbourhood need not imitate a particular graph renderer. Choose a keyed
visual vocabulary and a layout that makes its relationships legible; the soft style is one option.

## Soft ontology style

The target is the `soft-*.png` family, including the dense examples. This is a reusable appearance, not a
fourth ontology notation. It does not prescribe a domain, graph topology, node count or panel arrangement.

### Visual vocabulary

| Element | Shared treatment |
|---|---|
| Class or element type | Small-radius rectangle, bold monospace, soft fill, thin black outline, tiny hard shadow |
| Instance or resource | Capsule, regular monospace, lighter family fill, the same outline and shadow treatment |
| Literal or field value | White small-radius rectangle, **the same black outline, monospace size and tiny shadow** as other nodes |
| Text excerpt | White box using the value treatment, with more padding and line spacing for multiple lines |
| Reference | Thin black arrow with a small head; name next to its edge |
| Attribute | Grey arrow to a value; grey distinguishes the edge, not a separate low-contrast box style |
| Type relation | Dotted grey arrow, instance to class, labelled or explained in the key |
| Region | Very light grey fill, soft corners, little or no border |
| Key | Symbols drawn with the actual node/edge styles, aligned to their text, inside a light frame |

Use a few pale families: `sogblue` (`AEC7E8`), `sogorange` (`FFBB78`) and `soggreen` (`98DF8A`). A class can
use the base shade and its instances a 45% tint. Colours may group domains, roles or namespaces; define
their meaning per figure and keep it consistent across a paper. Green is not inherently ontology, orange
is not inherently mapping, and colour alone need not distinguish class from instance.

Node outlines are 0.55 pt; reference arrows 0.6 pt. The hard shadow is offset about 0.7–0.8 pt right/down.
Values and class boxes use 2 pt corners, instances 7 pt, regions 4 pt with `black!3.5` fill. Tiny key symbols
need smaller corner radii (2 pt for boxes, about 4 pt for capsules); a large radius on a tiny box can fold
its outline. Keep white values visually finished: do not revert them to thin grey, shadowless boxes.

Identifiers, predicates and code use monospace; titles and explanations use the paper's sans-serif font.
Nodes use 8 pt type at natural size, edge labels about 7.4 pt. The samples use DejaVu Sans / DejaVu Sans Mono.
`softontology.sty` does not select fonts, so a house-style paper can retain Source Sans Pro / Inconsolata.
Code excerpts use their own line spacing. Keep red outlines, changed text, strike-throughs or status marks
optional and explained; they are emphasis devices, not required decoration.

### Reuse without importing the example's structure

Copy `assets/softontology.sty` beside the new source and start from the closest `soft-*.tex` example. The
package supplies only appearance. Its styles are prefixed `sog ` to avoid clashes with other packages:

```tex
\node[sog kind=sogblue] (person) at (0,0) {Person};
\node[sog entity=sogblue] (alice) at (0,-1.5) {:alice};
\node[sog value] (name) at (3,-1.5) {"Alice Chen"};
\draw[sog type] (alice) -- node[sog lab,right] {rdf:type} (person);
\draw[sog attr] (alice) -- node[sog lab,above] {name} (name);
```

Other components: `sog code`, `sog region`, `sog title`, `sog subtitle`, `sog heading`, `sog note`,
`sog ref`, `sog key`, `sog keytext`, `sog swatch` and `sog edit`. Use a background layer for region/key
frames so their fill does not cover content. Retain standard symbols when a selected notation requires
them; these capsules and colours are not replacements for VOWL's notation.

Choose grouping from the story: a single graph, branches, rows, columns or graph plus text can all share
this appearance. Do not require TBox over ABox, one lane per type, three levels, a before/after comparison,
compilation panels, provenance badges, a fixed example vocabulary or fixed colour-to-layer assignments.
The sample titles, row repetition and node counts are demonstration content, not template requirements.

For a dense graph, inspect a dense sample first. Reserve channels for shared dependencies and space beside
vertical edges; stagger incoming anchors. Put a label on a specific segment of a bent path, not an arbitrary
fraction of the whole path that may land on a bend. Increase spacing or reorganize the graph before reducing
type size. Check long literals, branch labels, selection frames and key symbols in the rendered image.

The six samples are about 16.8–17.2 cm wide, intended for a full-width figure. Build them with:

```text
python scripts/build_figure.py assets/examples/ontology/soft-dense-lineage.tex --max-width 500 --png-dir assets/examples/ontology
```

For a new paper use its actual width budget, not 500 pt by default. Re-layout for a narrower slot instead of
scaling the entire sample down and shrinking its text. The node counts in the dense samples include literals
and exclude titles, labels, keys and code excerpts.

## The notations

**RDF graph, W3C convention** (`rdf-triples`). IRIs are ovals, literals rectangles, predicates labelled arrows
from subject to object; the RDF 1.1 XML Syntax states it in the text of its Figure 1 ("nodes are represented
as ovals ... string literal nodes have been written in rectangles"), and the RDF Primer's diagrams draw it so.
Blank nodes are small empty circles with their label (`_:b1`) beside them, not inside. Typed literals keep the
datatype in the label (`"1903"^^xsd:gYear`), language-tagged ones the tag (`"Marie Curie"@en`). Every prefix
used goes into the prefixes box. Tutorials that swap the shapes exist; do not follow them.

**VOWL 2** (`vowl-schema`). The Visual Notation for OWL Ontologies, the notation of WebVOWL and ProtégéVOWL.
Classes are circles whose size may encode the number of instances; external classes (from another vocabulary)
dark blue with white text; object properties are labels on the edge in the class colour, datatype properties
green labels whose edge ends in a yellow datatype rectangle; rdfs:subClassOf is a dashed edge labelled
"Subclass of"; a property with the same class as domain and range is a loop. The colours are VOWL's own and
are part of the notation: `#acf` class and object property, `#36c` external, `#9c6` datatype property,
`#fc3` datatype and literal, black outlines (WebVOWL's `vowl.css`). Do not recolour them to tab10.

**TBox over ABox** (`tbox-abox`). The OWL notations that draw classes as boxes (Graffoo, Chowlk, OWLGrEd)
agree on the parts this figure uses: a class is a box with its name only; an object property an arrow between
two classes; a datatype property an arrow from its class to a datatype (Graffoo) rather than a line inside the
class box, so that it can be labelled and routed like any other property; rdfs:subClassOf an open triangle;
individuals a shape and colour of their own (here orange chips), tied to their class by rdf:type. Chowlk's specification adds that colours carry no meaning of the model and may mark namespaces; here
the fill marks the kind of node (class blue, individual orange, datatype or literal green) and every outline is
black. Properties listed inside a class box (UML style) were tried and dropped: the attributes cannot then be
connected to anything.

## Layout rules

1. **Choose placement by structure, not a fixed node-count threshold.** Hand or grid-based placement works
   for a few dozen nodes when they have clear roles and reserved label space, as the dense soft examples do.
   For less regular graphs, compute positions in Python (`networkx.spring_layout` with a fixed seed, or
   Graphviz `dot` for a hierarchy), then refine routing and labels. The graphdrawing library needs LuaLaTeX
   and can move nodes whenever the graph changes.
2. **Rows by role, columns by class.** In `tbox-abox` the TBox has a row of superclasses and datatypes over
   a row of classes, and every individual sits in the column of its class, so every rdf:type link is
   vertical. Stack classes that play the same role in the same row.
3. **Route an assertion as the axiom it instantiates.** received points left in both layers, discovered right;
   bornIn, which would cross a node in both, goes around its row, above in the TBox and below in the ABox.
   The reader then matches the two layers edge by edge.
4. **Leave straight lines straight, route around with right angles.** An edge that would cross a node goes
   around it with `|-` and `-|` through a free lane; it never crosses a label. Where two edges enter one node
   from the same side, shift one of them (`[xshift=-10pt]cty.north`).
5. **Edge labels on the edge, on a white patch, or beside a vertical one.** RDF predicates sit on a white
   patch in the middle of their arrow; a short horizontal arrow takes its label above (`above=1pt,
   fill=none`), or the patch hides the arrowhead. VOWL property labels are the coloured boxes themselves.
   Labels of vertical edges go to the right. In `tbox-abox` labels sit above horizontal edges.
6. **Keys: align each symbol to its text.** Use a horizontal key when it fits, or stack entries. Draw each symbol as its own node at the
   same y as its text, in a `\graphkey` frame. An inline `\tikz` inside a legend node inherits that node's
   `anchor` and drifts below the text (see `pitfalls.md`); cardfig's `\legswatch` sets `anchor=center` for
   this reason.
7. **Size: use the paper's actual figure slot.** The three original notation examples fit the 13.8 cm budget of a 5.5 in text
   width; long IRIs (`ex:NobelPrizePhysics`) decide the width, so shorten the local names before shrinking
   the font below 8 pt.

## Styles

`classicfig.sty`, RDF: `rdf iri`, `rdf focus` (the resource the figure is about, a thicker oval),
`rdf literal`, `rdf blank`, `rdf edge`, `rdf pred` (the predicate label), `rdf prefixes` (wheat box).
VOWL: `vowl class=<size>` (default 1.5 cm), `vowl external=<size>`, `vowl datatype`, `vowl objprop` and
`vowl dataprop` (labels in the middle of their edge), `vowl prop box` (the same box anywhere, for a key),
`vowl edge`, `vowl subclass`, `vowl subclass label`; colours `vowlclass`, `vowlexternal`, `vowldatatype`,
`vowldataprop`. Both: `graph key` and `\graphkey{x,y}{width}{height}` for the key frame.

`cardfig.sty`: `onto class` (for `\classtag`), `onto individual`, `onto datatype`, `onto obj`, `onto data`,
`onto sub`, `onto type`, `onto lab`, `onto dlab`, `onto rule`; colours `ontoclass`, `ontoind`, `ontodata`;
layer names with the existing `grp` style. These styles carry no kept/added meaning; for a figure that
contrasts what is extracted with what is added, use the card styles (`cls`, `faintcls`, `addedcls`) of
`pipeline-stages` instead.

## Checklist

- A requested published notation retains its prescribed symbols; a custom explanatory diagram defines its vocabulary in the key.
- For the soft style, white values share the nodes' black outline, type size, small corners and shadow; their key symbols agree.
- Every prefix used appears in the prefixes box (RDF), or no prefixes at all.
- No edge crosses a node or a label; no two labels touch (read enlarged crops of the crowded parts).
- Every key symbol sits on the centre line of its text.
- rdf:type links vertical (`tbox-abox`), each assertion routed as its axiom.
- The figure compiles with `build_figure.py`, width verdict ok, and the render was read.

## Sources

- W3C, *RDF 1.1 XML Syntax*, Section 2 and Figure 1 (<https://www.w3.org/TR/rdf-syntax-grammar/>); *RDF 1.1
  Primer* (<https://www.w3.org/TR/rdf11-primer/>).
- Negru, Lohmann, Haag, *VOWL: Visual Notation for OWL Ontologies*, specification v2
  (<http://purl.org/vowl/spec/>); Lohmann et al., *Visualizing ontologies with VOWL*, Semantic Web 7(4), 2016;
  WebVOWL's stylesheet `src/webvowl/css/vowl.css` (<https://github.com/VisualDataWeb/WebVOWL>) for the colours.
- Falco, Gangemi, Peroni, Shotton, Vitali, *Modelling OWL Ontologies with Graffoo*, ESWC 2014 Satellite Events
  (<https://essepuntato.it/graffoo/>).
- Chávez-Feria, García-Castro, Poveda-Villalón, *Chowlk: from UML-Based Ontology Conceptualizations to OWL*,
  ESWC 2022 (<https://chowlk.linkeddata.es/notation.html>).
- Bārzdiņš et al., *OWLGrEd: a UML Style Graphical Notation and Editor for OWL 2*, OWLED 2010.
- Dudáš, Lohmann, Svátek, Pavlov, *Ontology visualization methods and tools: a survey of the state of the
  art*, The Knowledge Engineering Review 33, 2018.
