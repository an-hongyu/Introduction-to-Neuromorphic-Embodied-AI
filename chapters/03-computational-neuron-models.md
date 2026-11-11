---
title: "Chapter 3 · Computational Models of Neurons"
---

## 3.1 Learning objectives and the modeling question

A computational neuron model is a set of equations and event rules that predicts some aspect of a neuron's response. The right model depends on the question: membrane-current mechanisms, spike timing, population activity, learning dynamics, or hardware cost. More state variables do not automatically make a model more useful, and fewer state variables do not automatically make it biologically wrong [[1]](#models-ref-1).

After this chapter, you should be able to distinguish rate models from spike-generation models, implement a leaky integrate-and-fire neuron with explicit units, explain what conductance-based models add, and choose a model with a stated validation target.

## 3.2 Three levels of description

| Description | Example output | What it does not establish by itself |
|---|---|---|
| Tuning or rate model | Expected firing rate as a function of position or input | Membrane mechanism or individual spike times |
| Point spiking-neuron model | Voltage-like state and emitted spike times | Full dendritic geometry or molecular mechanisms |
| Conductance-based or compartmental model | Ionic currents, voltage dynamics, and possibly spatial compartments | Correctness for a cell type without parameter calibration |

The [Gaussian place field in Chapter 2](02-spatial-cells.md) belongs to the first category. A prescribed rate can drive a stochastic spike generator, or it can be mapped into an input current for a dynamical neuron. Those are different model constructions, with different assumptions and calibration requirements.

## 3.3 A rate model with Poisson spike counts

Let $r_i(t)$ be a nonnegative rate in Hz. A convenient conditional model for counts in bins of duration $\Delta t$ seconds is

$$
N_i[n]\sim\operatorname{Poisson}\!\left(r_i[n]\Delta t\right).
$$

The expected count and count variance are both $r_i[n]\Delta t$. For a Poisson bin count, the probability of at least one spike is

$$
P\bigl(N_i[n]\geq1\bigr)=1-e^{-r_i[n]\Delta t}.
$$

**Worked example.** At 20 Hz with a 5 ms bin, the expected count is 0.1 and the probability of at least one spike is approximately 0.0952. A count model can produce more than one event per bin. Replacing its count with a Boolean event loses multiplicity.

```python
import numpy as np
rng = np.random.default_rng(2026)
rate_hz = 20.0
dt_s = 0.005
counts = rng.poisson(rate_hz * dt_s, size=200)
print("Spikes in one simulated second:", counts.sum())
```

