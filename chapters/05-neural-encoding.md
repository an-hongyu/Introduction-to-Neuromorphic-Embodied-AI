---
title: "Chapter 5 · Neural Encoding and the ANN–SNN Bridge"
---

## 5.1 Learning objectives

By the end of this chapter, you should be able to define a feature-to-current or feature-to-rate mapping, distinguish a spike event from a firing-rate estimate, compare ANN and SNN abstractions, and explain what information an encoder discards. This connects the course's neural-system-to-ANN material with the sensor experiments in Chapters 6–8.

## 5.2 What does a spike represent?

A spike train can be written as $s_i(t)=\sum_k\delta(t-t_{ik})$, where $t_{ik}$ is the time of event $k$ in channel $i$. Individual events are discrete; **their timing and frequency can carry information**. LIF simplifies the action-potential waveform, while retaining event times and allowing rate measurements [[1]](#encoding-ref-1). Binary event output does not mean that the temporal sequence contains only one bit of information.

For a window of length $T$ seconds containing $K$ events,

$$
\widehat r=K/T\quad\text{Hz}.
$$

**Worked example.** Four events in 100 ms give 40 Hz. Shifting the window boundary can change this count, especially for a transient input. A first-spike latency measures a different quantity: $\ell=t_{\mathrm{first}}-t_{\mathrm{cue}}$. Declare the cue onset, handling of trials with no spike, and observation window. Neither statistic is an intrinsic property of the encoder alone.

```python
import numpy as np
spikes_s = np.array([0.012, 0.037, 0.061, 0.088])
window_s = 0.100
rate_hz = np.count_nonzero((spikes_s >= 0) & (spikes_s < window_s)) / window_s
print(rate_hz, spikes_s[0])  # 40.0 Hz; first event at 0.012 s
```

## 5.3 A transparent encoding contract

A feature $z\in[0,1]$ may prescribe a rate $r(z)=r_{\min}+(r_{\max}-r_{\min})z$, or a current $I(z)=I_0+I_1z$. These are **alternative constructions**. Prescribing 40 Hz to a Poisson generator does not guarantee that applying a numerically similar current to an LIF neuron produces 40 Hz.

Use this contract for each sensor:

| Item | Example | Why it matters |
|---|---|---|
| Raw measurement and units | RGB intensities; acceleration in m/s²; range in m | Makes preprocessing reproducible |
| Feature definition | Red contrast averaged over a region | Determines what information survives |
| Validity and timestamp | Finite range, scan time, sensor frame | Missing data must not look like a valid weak signal |
| Neural mapping | $I=50+250z$ pA | Establishes gain, baseline, and saturation |
| Output statistic | Events per 500 ms; first-event latency | Determines what the decoder can use |

With the Chapter 3 parameters, $I=50+250z$ crosses the passive rheobase of 150 pA only when $z>0.4$. At $z=0.4$, voltage approaches threshold asymptotically; a finite window has no spike. At $z=1$, current is 300 pA and the analytical periodic rate is approximately 63.04 Hz. Check both first-event delay and long-run rate before selecting a motor-response threshold.

## 5.4 ANN and SNN: a useful bridge

An ANN layer computes $\mathbf y=\phi(\mathbf W\mathbf x+\mathbf b)$. A point SNN neuron evolves a state across time and emits events. The weighted sum is a useful shared abstraction; time constants, reset, refractory behavior, and synaptic filters add assumptions to the spiking construction [[1]](#encoding-ref-1).

| Question | ANN teaching layer | LIF teaching neuron |
|---|---|---|
| Input | Feature vector per forward pass | Current or filtered events over time |
| State | Often none between passes | Voltage and refractory state |
| Output | Continuous activation | Event times; optional filtered activity |
| Learning | May use backpropagation | May use local, surrogate-gradient, or other specified rules |

An SNN is not automatically more accurate, more biological, or more energy efficient. Those conclusions need a task, a trained model, and a measured implementation. The course's ANN material provides a vocabulary for features, weights, nonlinearities, and evaluation; it does not make ANN-to-SNN conversion an identity.

## 5.5 Example — encode three modalities

[Laboratory 6](../notebooks/sensory_encoding.ipynb) contains three synthetic experiments: RGB red contrast mapped to physical-unit LIF current, acceleration mapped to a causal vibration feature, and 360 range rays compressed into 36 angular channels. Each has a different unit, validity rule, and retained information. Run it in [Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/sensory_encoding.ipynb).

Keep the preprocessing fixed when comparing learning rules. Otherwise an apparent learning benefit could come from changing the input detector. Use separate voltage and event panels, then report the statistic the downstream behavior actually consumes.

## 5.6 Exercises

1. Compare two event trains with the same count but different first-event latencies.
2. At $z=0.6$, calculate current and passive equilibrium for the mapping above.
3. Explain why an invalid range with rate zero needs a validity mask.
4. Compare a 50 ms and a 500 ms response window. What changes besides the estimated rate?

## References

(encoding-ref-1)=

[1] W. Gerstner, W. M. Kistler, R. Naud, and L. Paninski, *Neuronal Dynamics*. Cambridge, U.K.: Cambridge University Press, 2014, chs. 1, 5, and 7. [Online textbook](https://neuronaldynamics.epfl.ch/online/).

## Additional Reading Materials

Read the rate and spike descriptions in [[1]](#encoding-ref-1), then compare [Chapter 2](02-spatial-cells.md)'s imposed spatial tuning with [Chapter 3](03-computational-neuron-models.md)'s dynamical membrane model. Use the [course reading map](course-reading-map.md) to connect the ANN lectures to these explicit modeling choices.
