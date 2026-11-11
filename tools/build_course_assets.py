"""Reproduce original course-aligned examples and four self-contained notebooks."""
from pathlib import Path
import inspect
import runpy
import nbformat
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
LIF = runpy.run_path(str(ROOT / 'tools/build_lif_examples.py'))['MODEL']

HH = r'''
import numpy as np
import matplotlib.pyplot as plt

def hh_rates(v):
    # Absolute V in mV; rates in ms^-1. Removable singularities use limits.
    def ratio(x, scale):
        return scale * (1 + x / (2 * scale)) if abs(x / scale) < 1e-7 else x / (-np.expm1(-x / scale))
    return np.array([0.1 * ratio(v + 40, 10), 4 * np.exp(-(v + 65) / 18),
                     0.07 * np.exp(-(v + 65) / 20), 1 / (1 + np.exp(-(v + 35) / 10)),
                     0.01 * ratio(v + 55, 10), 0.125 * np.exp(-(v + 65) / 80)])

def simulate_hh(drive=10.0, dt=0.01, duration=65.0, g_na=120.0, g_k=36.0):
    """Single compartment; mV, ms, uA/cm^2, mS/cm^2, uF/cm^2.

    Classical squid-axon kinetics at 6.3 deg C; no temperature rescaling.
    Step current from 10 to 50 ms. RK4, held current per interval; no reset.
    """
    t = np.arange(round(duration / dt) + 1) * dt
    current = np.where((t >= 10) & (t < 50), drive, 0.0)
    rates = hh_rates(-65)
    state = np.empty((len(t), 4))
    state[0] = [-65, rates[0] / sum(rates[:2]), rates[2] / sum(rates[2:4]), rates[4] / sum(rates[4:])]
    def derivative(s, injected):
        v, m, h, n = s
        am, bm, ah, bh, an, bn = hh_rates(v)
        ina = g_na * m**3 * h * (v - 50)
        ik = g_k * n**4 * (v + 77)
        il = 0.3 * (v + 54.387)
        return np.array([injected - ina - ik - il,
                         am * (1 - m) - bm * m, ah * (1 - h) - bh * h,
                         an * (1 - n) - bn * n])
    for k in range(len(t) - 1):
        s, i = state[k], current[k]
        a = derivative(s, i); b = derivative(s + dt * a / 2, i)
        c = derivative(s + dt * b / 2, i); d = derivative(s + dt * c, i)
        state[k + 1] = s + dt * (a + 2*b + 2*c + d) / 6
    v, m, h, n = state.T
    currents = np.column_stack([g_na*m**3*h*(v-50), g_k*n**4*(v+77), .3*(v+54.387)])
    up = np.flatnonzero((v[:-1] < 0) & (v[1:] >= 0))
    events = t[up] + dt * (-v[up]) / (v[up + 1] - v[up])
    return t, current, state, currents, events
'''

HH_PLOT = r'''
# EDIT drive, g_na, or g_k, then rerun this cell.
t, current, state, ionic, events = simulate_hh(drive=10, g_na=120, g_k=36)
fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True, constrained_layout=True)
ax[0].plot(t, current, color='#24628a'); ax[0].set(ylabel='Input (µA/cm²)', title='Hodgkin–Huxley: current, voltage, gates, and ionic currents')
ax[1].plot(t, state[:, 0], color='#24628a'); ax[1].set(ylabel='Voltage (mV)')
for k, name in enumerate(['m: Na activation', 'h: Na inactivation', 'n: K activation']): ax[2].plot(t, state[:, k+1], label=name)
ax[2].set(ylabel='Gate state', ylim=(0, 1)); ax[2].legend(fontsize=9, loc='upper right')
for k, name in enumerate(['Na', 'K', 'leak']): ax[3].plot(t, ionic[:, k], label=name)
ax[3].set(xlabel='Time (ms)', ylabel='Outward current (µA/cm²)'); ax[3].legend(fontsize=9)
plt.show()
print('Upward 0 mV crossings (ms):', np.round(events, 3))
'''

