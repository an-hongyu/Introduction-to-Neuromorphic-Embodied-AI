---
title: "Solutions II — Sensors and Embodied Learning"
---

# Solutions to Exercises — Part II: Sensors and Embodied Robotics

Worked answers use the chapter's specified units and model conventions. Suggested experiments are protocols to run, not unverified numerical outcomes.

(vision-solutions)=
## Chapter 6 — 6.12 Exercises

[Original exercises](06-visual-perception.md#66-exercises)

1. **Red cue.** For $(R,G,B)=(0.8,0.2,0.2)$, contrast is $z_R=\operatorname{clip}(0.8-(0.2+0.2)/2,0,1)=0.6$; $I=50+250z_R=200$ pA.
2. **Smaller red target.** With per-pixel red contrast $c$ and target coverage fraction $q$ on a zero-contrast background, the ROI-averaged feature is approximately $qc$. A smaller cue therefore reduces feature and encoded drive even if its hue remains unchanged.
3. **Held-out lighting.** Partition image scenes and lighting conditions before tuning. Fix preprocessing/thresholds on training/validation only; on unseen illumination/exposure/white-balance cases report true/false detections and resulting neural activity without retraining.
4. **Clipping order.** Mean of clipped contrasts need not equal clip of the mean. For contrasts $(-0.4,0.8)$, clip-then-average is $(0+0.8)/2=0.4$; average-then-clip is $0.2$. The textbook's $z_R$ clips each pixel before averaging.


5. **Separate the roles.** A camera is the sensor; a measured cue or mask is a perception output; choosing a turn is a planning/control decision; the motors are actuators. An RGB array records measurements, not a motor command.
6. **Measurement units.** Radiant flux measures physical power in W; luminous flux measures visually weighted flux in lm. Irradiance is W/m² and illuminance is lx = lm/m². A pixel value is a digitized sample and needs a calibration and acquisition model before it can be interpreted as lux.
7. **Projection.** $x'=8(150)/600=2$ mm. At $Z=1200$ mm, $x'=1$ mm. With the physical image plane behind the pinhole and the same axis orientation, the coordinates are $-2$ mm and $-1$ mm, expressing inversion.
8. **Bayer and resolution.** The representative block has one R, two G, and one B site. $4912\times3684=18{,}095{,}808$ sites, approximately 18.1 MP. A filtered photosite is not a complete RGB triplet.
9. **Color matching.** Write $A\mathbf c=\mathbf t$, where columns of $A$ are the three response vectors to the primaries. If $A$ is invertible, $\mathbf c=A^{-1}\mathbf t$. A coefficient $R<0$ means moving $|R|\mathbf p_R$ to the test-light side; no source emits negative power.
10. **Normalized RGB.** The sum is 1.6 and the ratios are $(0.3125,0.125,0.5625)$. Their maximum is 0.5625, compared with 0.9 for the original values. The code on slide 66 converts the normalized values. Black gives a zero denominator and must be handled separately. These ratios alone do not establish CIE chromaticity coordinates.
11. **Threshold.** The binary result is $[0,0,1,1]$ under the stated greater-than-or-equal convention. On normalized inputs use $180/255\approx0.705882$.
12. **Mean filter.** The first selected block sums to 180, giving 20. The second displayed block sums to $50+10+37+20+30+72+10+20+11=260$, giving $260/9\approx28.8889$. The second printed list on the lecture slide uses different entries and does not support that displayed result; the chapter identifies which matrix is used.
13. **Gaussian kernel.** For $h=1$, $\sigma=1$, unnormalized center, side, and corner weights are $1$, $e^{-1/2}$, and $e^{-1}$. Divide by $1+4e^{-1/2}+4e^{-1}\approx4.8976404$. The normalized weights are approximately 0.20417996, 0.12384140, and 0.07511361, respectively. They sum to 1, so an edge-padded constant image remains constant. Window size and $\sigma$ are different parameters.
14. **Point versus neighborhood.** A point operation uses the corresponding pixel only; a neighborhood filter combines adjacent pixels. Smoothing can mix a small landmark with its background, reducing contrast and possibly preventing threshold crossing. This prediction should be tested at fixed cue size, kernel, and boundary convention.
15. **Masking.** With $M=1$, $Z=F$; with $M=0$, $Z=B$. For $F=(1,0,0)$ and $B=(0,0,1)$, these are red and blue. An incorrect mask selects the wrong source, even when the compositing arithmetic is correct.
16. **Failure localization.** Log frame, ROI, preprocessing, feature, current, spikes, weights, and action. A visible target with a missing feature indicates acquisition/perception trouble. A correct feature but unexpected current or neural response points to encoding or neuron-model implementation. Verified cue activity without the learned response points to association/readout. Keep parameters frozen in held-out trials and separate these outcomes from actuation failure.

## Chapter 7 — 7.5 Exercises

[Original exercises](07-inertial-sensing.md#75-exercises)

1. **Window $W=40$.** At $f_s=200$ Hz, $W=20$ covers 100 ms and $W=40$ covers 200 ms. The longer trailing window smooths fluctuations but usually increases response/recovery time. Exact onset delay depends on threshold, signal, and phase, not only window length.
2. **100 ms at 100 Hz.** $W=f_sT=100(0.1)=10$ samples.
3. **Gravity projection.** Accelerometer axes are in the moving sensor frame; gravity is not always aligned with sensor z. Blindly subtracting $9.81$ from z can introduce error. Transform an estimated world gravity vector to the sensor frame or use appropriate baseline/high-pass methods.
4. **Synthetic tilt control.** Add a slow time-varying gravity projection to the original signal, preserve the known vibration interval, and count detections outside it with the unmodified algorithm. Compare raw and detrended filters on the same noise seed. A numerical false-positive count requires running the altered experiment.

(lidar-solutions)=
## Chapter 8 - 8.13 Exercises

[Original exercises](08-lidar-encoding.md#85-exercises)

1. **Distance to prescribed rate.** With $d_{\max}=5$ m, $r(d)=5+45(1-d/5)$ Hz. At 1.5 m, $r=36.5$ Hz; at 4 m, $r=14$ Hz. These are encoder targets, not guaranteed LIF output rates.
2. **Minimum versus median.** For $(1,4,4,4,4)$ m, the minimum is 1 m and the median is 4 m. The minimum preserves a thin observed obstacle but responds to an isolated spurious close return. The median suppresses that outlier but can also remove a real thin obstacle. A justified aggregation rule needs a stated task and test.
3. **Rotation.** For a fixed environment and an aligned sensor, rotating the robot changes the body-relative directions of returns and their sector indices. Correct world-frame endpoints should remain fixed for static objects when pose and mounting transforms are applied. A 90-degree rotation corresponds to nine 10-degree sectors for an ideal circular index shift, but real occlusion and motion must also be considered.
4. **Missing versus maximum.** The chapter's conservative code rejects nonfinite ranges and out-of-limit measurements. A finite accepted range equal to 5 m produces 5 Hz with a true validity mask. Unknown produces a placeholder 0 Hz with a false mask. Infinity may have a driver-specific no-return meaning; this interpretation must not be inferred solely from the number. NaN is not a measured wall or measured free space.
5. **Flight time.** $d=(3\times10^8)(100\times10^{-9})/2=15$ m. The measured time includes outward and return travel. Without division by two, the result would be the 30 m total path rather than the one-way range.
6. **Return separation.** $\delta d=(3\times10^8)(10^{-9})/2=0.15$ m. This is an ideal relation between temporal and range separation. It does not establish calibration error, absolute accuracy, or whether the actual receiver can resolve two overlapping waveforms.
7. **Hardware and neural channels.** The laser/transmit path sends light; receive optics and detector collect returns; scanning selects direction; the electronics handle timing/readout/processing. An elevation channel in the illustrated instrument is a physical directional measurement channel. A neural sector is a chosen aggregation of accepted planar measurements; one planar scanner can supply all 36 sectors.
8. **Different steering mechanisms.** The cited silicon-photonic work uses MEMS-actuated optical switches in a focal-plane switch array. The animation illustrates phase-controlled interference. They are not interchangeable device descriptions; a generic 'no moving parts' caption does not describe every internal component in the former.
9. **Return-order colors.** Red, yellow, and green identify the first, second, and third returns in the lecture example. A later surface can produce a stronger return than an earlier surface. Return order, peak strength, and visible surface color are different attributes.
10. **Angular geometry.** FOV is angular coverage, whereas spacing describes sampled directions. $2(10)\sin(0.5^\circ)\approx0.17453$ m and $2(10)\sin(5^\circ)\approx1.74311$ m. These are separations of equal-range endpoints. A 10-degree neural sector may contain many raw rays, not just one ray.
11. **Sector convention.** The respective indices are $0,0,18,27,35,0$. The wrap maps $180^\circ$ to $-180^\circ$. Under this convention forward lies at the start of sector 18, rather than at its center.
12. **Encoded samples.** Valid sectors are 18, 27, and 35, with distances 0.8, 3, and 5 m and rates 42.8, 23, and 5 Hz. The NaN contributes no valid sample. Other sectors have unknown distances, zero placeholder rates, and false masks.
13. **Poisson interpretation.** The expected count is $42.8(0.5)=21.4$. The 1 ms probability is $1-\exp(-42.8\times0.001)\approx0.041897$, about 4.19%. A count expectation averages over hypothetical repetitions and need not be an integer; each realized count is integer-valued. The code samples counts, permitting more than one event per bin.
14. **Motion during a scan.** Translation is $1(0.1)=0.1$ m and heading change is $90(0.1)=9^\circ$. First-ray time, per-ray time increment, frame identity, mounting transform, and a time-dependent pose estimate are needed to associate each measurement with the correct acquisition geometry. Scan time alone is not a substitute for all of these.
15. **World endpoint.** For the stated pose, $x_w=1+\cos90^\circ=1$ m and $y_w=2+\sin90^\circ=3$ m. With a mounting offset, apply $T_{bs}$ before the time-dependent body-to-world transform. Translation can change bearing and distance relative to the body origin, so adding only a yaw offset is not generally enough.
16. **Winter replay protocol.** Freeze preprocessing, validity policy, sector aggregation, and neural parameters before testing held-out sequences. Log raw measurements, timestamps, masks, sector minima, prescribed rates, event counts, and control decisions. Evaluate missing-sector frequency separately from unexpected near returns; check the numerical encoder on known synthetic inputs. Ground-truth annotations are used for evaluation, not supplied as hidden inputs. Compare matched replay conditions before attributing a difference to learning. No benchmark score follows without actually running the selected data.

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
