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
| [3. Computational Models of Neurons](chapters/03-computational-neuron-models.md) | How do equations produce neural activity? | Poisson counts, LIF interactive examples, HH gates, and sodium-ablation notebook |
| [4. Hebbian Learning](chapters/04-hebbian-learning.md) | How can experience change connections? | Association, Oja, STDP, eligibility traces, and paired-cue controls |

The neuroscience background draws on *Principles of Neural Science*, fifth edition. References use IEEE-style numbered citations with clickable source links. Equations, figures, and worked examples connect biological concepts to reproducible computational assumptions.

## From course topics to an embodied experiment

The [course-to-book reading map](chapters/course-reading-map.md) connects lectures, worked examples, and the final project. Continue with the following chapters after the four foundations.

| Chapter | What you build or evaluate |
|---|---|
| [5. Neural Encoding and the ANN–SNN Bridge](chapters/05-neural-encoding.md) | Explicit feature, current, rate, and latency contracts |
| [6. Visual Perception](chapters/06-visual-perception.md) | RGB cue features and LIF responses |
| [7. Inertial Sensing](chapters/07-inertial-sensing.md) | A causal vibration detector with units and timing |
| [8. LiDAR Encoding](chapters/08-lidar-encoding.md) | Thirty-six sectors, missing-data masks, and coordinate frames |
| [9. Nengo, ROS 2, and Gazebo](chapters/09-nengo-ros-gazebo.md) | One executable Nengo neuron and a staged simulator integration guide |
| [10. An Associative Learning Robot](chapters/10-associative-learning-robot.md) | A controlled cue-pairing experiment and robot validation protocol |

## Computational laboratories

- [Computational Models of Neurons: laboratory guide](chapters/computational-neuron-models-lab.md): begin with model choice, units, simulation steps, and validation.
- [Laboratory 1: LIF Neuron](notebooks/lif_neuron.ipynb): membrane integration, threshold, reset, and analytical checks.
- [Laboratory 2: Place Cells](notebooks/place_cells.ipynb): trajectory, stochastic spikes, and occupancy-normalized maps. See the [Place Cell laboratory guide](chapters/04-place-cells.md).
- [Laboratory 3: Hebbian Learning](notebooks/hebbian_learning.ipynb): paired-pattern association, ambiguous cues, and an illustrative STDP window.

- [Laboratory 4: Hodgkin–Huxley](notebooks/hodgkin_huxley.ipynb): gates, ionic currents, sodium ablation, and numerical checks.
- [Laboratory 5: Conditioning](notebooks/conditioning.ipynb): paired/unpaired/frozen controls and LIF recall.
- [Laboratory 6: Sensory Encoding](notebooks/sensory_encoding.ipynb): synthetic RGB, vibration, and 36-channel LiDAR.
- [Laboratory 7: One Neuron in Nengo](notebooks/nengo_single_neuron.ipynb): normalized-current simulation and rate validation.

Read the [Neuromorphic Embodied AI overview](chapters/01-introduction.md) for the closed-loop robot context and the [development roadmap](chapters/roadmap.md) for later topics.

## Learning outcomes

- Explain the distinction between biological findings and idealized computational models.
- Generate place-cell firing-rate fields and stochastic spike trains.
- Examine how occupancy, spike counts, and sampling affect spatial tuning estimates.
- Develop toward grid, head-direction, boundary, speed, and time-cell models.
- Integrate spatial representations with spiking learning and robot navigation.

## For students and researchers

Prerequisites: introductory Python, linear algebra, elementary probability, and basic neuroscience vocabulary. The laboratories use NumPy and Matplotlib and run on a standard laptop or Google Colab. Laboratory 7 also uses Nengo; installation instructions and pinned dependencies are provided.

> **Project status.** Ten chapters and seven executable laboratories are available. The ROS 2/Gazebo chapters provide integration and evaluation guides; a complete simulated robot has not been validated in this release. Advanced topics listed in the roadmap remain planned. The Spike Flow Networks material will be labeled as a research framework and separated from established neuroscience.

## Citation

An, H. (2026). *Introduction to Neuromorphic Embodied AI* (online textbook, first teaching release).
