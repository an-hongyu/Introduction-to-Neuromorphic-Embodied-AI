# Chapter 4 literature-figure credits

This record covers the seven external figures introduced in the expanded Spatial Cells chapter. Their copyright remains with the original authors. Each is credited next to its displayed figure and linked to its scientific source in the chapter references. The figures below are used under the Creative Commons Attribution 4.0 International license: https://creativecommons.org/licenses/by/4.0/ . No inference should be made that other figures in the same publications have the same rights when a separate credit line applies.

The build saves local JPEG copies in `assets/spatial-literature/`; the published HTML serves the copies with the rest of the book. Transformations are limited to image-format conversion and proportional resizing for the web. No panels are removed or rearranged, and no plotted observations, axes, or labels are changed. Downloaded bytes, accepted source URLs, and original dimensions are recorded in `source-downloads.json` by `tools/fetch_spatial_figures.py`.

| Local filename | Original authors and publication | Figure | Source and rights |
|---|---|---|---|
| `hippocampal-circuit.jpg` | Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 5th ed., 2024 | Chapter 7, `fig_hippo_mem_formation.png` | [Pinned textbook chapter](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/chapter-07.md); [frontmatter and license](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/frontmatter.md). CC BY 4.0. |
| `place-fields.jpg` | Mary Ann Go, Jake Rogers, Giuseppe P. Gava, Catherine E. Davey, Seigfred Prado, Yu Liu, and Simon R. Schultz, 2021 | Figure 6 | [Frontiers in Cellular Neuroscience article](https://doi.org/10.3389/fncel.2021.618658). Copyright 2021 the authors; CC BY 4.0. |
| `grid-fields.jpg` | Jose Antonio Perez-Escobar, Olga Kornienko, Patrick Latuske, Laura Kohler, and Kevin Allen, 2016 | Figure 2 | [eLife article](https://elifesciences.org/articles/16937). Copyright 2016 the authors; CC BY 4.0. |
| `head-direction.jpg` | Patricia Preston-Ferrer, Stefano Coletta, Markus Frey, and Andrea Burgalossi, 2016 | Figure 3 | [eLife article](https://elifesciences.org/articles/14592). Copyright 2016 the authors; CC BY 4.0. |
| `border-fields.jpg` | Jose Antonio Perez-Escobar, Olga Kornienko, Patrick Latuske, Laura Kohler, and Kevin Allen, 2016 | Figure 5 | [eLife article](https://elifesciences.org/articles/16937). Copyright 2016 the authors; CC BY 4.0. |
| `speed-cells.jpg` | Davide Spalla, Alessandro Treves, and Charlotte N. Boccara, 2022 | Figure 2 | [Nature Communications article](https://doi.org/10.1038/s41467-022-29583-z). Copyright 2022 the authors; CC BY 4.0. |
| `time-distance-cells.jpg` | Shai Abramson, Benjamin J. Kraus, John A. White, Michael E. Hasselmo, Dori Derdikman, and Genela Morris, 2023 | Figure 2 | [eLife article](https://doi.org/10.7554/eLife.83930); [full text and rights statement](https://pmc.ncbi.nlm.nih.gov/articles/PMC10712950/). Copyright 2023 the authors; CC BY 4.0. The separately restricted Elsevier apparatus panel in Figure 1A is NOT reproduced. |

## Reproducing the website locally

Before the usual book build, fetch and validate these assets:

```bash
python tools/fetch_spatial_figures.py
python tests/execute_notebook.py
BASE_URL=/Introduction-to-Neuromorphic-Embodied-AI jupyter book build --html --strict
python tests/check_build.py
```

The fetch script fails on missing/invalid images rather than replacing them with an unrelated illustration or silently publishing a broken figure. The source TIFFs are not redistributed; the reader-facing web images and their attribution are included in the build.

The existing `assets/spatial-cell-tuning.png` is separate: it contains synthetic teaching functions generated for this textbook, not recordings from any of the papers above. No complete third-party book or reference PDF is included.
