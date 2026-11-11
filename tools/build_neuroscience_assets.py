"""Generate original illustrations for the neuroscience foundation chapter."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
REST, THRESHOLD, TAU = -65., -55., 20.
time = np.linspace(0, 105, 2101)

def kernel(event_ms, amplitude_mv=6.):
    elapsed = time - event_ms
    return np.where(elapsed >= 0, amplitude_mv * np.exp(-np.maximum(elapsed, 0) / TAU), 0.)

plt.rcParams.update({'font.size': 10, 'axes.titlesize': 11, 'figure.dpi': 150})
fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.1), constrained_layout=True)
blue, green, orange, purple = '#24628a', '#268471', '#c78025', '#8655a3'
for ax in axes.flat:
    ax.axhline(REST, color='0.75', lw=.8)
    ax.axhline(THRESHOLD, color='0.3', ls=':', lw=1.2, label='Illustrative threshold')
    ax.set(xlim=(0, 105), ylim=(-68, -50), xlabel='Time (ms)', ylabel='Predicted voltage (mV)')
    ax.spines[['top', 'right']].set_visible(False)
axes[0, 0].plot(time, REST + kernel(10) + kernel(70), color=blue, lw=2, label='Total: two separated inputs')
axes[0, 0].set_title('A. Temporal integration: 60 ms separation')
axes[0, 1].plot(time, REST + kernel(10) + kernel(15), color=blue, lw=2, label='Total: two closely timed inputs')
axes[0, 1].set_title('B. Temporal integration: 5 ms separation')
axes[1, 0].plot(time, REST + kernel(20), color=orange, lw=2, label='Either site alone: 6 mV peak')
axes[1, 0].plot(time, REST + 2 * kernel(20), color=green, lw=2, label='Two sites together: linear sum')
axes[1, 0].set_title('C. Spatial integration: coincident inputs')
axes[1, 1].plot(time, REST + 2 * kernel(20), color=green, lw=1.5, ls='--', label='Excitatory contributions only')
axes[1, 1].plot(time, REST + 2 * kernel(20) + kernel(20, -5), color=purple, lw=2, label='With opposing contribution')
axes[1, 1].set_title('D. Opposing voltage contributions')
for ax in axes.flat:
    ax.legend(fontsize=8, loc='upper right')
fig.suptitle('Linear voltage illustrations: no action-potential waveform or reset is simulated', fontsize=12)
fig.savefig(ASSETS / 'neural-integration.png', dpi=170, facecolor='white')
plt.close(fig)
assert np.isclose(6 + 6 * np.exp(-5 / TAU), 10.6728046984)
assert 6 + 6 * np.exp(-60 / TAU) < 10

svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 640" role="img" aria-labelledby="title desc">
<title id="title">Chemical synaptic transmission between neurons A and B</title>
<desc id="desc">Six steps link an axonal action potential to calcium entry, vesicle fusion, transmitter diffusion, receptor activation, and integration by the receiving neuron. Clearance and recovery are shown separately.</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L0 6L7 3Z" fill="#68869a"/></marker></defs>
<rect width="1100" height="640" rx="18" fill="#f4f8fb"/>
<g font-family="Arial,sans-serif" fill="#18364c">
<text x="30" y="36" font-size="25" font-weight="bold">From neuron A to neuron B: chemical synaptic transmission</text>
<text x="30" y="62" font-size="16">Presynaptic electrical activity → chemical communication → postsynaptic response</text>
'''
steps = [
 (35, 90, '1. Action potential in A', ['A generates its own spike.', 'Axonal conduction brings', 'depolarization to the terminal.'], '#e2edf5'),
 (390, 90, '2. Calcium entry', ['Voltage-gated calcium', 'channels open. Ca2+ enters', 'the presynaptic terminal.'], '#e2edf5'),
 (745, 90, '3. Vesicle fusion', ['Local calcium activates', 'release machinery. Vesicles', 'fuse with the membrane.'], '#e2edf5'),
 (745, 305, '4. Transmitter release', ['Vesicular contents enter', 'the cleft and diffuse toward', 'postsynaptic receptors.'], '#f8ebd6'),
 (390, 305, '5. Receptor response', ['Ionotropic channels or', 'metabotropic pathways', 'change the state of B.'], '#e1efe6'),
 (35, 305, '6. Integration in B', ['B combines this response', 'with its other inputs and state.', 'B may or may not fire.'], '#e1efe6'),
]
for x, y, title, lines, fill in steps:
    svg += f'<rect x="{x}" y="{y}" width="320" height="155" rx="12" fill="{fill}" stroke="#aec4d1" stroke-width="1.5"/>'
    svg += f'<text x="{x+17}" y="{y+33}" font-size="21" font-weight="bold">{title}</text>'
    for j, line in enumerate(lines):
        svg += f'<text x="{x+17}" y="{y+68+j*25}" font-size="17">{line}</text>'
svg += '''<g stroke="#68869a" stroke-width="3" fill="none" marker-end="url(#arrow)">
<path d="M358 166H380"/><path d="M713 166H735"/><path d="M905 249V292"/>
<path d="M741 380H720"/><path d="M386 380H365"/></g>
<rect x="35" y="500" width="1030" height="106" rx="12" fill="white" stroke="#c4d5df"/>
<text x="55" y="531" font-size="20" font-weight="bold">Clearance and recovery shape the next response</text>
<text x="55" y="560" font-size="17">Transport, enzymatic inactivation, and diffusion terminate transmitter action in synapse-dependent ways.</text>
<text x="55" y="586" font-size="17">Vesicle recycling and release dynamics also influence subsequent communication.</text>
</g></svg>'''
(ASSETS / 'chemical-synapse-transmission.svg').write_text(svg)
print('Generated original neural integration and chemical-transmission figures.')
