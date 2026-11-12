---
title: "Chapter 10 · Capstone: An Associative Learning Robot"
---

## 10.1 Learning objectives and experimental question

Can pairing a visual cue with a vibration cue make the visual cue alone elicit a motor response? You will define this question as a controlled experiment, connect sensing to neural inputs, separate training from evaluation, and report which components were actually run.

The course final project motivates a red visual CS, a vibration US, and a learned motion response. Related published work explores visual–vibration association with a mobile robot and neuromorphic computing [[1]](#capstone-ref-1). That publication's brightness cues, processing, network, and deployment differ from this red-cue teaching variant. Our compact NumPy/LIF experiment is executable; the Gazebo transfer is a guided extension requiring independent implementation and validation.

## 10.2 Four stages, one fixed response definition

| Stage | Inputs | Learning | Expected teaching behavior |
|---|---|---|---|
| Baseline CS test | Red cue alone | Disabled | No response with the initial weak CS weight |
| Baseline US test | Vibration alone | Disabled | Response through the fixed US pathway |
| Pairing | CS and US together | Enabled | CS weight increases under the declared rule |
| Recall test | CS alone | Disabled | Learned drive may cross the fixed response criterion |

These are operational labels for the experiment, not claims about an animal's experience. Choose the response criterion before training. [Laboratory 5](../notebooks/conditioning.ipynb) uses at least three LIF events during a 500 ms observation window, followed by a hypothetical 0.1 m/s command lasting 2 s. It reports the ideal 0.2 m consequence of that command, not measured robot displacement.

## 10.3 Connect the modules

```{mermaid}
flowchart TD
    A["RGB image → red feature / CS"] --> C["Weighted drive and declared learning rule"]
    B["IMU → causal vibration feature / US"] --> C
    C --> D["LIF readout → event-window criterion"]
    D --> E["Motor command and measured behavior"]
```

For the executable trial example, $x$ and $u$ are binary detected cues and the trainable CS connection follows

$$
y_k=\mathbf1[w_kx_k+u_k>0.5],\qquad
w_{k+1}=w_k+\eta x_ky_k(1-w_k).
$$

The US connection remains fixed. Chapter 4 derives the closed-form paired weight and compares this bounded coactivity rule with Oja and STDP. The spiking readout is evaluated separately with $I=50+200(wx+u)$ pA. Do not call this trial rule spike-timing-dependent plasticity, and do not claim that a trial-based teaching variable is an experimentally measured postsynaptic signal.

## 10.4 Worked experiment and parameter changes

Run the [notebook in Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/conditioning.ipynb), or {download}`download Laboratory 5 <../notebooks/conditioning.ipynb>`. It includes the complete physical-unit LIF implementation, training schedules, frozen probes, and two figures.

```python
# Run Laboratory 5 definitions first.
paired = train_association('paired', trials=12, eta=.1)
unpaired = train_association('unpaired', trials=12, eta=.1)
frozen = train_association('frozen', trials=12, eta=.1)
for label, weights in [('paired', paired), ('unpaired', unpaired), ('frozen', frozen)]:
    t, v, events, drive, ideal_distance = probe_association(weights[-1], cs=1, us=0)
    print(label, weights[-1], len(events), ideal_distance)
```

The paired weight reaches approximately 0.73169; the two controls remain 0.05. The paired CS-alone current is approximately 196.34 pA, compared with 60 pA before learning. At the fixed response criterion, the default paired model responds to CS after learning, while the controls do not.

```{figure} ../assets/conditioning-course-response.png
:label: fig-conditioning-response
:alt: Before and after CS-alone membrane voltage, separate event raster, and ideal travel after the probe window
:width: 100%

Original frozen-probe outputs. Voltage and spike events occupy different panels. The bottom panel is a post-probe ideal-distance calculation under a chosen motor command; it is not a Gazebo trajectory or a distance already traveled during the probe.
```

**Try three changes.** Reduce pairings to two; reduce learning rate to 0.02; increase the initial weight until CS already elicits a baseline response. For each, predict the weight, current, event count, and behavioral classification. The third change demonstrates why a successful final response is insufficient without a baseline.

## 10.5 Controls and held-out evaluation

Use matched exposure counts for paired and nonoverlapping unpaired schedules. Include a frozen-learning condition. For continuous signals, add a shuffled-timing control that preserves exposure but disrupts pairing; the notebook's binary nonoverlapping schedule is a simpler control, not that full time-shuffle experiment.

Hold preprocessing, neural parameters, observation window, and controller settings fixed across conditions. Freeze all weights during evaluation. Vary cue brightness, vibration amplitude, noise, and cue placement on held-out trials. Do not choose thresholds on those same tests. Reset state between trials, distinguish within-seed repeats from independent seeds, and report uncertainty for stochastic experiments. The default trial calculation is deterministic and does not require invented error bars.

## 10.6 Transfer to Gazebo and report evidence

Follow [Chapter 9](09-nengo-ros-gazebo.md)'s milestones. Use actual image and IMU messages to compute cues; log simulator stimulus labels only as evaluation ground truth. A stimulus flag fed directly to the neuron bypasses the perception problem.

| Evidence | Minimum report |
|---|---|
| Inputs | Images, IMU trace, extracted features, timestamps, masks |
| Neural activity | Voltage, separate event times, input scaling, response window |
| Learning | Weight trajectory, exact update equation, enabled/disabled intervals |
| Behavior | Command, measured pose/displacement, response criterion, failures |
| Controls | Baseline, unpaired exposure, frozen learning, held-out conditions |
| Reproducibility | Versions, seeds, reset procedure, logs, source commit |

Only call the Gazebo phase complete when those recordings exist. A physical robot and a neuromorphic-chip deployment require additional experiments; neither follows from a working NumPy association example. Likewise, this capstone does not yet establish navigation, place-cell learning, or a validated SFN architecture.

## 10.7 Exercises

1. Derive the minimum paired weight needed to exceed the passive LIF rheobase. Why does a three-event criterion add a finite-window requirement?
2. Compare nonoverlapping and shuffled controls for a temporally filtered input.
3. Design a train/test split that measures generalization across cue brightness.
4. Explain how a moving red object can expose a detector failure independently of learning.

## References

(capstone-ref-1)=

[1] Noah Zins, Yan Zhang, and Hongyu An, “Implementation of Associative Memory Learning in Mobile Robots Using Neuromorphic Computing,” in *Neuromorphic Computing*, 2023, doi: [10.5772/intechopen.110364](https://www.intechopen.com/chapters/86265).

## Additional Reading Materials

Read [[1]](#capstone-ref-1), noting which published choices differ from the course's red-cue project. Revisit [Chapter 4](04-hebbian-learning.md) for stabilization, STDP, and eligibility traces; compare Nengo's documented Oja rule before choosing it for an extension. Future spatial-memory and neuromorphic-hardware work is listed separately in the [roadmap](roadmap.md).
