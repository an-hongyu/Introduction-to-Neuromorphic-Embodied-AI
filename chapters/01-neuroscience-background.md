---
title: "Chapter 1 · Introduction to Neural Systems, Neurons, and Synapses"
---

The nervous system links sensation to action through networks of neurons. To build neuromorphic systems, we first need to understand **how neural signals arise within a cell and how they pass between cells**. This chapter develops that picture at three levels: the nervous system, the individual neuron, and the synapse.

**Learning objectives.** By the end of this chapter, you should be able to describe the organization of a nervous system; identify the main parts of a neuron; explain membrane voltage, spike initiation, and spike propagation; trace chemical synaptic transmission; and distinguish excitation, inhibition, spatial and temporal integration, and plasticity.

## 1.1 Nervous System

A nervous system allows an organism to sense its surroundings, combine sensory information with its internal state, and coordinate behavior. In vertebrates, the **central nervous system (CNS)** consists of the brain and spinal cord. The **peripheral nervous system (PNS)** connects the CNS with receptors, muscles, and organs. Sensory pathways carry information toward central circuits; motor pathways carry commands toward effectors. These pathways form a feedback loop rather than a one-way chain.

The brain contains specialized yet interconnected regions. Sensory and motor cortices process and influence particular forms of perception and action; structures such as the hippocampus are important for memory and spatial behavior. This book introduces those spatial representations in [Chapter 4](02-spatial-cells.md). For now, the essential point is that **behavior emerges from coordinated neural circuits**, not from a single isolated neuron [[1]](#neuro-ref-1).

**How do we study neural systems?** Different questions require different experimental approaches. Animal models make it possible to study circuits and behavior under conditions that cannot routinely be reproduced in human experiments. Rodents are particularly important for spatial navigation and memory studies. Simpler preparations can isolate cellular mechanisms: research using the sea slug *Aplysia*, highlighted in the supplied lecture, helped establish how changes in synaptic transmission contribute to learning and memory [[5]](#neuro-ref-5).

```{figure} ../assets/ch1-neuroscience/aplysia-animal-model.webp
:label: fig-ch1-aplysia
:alt: Sea slug Aplysia photographed underwater on the seafloor, as shown in the neuroscience lecture.
:width: 76%

**An animal model for synaptic learning.** The large, experimentally accessible neurons of *Aplysia* made it useful for mechanistic studies of synapses and memory. Source: *Neuroscience Foundations – Introduction*, slide 7 [[5]](#neuro-ref-5).
```

Neural activity can also be measured or modified by **neural interfaces**. Scalp electroencephalography (EEG) records population-level electrical activity without penetrating the skull. Electrocorticography (ECoG) records closer to the cortical surface, while intracortical electrodes can capture more localized signals, sometimes including spikes. Deep brain stimulation (DBS) instead delivers electrical stimulation to specific brain targets, for example to treat symptoms of Parkinson's disease. The choice of interface depends on what must be measured or controlled, as well as safety and invasiveness [[5]](#neuro-ref-5).

```{figure} ../assets/ch1-neuroscience/neural-recording-modalities.webp
:label: fig-ch1-recording
:alt: Lecture illustration comparing scalp EEG, surface electrodes, and intracortical recording arrangements.
:width: 88%

**Different recording locations reveal different signals.** Noninvasive EEG, cortical-surface ECoG, and intracortical electrodes differ in placement and the neural activity they can resolve. Source: *Neuroscience Foundations – Introduction*, slide 26 [[5]](#neuro-ref-5).
```

The same **sense–integrate–act** structure appears in embodied AI. Sensors supply observations, neural or computational circuits maintain internal state, and actuators change the environment. Understanding this biological loop gives us a foundation for designing and evaluating neuromorphic robots.

## 1.2 Neurons

A **neuron** is an electrically excitable cell specialized for communication. Its main structures are the **dendrites**, **soma (cell body)**, **axon**, and **presynaptic terminals**. Dendrites receive many incoming signals; the soma supports cellular function and participates in integration; the axon conducts action potentials; and its terminals influence other cells. In many neurons, spikes begin near the **axon initial segment**, where voltage-gated channels are concentrated [[1]](#neuro-ref-1), ch. 2.

```{figure} ../assets/neuron-anatomy-chemical-synapse-2026.svg
:label: fig-ch1-neuron-anatomy
:alt: Labeled neuronal anatomy showing dendrites, soma, nucleus, axon and presynaptic terminals.
:width: 100%

**Anatomy of a typical neuron.** Dendrites and the soma participate in receiving and integrating signals; the axon carries the neuron's output toward its terminals. This is a schematic, not a universal morphology.
```

**Membrane potential.** Neurons maintain different ion concentrations inside and outside their membranes. Selective permeability, ion channels, and ion transporters create an electrical potential difference. With the outside as the reference,

$$
V_m=V_{\mathrm{inside}}-V_{\mathrm{outside}}.
$$

A common resting example is $V_m=-65\,\mathrm{mV}$, although resting values differ across cells. A shift toward less negative voltage is called **depolarization**; a shift toward more negative voltage is **hyperpolarization**. Sodium, potassium, calcium, and chloride channels contribute differently because of their selectivity and ionic driving forces.

```{figure} ../assets/ch1-neuroscience/membrane-charge-distribution.webp
:label: fig-ch1-charge
:alt: Lecture schematic of ionic charge distributions on either side of a neuronal membrane.
:width: 68%

**Charge separation across the membrane.** Local charge separation gives rise to membrane voltage even though the bulk intracellular and extracellular solutions remain approximately electrically neutral. Source: *Neuroscience Foundations – Neurons*, slide 16 [[6]](#neuro-ref-6).
```

```{figure} ../assets/ch1-neuroscience/ion-channel-types.webp
:label: fig-ch1-ion-channels
:alt: Illustration of different ion-channel proteins spanning a cell membrane.
:width: 82%

**Selective ion channels.** The type and state of an ion channel determine which ions can flow and how membrane voltage responds. Source: *Neuroscience Foundations – Neurons*, slide 24 [[6]](#neuro-ref-6).
```

A passive membrane can be approximated by a resistor–capacitor (RC) system:

$$
C_m\frac{dV_m}{dt}=-g_L(V_m-E_L)+I_{\mathrm{in}}.
$$

Here $C_m$ is membrane capacitance, $g_L$ is leak conductance, $E_L$ is its reversal potential, and $I_{\mathrm{in}}$ is applied inward-positive current. The membrane time constant is $\tau_m=C_m/g_L$. For example, $C_m=200\,\mathrm{pF}$ and $g_L=10\,\mathrm{nS}$ give $\tau_m=20\,\mathrm{ms}$. This passive equation explains gradual voltage integration, but not the full biological spike waveform. [Chapter 2](03-computational-neuron-models.md) develops the LIF, Hodgkin–Huxley, and Izhikevich models.

**From graded voltage to a spike.** Small inputs produce **graded** voltage responses. When depolarization is sufficient to recruit regenerative voltage-gated currents, the neuron generates an **action potential**, or **spike**. A spike is an all-or-none event under a given set of cellular conditions; its amplitude is not a simple analog readout of input strength. Stronger sustained input can instead change the **timing and frequency** of spikes. Threshold varies with membrane state and recent activity, so a fixed threshold is a useful model approximation rather than a universal biological constant.

```{figure} ../assets/ch1-neuroscience/action-potential-waveforms.webp
:label: fig-ch1-spikes
:alt: Lecture graphs of membrane potential across the threshold and the action potential waveform.
:width: 92%

**Threshold and action-potential waveform.** Subthreshold voltage changes are graded; suprathreshold excitation initiates a regenerative spike. Source: *Neuroscience Foundations – Neurons*, slide 38 [[6]](#neuro-ref-6).
```

Once initiated, the spike propagates along the axon through successive activation of voltage-gated channels. A **refractory period** follows each spike, limiting the ability to generate another spike immediately. A neuron's output is therefore described not only by whether it fires but also by its **spike train**. If four spikes are observed over 100 ms, the window-averaged rate is $4/0.1=40$ Hz; that rate does not specify the exact spike times.

```{figure} ../assets/ch1-neuroscience/axon-spike-propagation.webp
:label: fig-ch1-axon-propagation
:alt: Lecture schematic of an action potential traveling down a neuronal axon.
:width: 94%

**Axonal conduction.** Regenerative membrane dynamics allow action potentials to propagate over distance. Source: *Neuroscience Foundations – Neurons*, slide 41 [[6]](#neuro-ref-6).
```

For computation, a neuron is not simply a binary switch: its response depends on **input location, timing, membrane state, and recent history**. The output spikes then influence other cells through synapses.

## 1.3 Synapses

A **synapse** is a specialized connection through which one neuron influences another. The transmitting neuron is **presynaptic**; the receiving neuron is **postsynaptic**. In a typical **chemical synapse**, the axon terminal and the postsynaptic membrane are separated by a narrow **synaptic cleft**. Unlike the continuous passage of a signal through a wire, a presynaptic spike is converted into a chemical message and then into an electrical response [[1]](#neuro-ref-1), ch. 8.

```{figure} ../assets/ch1-neuroscience/chemical-synapse-panels.webp
:label: fig-chemical-transmission
:alt: Original lecture panels A through C showing presynaptic calcium entry, vesicle fusion and neurotransmitter release, postsynaptic receptor-channel opening, and a delayed graded EPSP.
:width: 100%

**From neuron A's spike to neuron B's response.** (A) Terminal depolarization opens voltage-gated $\mathrm{Ca}^{2+}$ channels. (B) Calcium triggers synaptic vesicle fusion and neurotransmitter release. (C) Neurotransmitter binds postsynaptic receptors, producing a graded postsynaptic response. The lower-left EPSP remains below threshold: it is **not** a second spike. Figure from *Neuroscience Foundations – Synapse*, slide 10 [[7]](#neuro-ref-7); the lecture adapts the transmission sequence discussed in *Principles of Neural Science* [[1]](#neuro-ref-1).
```

The conversion has three main stages. **First**, an arriving action potential opens voltage-gated calcium channels, allowing calcium to enter the terminal. **Second**, calcium-dependent release machinery causes vesicles to fuse with the presynaptic membrane and release neurotransmitter into the cleft. **Third**, neurotransmitter binds postsynaptic receptors and alters ion conductance or intracellular signaling. Release is probabilistic, and a presynaptic spike does not guarantee a postsynaptic spike.

Receptors determine the effect of a transmitter. **Ionotropic receptors** directly gate ion channels and commonly produce fast responses. **Metabotropic receptors** act through intracellular signaling and often produce slower, longer-lasting effects. Thus the same neurotransmitter may have different effects on different target cells.

**Excitation and inhibition.** An **excitatory postsynaptic potential (EPSP)** tends to make firing more likely; an **inhibitory postsynaptic potential (IPSP)** tends to make it less likely. The resulting voltage depends on conductance and driving force, not merely on a count of excitatory and inhibitory synapses. Under an inward-positive convention,

$$
I_{\mathrm{syn}}(t)=g_{\mathrm{syn}}(t)\big(E_{\mathrm{syn}}-V_m(t)\big).
$$

For $g_{\mathrm{syn}}=3\,\mathrm{nS}$, $E_{\mathrm{syn}}=0\,\mathrm{mV}$, and $V_m=-65\,\mathrm{mV}$, the current is $+195\,\mathrm{pA}$. The current becomes smaller as voltage approaches the reversal potential.

```{figure} ../assets/ch1-neuroscience/epsp-ipsp-summation.webp
:label: fig-conductance-balance
:alt: Lecture illustration of excitatory and inhibitory inputs summed at the axon hillock.
:width: 78%

**EPSPs and IPSPs combine at the receiving neuron.** Their timing and relative effects help determine whether threshold is reached. Source: *Neuroscience Foundations – Synapse*, slide 29 [[7]](#neuro-ref-7).
```

An inhibitory conductance can also reduce the response to excitation without producing a large negative voltage shift. This **shunting inhibition** increases total membrane conductance and shortens the passive integration time constant. If $C_m=200\,\mathrm{pF}$, $g_L=10\,\mathrm{nS}$, and an additional $g_I=20\,\mathrm{nS}$ has $E_I=E_L$, then $\tau_{\mathrm{eff}}=200/(10+20)=6.67\,\mathrm{ms}$. Under a constant 120 pA input, the steady voltage shift is $120/30=4$ mV. These are passive-model predictions, not complete spike simulations.

**Spatial and temporal integration.** A neuron combines signals arriving from many synapses. **Spatial summation** combines inputs at different locations; **temporal summation** combines inputs that arrive close together in time. The location of a synapse matters because a local dendritic EPSP may attenuate before reaching the axon initial segment. Therefore, two distal 6 mV EPSPs do not necessarily produce a 12 mV depolarization at the spike-initiation zone.

```{figure} ../assets/ch1-neuroscience/spatial-and-temporal-integration.webp
:label: fig-neural-integration
:alt: Three panels from the synapse lecture showing single input, spatial summation, and temporal summation.
:width: 100%

**Two ways inputs combine.** Spatial summation combines signals from distinct sites; temporal summation reflects closely timed responses. Both affect the receiving neuron's membrane potential. Source: *Neuroscience Foundations – Synapse*, slide 24 [[7]](#neuro-ref-7).
```

For a simple decaying voltage contribution after an input at $t_k$, use

$$
\Delta V(t)=A\exp\!\left[-\frac{t-t_k}{\tau}\right],\qquad t\ge t_k.
$$

With $A=6$ mV and $\tau=20$ ms, a second identical event arriving 5 ms later produces an illustrative total contribution of $6+6e^{-5/20}\approx10.67$ mV. With a separation of 20 ms, the total is $6+6e^{-1}\approx8.21$ mV. From a $-65$ mV resting value, those passive sums predict $-54.33$ mV and $-56.79$ mV, respectively. Against an illustrative $-55$ mV threshold, **the timing—not just the number of inputs—changes the predicted outcome**. This exponential voltage kernel is a teaching approximation, not a detailed synaptic conductance model.

**Transmission versus plasticity.** A synapse can transmit a signal without changing its strength. **Synaptic plasticity** refers to changes in the effectiveness of later transmission. Short-term facilitation and depression alter responses over relatively brief periods; long-term potentiation (LTP) and depression (LTD) describe longer-lasting strengthening or weakening. A larger second voltage peak alone does not prove facilitation, because it may reflect overlap with the first EPSP. A connection weight $w_{ij}$ in a model summarizes an effective influence, not a single biological molecule. [Chapter 3](04-hebbian-learning.md) introduces explicit Hebbian and spike-timing-dependent learning rules.

The resulting computational view is straightforward: **sensory signals alter membrane and synaptic state; neurons integrate those signals; output spikes influence downstream neurons; and plasticity can change future responses**. The following chapters turn this biological picture into equations, neural codes, and robotic controllers.

## Exercises and checks for understanding

<!-- exercise-center:ch1 -->
[Interactive questions and expandable worked answers](../exercises/ch1.md) are available in the dedicated exercise section.

1. Trace the input, integration, conduction, and output functions of a neuron. Explain why the soma is not a complete description of every neuron's computation.
2. Distinguish an EPSP from an action potential. Explain why a spike in neuron A does not guarantee a spike in neuron B.
3. With the temporal-kernel example in Section 1.3, calculate the combined contribution for two 6 mV events separated by 20 ms. Does the linear voltage prediction exceed the stated comparison level?
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

(neuro-ref-5)=

[5] H. An, *Neuromorphic Robotic Systems: Neuroscience Foundations for Neuromorphic Robotics — Introduction*, lecture slides, Michigan Technological University, 2026.

(neuro-ref-6)=

[6] H. An, *Neuromorphic Robotic Systems: Neuroscience Foundations for Neuromorphic Robotics — Neurons*, lecture slides, Michigan Technological University, 2026.

(neuro-ref-7)=

[7] H. An, *Neuromorphic Robotic Systems: Neuroscience Foundations for Neuromorphic Robotics — Synapse*, lecture slides, Michigan Technological University, 2026.
