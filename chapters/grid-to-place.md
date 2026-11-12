---
title: Grid Cells and Grid-to-Place Mapping
---

# Grid Cells and Grid-to-Place Mapping

## Learning objectives

By the end of this section, you should be able to:

- Implement a periodic hexagonal grid-cell firing field.
- Distinguish lattice spacing from spatial frequency.
- Predict how grid orientation and phase affect a firing pattern.
- Construct an explicit grid-to-place readout.
- Explain why summing periodic inputs does not automatically yield a single learned place field. Read [Chapter 3](02-spatial-cells.md) first; this section supplies its mathematical and interactive companion.

## 1. Read the source models before choosing parameters

Liu, Bai, and An's 2025 paper parameterizes a grid cell by spacing, orientation, and two phases, and describes a thresholded sum for the grid-to-place interaction [[1]](#grid-ref-1). Its Figure 2 varies scale, angle, $\kappa$, and $\zeta$. The available 2026 author manuscript gives a rectified cosine-interference equation explicitly [[2]](#grid-ref-2). These sources motivate the experiment below; the normalization, fixed weights, physical units, and threshold used here are specified teaching choices.

| Source | Reported expression or convention | What needs to be explicit in executable teaching code |
|---|---|---|
| 2025, sec. 2.1.1, eq. (1) [[1]](#grid-ref-1) | $G_j=[s_j,\theta_j,\phi_j^1,\phi_j^2]$; $s_j$ is called spacing | Units and the conversion from physical distance to periodic phase |
| 2025, eq. (3) | $\sigma=\tan^{-1}\!\left[\kappa(d_i/s_j-\zeta)\right]$ | The periodic definition of $d_i$ and a nonnegative, unit-bearing rate conversion; the arctangent alone is not a complete hexagonal rate map |
| 2025, sec. 2.1.2, eq. (7) | $P_c(t)=\Theta\!\left(\sum_{i=1}^N G_{C_i}(t)\right)$ | The threshold inside $\Theta$, input scaling, connectivity, and whether outputs are events, binary states, or rates |
| 2026 author manuscript, sec. III-D, eq. (8) [[2]](#grid-ref-2) | $g_i(x,y)=\max\{0,\kappa[\cos(s_i d_1)+\cos(s_i d_2)+\cos(s_i d_3)]+b\}$ | Here $s_i$ controls **spatial frequency**; $d_m$ are projections along three axes separated by 60° |

The same letter $s$ therefore must not silently mean both a distance and its inverse. We use **$\lambda$ for nearest-neighbor grid spacing in metres**, and **$k$ for angular spatial frequency in rad/m**. The 2026 equation was checked against the available author manuscript; the linked DOI identifies the published article. The interactive example is an explicit extension of this model family, not a reproduction of every parameter or robot experiment in either paper.

The 2025 arctangent expression uses $\zeta$ inside its argument. For the cosine example below, we use $\zeta$ as the additive $b$ term. These operations differ. Statements about parameter effects must refer to the actual equation being run.

## 2. A complete hexagonal grid formula

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

Here $[a]_+=\max(0,a)$ and $r_G=20\ \mathrm{Hz}$. The 20 Hz multiplier is a declared teaching scale. $\kappa$ and $\zeta$ are dimensionless here. This is a spatial tuning function; it does not integrate velocity, generate action potentials, or learn a map from sensory measurements.

### 2.1 Why this frequency gives the requested spacing

At $\theta=0$, moving from a peak by $(\lambda,0)$ changes the three cosine arguments by $(2\pi,0,-2\pi)$. Moving by $(\lambda/2,\sqrt3\lambda/2)$ changes them by $(2\pi,2\pi,0)$. Thus both translation vectors reproduce the field, have length $\lambda$, and meet at 60°: they generate a triangular lattice of firing peaks.

The wave-vector directions are offset by 30° so that **$\theta$ labels a real-space nearest-neighbor lattice axis**. Without this declaration, a figure's lattice angle and a cosine wave-vector angle can differ by 30°. Rotating the ideal field by 60° leaves it unchanged. Convert slider degrees to radians before evaluating trigonometric functions.

### 2.2 Phase is a translation, not a change in grid size

The equivalent wave phases are $\varphi_{jm}=k_j\mathbf e_{jm}^{\top}\mathbf p_j$, giving cosine arguments $k_j\mathbf e_{jm}^{\top}\mathbf r-\varphi_{jm}$. Only two are independent: with the axes above, $\varphi_{j2}=\varphi_{j1}-\varphi_{j0}$ modulo $2\pi$. Three unconstrained phase sliders need not preserve the same translated peak lattice.

The browser therefore exposes two physical translations, $p_x$ and $p_y$, in metres. Translating all inputs together translates their shared readout; translating only one input generally disrupts the shared maximum.

## 3. What each parameter changes

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

## 4. From multiple grid inputs to a place-like output

The paper's threshold-sum idea becomes executable only after scaling and threshold are specified. A general weighted construction is

$$
z_\ell(\mathbf r)=\sum_j w_{\ell j}g_j(\mathbf r),\qquad
b_\ell(\mathbf r)=\mathbf1[z_\ell(\mathbf r)>T_\ell].
$$

Here $g$ is in Hz, weights are dimensionless, $z$ and $T$ are in Hz, and $b$ is a binary state rather than a firing rate. A zero threshold applied to nonnegative inputs can activate broad parts of the arena. An unspecified step function does not establish localization.

### 4.1 The exact readout in the interactive experiment

For the single output shown below, normalize each input by its theoretical maximum,

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

### 4.2 Why diversity and threshold matter

A single periodic grid retains repeated peaks after thresholding. Six identical grids averaged together give exactly the same normalized field. Inputs with different spacings and orientations can have a strong common peak while other peaks overlap less well; thresholding can isolate that common region **within a particular arena**. This does not guarantee a unique location over arbitrary space [[3]](#grid-ref-3).

The presets deliberately align each grid's phase anchor at $(0.12,-0.08)$ m with fixed weights of 1. They are a designed coincidence example. No Gaussian place field or target-shaped image is inserted into the output. Different output neurons would need different connectivity, thresholds, or learned representations; copying the same weight row produces the same output.

## 5. Interactive experiment

(grid-place-live-example)=

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

## 6. Editable Python example

[Laboratory 8](../notebooks/grid_to_place.ipynb) provides the full equations and parameter dictionaries, two executed figures, and geometry checks. [Run it in Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/grid_to_place.ipynb), or {download}`download the notebook <../notebooks/grid_to_place.ipynb>`.

```python
# Run the definitions in Laboratory 8 first.
cells = make_cells()
cells[0]['spacing'] = 0.76
cells[0]['orientation'] = 30
rates, drive, place = grid_to_place(X, Y, cells, count=6, threshold=0.78)
```

Compare current maps, rather than relying on the attractiveness of a hexagonal image. Check the distance between adjacent peaks, repeat after a 60° rotation, halve the spatial sampling interval, and compare the output outside the preferred region as well as at the largest peak.

## 7. From a fixed readout to learned mapping

This experiment evaluates a fixed feedforward function of supplied position. A learned mapping additionally needs an input trajectory, an output/competition mechanism, an explicit update rule, and held-out evaluation. A dimensionless discrete Oja example is $\Delta w_j=\eta y(x_j-yw_j)$; [Chapter 4](04-hebbian-learning.md) explains its stabilization and its difference from STDP. Choosing a rule does not demonstrate that a stable place field will emerge.

Evaluate stability across independent exploration trajectories, remote responses, field position/width, cue changes, and frozen-weight recall. Avoid selecting a desired center and then presenting that imposed center as unsupervised discovery. Similarly, grid-to-place mapping is not synonymous with CA3-to-CA1 mapping: canonical grid activity is associated with entorhinal circuits, while multiple hippocampal regions can contain place-related responses. Biological spatial representations involve interacting pathways and sensory signals [[3]](#grid-ref-3).

## Exercises

1. Show that the two lattice vectors in Section 2.1 preserve all three cosine values.
2. Explain why six identical inputs cannot remove periodic aliases under the normalized readout.
3. Double $\kappa$ with zero offset. Compare raw grid rate, normalized input, and output.
4. Shift just one input phase, then shift all phases by the same translation. Explain the difference.
5. Lower $\tau$ and count secondary patches. Repeat with a larger arena and finer sampling.
6. Design a learning experiment that distinguishes an imposed shared phase anchor from an emergent place field.

## References

(grid-ref-1)=

[1] Tianze Liu, Kang Jun Bai, and Hongyu An, “Replicating associative learning of rodents with a neuromorphic robot in an open-field arena,” *Frontiers in Neuroscience*, vol. 19, Art. no. 1565780, 2025, doi: [10.3389/fnins.2025.1565780](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2025.1565780/full).

**Model provenance for [1].** Sections 2.1.1–2.1.2, eqs. (1)–(7), Fig. 2. Open access, CC BY; equations discussed with attribution.

(grid-ref-2)=

[2] Tianze Liu, Zihan Jin, Dong Song, and Hongyu An, “A Neuromorphic Robot as a Digital Twin for Rodent Spatial Representation in Dynamic Environment Navigation,” *IEEE Journal on Emerging and Selected Topics in Circuits and Systems*, 2026, doi: [10.1109/JETCAS.2026.3733540](https://doi.org/10.1109/JETCAS.2026.3733540).

**Model provenance for [2].** The cosine form was checked against the available author manuscript, sec. III-D, eq. (8); final publication metadata: [institutional record](https://digitalcommons.mtu.edu/michigantech-p2/3029/).

(grid-ref-3)=

[3] Daniel Bush, Caswell Barry, and Neil Burgess, “What do grid cells contribute to place cell firing?,” *Trends in Neurosciences*, vol. 37, no. 3, pp. 136–145, 2014, doi: [10.1016/j.tins.2013.12.003](https://pubmed.ncbi.nlm.nih.gov/24485517/).

## Additional Reading Materials

Read the 2025 paper's parameter definitions and Figure 2 alongside the executable equations above. Compare the available 2026 cosine formulation before transferring numerical parameters between versions. Then read the grid-to-place review [[3]](#grid-ref-3) and the [research roadmap](roadmap.md) for learned representations, path integration, and experimental validation. The browser and notebook are a specified teaching model, not a reproduction of the full published robot.