HH_CONTROL = r'''
fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True, constrained_layout=True,
                       gridspec_kw={'height_ratios': [3, 1]})
for g_na, color, label in [(120, '#24628a', 'Standard conductance'), (0, '#b75d45', 'Na conductance set to zero')]:
    t, _, s, _, e = simulate_hh(g_na=g_na)
    ax[0].plot(t, s[:, 0], color=color, label=label)
    ax[1].vlines(e, 0.1 if g_na else 0.6, 0.4 if g_na else 0.9, color=color)
ax[0].set(ylabel='Voltage (mV)', title='A parameter ablation, not a simulated drug dose'); ax[0].legend(fontsize=9)
ax[1].set(xlabel='Time (ms)', ylabel='Events', yticks=[], ylim=(0, 1))
plt.show()

_, _, quiet, _, no_events = simulate_hh(drive=0)
assert len(no_events) == 0 and np.max(np.abs(quiet[:, 0] + 65)) < 0.1
_, _, normal, _, e = simulate_hh()
_, _, blocked, _, eb = simulate_hh(g_na=0)
assert len(e) >= 2 and len(eb) == 0 and normal[:, 0].max() > 30
assert np.all((normal[:, 1:] >= 0) & (normal[:, 1:] <= 1))
assert np.isfinite(hh_rates(-40)).all() and np.isfinite(hh_rates(-55)).all()
ef = simulate_hh(dt=.005)[4]
assert len(ef) == len(e) and np.max(np.abs(e - ef)) < .05
print('HH checks passed: rest, gate bounds, Na ablation, singularities, and time-step refinement.')
'''

CONDITION = r'''
def train_association(mode='paired', trials=12, eta=.1, initial=.05):
    """Bounded trial-based Hebbian example. x,y,w are dimensionless.
    This is not Oja or STDP, and it does not simulate animal fear.
    """
    weight, history = initial, [initial]
    for _ in range(trials):
        schedule = [(1., 1.)] if mode == 'paired' else [(1., 0.), (0., 1.)]
        for cs, us in schedule:
            post = float(weight * cs + us > .5)
            if mode != 'frozen':
                weight += eta * cs * post * (1 - weight)
        history.append(weight)
    return np.asarray(history)

def probe_association(weight, cs, us):
    # Learning is disabled during every probe. Readout is a separate LIF neuron.
    drive = 50 + 200 * (weight * cs + us)  # pA: declared teaching mapping
    t, v, events = simulate_lif(np.full(5000, drive))
    move = len(events) >= 3  # response criterion over the 500 ms window
    return t, v, events, drive, .1 * 2.0 if move else 0.0  # ideal travel distance, m
'''

COND_PLOT = r'''
# EDIT eta or trials. Compare paired, unpaired, and frozen-learning controls.
trials, eta = 12, .1
histories = {mode: train_association(mode, trials=trials, eta=eta) for mode in ['paired', 'unpaired', 'frozen']}
fig, ax = plt.subplots(1, 2, figsize=(11, 4.3), constrained_layout=True)
for mode, values in histories.items(): ax[0].plot(values, marker='o', ms=3, label=mode)
ax[0].set(xlabel='Training trial', ylabel='CS connection weight', ylim=(0, 1), title='A. Weight change requires coactivity'); ax[0].legend()
labels = ['CS only', 'US only', 'CS + US']
before = [len(probe_association(.05, *p)[2]) for p in [(1,0), (0,1), (1,1)]]
after = [len(probe_association(histories['paired'][-1], *p)[2]) for p in [(1,0), (0,1), (1,1)]]
x = np.arange(3)
ax[1].bar(x-.18, before, .36, label='Before', color='#b75d45'); ax[1].bar(x+.18, after, .36, label='After paired training', color='#24628a')
ax[1].set(xticks=x, xticklabels=labels, ylabel='Readout spikes / 500 ms', title='B. Frozen-weight probe trials'); ax[1].legend(fontsize=9)
plt.show()
'''

COND_RESPONSE = r'''
fig, ax = plt.subplots(3, 1, figsize=(10, 6.5), constrained_layout=True,
                       gridspec_kw={'height_ratios': [3, 1, 1]})
for row, (weight, color, label) in enumerate([(.05, '#b75d45', 'Before'), (histories['paired'][-1], '#24628a', 'After')]):
    t, v, events, drive, distance = probe_association(weight, 1, 0)
    ax[0].plot(t, v, color=color, label=f'{label}: {drive:.1f} pA')
    ax[1].vlines(events, row+.1, row+.8, color=color)
    ax[2].barh(row, distance, color=color, height=.55)
ax[0].axhline(-50, ls='--', color='.6'); ax[0].set(ylabel='Voltage (mV)', title='CS-alone recall: voltage, output events, and ideal motor response'); ax[0].legend(fontsize=9)
ax[1].set(xlabel='Probe time (ms)', ylabel='Events', yticks=[.45,1.45], yticklabels=['Before','After'], xlim=(0,500))
ax[0].set(xlim=(0,500))
ax[2].set(xlabel='Ideal travel AFTER the probe: 0.1 m/s × 2 s (m)', xlim=(0,.24), yticks=[0,1], yticklabels=['Before','After'])
plt.show()
assert np.isclose(histories['paired'][-1], 1 - .95 * (1-eta)**trials)
assert np.allclose(histories['unpaired'], .05) and np.allclose(histories['frozen'], .05)
assert probe_association(.05, 1, 0)[4] == 0
# The default reference must respond; edits may deliberately abolish recall.
assert probe_association(train_association('paired')[-1], 1, 0)[4] == .2
assert probe_association(.05, 0, 1)[4] == .2
print('Association checks passed: paired/unpaired/frozen controls and learning-disabled recall.')
print('Final paired weight:', histories['paired'][-1])
'''

