# Reference-textbook figure credits

The four files below are reproduced **without modification** from Chapter 2 of *Computational Cognitive Neuroscience*, fifth edition. Copyright © 2024 Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors. They remain attributed to those creators, rather than to the author of this textbook.

- Source repository: https://github.com/compcogneuro/book
- Pinned source commit: `e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d`
- Edition/copyright statement: https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/frontmatter.md
- Source chapter: https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/chapter-02.md
- License: Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/
- Full source license, including disclaimer of warranties: https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/LICENSE

The fifth-edition source is distinct from the supplied first-edition PDF snapshot. Figure titles and source labels are used to identify the images independently of changing online figure numbering. Only display width and surrounding explanatory captions are set in this textbook; the source pixels are unchanged. No endorsement is implied.

| Local image | Source file under `figures/` | Source figure label | SHA-256 |
|---|---|---|---|
| `ccn-neuron-detector.png` | `fig_neuron_as_detect.png` | `fig-neuron-as-detect` | `914b4cf056a904be0e54305cd94b5469df441a21413b3cc6737683289b11b1a5` |
| `ccn-synapse.png` | `fig_synapse.png` | `fig-synapse` | `a9713263d3d6c6a9bc8146948c6332383295325783699bd46c443b26c138b8b3` |
| `ccn-excitation-inhibition.png` | `fig_vm_as_tug_of_war.png` | `fig-vm-as-tug-of-war` | `9f95f54b1dc842934793d7f232150596dca7bf7e0abcfd56a1f2451cafca0b9f` |
| `ccn-integration-cases.png` | `fig_vm_as_tug_of_war_cases.png` | `fig-vm-as-tug-of-war-cases` | `d156a4532fe61acc1c1bc5e1068f0a31a6a0dbfd7e50c97e9e6ee45a69f13c92` |

The two tug-of-war images are retained as attributed source assets but are no longer displayed in Chapter 1. The chapter uses the original `excitation-inhibition-balance.svg` teaching illustration instead.


## Original RC circuit and LIF examples

`lif-rc-circuit.svg`, `lif-rc-charging.png`, `lif-temporal-integration.png`,
and `lif-spatial-integration.png` are original teaching illustrations, not
reproductions of reference-book artwork. `lif-neuron-model.png` is regenerated
from the same self-contained notebook model. The RC circuit follows the
standard formulation in W. Gerstner et al., *Neuronal Dynamics*, Cambridge
University Press, 2014, sec. 1.3.1, Fig. 1.6:
https://neuronaldynamics.epfl.ch/online/Ch1.S3.html .

Reproduce the diagram, all four plots, and `notebooks/lif_neuron.ipynb` with
`python tools/build_lif_examples.py`. Code and notebook are released under the
repository code license; original diagram and explanatory captions use the
repository text license. All parameter values are stated teaching assumptions.
