"""Reproduce Chapter 2's original RC diagram, worked plots, and LIF notebook.

Run from any directory: python tools/build_lif_examples.py
The notebook embeds all simulation code; Colab needs no repository imports.
"""
from pathlib import Path
import textwrap
import inspect
import nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'path'})

MODEL = r'''
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

def analytical_rate(current_pa, capacitance_pf=200.0, leak_ns=10.0,
                    rest_mv=-65.0, threshold_mv=-50.0, reset_mv=-65.0,
                    refractory_ms=2.0):
    steady_mv = rest_mv + current_pa / leak_ns
    if steady_mv <= threshold_mv:
        return 0.0
    crossing_ms = (capacitance_pf / leak_ns) * np.log(
        (steady_mv - reset_mv) / (steady_mv - threshold_mv))
    return 1000.0 / (crossing_ms + refractory_ms)

def plot_response(ax, time, voltage, spikes, label, color, threshold=-50.0):
    ax.plot(time, voltage, color=color, label=label, lw=1.8)
    if len(spikes):
        ax.vlines(spikes, threshold + 0.7, threshold + 3.0, color=color, lw=1.5)
    ax.axhline(threshold, color='0.55', ls='--', lw=0.9)
    ax.set(xlabel='Time (ms)', ylabel='Voltage (mV)')
'''

PARAMETERS = r'''
# EDIT these numbers, then rerun this cell and Example 1.
dt_ms = 0.1
duration_ms = 500.0
current_pa = 200.0
capacitance_pf = 200.0
leak_ns = 10.0
threshold_mv = -50.0
refractory_ms = 2.0
parameters = dict(dt_ms=dt_ms, capacitance_pf=capacitance_pf,
                  leak_ns=leak_ns, threshold_mv=threshold_mv,
                  refractory_ms=refractory_ms)
print(f'R = {1000 / leak_ns:.1f} MΩ; tau = {capacitance_pf / leak_ns:.1f} ms')
'''

EXAMPLE1 = r'''
current = np.full(round(duration_ms / dt_ms), current_pa)
time, voltage, spikes = simulate_lif(current, **parameters)
rate = 0.0 if len(spikes) < 2 else 1000.0 / np.diff(spikes).mean()
print(f'{len(spikes)} spikes in {duration_ms:g} ms; interval-based rate = {rate:.2f} Hz')
fig, axes = plt.subplots(1, 2, figsize=(11, 4.1), constrained_layout=True)
plot_response(axes[0], time, voltage, spikes, 'Voltage / spike events', '#24628a', threshold_mv)
axes[0].set(xlim=(0, min(160, duration_ms)), title='A. Change the parameters above')
axes[0].legend(fontsize=8, loc='lower right')
currents = np.linspace(80, 300, 23)
simulated = []
for value in currents:
    _, _, events = simulate_lif(np.full(round(2000 / dt_ms), value), **parameters)
    simulated.append(0.0 if len(events) < 2 else 1000 / np.diff(events).mean())
expected = [analytical_rate(i, **{k: v for k, v in parameters.items() if k != 'dt_ms'})
            for i in currents]
axes[1].plot(currents, expected, color='#24628a', label='Analytical')
axes[1].plot(currents, simulated, 'o', ms=3.5, color='#b6483b', label='Simulated')
axes[1].set(xlabel='Current (pA)', ylabel='Steady firing rate (Hz)', title='B. Current–rate relation')
axes[1].legend(fontsize=9)
plt.show()
'''

RC_EXAMPLE = r'''
# Compare capacitance while keeping resistance and current fixed.
dt_rc = 0.1
sample_rc = np.arange(1000) * dt_rc
step_current = pulse_train(sample_rc, [10], width_ms=80, amplitude_pa=100)
fig, axes = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
for cap, color in [(100, '#b6483b'), (200, '#24628a'), (400, '#268471')]:
    t, v, _ = simulate_lif(step_current, dt_ms=dt_rc, capacitance_pf=cap,
                          spiking=False)
    axes[0].plot(t, v, color=color, label=f'C = {cap} pF; tau = {cap / 10:g} ms')
axes[0].set(xlabel='Time (ms)', ylabel='Voltage (mV)', title='A. Larger C charges more slowly')
axes[0].legend(fontsize=9)
axes[1].step(sample_rc, step_current, where='post', color='#24628a')
axes[1].set(xlabel='Time (ms)', ylabel='Applied current (pA)', title='B. Same 100 pA input')
plt.show()
'''

