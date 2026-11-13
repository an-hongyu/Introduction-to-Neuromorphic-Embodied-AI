---
title: "Chapter 3 · Hebbian Learning and Synaptic Plasticity"
---

## 3.1 Learning objectives: changing connections through experience

The previous chapters introduced biological signaling and computational neuron dynamics. A network with fixed parameters can respond to input without learning. This chapter introduces rules that change connections according to activity, beginning with the organizing idea associated with Hebb [[1]](#hebb-ref-1).

By the end of this chapter, you should be able to:

- Explain how paired neural activity can increase the response to the same presynaptic stimulus.
- Write a local two-factor Hebbian update and compare potentiation and depression in four rate-threshold rules.
- Explain why unconstrained Hebbian growth can be unstable and how Oja's rule addresses it.
- Interpret a continuous rate-dependent learning threshold.
- Distinguish firing-rate plasticity from spike-timing-dependent plasticity (STDP), using a stated spike-time sign convention.
- Explain how a third factor can modulate a stored eligibility trace.

Hebb's proposal concerns strengthening a connection when presynaptic activity repeatedly contributes to postsynaptic activation. A simple correlation rule is one mathematical interpretation, not the complete original theory and not a universal rule for every synapse. Biological plasticity depends on cell type, signaling pathways, activity history, and experimental conditions [[2]](#hebb-ref-2).

## 3.2 A two-factor Hebbian rule

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

## 3.3 Biological potentiation and a computational learning rule

Long-term potentiation (LTP) describes a persistent increase in synaptic efficacy under specified experimental protocols; long-term depression (LTD) describes a persistent decrease. A classic study demonstrated lasting potentiation in the rabbit dentate area following stimulation of the perforant path [[3]](#hebb-ref-3). These observations motivate plasticity models, but “LTP,” “Hebbian learning,” and “memory” are not interchangeable terms.

For example, a positive numerical weight update is not by itself an LTP experiment. It specifies no transmitter, receptor, induction protocol, or persistence mechanism. Conversely, synaptic changes can involve mechanisms that a scalar weight does not distinguish. Our goal is to make a useful model with an explicit scope and connect it to relevant evidence, not assign every line of code a unique biological mechanism.

### 3.3.1 What changes after a Hebbian pairing protocol?

The lecture builds a three-stage experiment [[8]](#hebb-ref-8), slides 18–21. **Before pairing**, a presynaptic test spike evokes a small excitatory postsynaptic potential (EPSP), but the postsynaptic cell does not fire. **During pairing**, presynaptic and postsynaptic activity occur together. **After pairing**, the same presynaptic test stimulus can evoke a larger EPSP, indicating increased effective synaptic transmission under the conditions of the experiment.

```{figure} ../assets/hebb-course/hebbian-pairing-protocol.svg
:label: fig-hebbian-pairing-protocol
:alt: Three stages: a presynaptic test spike evokes a small subthreshold EPSP, paired pre- and postsynaptic spikes form the training episode, and the same test input later evokes a larger EPSP.
:width: 100%

**An illustrative pairing protocol.** A controlled comparison of the same input before and after coactivity is more informative than observing firing during training alone. Redrawn from the course lecture, slides 19–21 [[8]](#hebb-ref-8). The pictured change is a teaching schematic, not a numerical outcome measured in this book.

```

To interpret a larger test response as a lasting synaptic change, the induction and test conditions, recording site, baseline stability, and duration of persistence must be specified. A larger EPSP by itself does not identify the underlying receptor or release mechanism; simultaneous voltage summation and altered intrinsic excitability also need suitable controls.

### 3.3.2 Four rate-threshold variants of Hebbian plasticity

The lecture compares **four alternative rules** [[8]](#hebb-ref-8), slides 24–28. Classify presynaptic and postsynaptic activities as *high* if their rates exceed a chosen threshold $r_T$, and *low* otherwise. Each rule strengthens a connection when both rates are high, but they differ in which mismatched states produce long-term depression (LTD).

```{figure} ../assets/hebb-course/four-hebbian-threshold-rules.svg
:label: fig-hebbian-threshold-rules
:alt: Four quadrant diagrams compare LTP and LTD for high and low presynaptic and postsynaptic firing rates under four alternative threshold-based learning rules.
:width: 100%

**Four possible update maps.** Green indicates potentiation, red indicates depression, and white indicates no modeled update. Adapted from lecture slides 24–28 [[8]](#hebb-ref-8). These maps are modeling alternatives, not four mandatory steps of one biological learning process.

```

| Presynaptic / postsynaptic activity | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|---|---|---|---|---|
| High / high | LTP | LTP | LTP | LTP |
| High / low | No update | LTD | LTD | No update |
| Low / high | No update | LTD | No update | LTD |
| Low / low | No update | No update | No update | No update |

For **Rule 1**, a continuous-time illustrative gate is

$
\tau_w\frac{dw_{ji}}{dt}=
H(r_{\mathrm{pre}}-r_T)\,
H(r_{\mathrm{post}}-r_T),
$

where $H(z)=1$ for $z>0$ and $H(z)=0$ for $z\leq0$. Here $w_{ji}$ is a dimensionless weight and $\tau_w$ sets an update time scale. The choice at exactly $r_T$ is a modeling convention. The rule ignores spike ordering and gives no depression. Rules 2–4 instead prescribe depression for different mismatched activity states.

These rate-threshold diagrams are simple phenomenological descriptions of activity-dependent strengthening and weakening. They should not be interpreted as universally applicable biological induction protocols.

## 3.4 Correlation, covariance, and uncontrolled growth

With nonnegative $x_i$ and $y_j$, the basic rule only increases active weights. If $y_j$ is itself driven by those weights, positive feedback can make them grow without bound. Setting a smaller learning rate slows growth but does not provide a general stability guarantee.

A covariance-style alternative uses deviations from running mean activity:

$$
\Delta w_{ji}=\eta(y_j-\overline y_j)(x_i-\overline x_i).
$$

This distinguishes above- and below-average activity in the model. It can produce positive or negative updates; it also requires a definition of how means are estimated and on what time scale. A negative update to an excitatory weight means weakening that weight, not automatically converting it into a biologically inhibitory synapse.

Several constraints are possible: bounded weights, decay, normalization, competition, and homeostatic regulation. Each changes the learning dynamics. A model should name the constraint and test its effect rather than add it invisibly when weights become numerically inconvenient [[2]](#hebb-ref-2).

### 3.4.1 A continuous rule with a postsynaptic rate threshold

The lecture also replaces binary gates with a smooth rule [[8]](#hebb-ref-8), slide 29. For clarity about units, normalize firing rates using a declared reference $r_0>0$: $\rho_{\mathrm{pre}}=r_{\mathrm{pre}}/r_0$, $\rho_{\mathrm{post}}=r_{\mathrm{post}}/r_0$, and $\rho_T=r_T/r_0$. A dimensionally consistent version of the slide's functional form is

$
\tau_w\frac{dw_{ji}}{dt} =
\rho_{\mathrm{pre}}\,\rho_{\mathrm{post}}
(\rho_{\mathrm{post}}-\rho_T).
$

With positive presynaptic activity, the **postsynaptic rate determines the sign**: activity below threshold depresses the weight, activity above threshold potentiates it, and equality gives zero update. Presynaptic activity scales the magnitude. The shape of this curve is not an experimentally fitted law and does not guarantee bounded learning.

```{figure} ../assets/hebb-course/rate-threshold-plasticity.svg
:label: fig-hebbian-continuous-threshold
:alt: The continuous rate-learning update crosses zero at 15 Hz postsynaptic firing rate, with depression below the threshold and potentiation above it.
:width: 92%

**Continuous rate-threshold plasticity.** An illustrative threshold $r_T=15$ Hz separates negative and positive updates for fixed positive presynaptic activity. Redrawn from lecture slide 29 [[8]](#hebb-ref-8). The vertical magnitude is a scaled model quantity.

```

**Worked comparison.** Set $r_0=10$ Hz, $r_{\mathrm{pre}}=10$ Hz, $r_T=15$ Hz, and $\tau_w=10$ s. At $r_{\mathrm{post}}=5$ Hz, the right-hand side is $(1)(0.5)(0.5-1.5)=-0.5$, giving $dw/dt=-0.05\,\mathrm{s}^{-1}$. At $r_{\mathrm{post}}=20$ Hz, it is $(1)(2)(2-1.5)=1$, giving $dw/dt=+0.10\,\mathrm{s}^{-1}$. These are chosen normalized teaching values, not measured plasticity rates.

## 3.5 Oja's rule: learning with a stabilizing term

For a single linear output $y=\mathbf w^\top\mathbf x$, Oja's rule adds activity-dependent normalization [[4]](#hebb-ref-4):

$$
\Delta\mathbf w=\eta y(\mathbf x-y\mathbf w).
$$

The first term is Hebbian; the second opposes growth along the current weight vector. With suitably small learning steps and appropriate assumptions on stationary, zero-mean inputs, the rule is related to learning a principal direction of the input covariance. This does not mean that any nonlinear spiking circuit using an Oja-like term is guaranteed to perform principal-component analysis.

**Worked example.** Let $\mathbf x=(1,0)$ and $\mathbf w=(0.6,0.8)$. Then $y=0.6$. At $\eta=0.1$, $\Delta\mathbf w=(0.0384,-0.0288)$. The new weight vector is $(0.6384,0.7712)$. Its norm remains near one for this small step, but discrete updates do not enforce exact normalization at every iteration.

## 3.6 Spike-timing-dependent plasticity

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


```{figure} ../assets/hebb-course/stdp-spike-ordering.svg
:label: fig-hebbian-stdp-ordering
:alt: Spike timing shows pre-before-post associated with positive delta t and potentiation, and post-before-pre with negative delta t and depression, plus an exponential learning window.
:width: 100%

**Spiking order matters.** When the presynaptic spike precedes the postsynaptic spike, $\Delta t>0$ in this chapter and the illustrative window potentiates the connection; reversing the order gives $\Delta t<0$ and depression. Adapted from lecture slides 30–34 [[8]](#hebb-ref-8). The source slides plot the *opposite* horizontal sign convention; the figure has been redrawn to agree with the equation above.

```

A rate rule can give identical updates to spike trains with the same average rates even when individual spike order is reversed. STDP distinguishes those cases by construction. Biological STDP windows may differ in shape, polarity, and cell-type dependence; the sign convention and model parameters must be specified independently of the diagram.

## 3.7 Eligibility traces and a third factor

A reward may arrive after the neural events that should receive credit. A **three-factor** learning rule can retain a local eligibility state and modulate its effect with another signal [[6]](#hebb-ref-6):

$$
\tau_e\frac{de_{ji}}{dt}=-e_{ji}+f\!\left(x_i,y_j\right),
\qquad
\frac{dw_{ji}}{dt}=\eta M(t)e_{ji}(t).
$$

$e_{ji}$ is an eligibility trace; $\tau_e$ is its decay time constant; $f$ forms local coactivity; and $M(t)$ is a modulatory signal. Here $f$ and $e$ share units, and $\eta$ must make the weight derivative dimensionally consistent. The modulator might represent a reward-related quantity in a chosen algorithm; it is not automatically identical to a measured dopamine signal.

If a trace is set to 1 and receives no further input, it decays to $e^{-\Delta/\tau_e}$ after delay $\Delta$. With $\tau_e=0.5$ s, a reward arriving 0.5 s later encounters a trace of approximately 0.368. A much later reward has less effect under this chosen decay law. This is a mechanism for retaining candidate credit, not a guarantee of correct causal attribution.

## 3.8 Worked example: association, partial cues, and interference

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

### 3.8.1 Course case — a visual cue acquires a motor response

Use a red visual cue as the conditioned stimulus (CS) and vibration as the unconditioned stimulus (US). Before training, US alone drives the output; CS alone does not. Pair them, freeze learning, then probe CS alone. This course variant is motivated by associative robotic learning [[7]](#hebb-ref-7). The published system uses different visual processing, network details, and hardware; our small example is not its reproduction.

Let $x,u\in\{0,1\}$ denote detected CS and US, $w$ the CS weight, and $y=\mathbf1[wx+u>0.5]$ a trial-level teaching response. Choose a **bounded coactivity rule**:

$$
w_{k+1}=w_k+\eta x_k y_k(1-w_k),\qquad 0\leq\eta\leq1.
$$

All variables here are dimensionless. This is a chosen saturation rule, not Oja's rule or STDP. During paired trials $x=y=1$, so $w_k=1-(1-w_0)(1-\eta)^k$. With $w_0=0.05$, $\eta=0.1$, and 12 pairings, $w_{12}\approx0.73169$. Nonoverlapping CS and US presentations leave the weight unchanged in the default unpaired control because isolated CS never crosses the teaching threshold.

```python
# Standalone trial-level calculation; no simulator required.
w, eta = 0.05, 0.1
for _ in range(12):
    cs, us = 1.0, 1.0
    response = float(w * cs + us > 0.5)
    w += eta * cs * response * (1 - w)
print(w)  # 0.73169194034305
```

A separate LIF readout receives $I=50+200(wx+u)$ pA. CS alone therefore supplies 60 pA before learning and about 196.34 pA afterward. Use the Chapter 2 parameters and a fixed 500 ms probe; at least three events count as a response. Learning stays disabled throughout every probe. The trial-level variable $y$ trains the weight; the spiking readout evaluates its consequence. It does not retroactively supply spike-timing-dependent updates.

```{figure} ../assets/conditioning-course-learning.png
:label: fig-conditioning-learning
:alt: Paired, unpaired, and frozen learning weights and before versus after frozen-probe spike counts
:width: 100%

Original synthetic results. Both unpaired and frozen-learning controls retain the initial weight. A larger learned weight alone is insufficient: compare the held-out response conditions too.
```

[Laboratory 5](../notebooks/conditioning.ipynb) contains the complete training function, physical-unit LIF readout, and controls. Change learning rate, trial count, or initial weight. A larger initial weight can make CS effective before pairing and change the unpaired control; state these conditions when interpreting results. [Chapter 10](10-associative-learning-robot.md) turns this example into a staged robot experiment with separate sensing, learning, and behavioral evaluation.

## 3.9 Connecting spatial representations to behavior

A place-like population might provide context, an action population might describe a candidate movement, and a reward-related signal might modulate a local trace. This is a useful way to formulate a testable robot learning architecture. It still requires explicit action selection, weight constraints, exploration, and evaluation.

For example, test whether a robot can recall an association from a partial cue, whether unrelated associations interfere, whether the rule changes behavior after a goal moves, and whether the same behavior appears with learning disabled. Keep training experiences separate from held-out evaluation conditions. A weight heatmap alone demonstrates a parameter change; a controlled behavioral comparison is needed to establish a benefit to navigation.

Later SFN material will build on these ideas as a proposed research framework. Its rules, capacity, and consolidation behavior should be identified as hypotheses until evaluated; they should not be presented as consequences of Hebb's original proposal.

## 3.10 Exercises

1. Starting at $w=0.4$, compute ten updates with $x=y=1$ and $\eta=0.02$. Why does this rule need a growth constraint?
2. Derive the shape of $\mathbf y\mathbf x^\top$ for 36 inputs and 10 outputs.
3. Calculate the STDP update at $\Delta t=-10$ ms for $A_-=0.012$ and $\tau_-=20$ ms.
4. Explain why the shared cue in the association example cannot distinguish the two stored patterns.
5. Compare recall before learning, after learning, and after shuffling the supplied pairings.
6. Design a reward-delay experiment that separates an eligibility-trace model from an instantaneous two-factor rule.

## References

(hebb-ref-1)=

[1] Donald O. Hebb, *The Organization of Behavior: A Neuropsychological Theory*. New York, NY, USA: Wiley, 1949. [Original-edition catalog record](https://wellcomecollection.org/works/g4sfzum4); [publisher's 2002 reissue](https://www.routledge.com/The-Organization-of-Behavior-A-Neuropsychological-Theory/Hebb/p/book/9780805843002).

(hebb-ref-2)=

[2] Eric R. Kandel, James H. Schwartz, Thomas M. Jessell, Steven A. Siegelbaum, and Albert James Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013, chs. 65–67. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(hebb-ref-3)=

[3] Timothy V. P. Bliss and Terje Lømo, “Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit following stimulation of the perforant path,” *The Journal of Physiology*, vol. 232, no. 2, pp. 331–356, 1973, doi: [10.1113/jphysiol.1973.sp010273](https://pubmed.ncbi.nlm.nih.gov/4727084/).

(hebb-ref-4)=

[4] Erkki Oja, “A simplified neuron model as a principal component analyzer,” *Journal of Mathematical Biology*, vol. 15, no. 3, pp. 267–273, 1982, doi: [10.1007/BF00275687](https://pubmed.ncbi.nlm.nih.gov/7153672/).

(hebb-ref-5)=

[5] Guo-qiang Bi and Mu-ming Poo, “Synaptic modifications in cultured hippocampal neurons: Dependence on spike timing, synaptic strength, and postsynaptic cell type,” *The Journal of Neuroscience*, vol. 18, no. 24, pp. 10464–10472, 1998, doi: [10.1523/JNEUROSCI.18-24-10464.1998](https://pubmed.ncbi.nlm.nih.gov/9852584/).

(hebb-ref-6)=

[6] Wulfram Gerstner, Marco Lehmann, Vasiliki Liakoni, Dane Corneil, and Johanni Brea, “Eligibility traces and plasticity on behavioral time scales: Experimental support of neoHebbian three-factor learning rules,” *Frontiers in Neural Circuits*, vol. 12, Art. no. 53, 2018, doi: [10.3389/fncir.2018.00053](https://pubmed.ncbi.nlm.nih.gov/30108488/).


(hebb-ref-7)=

[7] Noah Zins, Yan Zhang, and Hongyu An, “Implementation of Associative Memory Learning in Mobile Robots Using Neuromorphic Computing,” in *Neuromorphic Computing*, 2023, doi: [10.5772/intechopen.110364](https://www.intechopen.com/chapters/86265).

(hebb-ref-8)=

[8] H. An, *Neuromorphic Robotic Systems: Computational Models of Neural Systems—Hebbian's Rule*, lecture slides, Department of Electrical and Computer Engineering, Michigan Technological University, n.d., slides 18–34. Author-supplied PowerPoint.

(hebb-ref-9)=

[9] P. Miller, *An Introductory Course in Computational Neuroscience*. Cambridge, MA, USA: MIT Press, 2018. Listed as additional background reading in the supplied lecture, slide 35.

## Additional Reading Materials

Read Hebb's original proposal [[1]](#hebb-ref-1) alongside the course lecture's pairing and threshold-rule illustrations [[8]](#hebb-ref-8). For further background on rate-based modeling, see Miller [[9]](#hebb-ref-9). Then compare the explicit stabilization in Oja [[4]](#hebb-ref-4), the experimental timing dependence in Bi and Poo [[5]](#hebb-ref-5), and the delayed modulation discussed in Gerstner et al. [[6]](#hebb-ref-6). Read the robot chapter [[7]](#hebb-ref-7) alongside our course variant and list the differences in cues, learning rule, and deployment.
