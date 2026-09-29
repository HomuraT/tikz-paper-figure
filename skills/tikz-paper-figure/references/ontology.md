# Ontology and RDF diagrams

Three examples in `assets/examples/ontology/` draw the three things a knowledge-graph or ontology paper most
often has to show: the triples about one resource, the schema of an ontology, and a schema together with the
individuals that instantiate it. Each follows a published notation instead of inventing one, because readers
from the Semantic Web community know these notations and read a departure from them as an error. This file
says which example to open, what each notation prescribes and where it comes from, the layout rules collected
while building the examples, the styles, and a checklist.

Contents: [Which example](#which-example-to-open) · [Notations](#the-notations) · [Layout](#layout-rules) ·
[Styles](#styles) · [Checklist](#checklist) · [Sources](#sources)

## Which example to open

| The figure shows | Example | Package | Style family |
|---|---|---|---|
| RDF data: the triples about one resource, literals and datatypes, a blank node | `rdf-triples.tex` | `classicfig.sty` | classic |
| An ontology's schema (TBox): classes, object and datatype properties, subclasses, external classes | `vowl-schema.tex` | `classicfig.sty` | classic |
| A schema and its individuals together (TBox over ABox), which fact instantiates which axiom | `tbox-abox.tex` | `cardfig.sty` | house |

The package follows the paper, as for every other figure (one paper, one style; `SKILL.md`, Choosing a
style). `tbox-abox` belongs to the house style: Source Sans and Inconsolata, cardfig's class boxes and chips,
so it sits beside card figures in an ML paper; its fills are tab20's light shades, so it does not clash with
the classic figures of a paper either, but its fonts do. `rdf-triples` and `vowl-schema` are plain TikZ on
`classicfig.sty` (DejaVu Sans and DejaVu Sans Mono).

A general knowledge-graph neighbourhood (entities coloured by type, relation labels along the edges, no
schema) is not one of these notations; draw it as `networkx.draw` would, in the classic colours, with the
coordinates computed in Python (see Layout rules, rule 1).

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

1. **Place by hand for a figure of a dozen nodes; compute larger ones.** Hand placement gives aligned rows and
   free label space that no force layout does. Past about fifteen nodes, compute the positions in Python
   (`networkx.spring_layout` with a fixed seed, or Graphviz `dot` for a hierarchy) and paste the coordinates,
   as the classic style does with its numbers. The graphdrawing library needs LuaLaTeX and moves nodes
   whenever the graph changes.
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
6. **Keys: one symbol per row, placed on the text's centre line.** Draw each symbol as its own node at the
   same y as its text, in a `\graphkey` frame. An inline `\tikz` inside a legend node inherits that node's
   `anchor` and drifts below the text (see `pitfalls.md`); cardfig's `\legswatch` sets `anchor=center` for
   this reason.
7. **Size: one column is 12 to 13 cm here.** All three examples fit the 13.8 cm budget of a 5.5 in text
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

- The notation is the published one: shapes and colours as above, no invented symbol without a key entry.
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
