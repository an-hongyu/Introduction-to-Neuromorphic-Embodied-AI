---
title: "Chapter 1 · Introduction to Neural Systems, Neurons, and Synapses"
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

A **neural circuit** consists of connected neurons whose activity influences one another. **Convergence** means that several neurons send input to a common target; **divergence** means that one neuron sends output to multiple targets. These patterns allow a circuit to combine information and distribute its consequences. Inhibition can coordinate competing actions as well as suppress activity. For example, activating a pathway that contracts one muscle while inhibiting its antagonist supports coordinated movement [[1]](#neuro-ref-1), ch. 2.

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

**How a sensory stimulus becomes a spike train.** In the muscle-spindle example, increasing stretch generally increases the graded receptor potential; this can increase the **frequency** of spikes generated at the trigger zone. A longer stimulus can extend the spike train. The axon conducts these events to the terminal, where spike frequency and count help regulate transmitter release. This is a conceptual encoding example, not a universal linear relationship for every receptor [[4]](#neuro-ref-4).

```{figure} ../assets/stimulus-to-spike-reference-layout.webp
:label: fig-stimulus-spike-transmitter
:alt: Muscle-spindle sensory neuron above three aligned rows of weaker, stronger, and longer stretch stimuli; columns A-D show receptor potentials, trigger-zone spikes with threshold lines, axonal action potentials, and transmitter release
:width: 100%

**From graded sensory input to neural output.** The stimulus changes the receptor potential, whereas individual action potentials remain regenerative events of roughly stereotyped amplitude. Information is reflected in spike timing, frequency, and number, and transmitter release also depends on presynaptic state. Original educational redraw informed by *Principles of Neural Science*, 4th ed., ch. 2, Fig. 2-10 [[4]](#neuro-ref-4); curves and release dots are schematic.
```

A mathematical spike train records event times:

$$
s_i(t)=\sum_k\delta\!\left(t-t_i^{(k)}\right),\qquad
\widehat r_i=\frac{N_i}{T}.
$$

Here $t_i^{(k)}$ is spike $k$ of neuron $i$, $\delta$ is the Dirac delta, $N_i$ is the count in a window of duration $T$, and $\widehat r_i$ is a count-based rate estimate. Five spikes in 0.2 s give 25 Hz. Five evenly spaced spikes and five clustered spikes can have the same window-averaged rate while affecting a downstream neuron differently because of temporal integration and synaptic dynamics [[3]](#neuro-ref-3).

## 1.5 Synapses: the connections between cells

A **synapse** is a specialized contact through which a neuron communicates with another cell. At a chemical synapse, **presynaptic** identifies the releasing side and **postsynaptic** identifies the receiving side. These are roles at a particular connection: a neuron can be postsynaptic to one cell and presynaptic to another [[1]](#neuro-ref-1), ch. 8.

### 1.5.1 What structures make up a chemical synapse?

A chemical synapse has three principal components:

| Component | Main structures and role |
|---|---|
| **Presynaptic terminal** | Synaptic vesicles store transmitter; active zones contain release machinery and nearby voltage-gated calcium channels. |
| **Synaptic cleft** | A narrow extracellular gap separates the two cell membranes. |
| **Postsynaptic membrane** | Receptors and associated proteins determine how the target responds to transmitter. |

```{figure} ../assets/synapse-modern.svg
:label: fig-ccn-synapse
:alt: Overview of presynaptic and postsynaptic neurons with an inset identifying vesicles, the synaptic cleft, and postsynaptic receptors
:width: 100%

**Anatomy of a chemical synapse.** The terminal of one neuron faces a receptor-bearing membrane of another. The inset identifies the components of this contact. Original schematic; not to scale.
```

Contacts can occur on dendritic spines, dendritic shafts, the soma, or axonal regions. Their location affects how an input interacts with nearby signals and influences spike initiation. A synapse therefore has a physical location and molecular organization, not merely a numerical weight [[1]](#neuro-ref-1), chs. 8 and 10.

### 1.5.2 Chemical versus electrical synapses

| Type | Connection between cells | Functional consequence |
|---|---|---|
| **Chemical** | Transmitter acts across a cleft on target-cell receptors. | Transmission depends on release, receptor properties, and response kinetics. |
| **Electrical** | Gap-junction channels provide a direct pathway for intercellular current. | Voltage changes can influence the coupled cell rapidly; many connections permit bidirectional signaling. |

For a simple electrical synapse, inward current into B is $I_{A\to B}=g_{\mathrm{gap}}(V_A-V_B)$, where $g_{\mathrm{gap}}$ is the coupling conductance. Real junctions may show rectification or other departures from this approximation. Chemical transmission instead has distinct release and receptor sides; its sequence is developed in Section 1.7 [[1]](#neuro-ref-1), ch. 8.

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

At a chemical synapse, a spike in neuron A can influence neuron B through a sequence of electrical and chemical events. The figure below follows this sequence through an excitatory synapse [[1]](#neuro-ref-1), ch. 8, Fig. 8–8.

```{figure} https://uw.pressbooks.pub/app/uploads/sites/692/2023/05/synaptictransmission.jpg
:label: fig-chemical-transmission
:alt: Panels A-C show presynaptic calcium entry, vesicle fusion and transmitter release, and postsynaptic receptor-channel opening; the left traces show a presynaptic action potential followed by a delayed, subthreshold EPSP
:width: 100%

**From a presynaptic spike to a postsynaptic potential.** Panels A–C show calcium entry, transmitter release, and receptor activation. The lower-left trace is a graded EPSP, not a second action potential. Source: *Principles of Neural Science*, 5th ed., Fig. 8–8 [[1]](#neuro-ref-1), as displayed in the [University of Washington teaching chapter](https://uw.pressbooks.pub/physiology/chapter/synapses-and-neurotransmitter-receptors/). © McGraw-Hill.
```

### 1.7.1 Panels A–C: converting a spike into a synaptic response

**A — Calcium entry.** An action potential depolarizes the presynaptic terminal, opening voltage-gated $\mathrm{Ca}^{2+}$ channels near the active zone. Calcium enters the terminal and acts as an intracellular release signal; it is not the neurotransmitter that carries the message across the cleft.

**B — Vesicle fusion and release.** The local calcium increase activates release machinery, allowing transmitter-filled vesicles to fuse with the presynaptic membrane. Their contents enter the cleft by **exocytosis**. Release is probabilistic and depends on the condition of the terminal.

**C — Receptor activation.** Transmitter diffuses across the cleft and binds postsynaptic receptors. In the illustrated fast excitatory connection, receptor channels open and net inward current depolarizes the receiving cell. The $\mathrm{Na}^{+}$ arrows illustrate this inward contribution; they do not imply that every excitatory receptor is sodium-selective. Other receptor types produce different effects, as introduced in Section 1.6 [[1]](#neuro-ref-1), chs. 8 and 12.

### 1.7.2 When does the receiving neuron generate a new spike?

The **postsynaptic current** is ion flow associated with receptor activation; the **postsynaptic potential** is the resulting change in membrane voltage. Voltage depends on that current, membrane capacitance, other conductances, and input location. In this excitatory example the response is an **excitatory postsynaptic potential (EPSP)** [[1]](#neuro-ref-1), ch. 10.

Notice the two traces at the left of the figure: the upper trace is a presynaptic action potential, whereas the lower trace rises after a delay and remains below the marked threshold. **The figure does not show a postsynaptic spike.** A new spike requires sufficient depolarization at B's spike-initiation region, after integration with other inputs and its ongoing state. Spatial and temporal summation are described in Sections 1.2.4–1.2.5; inhibition and refractoriness can prevent firing.

**Worked example.** With an illustrative baseline of $-65$ mV and threshold of $-55$ mV, a 2 mV EPSP at the observation site reaches only $-63$ mV. It does not trigger the specified threshold rule. Additional appropriately timed excitation may permit firing, but adding a fixed number of inputs is not a universal biological rule.

Thus, **presynaptic spike → chemical transmission → graded postsynaptic response → possible new spike**. The last step is conditional: neuron B generates its own action potential rather than receiving a copied spike from neuron A.

### 1.7.3 Synaptic delay and recovery

Release and receptor activation take time, producing a **synaptic delay** between the arriving presynaptic spike and the onset of the postsynaptic response. The figure's 1 ms scale bar is a time reference, not a universal delay for all synapses; this delay is also distinct from the time required for B to reach firing threshold [[1]](#neuro-ref-1), ch. 8.

Transmitter action is limited by diffusion, uptake, and, for some transmitters, enzymatic breakdown. Vesicle recycling and recovery of release machinery influence later responses. These processes complete the transmission cycle; changes in the connection's efficacy are considered separately under synaptic plasticity in Section 1.9 [[1]](#neuro-ref-1), chs. 12–13.

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

The main biological reference is *Principles of Neural Science*, fifth edition [[1]](#neuro-ref-1). Use Chapter 2 for the functional organization of a neuron, Chapters 6–7 for membrane properties and action potentials, Chapters 8 and 10 for synapses and integration, Chapters 11–13 for receptors, release, and neurotransmitters, and Chapters 66–67 for plasticity and memory. The explanatory text, numerical examples, and original schematic figures were prepared for this book. The sensory-coding diagram is an independent educational redraw of concepts discussed in the fourth edition [[4]](#neuro-ref-4), not a reproduced textbook figure. Parameter values in worked examples are stated assumptions, not measurements from a particular cell.

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

[2] Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 5th ed., 2024, ch. 2. [Open textbook source](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/chapter-02.md); [edition and copyright](https://github.com/compcogneuro/book/blob/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/frontmatter.md); [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

(neuro-ref-3)=

[3] Wulfram Gerstner, Werner M. Kistler, Richard Naud, and Liam Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014, chs. 1–3 and 6. [Online textbook](https://neuronaldynamics.epfl.ch/online/).

(neuro-ref-4)=

[4] Eric R. Kandel, James H. Schwartz, and Thomas M. Jessell, Eds., *Principles of Neural Science*, 4th ed. New York, NY, USA: McGraw-Hill, 2000, ch. 2, Fig. 2-10. [Chapter 2 source](https://neurodatasharing.bme.gatech.edu/cloud/Fong%20et%20al/Additional%20Data/Images/Imaging%20resources/KSJ_Ch2.pdf).
