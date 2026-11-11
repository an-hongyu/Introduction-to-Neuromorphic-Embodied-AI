---
title: "Chapter 3 · Computational Models of Neurons"
---

## 3.1 Learning objectives and the modeling question

A computational neuron model is a set of equations and event rules that predicts some aspect of a neuron's response. The right model depends on the question: membrane-current mechanisms, spike timing, population activity, learning dynamics, or hardware cost. More state variables do not automatically make a model more useful, and fewer state variables do not automatically make it biologically wrong [[1]](#models-ref-1).

After this chapter, you should be able to distinguish rate models from spike-generation models, map an LIF equation to an RC circuit, implement a leaky integrate-and-fire neuron with explicit units, change parameters to test temporal and multisource integration, explain what conductance-based models add, and choose a model with a stated validation target.

**Learn by changing a model.** Worked examples are part of the chapter, before the exercises. Follow **predict → run → change one parameter → explain**. The [self-contained LIF notebook](../notebooks/lif_neuron.ipynb) reproduces all four examples and plots. [Open it in Google Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/lif_neuron.ipynb) to edit code and rerun it, or {download}`download the notebook <../notebooks/lif_neuron.ipynb>` for JupyterLab. The published page shows the code and reference outputs; execute edited code in Colab or JupyterLab.

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

### 3.4.1 Where are the resistor and capacitor?

