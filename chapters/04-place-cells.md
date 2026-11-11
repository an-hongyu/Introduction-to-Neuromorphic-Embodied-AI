---
title: "Laboratory Guide · Place Cell Models"
---

# Place Cell Laboratory Guide

This guide accompanies [Chapter 2: Spatial Cells](02-spatial-cells.md), [Chapter 3: Computational Models of Neurons](03-computational-neuron-models.md), and Laboratory 1.

## Objectives

Build an idealized place field; convert a conditional rate into spikes; generate spatial rate maps that correct for occupancy; identify limitations of this baseline model.

## L1.1 Biological motivation

Place cells are neurons showing spatially modulated activity in particular contexts. Their fields can be influenced by sensory landmarks, movement, task demands, and environmental change. One Gaussian field is a **didactic approximation**, not a universal biological law.

## L1.2 Gaussian firing-rate model

Let $\mathbf{x}=(x,y)$ be position and $\boldsymbol{\mu}_i$ a preferred location of neuron $i$. We use

$$
r_i(\mathbf{x})=r_{\min,i}+(r_{\max,i}-r_{\min,i})
\exp\left[-\frac{\|\mathbf{x}-\boldsymbol{\mu}_i\|^2}{2\sigma_i^2}\right].
$$

All spatial coordinates and $\sigma_i$ use meters; firing rates use spikes/s (Hz). Peak rate occurs at $\mathbf{x}=\boldsymbol{\mu}_i$. At distance $\sigma_i$, the excess rate over baseline is $e^{-1/2}\approx0.607$ times its peak excess value.

## L1.3 From expected rates to spikes

For a simulation time step $\Delta t$ in seconds, assume conditionally independent, inhomogeneous Poisson firing. The number of spikes in a bin has distribution

$$N_i[t]\sim\operatorname{Poisson}(r_i(\mathbf{x}_t)\Delta t).$$

For bins small enough that multiple events are rare, a binary event can be drawn with probability $1-\exp[-r_i(\mathbf{x}_t)\Delta t]$. In this notebook we sample Poisson counts, which remain valid even for larger bins.

## L1.4 Occupancy normalization

Divide the arena into bins indexed by $b$. Let $T_b$ be total time spent in bin $b$, and $K_b$ the total observed spikes. A naive estimate is $\hat r_b=K_b/T_b$ for $T_b>0$. Bins with no visits should be masked, **not set to zero**, and low-occupancy estimates are noisy. Smoothness must not be confused with empirical evidence of a broad field.

## L1.5 Executable laboratory

Open [Place Cell Notebook](../notebooks/place_cells.ipynb). It simulates a reproducible trajectory, plots true firing field, observed spikes and rate estimate, and reports occupancy coverage plus simple error metrics.

[Run the notebook in Google Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/place_cells.ipynb), or {download}`download the Jupyter notebook <../notebooks/place_cells.ipynb>` and run it locally with JupyterLab. The published notebook includes reproducible code, computed results, and figures.

## L1.6 Research extensions

- Replace circular Gaussian fields with elliptical or multimodal fields.
- Compare Poisson spiking with refractory or LIF mechanisms.
- Add boundary effects and landmark remapping.
- Calibrate model statistics against experimental rodent recordings, while separating training and validation sessions.
- Expand to a population and benchmark position decoding against a non-neural baseline.

## Exercises

1. Double $\sigma$ and quantify how the proportion of arena above 10 Hz changes.
2. Halve $\Delta t$ while keeping the trajectory duration fixed. What should happen to *expected total spike count*?
3. Repeat with five random seeds. Estimate variation in the occupancy-normalized field.
4. Explain why true simulated position used to compute the field is not proof of a robot's ability to localize itself.

## References

[1] J. O'Keefe and J. Dostrovsky, “The hippocampus as a spatial map. Preliminary evidence from unit activity in the freely-moving rat,” *Brain Res.*, vol. 34, no. 1, pp. 171–175, 1971, doi: [10.1016/0006-8993(71)90358-1](https://pubmed.ncbi.nlm.nih.gov/5124915/).

[2] W. Gerstner, W. M. Kistler, R. Naud, and L. Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014. [Online textbook](https://neuronaldynamics.epfl.ch/online/).
