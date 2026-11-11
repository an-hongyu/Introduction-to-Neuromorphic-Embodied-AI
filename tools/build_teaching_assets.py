"""Reproduce original textbook diagrams and the two introductory notebooks."""
from pathlib import Path
import textwrap
import nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.titlesize': 11, 'figure.dpi': 140})

lif_code = r'''
import numpy as np
import matplotlib.pyplot as plt

def simulate_lif(current_pa=200.0, duration_ms=500.0, dt_ms=0.1):
    tau_ms, leak_ns, rest_mv = 20.0, 10.0, -65.0
    threshold_mv, reset_mv, refractory_ms = -50.0, -65.0, 2.0
    voltage, hold_steps = reset_mv, 0
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

def analytical_rate(current_pa):
    steady_mv = -65.0 + current_pa / 10.0
    if steady_mv <= -50.0:
        return 0.0
    crossing_ms = 20.0 * np.log((steady_mv + 65.0) / (steady_mv + 50.0))
    return 1000.0 / (crossing_ms + 2.0)

trace, spikes = simulate_lif()
assert len(spikes) > 2
assert abs(spikes[0] - 20.0 * np.log(4.0)) <= 0.11
assert len(simulate_lif(100.0)[1]) == 0
_, fine_spikes = simulate_lif(dt_ms=0.05)
assert abs(np.diff(fine_spikes).mean() - (20 * np.log(4) + 2)) <= 0.11
print('Analytical rate at 200 pA: %.2f Hz' % analytical_rate(200.0))
print('Simulated rate at 200 pA: %.2f Hz' % (1000 / np.diff(spikes).mean()))
'''
lif_plot = r'''
currents = np.linspace(80.0, 300.0, 23)
simulated = []
for current in currents:
    _, events = simulate_lif(current_pa=current, duration_ms=2000.0)
    simulated.append(0.0 if len(events) < 2 else 1000.0 / np.diff(events).mean())
expected = np.array([analytical_rate(i) for i in currents])
assert np.max(np.abs(np.array(simulated) - expected)) < 0.6
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), constrained_layout=True)
time_ms = (np.arange(len(trace)) + 1) * 0.1
axes[0].plot(time_ms, trace, color='#24628a', label='Reset voltage trace')
axes[0].vlines(spikes[spikes <= 160], -49, -44, color='#b6483b', label='Spike events')
axes[0].axhline(-50, ls='--', color='0.5', lw=1, label='Threshold')
axes[0].set(xlim=(0, 160), ylim=(-67, -41), xlabel='Time (ms)', ylabel='Voltage (mV)', title='A. LIF at 200 pA')
axes[0].legend(fontsize=8, loc='lower right')
axes[1].plot(currents, expected, '-', color='#24628a', label='Analytical')
axes[1].plot(currents, simulated, 'o', ms=4, color='#b6483b', label='Simulated, step = 0.1 ms')
axes[1].set(xlabel='Current (pA)', ylabel='Steady firing rate (Hz)', title='B. Constant-input response')
axes[1].legend(fontsize=8)
plt.show()
'''
hebb_code = r'''
import numpy as np
import matplotlib.pyplot as plt
patterns = np.array([[1., 1., 0.], [0., 1., 1.]])
paired_outputs = np.eye(2)
weights = np.zeros((2, 3))
for _ in range(8):
    for x, y in zip(patterns, paired_outputs):
        weights += 0.1 * np.outer(y, x)
cues = np.array([[1., 0., 0.], [0., 0., 1.], [0., 1., 0.]])
scores = cues @ weights.T
assert np.allclose(weights, [[0.8, 0.8, 0], [0, 0.8, 0.8]])
assert np.allclose(scores, [[0.8, 0], [0, 0.8], [0.8, 0.8]])
print('Weights (output rows, input columns):\n', weights)
print('Partial-cue output scores:\n', scores)
print('The shared-feature cue is ambiguous; these are not probabilities.')

def pair_stdp(delta_ms, a_plus=0.01, a_minus=0.012, tau_ms=20.0):
    delta_ms = np.asarray(delta_ms, dtype=float)
    return np.where(delta_ms > 0, a_plus * np.exp(-delta_ms / tau_ms),
                    np.where(delta_ms < 0, -a_minus * np.exp(delta_ms / tau_ms), 0.0))
assert np.isclose(pair_stdp(10), 0.01 * np.exp(-0.5))
assert pair_stdp(-10) < 0 and pair_stdp(0) == 0
'''
hebb_plot = r'''
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), constrained_layout=True)
im = axes[0].imshow(weights, vmin=0, vmax=0.8, cmap='Blues')
axes[0].set(xticks=[0, 1, 2], xticklabels=['Feature 1', 'Shared', 'Feature 3'],
            yticks=[0, 1], yticklabels=['Output 1', 'Output 2'], title='A. Paired-pattern weights')
for row in range(2):
    for col in range(3):
        axes[0].text(col, row, '%.1f' % weights[row, col], ha='center', va='center',
                     color='white' if weights[row, col] > 0.4 else '#17334c')
fig.colorbar(im, ax=axes[0], shrink=0.7, label='Weight (a.u.)')
x = np.arange(3)
axes[1].bar(x - 0.18, scores[:, 0], 0.36, label='Output 1', color='#24628a')
axes[1].bar(x + 0.18, scores[:, 1], 0.36, label='Output 2', color='#d08a35')
axes[1].set(xticks=x, xticklabels=['Feature 1', 'Feature 3', 'Shared'], ylim=(0, 1),
            ylabel='Output score (a.u.)', title='B. Partial-cue recall')
axes[1].legend(fontsize=8)
delta = np.linspace(-80, 80, 801)
for mask, color in [(delta < 0, '#b6483b'), (delta > 0, '#268471')]:
    axes[2].plot(delta[mask], pair_stdp(delta[mask]), color=color)
axes[2].scatter([0], [0], color='0.3', s=15, zorder=3)
axes[2].axhline(0, color='0.6', lw=0.7)
axes[2].axvline(0, color='0.6', lw=0.7)
axes[2].set(xlabel='Post minus pre spike time (ms)', ylabel='Weight change (a.u.)',
            title='C. Illustrative STDP window')
plt.show()
'''

