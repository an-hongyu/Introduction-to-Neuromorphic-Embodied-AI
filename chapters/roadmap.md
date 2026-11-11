---
title: Curriculum and Development Roadmap
---

# Curriculum and Development Roadmap

The four foundation chapters and three computational laboratories below are available. Later topics remain planned. Chapter numbers follow the revised teaching sequence.

## Part I — Foundations: available

1. [Neuroscience Background](01-neuroscience-background.md): neurons, membrane potential, action potentials, synapses, excitation, and inhibition.
2. [Spatial Cells](02-spatial-cells.md): place, grid, head-direction, border/boundary, speed-related, and time-related activity.
3. [Computational Models of Neurons](03-computational-neuron-models.md): rate/count models, LIF, conductance-based models, and model selection.
4. [Hebbian Learning](04-hebbian-learning.md): two-factor updates, growth constraints, Oja's rule, STDP, and three-factor learning.

## Companion laboratories: available

- [Computational Models of Neurons laboratory guide](computational-neuron-models-lab.md) and [Laboratory 1: LIF Neuron](../notebooks/lif_neuron.ipynb).
- [Place Cell laboratory guide](04-place-cells.md) and [Laboratory 2 notebook](../notebooks/place_cells.ipynb).
- [Laboratory 3: Hebbian Association and STDP](../notebooks/hebbian_learning.ipynb).
- Supplementary [Neuromorphic Embodied AI overview](01-introduction.md).

## Part II — Spatial representations: planned

5. Neural Encoding and Population Representations
6. Place Cell Models and Remapping
7. Grid Cell Models
8. Head-Direction Cell Models
9. Border and Boundary Vector Cells
10. Speed Cells and Path Integration
11. Time Cells and Sequential Encoding

## Part III — Spatial networks and memory: planned

12. Coupling Grid and Place Cells
13. Multimodal Sensory Integration
14. Learning Spatial Representations through Plasticity
15. Cognitive Maps and Population Decoding
16. Associative Memory in Spiking Networks
17. Spike Flow Networks: Models and Testable Hypotheses
18. Reward-Guided Navigation and Memory Consolidation
19. Goal-Directed Navigation and Planning

## Part IV — Embodied implementations and validation: planned

20. LiDAR-to-Spike Encoding (36 sectors, 10 degrees per sector)
21. Spatial Cells in ROS and Gazebo
22. Neuromorphic Hardware Implementation
23. Calibration with Rodent Electrophysiology
24. Benchmarks, Ablations, and Open Problems

## Writing and evidence conventions

Use IEEE-style numbered references in order of first citation within each chapter. Citation numbers link to reference entries, and entries link to DOI records, publisher pages, or authoritative online texts. Define variables and units at their first use and distinguish biological observations from chosen model assumptions.

The neuroscience foundation uses *Principles of Neural Science*, fifth edition, as a reference. Original teaching figures and examples are created for this book. A chapter should distinguish prior experimental evidence, established modeling precedents, pedagogical assumptions, and proposed research. Planned material is not evidence of a completed model or validated robot.


(reference-book-reading-map)=
## Reference-book reading map

The following editions were supplied as course references. The reading selections connect biological explanation, mathematical abstraction, and reproducible experiments; each book has a different emphasis. The current online edition of a living textbook may differ from the supplied snapshot.

| Reference | Selected reading | Role in this textbook |
|---|---|---|
| *Principles of Neural Science*, 5th ed. [[1]](#reading-ref-1) | Chs. 2, 4, 6–8, and 10 | Biological foundations: neurons, membrane signaling, and synapses in Chapter 1 |
| *Neuroscience: Exploring the Brain*, 4th ed. [[2]](#reading-ref-2) | Chs. 2–5; Ch. 25 for learning | An accessible route from cellular structure to resting voltage, action potentials, transmission, and plasticity |
| *Computational Neuroscience: A First Course* [[3]](#reading-ref-3) | Ch. 1; Ch. 2; Secs. 4.3–4.4; Ch. 5 | Membrane equations and reduced models; tuning; association and Oja's rule; population representations |
| *Computational Cognitive Neuroscience*, 1st ed. [[4]](#reading-ref-4) | Chs. 2–4; Ch. 8 | The conceptual progression from neuron to network, learning mechanism, and memory |
| *Artificial Intelligence in the Age of Neural Networks and Brain Computing* [[5]](#reading-ref-5) | Ch. 1, “Nature's Learning Rule: The Hebbian-LMS Algorithm”; Ch. 6, “Evolving and Spiking Connectionist Systems for Brain-Inspired Artificial Intelligence” | Supplementary perspectives on learning algorithms, spike representations, and network design |

For beginners, read the cellular foundations first, then work through the neuron-model guide and LIF notebook. Compare the Place Cell notebook's imposed spatial rate with the dynamical LIF model. Only then study weight updates and their evaluation in the Hebbian laboratory. Learning-rule names should not conceal their differences: the Hebbian-LMS algorithm discussed in the edited volume is a specific construction, not a synonym for every Hebbian or STDP rule.

The explanations and teaching assets in this textbook are original. References support the relevant concepts; numerical teaching parameters and robot examples are explicitly chosen assumptions. Experimental spatial-cell findings continue to be linked to their primary research papers.

### Book references

(reading-ref-1)=
[1] E. R. Kandel, J. H. Schwartz, T. M. Jessell, S. A. Siegelbaum, and A. J. Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(reading-ref-2)=
[2] M. F. Bear, B. W. Connors, and M. A. Paradiso, *Neuroscience: Exploring the Brain*, 4th ed. Philadelphia, PA, USA: Wolters Kluwer, 2016. [National Library of Medicine catalog](https://www.ncbi.nlm.nih.gov/nlmcatalog/101647616).

(reading-ref-3)=
[3] H. A. Mallot, *Computational Neuroscience: A First Course*. Cham, Switzerland: Springer, 2013, doi: 10.1007/978-3-319-00861-5. [Publisher](https://link.springer.com/book/10.1007/978-3-319-00861-5).

(reading-ref-4)=
[4] R. C. O'Reilly, Y. Munakata, M. J. Frank, T. E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 1st ed. Wiki Book, 2012, supplied PDF snapshot generated Aug. 25, 2016. [Institutional publication record](https://experts.colorado.edu/display/pubid_85822); [current online edition](https://book.compcogneuro.org/).

(reading-ref-5)=
[5] R. Kozma, C. Alippi, Y. Choe, and F. C. Morabito, Eds., *Artificial Intelligence in the Age of Neural Networks and Brain Computing*. London, U.K.: Academic Press, 2019. [Publisher](https://www.sciencedirect.com/science/book/9780128154809).