SENSORS = r'''
def red_feature(rgb):
    rgb = np.asarray(rgb, dtype=float)
    if rgb.ndim < 1 or rgb.shape[-1] != 3 or not np.isfinite(rgb).all() or np.any((rgb < 0) | (rgb > 1)):
        raise ValueError('RGB values must be normalized into [0,1].')
    return np.clip(rgb[...,0] - .5*(rgb[...,1]+rgb[...,2]), 0, 1).mean()

def causal_rms(signal, window):
    return np.sqrt(np.convolve(np.asarray(signal)**2, np.ones(window)/window, mode='valid'))

def sector_encode(ranges, angles, range_min=.05, range_max=5., sectors=36):
    ranges, angles = np.asarray(ranges), np.asarray(angles)
    good = np.isfinite(ranges) & np.isfinite(angles) & (ranges >= range_min) & (ranges <= range_max)
    safe_angles = np.where(np.isfinite(angles), angles, 0.)
    bins = np.floor(((safe_angles + np.pi) % (2*np.pi)) / (2*np.pi) * sectors).astype(int)
    distance = np.full(sectors, np.nan)
    for k in range(sectors):
        values = ranges[good & (bins == k)]
        if len(values): distance[k] = np.min(values)
    valid = np.isfinite(distance)
    rates = np.zeros(sectors)
    rates[valid] = 5 + 45*(1 - distance[valid]/range_max)
    return distance, rates, valid
'''

SENSOR_PLOTS = [r'''
patches = {'Red': [.9,.1,.1], 'White': [.8,.8,.8], 'Blue': [.1,.1,.9], 'Dim red': [.45,.05,.05]}
features = [red_feature(np.tile(rgb, (12,12,1))) for rgb in patches.values()]
counts = [len(simulate_lif(np.full(5000, 50+250*x))[2]) for x in features]
fig, ax = plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
ax[0].bar(list(patches), features, color=['#b75d45','.7','#24628a','#ce998c']); ax[0].set(ylabel='Red-excess feature [0,1]',title='A. Synthetic RGB patches')
ax[1].bar(list(patches), counts, color='#24628a'); ax[1].set(ylabel='LIF spikes / 500 ms',title='B. Declared mapping: I = 50 + 250s pA')
plt.show()
assert features[0] > features[3] > features[1] == features[2] == 0
assert counts[0] > 0 and counts[1] == counts[2] == 0
''', r'''
rng = np.random.default_rng(2026)
time = np.arange(600) / 200
active = (time >= .8) & (time < 1.6)
raw = 9.81 + active*np.sin(2*np.pi*20*time) + .02*rng.standard_normal(len(time))
bias = raw[time < .3].mean()  # stationary, fixed-orientation calibration only
window = 20
rms = causal_rms(raw-bias, window)
tr = time[window-1:]
fig, ax = plt.subplots(2,1,figsize=(10,5),sharex=True,constrained_layout=True)
ax[0].plot(time,raw,color='#24628a'); ax[0].set(ylabel='Sensor z (m/s²)',title='A. Synthetic acceleration with stationary gravity offset')
ax[1].plot(tr,rms,color='#24628a'); ax[1].axhline(.4,ls='--',color='#b75d45',label='Chosen detector threshold')
ax[1].set(xlabel='Time (s)',ylabel='Trailing RMS (m/s²)',title='B. Causal 100 ms window'); ax[1].legend()
plt.show()
assert np.median(rms[(tr>1)&(tr<1.4)]) > .6
assert np.median(rms[tr<.6]) < .05
''', r'''
angles = np.linspace(-np.pi,np.pi,360,endpoint=False)
ranges = np.full(360,3.0); ranges[np.abs(angles)<np.deg2rad(15)] = .8
ranges[100:110] = np.nan  # an entire sector is missing, not free space
distance, rates, valid = sector_encode(ranges,angles)
centers = np.deg2rad(np.arange(36)*10-175)
fig, ax = plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
ax[0].plot(np.rad2deg(centers),distance,'o-',color='#24628a'); ax[0].set(xlabel='Body-relative sector center (deg)',ylabel='Nearest valid range (m)',title='A. 36 sectors, 10° each')
ax[1].bar(np.rad2deg(centers),rates,width=8,color=np.where(valid,'#24628a','#b75d45')); ax[1].set(xlabel='Sector center (deg)',ylabel='Prescribed rate (Hz)',title='B. Unknown sector: zero input + invalid mask')
plt.show()
assert len(distance)==36 and (~valid).any()
assert rates[valid & (distance<1)].min() > rates[valid & (distance>2)].max()
assert np.all(rates[~valid]==0)
print('Sensor checks passed: RGB mapping, causal RMS, 36-sector mask and monotone range encoding.')
''']