for name, title, intro, code, plot in [
    ('lif_neuron', 'Laboratory 1 — Leaky Integrate-and-Fire Neuron',
     'Companion to Chapter 3. All currents use pA, voltages mV, conductances nS, and time ms. The model uses an exact passive step and endpoint spike detection. Run all cells to reproduce the checks and figure. Parameters are pedagogical, not fitted to a biological recording.', lif_code, lif_plot),
    ('hebbian_learning', 'Laboratory 3 — Hebbian Association and STDP',
     'Companion to Chapter 4. This controlled pairing example uses dimensionless activities and supplied output patterns. It demonstrates partial-cue recall and ambiguity, not autonomous learning. The STDP window is illustrated separately and does not train the association matrix.', hebb_code, hebb_plot),
]:
    nb = nbformat.v4.new_notebook(cells=[
        nbformat.v4.new_markdown_cell('# ' + title + '\n\n' + intro + '\n\n[Run in Google Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/' + name + '.ipynb)'),
        nbformat.v4.new_code_cell(textwrap.dedent(code).strip()),
        nbformat.v4.new_code_cell(textwrap.dedent(plot).strip()),
        nbformat.v4.new_markdown_cell('## Experiments\n\n' +
            ('1. Halve the time step and compare spike intervals.\n2. Double membrane capacitance with conductance fixed.\n3. Compare current-based input with a conductance-based extension.\n\n## References\n\n[1] W. Gerstner, W. M. Kistler, R. Naud, and L. Paninski, *Neuronal Dynamics*, Cambridge University Press, 2014. [Online textbook](https://neuronaldynamics.epfl.ch/online/).' if name == 'lif_neuron' else
             '1. Compare scores before and after pairing.\n2. Shuffle the output pairings and compare recall.\n3. Add overlapping patterns and measure interference.\n4. Change the STDP time constant and inspect the timing window.\n\n## References\n\n[1] D. O. Hebb, *The Organization of Behavior*, Wiley, 1949. [Catalog record](https://wellcomecollection.org/works/g4sfzum4).\n\n[2] G.-Q. Bi and M.-M. Poo, “Synaptic modifications in cultured hippocampal neurons: Dependence on spike timing, synaptic strength, and postsynaptic cell type,” *J. Neurosci.*, vol. 18, no. 24, pp. 10464–10472, 1998. [DOI](https://pubmed.ncbi.nlm.nih.gov/9852584/).'))
    ])
    nb.metadata.kernelspec = {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}
    nb.metadata.language_info = {'name': 'python'}
    # Downloads are notebook-specific; do not inherit the Place Cell download.
    nb.metadata.myst = {'downloads': [
        {'file': name + '.ipynb', 'title': 'Download this notebook'},
        {'url': 'https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/' + name + '.ipynb', 'title': 'Run in Google Colab'}]}
    nbformat.write(nb, ROOT / 'notebooks' / (name + '.ipynb'))
    namespace = {}
    exec(code, namespace)
    original_show = plt.show
    plt.show = lambda: None
    exec(plot, namespace)
    filename = 'lif-neuron-model.png' if name == 'lif_neuron' else 'hebbian-learning.png'
    namespace['fig'].savefig(ASSETS / filename, dpi=160, facecolor='white')
    plt.close('all')
    plt.show = original_show

