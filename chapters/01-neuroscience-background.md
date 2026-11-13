---
title: "Chapter 1 · Neurons and Synapses"
---

## 1.1 Learning Objectives

A neuron is a special cell in the nervous that receive signals from other neurons. It receives signals at particular places and times, combines them with its ongoing electrical and biochemical state, and influences other cells through synaptic connections. 

By the end of this chapter, you should be able to:

- Explain a neuron's input, integrative, conducting, and output functions.
- Distinguish a graded postsynaptic potential from an action potential.
- Explain spike threshold, spatial integration, and temporal integration.
- Trace chemical signaling from one neuron to another.
- Distinguish excitation, inhibition, ordinary synaptic transmission, and synaptic plasticity.

## 1.2 What is a neuron?

A **neuron** is an electrically excitable cell specialized for receiving, transforming, and communicating information. Its function depends on its membrane, ion channels, geometry, connections, and recent activity. A useful starting point is to follow the transformations between **input**, **integration**, **conduction**, and **output**, rather than memorize an anatomical drawing alone [[1]](#neuro-ref-1), ch. 2.

### 1.2.1 Functional regions: receive, integrate, conduct, and transmit

| Region | What happens there? | Why does it matter computationally? |
|---|---|---|
| Dendrites and their spines | Many synaptic inputs change local conductances and voltage; dendrites can also support active events | The location and timing of input affect its influence on the cell |
| Soma, or cell body | Maintains cellular metabolism, synthesizes proteins, and participates in electrical integration | The cell must maintain its signaling machinery; somatic voltage is only one view of a distributed system |
| Axon initial segment | In many neurons, a high density of voltage-gated channels makes this an important action-potential initiation region | Combined input can be converted into a discrete output event |
| Axon and its branches | Regenerate and conduct action potentials toward terminals | An output can reach multiple targets with finite delays |
| Presynaptic terminals | At typical chemical synapses, convert electrical activity into regulated transmitter release | Communication depends on release probability, receptors, and synaptic dynamics |

Dendrites are not merely passive wires, and the soma is not a universal centralized calculator. Voltage-dependent channels and local dendritic events can change how signals combine. Likewise, not every neuron follows one rigid input-to-axon sequence: some cells communicate mainly through graded potentials, some fire spontaneously, and initiation sites vary with cell type. The table is a functional guide, not a universal wiring rule.

```{figure} ../assets/ccn-neuron-detector.png
:label: fig-ccn-neuron-detector
:alt: Reference-textbook diagram comparing a detector with a neuron, labeling inputs, integration, output, dendrites, synapses, soma, and axon
:width: 85%

**Reference-book figure: input, integration, and output.** Reproduced unchanged from Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 5th ed., ch. 2, “Neuron as a detector” [[2]](#neuro-ref-2). © 2024 the authors and contributors; [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). [Original figure](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/figures/fig_neuron_as_detect.png).
```

**Read the picture.** Follow the separate inputs toward the integration region and then the output axon. The diagram is a functional abstraction: integration can occur throughout dendrites as well as the soma, and the axon initial segment is an important spike-initiation site in many neurons. The purple cell body should not be interpreted as the only place where computation occurs.

A **neural circuit** consists of connected neurons whose activity influences one another. **Convergence** means that several neurons send input to a common target; **divergence** means that one neuron sends output to multiple targets. These patterns allow a circuit to combine information and distribute its consequences. Inhibition can coordinate competing actions as well as suppress activity. For example, activating a pathway that contracts one muscle while inhibiting its antagonist supports coordinated movement [[1]](#neuro-ref-1), ch. 2.

```{figure} ../assets/neuron-synapse.svg
:label: fig-neuron-synapse
:alt: Labeled anatomy of a pink neuron showing dendrites, nucleus, soma, axon initial segment, myelinated axon, and axon terminals, with a circular inset of neurotransmitter release at a chemical synapse
:width: 100%

**Neuron anatomy and chemical synaptic transmission.** Dendrites receive synaptic inputs, the soma and dendrites integrate electrical signals, and action potentials typically initiate near the axon initial segment and propagate along the axon toward its terminals. The enlarged inset illustrates presynaptic transmitter release and receptors on the postsynaptic membrane. Original teaching illustration; schematic and not to scale.
```

**Glial cells** support this system. Their roles include maintaining the extracellular environment, supporting metabolism, forming myelin, and participating in transmitter handling and interactions at synapses. A simulation that omits glia is choosing a scope of explanation; it is not showing that glia are biologically unimportant.

### 1.2.2 Graded input signals and spike output signals

A synaptic input typically first produces a local **postsynaptic potential**: a change in the receiving cell's membrane voltage. It is **graded**, meaning that its size and duration can vary with the synaptic conductance, driving force, location, and condition of the membrane. Small local signals can decay as they spread through the cell.

An **action potential**, in contrast, is a regenerative electrical event. Once initiated under suitable conditions, it can propagate along the axon without the progressive amplitude loss characteristic of passive spread. Its event-like nature makes it useful for communication over distance. This does not make every spike waveform identical across neurons or conditions.

The crucial transformation is therefore not “one incoming spike becomes one outgoing spike.” Many inputs may contribute to one output event, some inputs may prevent that event, and the same input can have different effects depending on the cell's state. A single sufficiently strong connection can be effective in some circuits, but many central synaptic inputs are individually subthreshold [[1]](#neuro-ref-1), chs. 2 and 10.

### 1.2.3 What is threshold?

**Spike threshold** refers to the conditions under which membrane dynamics enter the regenerative process that produces an action potential. In a common sodium-dependent mechanism, depolarization opens voltage-gated sodium channels; inward sodium current produces further depolarization, opening more channels. When this reinforcing process can overcome the opposing currents, an action potential develops [[1]](#neuro-ref-1), chs. 2 and 7.

Threshold is often introduced as a voltage level. For a teaching example, let resting voltage be $-65\,\mathrm{mV}$ and a model threshold be $-55\,\mathrm{mV}$. A 4 mV depolarization leaves voltage at $-61$ mV, below that threshold. A combined 11 mV depolarization would bring the passive prediction to $-54$ mV, crossing the specified comparison level. In a threshold/reset model, that crossing records a spike and triggers reset.

These numbers are illustrative. A biological threshold is not a universal $-55$ mV switch: it depends on channel availability, recent spikes, the rate of depolarization, and where voltage is measured. The axon initial segment is a common trigger region in many neurons, but a voltage recorded at the soma is not necessarily the local voltage where the spike begins. Refractoriness can make an input ineffective shortly after a spike even when it would otherwise be effective.

It is also essential to specify **which threshold** is meant. A spike-generation threshold belongs to a neuron's electrical dynamics. A threshold for inducing a particular plasticity process concerns conditions for changing a connection. A robot's distance threshold is a control decision. These are different quantities, with different units and mechanisms.

### 1.2.4 Spatial integration: where do inputs arrive?

**Spatial integration** describes how inputs at different locations on a neuron jointly influence its response. **Spatial summation** is the combining of postsynaptic effects arising at those different sites. Two presynaptic neurons may activate separate synapses on the same receiving neuron; their effects can overlap and contribute to whether the receiving neuron fires [[1]](#neuro-ref-1), ch. 10.

Consider two excitatory synapses, A and B. Suppose each produces a peak depolarizing contribution of 6 mV at a common observation site when activated alone. With a resting voltage of $-65$ mV, either alone peaks near $-59$ mV. Under a deliberately linear approximation, coincident A and B contribute 12 mV and reach $-53$ mV, beyond a model threshold of $-55$ mV. The receiving cell can therefore respond to a combination that neither input produces alone.

The phrase **at a common observation site** matters. A 6 mV response measured locally on a distal dendrite need not produce 6 mV at the soma or initial segment. Passive spread attenuates and filters signals; dendritic branching, membrane resistance, synapse position, and active channels all affect the result. In a simple passive cable, the **length constant** describes how far a voltage change spreads before substantial attenuation. It is a property of that approximation, not the physical length of the axon.

Real inputs need not add linearly. A synapse changes conductance, altering the response to other inputs. Nearby inputs may interact through shared driving forces, and active dendritic events can amplify some combinations. Inhibitory synapses can influence a local branch, the soma, or spike initiation. Thus, counting excitatory contacts and subtracting inhibitory contacts is insufficient to predict the output.

### 1.2.5 Temporal integration: when do inputs arrive?

**Temporal integration** describes how a neuron's response depends on the timing and history of its inputs. **Temporal summation** occurs when a new postsynaptic response arrives before an earlier response has decayed. Repeated activation of one synapse is the simplest example; inputs from several synapses can also interact in time [[1]](#neuro-ref-1), ch. 10.

For an illustrative decaying voltage contribution,

$$
\Delta V(t)=A\exp\left[-\frac{t-t_k}{\tau}\right],\qquad t\geq t_k,
$$

$A$ is the contribution immediately after an idealized event at time $t_k$, and $\tau$ is its decay time constant. This instantaneous jump followed by a decay is a teaching approximation; a real postsynaptic potential has a finite rise and depends on synaptic as well as membrane dynamics.

Let $A=6$ mV and $\tau=20$ ms. If a second identical event arrives 5 ms later, the first still contributes $6e^{-5/20}\approx4.67$ mV. Immediately after the second event, the total contribution is about 10.67 mV. From $-65$ mV, the linear prediction reaches $-54.33$ mV, exceeding a specified $-55$ mV threshold. If the events are separated by 60 ms, only $6e^{-60/20}\approx0.30$ mV remains from the first; the combined contribution is approximately 6.30 mV and stays below that threshold. **The event count is the same; the timing changes the predicted outcome.**

A longer membrane time constant often permits input effects to overlap over a longer interval in a passive approximation. A shorter time constant favors a narrower coincidence window. Receptor kinetics, inhibition, ongoing conductance, and active channels also shape this window. Spatial and temporal integration operate together: a neuron's response depends on **which inputs arrive, where, when, and in what state the cell receives them**.

```{figure} ../assets/neural-integration.png
:label: fig-neural-integration
:alt: Four original teaching plots comparing separated versus closely timed inputs, coincident inputs at different synapses, and an opposing hyperpolarizing contribution
:width: 100%

Integration examples using linear voltage kernels, a −65 mV baseline, and an illustrative −55 mV comparison level. These are passive voltage predictions: action-potential waveforms and reset are not simulated. Panel D illustrates an opposing hyperpolarizing contribution, not a conductance-based model of shunting inhibition.
```

## 1.3 Membrane potential: the electrical state that inputs change

The **membrane potential** is the electrical potential inside a cell relative to outside:

$$
V_m=V_{\mathrm{inside}}-V_{\mathrm{outside}}.
$$

A value of $-65$ mV means that the inside is 65 mV below the outside under this convention. It is an example resting value, not a constant shared by all neurons. **Depolarization** shifts voltage in the positive direction; **hyperpolarization** shifts it in the negative direction relative to the comparison state.

The lipid membrane limits direct ion passage, while channels provide selective pathways. Unequal ion concentrations and selective permeability together help determine voltage. A channel's **reversal potential** is the voltage at which the net current through that channel population is zero under the stated ionic conditions. Opening channels does not simply “add electricity”: it changes which ionic driving forces influence the membrane. Pumps and transporters maintain the gradients that make signaling possible; an ion pump is not a device that individually creates and resets every spike [[1]](#neuro-ref-1), chs. 6–7.

The membrane also stores separated charge, giving it capacitance. A lumped passive approximation is

$$
C_m\frac{dV_m}{dt}=-g_L(V_m-E_L)+I_{\mathrm{in}}.
$$

| Symbol | Meaning | Example unit |
|---|---|---|
| $C_m$ | Total membrane capacitance in this lumped model | pF |
| $g_L$ | Leak conductance | nS |
| $E_L$ | Leak reversal potential | mV |
| $I_{\mathrm{in}}$ | Net inward-positive applied current | pA |
| $t$ | Time | ms |

The leak term draws voltage toward $E_L$. Capacitance makes voltage change gradually rather than instantaneously under a finite current. The passive membrane time constant is $\tau_m=C_m/g_L$; this helps explain why the timing of inputs matters. The model omits the active currents needed to generate a biological spike.

**Worked example.** With $C_m=200$ pF and $g_L=10$ nS, $\tau_m=20$ ms. A constant 100 pA input produces a passive steady-state shift of $I_{\mathrm{in}}/g_L=10$ mV. Starting from $E_L=-65$ mV, voltage approaches $-55$ mV. It does not reach this asymptote instantaneously. If a threshold is placed exactly at that asymptote, a neuron starting below it does not cross it in finite time in the ideal passive equation. [Chapter 2](03-computational-neuron-models.md) adds explicit spike-generation rules and checks their numerical implementation.

## 1.4 Action potentials, propagation, and spike trains

An **action potential** is a rapid, regenerative voltage excursion caused by voltage-dependent ionic currents. In a standard sodium-dependent description, inward sodium current drives much of the rising phase; sodium-channel inactivation and outward potassium current contribute to repolarization. The contributions and waveform vary across neurons [[1]](#neuro-ref-1), ch. 7.

Once an axonal region depolarizes, local current can bring neighboring excitable membrane into the regenerative process. This repeated regeneration allows propagation. It is not a fixed parcel of transmitter traveling down the axon. Myelin changes the electrical properties of the axonal membrane, and action potentials are regenerated at exposed nodes in myelinated fibers.

Following a spike, sodium-channel availability and other currents change. During an **absolute refractory period**, another spike cannot be elicited through the usual mechanism. During a **relative refractory period**, a stronger depolarizing drive may be required. Refractoriness and adaptation make output depend on recent history, so a neuron is not a memoryless comparator.

“All-or-none” describes the regenerative character of an action potential under specified conditions. It does not mean that neurons encode only a single bit about the world. Stronger input can change the number, rate, timing, or pattern of spikes and the activity of a population; it generally does not communicate input strength by making each spike arbitrarily taller.

A mathematical spike train records event times:

$$
s_i(t)=\sum_k\delta\!\left(t-t_i^{(k)}\right),\qquad
\widehat r_i=\frac{N_i}{T}.
$$

Here $t_i^{(k)}$ is spike $k$ of neuron $i$, $\delta$ is the Dirac delta, $N_i$ is the count in a window of duration $T$, and $\widehat r_i$ is a count-based rate estimate. Five spikes in 0.2 s give 25 Hz. Five evenly spaced spikes and five clustered spikes can have the same window-averaged rate while affecting a downstream neuron differently because of temporal integration and synaptic dynamics [[3]](#neuro-ref-3).

## 1.5 Synapses: the connections between cells

A **synapse** is a specialized communication site between cells. The sending side is **presynaptic**; the receiving side is **postsynaptic**. These terms name roles at a connection. The postsynaptic neuron at one synapse may be the presynaptic neuron at another [[1]](#neuro-ref-1), ch. 8.

### 1.5.1 What structures make up a chemical synapse?

At a typical chemical synapse, the presynaptic terminal contains **synaptic vesicles** holding transmitter, release machinery concentrated at **active zones**, and voltage-gated calcium channels. The **synaptic cleft** is the extracellular gap between the cells. The postsynaptic membrane contains receptors and associated proteins that determine how it responds to the released chemical signal.

Many excitatory contacts onto cortical pyramidal neurons occur on dendritic spines; other contacts occur on dendritic shafts, the soma, or axonal regions. Location affects function. A connection near a particular dendritic input can control that local interaction, while a connection near an output-triggering region can have strong influence over spike initiation. The biological synapse is therefore richer than a scalar weight attached to an abstract edge.

```{figure} ../assets/synapse-modern.svg
:label: fig-ccn-synapse
:alt: Original diagram of a presynaptic neuron and a postsynaptic neuron, showing axonal communication and an enlarged chemical synapse with vesicles, neurotransmitter, synaptic cleft, and postsynaptic receptors
:width: 100%

**Chemical communication between neurons.** A presynaptic action potential reaches an axon terminal and may trigger neurotransmitter release. The transmitter activates postsynaptic receptors, changing the receiving neuron's state. The inset illustrates the principal components of a chemical synapse; the drawing is schematic and not to scale.
```

**Read the picture from bottom to top.** The lower terminal is presynaptic; its vesicles contain transmitter. The cleft separates it from the upper postsynaptic spine. Red transmitter molecules and the labeled ions are different entities: transmitter binds receptors, whereas ions carry current through suitable channels. AMPA and NMDA are ionotropic glutamate receptors; mGlu denotes a metabotropic glutamate receptor. VGCC denotes a voltage-gated calcium channel. This is an example glutamatergic synapse, not a diagram of every synapse type. The source uses `Ca++` for $\mathrm{Ca}^{2+}$ and `Na+` for $\mathrm{Na}^{+}$.

### 1.5.2 Chemical versus electrical synapses

| Type | How a signal crosses between cells | Important consequence |
|---|---|---|
| Chemical | A released transmitter activates receptors on a target cell | Receptor identity, release probability, delay, and response kinetics matter |
| Electrical | Gap-junction channels provide a direct pathway for intercellular current | Coupling can rapidly convey voltage changes and help coordinate activity |

For a simple electrical coupling, current into cell B can be modeled as $I_{A\to B}=g_{\mathrm{gap}}(V_A-V_B)$. Real junctions can have more complex properties, including rectification. Many electrical synapses permit bidirectional influence; chemical synapses usually have a structurally defined release side and receptor side. This chapter focuses on chemical transmission because transmitter release, receptors, and plasticity are central to the later learning models.

### 1.5.3 A postsynaptic potential is a response, not another action potential

A **postsynaptic current** is the ionic current associated with receptor activation. A **postsynaptic potential** is the resulting voltage response, which also depends on capacitance, other conductances, and the location of the input. They are related but are not the same measurement.

One presynaptic spike can produce a small postsynaptic potential without causing a postsynaptic spike. It can also fail to produce detectable release at a particular synapse. The receiving cell integrates this input with other signals and its own state. That is why a connection should not be pictured as automatically copying spikes from one neuron to another.

## 1.6 What is a neurotransmitter?

A **neurotransmitter** is a chemical messenger released by a neuron that acts on specific receptors to influence a target cell. In the conventional vesicular mechanism, it is synthesized, packaged, released, bound by receptors, and then removed or inactivated. The broader biological category includes specialized signaling mechanisms that do not all follow the same packaging rule [[1]](#neuro-ref-1), ch. 13.

A **transmitter molecule**, a **receptor**, and an **ion** are different entities. For example, glutamate can bind an AMPA receptor; the activated receptor-channel allows ionic current. Glutamate does not need to enter the postsynaptic cell and become sodium, and calcium entry into a presynaptic terminal is not the same event as transmitter binding on the receiving side.

### 1.6.1 Examples and why receptors matter

| Messenger | Examples of receptor-dependent actions |
|---|---|
| Glutamate | AMPA and NMDA receptors contribute to excitatory transmission at many central synapses; metabotropic glutamate receptors act through signaling pathways |
| GABA | GABA-A receptors conduct mainly anionic current; GABA-B receptors act through G proteins and can affect channels and release |
| Glycine | Glycine receptors mediate important inhibitory actions, especially in spinal and brainstem circuits; glycine also has other receptor-specific roles |
| Acetylcholine | Nicotinic receptors are ion channels; muscarinic receptors act through G proteins, allowing different effects in different targets |
| Dopamine, norepinephrine, and serotonin | Receptor-dependent signaling can modify excitability, transmission, and plasticity; these messengers do not have one universal “positive” or “negative” effect |
| Neuropeptides | Can alter cellular and synaptic responses through specific receptors, often with different release and time-course requirements from fast transmission |

These examples are a guide, not a complete catalog. A neuron can release more than one messenger. A transmitter's effect depends on the receptors expressed by the target, the relevant ionic gradients, and the circuit state. Calling dopamine a reward number or classifying every molecule permanently as an excitatory or inhibitory label hides the mechanisms we need to understand [[1]](#neuro-ref-1), chs. 11 and 13.

### 1.6.2 Ionotropic and metabotropic receptors

An **ionotropic receptor** is itself part of a ligand-gated ion channel. Transmitter binding changes the channel's opening, allowing a relatively direct effect on ionic conductance. AMPA and GABA-A receptors are examples.

A **metabotropic receptor** influences the cell through intracellular signaling, commonly involving G proteins and downstream effectors. It may alter channels, release machinery, or other biochemical processes. Its effects often develop more slowly and last longer than a fast ionotropic response, although exact time courses vary. Muscarinic acetylcholine and GABA-B receptors are examples. Fast transmission and modulation are useful distinctions, but the same messenger can act through several receptor families.

## 1.7 How does one neuron influence another?

Follow a typical chemical connection from neuron A to neuron B. Each step is a distinct physical process [[1]](#neuro-ref-1), chs. 8 and 12–13.

1. **Neuron A generates and conducts an action potential.** Its own inputs and membrane dynamics determine whether it fires. The action potential propagates along its axon toward a terminal contacting B.
2. **The terminal depolarizes and calcium channels open.** Voltage-gated calcium channels allow calcium to enter the presynaptic terminal down its electrochemical gradient.
3. **Calcium promotes vesicle fusion.** Calcium-sensitive release machinery couples the local calcium rise to fusion of release-ready vesicles with the presynaptic membrane. Fusion proteins and their regulation are essential; calcium does not simply push the transmitter across the cleft.
4. **Transmitter is released and diffuses.** Vesicle contents enter the extracellular cleft by exocytosis. Release occurs in vesicular packets and is probabilistic. A presynaptic spike need not release an identical number of packets on every trial.
5. **Receptors on B are activated.** Binding changes channel conductance directly or initiates intracellular signaling. Ionic current and other receptor-dependent processes alter B's state.
6. **B integrates the response.** Its resulting voltage and conductances interact with other inputs, ongoing activity, and refractoriness. B produces its own action potential only if its spike-generating dynamics support it.
7. **The chemical signal is terminated and the machinery recovers.** Transporters take some transmitters into neurons or glia; enzymes inactivate some; diffusion also removes molecules from the immediate site. Vesicle membrane is recycled. These processes differ across transmitters and synapses.

For acetylcholine, enzymatic breakdown in the cleft is an important termination route. For glutamate, uptake by transporters in nearby cells is central to clearance. The transmitter is not normally left in the cleft indefinitely. Signal duration depends on release, clearance, receptor kinetics, and intracellular processes, rather than just on the duration of A's spike.

```{figure} ../assets/chemical-synapse-transmission.svg
:label: fig-chemical-transmission
:alt: Original six-step diagram from a presynaptic action potential through calcium entry, vesicle release, transmitter diffusion, receptor response, and postsynaptic integration
:width: 100%

Electrical activity in A is converted into chemical signaling and then into a response in B. The two cells generate their own electrical events. The lower strip highlights clearance and recovery, which help determine when and how the connection can respond again.
```

**Example: why B does not necessarily fire.** Suppose one spike in A produces a 2 mV EPSP at B's observation site. With B near $-65$ mV and an illustrative threshold at $-55$ mV, that input alone is insufficient. Several appropriately timed excitatory inputs may combine to make firing possible. An inhibitory conductance, a recent spike in B, or a weaker-than-usual release event may prevent it. A synapse communicates an influence; the downstream neuron determines its response.

## 1.8 Excitatory and inhibitory synaptic actions

An **excitatory** action tends to increase the probability of postsynaptic firing under the relevant conditions. An **inhibitory** action tends to reduce it. An **excitatory postsynaptic potential (EPSP)** is a voltage response associated with excitation; an **inhibitory postsynaptic potential (IPSP)** is associated with inhibition. A small EPSP need not cause a spike, and inhibition need not produce a large negative-going voltage trace [[1]](#neuro-ref-1), ch. 10.

```{figure} ../assets/excitation-inhibition-balance.svg
:label: fig-conductance-balance
:alt: Original conductance diagram showing excitatory, inhibitory, and leak currents, with three passive steady-state membrane-voltage comparisons
:width: 100%

**Conductance balance and membrane voltage.** Original teaching illustration based on the conductance framework in [[1]](#neuro-ref-1), ch. 10, and [[3]](#neuro-ref-3). The shaded region lies above an illustrative −50 mV comparison level. The plotted values are passive steady-state predictions, not simulated action potentials.
```

**Read the diagram.** Each input changes a conductance and its associated ionic current. For constant conductances and no applied current, the passive equilibrium is

$$
V_\infty=\frac{g_LE_L+g_EE_E+g_IE_I}{g_L+g_E+g_I}.
$$

Here $g_E$, $g_I$, and $g_L$ are excitatory, inhibitory, and leak conductances; $E_E$, $E_I$, and $E_L$ are their reversal potentials. In this teaching example, $g_L=10$ nS, $E_L=-65$ mV, $E_E=0$ mV, and $E_I=-75$ mV. Adding 4 nS of excitation shifts the passive equilibrium from −65 mV to approximately −46.4 mV. Keeping that excitation and adding 8 nS of inhibition shifts it back to approximately −56.8 mV. The voltage depends on the conductances and driving forces together; it is not obtained by simply subtracting a count of inhibitory inputs from a count of excitatory inputs. Reversal potentials and threshold are stated example values, not constants shared by all neurons.

### 1.8.1 Conductance and driving force

Use an inward-positive current convention:

$$
I_{\mathrm{syn}}(t)=g_{\mathrm{syn}}(t)\left(E_{\mathrm{syn}}-V_m(t)\right).
$$

$g_{\mathrm{syn}}$ is synaptic conductance, $E_{\mathrm{syn}}$ its reversal potential, and $E_{\mathrm{syn}}-V_m$ the driving force. A receptor's effect is determined by both the conductance it changes and the voltage toward which that conductance drives the membrane.

At $V_m=-60$ mV, a 2 nS conductance with $E_{\mathrm{syn}}=0$ mV produces $+120$ pA. A 2 nS conductance with reversal $-75$ mV produces $-30$ pA. The same conductance magnitude therefore does not imply the same current, and neither current is a fixed spike probability. As voltage changes, the driving force changes too.

### 1.8.2 Hyperpolarization and shunting inhibition

An inhibitory conductance can pull voltage toward a reversal potential below the current membrane voltage, producing hyperpolarization. It can also restrain excitation while producing little voltage change on its own. This second situation is **shunting inhibition**.

To see why, add inhibitory conductance $g_I$ with reversal $E_I$:

$$
C_m\frac{dV_m}{dt}=-g_L(V_m-E_L)-g_I(V_m-E_I)+I_{\mathrm{in}}.
$$

If $E_I=E_L$, the inhibitory conductance does not shift the zero-input resting voltage in this simple model. It does, however, increase total conductance. The effective passive time constant becomes $C_m/(g_L+g_I)$, and the steady depolarization produced by the same constant input current becomes $I_{\mathrm{in}}/(g_L+g_I)$.

**Worked example.** Take $C_m=200$ pF, $g_L=10$ nS, $E_L=E_I=-65$ mV, and $I_{\mathrm{in}}=120$ pA. Without the inhibitory conductance, the steady shift is 12 mV and the time constant is 20 ms. Adding $g_I=10$ nS leaves zero-input rest at $-65$ mV but reduces the input-driven shift to 6 mV and the time constant to 10 ms. Against an illustrative $-55$ mV threshold, the first passive steady voltage lies above the comparison level and the second below it. This is a current-driven passive example; a complete spiking model must also implement its threshold and output dynamics.

The sign of a voltage deflection and the functional effect on firing are consequently not identical. Chloride gradients and the relation between reversal potential, rest, and spike threshold matter. GABA-A responses can be depolarizing in some cells or conditions, so their effect cannot be inferred solely from the transmitter's name. Inhibition also changes the time window for integration and can organize circuit timing rather than simply silence a neuron.

## 1.9 What is synaptic plasticity?

**Synaptic plasticity** is a change in the effectiveness or properties of synaptic transmission. It concerns how a connection responds after its history or regulatory state changes, rather than simply whether a postsynaptic response occurs now. Both strengthening and weakening can be plasticity. Changes can be presynaptic, postsynaptic, structural, or combinations of these [[1]](#neuro-ref-1), chs. 12 and 66–67.

### 1.9.1 Ordinary transmission versus a changing connection

During ordinary transmission, a presynaptic event changes postsynaptic conductance and voltage. If the connection's properties remain fixed, repeating the same event under the same conditions can generate the same expected response. The temporary voltage change is not by itself evidence that the connection learned.

A plastic connection changes how later input affects the target. Possible mechanisms include changes in transmitter-release probability, available vesicles, receptor number or function, and the number or structure of contacts. Intrinsic plasticity, such as a lasting change in a neuron's excitability, is related but is not the same as a change at a particular synapse.

### 1.9.2 Short-term and long-term forms

| Form | What changes? | Example interpretation |
|---|---|---|
| Short-term facilitation | A recent input makes a subsequent response stronger for a limited period | Residual presynaptic calcium can contribute to increased release at some synapses |
| Short-term depression | Recent activity reduces subsequent response strength | Limited availability of release-ready vesicles can contribute; mechanisms depend on the synapse |
| Long-term potentiation (LTP) | Synaptic efficacy remains increased beyond the inducing activity | Some pathways express lasting changes in receptor-mediated response and other mechanisms |
| Long-term depression (LTD) | Synaptic efficacy remains decreased beyond the inducing activity | Persistent weakening can alter how a pathway contributes to later responses |

These labels describe classes of effects, not a universal mechanism or an exact duration shared by all synapses. A strongly facilitating connection and a depressing connection can respond differently to the same spike train. Long-term changes can involve signaling cascades, gene expression, protein synthesis, or structural remodeling depending on the preparation and stage. Short-term plasticity is also distinct from a brief voltage response: the former changes transmission of a subsequent event; the latter is the response to an event.

### 1.9.3 An example of coincidence-dependent plasticity

At a well-studied glutamatergic connection from hippocampal CA3 to CA1, NMDA receptors are important in inducing particular forms of LTP. Under usual extracellular magnesium conditions, efficient NMDA current requires transmitter binding together with sufficient postsynaptic depolarization to relieve voltage-dependent magnesium block; appropriate co-agonist occupancy is also required. Calcium entry can then initiate intracellular pathways that change synaptic efficacy, including changes in AMPA receptor-mediated transmission [[1]](#neuro-ref-1), chs. 10 and 67.

This example links **integration** to **plasticity**: combined inputs can change postsynaptic voltage, and that voltage can help determine whether a plasticity-inducing biochemical signal occurs. It does not mean that every coincident pair of spikes strengthens every synapse, or that all hippocampal LTP is NMDA dependent. Different pathways and stimulation histories can recruit different mechanisms.

### 1.9.4 What a synaptic weight represents

A computational weight $w_{ij}$ often summarizes how strongly neuron $j$ influences neuron $i$. It is not a neurotransmitter molecule, a single receptor, or a unique anatomical quantity. For example, a conductance model may use

$$
g_{ij}(t)=w_{ij}z_{ij}(t),
$$

where $w_{ij}$ is a maximal conductance in nS and $z_{ij}(t)$ is a dimensionless activation variable. With $w_{ij}$ fixed, an incoming event can change $z_{ij}$ and produce transmission without long-term weight change. A model can separately include short-term release dynamics or a rule that changes $w_{ij}$. Other models use dimensionless weights; their units and interpretation must be declared.

**Worked example.** A controlled test input produces an average 1 mV EPSP before an induction protocol and 1.5 mV afterward. Under comparable recording and membrane conditions, this is a 50% increase in the measured response. It supports a change in effective transmission; it does not by itself identify whether release probability, receptor properties, or another factor caused it. Ongoing voltage changes and trial-to-trial release variability must be considered before attributing a response difference to plasticity.

[Chapter 3](04-hebbian-learning.md) turns selected plasticity ideas into explicit learning rules, including Hebbian updates and STDP. Those rules are mathematical hypotheses about changes in a model, not complete molecular accounts of memory. Plasticity contributes to learning and memory, but a lasting change at one connection alone does not explain an entire learned behavior.

## 1.10 From a biological circuit to embodied AI

Consider a mobile robot approaching a wall. A range measurement is sensor data. An encoder converts it into an input current, rate, or spike sequence. A neuron model integrates that input with other signals and its current state. Synaptic models specify how one unit influences another. A controller converts circuit activity into an action. A learning mechanism may change how the circuit responds to later experience.

Keep the following mappings explicit:

| Biological concept | A possible computational abstraction | What must still be specified |
|---|---|---|
| Spatial integration | Weighted input from several channels or dendritic compartments | Input locations, weights, and whether combination is linear |
| Temporal integration | A membrane or synaptic state with a decay time constant | Units, time step, and input timing |
| Spike initiation | A threshold and reset rule in LIF | Threshold, reset, refractory handling, and numerical detection |
| Chemical transmission | A delayed, event-driven synaptic current or conductance | Reversal potential, kinetics, and release assumptions |
| Excitation and inhibition | Inputs with different functional effects and reversal potentials | Driving forces and the target neuron's state |
| Plasticity | Changes in efficacy or release dynamics | Rule, time scale, constraints, and evaluation protocol |

This project's planned LiDAR example uses 36 angular sectors of $10^\circ$ each. Combining neighboring sectors could illustrate spatial input integration; accumulating evidence over successive samples could illustrate temporal integration. These are engineering representations. They do not establish that an animal uses 36 corresponding sensory neurons or implements the chosen equations. A robot example should state what is sensed, how it is encoded, what the neurons compute, and what actually changes during learning.

## Additional Reading Materials

The main biological reference is *Principles of Neural Science*, fifth edition [[1]](#neuro-ref-1). Use Chapter 2 for the functional organization of a neuron, Chapters 6–7 for membrane properties and action potentials, Chapters 8 and 10 for synapses and integration, Chapters 11–13 for receptors, release, and neurotransmitters, and Chapters 66–67 for plasticity and memory. The explanatory text, numerical examples, and figures identified as original were created for this book. Reproduced reference-book figures are credited separately in their captions. Parameter values in worked examples are stated assumptions, not measurements from a particular cell.

For the computational treatment, use *Neuronal Dynamics* [[3]](#neuro-ref-3), Chapters 1–3 for single-neuron and synaptic models and Chapter 6 for spike trains and neuronal variability. See the [reference-book reading map](roadmap.md#reference-book-reading-map) for further selections across the textbook.

## 1.11 Exercises and checks for understanding

1. Trace the input, integration, conduction, and output functions of a neuron. Explain why the soma is not a complete description of every neuron's computation.
2. Distinguish an EPSP from an action potential. Explain why a spike in neuron A does not guarantee a spike in neuron B.
3. With the temporal-kernel example in Section 1.2.5, calculate the combined contribution for two 6 mV events separated by 20 ms. Does the linear voltage prediction exceed the stated comparison level?
4. Two distal synapses each produce a 6 mV local EPSP. Explain why it is insufficient to conclude that the axon initial segment receives a 12 mV depolarization.
5. Explain threshold in terms of regenerative membrane dynamics. Give two reasons a fixed threshold is only an approximation to biological spike initiation.
6. List the steps from a presynaptic action potential to a postsynaptic response, naming the roles of calcium, vesicles, transmitter, and receptor.
7. Compare ionotropic and metabotropic receptors. Explain how the same neurotransmitter can have different effects on different target cells.
8. For $g_{\mathrm{syn}}=3$ nS, $E_{\mathrm{syn}}=0$ mV, and $V_m=-65$ mV, calculate inward-positive synaptic current. What happens to the driving force as voltage approaches the reversal potential?
9. Recalculate the shunting example with $g_I=20$ nS. Find the effective time constant and the steady shift produced by the same 120 pA current.
10. A second EPSP is larger than the first. Propose a short-term synaptic explanation and explain why temporal voltage summation could also affect what is measured.
11. Distinguish synaptic transmission, short-term plasticity, LTP/LTD, and intrinsic excitability changes. Which of these does a fixed-weight LIF network necessarily include?
12. Design a robot example that separately identifies a measured input, a dynamic state, a connection efficacy, and an observable output. State what evidence would be needed to claim learning.


## References



(neuro-ref-1)=

[1] Eric R. Kandel, James H. Schwartz, Thomas M. Jessell, Steven A. Siegelbaum, and Albert James Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013, chs. 2, 6–8, 10–13, and 66–67. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(neuro-ref-2)=

[2] Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 5th ed., 2024, ch. 2. [Open textbook source](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/chapter-02.md); [edition and copyright](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/frontmatter.md); [CC BY 4.0 license](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/LICENSE).

(neuro-ref-3)=

[3] Wulfram Gerstner, Werner M. Kistler, Richard Naud, and Liam Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014, chs. 1–3 and 6. [Online textbook](https://neuronaldynamics.epfl.ch/online/).