TEMPORAL = r'''
# EDIT separation_ms (6 -> 40), pulse_pa, or capacitance_pf here.
separation_ms = 6.0
pulse_pa = 600.0
temporal_capacitance_pf = 200.0
sample = np.arange(1000) * 0.1
fig, axes = plt.subplots(2, 2, figsize=(11, 6), sharex=True, constrained_layout=True)
for column, separation in enumerate([separation_ms, 40.0]):
    current = pulse_train(sample, [20, 20 + separation], width_ms=4,
                          amplitude_pa=pulse_pa)
    t, v, events = simulate_lif(current, capacitance_pf=temporal_capacitance_pf)
    _, passive, _ = simulate_lif(current, capacitance_pf=temporal_capacitance_pf,
                                  spiking=False)
    plot_response(axes[0, column], t, v, events, 'LIF + events', '#24628a')
    axes[0, column].plot(t, passive, ':', color='#b6483b', label='Passive RC, no reset')
    axes[0, column].set(title=f'Onset separation = {separation:g} ms; spikes = {len(events)}', ylim=(-66, -43))
    axes[0, column].legend(fontsize=8, loc='lower right')
    axes[1, column].step(sample, current, where='post', color='#24628a')
    axes[1, column].set(xlabel='Time (ms)', ylabel='Input current (pA)', xlim=(0, 100), ylim=(-20, 650))
plt.show()
'''

SPATIAL = r'''
# Separate rows are different input sources, all reaching one compartment.
# EDIT weight_b, delay_b_ms, or inhibitory_pa; the other examples stay fixed.
weight_b = 1.0
delay_b_ms = 0.0
inhibitory_pa = -150.0
sample = np.arange(800) * 0.1
source_a = pulse_train(sample, [30], width_ms=8, amplitude_pa=250)
source_b = pulse_train(sample, [30 + delay_b_ms], width_ms=8, amplitude_pa=250)
source_i = pulse_train(sample, [30], width_ms=8, amplitude_pa=inhibitory_pa)
channels = np.vstack([source_a, source_b, source_i])
cases = [('A only', np.array([1., 0., 0.])),
         ('A + B', np.array([1., weight_b, 0.])),
         ('A + B + negative current', np.array([1., weight_b, 1.]))]
fig, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, constrained_layout=True)
for col, (label, weights) in enumerate(cases):
    current = weights @ channels
    t, v, events = simulate_lif(current)
    _, passive, _ = simulate_lif(current, spiking=False)
    plot_response(axes[0, col], t, v, events, 'LIF + events', '#24628a')
    axes[0, col].plot(t, passive, ':', color='#b6483b', label='Passive RC')
    axes[0, col].set(title=f'{label}\nspikes = {len(events)}', ylim=(-66, -44))
    axes[0, col].legend(fontsize=8, loc='lower right')
    axes[1, col].step(sample, current, where='post', color='#24628a')
    axes[1, col].set(xlabel='Time (ms)', ylabel='Total current (pA)', xlim=(15, 65), ylim=(-20, 550))
plt.show()
'''

