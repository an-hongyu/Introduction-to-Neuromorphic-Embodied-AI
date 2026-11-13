---
title: "Chapter 4 · Spatial Cells and Their Models"
---

## 4.1 Learning Objectives

A navigation system must represent more than its current coordinates. It needs to distinguish location, orientation, movement, environmental boundaries, and the order of events. This chapter introduces the **hippocampal–entorhinal system** and six experimentally identified response classes: **place cells, grid cells, head-direction cells, border cells, speed cells, and time cells**. The last two supply movement and temporal information rather than location alone. Each cell type is introduced together with its mathematical model and interpretation. The place-cell section contains the grid-to-place readout and interactive experiment; the grid-cell section derives the input fields used by that readout.

By the end of this chapter, you should be able to:

- Identify the hippocampus, dentate gyrus, CA3, CA1, subiculum, and medial and lateral entorhinal cortex, and trace their principal connections.
- Distinguish the experimental signatures of place, grid, head-direction, border, speed, and time cells.
- Read spatial rate maps, polar tuning curves, speed-response curves, and trial-aligned temporal activity plots.
- Construct place, grid, head-direction, border, speed, and time tuning functions with explicit variables and units.
- Implement a weighted grid-to-place readout and explain how spacing, orientation, phase, normalization, and threshold affect its output.
- Explain how self-motion and environmental cues can jointly support navigation, and design controls for competing explanations of neural tuning.
- Relate these representations to neuromorphic robots without treating sensor measurements or simulator ground truth as evidence of biological equivalence.

## 4.2 The hippocampal–entorhinal system

### 4.2.1 A circuit for spatial experience and memory

