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

- [Place Cell laboratory guide](04-place-cells.md) and [Laboratory 1 notebook](../notebooks/place_cells.ipynb).
- [Laboratory 2: LIF Neuron](../notebooks/lif_neuron.ipynb).
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