CHECKS = r'''
# Reference checks use explicit defaults, independent of your editable cells.
_, zero_v, zero_events = simulate_lif(np.zeros(1000))
assert np.allclose(zero_v, -65) and len(zero_events) == 0
_, _, low = simulate_lif(np.full(5000, 100.0))
assert len(low) == 0
crossing = 20 * np.log(4)
_, _, coarse = simulate_lif(np.full(5000, 200.0))
_, _, fine = simulate_lif(np.full(10000, 200.0), dt_ms=0.05)
assert abs(coarse[0] - crossing) <= 0.1
assert abs(fine[0] - crossing) <= abs(coarse[0] - crossing) + 1e-10
assert abs(np.diff(fine).mean() - (crossing + 2)) <= 0.05
_, _, slower = simulate_lif(np.full(10000, 200.0), capacitance_pf=400)
assert abs(slower[0] - 2 * crossing) <= 0.1
rate_errors = []
for drive in np.linspace(80, 300, 23):
    _, _, events = simulate_lif(np.full(20000, drive))
    measured = 0.0 if len(events) < 2 else 1000 / np.diff(events).mean()
    rate_errors.append(abs(measured - analytical_rate(drive)))
assert max(rate_errors) < 0.6
# A passive step should agree with the analytical RC charging curve.
t, v, _ = simulate_lif(np.full(1000, 100.0), spiking=False)
assert np.allclose(v, -55 + (-65 + 55) * np.exp(-t / 20))
sample = np.arange(1000) * 0.1
assert len(simulate_lif(pulse_train(sample, [20, 26]))[2]) == 1
assert len(simulate_lif(pulse_train(sample, [20, 60]))[2]) == 0
a = pulse_train(sample, [30], width_ms=8, amplitude_pa=250)
negative = pulse_train(sample, [30], width_ms=8, amplitude_pa=-150)
assert len(simulate_lif(a)[2]) == 0
assert len(simulate_lif(2 * a)[2]) == 1
assert len(simulate_lif(2 * a + negative)[2]) == 0
# Superposition applies to passive voltage shifts, before threshold/reset.
_, va, _ = simulate_lif(a, spiking=False)
_, vab, _ = simulate_lif(2 * a, spiking=False)
assert np.allclose(vab + 65, 2 * (va + 65))
print('Passed: baseline, analytical RC, spike timing, step refinement, temporal and multisource integration.')
print(f'Default first spike: {coarse[0]:.2f} ms; analytical: {crossing:.5f} ms')
print(f'Default interval rate: {1000 / np.diff(coarse).mean():.2f} Hz; analytical: {analytical_rate(200):.2f} Hz')
'''

def markdown(text):
    return nbformat.v4.new_markdown_cell(inspect.cleandoc(text))

def code(text):
    return nbformat.v4.new_code_cell(textwrap.dedent(text).strip())

