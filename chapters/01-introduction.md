---
title: "Overview · Neuromorphic Embodied AI"
---

# Neuromorphic Embodied AI: A Closed-Loop Overview

## O.1 Learning objectives

After this chapter, you should be able to (1) distinguish embodied intelligence from offline perception, (2) describe how sensory cues, self-motion, neural state and actions form a closed loop, and (3) identify the main classes of spatial cells and their computational roles.

## O.2 Intelligence in a closed sensorimotor loop

An embodied agent perceives the environment, changes its state through action, and obtains new observations as a result. Denote physical state by $\mathbf{x}_t$, sensor data by $\mathbf{o}_t$, internal neural state by $\mathbf{z}_t$, and motor command by $\mathbf{a}_t$. A simplified loop is

$$
\mathbf{o}_t = h(\mathbf{x}_t)+\boldsymbol{\epsilon}_t,\qquad
\mathbf{z}_{t+1}=F(\mathbf{z}_t,\mathbf{o}_t,\mathbf{a}_{t}),
$$

$$
\mathbf{a}_t=\pi(\mathbf{z}_t),\qquad
\mathbf{x}_{t+1}=f(\mathbf{x}_t,\mathbf{a}_t)+\boldsymbol{\eta}_t.
$$

The variables $\boldsymbol{\epsilon}_t$ and $\boldsymbol{\eta}_t$ represent observation and transition noise. These equations are a *general modeling scaffold*, not a claim that animals explicitly compute these functions.

## O.3 Why spikes?

Biological neurons communicate through action potentials. A spike train for neuron $i$ can be idealized as

$$s_i(t)=\sum_k \delta(t-t_i^{(k)}),$$

where $t_i^{(k)}$ is the time of the $k$th spike. In simulations we often use discrete bins $s_i[n]\in\{0,1\}$ and specify an explicit bin width $\Delta t$.

A neuromorphic model may compute with event-driven spikes and local synaptic state. It does **not** automatically follow that the model is biologically realistic or more energy efficient. Those properties must be tested separately.

## O.4 Spatial neural codes

| Neural population | Common experimental association | Introductory computational role |
|---|---|---|
| Place cells | Location-selective activity, especially in hippocampus | Represent candidate locations |
| Grid cells | Periodic spatial firing in medial entorhinal cortex | Support spatial metric/path-integration hypotheses |
| Head-direction cells | Heading-dependent firing | Represent orientation |
| Border/boundary-related cells | Environmental boundaries | Encode geometry and wall proximity |
| Speed cells | Movement-speed modulation | Represent locomotion magnitude |
| Time cells | Sequential activity tied to elapsed time in tasks | Represent temporal context |

These labels identify experimentally studied response patterns; functions are hypotheses and model choices rather than one-to-one biological assignments. Real neural responses depend on task, environment, behavioral state, and cell population.

## O.5 A minimal place-cell code

Consider a one-meter square arena and a single idealized cell with a preferred center $\boldsymbol{\mu}$. A useful starting rate model is

$$r(\mathbf{x})=r_{\min}+(r_{\max}-r_{\min})\exp\left(-\frac{\|\mathbf{x}-\boldsymbol{\mu}\|^2}{2\sigma^2}\right).$$

Here $r_{\min}$ is baseline firing, $r_{\max}$ is peak firing, and $\sigma$ is field width. This is an intentionally simplified phenomenological model; a biological field need not be circular or Gaussian.

In the [Place Cell chapter](04-place-cells.md) we will generate trajectories, conditionally stochastic spikes, occupancy-normalized rate maps, and a basic decoding exercise.

## O.6 From spatial codes to memory and behavior

We will distinguish four levels:

1. **Encode** sensor and motion variables into neural activities.
2. **Represent** spatial location, direction and context using populations.
3. **Learn** associations between spatial context, actions and outcomes.
4. **Act and validate** in a controlled simulated environment, then in robot hardware as appropriate.

The book will later introduce **Spike Flow Networks (SFNs)** as a proposed framework for organizing learnable ensemble-to-ensemble associations. Its capacity and consolidation rules will be presented as research hypotheses unless formally validated.

## O.7 Worked thought experiment

A robot starts at $(0.1,0.1)$ m and moves to $(0.5,0.5)$ m. A place cell centered at $(0.5,0.5)$ m should have a higher *expected* firing rate at the second location for fixed $\sigma$, but stochastic spike counts in short windows may not strictly increase on every run. This distinction motivates trial repetition and rate-map estimation.

## O.8 Exercises

1. Define the roles of $\mathbf{x}_t$, $\mathbf{o}_t$, $\mathbf{z}_t$, and $\mathbf{a}_t$ in a robot using LiDAR.
2. For $r_{\min}=0$, $r_{\max}=20$ Hz and $\sigma=0.15$ m, compute the expected rate at the field center and at a distance of 0.15 m.
3. Explain why a map of raw spike counts can be misleading when the robot visits some locations longer than others.
4. Propose an ablation study to evaluate whether head-direction signals improve spatial decoding.

## References

[1] J. O'Keefe and J. Dostrovsky, “The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat,” *Brain Res.*, vol. 34, no. 1, pp. 171–175, 1971, doi: [10.1016/0006-8993(71)90358-1](https://doi.org/10.1016/0006-8993(71)90358-1).

[2] T. Hafting, M. Fyhn, S. Molden, M.-B. Moser, and E. I. Moser, “Microstructure of a spatial map in the entorhinal cortex,” *Nature*, vol. 436, pp. 801–806, 2005, doi: [10.1038/nature03721](https://doi.org/10.1038/nature03721).

[3] J. S. Taube, R. U. Muller, and J. B. Ranck, Jr., “Head-direction cells recorded from the postsubiculum in freely moving rats. I. Description and quantitative analysis,” *J. Neurosci.*, vol. 10, no. 2, pp. 420–435, 1990, doi: [10.1523/JNEUROSCI.10-02-00420.1990](https://doi.org/10.1523/JNEUROSCI.10-02-00420.1990).

[4] W. Gerstner, W. M. Kistler, R. Naud, and L. Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014. [Online textbook](https://neuronaldynamics.epfl.ch/online/).