The **hippocampus** is a medial temporal-lobe structure involved in memory and spatial processing. It is not an isolated position sensor. Its interactions with the **entorhinal cortex (EC)** connect ongoing sensory and contextual information with memory. In rodent navigation experiments, recordings from this wider system reveal neural responses related to location, heading, boundaries, motion, and elapsed time [[1]](#spatial-ref-1).

The hippocampus proper contains the CA fields, including **CA1, CA2, and CA3**. The **dentate gyrus (DG)** and **subiculum** are closely associated components of the hippocampal formation. CA2 is a distinct region even when a simplified teaching diagram omits it. EC is commonly divided into **medial entorhinal cortex (MEC)** and **lateral entorhinal cortex (LEC)**; their contributions differ, but a rigid division into an exclusively spatial MEC and exclusively nonspatial LEC is too strong [[1]](#spatial-ref-1).

A useful first route through the circuit is

$$
\mathrm{EC}\ \longrightarrow\ \mathrm{DG}\ \longrightarrow\ \mathrm{CA3}\ \longrightarrow\ \mathrm{CA1}.
$$

This **trisynaptic pathway** includes entorhinal input to DG, DG mossy-fiber projections to CA3, and CA3 Schaffer-collateral projections to CA1. It is not the whole circuit: EC also projects directly to CA3 and CA1, CA3 contains recurrent connections, and hippocampal output interacts with subiculum and EC. Consequently, a one-way pipeline from grid cells to place cells is not a complete anatomical description [[1]](#spatial-ref-1), [[2]](#spatial-ref-2).

```{figure} ../assets/spatial-literature/hippocampal-circuit.jpg
:label: fig-spatial-hippocampal-circuit
:alt: Open-textbook diagram of cortical pathways converging on entorhinal cortex and hippocampal dentate gyrus, CA3, and CA1
:width: 85%

**The hippocampus in a wider cortical memory system.** Follow cortical inputs toward EC, then compare the indirect route through DG and CA3 with the route to CA1. This is a simplified circuit diagram, not an exhaustive connectivity atlas or a map of mutually exclusive cell classes. Reproduced from O'Reilly and colleagues, *Computational Cognitive Neuroscience*, ch. 7, “Hippocampal Anatomy” [[2]](#spatial-ref-2), under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and converted to JPEG, with no changes to labels or panels.
```

| Region or pathway | Anatomical point to recognize | Modeling question it motivates |
|---|---|---|
| DG | Receives entorhinal input and projects to CA3 | Can similar experiences acquire more distinct representations? |
| CA3 | Receives DG/EC inputs and has recurrent connectivity | Can a partial cue reactivate an associated pattern? |
| CA1 | Receives CA3 and direct entorhinal inputs | How are different information streams combined? |
| Subiculum | Participates in hippocampal output and wider loops | How does spatial activity influence downstream systems? |
| MEC and LEC | Interconnected cortical interfaces with hippocampus | How are motion, landmarks, objects, and context incorporated? |

The questions in the last column are computational interpretations, not a claim that each region performs only one operation. The historical **cognitive-map** account connects hippocampal activity to relations among places, rather than just a chain of learned motor commands [[3]](#spatial-ref-3).

### 4.2.2 A response class is not a complete cell identity

“Place cell” and “grid cell” describe measured firing patterns. They do not by themselves specify a unique molecular identity, a particular neuron equation, or an immutable role. A neuron can show mixed selectivity, and its apparent tuning depends on the environment, behavioral sampling, and analysis.

Let $\mathbf{x}(t)=[x(t),y(t)]^\top$ denote position, $\theta(t)$ heading, $v(t)$ speed, $\tau$ elapsed time from a defined event, and $c$ context. A general descriptive rate is

$$
r_i(\mathbf{x},\theta,v,\tau,c)
=\frac{\mathbb{E}[N_i(t,t+\Delta t)\mid\mathbf{x},\theta,v,\tau,c]}{\Delta t}.
$$

Here $N_i$ is a spike count, $\Delta t$ is in seconds, and $r_i$ is in Hz. Estimating this relationship is different from explaining how a circuit creates it. The LIF, HH, and Izhikevich models in [Chapter 2](03-computational-neuron-models.md) describe neuronal dynamics; the tuning functions below describe relationships between activity and selected variables.

(place-cell-models)=

## 4.3 Place cells and their models

### 4.3.1 Biological signature and experimental discovery

O'Keefe and Dostrovsky reported hippocampal neurons whose discharge depended on where a freely moving rat was located [[4]](#spatial-ref-4). A region associated with elevated firing is a **place field**. Place cells are especially well studied among CA1 and CA3 pyramidal neurons. A population with different preferred locations can provide information about position, although an individual neuron's activity is usually ambiguous and variable.

A place field is not a permanent GPS coordinate. Rotating a salient cue, changing the enclosure, or changing contextual conditions can alter the spatial activity pattern. Such changes are described as **remapping**; a change in preferred location and a change in firing rate within an otherwise similar field are not the same observation [[5]](#spatial-ref-5). Some cells have more than one field, particularly in larger or structured environments.

### 4.3.2 How to read a place-cell figure

Start with the animal's trajectory, then locate activity events along it, and finally examine the occupancy-corrected spatial map. A dense cluster of events can reflect either elevated activity or simply more time spent at that location. Also identify the recording modality: **calcium events are not identical to directly recorded spikes**.

```{figure} ../assets/spatial-literature/place-fields.jpg
:label: fig-spatial-place-recordings
:alt: Published open-field trajectories with activity-event locations and normalized CA1 place-field maps, with population field distributions and between-session changes
:width: 100%

**Place-selective activity in an open environment.** In panel A, compare the event locations above each normalized spatial map; the other panels describe field positions, sizes, information, and session-to-session shifts. These are calcium-imaging results from head-fixed mice navigating an air-floating real-world platform, not extracellular spike recordings from freely moving rats. Reproduced from Go et al., Fig. 6 [[6]](#spatial-ref-6), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and format-converted only.
```

(place-gaussian-model)=

### 4.3.3 Gaussian place-field model

A convenient teaching approximation is a circular Gaussian:

$$
r_i(\mathbf{x})=r_0+(r_{\mathrm{peak}}-r_0)
\exp\!\left[-\frac{\|\mathbf{x}-\boldsymbol\mu_i\|^2}{2\sigma_i^2}\right].
$$

$\boldsymbol\mu_i$ is the preferred location, $\sigma_i$ is field width, and both use meters; $r_0$ and $r_{\mathrm{peak}}$ are rates in Hz. With $r_0=0.2$ Hz, $r_{\mathrm{peak}}=25$ Hz, and $\sigma_i=0.14$ m, the center rate is 25 Hz and the rate one $\sigma_i$ away is $0.2+24.8e^{-1/2}\approx15.24$ Hz.

This equation **imposes** a field. It does not explain learning, remapping, or the origin of its inputs. A model claiming place-field formation must specify plasticity, experience, and held-out tests. A robot whose true simulator position drives this equation is demonstrating an encoder, not autonomous localization.

(place-spike-generation)=

### 4.3.4 From a place-field rate to spike events

For a simulation time step $\Delta t$ in seconds, assume conditionally independent, inhomogeneous Poisson firing. The number of spikes in a bin has distribution

$$N_i[t]\sim\operatorname{Poisson}(r_i(\mathbf{x}_t)\Delta t).$$

For bins small enough that multiple events are rare, a binary event can be drawn with probability $1-\exp[-r_i(\mathbf{x}_t)\Delta t]$. In this notebook we sample Poisson counts, which remain valid even for larger bins.

This assumption generates stochastic events from a specified rate; it does not implement membrane dynamics, refractoriness, or learning [[22]](#spatial-ref-22). Reconstruct the rate with the occupancy-normalized estimator in [Section 4.8](#spatial-tuning-estimation), and compare it with the imposed field on sufficiently visited bins.

(grid-place-readout)=

### 4.3.5 A place-like readout from grid inputs

The threshold-sum construction in Liu et al. [[20]](#spatial-ref-20) becomes executable only after scaling and threshold are specified. Here $g_j$ denotes a grid-rate input; its complete formula is developed in [Section 4.4](#grid-cell-models). A general weighted construction is

$$
z_\ell(\mathbf r)=\sum_j w_{\ell j}g_j(\mathbf r),\qquad
b_\ell(\mathbf r)=\mathbf1[z_\ell(\mathbf r)>T_\ell].
$$

Here $g$ is in Hz, weights are dimensionless, $z$ and $T$ are in Hz, and $b$ is a binary state rather than a firing rate. A zero threshold applied to nonnegative inputs can activate broad parts of the arena. An unspecified step function does not establish localization.

**The exact normalized readout.**

For the single output shown below, use nonnegative grid gain $\kappa_j\geq0$ and normalize each input by its theoretical maximum,

$$
g_{j,\max}=r_G\max(0,3\kappa_j+\zeta_j).
$$

$$
h_j(\mathbf r)=\begin{cases}g_j(\mathbf r)/g_{j,\max},&g_{j,\max}>0,\\0,&g_{j,\max}=0.\end{cases}
$$

For nonnegative weights, compute the weighted mean and rate proxy,

$$
S(\mathbf r)=\frac{\sum_{j=1}^N w_jh_j(\mathbf r)}{\sum_{j=1}^N w_j}.
$$

$$
r_P(\mathbf r)=r_{P,\max}\left[\frac{S(\mathbf r)-\tau}{1-\tau}\right]_+.
$$

Use $0\leq\tau<1$ and $r_{P,\max}=25\ \mathrm{Hz}$. If the total weight is zero, define $S=0$. Then $0\leq S\leq1$ and $0\leq r_P\leq25$ Hz. The associated binary activation is $\mathbf1[S>\tau]$. Both numerator and denominator of $S$ use the selected first $N$ inputs; excluded grids contribute nothing.

This normalization deliberately removes pure multiplicative gain changes when $\zeta=0$. Increasing $\kappa$ changes the raw grid-rate panels but leaves this normalized readout unchanged. A model using the unnormalized sum $z$ would behave differently. The browser reports both kinds of quantities so that display normalization cannot be mistaken for a biological gain mechanism.

**Why diversity and threshold matter.**

A single periodic grid retains repeated peaks after thresholding. Six identical grids averaged together give exactly the same normalized field. Inputs with different spacings and orientations can have a strong common peak while other peaks overlap less well; thresholding can isolate that common region **within a particular arena**. This does not guarantee a unique location over arbitrary space [[19]](#spatial-ref-19).

The presets deliberately align each grid's phase anchor at $(0.12,-0.08)$ m with fixed weights of 1. They are a designed coincidence example. No Gaussian place field or target-shaped image is inserted into the output. Different output neurons would need different connectivity, thresholds, or learned representations; copying the same weight row produces the same output.

(grid-place-live-example)=

### 4.3.6 Interactive grid-to-place experiment

Use **One grid only**, **Identical grids**, then **Diverse grids**. Select a grid before editing its parameters. Watch the selected input, pooled drive, place-like output, and numerical probe contributions. Click any map or use the probe sliders to inspect the same position across all inputs.

```{iframe} /Introduction-to-Neuromorphic-Embodied-AI/grid-place-interactive.html
:label: grid-place-playground
:class: grid-place-playground
:title: Interactive grid cell to place cell mapping
:width: 100%
```

[Open the interactive experiment in a full-width page](https://an-hongyu.github.io/Introduction-to-Neuromorphic-Embodied-AI/grid-place-interactive.html).

All maps cover a 2 m × 2 m arena. Input maps share a fixed 0–80 Hz color scale; the readout uses a fixed 0–25 Hz scale. Maps are sampled on a 121 × 121 grid (approximately 1.67 cm spacing), while probe values use the continuous formula. The “half-peak patches” metric counts four-connected regions above half the sampled output maximum. It is a numerical diagnostic, not an experimental count of biological place fields. Border truncation and sampling resolution affect it.

At the default settings and resolution, the diverse preset has one half-peak patch; the single/identical presets have repeated patches. These are regression examples for this arena, not a universal result about all parameter choices. A sufficiently high threshold, zero weights, or suppressed inputs can produce no output.

(place-model-notebooks)=

### 4.3.7 Editable Python experiments

[Laboratory 2](../notebooks/place_cells.ipynb) implements the Gaussian rate field, a reproducible trajectory, Poisson spike counts, and occupancy-normalized maps. [Run it in Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/place_cells.ipynb), or {download}`download the Place Cell notebook <../notebooks/place_cells.ipynb>`. The [laboratory guide](04-place-cells.md) supplies the execution sequence and parameter-change tasks, rather than a second copy of the model derivation.

[Laboratory 8](../notebooks/grid_to_place.ipynb) provides the full equations and parameter dictionaries, two executed figures, and geometry checks. [Run it in Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/grid_to_place.ipynb), or {download}`download the notebook <../notebooks/grid_to_place.ipynb>`.

```python
# Run the definitions in Laboratory 8 first.
cells = make_cells()
cells[0]['spacing'] = 0.76
cells[0]['orientation'] = 30
rates, drive, place = grid_to_place(X, Y, cells, count=6, threshold=0.78)
```

Compare current maps, rather than relying on the attractiveness of a hexagonal image. Check the distance between adjacent peaks, repeat after a 60° rotation, halve the spatial sampling interval, and compare the output outside the preferred region as well as at the largest peak.

(learned-place-models)=

### 4.3.8 From a fixed readout to learned place fields

This experiment evaluates a fixed feedforward function of supplied position. A learned mapping additionally needs an input trajectory, an output/competition mechanism, an explicit update rule, and held-out evaluation. A dimensionless discrete Oja example is $\Delta w_j=\eta y(x_j-yw_j)$; [Chapter 3](04-hebbian-learning.md) explains its stabilization and its difference from STDP. Choosing a rule does not demonstrate that a stable place field will emerge.

Evaluate stability across independent exploration trajectories, remote responses, field position/width, cue changes, and frozen-weight recall. Avoid selecting a desired center and then presenting that imposed center as unsupervised discovery. Similarly, grid-to-place mapping is not synonymous with CA3-to-CA1 mapping: canonical grid activity is associated with entorhinal circuits, while multiple hippocampal regions can contain place-related responses. Biological spatial representations involve interacting pathways and sensory signals [[19]](#spatial-ref-19).

(grid-cell-models)=

## 4.4 Grid cells and their models

### 4.4.1 The hexagonal firing pattern

Hafting and colleagues described MEC neurons with multiple firing fields arranged in an approximately triangular lattice, giving a hexagonal pattern of neighbors around a field [[7]](#spatial-ref-7). Three properties characterize an idealized grid: **spacing** is the distance between neighboring peaks, **orientation** is the lattice rotation, and **phase** is its translation in space. Spatial phase here is not the phase of a theta oscillation.

A grid pattern is normally visible only after combining activity over a trajectory. An animal does not activate every field of one cell simultaneously. Nor does a repeated pattern uniquely determine absolute position: several locations share a similar phase within a single grid. Different phases, spatial scales, and additional cues can help distinguish them.

```{figure} ../assets/spatial-literature/grid-fields.jpg
:label: fig-spatial-grid-recordings
:alt: Published grid-cell rate maps in light and darkness, together with spatial periodicity, information, and stability analyses
:width: 100%

**Grid patterns are regular but depend on experimental conditions.** Begin with panel A: repeated hotspots are clearer in the illuminated trials than in the dark trials of this experiment. Other panels quantify periodicity, information, and stability. This does not imply that every grid cell immediately loses all spatial information in every dark environment. Reproduced from Pérez-Escobar et al., Fig. 2 [[8]](#spatial-ref-8), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and format-converted only.
```

A spatial autocorrelogram asks how well a map resembles a shifted copy of itself. An ideal grid produces six surrounding peaks. **Gridness** compares rotational symmetry, but a sixfold-looking plot alone is insufficient: field sampling, occupancy, smoothing, arena shape, and shuffled controls matter. Spatial autocorrelation is not the same as spike-time autocorrelation.

(grid-model-sources)=

### 4.4.2 Source models and parameter conventions

Liu, Bai, and An's 2025 paper parameterizes a grid cell by spacing, orientation, and two phases, and describes a thresholded sum for the grid-to-place interaction [[20]](#spatial-ref-20). Its Figure 2 varies scale, angle, $\kappa$, and $\zeta$. The available 2026 author manuscript gives a rectified cosine-interference equation explicitly [[21]](#spatial-ref-21). These sources motivate the experiment below; the normalization, fixed weights, physical units, and threshold used here are specified teaching choices.

| Source | Reported expression or convention | What needs to be explicit in executable teaching code |
|---|---|---|
| 2025, sec. 2.1.1, eq. (1) [[20]](#spatial-ref-20) | $G_j=[s_j,\theta_j,\phi_j^1,\phi_j^2]$; $s_j$ is called spacing | Units and the conversion from physical distance to periodic phase |
| 2025, eq. (3) | $\sigma=\tan^{-1}\!\left[\kappa(d_i/s_j-\zeta)\right]$ | The periodic definition of $d_i$ and a nonnegative, unit-bearing rate conversion; the arctangent alone is not a complete hexagonal rate map |
| 2025, sec. 2.1.2, eq. (7) | $P_c(t)=\Theta\!\left(\sum_{i=1}^N G_{C_i}(t)\right)$ | The threshold inside $\Theta$, input scaling, connectivity, and whether outputs are events, binary states, or rates |
| 2026 author manuscript, sec. III-D, eq. (8) [[21]](#spatial-ref-21) | $g_i(x,y)=\max\{0,\kappa[\cos(s_i d_1)+\cos(s_i d_2)+\cos(s_i d_3)]+b\}$ | Here $s_i$ controls **spatial frequency**; $d_m$ are projections along three axes separated by 60° |

The same letter $s$ therefore must not silently mean both a distance and its inverse. We use **$\lambda$ for nearest-neighbor grid spacing in metres**, and **$k$ for angular spatial frequency in rad/m**. The 2026 equation was checked against the available author manuscript; the linked DOI identifies the published article. The interactive example is an explicit extension of this model family, not a reproduction of every parameter or robot experiment in either paper.

The 2025 arctangent expression uses $\zeta$ inside its argument. For the cosine example below, we use $\zeta$ as the additive $b$ term. These operations differ. Statements about parameter effects must refer to the actual equation being run.

(grid-cosine-model)=

### 4.4.3 Complete hexagonal grid formula

Let $\mathbf r=(x,y)^\top$ be position and $\mathbf p_j=(p_{x,j},p_{y,j})^\top$ be a spatial translation, both in metres. Define three unit wave vectors,

$$
\mathbf e_{jm}=\begin{bmatrix}
\cos(\theta_j+\pi/6+m\pi/3)\\
\sin(\theta_j+\pi/6+m\pi/3)
\end{bmatrix},\quad m\in\{0,1,2\},\qquad
k_j=\frac{4\pi}{\sqrt3\lambda_j}.
$$

Then define a nonnegative grid-rate proxy,

$$
g_j(\mathbf r)=r_G\left[\kappa_j\sum_{m=0}^{2}
\cos\!\left(k_j\mathbf e_{jm}^{\top}(\mathbf r-\mathbf p_j)\right)
+\zeta_j\right]_+.
$$

Here $[a]_+=\max(0,a)$ and $r_G=20\ \mathrm{Hz}$. The 20 Hz multiplier is a declared teaching scale. $\kappa\geq0$ and $\zeta$ are dimensionless here. This is a spatial tuning function; it does not integrate velocity, generate action potentials, or learn a map from sensory measurements.

(grid-spacing-geometry)=

### 4.4.4 Spacing and orientation

At $\theta=0$, moving from a peak by $(\lambda,0)$ changes the three cosine arguments by $(2\pi,0,-2\pi)$. Moving by $(\lambda/2,\sqrt3\lambda/2)$ changes them by $(2\pi,2\pi,0)$. Thus both translation vectors reproduce the field, have length $\lambda$, and meet at 60°: they generate a triangular lattice of firing peaks.

The wave-vector directions are offset by 30° so that **$\theta$ labels a real-space nearest-neighbor lattice axis**. Without this declaration, a figure's lattice angle and a cosine wave-vector angle can differ by 30°. Rotating the ideal field by 60° leaves it unchanged. Convert slider degrees to radians before evaluating trigonometric functions.

(grid-phase-model)=

### 4.4.5 Phase as a spatial translation

The equivalent wave phases are $\varphi_{jm}=k_j\mathbf e_{jm}^{\top}\mathbf p_j$, giving cosine arguments $k_j\mathbf e_{jm}^{\top}\mathbf r-\varphi_{jm}$. Only two are independent: with the axes above, $\varphi_{j2}=\varphi_{j1}-\varphi_{j0}$ modulo $2\pi$. Three unconstrained phase sliders need not preserve the same translated peak lattice.

The browser therefore exposes two physical translations, $p_x$ and $p_y$, in metres. Translating all inputs together translates their shared readout; translating only one input generally disrupts the shared maximum.

(grid-model-parameters)=

### 4.4.6 What each parameter changes

| Parameter | Change one variable | Predicted effect in this equation |
|---|---|---|
| $\lambda$ (m) | Double spacing | Nearest peaks move twice as far apart; $k$ halves |
| $k$ (rad/m) | Double angular frequency | Spacing halves, since $\lambda=4\pi/(\sqrt3 k)$ |
| $\theta$ (rad; slider in degrees) | Add 15° | Rotate the lattice around its phase anchor; spacing is preserved |
| $p_x,p_y$ (m) | Shift one coordinate | Translate firing peaks; do not change lattice spacing |
| $\kappa$ | Increase gain with $\zeta=0$ | Increase raw rates; peak locations and the rectified support stay fixed |
| $\zeta$ | Increase the additive offset at fixed gain | Raise the pre-rectification activity and expand the positive-response regions; peak spacing stays fixed |
| Readout threshold $\tau$ | Increase threshold | Narrow or remove output regions; no guarantee of exactly one region |
| Connection weights $w_j$ | Reduce one input's weight | Reduce that input's contribution to the pooled drive |

“Grid size” can mean **distance between firing fields** or **width of each individual firing field**. They are different measurements. Spacing controls the former. Offset, gain/offset ratio, and the chosen activity threshold affect the latter. For example, at $\zeta=0$, scaling $\kappa$ alone multiplies rates without changing the region where the raw field is positive. A fixed *absolute* firing-rate cutoff can still change the measured field width.

**Worked example.** With $\lambda=0.38$ m, $k\approx19.09$ rad/m. At $\mathbf r=\mathbf p$, $\kappa=0.5$, and $\zeta=0$, all cosines equal 1 and $g=30$ Hz. At $\theta=0$, another 30 Hz peak occurs at $\mathbf p+(0.38,0)$ m. Doubling spacing moves that neighbor to $\mathbf p+(0.76,0)$ m; it does not double the central rate.

(grid-path-integration)=

### 4.4.7 From a tuning field to path integration

A **path-integration model** must instead update internal state using self-motion over time. Continuous-attractor grid models are one explicit approach [[9]](#spatial-ref-9). Noise can accumulate, so landmark corrections and boundary information become important. The mathematical ability to integrate velocity is distinct from evidence that a particular biological population implements one proposed algorithm.

The [place-cell readout in Section 4.3.5](#grid-place-readout) combines these grid inputs. Use the [interactive experiment in Section 4.3.6](#grid-place-live-example) to test the parameter predictions here, then reproduce the calculations in [Laboratory 8](../notebooks/grid_to_place.ipynb).

(head-direction-models)=

## 4.5 Head-direction cells and their models

### 4.5.1 Heading is not position or movement direction

Head-direction cells fire preferentially when the animal faces a particular direction relative to an environmental reference. Classical recordings characterized this tuning in the rat postsubiculum, also called the dorsal presubiculum [[10]](#spatial-ref-10). Directional signals also occur in a wider network, including thalamic and parahippocampal regions; they are not confined to the hippocampus.

A cell can retain a preferred heading while the animal occupies different locations. Conversely, an animal at one location can face many directions. Head orientation must also be separated from travel direction: a rat can move backward or turn its head independently of its trajectory.

```{figure} ../assets/spatial-literature/head-direction.jpg
:label: fig-spatial-head-direction
:alt: Anatomically identified presubicular neurons with head-angle traces, spike locations, and polar head-direction tuning curves
:width: 100%

**Directional tuning and identified neurons.** Compare the spike marks on the heading traces with the polar curves: high firing is concentrated around a preferred angle. Panels C/G summarize tuning; D/H compare recording halves. These recordings used passive rotation of awake rats, so the figure is not a free-navigation trajectory experiment. Reproduced from Preston-Ferrer et al., Fig. 3 [[11]](#spatial-ref-11), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and format-converted only.
```

### 4.5.2 Circular tuning model and robot coordinates

A smooth circular approximation is

$$
r_i(\theta)=r_0+A_i\exp\!\left[\kappa_i\bigl(\cos(\theta-\theta_i)-1\bigr)\right].
$$

$\theta$ and preferred angle $\theta_i$ are in radians, $A_i$ is the peak increment in Hz, and $\kappa_i\geq0$ controls concentration. The maximum is $r_0+A_i$. Angular differences must wrap around: $359^\circ$ is only $2^\circ$ from $1^\circ$, not $358^\circ$ away. A polar curve plots angle around the circle and activity along the radius; it is **not a map of where spikes occurred**.

For a robot, define body yaw, camera/LiDAR mounting angle, and velocity direction separately. A ring-attractor implementation adds recurrent dynamics that maintain and update an angular population state; the tuning curve alone does not create that memory.

(border-cell-models)=

## 4.6 Border cells and their models

### 4.6.1 Firing near environmental limits

Entorhinal **border cells** show activity concentrated near particular environmental boundaries [[12]](#spatial-ref-12). A cell may respond along one side of an enclosure rather than near every wall. Boundaries can be physical walls or other limits, depending on the task and preparation.

Related **boundary-vector cells** were reported in the subiculum [[13]](#spatial-ref-13). Boundary-vector accounts describe sensitivity to a boundary at a preferred distance and allocentric direction. These concepts overlap, but “border cell,” “boundary-vector cell,” and “nearest-obstacle sensor” are not interchangeable labels.

```{figure} ../assets/spatial-literature/border-fields.jpg
:label: fig-spatial-border-recordings
:alt: Five recorded border-cell spatial maps compared between illuminated and dark trials, with summary measures of boundary confinement and polarity
:width: 100%

**Boundary-related firing in recorded neurons.** In panel A, identify the active arc near the arena perimeter and compare light/dark conditions for the same cell. The plots quantify how strongly firing remains boundary-associated. Reproduced from Pérez-Escobar et al., Fig. 5 [[8]](#spatial-ref-8), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and format-converted only.
```

### 4.6.2 Boundary-distance model and coordinate transformations

For an arena with a selected wall $w$, a simple near-wall rate is

$$
r_w(\mathbf{x})=r_0+A\exp[-d_w(\mathbf{x})^2/(2\sigma_b^2)].
$$

$d_w$ is distance to that wall and $\sigma_b$ is a distance scale, both in meters. This produces a band near one chosen boundary. Replacing $d_w$ by distance to the nearest wall changes the represented variable and makes the cell respond around the whole enclosure. Neither construction is a complete boundary-vector model.

For a two-dimensional robot, a beam of range $d$ and bearing $\alpha$ gives a sensor-frame endpoint $[d\cos\alpha,d\sin\alpha]^\top$. To express it in a world frame, use calibrated mounting and timestamped pose transforms. A 36-sector LiDAR encoder is therefore **egocentric sensory input**; an allocentric boundary representation requires additional computation. Test boundary sensitivity by changing enclosure geometry while controlling occupancy, orientation, and sensory visibility.

## 4.7 Speed cells, time cells, and their models

(speed-cell-models)=

### 4.7.1 Speed cells: activity, model, and self-motion updating

**Speed cells** show systematic modulation of activity with running speed. Kropff and colleagues characterized a population of speed-modulated neurons in MEC [[14]](#spatial-ref-14). A speed signal can supply the magnitude needed for self-motion updating, but a firing-rate correlation is not by itself proof that the neuron causally integrates distance.

Linear speed $v=\|\dot{\mathbf{x}}\|$ is nonnegative and has units such as m/s. Angular velocity $\omega=\dot\theta$ has units such as rad/s and can distinguish clockwise from counterclockwise motion. These are separate quantities. Recordings across MEC, presubiculum, and parasubiculum reveal linear and angular speed modulation, including mixed selectivity [[15]](#spatial-ref-15).

```{figure} ../assets/spatial-literature/speed-cells.jpg
:label: fig-spatial-speed-recordings
:alt: Published linear-speed coding figure with speed schematics, rate-versus-speed tuning, shuffled controls, and firing-rate and running-speed time courses
:width: 100%

**Reading a speed code.** The tuning curves relate firing rate to linear speed; the time-series comparison shows whether activity covaries with movement over a session. Shuffled distributions help assess whether the association exceeds chance. A speed curve is neither a place field nor a head-direction polar plot. Reproduced from Spalla, Treves, and Boccara, Fig. 2 [[15]](#spatial-ref-15), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and format-converted only.
```

An elementary rate approximation is $r(v)=[b+kv]_+$. With $v$ in m/s, $b$ is in Hz and $k$ in Hz/(m/s). For the teaching values $b=3$ Hz and $k=40$ Hz/(m/s), $v=0.25$ m/s gives 13 Hz. This linear response is an assumption over a chosen range, not a law obeyed by all speed-sensitive neurons.

To test speed coding, compare different speeds at matched locations and headings. Control for occupancy, acceleration, reward approach, and behavioral state, and evaluate on held-out runs. In a model, velocity integration can use

$$
\widehat{\mathbf{x}}_{n+1}=\widehat{\mathbf{x}}_n+
\widehat v_n\Delta t
\begin{bmatrix}\cos\widehat\psi_n\\\sin\widehat\psi_n\end{bmatrix},
$$

where $\psi$ is **travel direction**, not necessarily head direction. For a nonholonomic robot moving forward, body yaw may approximate it; that relationship must be stated rather than silently assumed.

(time-cell-models)=

### 4.7.2 Time cells: temporal fields and their model

**Time cells** show activity concentrated around particular moments relative to a defined event or task interval. MacDonald and colleagues demonstrated hippocampal temporal sequences that bridge separated events [[16]](#spatial-ref-16); internally generated hippocampal sequences during a delay also motivated this research [[17]](#spatial-ref-17). These responses help describe temporal organization, but are not evidence for a neuron reading an absolute wall clock.

The reference event matters. The same number of seconds after entering a maze, receiving a cue, or starting a treadmill are different variables. Position, traveled distance, speed, and task expectation may covary with elapsed time. A sequence of peak times is therefore not enough to identify pure time coding.

```{figure} ../assets/spatial-literature/time-distance-cells.jpg
:label: fig-spatial-time-recordings
:alt: Published examples comparing time-coding and distance-coding hippocampal neurons across different treadmill velocities and analysis coordinates
:width: 100%

**Distinguishing elapsed time from traveled distance.** Compare the first two example columns with the next two, then inspect whether response timing or traveled distance remains more consistent when speed changes. These are experimental-data analyses, not a synthetic sequence of Gaussian fields. Reproduced from Abramson et al., Fig. 2 [[18]](#spatial-ref-18), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); resized and format-converted only. The separately restricted apparatus panel in that paper's Fig. 1 is not reproduced.
```

A teaching temporal field can be written

$$
r_i(\tau)=r_0+A_i\exp[-(\tau-\tau_i)^2/(2\sigma_{t,i}^2)],
\qquad \tau=t-t_{\mathrm{event}}.
$$

$\tau_i$ and $\sigma_{t,i}$ are preferred elapsed time and temporal width in seconds. This is an imposed timing profile, not a learned sequence or a complete time-cell mechanism. To display a population sequence, sort cells by peak time using training trials, and test that ordering on separate trials; sorting the same noisy data used for display can manufacture an apparent sequence.

A practical control varies treadmill speed. Under idealized time coding, a cell fires near the same elapsed time; under idealized distance coding, its response time changes approximately as $d/v$. Actual neurons can mix both variables, and task requirements affect their expression [[18]](#spatial-ref-18). Time cells belong in this chapter because spatial experience unfolds in time, not because temporal selectivity is itself spatial tuning.

(spatial-tuning-estimation)=

## 4.8 Estimating and comparing neural tuning

### 4.8.1 Correct for occupancy before interpreting a map

For spatial bin $b$, let $K_b$ be its spike count and $T_b$ its occupancy time. Then

$$
\widehat r_b=K_b/T_b,\qquad T_b>0.
$$

Twenty spikes during 2 s give 10 Hz; ten spikes during 0.5 s give 20 Hz. Raw counts would rank these locations in the opposite order. An unvisited bin is **unknown**, not biologically silent. The same principle applies to angle bins and speed bins: normalize by the time for which the corresponding state was sampled.

Synchronize behavior and neural recordings; report bin sizes, smoothing, and minimum occupancy; inspect raw data alongside processed maps. Preserve track geometry and masks instead of smoothing across walls or unvisited gaps. For a decoder, use independent trials, sessions, or temporally separated blocks rather than treating adjacent samples as independent tests.

### 4.8.2 Different plots answer different questions

| Response class | Horizontal or spatial variable | Characteristic visualization | Important control |
|---|---|---|---|
| Place | Position $\mathbf{x}$ | Trajectory/events and occupancy-normalized map | Location sampling and contextual remapping |
| Grid | Position $\mathbf{x}$ | Repeated fields and spatial autocorrelation | Arena geometry, sampling, shuffled grid scores |
| Head direction | Heading $\theta$ | Circular or polar rate curve | Directional occupancy and cue rotation |
| Border | Boundary geometry | Boundary-associated firing map | Move or insert boundaries; separate heading effects |
| Speed | Linear speed $v$ or angular velocity $\omega$ | Rate–speed relation and temporal covariation | Position, heading, behavioral-state covariates |
| Time | Elapsed time $\tau$ | Trial rasters, temporal tuning, ordered population activity | Speed, distance, event identity, held-out ordering |

The following compact comparison uses synthetic functions, unlike the published experimental figures above.

```{figure} ../assets/spatial-cell-tuning.png
:label: fig-spatial-tuning
:alt: Six synthetic teaching panels illustrating place, grid, heading, boundary, speed, and elapsed-time tuning
:width: 100%

**Idealized response signatures for comparison.** These are generated teaching curves, not neural recordings and not evidence that a circuit learned the representations. Interpret the axes separately: meters for space, degrees for orientation, Hz for rate, and seconds for elapsed time.
```

## 4.9 From distributed representations to embodied AI

### 4.9.1 Different signals describe the same experience

Consider a robot at $(0.5,0.4)$ m, facing north near an eastern wall, initially stationary. Place-like activity can specify location, head-direction-like activity orientation, and boundary-related activity environmental geometry. Speed-dependent activity can change when it starts moving, whereas a temporal sequence may track time since a cue even before movement begins. No single population needs to carry the entire state.

This is a useful engineering decomposition, **not a settled biological wiring diagram**. The hippocampal–entorhinal network has parallel pathways, recurrent interactions, and mixed selectivity. Grid-to-place conversion is one family of models, not an established universal one-way transformation; the literature also examines contributions in the reverse direction and from non-grid inputs [[19]](#spatial-ref-19).

For a biologically inspired robot, keep three levels distinct: measured inputs such as LiDAR and odometry; estimated internal variables such as pose or event-relative time; and neural dynamics that encode, retain, or learn from those variables. A tuning function evaluated at the true simulator pose bypasses the estimation problem. A place representation also does not itself specify an action: navigation requires a policy or readout, a goal definition, and an experimentally testable learning mechanism.

### 4.9.2 Laboratories and a research bridge

Continue with the [Place Cell laboratory guide](04-place-cells.md) and [Place Cell notebook](../notebooks/place_cells.ipynb), which use a one-meter-square arena, a 300 s synthetic trajectory, and Poisson spike counts. They measure occupancy coverage and error relative to an imposed field. Then use the [Grid-to-Place laboratory](../notebooks/grid_to_place.ipynb) to explore combinations of periodic inputs.

Liu, Bai, and An provide a published example linking spatial-cell-inspired modeling to associative learning in an open-field neuromorphic robot [[20]](#spatial-ref-20). It is an engineering case study rather than proof that its modeled units are biologically identical to the cell classes reviewed here. Keep learning, frozen post-learning evaluation, and sensory-control conditions separate.

## Additional Reading Materials

For the computational models, read Liu et al. [[20]](#spatial-ref-20), secs. 2.1.1-2.1.2, eqs. (1)-(7), and Fig. 2, alongside the explicit conventions in Section 4.4.2. Compare the 2026 cosine formulation [[21]](#spatial-ref-21), sec. III-D, eq. (8), before transferring parameters between versions. The browser and notebook are specified teaching models, not reproductions of the complete published robot.

For biological context, read *Principles of Neural Science* [[1]](#spatial-ref-1) alongside the hippocampal anatomy and memory discussion in *Computational Cognitive Neuroscience* [[2]](#spatial-ref-2). O'Keefe and Nadel's *The Hippocampus as a Cognitive Map* [[3]](#spatial-ref-3) provides the historical theoretical foundation; the authors have made a readable copy available through UCL.

For primary discoveries, begin with place cells [[4]](#spatial-ref-4), grid cells [[7]](#spatial-ref-7), head-direction cells [[10]](#spatial-ref-10), border cells [[12]](#spatial-ref-12), speed cells [[14]](#spatial-ref-14), and time cells [[16]](#spatial-ref-16). Use the illustrated studies in this chapter to connect those definitions to real experimental measurements. The [grid-to-place model in Section 4.3.5](#grid-place-readout) and [Chapter 8 LiDAR encoder](08-lidar-encoding.md) supply the computational bridge.

(spatial-exercises)=

## 4.10 Exercises

1. Explain why one grid cell cannot uniquely identify position across a large environment.
2. Give a situation in which head orientation and travel direction differ.
3. Calculate rates for bins with $(K_b,T_b)=(12,0.6\,\mathrm{s})$ and $(30,3\,\mathrm{s})$.
4. Design a control that helps distinguish speed-related firing from firing caused by repeated visits to one location.
5. Explain why an imposed Gaussian place field and a learned place field require different evidence.
6. List the transformations needed to convert a body-relative LiDAR observation into an environment-relative boundary measurement.
7. Trace the hippocampal trisynaptic pathway and name a route that bypasses DG or CA3. Why is a strictly feedforward grid-to-place diagram incomplete?
8. An ideal time cell fires 3 s after treadmill onset. An ideal distance cell fires after 0.6 m of travel. Predict their firing times at 0.2 and 0.3 m/s, and explain how the test separates the hypotheses.
9. What additional interpretation is required when a place-field map comes from calcium imaging rather than extracellular spike recordings? Why is a normalized color scale not an absolute firing-rate scale?
10. Explain how to assess temporal sequence reliability without sorting and evaluating the same trials. State what such reliability would and would not demonstrate.

11. Show that the two lattice vectors in Section 4.4.4 preserve all three cosine values.
12. Explain why six identical inputs cannot remove periodic aliases under the normalized readout.
13. Double $\kappa$ with zero offset. Compare raw grid rate, normalized input, and output.
14. Shift just one input phase, then shift all phases by the same translation. Explain the difference.
15. Lower $\tau$ and count secondary patches. Repeat with a larger arena and finer sampling.
16. Design a learning experiment that distinguishes an imposed shared phase anchor from an emergent place field.

See the [worked solutions at the end of the book](solutions-foundations.md#spatial-solutions).

## References

(spatial-ref-1)=

[1] Eric R. Kandel, James H. Schwartz, Thomas M. Jessell, Steven A. Siegelbaum, and Albert James Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(spatial-ref-2)=

[2] Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 5th ed., 2024, ch. 7. [Open textbook chapter](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/chapter-07.md); [edition and license](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/frontmatter.md).

(spatial-ref-3)=

[3] John O'Keefe and Lynn Nadel, *The Hippocampus as a Cognitive Map*. Oxford, U.K.: Clarendon Press, 1978. [Author-authorized full text and bibliographic record](https://discovery.ucl.ac.uk/id/eprint/10103569/).

(spatial-ref-4)=

[4] John O'Keefe and Jonathan O. Dostrovsky, “The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat,” *Brain Research*, vol. 34, no. 1, pp. 171–175, 1971, doi: [10.1016/0006-8993(71)90358-1](https://doi.org/10.1016/0006-8993(71)90358-1).

(spatial-ref-5)=

[5] Robert U. Muller and John L. Kubie, “The effects of changes in the environment on the spatial firing of hippocampal complex-spike cells,” *The Journal of Neuroscience*, vol. 7, no. 7, pp. 1951–1968, 1987, doi: [10.1523/JNEUROSCI.07-07-01951.1987](https://doi.org/10.1523/JNEUROSCI.07-07-01951.1987).

(spatial-ref-6)=

[6] Mary Ann Go, Jake Rogers, Giuseppe P. Gava, Catherine E. Davey, Seigfred Prado, Yu Liu, and Simon R. Schultz, “Place cells in head-fixed mice navigating a floating real-world environment,” *Frontiers in Cellular Neuroscience*, vol. 15, Art. 618658, 2021, doi: [10.3389/fncel.2021.618658](https://doi.org/10.3389/fncel.2021.618658).

(spatial-ref-7)=

[7] Torkel Hafting, Marianne Fyhn, Sturla Molden, May-Britt Moser, and Edvard I. Moser, “Microstructure of a spatial map in the entorhinal cortex,” *Nature*, vol. 436, pp. 801–806, 2005, doi: [10.1038/nature03721](https://doi.org/10.1038/nature03721).

(spatial-ref-8)=

[8] José Antonio Pérez-Escobar, Olga Kornienko, Patrick Latuske, Laura Kohler, and Kevin Allen, “Visual landmarks sharpen grid cell metric and confer context specificity to neurons of the medial entorhinal cortex,” *eLife*, vol. 5, Art. e16937, 2016, doi: [10.7554/eLife.16937](https://doi.org/10.7554/eLife.16937).

(spatial-ref-9)=

[9] Yoram Burak and Ila R. Fiete, “Accurate path integration in continuous attractor network models of grid cells,” *PLOS Computational Biology*, vol. 5, no. 2, Art. e1000291, 2009, doi: [10.1371/journal.pcbi.1000291](https://doi.org/10.1371/journal.pcbi.1000291).

(spatial-ref-10)=

[10] Jeffrey S. Taube, Robert U. Muller, and James B. Ranck, Jr., “Head-direction cells recorded from the postsubiculum in freely moving rats. I. Description and quantitative analysis,” *The Journal of Neuroscience*, vol. 10, no. 2, pp. 420–435, 1990, doi: [10.1523/JNEUROSCI.10-02-00420.1990](https://doi.org/10.1523/JNEUROSCI.10-02-00420.1990).

(spatial-ref-11)=

[11] Patricia Preston-Ferrer, Stefano Coletta, Markus Frey, and Andrea Burgalossi, “Anatomical organization of presubicular head-direction circuits,” *eLife*, vol. 5, Art. e14592, 2016, doi: [10.7554/eLife.14592](https://doi.org/10.7554/eLife.14592).

(spatial-ref-12)=

[12] Trygve Solstad, Charlotte N. Boccara, Emilio Kropff, May-Britt Moser, and Edvard I. Moser, “Representation of geometric borders in the entorhinal cortex,” *Science*, vol. 322, no. 5909, pp. 1865–1868, 2008, doi: [10.1126/science.1166466](https://doi.org/10.1126/science.1166466).

(spatial-ref-13)=

[13] Colin Lever, Stephen Burton, Ali Jeewajee, John O'Keefe, and Neil Burgess, “Boundary vector cells in the subiculum of the hippocampal formation,” *The Journal of Neuroscience*, vol. 29, no. 31, pp. 9771–9777, 2009, doi: [10.1523/JNEUROSCI.1319-09.2009](https://doi.org/10.1523/JNEUROSCI.1319-09.2009).

(spatial-ref-14)=

[14] Emilio Kropff, James E. Carmichael, May-Britt Moser, and Edvard I. Moser, “Speed cells in the medial entorhinal cortex,” *Nature*, vol. 523, pp. 419–424, 2015, doi: [10.1038/nature14622](https://doi.org/10.1038/nature14622).

(spatial-ref-15)=

[15] Davide Spalla, Alessandro Treves, and Charlotte N. Boccara, “Angular and linear speed cells in the parahippocampal circuits,” *Nature Communications*, vol. 13, Art. 1907, 2022, doi: [10.1038/s41467-022-29583-z](https://doi.org/10.1038/s41467-022-29583-z).

(spatial-ref-16)=

[16] Christopher J. MacDonald, Kyle Q. Lepage, Uri T. Eden, and Howard Eichenbaum, “Hippocampal ‘time cells’ bridge the gap in memory for discontiguous events,” *Neuron*, vol. 71, no. 4, pp. 737–749, 2011, doi: [10.1016/j.neuron.2011.07.012](https://doi.org/10.1016/j.neuron.2011.07.012).

(spatial-ref-17)=

[17] Eva Pastalkova, Vladimir Itskov, Asohan Amarasingham, and György Buzsáki, “Internally generated cell assembly sequences in the rat hippocampus,” *Science*, vol. 321, no. 5894, pp. 1322–1327, 2008, doi: [10.1126/science.1159775](https://doi.org/10.1126/science.1159775).

(spatial-ref-18)=

[18] Shai Abramson, Benjamin J. Kraus, John A. White, Michael E. Hasselmo, Dori Derdikman, and Genela Morris, “Flexible coding of time or distance in hippocampal cells,” *eLife*, vol. 12, Art. e83930, 2023, doi: [10.7554/eLife.83930](https://doi.org/10.7554/eLife.83930).

(spatial-ref-19)=

[19] Daniel Bush, Caswell Barry, and Neil Burgess, “What do grid cells contribute to place cell firing?,” *Trends in Neurosciences*, vol. 37, no. 3, pp. 136–145, 2014, doi: [10.1016/j.tins.2013.12.003](https://doi.org/10.1016/j.tins.2013.12.003).

(spatial-ref-20)=

[20] Tianze Liu, Kang Jun Bai, and Hongyu An, “Replicating associative learning of rodents with a neuromorphic robot in an open-field arena,” *Frontiers in Neuroscience*, vol. 19, Art. 1565780, 2025, doi: [10.3389/fnins.2025.1565780](https://doi.org/10.3389/fnins.2025.1565780).

(spatial-ref-21)=

[21] Tianze Liu, Zihan Jin, Dong Song, and Hongyu An, “A Neuromorphic Robot as a Digital Twin for Rodent Spatial Representation in Dynamic Environment Navigation,” *IEEE Journal on Emerging and Selected Topics in Circuits and Systems*, 2026, doi: [10.1109/JETCAS.2026.3733540](https://doi.org/10.1109/JETCAS.2026.3733540).

(spatial-ref-22)=

[22] Wulfram Gerstner, Werner M. Kistler, Richard Naud, and Liam Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014, ch. 7. [Online textbook](https://neuronaldynamics.epfl.ch/online/Ch7.html).
