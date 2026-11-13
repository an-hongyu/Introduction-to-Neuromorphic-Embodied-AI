# Chapter 3: Hebbian lecture figure provenance

These four **book-optimized SVG diagrams are redrawn from the author's supplied PowerPoint**, rather than screenshots of complete lecture slides. Their scientific framing, three-stage protocol, four threshold-rule cases, and pre/post spike order come from *Neuromorphic Robotic Systems — Topic 3: Computational Models of Neural Systems, Hebbian's Rule* by Hongyu An, Michigan Technological University (undated PPTX supplied to the textbook project).

| Textbook asset | Lecture slide(s), 1-based | Content retained |
|---|---|---|
| `hebbian-pairing-protocol.svg` | 18–21 | Presynaptic test spike, concurrent training spikes, and increased test EPSP |
| `four-hebbian-threshold-rules.svg` | 24–28 | Four quadrant-wise alternatives for LTP, LTD and no modeled update |
| `rate-threshold-plasticity.svg` | 29 | Below-threshold depression and above-threshold potentiation as a function of postsynaptic firing rate |
| `stdp-spike-ordering.svg` | 30–34 | Pre-before-post versus post-before-pre spike timing and signed weight changes |

**Explicit adaptation:** The STDP plot in the supplied slides uses an abscissa that makes pre-before-post negative. Chapter 3 defines `delta t = t_post - t_pre`, so the new SVG intentionally reverses the plotted sign and changes the labels to match the chapter's mathematical convention. These SVGs are explanatory schematics, not extracted experimental data or fitted biological response curves.

**Scope:** The four thresholded rules are alternatives, not four sequential stages. Illustrative curve amplitudes and spike separation are not quantitative measurements from the source slides. Consult the chapter references for the original Hebb theory, LTP evidence, Oja normalization, and experimental STDP studies.
