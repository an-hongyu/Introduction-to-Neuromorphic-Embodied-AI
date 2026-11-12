---
title: "Chapter 9 · Nengo, ROS 2, and Gazebo Integration"
---

## 9.1 Learning objectives and scope

You will run one LIF neuron in Nengo, distinguish normalized neural values from physical units, define a sensor-to-controller message contract, and organize a staged ROS 2/Gazebo validation. The notebook experiment is executable and checked. **The ROS 2/Gazebo material below is an implementation and validation guide; a complete simulated robot is not supplied or claimed to have run in this release.**

## 9.2 One LIF neuron in Nengo

Nengo represents inputs with Nodes, neural populations with Ensembles, connections with Connection objects, and recorded values with Probes [[1]](#nengo-ref-1). Start with one neuron before introducing learned weights, sensor callbacks, or a robot.

[Laboratory 7](../notebooks/nengo_single_neuron.ipynb) runs a constant normalized current $J=1.5$ after 0.2 s, using $\tau_{\mathrm{RC}}=0.02$ s and $\tau_{\mathrm{ref}}=0.002$ s. In this convention the event threshold is 1 and reset is 0. For $J>1$,

$$
f(J)=\left[\tau_{\mathrm{ref}}+\tau_{\mathrm{RC}}\ln\left(\frac{J}{J-1}\right)\right]^{-1}.
$$

The analytical rate is about 41.71 Hz; the 1 ms-step simulation gives about 41.67 Hz. These normalized voltage and current values are not mV and pA. Compare with Chapter 2 only after deriving a conversion and aligning reset and refractory conventions.

```python
import nengo
with nengo.Network(seed=7) as network:
    stimulus = nengo.Node(lambda t: 1.5 if t >= .2 else 0.)
    cell = nengo.Ensemble(1, 1,
        neuron_type=nengo.LIF(tau_rc=.02, tau_ref=.002),
        gain=[2.], bias=[0.], encoders=[[1.]])
    # Neuron input is multiplied by gain=2. Compensate to deliver J=1.5.
    nengo.Connection(stimulus, cell.neurons, transform=.5, synapse=None)
    spike_probe = nengo.Probe(cell.neurons)
    voltage_probe = nengo.Probe(cell.neurons, 'voltage')
with nengo.Simulator(network, dt=.001, progress_bar=False) as sim:
    sim.run(.8)
```

The gain compensation is essential: omitting `transform=.5` doubles the effective current and produces a much higher rate. Connect directly to `cell.neurons` here so the example tests an explicit single-cell current rather than an ensemble's decoded representation. Probe output pulses are scaled by the inverse time step; identify events with a positive-output test, not by interpreting pulse amplitude as voltage.

```{figure} ../assets/nengo-course-neuron.png
:label: fig-nengo-course-neuron
:alt: Nengo normalized membrane voltage in the upper panel and a separate aligned event raster in the lower panel
:width: 100%

Original Nengo 4.0.0 experiment. Change normalized current or either time constant in the notebook. The input begins at 0.2 s; voltage and events remain separate.
```

The repository pins Nengo 4.0.0 with NumPy 1.26.4. For Colab, run `%pip install numpy==1.26.4 nengo==4.0.0 contourpy==1.3.3` before importing NumPy; restart the runtime if an incompatible NumPy version was already loaded, then run the notebook. The repository's Python 3.12 environment installs these dependencies together.

## 9.3 A reproducible teaching profile

Use Ubuntu 24.04, ROS 2 Jazzy, and Gazebo Harmonic for a documented long-term-support pairing [[2]](#nengo-ref-2). Record exact package versions in the experiment log. Existing Humble installations should follow their supported Gazebo pairing rather than mixing commands across distributions. This profile is a recommendation for the integration exercise, not evidence that this repository has installed or tested that simulator stack.

Begin with a robot that can publish sensor messages and accept velocity commands without a neural model. Then test the encoder on recorded messages. Only afterward connect the neural output. This ordering lets a failed stage be diagnosed independently.

## 9.4 Topic and timing contract

The following names are proposed teaching interfaces; inspect the running robot because actual names and message types vary. ROS message definitions specify units and fields [[3]](#nengo-ref-3).

| Proposed topic | Message | Required interpretation |
|---|---|---|
| `/camera/image_raw` | `sensor_msgs/Image` | Encoding, row stride, timestamp, and optical frame; convert RGB/BGR deliberately |
| `/imu` | `sensor_msgs/Imu` | m/s² and rad/s, frame, covariance, orientation availability |
| `/scan` | `sensor_msgs/LaserScan` | Radians, metres, range limits, scan timing, sensor frame |
| `/cmd_vel` | `geometry_msgs/Twist` | Linear m/s and angular rad/s in the controller's documented frame |
| `/neural_state` | Experiment-defined log | Neural step, features, masks, events, weights, and learning-enabled flag |

Some controllers use stamped velocity commands. Match the controller's configured type before publishing. Use simulation time consistently; keep message age limits and the neural update interval explicit. Do not equate one asynchronous callback with one fixed neural step. Buffer or resample inputs onto a declared time grid and record the age of every value used.

## 9.5 Validation milestones

1. **Simulator baseline:** demonstrate camera, IMU, and range topics; record frames, rates, and a short bag. Confirm zero commands stop the robot.
2. **Encoder replay:** feed the same recorded inputs into the sensory notebook functions; compare features with the synthetic tests.
3. **Neural replay:** reproduce the single-neuron rate check and separate voltage/event plots; reset state between trials.
4. **Controller connection:** gate a bounded velocity command using a declared event-window criterion. Stop on stale or invalid required inputs; log the reason.
5. **Learning trials:** follow Chapter 10's pairing, frozen tests, and controls with identical preprocessing and controller settings.

Save sensor features, model parameters, random seed, software versions, spikes, weights, commands, and measured pose. An ideal command of 0.1 m/s for 2 s predicts 0.2 m of straight travel; actual displacement needs odometry or ground-truth measurement and may differ because of acceleration limits, contact, or slip. The notebook does not measure that displacement.

## 9.6 Exercises

1. Remove gain compensation and explain the rate change before running.
2. Choose neural and sensor update rates; specify how stale measurements are detected.
3. Separate camera detection failure from association failure in a trial log.
4. Design a reset procedure for sensor buffers, neuron state, weights, and simulated pose.

## References

(nengo-ref-1)=

[1] Nengo developers, “Frontend API,” ver. 4.0.0. [API documentation](https://www.nengo.ai/nengo/v4.0.0/frontend-api.html).

(nengo-ref-2)=

[2] Gazebo contributors, “Installing Gazebo with ROS,” *Gazebo Harmonic documentation*. [Supported pairings](https://gazebosim.org/docs/harmonic/ros_installation/).

(nengo-ref-3)=

[3] ROS 2 contributors, *common_interfaces*, Jazzy branch. [Official message definitions](https://github.com/ros2/common_interfaces/tree/jazzy).

## Additional Reading Materials

After the single-cell example, read Nengo's [unsupervised learning example](https://www.nengo.ai/nengo/v4.0.0/examples/learning/learn-unsupervised.html) for the actual Oja API. It learns neural connections under its stated restrictions; it is distinct from Chapter 4's bounded trial rule. Use the course's ROS, Nengo, and Gazebo project material alongside the message contracts and milestones above.