def build_notebook_and_plots():
    nb = nbformat.v4.new_notebook(cells=[
        markdown(r'''# Laboratory 1 — Leaky Integrate-and-Fire Neuron

        Four worked examples accompany Chapter 2: current/rate, RC charging,
        temporal integration, and multisource integration. **Run all cells once.
        Then edit one parameter cell and rerun its example.** Code is self-contained
        and uses NumPy and Matplotlib (available in Colab). All values are teaching
        assumptions, not fitted biological measurements.

        [Run in Google Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/lif_neuron.ipynb)

        Units: pA, mV, pF, nS, ms. Stored voltage resets at spike detection;
        short vertical markers indicate separate spike events, not ionic waveforms.
        The dotted curves in integration plots show the passive RC prediction
        with threshold and reset disabled.'''),
        markdown(r'''## 1. Model and plotting helpers

        A current array specifies one value per interval. The returned voltage
        includes the initial state, so it is one sample longer. The exponential
        step is exact for a constant current within an interval; threshold detection
        is at interval endpoints. Refractory duration rounds upward to a full step.
        Use smaller steps to check timing convergence.'''), code(MODEL),
        markdown(r'''## 2. Example 1 — Change one neuron parameter

        Predict first, then run. At the defaults, $R_m=100$ MΩ, $\tau_m=20$ ms,
        first crossing is 27.73 ms, and the long-run rate is about 33.64 Hz.
        Try current 100/200/300 pA; capacitance 100/200/400 pF; leak 5/10/20 nS;
        threshold −55/−50/−45 mV; refractory 0/2/5 ms.
        Change one value at a time. Capacitance changes timing without changing
        the passive steady voltage; changing leak changes both.'''),
        code(PARAMETERS), code(EXAMPLE1),
        markdown(r'''## 3. Example 2 — Charge the membrane capacitor

        The 100 pA step has a passive equilibrium of −55 mV at 10 nS leak.
        Different capacitances approach the **same** equilibrium at different rates.
        At one time constant after onset, the voltage completes about 63.2% of its
        final shift. No threshold/reset is applied in this RC-only example.
        Edit the capacitance list and the pulse amplitude or width.'''), code(RC_EXAMPLE),
        markdown(r'''## 4. Example 3 — Temporal integration

        The same input source sends two 600 pA, 4 ms pulses. At 6 ms onset
        separation (2 ms quiet gap), their residual voltages combine and trigger
        one event; at 40 ms separation, neither pulse triggers an event.
        Pulse charge is unchanged. Only arrival timing differs.
        Try separation 6/12/20/40 ms, then change capacitance.
        If pulses overlap, their currents add: that is a different stimulus.'''), code(TEMPORAL),
        markdown(r'''## 5. Example 4 — Multiple sources: point-neuron spatial summation

        A and B are distinct presynaptic input channels, each 250 pA for 8 ms.
        One channel alone is subthreshold; their synchronous sum triggers one
        event. Adding −150 pA during the pulse prevents that event at defaults.
        Change B's weight or delay and observe coincidence sensitivity.

        This is **multisource summation into one isopotential compartment**.
        It does not model synaptic positions, dendritic distance, or cable filtering.
        Negative current is a current-based inhibitory approximation; it does not
        implement conductance-dependent shunting or an inhibitory reversal potential.
        The weights are fixed inputs to this experiment, not learned synaptic weights.'''),
        code(SPATIAL), markdown(r'''## 6. Reference checks

        These checks always use the documented baseline values, independently
        of your edits. They test numerical behavior, not biological validity.'''), code(CHECKS),
        markdown(r'''## Explain what changed

        For each example, record the parameter value and unit, a prediction,
        the voltage/input plot, spike count or first-spike time, and an explanation
        in terms of charge, leak, time constant, and threshold. These are guided
        worked examples; the chapter exercises ask you to transfer the ideas.

        ## References

        [1] Wulfram Gerstner, Werner M. Kistler, Richard Naud, and Liam Paninski,
        *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*.
        Cambridge, U.K.: Cambridge University Press, 2014, secs. 1.3–1.4.
        [RC circuit and integration](https://neuronaldynamics.epfl.ch/online/Ch1.S3.html);
        [limitations](https://neuronaldynamics.epfl.ch/online/Ch1.S4.html).
        Circuit and plots in this textbook are original teaching illustrations.''')
    ])
    nb.metadata.kernelspec = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
    nb.metadata.language_info = {'name': 'python'}
    nb.metadata.myst = {'downloads': [
        {'file': 'lif_neuron.ipynb', 'title': 'Download this notebook'},
        {'url': 'https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/lif_neuron.ipynb', 'title': 'Run in Google Colab'}]}
    nbformat.write(nb, ROOT / 'notebooks/lif_neuron.ipynb')
    scope = {}
    original_show = plt.show
    plt.show = lambda: None
    try:
        exec(MODEL, scope)
        exec(PARAMETERS, scope)
        for filename, source in [('lif-neuron-model.png', EXAMPLE1),
                                 ('lif-rc-charging.png', RC_EXAMPLE),
                                 ('lif-temporal-integration.png', TEMPORAL),
                                 ('lif-spatial-integration.png', SPATIAL)]:
            exec(source, scope)
            scope['fig'].savefig(ASSETS / filename, dpi=180, facecolor='white')
            plt.close('all')
        exec(CHECKS, scope)
    finally:
        plt.show = original_show

