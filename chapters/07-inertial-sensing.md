---
title: "Chapter 6 · Inertial Sensing and Vibration Encoding"
---

## 6.1 Learning objectives

By the end of this chapter, you should be able to:

- Distinguish acceleration, angular velocity, and orientation.
- Implement a causal vibration detector.
- Calculate the latency introduced by the detector's analysis window.
- Identify when gravity compensation is required for inertial measurements. In the course project, a vibration cue provides the US. It must be detected from a sensor signal rather than substituted with a simulation's hidden stimulus flag.

## 6.2 What does an IMU measure?

An accelerometer measures specific force in its sensor frame. A common idealized model is $\mathbf f_b=\mathbf R_{wb}^{\top}(\mathbf a_w-\mathbf g_w)+\mathbf b+\boldsymbol\epsilon$, where $\mathbf R_{wb}$ rotates body-frame vectors into the world frame, $\mathbf a_w$ is translational acceleration, $\mathbf g_w$ is gravity, and $\mathbf b$ is bias. A stationary, upward-facing z axis can read approximately $+9.81$ m/s². ROS IMU acceleration uses m/s² and angular velocity uses rad/s [[1]](#imu-ref-1).

A gyroscope measures angular velocity, not absolute heading. Integrating yaw rate accumulates bias and drift. An orientation estimate may be provided by a fusion system; it is not guaranteed by the presence of an IMU message. Document the sensor's frame and whether the reported acceleration includes gravity.

## 6.3 Worked example — causal vibration RMS

For the fixed-orientation synthetic experiment, estimate the stationary z baseline $b$ during a calibration interval, subtract it, and compute a trailing root-mean-square feature:

$$
r[n]=\sqrt{\frac{1}{W}\sum_{j=0}^{W-1}(a_z[n-j]-b)^2}.
$$

The sample is available only when the last sample in its window arrives. With $f_s=200$ Hz and $W=20$, the window spans 100 ms of sampling time. It contains no future samples; onset detection still incurs a signal-dependent delay. Thresholding at $0.4$ m/s² is a chosen teaching detector, not a sensor specification.

```python
import numpy as np
fs = 200.0
window = 20
# z_acceleration is a 1-D array in m/s²; first 0.3 s must be stationary.
def vibration_rms(z_acceleration):
    z = np.asarray(z_acceleration, dtype=float)
    baseline = z[:int(.3*fs)].mean()
    rms = np.sqrt(np.convolve((z-baseline)**2,
                             np.ones(window)/window, mode="valid"))
    time_s = np.arange(window-1, len(z))/fs  # right edge: no future samples
    return time_s, rms
```

[Laboratory 6](../notebooks/sensory_encoding.ipynb) generates a 20 Hz vibration from 0.8 to 1.6 s, amplitude 1 m/s², with a 9.81 m/s² stationary offset and seeded noise. In a full-cycle ideal window, sinusoidal RMS is $1/\sqrt2\approx0.707$ m/s². The quiet baseline remains well below the example threshold.

```{figure} ../assets/sensor-course-imu.png
:label: fig-sensor-imu
:alt: Synthetic z acceleration containing gravity offset and vibration, with a separate trailing RMS detector panel
:width: 100%

Original synthetic signal and causal feature. The baseline subtraction assumes fixed orientation; tilting the robot invalidates that simple compensation.
```

## 6.4 From vibration to a neural input

Choose either $u=\mathbf1[r>0.4]$ for the Chapter 4 trial-level example or a graded $z_U=\operatorname{clip}(r/r_{\mathrm{scale}},0,1)$ for a current encoder. State $r_{\mathrm{scale}}$ in m/s². Adding a US current is a model construction; it does not establish a biological mechanoreceptor response.

Changing sampling rate without changing $W$ changes the physical window duration. A 20 Hz input sampled at 30 Hz aliases; no neural encoder can recover the original waveform from those samples alone. For moving and tilting robots, transform acceleration using a validated orientation estimate or use an appropriate frequency-selective detector and test its failure conditions. Slow turns, bumps, and motor vibration are useful negative controls.

(65-exercises)=

## 6.5 Exercises

1. Change $W$ from 20 to 40. Compare onset delay, smoothing, and physical window length.
2. Keep 100 ms while changing the sampling rate to 100 Hz. What is the new $W$?
3. Explain why subtracting 9.81 from an arbitrary IMU z axis can be wrong.
4. Add a slow orientation-induced change to the synthetic trace and measure false detections.

## References

(imu-ref-1)=

[1] ROS 2 contributors, “Imu message,” *sensor_msgs*, Jazzy distribution. [Official message definition](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/Imu.msg).

## Additional Reading Materials

Read the course's MEMS accelerometer and gyroscope material, then inspect the units, covariance conventions, and unavailable-orientation flag in [[1]](#imu-ref-1). Continue to [Chapter 8](09-nengo-ros-gazebo.md) for timestamps and message contracts before consuming live measurements.
