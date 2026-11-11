---
title: "Chapter 1 · Neuroscience Background"
---

## 1.1 Learning objectives and reading guide

Before building a spiking robot, we need a vocabulary for the biological system that inspires it. By the end of this chapter, you should be able to identify the main parts of a neuron, explain how neurons communicate at synapses, distinguish a membrane potential from a spike, and separate neural activity from synaptic learning.

The biological background follows the topics developed in *Principles of Neural Science*, fifth edition, especially Chapters 2, 4, 6–8, and 10 [[1]](#neuro-ref-1). The explanations, numerical examples, and schematic below are original teaching material. The aim is to establish the concepts needed for spatial cognition and computational modeling, rather than reproduce the source textbook.

## 1.2 What is a neuron?

A **neuron** is a specialized cell that receives signals, changes its electrical and biochemical state, and communicates with other cells. A neuron is a living system, not simply a number passed through an activation function. Its shape, ion channels, receptors, and connections all influence its response [[1]](#neuro-ref-1).

| Structure | Biological role | Abstraction used later in this book |
|---|---|---|
| Dendrites | Receive many synaptic inputs and can perform local integration | Input channels or dendritic compartments |
| Soma, or cell body | Supports metabolism and participates in electrical integration | Part of the modeled membrane state |
| Axon initial segment | A common initiation site for action potentials | Spike-generation mechanism |
| Axon | Conducts action potentials to distant targets | Communication pathway with a delay |
| Presynaptic terminal | Releases transmitter at a chemical synapse | Event-triggered synaptic update |

This description fits a common neuronal organization; real neurons have diverse structures, and not every signal follows one rigid sequence. Dendrites can have active electrical properties, and some neural signals are graded rather than all-or-none spikes. A point-neuron model intentionally leaves much of this structure out.

```{figure} ../assets/neuron-synapse.svg
:label: fig-neuron-synapse
:alt: Original schematic showing dendrites, soma, axon, transmitter release, and postsynaptic receptors
:width: 100%

A neuron and a chemical synapse. The inset separates electrical propagation along the axon from chemical transmission between cells. This conceptual drawing is not to scale.
```

**Glial cells** are also essential. They contribute to the chemical environment, myelination, metabolic support, and interactions at synapses. Omitting glia from a first simulation is a choice of modeling scope; it does not imply that they are unimportant [[1]](#neuro-ref-1).

## 1.3 Membrane potential: voltage across a cell membrane

The membrane separates fluids with different ionic compositions. Ion channels provide selective pathways across it, while ion pumps and transporters help maintain concentration gradients. The **membrane potential** is the electrical potential inside the cell relative to the outside:

$$
V_m = V_{\mathrm{inside}}-V_{\mathrm{outside}}.
$$

A value of $-65\,\mathrm{mV}$ means that the inside is 65 mV below the outside under this convention. It is an illustrative resting value, not a universal constant. **Depolarization** means that $V_m$ becomes less negative; **hyperpolarization** means that it becomes more negative.

The lipid membrane also stores separated charge and therefore behaves partly like a capacitor. For a lumped, passive approximation,

$$
C_m\frac{dV_m}{dt}=-g_L(V_m-E_L)+I_{\mathrm{in}}.
$$

| Symbol | Meaning | Example unit |
|---|---|---|
| $C_m$ | Total membrane capacitance of the lumped model | pF |
| $g_L$ | Leak conductance | nS |
| $E_L$ | Leak reversal potential | mV |
| $I_{\mathrm{in}}$ | Net inward-positive input current | pA |
| $t$ | Time | ms |

The leak term draws voltage toward $E_L$. The input current can move it away. The passive time constant is $\tau_m=C_m/g_L$ [[1]](#neuro-ref-1). This circuit approximation becomes the starting point for the models in [Chapter 3](03-computational-neuron-models.md).

**Worked example.** Let $C_m=200$ pF and $g_L=10$ nS. Then $\tau_m=20$ ms. With a constant 100 pA input and no spike mechanism, the steady voltage shift is $I_{\mathrm{in}}/g_L=10$ mV. Starting at $-65$ mV, the passive model approaches $-55$ mV. This calculation predicts a passive voltage, not whether a particular biological neuron will fire.

## 1.4 Action potentials and spike trains

An **action potential**, or spike, is a rapid, regenerative voltage excursion produced by voltage-dependent ionic currents. In a standard description, inward sodium current contributes to the rising phase, while sodium-channel inactivation and outward potassium current contribute to repolarization. The relative contribution of specific channels depends on the neuron [[1]](#neuro-ref-1).

Once initiated, an action potential can propagate along an axon. A stronger input generally does not encode its strength by making every spike arbitrarily taller. Instead, information can be associated with changes in spike timing, spike count, firing rate, and population activity. The refractory period also limits how rapidly a neuron can generate successive spikes.

For neuron $i$, a mathematical spike train can be written as

$$
s_i(t)=\sum_k\delta\!\left(t-t_i^{(k)}\right),
$$

where $t_i^{(k)}$ is the time of spike $k$ and $\delta$ is the Dirac delta. This notation records event times; it does not describe the waveform of the action potential. A count-based estimate over a window of duration $T$ is

$$
\widehat r_i=\frac{N_i}{T}.
$$

For example, five spikes in 0.2 s give an estimated rate of 25 Hz. The number depends on the window: a short interval is useful for rapid changes but gives a noisy estimate. Spike timing and firing rate are complementary descriptions, not interchangeable measurements [[2]](#neuro-ref-2).

## 1.5 What is a synapse?

A **synapse** is a specialized site of communication between cells. The sending cell is **presynaptic**; the receiving cell is **postsynaptic**. Two broad mechanisms are important [[1]](#neuro-ref-1):

| Mechanism | How communication occurs | Consequence for a model |
|---|---|---|
| Chemical synapse | Transmitter released from a terminal binds to postsynaptic receptors | Model release, receptor effects, delay, and a time course as needed |
| Electrical synapse | Gap-junction channels couple cells directly | Model current driven by the voltage difference between cells |

At a typical chemical synapse, an arriving action potential opens voltage-gated calcium channels. Calcium entry promotes vesicle fusion and transmitter release. Transmitter crosses the synaptic cleft and binds to receptors; receptor activation can directly gate ion channels or act through signaling pathways. Release is probabilistic, so a presynaptic spike does not guarantee an identical postsynaptic response every time.

A simple synaptic conductance produces an inward-positive current

$$
I_{\mathrm{syn}}(t)=g_{\mathrm{syn}}(t)\bigl(E_{\mathrm{syn}}-V_m(t)\bigr).
$$

Here $g_{\mathrm{syn}}$ is conductance, $E_{\mathrm{syn}}$ is the synaptic reversal potential, and $E_{\mathrm{syn}}-V_m$ is the driving force. The current therefore depends on both the open-channel conductance and the current membrane voltage. This is more informative than treating every input as a fixed voltage increment.

## 1.6 Excitation, inhibition, and integration

An excitatory synaptic input tends to increase the probability of postsynaptic firing in the relevant state; an inhibitory input tends to reduce it. These effects depend on receptors, ionic driving forces, timing, and the rest of the circuit. In particular, inhibition need not always produce a large downward voltage deflection: increasing conductance can reduce the effect of concurrent excitation, a phenomenon called **shunting inhibition** [[1]](#neuro-ref-1).

**Temporal summation** concerns inputs arriving close together in time. **Spatial summation** concerns inputs arriving at different locations. A point-neuron model compresses spatial integration into a single state, while a compartmental model can distinguish dendritic locations.

**Worked example.** At $V_m=-60$ mV, a 2 nS synapse with $E_{\mathrm{syn}}=0$ mV contributes $+120$ pA under the inward-positive convention. A 2 nS synapse with reversal $-75$ mV contributes $-30$ pA. These instantaneous currents cannot simply be interpreted as fixed spike probabilities: the voltage and conductances continue to change.

## 1.7 Neural activity is different from learning

Neural **activity** describes evolving states such as membrane voltage, synaptic conductance, and spikes. **Plasticity** describes changes in neuronal or synaptic properties. In a network model, $V_i(t)$ may change every time step while a connection parameter $w_{ij}$ remains fixed. A learning rule changes $w_{ij}$ on a chosen time scale.

A synaptic weight is a useful abstraction for connection efficacy; it does not identify a unique molecular quantity. It might summarize release probability, receptor properties, effective conductance, or several mechanisms. [Chapter 4](04-hebbian-learning.md) introduces activity-dependent updates and explains why a mathematical Hebbian rule is not a complete biological account of memory.

## 1.8 Connection to embodied AI

Consider a mobile robot approaching a wall. A range measurement is sensor data. An encoder converts it into a model input or spike sequence. A neuron model transforms that input into activity. Connections combine signals, and a controller turns the resulting state into an action. A plasticity rule may change how those signals influence later actions.

In this project, the planned LiDAR example uses 36 angular sectors, each spanning $10^\circ$. Choosing one input channel per sector is an engineering representation; it does not establish that the animal nervous system uses 36 corresponding neurons. We will keep biological evidence, computational assumptions, and robot implementation choices explicit throughout the book.

## 1.9 Exercises

1. Explain the roles of dendrite, soma, axon initial segment, axon, and presynaptic terminal without using the word “weight.”
2. Compute the firing-rate estimate for eight spikes in 0.4 s. What information about their timing is lost?
3. For $g_{\mathrm{syn}}=3$ nS, $E_{\mathrm{syn}}=0$ mV, and $V_m=-65$ mV, calculate the instantaneous synaptic current using the stated sign convention.
4. Explain why an inhibitory conductance can reduce firing without a large hyperpolarization.
5. In a robot simulation, identify one state variable, one measured input, and one parameter that a learning rule could change.

## References

References use IEEE-style numbered citations. Each citation number links to its entry; each entry links to the source.

(neuro-ref-1)=

[1] E. R. Kandel, J. H. Schwartz, T. M. Jessell, S. A. Siegelbaum, and A. J. Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013, chs. 2, 4, 6–8, and 10. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(neuro-ref-2)=

[2] W. Gerstner, W. M. Kistler, R. Naud, and L. Paninski, *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge, U.K.: Cambridge University Press, 2014, ch. 1. [Online textbook](https://neuronaldynamics.epfl.ch/online/Ch1.html).
