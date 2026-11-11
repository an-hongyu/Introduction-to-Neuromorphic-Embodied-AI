---
title: Introduction to Neuromorphic Embodied AI
---

# Introduction to Neuromorphic Embodied AI

**From Spatial Neural Circuits to Autonomous Learning Robots**

*An open, computational textbook by Hongyu An*

```{image} assets/cover.svg
:alt: Stylized cover showing a mobile robot, spatial firing fields, and a neural navigation circuit
:width: 100%
```

## Learn spatial intelligence by building it

How can a robot form a spatial representation, remember where it has been, and learn to navigate from experience? This book connects biological spatial cognition to computational cell models, spiking neural networks, associative learning, and robotic control.

Each computational chapter links **biological evidence**, **explicit assumptions**, **mathematical models**, **executable Python**, and **experiments**. No biological claim should be inferred solely from the behavior of a simulation.

:::{card} Start here
Begin with [Chapter 1: Neuroscience Background](chapters/01-neuroscience-background.md), then study [Chapter 2: Spatial Cells](chapters/02-spatial-cells.md), [Chapter 3: Computational Models of Neurons](chapters/03-computational-neuron-models.md), and [Chapter 4: Hebbian Learning](chapters/04-hebbian-learning.md).
:::

## A four-chapter foundation

| Chapter | Central question | Worked material |
|---|---|---|
| [1. Neuroscience Background](chapters/01-neuroscience-background.md) | What are neurons, spikes, and synapses? | Membrane time constant and synaptic-current examples |
| [2. Spatial Cells](chapters/02-spatial-cells.md) | How is activity related to space, movement, and time? | Original tuning diagrams and occupancy calculations |
| [3. Computational Models of Neurons](chapters/03-computational-neuron-models.md) | How do equations produce neural activity? | Poisson counts, LIF derivation, and executable LIF notebook |
| [4. Hebbian Learning](chapters/04-hebbian-learning.md) | How can experience change connections? | Outer-product association, Oja's rule, STDP, and eligibility traces |

The neuroscience background draws on *Principles of Neural Science*, fifth edition. References use IEEE-style numbered citations with clickable source links. Equations, figures, and worked examples connect biological concepts to reproducible computational assumptions.

## Computational laboratories

- [Computational Models of Neurons: laboratory guide](chapters/computational-neuron-models-lab.md): begin with model choice, units, simulation steps, and validation.
- [Laboratory 1: LIF Neuron](notebooks/lif_neuron.ipynb): membrane integration, threshold, reset, and analytical checks.
- [Laboratory 2: Place Cells](notebooks/place_cells.ipynb): trajectory, stochastic spikes, and occupancy-normalized maps. See the [Place Cell laboratory guide](chapters/04-place-cells.md).
- [Laboratory 3: Hebbian Learning](notebooks/hebbian_learning.ipynb): paired-pattern association, ambiguous cues, and an illustrative STDP window.

Read the [Neuromorphic Embodied AI overview](chapters/01-introduction.md) for the closed-loop robot context and the [development roadmap](chapters/roadmap.md) for later topics.

## Learning outcomes

- Explain the distinction between biological findings and idealized computational models.
- Generate place-cell firing-rate fields and stochastic spike trains.
- Examine how occupancy, spike counts, and sampling affect spatial tuning estimates.
- Develop toward grid, head-direction, boundary, speed, and time-cell models.
- Integrate spatial representations with spiking learning and robot navigation.

## For students and researchers

Prerequisites: introductory Python, linear algebra, elementary probability, and basic neuroscience vocabulary. The laboratories use NumPy and Matplotlib and run on a standard laptop or Google Colab.

> **Project status.** The four foundation chapters and three executable laboratories are available. The later chapters listed in the roadmap are planned, not completed. The Spike Flow Networks material will be labeled as a research framework and separated from established neuroscience.

## Citation

An, H. (2026). *Introduction to Neuromorphic Embodied AI* (online textbook, first teaching release).