def build_circuit():
    fig, ax = plt.subplots(figsize=(12, 6.4))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.03, top=0.97)
    ax.set(xlim=(0, 12), ylim=(0, 6.4))
    ax.axis('off')
    ink, blue, coral = '#193746', '#24628a', '#b75d45'
    def wire(xs, ys, **kwargs):
        ax.plot(xs, ys, color=ink, lw=2, **kwargs)
    def label(x, y, text, size=12, **kwargs):
        ax.text(x, y, text, color=ink, fontsize=size, **kwargs)
    label(0.3, 6.0, 'LIF: a passive RC membrane + a threshold/reset rule', 18, weight='bold')
    label(0.3, 5.6, 'Equivalent membrane circuit', 14, weight='bold')
    wire([1.1, 6.1], [4.8, 4.8]); wire([1.1, 6.1], [1.2, 1.2])
    # Input source, upward-positive current.
    wire([1.1, 1.1], [4.8, 3.5]); wire([1.1, 1.1], [2.6, 1.2])
    ax.add_patch(Circle((1.1, 3.05), .45, fill=False, ec=blue, lw=2))
    ax.annotate('', xy=(1.1, 3.36), xytext=(1.1, 2.76),
                arrowprops={'arrowstyle': '-|>', 'color': blue, 'lw': 2})
    label(.35, 3.9, r'$I(t)$', 16)
    label(.05, 2.1, 'Input current', 11)
    # Membrane capacitor (not an input capacitor).
    wire([3.25, 3.25], [4.8, 3.25]); wire([3.25, 3.25], [2.95, 1.2])
    wire([2.75, 3.75], [3.25, 3.25]); wire([2.75, 3.75], [2.95, 2.95])
    label(3.9, 3.35, r'$C_m$', 16); label(3.9, 2.94, '200 pF', 11)
    # Leak resistor in series with a signed reversal-potential source.
    wire([5.6, 5.6], [4.8, 4.05])
    zig_y = np.linspace(4.05, 2.9, 9)
    zig_x = [5.6] + [5.6 + (.18 if k % 2 else -.18) for k in range(1, 8)] + [5.6]
    wire(zig_x, zig_y)
    wire([5.6, 5.6], [2.9, 2.35]); wire([5.6, 5.6], [1.55, 1.2])
    ax.add_patch(Circle((5.6, 1.95), .4, fill=False, ec=ink, lw=2))
    label(5.6, 2.03, '+', 15, ha='center'); label(5.6, 1.69, '−', 15, ha='center')
    label(6.0, 3.75, r'$R_m=1/g_L$', 14)
    label(6.0, 3.35, r'$100\ \mathrm{M}\Omega$', 12)
    label(6.12, 2.08, r'$E_L=-65\ \mathrm{mV}$', 12)
    label(6.12, 1.72, 'Signed reversal source', 9)
    # Common extracellular reference.
    wire([3.25, 3.25], [1.2, .94])
    for y, half in [(.94, .30), (.81, .20), (.68, .10)]:
        wire([3.25 - half, 3.25 + half], [y, y])
    label(.3, .3, 'Bottom rail: extracellular reference (0 mV)', 11)
    ax.plot(3.25, 4.8, 'o', color=ink, ms=6)
    label(3.35, 4.98, r'$V(t)$  (inside relative to outside)', 12)
    # Dashed sensing signal to an abstract algorithm block, not another current branch.
    ax.annotate('', xy=(8.3, 4.8), xytext=(6.1, 4.8),
                arrowprops={'arrowstyle': '->', 'linestyle': '--', 'color': coral, 'lw': 1.8})
    ax.add_patch(FancyBboxPatch((8.35, 2.8), 3.25, 2.55, boxstyle='round,pad=0.12',
                              fc='#f7f2ee', ec='#ddcfc5', lw=1.3))
    label(8.58, 4.92, 'Abstract event rule', 14, weight='bold')
    label(8.58, 4.38, r'If $V\geq V_{\mathrm{th}}$:', 14)
    label(8.58, 3.94, 'record a spike time', 12)
    label(8.58, 3.50, r'$V\leftarrow V_{\mathrm{reset}}$', 14)
    label(8.58, 3.05, r'hold for $t_{\mathrm{ref}}$', 12)
    label(8.4, 2.35, 'Threshold/reset is added to RC.', 11)
    label(8.4, 1.98, 'R and C alone do not generate spikes.', 10)
    label(8.4, 1.25, r'$\tau_m=R_m C_m=20\ \mathrm{ms}$', 16)
    fig.savefig(ASSETS / 'lif-rc-circuit.svg', facecolor='white')
    plt.close(fig)

if __name__ == '__main__':
    build_notebook_and_plots()
    build_circuit()
    print('Generated the self-contained LIF notebook, four plots, and original RC schematic.')
