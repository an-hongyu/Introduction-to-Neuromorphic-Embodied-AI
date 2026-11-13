---
title: Course-to-Book Reading Map
---

# Course-to-Book Reading Map

This map connects the supplied course lectures and final project to the textbook. Lecture filenames and internal topic numbers are not always consistent, and the course folders contain overlapping published and lecture copies. Use **topic names and scientific content** rather than assuming that a filename's number is the final teaching order.

## Topic crosswalk

| Course material | Textbook destination | Worked activity and present scope |
|---|---|---|
| Introduction; neurons | [Chapter 1](01-neuroscience-background.md) | Membrane voltage, threshold, temporal/spatial integration, original biological schematics |
| Synapses; associative learning and plasticity | [Chapters 1](01-neuroscience-background.md) and [3](04-hebbian-learning.md) | Transmission, excitation/inhibition, bounded learning versus Oja/STDP |
| Spatial representations | [Chapter 4](02-spatial-cells.md) | Primary evidence and each cell type's model, grid-to-place interaction, occupancy normalization, and spatial notebooks |
| Hodgkin–Huxley model | [Chapter 2, HH section](03-computational-neuron-models.md#fig-hh-course-dynamics) | Complete gates/units, RK4 notebook, sodium ablation and convergence checks |
| Leaky integrate-and-fire model | [Chapter 2](03-computational-neuron-models.md) | RC circuit, embedded interactive experiment, temporal and multisource integration |
| Hebbian learning | [Chapter 3](04-hebbian-learning.md) | Outer-product memory and controlled visual–vibration association |
| Visual Perception I/II | [Chapter 6](06-visual-perception.md) | Lecture-based light and imaging, CCD/CMOS/Bayer, tristimulus and color matching, image arrays, mean/Gaussian filters, chroma keying, and the existing RGB-to-LIF experiment |
| IMU | [Chapter 7](07-inertial-sensing.md) | Units/frames, gravity limitations, causal RMS vibration detector |
| LiDAR | [Chapter 8](08-lidar-encoding.md) | Lecture ranging, scanning, point clouds, original images/animations/videos, weather, motion distortion, and return ambiguities; 36-sector encoding with validity masks and coordinate transforms |
| ROS, Nengo, Gazebo project preparation | [Chapter 9](09-nengo-ros-gazebo.md) | Executed single-cell Nengo notebook; simulator integration milestones and message contract |
| Final associative robot project | [Chapter 10](10-associative-learning-robot.md) | CS/US protocol, executed NumPy/LIF example, controls, frozen evaluation, Gazebo extension guide |

The foundation sequence is Neurons and Synapses (Chapter 1), Computational Models of Neurons (Chapter 2), Hebbian Learning and Synaptic Plasticity (Chapter 3), and Spatial Cells and Their Models (Chapter 4). Sensory and implementation material follows them rather than inserting an unexplained coding laboratory ahead of neuron models. Spatial-cell research remains central: sensory measurements are explicitly distinguished from place/grid/border representations.

## Eight executable laboratories

| Laboratory | Notebook | Main experiment |
|---|---|---|
| 1 | [LIF neuron](../notebooks/lif_neuron.ipynb) | RC dynamics, temporal/multisource integration, analytical rate |
| 2 | [Place Cells](../notebooks/place_cells.ipynb) | Synthetic trajectory, stochastic spikes, occupancy-normalized map |
| 3 | [Hebbian association](../notebooks/hebbian_learning.ipynb) | Partial cues and an illustrative STDP window |
| 4 | [Hodgkin–Huxley](../notebooks/hodgkin_huxley.ipynb) | Gates, signed ionic currents, sodium ablation, time-step refinement |
| 5 | [Conditioning](../notebooks/conditioning.ipynb) | Paired/unpaired/frozen schedules and separate LIF recall |
| 6 | [Sensory encoding](../notebooks/sensory_encoding.ipynb) | Synthetic vision, causal vibration, and LiDAR masks |
| 7 | [One neuron in Nengo](../notebooks/nengo_single_neuron.ipynb) | Normalized-current API example and analytical firing-rate check |
| 8 | [Grid Cells to Place-Like Fields](../notebooks/grid_to_place.ipynb) | Cosine grid geometry, explicit weighted readout, and periodic-alias controls |

Notebooks are self-contained and link to Colab; download them for local editing. Laboratory 7 additionally requires Nengo. Repository dependencies are pinned where needed for compatibility. Automated builds execute all eight laboratories before publishing.

## What has and has not been demonstrated

Python figures and assertions test explicitly chosen teaching models on synthetic data. They do not validate biological cell identity, camera accuracy, navigation, a Gazebo world, or a neuromorphic hardware deployment. Chapter 9 provides the integration contract, and Chapter 10 specifies the evidence required before claiming a completed robot experiment. Hardware, rodent calibration, and advanced spatial-memory networks remain labeled planned in the [roadmap](roadmap.md).

## Additional Reading Materials

Use the [reference-book reading map](roadmap.md#reference-book-reading-map) for biological and computational background. The explanations, code, and newly generated figures are original teaching material; source books and course slide PDFs are not redistributed.