NENGO = r'''
import numpy as np
import matplotlib.pyplot as plt
import nengo
# EDIT normalized_current (threshold is 1), tau_rc, or tau_ref.
normalized_current, tau_rc, tau_ref = 1.5, .02, .002
with nengo.Network(seed=7) as network:
    stimulus = nengo.Node(lambda t: normalized_current if t >= .2 else 0.)
    cell = nengo.Ensemble(1,1,neuron_type=nengo.LIF(tau_rc=tau_rc,tau_ref=tau_ref),
                          gain=[2.],bias=[0.],encoders=[[1.]])
    # Nengo multiplies neuron input by gain=2; compensate to obtain J.
    nengo.Connection(stimulus,cell.neurons,transform=.5,synapse=None)
    events_probe = nengo.Probe(cell.neurons)
    voltage_probe = nengo.Probe(cell.neurons,'voltage')
with nengo.Simulator(network,dt=.001,progress_bar=False) as sim:
    sim.run(.8)
time = sim.trange()
event_times = time[sim.data[events_probe][:,0]>0]
fig, ax = plt.subplots(2,1,figsize=(10,5),sharex=True,constrained_layout=True,
                       gridspec_kw={'height_ratios':[3,1]})
ax[0].plot(time,sim.data[voltage_probe][:,0],color='#24628a'); ax[0].set(ylabel='Normalized voltage',title='Nengo: direct current to one LIF neuron')
ax[1].vlines(event_times,0,1,color='#b75d45'); ax[1].set(xlabel='Time (s)',ylabel='Events',yticks=[])
plt.show()
assert np.all(event_times>=.2)
if normalized_current <= 1:
    assert len(event_times) == 0
    print('At/below threshold: no output events in this deterministic example.')
elif len(event_times) >= 2:
    expected = 1/(tau_ref + tau_rc*np.log(normalized_current/(normalized_current-1)))
    measured = 1/np.diff(event_times).mean()
    assert abs(expected-measured)/expected < .06
    print(f'Nengo {nengo.__version__}: analytical {expected:.2f} Hz, simulated {measured:.2f} Hz')
else:
    print('Too few events to estimate an interval rate; extend the simulation.')
'''

def md(text): return nbformat.v4.new_markdown_cell(inspect.cleandoc(text))
def code(text): return nbformat.v4.new_code_cell(inspect.cleandoc(text))

def notebook(name,title,intro,sources,figures,reference):
    cells=[md('# '+title+'\n\n'+intro+'\n\nRun all cells, then change one parameter at a time. Figures are synthetic teaching outputs.\n\n[Run in Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/'+name+'.ipynb)')]
    for heading,source in sources:
        cells.extend([md(heading),code(source)])
    cells.append(md(reference))
    nb=nbformat.v4.new_notebook(cells=cells)
    nb.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
    nb.metadata.language_info={'name':'python'}
    nb.metadata.myst={'downloads':[{'file':name+'.ipynb','title':'Download this notebook'}]}
    nbformat.write(nb,ROOT/'notebooks'/f'{name}.ipynb')
    scope={}
    original=plt.show;plt.show=lambda:None
    try:
        for _,source in sources:
            exec(source,scope)
            if 'fig' in scope and plt.get_fignums():
                destination=next(figures)
                scope['fig'].savefig(ROOT/'assets'/destination,dpi=160,facecolor='white')
                plt.close('all')
    finally: plt.show=original