Yes: the passive part of LIF has an **RC equivalent circuit**. The membrane separates charge, represented by capacitance $C_m$. A leak path is represented by resistance $R_m=1/g_L$. A reversal-potential source $E_L$ sets the voltage to which the membrane relaxes without input. The capacitor is connected between the intracellular node and extracellular reference; the resistor and reversal source form the parallel leak branch. See the standard [*Neuronal Dynamics*, Fig. 1.6 and Section 1.3.1](https://neuronaldynamics.epfl.ch/online/Ch1.S3.html) [[1]](#models-ref-1).

```{figure} ../assets/lif-rc-circuit.svg
:label: fig-lif-rc-circuit
:alt: Original equivalent circuit with an input current source, membrane capacitor, leak resistor in series with a signed leak-reversal voltage source, and a separate abstract threshold and reset block
:width: 100%

**From membrane circuit to LIF.** Original teaching schematic based on the RC formulation in [[1]](#models-ref-1), sec. 1.3.1; the linked reference contains the source textbook's Fig. 1.6. The signed source voltage is −65 mV with the polarity shown. The dashed connection senses voltage for an abstract event rule; it is not an additional ionic-current branch or a transistor-level implementation.
```

| Circuit element | Neuron interpretation | What the student changes |
|---|---|---|
| Capacitor $C_m$ | Membrane stores charge; $I_C=C_m\,dV/dt$ | `capacitance_pf` changes charging speed |
| Leak resistor $R_m=1/g_L$ | Passive leak current $(V-E_L)/R_m$ | `leak_ns` changes leak, input resistance, and time constant |
| Signed source $E_L$ | Effective leak reversal potential | `rest_mv` changes the no-input equilibrium |
| Current source $I(t)$ | Injected current or an approximation to summed synaptic currents | Current amplitude, duration, and arrival times |
| Threshold/reset rule | Records events and restarts the state after a spike | `threshold_mv`, `reset_mv`, and `refractory_ms` |

Kirchhoff's current law gives

$$
I(t)=I_C+I_R=C_m\frac{dV}{dt}+\frac{V-E_L}{R_m}.
$$

Rearranging gives the LIF subthreshold equation. With 10 nS leak, $R_m=100$ MΩ; with 200 pF capacitance, $R_mC_m=20$ ms. The source represents a reversal potential phenomenologically, not a literal cellular battery. **An RC circuit alone charges and discharges; the threshold/reset rule adds the “fire” part.** Changing capacitance while keeping resistance fixed changes the speed but not the constant-current equilibrium $E_L+R_m I$.

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

(lif-editable-simulator)=

### 3.5.1 A simulator with editable physical parameters

Run this definition once before the example cells below. It accepts a **current array**, one value per time interval. Unlike a fixed-time-constant implementation, it computes `tau_ms = capacitance_pf / leak_ns`, so changing capacitance or resistance changes the dynamics correctly. Returned voltage includes the initial state and is one sample longer than the input. A separate event list stores spikes because the trace resets immediately after detection.

```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_lif(current_pa, dt_ms=0.1, capacitance_pf=200.0,
                 leak_ns=10.0, rest_mv=-65.0, threshold_mv=-50.0,
                 reset_mv=-65.0, refractory_ms=2.0, spiking=True):
    """One current value per time interval; return time, voltage, spike times.

    Units: pA, ms, pF, nS, mV. Initial voltage is reset_mv.
    Exact passive update for piecewise-constant current; endpoint events.
    spiking=False exposes the passive RC response without threshold/reset.
    """
    current = np.asarray(current_pa, dtype=float)
    if current.ndim != 1 or current.size == 0 or not np.isfinite(current).all():
        raise ValueError('Supply a nonempty, finite 1-D current array.')
    if dt_ms <= 0 or capacitance_pf <= 0 or leak_ns <= 0 or refractory_ms < 0:
        raise ValueError('dt, capacitance, and leak must be positive; refractory >= 0.')
    if reset_mv >= threshold_mv:
        raise ValueError('Reset must be below threshold.')
    tau_ms = capacitance_pf / leak_ns
    decay = np.exp(-dt_ms / tau_ms)
    time = np.arange(current.size + 1) * dt_ms
    voltage = np.empty(time.size)
    voltage[0] = reset_mv
    spikes, hold = [], 0
    # Round refractory duration upward to a whole number of time steps.
    refractory_steps = int(np.ceil(refractory_ms / dt_ms - 1e-12))
    for k, injected_pa in enumerate(current):
        if hold > 0:
            voltage[k + 1] = reset_mv
            hold -= 1
        else:
            steady_mv = rest_mv + injected_pa / leak_ns
            voltage[k + 1] = steady_mv + (voltage[k] - steady_mv) * decay
            if spiking and voltage[k + 1] >= threshold_mv:
                spikes.append(time[k + 1])
                voltage[k + 1] = reset_mv
                hold = refractory_steps
    return time, voltage, np.asarray(spikes)

def pulse_train(time_ms, starts_ms, width_ms=4.0, amplitude_pa=600.0):
    """Rectangular current pulses; time_ms contains interval start times."""
    current = np.zeros_like(time_ms, dtype=float)
    for start in starts_ms:
        current += amplitude_pa * ((time_ms >= start) & (time_ms < start + width_ms))
    return current
```

Use pF, nS, mV, pA, and ms throughout: pF × mV/ms and nS × mV both give pA. Current is held constant within each interval. The passive update is exact under that assumption, but spike times are detected only at endpoints. The refractory interval rounds upward to whole steps. Halve the time step to check timing sensitivity.

### 3.5.2 Example 1 — Change current, capacitance, leak, and threshold

**Predict.** A 100 pA current approaches −55 mV and remains below threshold. A 200 pA current approaches −45 mV and produces repeated events. What happens if capacitance doubles while the input stays at 200 pA?

```python
# Change ONE parameter, then rerun this cell.
dt_ms = 0.1
current_pa = 200.0
capacitance_pf = 200.0
leak_ns = 10.0
threshold_mv = -50.0
refractory_ms = 2.0
current = np.full(round(500 / dt_ms), current_pa)
t, v, spikes = simulate_lif(
    current, dt_ms=dt_ms, capacitance_pf=capacitance_pf,
    leak_ns=leak_ns, threshold_mv=threshold_mv,
    refractory_ms=refractory_ms)
print("Spike count:", len(spikes), "First events (ms):", spikes[:5])
plt.plot(t, v, label="Voltage (resets after a spike)")
plt.axhline(threshold_mv, ls="--", color="gray", label="Threshold")
plt.xlabel("Time (ms)"); plt.ylabel("Voltage (mV)")
plt.legend(); plt.show()
```

**Reference result.** At the defaults, the first detected event is 27.8 ms, compared with the analytical 27.73 ms. Subsequent intervals are 29.8 ms, or about 33.56 Hz. There are 16 events in 500 ms; that finite-window count gives 32 Hz, which differs from the interval-based steady rate because of the initial transient and window boundaries.

| Change one parameter | Try | Predict and explain |
|---|---|---|
| Input current | 100, 200, 300 pA | Does the passive equilibrium exceed threshold? |
| Capacitance | 100, 200, 400 pF | How does first-spike time change at fixed leak and current? |
| Leak conductance | 5, 10, 20 nS | Both the time constant and equilibrium change; stronger leak need not mean faster spiking |
| Threshold | −55, −50, −45 mV | At −45 mV, the 200 pA equilibrium equals threshold and is approached asymptotically |
| Refractory duration | 0, 2, 5 ms | The first spike is unchanged, while later interspike intervals change |

```{figure} ../assets/lif-neuron-model.png
:label: fig-lif-model
:alt: Default LIF voltage trace with separate spike events and a current-rate curve comparing simulation with the analytical prediction
:width: 100%

**Example 1 reference output.** The notebook displays separate event markers and compares simulated long-run interval rates with the analytical curve. Vertical markers are events, not modeled action-potential waveforms. All parameters are teaching assumptions.
```

### 3.5.3 Example 2 — Watch the capacitor charge

**Predict.** Inject the same 100 pA step into cells with 100, 200, and 400 pF capacitance while keeping leak at 10 nS. All have the same passive equilibrium of −55 mV. Their time constants are 10, 20, and 40 ms.

```python
sample = np.arange(1000) * 0.1
current = pulse_train(sample, [10], width_ms=80, amplitude_pa=100)
for cap in [100, 200, 400]:
    t, v, _ = simulate_lif(current, capacitance_pf=cap, spiking=False)
    plt.plot(t, v, label=f"C = {cap} pF")
plt.xlabel("Time (ms)"); plt.ylabel("Voltage (mV)")
plt.legend(); plt.show()
```

**Explain.** For a step beginning at $t_0$, $V(t)=V_\infty+[V(t_0)-V_\infty]e^{-(t-t_0)/\tau_m}$. After one time constant, about 63.2% of the final voltage shift is complete. A short pulse may end before that equilibrium is reached. `spiking=False` deliberately removes threshold/reset to isolate the circuit response. **Try:** shorten the pulse to 10 ms and explain why larger capacitance now gives a smaller peak shift.

```{figure} ../assets/lif-rc-charging.png
:label: fig-lif-rc-charging
:alt: Three passive RC voltage traces for different capacitances driven by the same rectangular 100 pA current step
:width: 100%

**Example 2 reference output.** Capacitance controls the approach to equilibrium and the return toward rest after the current ends. The right panel shows the common input; no spike/reset mechanism is active.
```

### 3.5.4 Example 3 — Temporal integration: same source, different arrival times

One source delivers two identical 600 pA pulses, each lasting 4 ms. Compare onset separations of 6 ms and 40 ms. The charge per pulse stays fixed. In the closer pair, the second pulse arrives while much of the first voltage response remains.

```python
sample = np.arange(1000) * 0.1
for separation_ms in [6.0, 40.0]:  # edit these separations
    current = pulse_train(sample, [20, 20 + separation_ms],
                          width_ms=4, amplitude_pa=600)
    t, v, spikes = simulate_lif(current)
    print(separation_ms, "ms separation:", len(spikes), "spikes")
    plt.plot(t, v, label=f"Separation = {separation_ms:g} ms")
plt.axhline(-50, ls="--", color="gray")
plt.xlabel("Time (ms)"); plt.ylabel("Voltage (mV)")
plt.legend(); plt.show()
```

**Reference result.** A single pulse raises the passive voltage by $60(1-e^{-4/20})\approx10.88$ mV. At the end of the second pulse, the passive shift is approximately $10.88(1+e^{-\Delta/20})$ mV for nonoverlapping pulses with onset separation $\Delta$. It is about 18.93 mV at 6 ms, exceeding the 15 mV distance to threshold, versus 12.35 mV at 40 ms. The LIF model therefore emits one event for the close pair and none for the separated pair. The passive prediction continues above threshold only when reset is disabled.

**Try:** change separation to 12 or 20 ms, then change capacitance to 400 pF. Predict again: capacitance changes both voltage rise during a finite pulse and decay between pulses. If the separation is less than 4 ms, the pulses overlap and their currents add.

```{figure} ../assets/lif-temporal-integration.png
:label: fig-lif-temporal-integration
:alt: Identical paired current pulses with 6 ms and 40 ms onset separation, showing one versus zero LIF spikes and the corresponding passive RC predictions
:width: 100%

**Example 3 reference output.** Top: LIF reset trace and passive RC prediction without reset. Bottom: identical-charge input pulses at different separations. Matching voltage and current scales support comparison.
```

### 3.5.5 Example 4 — Spatial integration: different input sources

At the point-neuron level, spatial summation means combining **distinct input sources** into the same compartment. Write their current contributions as

$$
I_{\mathrm{total}}[n]=\sum_j w_j I_j[n].
$$

Here $I_j$ is a prescribed current waveform in pA and $w_j$ is a dimensionless, fixed weight. A and B each deliver 250 pA for 8 ms; a third channel delivers −150 pA at the same time.

```python
sample = np.arange(800) * 0.1
a = pulse_train(sample, [30], width_ms=8, amplitude_pa=250)
b = pulse_train(sample, [30], width_ms=8, amplitude_pa=250)
negative = pulse_train(sample, [30], width_ms=8, amplitude_pa=-150)
weight_b = 1.0  # try 0.0, 0.5, 1.0, 1.5
for label, current in [("A only", a), ("A + B", a + weight_b * b),
                       ("A + B + negative current", a + weight_b * b + negative)]:
    t, v, spikes = simulate_lif(current)
    print(label, ":", len(spikes), "spikes")
    plt.plot(t, v, label=label)
plt.axhline(-50, ls="--", color="gray")
plt.xlabel("Time (ms)"); plt.ylabel("Voltage (mV)")
plt.legend(); plt.show()
```

**Reference result.** One channel produces a passive peak shift of $25(1-e^{-8/20})\approx8.24$ mV. Two synchronous channels produce about 16.48 mV and cross threshold. Adding the negative current gives 350 pA total, with a passive shift of about 11.54 mV, below threshold. The respective LIF event counts are **0, 1, and 0**.

**Try:** delay B by changing its onset from 30 to 40 ms, or vary `weight_b`. Explain why multiple sources still require favorable timing. The notebook keeps each source in a separate array and combines them with a weight vector so that the origin of every contribution remains visible.

```{figure} ../assets/lif-spatial-integration.png
:label: fig-lif-spatial-integration
:alt: One current channel, two synchronous channels, and two channels plus a negative input, with LIF voltage and passive RC predictions above total-current plots
:width: 100%

**Example 4 reference output.** Two individually subthreshold input channels can jointly trigger an event. A simultaneous negative current prevents that event in the stated example. All three conditions use the same membrane parameters.
```

**Scope of the example.** A single-compartment LIF model has no dendritic coordinates: it cannot predict the difference between a distal and proximal synapse or branch-specific nonlinear integration. Those questions need cable or multicompartment models [[1]](#models-ref-1), secs. 1.4.4, 3.2, and 3.4. Also, a negative prescribed current is an inhibitory *approximation*: it does not implement conductance-dependent shunting, changing input resistance, or a reversal potential. The [conductance example in Chapter 1](01-neuroscience-background.md#fig-conductance-balance) explains that distinction. Passive voltage shifts superpose before threshold/reset; full spike-output responses need not superpose.

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

This example adds a useful comparison: Hodgkin–Huxley describes explicit channel-gating variables; a two-variable reduction emphasizes excitation and recovery; LIF uses a passive voltage equation with discrete threshold/reset events. A reduced model can clarify qualitative behavior while leaving channel-specific questions unanswered. The present executable laboratory implements the four LIF/RC worked examples; no FitzHugh–Nagumo implementation is claimed here.

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