The expected total is 20; an individual realization need not equal 20. Independent Poisson sampling does not include an absolute refractory period, adaptation, or history-dependent firing. It is a baseline assumption to test, not a definition of biological spiking [[1]](#models-ref-1).

## 3.4 Leaky integrate-and-fire: integrate, cross threshold, reset

The **leaky integrate-and-fire (LIF)** model uses a passive voltage equation between spikes:

$$
C_m\frac{dV}{dt}=-g_L(V-E_L)+I(t).
$$

When $V$ reaches $V_{\mathrm{th}}$, the model emits an event and applies a reset:

$$
V\geq V_{\mathrm{th}}\quad\Longrightarrow\quad
\text{emit spike},\qquad V\leftarrow V_{\mathrm{reset}}.
$$

During an optional absolute refractory period $t_{\mathrm{ref}}$, hold $V$ at the reset voltage. This event rule replaces the action-potential waveform; a plotted vertical spike marker is not a simulated sodium-current-driven upstroke.

With $\tau_m=C_m/g_L$ and $R_m=1/g_L$, the subthreshold equation becomes

$$
\tau_m\frac{dV}{dt}=-(V-E_L)+R_m I(t).
$$

For constant input during a step, an exact subthreshold update is

$$
V_{n+1}=V_\infty+(V_n-V_\infty)e^{-\Delta t/\tau_m},
\qquad V_\infty=E_L+I/g_L.
$$

The exponential update is exact between events under the constant-input assumption. Detecting a threshold crossing only at time-step endpoints still quantizes spike times.

## 3.5 A worked LIF neuron with units

Use these pedagogical parameters:

| Parameter | Value | Meaning |
|---|---:|---|
| $C_m$ | 200 pF | Total capacitance |
| $g_L$ | 10 nS | Leak conductance |
| $E_L$ | −65 mV | Leak reversal potential |
| $V_{\mathrm{reset}}$ | −65 mV | Reset voltage |
| $V_{\mathrm{th}}$ | −50 mV | Threshold |
| $t_{\mathrm{ref}}$ | 2 ms | Absolute refractory duration |
| $I$ | 200 pA | Constant input current |

Then $\tau_m=20$ ms and $V_\infty=-45$ mV. Starting from reset, the subthreshold crossing time is

$$
t_{\mathrm{cross}}=\tau_m\ln\!\left(
\frac{V_\infty-V_{\mathrm{reset}}}{V_\infty-V_{\mathrm{th}}}
\right)=20\ln(4)\approx27.73\ \mathrm{ms}.
$$

The steady firing rate including the refractory interval is approximately

$$
f=\frac{1000}{t_{\mathrm{cross}}+t_{\mathrm{ref}}}
\approx33.64\ \mathrm{Hz},
$$

where 1000 converts a period in milliseconds into events per second. The expression assumes $V_\infty>V_{\mathrm{th}}$ and periodic constant drive. At or below the asymptotic threshold, this deterministic model does not repeatedly fire from reset.

```python
import numpy as np

def simulate_lif(current_pa=200.0, duration_ms=500.0, dt_ms=0.1):
    tau_ms, leak_ns, rest_mv = 20.0, 10.0, -65.0
    threshold_mv, reset_mv, refractory_ms = -50.0, -65.0, 2.0
    voltage = reset_mv
    hold_steps = 0
    trace, spikes = [], []
    for step in range(round(duration_ms / dt_ms)):
        if hold_steps > 0:
            voltage = reset_mv
            hold_steps -= 1
        else:
            steady_mv = rest_mv + current_pa / leak_ns
            voltage = steady_mv + (voltage - steady_mv) * np.exp(-dt_ms / tau_ms)
            if voltage >= threshold_mv:
                spikes.append((step + 1) * dt_ms)
                voltage = reset_mv
                hold_steps = round(refractory_ms / dt_ms)
        trace.append(voltage)
    return np.asarray(trace), np.asarray(spikes)
```

The returned trace stores the reset value at a detected spike. Keep the separate event list; do not try to recover spike times by searching this trace for action-potential peaks. The [LIF notebook](../notebooks/lif_neuron.ipynb) plots the trace, event markers, and a current–rate curve and compares simulated intervals with the analytical result.

```{figure} ../assets/lif-neuron-model.png
:label: fig-lif-model
:alt: LIF membrane voltage with separate spike-event markers and a current versus firing-rate curve
:width: 100%

A synthetic LIF example. Event markers are drawn above the reset trace; they do not represent modeled action-potential waveforms. The current–rate panel compares long-run simulated rates with the analytical constant-input prediction.
```

## 3.6 Conductance-based models and Hodgkin–Huxley

The Hodgkin–Huxley framework describes voltage through ionic conductances and gating variables [[2]](#models-ref-2). In a modern inward-positive input convention, a representative equation is

$$
C_m\frac{dV}{dt}=I_{\mathrm{ext}}
-\overline g_{\mathrm{Na}}m^3h(V-E_{\mathrm{Na}})
-\overline g_{\mathrm{K}}n^4(V-E_{\mathrm{K}})
-g_L(V-E_L).
$$

Each gate $q\in\{m,h,n\}$ evolves according to voltage-dependent opening and closing rates,

$$
\frac{dq}{dt}=\alpha_q(V)(1-q)-\beta_q(V)q.
$$

Here $m$ and $h$ describe sodium activation and inactivation, while $n$ describes potassium activation in the classical model. If conductances are specified per membrane area, capacitance and current must also be specified per area. Do not mix a current density with the total capacitance used in the LIF example.

A complete simulation additionally needs rate functions, reversal potentials, parameter values, temperature assumptions, initial conditions, and a numerical method. The equations above introduce the structure; they are not presented as a complete runnable Hodgkin–Huxley implementation or as a universal parameterization for hippocampal cells.

## 3.7 Adaptive exponential and Izhikevich models

The adaptive exponential integrate-and-fire model adds an exponential spike-initiation term and a recovery current [[3]](#models-ref-3):

$$
C_m\dot V=-g_L(V-E_L)+g_L\Delta_Te^{(V-V_T)/\Delta_T}-w+I,
\qquad
\tau_w\dot w=a(V-E_L)-w.
$$

On a chosen spike event, voltage is reset and $w$ is increased by a specified amount. $w$ is an adaptation current, $a$ a conductance, $\tau_w$ an adaptation time constant, and $\Delta_T$ a voltage scale. These parameters allow richer responses than a passive LIF model, but must be calibrated for the intended application.

The Izhikevich model uses two coupled state variables with a reset and can reproduce several qualitative spiking and bursting patterns with different parameter choices [[4]](#models-ref-4). Its compact form is useful for exploring population dynamics. Reproducing one firing pattern does not establish that its internal variables uniquely correspond to the biological mechanisms of a specific cell.

| Model | Principal state | Useful first question |
|---|---|---|
| Poisson rate-to-count model | Prescribed rate | How does stochastic sampling affect a tuning map? |
| LIF | Voltage plus reset/refractory state | How do integration and thresholding transform inputs into events? |
| Adaptive exponential model | Voltage and adaptation current | Does adaptation alter responses to sustained input? |
| Izhikevich model | Voltage-like and recovery variables | Which qualitative firing regimes affect the network? |
| Hodgkin–Huxley-type model | Voltage and channel gates | Which ionic mechanisms shape the response? |

## 3.8 Synaptic input and model validation

A current-based synapse prescribes a current waveform. A conductance-based synapse uses a term such as $g_{\mathrm{syn}}(t)(E_{\mathrm{syn}}-V)$ and therefore changes both current and effective membrane conductance. State which form you use, along with its time course, delay, units, and sign convention.

Before using a neuron model in a spatial network, test a zero-input baseline, a subthreshold input, a suprathreshold input, and the effect of a smaller time step. Compare quantities that matter to the task: firing rate, spike timing, adaptation, stability, latency, or hardware energy. Energy efficiency must be measured on the stated implementation; it cannot be inferred from the presence of spikes.

For the running LIF example, verify $\tau_m=20$ ms and $t_{\mathrm{cross}}\approx27.73$ ms analytically. Then compare the simulated interspike interval at 0.1 ms and 0.05 ms resolution. Agreement under refinement is more informative than an attractive voltage plot alone.

### Model reduction: a two-variable excitable system

Mallot introduces the FitzHugh–Nagumo system as a reduced description for studying excitation and recovery [[5]](#models-ref-5). One dimensionless form is

$$
\frac{dv}{ds}=v(a-v)(v-1)-w+j, \qquad
\frac{dw}{ds}=bv-\gamma w.
$$

Here $v$ is an excitation variable, $w$ is a recovery variable, $s$ is scaled time, $j$ is an applied drive, and $a$, $b$, and $\gamma$ are model parameters. These variables are dimensionless; they must not be inserted into the LIF notebook as mV, ms, or pA without defining a transformation. The curves $w=v(a-v)(v-1)+j$ and $w=(b/\gamma)v$, for nonzero $\gamma$, are the nullclines. Their intersections are equilibrium candidates. Stability requires analysis of the dynamics near an intersection, rather than merely finding a crossing.

This example adds a useful comparison: Hodgkin–Huxley describes explicit channel-gating variables; a two-variable reduction emphasizes excitation and recovery; LIF uses a passive voltage equation with discrete threshold/reset events. A reduced model can clarify qualitative behavior while leaving channel-specific questions unanswered. The present executable laboratory implements LIF; no FitzHugh–Nagumo implementation is claimed here.

Begin the practical sequence with the [Computational Models of Neurons laboratory guide](computational-neuron-models-lab.md), then run Laboratory 1 before the Place Cell rate-model experiment.

## 3.9 Exercises

1. Compute the expected spike count and probability of at least one event for 50 Hz in a 2 ms bin.
2. For the LIF parameters above, explain why 100 pA does not produce sustained firing from reset.
3. Change capacitance to 400 pF while keeping conductance and current fixed. Which steady-state quantities remain the same, and which timing quantities change?
4. Explain the difference between a reset rule and a modeled action-potential waveform.
5. Choose a model for (a) occupancy-map uncertainty, (b) adaptation, and (c) sodium-channel dynamics. Defend each choice.

## References

(models-ref-1)=

[1] W. Gerstner, W. M. Kistler, R. Naud, and L. Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014, chs. 1–3 and 5–6. [Online textbook](https://neuronaldynamics.epfl.ch/online/).

(models-ref-2)=

[2] A. L. Hodgkin and A. F. Huxley, “A quantitative description of membrane current and its application to conduction and excitation in nerve,” *J. Physiol.*, vol. 117, no. 4, pp. 500–544, 1952, doi: [10.1113/jphysiol.1952.sp004764](https://pubmed.ncbi.nlm.nih.gov/12991237/).

(models-ref-3)=

[3] R. Brette and W. Gerstner, “Adaptive exponential integrate-and-fire model as an effective description of neuronal activity,” *J. Neurophysiol.*, vol. 94, no. 5, pp. 3637–3642, 2005, doi: [10.1152/jn.00686.2005](https://pubmed.ncbi.nlm.nih.gov/16014787/).

(models-ref-4)=

[4] E. M. Izhikevich, “Simple model of spiking neurons,” *IEEE Trans. Neural Netw.*, vol. 14, no. 6, pp. 1569–1572, 2003, doi: [10.1109/TNN.2003.820440](https://pubmed.ncbi.nlm.nih.gov/18244602/).


(models-ref-5)=

[5] H. A. Mallot, *Computational Neuroscience: A First Course*. Cham, Switzerland: Springer, 2013, sec. 1.3, doi: 10.1007/978-3-319-00861-5. [Publisher](https://link.springer.com/book/10.1007/978-3-319-00861-5).