if __name__=='__main__':
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    notebook('hodgkin_huxley','Laboratory 4 — Hodgkin–Huxley Mechanisms',
      'Companion to Chapter 3. Uses mV, ms, current density µA/cm², conductance density mS/cm², and capacitance density µF/cm². Classical squid-axon kinetics are used without temperature scaling (6.3 °C). No threshold/reset generates the voltage waveform.',
      [('## 1. Model and numerical convention',HH),('## 2. Change the applied current and channel conductances',HH_PLOT),('## 3. Sodium ablation and numerical checks',HH_CONTROL)],
      iter(['hh-course-dynamics.png','hh-course-ablation.png']),
      '## References\n\n[1] A. L. Hodgkin and A. F. Huxley, “A quantitative description of membrane current and its application to conduction and excitation in nerve,” *J. Physiol.*, vol. 117, pp. 500–544, 1952. [DOI](https://doi.org/10.1113/jphysiol.1952.sp004764).\n\n[2] Brian 2 developers, “Hodgkin–Huxley equations (1952).” [Reference implementation](https://brian2.readthedocs.io/en/stable/examples/compartmental.hodgkin_huxley_1952.html). This notebook shifts the voltage origin by −65 mV, uses one compartment, initializes gates at equilibrium, and uses RK4; it is not a reproduction of the Brian cable experiment.')
    notebook('conditioning','Laboratory 5 — From Paired Cues to a Motor Response',
      'Companion to Chapters 4 and 10. CS = a visual cue; US = a vibration cue. A bounded trial-based coactivity rule changes the CS connection. A separate physical-unit LIF neuron reads out the learned drive. Ideal motor distance is an explicit controller assumption; this is not a Gazebo or hardware run.',
      [('## 1. LIF readout (pA, mV, pF, nS, ms)',LIF),('## 2. Bounded coactivity learning and frozen probes',CONDITION),('## 3. Paired, unpaired, and frozen-learning controls',COND_PLOT),('## 4. Separate voltage, event, and motor panels',COND_RESPONSE)],
      iter(['conditioning-course-learning.png','conditioning-course-response.png']),
      '## References\n\n[1] D. O. Hebb, *The Organization of Behavior*. Wiley, 1949. [Catalog](https://wellcomecollection.org/works/g4sfzum4).\n\n[2] N. Zins, Y. Zhang, and H. An, “Implementation of Associative Memory Learning in Mobile Robots Using Neuromorphic Computing,” in *Neuromorphic Computing*, 2023, doi: 10.5772/intechopen.110364. [Chapter](https://www.intechopen.com/chapters/86265). The teaching model here differs from that publication in sensory processing, learning rule, neuron count, and deployment platform. It illustrates controls and does not reproduce the published experiment.')
    notebook('sensory_encoding','Laboratory 6 — RGB, Vibration, and LiDAR Encoding',
      'Companion to Chapters 5–8. All input data are generated here. No camera, IMU, LiDAR, ROS, or Gazebo is required. The examples test numerical mappings, not real-world detector accuracy.',
      [('## 1. Physical-unit LIF helper',LIF),('## 2. Feature definitions and validity masks',SENSORS)]+list(zip(['## 3. Synthetic color patches','## 4. Causal vibration detection','## 5. Thirty-six LiDAR sectors'],SENSOR_PLOTS)),
      iter(['sensor-course-vision.png','sensor-course-imu.png','sensor-course-lidar.png']),
      '## References\n\n[1] P. Corke, *Robotics, Vision and Control: Fundamental Algorithms in Python*. Springer, 2023. [DOI](https://doi.org/10.1007/978-3-031-06469-2).\n\n[2] ROS 2 contributors, “LaserScan message.” [Message contract](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/LaserScan.msg). All feature functions and numerical examples in this notebook are original teaching choices.')
    notebook('nengo_single_neuron','Laboratory 7 — One LIF Neuron in Nengo',
      'Companion to Chapter 9. Use the repository environment (Nengo 4.0.0 and NumPy 1.26.4). In Colab, run `%pip install numpy==1.26.4 nengo==4.0.0 contourpy==1.3.3` before imports and restart the runtime if NumPy was already imported. Nengo current and voltage here are normalized values, not pA or mV.',
      [('## One neuron, a direct current connection, and two separate output plots',NENGO)],
      iter(['nengo-course-neuron.png']),
      '## References\n\n[1] Nengo developers, “Frontend API,” ver. 4.0.0. [LIF, Ensemble, Connection, and Probe](https://www.nengo.ai/nengo/v4.0.0/frontend-api.html). This is a single-neuron API check, not a learned robot or a Nengo Oja implementation.')
    print('Generated four course notebooks and eight original figures.')
