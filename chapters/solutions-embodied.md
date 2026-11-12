---
title: "Solutions II — Sensors and Embodied Learning"
---

# Solutions to Exercises — Part II: Neural Encoding and Embodied Robotics

Worked answers use the chapter's specified units and model conventions. Suggested experiments are protocols to run, not unverified numerical outcomes.

## Chapter 5 — 5.6 Exercises

[Original exercises](05-neural-encoding.md#56-exercises)

1. **Count and latency.** Two spike trains can have the same count $K$ and mean rate $K/T$ yet different first-event times. A temporally sensitive downstream neuron may respond differently; report latency, interval structure, and count separately.
2. **Feature-to-current map.** For $z=0.6$, $I=50+250(0.6)=200$ pA. With $E_L=-65$ mV and $g_L=10$ nS, passive equilibrium is $V_\infty=-65+200/10=-45$ mV, above the chapter's $-50$ mV event threshold.
3. **Invalid zero rate.** An invalid range encoded as zero would be indistinguishable from a genuinely weak valid feature. Carry a separate validity mask and timestamp; distinguish absent evidence from measured no-obstacle evidence.
4. **Window duration.** A 500 ms window averages more spikes and often reduces sampling variance, but costs latency and mixes changing states. A 50 ms window responds sooner but has noisier rate estimates and more zero-count windows. Compare detection delay, count distribution, and transient performance.

## Chapter 6 — 6.6 Exercises

[Original exercises](06-visual-perception.md#66-exercises)

1. **Red cue.** For $(R,G,B)=(0.8,0.2,0.2)$, contrast is $z_R=\operatorname{clip}(0.8-(0.2+0.2)/2,0,1)=0.6$; $I=50+250z_R=200$ pA.
2. **Smaller red target.** With per-pixel red contrast $c$ and target coverage fraction $q$ on a zero-contrast background, the ROI-averaged feature is approximately $qc$. A smaller cue therefore reduces feature and encoded drive even if its hue remains unchanged.
3. **Held-out lighting.** Partition image scenes and lighting conditions before tuning. Fix preprocessing/thresholds on training/validation only; on unseen illumination/exposure/white-balance cases report true/false detections and resulting neural activity without retraining.
4. **Clipping order.** Mean of clipped contrasts need not equal clip of the mean. For contrasts $(-0.4,0.8)$, clip-then-average is $(0+0.8)/2=0.4$; average-then-clip is $0.2$. The textbook's $z_R$ clips each pixel before averaging.

## Chapter 7 — 7.5 Exercises

[Original exercises](07-inertial-sensing.md#75-exercises)

1. **Window $W=40$.** At $f_s=200$ Hz, $W=20$ covers 100 ms and $W=40$ covers 200 ms. The longer trailing window smooths fluctuations but usually increases response/recovery time. Exact onset delay depends on threshold, signal, and phase, not only window length.
2. **100 ms at 100 Hz.** $W=f_sT=100(0.1)=10$ samples.
3. **Gravity projection.** Accelerometer axes are in the moving sensor frame; gravity is not always aligned with sensor z. Blindly subtracting $9.81$ from z can introduce error. Transform an estimated world gravity vector to the sensor frame or use appropriate baseline/high-pass methods.
4. **Synthetic tilt control.** Add a slow time-varying gravity projection to the original signal, preserve the known vibration interval, and count detections outside it with the unmodified algorithm. Compare raw and detrended filters on the same noise seed. A numerical false-positive count requires running the altered experiment.

## Chapter 8 — 8.5 Exercises

[Original exercises](08-lidar-encoding.md#85-exercises)

1. **Distance-to-rate conversion.** For valid $d$ in metres, $r(d)=5+45(1-d/5)$ Hz. At 1.5 m, $r=36.5$ Hz; at 4 m, $r=14$ Hz.
2. **Minimum versus median.** For $(1,4,4,4,4)$ m, minimum is 1 m and median is 4 m. Minimum preserves a thin close hazard but is sensitive to isolated errors; median is robust to a single outlier but can miss a thin obstacle.
3. **90° rotation.** Body-relative ray bearings/sector assignment change with sensor or robot rotation. Properly transformed world-coordinate obstacle points should remain fixed for stationary obstacles if pose and mounting transforms are correct. Distinguish a rotated scan array from physical motion.
4. **Invalid versus maximum.** NaN is unusable; infinity may indicate no detection or out-of-range depending on the driver; a finite maximum may be a real return or a vendor sentinel. Use the specified sensor/ROS contract, preserve distinctions, and avoid inventing a wall exactly at maximum range.

## Chapter 9 — 9.6 Exercises

[Original exercises](09-nengo-ros-gazebo.md#96-exercises)

1. **Remove gain compensation.** The 2× gain with 0.5 connection transform originally delivers normalized $J=1.5$. Without compensation $J=3$. For $f(J)=[\tau_{\mathrm{ref}}+\tau_{\mathrm{RC}}\ln(J/(J-1))]^{-1}$ with $0.002$ s and $0.02$ s, rate increases from about 41.71 Hz to $[0.002+0.02\ln(3/2)]^{-1}\approx98.92$ Hz.
2. **Update rates and staleness.** For illustration choose LiDAR 10 Hz, camera 20 Hz, neural simulation 1000 Hz, and controller 20 Hz. Timestamp each sensor message, hold or reject values only under a documented age rule (e.g., stale after 200 ms), and report dropped messages and update jitter. These rates are design examples, not recorded platform measurements.
3. **Failure classification.** Log raw image/ROI red feature, cue detection, US detection, neural current, connection weight, spikes, and motor command. Red present but cue absent indicates vision/encoding failure; verified cue present but learned response absent points to neural association/readout; command without movement points to actuation or simulator state.
4. **Independent reset.** Reset simulator pose/velocity, sensor queues and timestamps, neural membrane/synaptic/refractory state, motor commands, and stochastic seeds as appropriate. For training decide explicitly whether weights persist; for testing load a fixed weight checkpoint and disable updates.

## Chapter 10 — 10.7 Exercises

[Original exercises](10-associative-learning-robot.md#107-exercises)

1. **Weight for firing.** In CS-only recall, $I=50+200w$ pA. Passive rheobase is 150 pA, hence $50+200w>150$ requires **$w>0.5$**; equality does not cross in finite time in the ideal constant-current model. Three spikes within 500 ms require sufficient first-spike time plus two further interspike intervals including refractoriness, so this inequality alone is not sufficient.
2. **Pairing controls.** With a filtered CS, recent CS activity can persist after its visible offset. Non-overlapping presentations must be separated by delays exceeding the relevant synaptic/eligibility memory. Also shuffle pairings independently while matching cue counts, US counts, and timing statistics; compare frozen CS-only probes.
3. **Brightness generalization.** Train with selected cue brightness levels and reserve unseen brightness/lighting combinations (and preferably distinct scenes) for a fixed test set. Freeze preprocessing/weights; report perception accuracy, spikes, and action decisions across held-out levels without tuning on test data.
4. **Moving red object.** Motion changes ROI coverage, blur, and frame-to-frame appearance. Test moving cues with weights frozen and log red-feature detection before assessing associative behavior. Missing CS despite a visible cue diagnoses perception/encoding, not a failure of the learned weight.