coord = np.linspace(0, 1, 160)
X, Y = np.meshgrid(coord, coord)
place = 0.2 + 24.8 * np.exp(-((X-.55)**2+(Y-.48)**2)/(2*.14**2))
k = 2 * np.pi / .28
waves = sum(np.cos(k * (X*np.cos(a) + Y*np.sin(a))) for a in [0, np.pi/3, 2*np.pi/3])
grid = 25 * np.maximum(waves / 3, 0)**2
boundary = 25 * np.exp(-X**2 / (2 * .07**2))
fig, axes = plt.subplots(2, 3, figsize=(11, 6.6), constrained_layout=True)
for ax, field, title in [(axes[0,0],place,'A. Place-like field'),(axes[0,1],grid,'B. Grid-like field'),(axes[1,0],boundary,'D. West-boundary field')]:
    im = ax.imshow(field, origin='lower', extent=(0,1,0,1), vmin=0, vmax=25, cmap='inferno')
    ax.set(xlabel='x (m)', ylabel='y (m)', title=title)
    fig.colorbar(im, ax=ax, label='Rate (Hz)', shrink=.7)
theta = np.linspace(0, 360, 361)
axes[0,2].plot(theta, .2+24.8*np.exp(3*(np.cos(np.deg2rad(theta-90))-1)), color='#24628a')
axes[0,2].set(xlabel='Heading (degrees)', ylabel='Rate (Hz)', title='C. Heading tuning', xlim=(0,360), xticks=[0,90,180,270,360])
speed = np.linspace(0,.4,100)
axes[1,1].plot(speed, 2+50*speed, color='#268471')
axes[1,1].set(xlabel='Speed (m/s)', ylabel='Rate (Hz)', title='E. Speed-related tuning')
time = np.linspace(0,10,300)
for center in [2,5,8]:axes[1,2].plot(time, 20*np.exp(-(time-center)**2/(2*.7**2)))
axes[1,2].set(xlabel='Elapsed time (s)', ylabel='Rate (Hz)', title='F. Three time-related fields')
fig.savefig(ASSETS/'spatial-cell-tuning.png', dpi=160, facecolor='white')
plt.close(fig)

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 510" role="img" aria-labelledby="title desc">
<title id="title">Neuron structure and chemical synaptic transmission</title>
<desc id="desc">An original schematic of a neuron with dendrites, soma, initial segment and axon, followed by a chemical synapse inset with calcium entry, transmitter vesicles and receptors.</desc>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0 0L0 6L8 3Z" fill="#bc593c"/></marker></defs>
<rect width="1100" height="510" rx="18" fill="#f4f8fb"/>
<g font-family="Arial,sans-serif" fill="#18364c"><text x="30" y="38" font-size="23" font-weight="bold">A. Neuron: receive, integrate, and transmit</text>
<g stroke="#266b8c" stroke-width="8" fill="none" stroke-linecap="round"><path d="M210 205L140 140L90 135M140 140L135 92M210 205L125 215L60 185M125 215L80 250M210 205L170 280L115 305M170 280L190 330"/></g>
<ellipse cx="250" cy="205" rx="59" ry="49" fill="#c8e1ee" stroke="#266b8c" stroke-width="4"/><circle cx="250" cy="205" r="17" fill="#83b4cd"/>
<path d="M310 205L750 205M750 205L815 140M750 205L825 205M750 205L815 270" fill="none" stroke="#266b8c" stroke-width="8" stroke-linecap="round"/>
<g fill="#266b8c"><circle cx="818" cy="138" r="11"/><circle cx="828" cy="205" r="11"/><circle cx="818" cy="272" r="11"/></g>
<g font-size="18"><text x="45" y="75">Dendrites</text><text x="218" y="285">Soma</text><text x="320" y="262">Initial segment</text><text x="550" y="250">Axon</text><text x="805" y="104">Terminals</text></g>
<path d="M390 165L690 165" stroke="#bc593c" stroke-width="3" marker-end="url(#arrow)"/>
<text x="435" y="145" font-size="17" fill="#96462f">Spike propagation</text>
<path d="M830 280L900 305" stroke="#6f8795" stroke-width="2" stroke-dasharray="5 5"/>
<rect x="35" y="350" width="1030" height="130" rx="12" fill="white" stroke="#cad9e3"/>
<text x="52" y="378" font-size="20" font-weight="bold">B. Chemical synapse (enlarged schematic)</text>
<rect x="410" y="394" width="190" height="35" rx="9" fill="#c8e1ee" stroke="#266b8c" stroke-width="2"/>
<rect x="410" y="452" width="190" height="16" rx="5" fill="#d4e6d8" stroke="#44846a" stroke-width="2"/>
<g fill="#bc593c"><circle cx="455" cy="408" r="7"/><circle cx="480" cy="408" r="7"/><circle cx="505" cy="408" r="7"/><circle cx="475" cy="438" r="3"/><circle cx="493" cy="440" r="3"/><circle cx="510" cy="436" r="3"/></g>
<g stroke="#44846a" stroke-width="5"><path d="M470 447v17M495 447v17M520 447v17"/></g>
<g font-size="16"><text x="52" y="413">Presynaptic spike → calcium entry</text><text x="650" y="414">Vesicles release transmitter</text><text x="650" y="445">Cleft → postsynaptic receptors</text><text x="52" y="458">Receptor activation changes postsynaptic state</text></g>
</g></svg>'''
(ASSETS/'neuron-synapse.svg').write_text(svg)
print('Generated four original teaching figures and two executable notebooks.')
