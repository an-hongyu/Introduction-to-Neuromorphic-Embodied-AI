---
title: "Chapter 4 · Hebbian Learning"
---

# 4. Hebbian Learning

## 4.1 Learning objectives: changing connections through experience

The previous chapters introduced signals, representations, and neuron dynamics. A network with fixed parameters can respond to input without learning. This chapter introduces rules that change connections according to activity, beginning with the organizing idea associated with Hebb [[1]](#hebb-ref-1).

After this chapter, you should be able to write a local two-factor update, explain why unconstrained Hebbian growth is unstable, distinguish rate-based learning from spike-timing-dependent plasticity, and describe how a third factor can modulate a stored eligibility trace.

Hebb's proposal concerns strengthening a connection when presynaptic activity repeatedly contributes to postsynaptic activation. A simple correlation rule is one mathematical interpretation, not the complete original theory and not a universal rule for every synapse. Biological plasticity depends on cell type, signaling pathways, activity history, and experimental conditions [[2]](#hebb-ref-2).

## 4.2 A two-factor Hebbian rule

Let $x_i$ be presynaptic activity, $y_j$ postsynaptic activity, and $w_{ji}$ the weight **from input $i$ to output $j$**. For dimensionless activities sampled once per learning step, a simple rule is

$$
\Delta w_{ji}=\eta y_jx_i,
\qquad
w_{ji}\leftarrow w_{ji}+\Delta w_{ji}.
$$

$\eta$ is a learning-rate parameter. This is called a **two-factor** rule because the update depends on both presynaptic and postsynaptic activity. Locality means that the required variables are available at or near the synapse in the model; it does not mean that all needed biological mechanisms have been demonstrated.

**Worked example.** With $x_i=0.5$, $y_j=0.6$, and $\eta=0.01$, the increment is 0.003. A weight of 0.2 becomes 0.203. If either activity is zero, this particular rule gives no update. If activities carry physical units such as Hz, the learning coefficient must have corresponding units; do not reuse a dimensionless coefficient without specifying the normalization.

For vector activities, the same update is an outer product,

$$
\Delta\mathbf W=\eta\mathbf y\mathbf x^\top.
$$

If there are three inputs and two outputs, $\mathbf W$ has shape $2\times3$. Reversing this convention silently changes the interpretation of a connection matrix.

## 4.3 Biological potentiation and a computational learning rule

Long-term potentiation (LTP) describes a persistent increase in synaptic efficacy under specified experimental protocols; long-term depression (LTD) describes a persistent decrease. A classic study demonstrated lasting potentiation in the rabbit dentate area following stimulation of the perforant path [[3]](#hebb-ref-3). These observations motivate plasticity models, but “LTP,” “Hebbian learning,” and “memory” are not interchangeable terms.

For example, a positive numerical weight update is not by itself an LTP experiment. It specifies no transmitter, receptor, induction protocol, or persistence mechanism. Conversely, synaptic changes can involve mechanisms that a scalar weight does not distinguish. Our goal is to make a useful model with an explicit scope and connect it to relevant evidence, not assign every line of code a unique biological mechanism.

## 4.4 Correlation, covariance, and uncontrolled growth

With nonnegative $x_i$ and $y_j$, the basic rule only increases active weights. If $y_j$ is itself driven by those weights, positive feedback can make them grow without bound. Setting a smaller learning rate slows growth but does not provide a general stability guarantee.

A covariance-style alternative uses deviations from running mean activity:

$$
\Delta w_{ji}=\eta(y_j-\overline y_j)(x_i-\overline x_i).
$$

This distinguishes above- and below-average activity in the model. It can produce positive or negative updates; it also requires a definition of how means are estimated and on what time scale. A negative update to an excitatory weight means weakening that weight, not automatically converting it into a biologically inhibitory synapse.

Several constraints are possible: bounded weights, decay, normalization, competition, and homeostatic regulation. Each changes the learning dynamics. A model should name the constraint and test its effect rather than add it invisibly when weights become numerically inconvenient [[2]](#hebb-ref-2).

## 4.5 Oja's rule: learning with a stabilizing term

For a single linear output $y=\mathbf w^\top\mathbf x$, Oja's rule adds activity-dependent normalization [[4]](#hebb-ref-4):

$$
\Delta\mathbf w=\eta y(\mathbf x-y\mathbf w).
$$

The first term is Hebbian; the second opposes growth along the current weight vector. With suitably small learning steps and appropriate assumptions on stationary, zero-mean inputs, the rule is related to learning a principal direction of the input covariance. This does not mean that any nonlinear spiking circuit using an Oja-like term is guaranteed to perform principal-component analysis.

**Worked example.** Let $\mathbf x=(1,0)$ and $\mathbf w=(0.6,0.8)$. Then $y=0.6$. At $\eta=0.1$, $\Delta\mathbf w=(0.0384,-0.0288)$. The new weight vector is $(0.6384,0.7712)$. Its norm remains near one for this small step, but discrete updates do not enforce exact normalization at every iteration.

## 4.6 Spike-timing-dependent plasticity

Rate rules average activity over windows. **Spike-timing-dependent plasticity (STDP)** makes the update depend on relative spike timing. Bi and Poo demonstrated timing-dependent potentiation and depression in cultured hippocampal neurons, with effects also depending on initial synaptic strength and postsynaptic cell type [[5]](#hebb-ref-5).

Define the timing difference as

$$
\Delta t=t_{\mathrm{post}}-t_{\mathrm{pre}}.
$$

An illustrative pair-based window is

$$
\Delta w=
\begin{cases}
 A_+e^{-\Delta t/\tau_+}, & \Delta t>0,\\
 -A_-e^{\Delta t/\tau_-}, & \Delta t<0,\\
 0, & \Delta t=0.
\end{cases}
$$

Here $A_+$ and $A_-$ set update magnitudes; $\tau_+$ and $\tau_-$ set time scales. The zero-lag value is an explicit convention in this teaching model. The sign convention matters: a presynaptic spike followed 10 ms later by a postsynaptic spike has $\Delta t=+10$ ms.

For $A_+=0.01$ and $\tau_+=20$ ms, that pair produces $\Delta w\approx0.00607$. A postsynaptic spike occurring first gives a negative timing difference and uses the depression branch. A complete implementation must also state how pairs are selected, how repeated spikes are handled, and how weights are bounded. This exponential window is a phenomenological approximation, not a fit to every synapse.

## 4.7 Eligibility traces and a third factor

A reward may arrive after the neural events that should receive credit. A **three-factor** learning rule can retain a local eligibility state and modulate its effect with another signal [[6]](#hebb-ref-6):

$$
\tau_e\frac{de_{ji}}{dt}=-e_{ji}+f\!\left(x_i,y_j\right),
\qquad
\frac{dw_{ji}}{dt}=\eta M(t)e_{ji}(t).
$$

$e_{ji}$ is an eligibility trace; $\tau_e$ is its decay time constant; $f$ forms local coactivity; and $M(t)$ is a modulatory signal. Here $f$ and $e$ share units, and $\eta$ must make the weight derivative dimensionally consistent. The modulator might represent a reward-related quantity in a chosen algorithm; it is not automatically identical to a measured dopamine signal.

If a trace is set to 1 and receives no further input, it decays to $e^{-\Delta/\tau_e}$ after delay $\Delta$. With $\tau_e=0.5$ s, a reward arriving 0.5 s later encounters a trace of approximately 0.368. A much later reward has less effect under this chosen decay law. This is a mechanism for retaining candidate credit, not a guarantee of correct causal attribution.

## 4.8 Worked example: association, partial cues, and interference

Consider three input features and two output labels. During an explicitly supplied pairing phase, present

$$
\mathbf x^{(1)}=(1,1,0)^\top,\quad\mathbf y^{(1)}=(1,0)^\top,
\qquad
\mathbf x^{(2)}=(0,1,1)^\top,\quad\mathbf y^{(2)}=(0,1)^\top.
$$

Starting with zero weights, eight repetitions of both pairs at $\eta=0.1$ give

$$
\mathbf W=
\begin{bmatrix}
0.8&0.8&0\\
0&0.8&0.8
\end{bmatrix}.
$$

```python
import numpy as np
patterns = np.array([[1., 1., 0.], [0., 1., 1.]])
paired_outputs = np.eye(2)
weights = np.zeros((2, 3))
for _ in range(8):
    for x, y in zip(patterns, paired_outputs):
        weights += 0.1 * np.outer(y, x)
for cue in ([1., 0., 0.], [0., 0., 1.], [0., 1., 0.]):
    print(cue, "->", weights @ np.array(cue))
```

The first two partial cues produce output scores $(0.8,0)$ and $(0,0.8)$. The shared feature produces $(0.8,0.8)$ and is ambiguous. The scores are not calibrated probabilities, and a tie-breaking decision would be an additional rule.

The output patterns are supplied during pairing. This is a controlled associative-memory demonstration, not evidence that an autonomous agent discovered the labels, learned a navigation policy, or consolidated a biological memory. The [Hebbian learning notebook](../notebooks/hebbian_learning.ipynb) reproduces the matrix and plots both partial-cue responses and the illustrative STDP window.

```{figure} ../assets/hebbian-learning.png
:label: fig-hebbian-learning
:alt: Learned association matrix, partial-cue output scores including an ambiguous shared cue, and a synthetic STDP learning window
:width: 100%

A bounded-duration teaching experiment: paired-pattern outer-product learning, partial-cue recall, and a separately illustrated STDP rule. The STDP window does not train the matrix shown in the first panel.
```

## 4.9 Connecting spatial representations to behavior

A place-like population might provide context, an action population might describe a candidate movement, and a reward-related signal might modulate a local trace. This is a useful way to formulate a testable robot learning architecture. It still requires explicit action selection, weight constraints, exploration, and evaluation.

For example, test whether a robot can recall an association from a partial cue, whether unrelated associations interfere, whether the rule changes behavior after a goal moves, and whether the same behavior appears with learning disabled. Keep training experiences separate from held-out evaluation conditions. A weight heatmap alone demonstrates a parameter change; a controlled behavioral comparison is needed to establish a benefit to navigation.

Later SFN material will build on these ideas as a proposed research framework. Its rules, capacity, and consolidation behavior should be identified as hypotheses until evaluated; they should not be presented as consequences of Hebb's original proposal.

## 4.10 Exercises

1. Starting at $w=0.4$, compute ten updates with $x=y=1$ and $\eta=0.02$. Why does this rule need a growth constraint?
2. Derive the shape of $\mathbf y\mathbf x^\top$ for 36 inputs and 10 outputs.
3. Calculate the STDP update at $\Delta t=-10$ ms for $A_-=0.012$ and $\tau_-=20$ ms.
4. Explain why the shared cue in the association example cannot distinguish the two stored patterns.
5. Compare recall before learning, after learning, and after shuffling the supplied pairings.
6. Design a reward-delay experiment that separates an eligibility-trace model from an instantaneous two-factor rule.

## References

(hebb-ref-1)=

[1] D. O. Hebb, *The Organization of Behavior: A Neuropsychological Theory*. New York, NY, USA: Wiley, 1949. [Original-edition catalog record](https://wellcomecollection.org/works/g4sfzum4); [publisher's 2002 reissue](https://www.routledge.com/The-Organization-of-Behavior-A-Neuropsychological-Theory/Hebb/p/book/9780805843002).

(hebb-ref-2)=

[2] E. R. Kandel, J. H. Schwartz, T. M. Jessell, S. A. Siegelbaum, and A. J. Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013, chs. 65–67. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(hebb-ref-3)=

[3] T. V. P. Bliss and T. Lømo, “Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path,” *J. Physiol.*, vol. 232, no. 2, pp. 331–356, 1973, doi: [10.1113/jphysiol.1973.sp010273](https://doi.org/10.1113/jphysiol.1973.sp010273).

(hebb-ref-4)=

[4] E. Oja, “A simplified neuron model as a principal component analyzer,” *J. Math. Biol.*, vol. 15, no. 3, pp. 267–273, 1982, doi: [10.1007/BF00275687](https://doi.org/10.1007/BF00275687).

(hebb-ref-5)=

[5] G.-Q. Bi and M.-M. Poo, “Synaptic modifications in cultured hippocampal neurons: Dependence on spike timing, synaptic strength, and postsynaptic cell type,” *J. Neurosci.*, vol. 18, no. 24, pp. 10464–10472, 1998, doi: [10.1523/JNEUROSCI.18-24-10464.1998](https://doi.org/10.1523/JNEUROSCI.18-24-10464.1998).

(hebb-ref-6)=

[6] W. Gerstner, M. Lehmann, V. Liakoni, D. Corneil, and J. Brea, “Eligibility traces and plasticity on behavioral time scales: Experimental support of neoHebbian three-factor learning rules,” *Front. Neural Circuits*, vol. 12, Art. no. 53, 2018, doi: [10.3389/fncir.2018.00053](https://doi.org/10.3389/fncir.2018.00053).
