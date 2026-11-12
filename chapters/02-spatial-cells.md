---
title: "Chapter 3 · Spatial Cells"
---

## 3.1 Learning objectives: from spikes to representations

[Chapter 1](01-neuroscience-background.md) described how neurons signal. This chapter asks what a neuron's activity is related to while an animal moves. By the end of this chapter, you should be able to:

- Distinguish place-cell, grid-cell, head-direction-cell, and boundary-related firing patterns.
- Explain how movement speed and temporal context relate to spatial neural activity.
- Interpret a spatial firing-rate map.
- Distinguish observed neural correlations from demonstrated causal mechanisms.

The hippocampal formation and connected regions, including entorhinal cortex, are important for spatial and memory-related processing [[1]](#spatial-ref-1). We will use “spatial cells” as a teaching umbrella for experimentally characterized tuning patterns and their supporting signals. These labels do not imply that the brain contains independent, perfectly separated modules for every variable.

## 3.2 What does “a cell represents position” mean?

Suppose we record spikes while tracking an animal's position $\mathbf{x}(t)$, heading $\theta(t)$, and speed $v(t)$. Saying that a cell has spatial tuning means that its discharge statistics depend on spatial variables in the measured conditions. A useful descriptive object is a conditional rate,

$$
r_i(\mathbf{x},\theta,v,c)=\mathbb{E}\!\left[\frac{N_i(t,t+\Delta t)}{\Delta t}\;\middle|\;\mathbf{x},\theta,v,c\right],
$$

where $N_i(t,t+\Delta t)$ is a spike count, $\Delta t$ is a short observation interval, and $c$ summarizes context. This expression defines what is being estimated; it does not prescribe the circuit that produces it.

A **tuning model** predicts activity from a behavioral variable. A **neuron dynamics model**, developed in [Chapter 2](03-computational-neuron-models.md), predicts how internal state evolves and generates spikes. A Gaussian place field is a tuning model; a leaky integrate-and-fire neuron is a dynamics model. The two can be combined, but one is not evidence for the other.

## 3.3 Place cells: location-selective activity

O'Keefe and Dostrovsky reported hippocampal units with activity related to the animal's location [[2]](#spatial-ref-2). A region in which a cell fires more strongly is called a **place field**. The field is defined in the conditions of a recording session, not as a permanent GPS coordinate stored in the neuron.

Place-cell activity can depend on context and experience. A field can change when the environment or task changes; such changes are often discussed under **remapping** [[1]](#spatial-ref-1). Neither one Gaussian per neuron nor a fixed field center across all environments is a biological requirement.

For a transparent teaching example, set

$$
r(\mathbf{x})=r_0+(r_{\mathrm{peak}}-r_0)
\exp\!\left[-\frac{\|\mathbf{x}-\boldsymbol{\mu}\|^2}{2\sigma^2}\right].
$$

Here $r_0$ and $r_{\mathrm{peak}}$ are baseline and peak rates in Hz; $\boldsymbol{\mu}$ is a preferred location in meters; and $\sigma$ sets field width in meters. This is a deliberately imposed, circular field, not a model of how a place field develops.

**Worked example.** If $r_0=0.2$ Hz, $r_{\mathrm{peak}}=25$ Hz, and $\sigma=0.14$ m, the rate at the field center is 25 Hz. At a distance of one $\sigma$, it is $0.2+24.8e^{-1/2}\approx15.24$ Hz. A short stochastic spike count can still be zero at either position.

## 3.4 Grid cells: repeated spatial firing fields

Grid cells in medial entorhinal cortex can exhibit multiple firing fields arranged in an approximately hexagonal spatial pattern [[3]](#spatial-ref-3). Three descriptive properties are particularly useful:

| Property | Meaning |
|---|---|
| Spacing | Distance scale between neighboring firing fields |
| Orientation | Rotation of the spatial pattern relative to an external reference |
| Phase | Translation of the pattern within the environment |

Unlike a single localized place field, a grid pattern repeats. A single grid cell is therefore ambiguous about absolute position: several separated positions can produce similar activity. Population patterns, other spatial signals, and context help resolve such ambiguity.

Grid activity motivates models of path integration, in which self-motion updates an internal location estimate. That interpretation is a hypothesis to implement and evaluate, not a consequence of drawing a hexagonal pattern.

### 3.4.1 From grid spacing to a place-like readout

The [Grid Cells and Grid-to-Place Mapping section](grid-to-place.md) now provides the complete cosine equations, spacing–frequency conversion, orientation/phase conventions, and weighted threshold readout. It follows Liu et al.'s published grid/threshold framework and an available later author manuscript, with all teaching extensions identified. An embedded interactive experiment lets you vary spacing, angle, phase, gain, baseline, weights, population size, and threshold. [Laboratory 8](../notebooks/grid_to_place.ipynb) reproduces the equations in editable Python.

Start with one grid, compare six identical grids, then try six diverse inputs. Repeated fields survive the first two constructions. A designed common peak in the diverse example illustrates a possible readout, not a demonstrated learning mechanism.

## 3.5 Head-direction cells: orientation rather than travel direction

Head-direction cells discharge preferentially when the animal's head points in a particular direction relative to a reference frame [[4]](#spatial-ref-4). Heading is different from location, and it is also different from the velocity direction: an animal can turn its head while stationary or move with its head oriented away from its travel direction.

A computational compass might use a circular tuning curve,

$$
r(\theta)=r_0+A\exp\!\left[\kappa\bigl(\cos(\theta-\theta_0)-1\bigr)\right],
$$

where $\theta$ and $\theta_0$ are angles in radians, $A$ is the peak rate above baseline, and $\kappa$ controls angular concentration. This chosen curve respects angular wraparound: $1^\circ$ and $359^\circ$ are close, despite a naive subtraction giving $358^\circ$.

For a robot, distinguish body yaw, sensor orientation, and motion direction explicitly before choosing which variable drives a head-direction-like population.

## 3.6 Border and boundary-related cells: geometry as a reference

Entorhinal border cells can show elevated firing near environmental boundaries [[5]](#spatial-ref-5). Broader boundary-related modeling also considers distance and direction to a boundary. These descriptions should not be collapsed into the statement that every boundary-related cell is simply a distance-to-the-nearest-wall sensor.

A robot's LiDAR beam reports range along a sensor-relative direction. A wall-related response defined in an environment-fixed frame requires additional geometry and an orientation estimate. Thus, one LiDAR sector is not automatically one biological border cell. The proposed 36-sector encoder is a sensor representation that could supply inputs to a later spatial network.

## 3.7 Speed cells and time cells: complementary variables

Speed-related entorhinal activity provides evidence for a movement-related signal that can support navigation models [[6]](#spatial-ref-6). A simple teaching rate might increase with nonnegative speed, but any such relationship must be tested over the speeds and behavioral states actually sampled. Speed measures movement magnitude; heading provides an angular reference.

Hippocampal **time cells** can show sequential activity related to elapsed time within a task interval [[7]](#spatial-ref-7). They are included here because navigation and memory unfold in time, not because time tuning is itself spatial location tuning. A sequence tied to time may also be influenced by position, movement, and task structure; an experiment needs to separate these possibilities.

Grid-to-place interactions also cannot be reduced to a universally established one-way conversion [[8]](#spatial-ref-8).

```{figure} ../assets/spatial-cell-tuning.png
:label: fig-spatial-tuning
:alt: Six synthetic panels showing place, grid, heading, boundary, speed, and elapsed-time tuning
:width: 100%

Synthetic tuning examples. All fields and curves are generated from explicit teaching functions; none are recordings or evidence that a circuit learned these representations. Spatial axes are in meters, angular axes in degrees, rates in Hz, and elapsed time in seconds.
```

## 3.8 How to estimate a spatial firing-rate map

For spatial bin $b$, let $K_b$ be the number of recorded spikes and $T_b$ the time spent in the bin. An occupancy-normalized estimate is

$$
\widehat r_b=\frac{K_b}{T_b},\qquad T_b>0.
$$

Consider two bins: one has 20 spikes in 2 s, and another has 10 spikes in 0.5 s. Raw spike counts rank the first bin higher, but the estimated rates are 10 Hz and 20 Hz, respectively. Unvisited bins have no rate estimate; they should be masked rather than assigned a biological rate of zero.

For a defensible analysis, record position and spikes on an aligned time base, report occupancy and bin size, impose a stated minimum occupancy, and assess reproducibility across sessions or trials. If you smooth a map, report the procedure and do not treat smooth appearance as independent evidence of tuning. For a learned decoder, separate fitting from evaluation and avoid randomly splitting highly adjacent trajectory samples without considering temporal dependence.

## 3.9 A robot example and the first laboratory

Imagine a robot at $(0.5,0.4)$ m facing north near the east wall. A place-like population can depend on its location; a heading population can depend on its orientation; boundary-related inputs can depend on the east wall; and speed-related signals can remain low if it is stationary. These signals describe different aspects of the same state.

A successful localization system must estimate state from available observations and motion. Supplying the true simulated position to a tuning function demonstrates encoding only. It does not show that the robot can infer its position, learn a map, or navigate to a goal.

Continue with the [Place Cell laboratory guide](04-place-cells.md) and [executable Place Cell notebook](../notebooks/place_cells.ipynb). The notebook uses a one-meter-square arena, a 300 s synthetic trajectory, and Poisson spike counts. It reports occupancy coverage and errors relative to the imposed rate field.

## 3.10 Exercises

1. Explain why one grid cell cannot uniquely identify position across a large environment.
2. Give a situation in which head orientation and travel direction differ.
3. Calculate rates for bins with $(K_b,T_b)=(12,0.6\,\mathrm{s})$ and $(30,3\,\mathrm{s})$.
4. Design a control that helps distinguish speed-related firing from firing caused by repeated visits to one location.
5. Explain why an imposed Gaussian place field and a learned place field require different evidence.
6. List the transformations needed to convert a body-relative LiDAR observation into an environment-relative boundary measurement.

## References

(spatial-ref-1)=

[1] Eric R. Kandel, James H. Schwartz, Thomas M. Jessell, Steven A. Siegelbaum, and Albert James Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013, chs. 17 and 67. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(spatial-ref-2)=

[2] John O'Keefe and Jonathan O. Dostrovsky, “The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat,” *Brain Research*, vol. 34, no. 1, pp. 171–175, 1971, doi: [10.1016/0006-8993(71)90358-1](https://pubmed.ncbi.nlm.nih.gov/5124915/).

(spatial-ref-3)=

[3] Torkel Hafting, Marianne Fyhn, Sturla Molden, May-Britt Moser, and Edvard I. Moser, “Microstructure of a spatial map in the entorhinal cortex,” *Nature*, vol. 436, pp. 801–806, 2005, doi: [10.1038/nature03721](https://pubmed.ncbi.nlm.nih.gov/15965463/).

(spatial-ref-4)=

[4] Jeffrey S. Taube, Robert U. Muller, and James B. Ranck, Jr., “Head-direction cells recorded from the postsubiculum in freely moving rats. I. Description and quantitative analysis,” *The Journal of Neuroscience*, vol. 10, no. 2, pp. 420–435, 1990, doi: [10.1523/JNEUROSCI.10-02-00420.1990](https://pubmed.ncbi.nlm.nih.gov/2303851/).

(spatial-ref-5)=

[5] Trygve Solstad, Charlotte N. Boccara, Emilio Kropff, May-Britt Moser, and Edvard I. Moser, “Representation of geometric borders in the entorhinal cortex,” *Science*, vol. 322, no. 5909, pp. 1865–1868, 2008, doi: [10.1126/science.1166466](https://pubmed.ncbi.nlm.nih.gov/19095945/).

(spatial-ref-6)=

[6] Emilio Kropff, James E. Carmichael, May-Britt Moser, and Edvard I. Moser, “Speed cells in the medial entorhinal cortex,” *Nature*, vol. 523, pp. 419–424, 2015, doi: [10.1038/nature14622](https://pubmed.ncbi.nlm.nih.gov/26176924/).

(spatial-ref-7)=

[7] Christopher J. MacDonald, Kyle Q. Lepage, Uri T. Eden, and Howard Eichenbaum, “Hippocampal ‘time cells’ bridge the gap in memory for discontiguous events,” *Neuron*, vol. 71, no. 4, pp. 737–749, 2011, doi: [10.1016/j.neuron.2011.07.012](https://pubmed.ncbi.nlm.nih.gov/21867888/).

(spatial-ref-8)=

[8] Daniel Bush, Caswell Barry, and Neil Burgess, “What do grid cells contribute to place cell firing?,” *Trends in Neurosciences*, vol. 37, no. 3, pp. 136–145, 2014, doi: [10.1016/j.tins.2013.12.003](https://pubmed.ncbi.nlm.nih.gov/24485517/).


## Additional Reading Materials

Start with the original place-cell [[2]](#spatial-ref-2) and grid-cell [[3]](#spatial-ref-3) studies, then read the grid-to-place review [[8]](#spatial-ref-8). For an engineering bridge, compare the body-relative measurements in [Chapter 8](08-lidar-encoding.md) with the environment-relative spatial representations here. A 36-channel range encoder is a sensory input, not evidence that it implements 36 biological border cells.
