---
title: "Solutions III — Spatial Models and Laboratories"
---

# Solutions to Exercises — Part III: Spatial Models and Computational Laboratories

Laboratory tasks that change parameters require running the supplied notebooks to obtain empirical plots and measured error statistics. The following provides analytical expectations and reproducible procedures; it does not invent experimental measurements.

## Grid Cells and Grid-to-Place Mapping — Exercises

[Original exercises](grid-to-place.md#exercises)

1. **Lattice translations.** With $k=4\pi/(\sqrt3\lambda)$ and wave vectors angled at $30^\circ$, $90^\circ$, and $150^\circ$, translation $(\lambda,0)$ changes the three cosine phases by $(2\pi,0,-2\pi)$; translation $(\lambda/2,\sqrt3\lambda/2)$ changes them by $(2\pi,2\pi,0)$. Since cosine is $2\pi$ periodic, all three terms remain unchanged. Both vectors have length $\lambda$ and are 60° apart.
2. **Six identical inputs.** Under the chapter's normalized, equally weighted readout, an average of six identical normalized grid functions equals one such function. All periodic aliases remain; neither averaging nor thresholding alone creates unique spatial information.
3. **Double $\kappa$.** For $\zeta=0$ and positive gain, doubling $\kappa$ doubles the raw rectified grid rate wherever nonzero and doubles the declared theoretical maximum $g_{\max}=3r_G\kappa$. Their ratio, normalized drive $S$, and resulting place output remain invariant, up to numerical error. This result depends on the normalization.
4. **One versus all phases.** Translating one grid changes its peaks relative to the remaining inputs and alters spatial conjunctions. Applying the same spatial translation to all inputs preserves their relative alignment and translates the combined pattern, subject to cropping by the arena.
5. **Lower threshold $\tau$.** Lowering threshold enlarges the regions where $S>\tau$, potentially revealing secondary patches or joining distinct components. Count connected regions with a fixed 4-/8-neighbor criterion, grid resolution, and intensity threshold; repeat on a larger arena and finer mesh. No universal patch count follows without executing the changed configuration.
6. **Learning rather than imposed anchor.** Initialize grid phases without a shared preferred target and permit only a specified learning rule to update readout weights during exploration. Compare against a fixed shared-phase-anchor construction, a frozen random network, and shuffled spatial experience. Evaluate held-out localization of firing, stability, and independence from hand-specified target coordinates. Showing an emergent field requires training-dependent change and these controls.

## Laboratory 1 — Computational Neuron Models, L1.5 Exercises

[Original exercises](computational-neuron-models-lab.md#l15-exercises-and-next-laboratory)

1. **Time-step refinement.** Run exactly the same LIF stimulus at 0.1 and 0.05 ms resolution. The Chapter 2 reference 200 pA model predicts a first crossing after approximately 27.73 ms from reset, before any offset due to stimulus start. Endpoint threshold detection quantizes spike times; refining the time step generally decreases this error. Compare measured first spike and mean ISI with analytical values.
2. **100 versus 200 pA.** $V_\infty=-65+100/10=-55$ mV is below the $-50$ mV threshold; $V_\infty=-65+200/10=-45$ mV is above it. Thus 100 pA remains subthreshold while sustained 200 pA can repeatedly cross and reset.
3. **Double capacitance.** With leak 10 nS and fixed current, $C_m$ from 200 to 400 pF doubles $\tau_m$ from 20 to 40 ms but leaves $V_\infty$ constant. The RC voltage rises more slowly; suprathreshold first-spike delay and mean ISI usually increase, lowering firing rate under otherwise identical settings.
4. **Spike events versus voltage peaks.** The LIF voltage trace is reset at threshold rather than showing an HH-like action-potential waveform. Search the separately returned event-time array for spikes; the reset trace alone cannot reconstruct the modeled sodium/potassium spike shape.
5. **Transition to place cells.** The neuron notebook maps prescribed current to a membrane-voltage trajectory and threshold/reset spikes. The Place Cell notebook maps known position to a prescribed rate field and samples spikes stochastically under a Poisson assumption. It changes both the source of rate input (trajectory) and the spike-generation model; neither is a demonstration of robot self-localization.

## Laboratory 2 — Place Cell from Scratch, Exercises

[Original exercises](04-place-cells.md#exercises)

1. **Double $\sigma$.** For $r(d)=20e^{-d^2/(2\sigma^2)}$ Hz with zero baseline, $r>10$ corresponds to $d<\sigma\sqrt{2\ln2}$. Doubling $\sigma$ doubles the contour radius and *would* quadruple the area if the disk were entirely inside the arena. For the actual 1 m square, calculate the fraction of grid positions above 10 Hz before/after because walls may clip the disks. State center, $\sigma$, and grid resolution.
2. **Halve $\Delta t$.** Expected total spike count is approximately $\sum_n r(\mathbf{x}_n)\Delta t$. With unchanged physical duration and trajectory, twice as many steps at half the step width preserve this time integral approximately. Realized counts still vary across runs.
3. **Five seeds.** Hold trajectory, true field, bins, smoothing, and duration fixed. Generate five independent spike realizations, calculate each occupancy-normalized field, and report binwise mean/sample SD plus error against the imposed field in sufficiently occupied bins. Numerical variation requires those five simulations; it cannot be inferred from a single map.
4. **Oracle pose versus localization.** The notebook supplies known simulator position to compute expected firing; the code does not need to estimate position from LiDAR or neural observations. To demonstrate localization, infer position without ground-truth pose as input, then compare decoded position with independent withheld ground truth on unseen trajectories.
