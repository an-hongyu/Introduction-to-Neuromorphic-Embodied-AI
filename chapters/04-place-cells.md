---
title: "Laboratory 2 - Place Cell Experiment Guide"
---

# Place Cell Laboratory Guide

The biological explanation, Gaussian place-field model, spike-generation assumptions, and grid-to-place model are integrated into [Chapter 4: Spatial Cells and Their Models](02-spatial-cells.md#place-cell-models). This page provides the execution sequence for [Laboratory 2](../notebooks/place_cells.ipynb), not a separate model chapter. Begin with the [Computational Models of Neurons laboratory guide](computational-neuron-models-lab.md) and its LIF notebook.

## Objectives

- Run the Gaussian place-field and Poisson-spike experiment with explicit units.
- Reconstruct a spatial rate map using occupancy normalization.
- Change one parameter at a time and distinguish imposed fields from learned representations.

## L2.1 Prepare the experiment

Read the [Gaussian place-field model](02-spatial-cells.md#place-gaussian-model) and [rate-to-spike construction](02-spatial-cells.md#place-spike-generation). Record the field center, width, baseline rate, peak rate, time step, and random seed before running the notebook. Spatial coordinates and widths use meters; rates use Hz; time steps use seconds.

## L2.2 Run and inspect

Open [Place Cell Notebook](../notebooks/place_cells.ipynb). It simulates a reproducible trajectory, plots the imposed firing field, sampled spikes, and estimated rate, and reports occupancy coverage and reconstruction error. Run cells in order and inspect each plot together with its units.

[Run in Google Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/place_cells.ipynb), or {download}`download the Jupyter notebook <../notebooks/place_cells.ipynb>` for JupyterLab.

## L2.3 Reconstruct and compare

Use the [occupancy-normalized estimator](02-spatial-cells.md#spatial-tuning-estimation). Mask unvisited bins, identify low-occupancy regions, and compare the estimate with the imposed rate field. Hold the trajectory fixed when comparing different spike-generation seeds. Report the smoothing and binning procedure rather than interpreting smoothness as biological evidence.

## L2.4 Extend the model

Try an elliptical or multimodal field, introduce landmark or boundary changes, compare Poisson events with a refractory or LIF mechanism, and evaluate a population decoder on held-out trajectories. These are extensions to test, not capabilities demonstrated by the baseline notebook. For a different place-field construction, continue to the [grid-to-place readout and interactive experiment](02-spatial-cells.md#grid-place-live-example) and [Laboratory 8](../notebooks/grid_to_place.ipynb).

## Exercises

1. Double $\sigma$ and quantify how the proportion of arena above 10 Hz changes.
2. Halve $\Delta t$ while keeping the trajectory duration fixed. What should happen to *expected total spike count*?
3. Repeat with five random seeds. Estimate variation in the occupancy-normalized field.
4. Explain why true simulated position used to compute the field is not proof of a robot's ability to localize itself.
