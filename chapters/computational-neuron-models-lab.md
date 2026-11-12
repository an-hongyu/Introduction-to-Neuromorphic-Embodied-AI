---
title: "Laboratory Guide · Computational Models of Neurons"
---

Begin the computational laboratories here, before the Place Cell experiment. [Chapter 2](03-computational-neuron-models.md) develops the theory; this section turns the equations into a reproducible single-neuron simulation. The first executable experiment uses a leaky integrate-and-fire (LIF) neuron. We then move from a neuron's temporal dynamics to spatial tuning in Laboratory 2.

## L1.1 What will we model?

A computational neuron maps inputs and internal state to an output. Choose what the experiment needs to explain before choosing a model [[1]](#neuron-lab-ref-1).

| Model | State or output | Question to ask in an experiment |
|---|---|---|
| Rate model | Expected firing rate | How does a chosen input change mean activity? |
| Poisson count model | Random spike counts conditional on a rate | How does stochastic sampling change an observed response? |
| LIF model | Membrane voltage and discrete spike events | How do integration, leak, threshold, and reset determine spike timing? |
| Conductance-based model | Voltage and channel-gating states | Which ionic mechanisms are needed to explain the voltage waveform? |

These are different abstractions, not interchangeable names for the same computation. In particular, a place field describes how activity depends on position; it does not specify how membrane voltage produces a spike. Laboratory 2 imposes a position-dependent rate and samples Poisson counts. It does not silently substitute that procedure for an LIF simulation.

## L1.2 Define the LIF experiment

For a constant applied current, use

$$
C_m\frac{dV}{dt}=-g_L(V-E_L)+I.
$$

Here $V$ is membrane voltage, $C_m$ membrane capacitance, $g_L$ leak conductance, $E_L$ leak reversal potential, and $I$ applied current. When voltage reaches the threshold $V_{\mathrm{th}}$, record a spike event, reset voltage to $V_{\mathrm{reset}}$, and hold it there for an absolute refractory interval $t_{\mathrm{ref}}$. The event is an abstraction of a spike; the model does not reproduce its ionic waveform [[1]](#neuron-lab-ref-1).

Use the same illustrative parameters as Chapter 2:

| Quantity | Value |
|---|---|
| $C_m$ | 200 pF |
| $g_L$ | 10 nS |
| $E_L$ and $V_{\mathrm{reset}}$ | −65 mV |
| $V_{\mathrm{th}}$ | −50 mV |
| $t_{\mathrm{ref}}$ | 2 ms |
| $I$ | 200 pA |
| Simulation step $\Delta t$ | 0.1 ms |

With pF, nS, mV, pA, and ms, both sides of the differential equation have units of pA. Define $\tau_m=C_m/g_L=20\,\mathrm{ms}$ and $V_\infty=E_L+I/g_L=-45\,\mathrm{mV}$. Between reset events, the exact passive update is

$$
V_{n+1}=V_\infty+(V_n-V_\infty)e^{-\Delta t/\tau_m}.
$$

The notebook checks threshold at the end of each step. Thus the passive voltage update is exact for constant current, while detected spike times still have finite time-step resolution.

## L1.3 Run the notebook

Open [Laboratory 1 — Leaky Integrate-and-Fire Neuron](../notebooks/lif_neuron.ipynb), [run it in Google Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/lif_neuron.ipynb), or {download}`download the notebook <../notebooks/lif_neuron.ipynb>` for local JupyterLab.

Run all cells in order. `simulate_lif` returns time, voltage, and a separate spike-event array. The notebook embeds its full simulation code, so Colab needs no repository imports. It contains four guided examples matching [Chapter 2, Section 2.5](03-computational-neuron-models.md#lif-editable-simulator):

| Example | Edit | Observe |
|---|---|---|
| Constant-current LIF | Current, capacitance, leak, threshold, refractory duration | First-spike time and current–rate curve |
| RC charging | Capacitance and pulse duration | Charging speed and return to rest |
| Temporal integration | Pulse separation, amplitude, capacitance | Close versus separated inputs and spike events |
| Multisource integration | B's weight/delay and negative input | Summed current, threshold crossings, and event counts |

Predict first, edit one parameter, rerun that example, then explain the change. Parameters in each example are explicit; editing Example 1 does not silently change Examples 2–4. The published figures show reference outputs. Execute edits in Colab or local JupyterLab. All numerical values are teaching assumptions, not parameters fitted to a biological recording.

```{figure} ../assets/lif-neuron-model.png
:alt: LIF reset voltage trace, separate spike-event markers, and analytical versus simulated firing rates

The single-neuron experiment. Spike events are shown separately because the stored voltage trace resets immediately after a detected threshold crossing.
```

## L1.4 Check the result before interpreting it

Starting at reset, the analytical first crossing time is

$$
t_{\mathrm{cross}}=\tau_m\ln\left(\frac{V_\infty-V_{\mathrm{reset}}}{V_\infty-V_{\mathrm{th}}}\right)
=20\ln(4)\,\mathrm{ms}\approx27.73\,\mathrm{ms}.
$$

Adding the 2 ms refractory interval gives a steady firing rate of approximately $33.64\,\mathrm{Hz}$. The notebook's 0.1 ms endpoint detection produces approximately $33.56\,\mathrm{Hz}$. Compare interspike intervals rather than a short recording's total spike count, which also depends on the initial transient and observation window. At 100 pA, the steady voltage is −55 mV, below threshold, so this deterministic experiment should produce no spikes from the chosen initial state.

Submit the voltage/event plot, the current–rate curve, your parameter values and units, and a short explanation of the analytical–numerical difference. A successful assertion confirms this implementation under its tested conditions; it does not establish biological validity.

## L1.5 Exercises and next laboratory

1. Change the time step from 0.1 ms to 0.05 ms. Compare the first spike time and mean interspike interval with the analytical values.
2. Increase current from 100 pA to 200 pA. Explain the transition using $V_\infty$ and threshold.
3. Set `capacitance_pf` to 400 in the Example 1 parameter cell. The simulator already computes `tau_ms = capacitance_pf / leak_ns`. Compare voltage rise and firing rate while keeping leak and current fixed. Explain the RC charging plot as well.
4. Explain why searching the returned voltage trace for an action-potential peak will not recover the separate spike-event array.
5. Before opening the Place Cell notebook, identify which input changes from a constant current to a position-dependent rate and which spike-generation assumption changes.

Continue to the [Place Cell laboratory guide](04-place-cells.md) and [Laboratory 2 — Building a Place Cell from Scratch](../notebooks/place_cells.ipynb), followed by [Laboratory 3 — Hebbian Association and STDP](../notebooks/hebbian_learning.ipynb).

## L1.6 Read from mechanism to computation

Mallot's treatment begins with excitable membranes and connects channel dynamics, reduced models, receptive fields, and network computation [[2]](#neuron-lab-ref-2). Use that progression to ask what each simplification retains: the LIF experiment retains passive integration and event timing but replaces the action-potential mechanism with a threshold/reset rule. Its threshold is a specified parameter, rather than a voltage-gated sodium current emerging from channel kinetics.

O'Reilly and colleagues introduce neural computation through inputs, integration, outputs, and then networks and learning [[3]](#neuron-lab-ref-3). For this laboratory, distinguish the **instantaneous state** (voltage), the **output** (spike-event times), and **parameters** (leak, threshold, and reset). None of these parameters learns in the present experiment. Synaptic weight changes belong to the later Hebbian laboratory.

For a membrane-level reading path, use Mallot Chapter 1, especially Sections 1.2–1.4. For a conceptual bridge toward cognition, read Chapters 2–4 of the supplied first-edition *Computational Cognitive Neuroscience*. The [reference-book reading map](roadmap.md#reference-book-reading-map) connects these readings to the four foundation chapters and identifies the editions used.

## References

(neuron-lab-ref-1)=
[1] Wulfram Gerstner, Werner M. Kistler, Richard Naud, and Liam Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014, ch. 1. [Online chapter](https://neuronaldynamics.epfl.ch/online/Ch1.html).


(neuron-lab-ref-2)=
[2] Hanspeter A. Mallot, *Computational Neuroscience: A First Course*. Cham, Switzerland: Springer, 2013, ch. 1, doi: 10.1007/978-3-319-00861-5. [Publisher](https://link.springer.com/book/10.1007/978-3-319-00861-5).

(neuron-lab-ref-3)=
[3] Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 1st ed. Wiki Book, 2012, chs. 2–4, supplied PDF snapshot generated Aug. 25, 2016. [Institutional publication record](https://experts.colorado.edu/display/pubid_85822); [current online edition](https://book.compcogneuro.org/).
