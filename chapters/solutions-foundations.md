---
title: "Solutions I — Foundations"
---

# Solutions to Exercises — Part I: Foundations

These solutions follow the models and assumptions of the corresponding chapters. Design questions give reference protocols rather than claiming that new experiments were performed.

## Overview — O.8 Exercises

[Original exercises](01-introduction.md#o8-exercises)

1. **Robot variables.** $\mathbf{x}_t$ is physical pose/motion state; $\mathbf{o}_t$ is the LiDAR observation; $\mathbf{z}_t$ is the internal neural state or memory; $\mathbf{a}_t$ is the chosen motor command. An observation is not the same as the true pose.
2. **Gaussian place-cell rate.** At the preferred location, $r=20$ Hz. At a distance $\sigma=0.15$ m, $r=20e^{-1/2}\approx12.13$ Hz. These are expected rates rather than guaranteed realized spike counts.
3. **Occupancy bias.** More time spent in one location produces more spikes even at the same rate. Use an occupancy-normalized estimate $\hat r_b=K_b/T_b$ for $T_b>0$, flag low-occupancy bins, and use consistent smoothing.
4. **Head-direction ablation.** Hold trajectories, train/test split, tuning, and random seeds fixed; compare a position decoder with heading inputs against an otherwise matched decoder without them. Report held-out position error and variability, separately for turns and straight segments. A performance difference is not, by itself, causal proof about biological circuitry.

## Chapter 1 — 1.11 Exercises and Checks for Understanding

[Original exercises](01-neuroscience-background.md#111-exercises-and-checks-for-understanding)

1. **Input, integration, conduction, output.** Synaptic and dendritic regions receive signals; membrane and dendritic properties integrate them; axonal membrane propagates regenerative spikes; terminals transmit to targets. The soma alone omits dendritic location effects, axonal initiation, and synaptic terminal dynamics.
2. **EPSP versus action potential.** An EPSP is a graded postsynaptic voltage response, whereas an action potential is regenerative. A presynaptic spike may fail to release transmitter, produce too small a drive, or encounter inhibition/refractoriness: it does not guarantee a postsynaptic spike.
3. **20 ms temporal separation.** At the second event the first contributes $6e^{-20/20}=2.21$ mV. The sum is $8.21$ mV; from $-65$ mV this predicts $-56.79$ mV, below the illustrative $-55$ mV threshold.
4. **Distal synapses.** Two local 6 mV EPSPs need not deliver 12 mV to the axon initial segment. Cable attenuation, dendritic branching, active channels, conductance changes, and inhibition alter transmission and summation. Compare contributions at a common observation site.
5. **Threshold.** A spike begins when regenerative inward currents overcome opposing currents. A fixed threshold is approximate because channel availability and recent spikes vary, and because depolarization rate and location affect initiation.
6. **Chemical transmission.** Presynaptic spike reaches terminal → voltage-gated calcium channels open → calcium-dependent vesicle fusion → transmitter release into cleft → receptor activation → postsynaptic electrical or biochemical response → removal/recycling of transmitter.
7. **Receptors.** Ionotropic receptors directly gate ion channels, usually rapidly; metabotropic receptors initiate intracellular signaling, often more slowly. Receptor subtype, ion selectivity, and cellular context allow one transmitter to produce different effects.
8. **Synaptic current.** Under inward-positive convention, $I=g(E_{\mathrm{syn}}-V_m)=3\,\mathrm{nS}\times65\,\mathrm{mV}=+195$ pA. Driving force approaches zero as $V_m$ approaches 0 mV.
9. **Shunting example.** With $C=200$ pF, leak $10$ nS, and added inhibitory conductance $20$ nS, total conductance is $30$ nS. $\tau_{\mathrm{eff}}=200/30=6.67$ ms; for 120 pA input the steady voltage shift is $120/30=4$ mV, under the example's reversal-potential assumptions.
10. **Second EPSP larger.** Short-term facilitation can increase release probability after the first event; however, overlapping unchanged EPSPs can also produce a larger combined voltage. Subtract residual voltage or fit a synaptic response model before inferring facilitation.
11. **Transmission versus plasticity.** Synaptic transmission is an event-dependent response; short-term plasticity transiently changes efficacy; LTP/LTD changes efficacy over longer periods; intrinsic plasticity changes excitability. A fixed-weight LIF circuit models membrane integration/events but does not necessarily include synaptic or intrinsic plasticity.
12. **Robot design.** Log measured LiDAR ranges, evolving LIF voltage/synaptic traces, connection weight, and angular velocity or actual turn. Compare pretraining and frozen post-training behavior with matched sensory tests and no-learning controls; a behavioral change beyond controls is required for a learning claim.

## Chapter 2 — 2.9 Exercises

[Original exercises](03-computational-neuron-models.md#29-exercises)

1. **Poisson probability.** At 50 Hz during $0.002$ s, expected count is $\lambda=0.1$. Thus $P(N\geq1)=1-e^{-0.1}=0.09516$ (9.52%).
2. **100 pA subthreshold.** With $E_L=-65$ mV, $g_L=10$ nS, and threshold $-50$ mV, $V_\infty=E_L+I/g_L=-55$ mV. It never crosses threshold from the stated reset.
3. **400 pF capacitance.** Holding current/leak fixed leaves $V_\infty$ and rheobase unchanged. Time constant doubles from 20 to 40 ms; rise, first-spike latency, and suprathreshold interspike interval increase, except for other fixed timing contributions.
4. **Reset versus waveform.** LIF records a threshold event and resets voltage; it does not integrate voltage-gated sodium/potassium channels to produce a full spike shape. Analyze LIF event timestamps separately from the membrane trace.
5. **Model selection.** (a) Use occupancy-conditioned probabilistic counts for rate-map uncertainty; (b) adaptive LIF for spike-frequency adaptation; (c) conductance-based sodium activation/inactivation dynamics (e.g., HH) for sodium-channel mechanisms. Validate against each intended measured quantity.

## Chapter 3 — 3.10 Exercises

[Original exercises](04-hebbian-learning.md#310-exercises)

1. **Ten updates.** With additive Hebbian learning $\Delta w=\eta xy=0.02$, $w_{10}=0.4+10(0.02)=0.60$. Sustained coactivity grows weight without bound unless normalized, bounded, or opposed by decay/homeostasis.
2. **Outer product.** For 36 inputs and 10 outputs, $\mathbf y\mathbf x^\top$ is a $10\times36$ matrix; entry $(j,i)$ updates the weight from input $i$ to output $j$.
3. **Negative-lag STDP.** $\Delta w=-0.012e^{-10/20}\approx-0.00728$, using the chapter's post-before-pre negative-lag branch.
4. **Shared cue.** The shared feature yields equal scores $(0.8,0.8)$ for the two stored patterns. It contains no class-discriminating information in this example.
5. **Recall controls.** Compare baseline weights, weights after correct pairings, and weights after label-pair shuffling with a frozen held-out probe set. Correctly paired learning should favor matching partial cues; shuffled pairings should disrupt that relation. Exact accuracies require notebook execution and should not be invented.
6. **Delayed reward.** Pair inputs once, deliver reward after controlled delays, and measure weight change with otherwise fixed activity. An eligibility-trace model with passive decay predicts delayed effects proportional to $e^{-\Delta/\tau_e}$; a simultaneous-only two-factor rule does not. Include no-reward, no-pairing, and randomized-delay controls.

(spatial-solutions)=

## Chapter 4 — 4.10 Exercises

[Original exercises](02-spatial-cells.md#spatial-exercises)

1. **Grid aliases.** A grid cell's periodic firing means multiple spatial positions can produce similar activity. Multiple phases/scales and non-grid cues may reduce aliasing; one cell is insufficient across several periods.
2. **Heading versus travel.** A robot can face north while moving east sideways, or reverse while still facing north. Heading is orientation; travel direction follows the velocity vector.
3. **Rates.** $12/0.6=20$ Hz and $30/3=10$ Hz. More spikes in the second bin do not imply greater firing rate.
4. **Speed confound.** Match speed within the same positions or vary speed repeatedly along the same route; then fit location-plus-speed and location-only predictors on held-out observations. Keep heading and occupancy controlled.
5. **Imposed versus learned field.** A Gaussian rate map directly computed from true position is a designer-specified encoder. Learning requires training-dependent parameter updates, held-out evaluation, and frozen/shuffled learning controls; supplying true pose does not demonstrate localization.
6. **Coordinate transforms.** Validate range/beam angle; reconstruct sensor-frame endpoints; apply calibrated sensor-to-base transform and timestamped base-to-world pose; derive environment-relative boundary geometry. Handle invalid returns and pose/scan uncertainty.
7. **Hippocampal pathways.** The principal trisynaptic route is EC → DG → CA3 → CA1. DG reaches CA3 through mossy fibers, and CA3 reaches CA1 through Schaffer collaterals. Direct EC → CA1 and EC → CA3 projections bypass earlier stages; recurrent CA3 connections and hippocampal–entorhinal loops add further interactions. A strictly one-way grid-to-place chain therefore omits important anatomy and does not establish how place fields emerge.
8. **Time versus distance.** The ideal time cell fires at 3 s at both speeds. The ideal distance cell follows $t=d/v$: $0.6/0.2=3$ s and $0.6/0.3=2$ s. At a single speed their firing can coincide, making the hypotheses hard to distinguish; varying speed separates a fixed-time response from a fixed-distance response. Real cells may show mixed coding or task-dependent changes, so assess repeated trials rather than one event.
9. **Recording modality and color scale.** Calcium imaging measures indicator fluorescence related to intracellular calcium. Event detection or deconvolution estimates activity under assumptions about indicator kinetics, sampling, and noise; it is not a direct measurement of every extracellular spike. A map normalized to its own maximum describes relative activity, not an absolute Hz scale, and maxima cannot automatically be compared across cells. State the modality, event-extraction procedure, occupancy correction, and normalization before interpreting the map.
10. **Independent sequence test.** Divide trials into training and test groups, estimate each cell's preferred time from training trials, and freeze the resulting cell order. Evaluate temporal tuning and population sequence consistency on held-out trials, comparing against suitable time-shifted or event-label-shuffled controls. This can support reproducible event-relative temporal information; it does not by itself demonstrate an intrinsic clock, identify the generating circuit, or exclude speed, distance, and task-state confounds.
