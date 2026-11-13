---
title: "Chapter 8 \u00b7 Neural Encoding for LiDAR Sensing"
---

## 8.1 Learning objectives

A LiDAR does not directly report an obstacle-avoidance decision or a place-cell response. It measures light returned from the environment. Those measurements must be associated with directions and acquisition times, interpreted in a coordinate frame, and transformed into the inputs consumed by a neural model.

This chapter follows the supplied **Introduction to LiDAR** lecture: ranging principles, scanning hardware, survey applications, return signals, sensor parameters, point clouds, and sensing limitations [[1]](#lidar-ref-1). The original lecture images, two animations, and three video links accompany the discussion. Sections 8.9-8.10 extend that material into the book's existing **36-channel neural encoder**; its parameters are teaching choices, not sensor specifications or experimental results reported in the lecture.

By the end of this chapter, you should be able to:

- Explain how a transmitted light signal and its return provide a range measurement.
- Identify the laser source, receiver, scanning mechanism, and timing electronics.
- Distinguish planar scanning, multibeam scanning, and the solid-state architectures illustrated in the lecture.
- Interpret field of view, angular sampling, range resolution, intensity, and multiple returns.
- Read a point cloud while keeping geometry, colorization, semantic labels, and acquisition time separate.
- Explain how surface properties, weather, and motion can corrupt a scan.
- Compress valid planar ranges into 36 sectors of 10 degrees each and generate a declared neural representation.
- Preserve missing-data masks and distinguish body-relative sensory activity from world-relative spatial-cell models.

## 8.2 What LiDAR measures

**LiDAR** stands for **Light Detection and Ranging**. In the lecture's pulsed ranging example, the instrument emits light, receives some of the light reflected by a target, and measures its round-trip delay. Associating range with beam direction produces geometric observations of the environment [[1]](#lidar-ref-1), slides 2-9.

The vehicle, handheld-device, and airborne examples illustrate different deployments of the same broad sensing idea. They do not imply that these systems have the same range, resolution, field of view, or scanning architecture.

```{figure} ../assets/lidar-lecture/lidar-applications.png
:label: fig-lidar-lidar-applications
:alt: LiDAR on vehicles, consumer devices, and airborne platforms; original media from the supplied LiDAR lecture
:width: 100%

**LiDAR on vehicles, consumer devices, and airborne platforms.** The source photographs illustrate different deployment platforms, not equal sensor capabilities. Source: lecture slide(s) 3 [[1]](#lidar-ref-1). Slide credit: Uber, Apple, Xiaomi, DJI.
```

### 8.2.1 Lecture video: LiDAR in a scene

The following is the original video linked on slide 2, **Lidar 101 from Velodyne Lidar**. Its title and poster come from the PowerPoint's online-media object. While watching, distinguish the physical scene from the point-cloud visualization and from any object labels added by a perception algorithm.

```{iframe} /Introduction-to-Neuromorphic-Embodied-AI/lidar-lecture-media.html?v=NZKvf1cXe8s
:label: lidar-video-nzkvf1cxe8s
:class: lidar-video-player
:title: Lidar 101 from Velodyne Lidar
:width: 100%
```

[Watch the original video on YouTube](https://www.youtube.com/watch?v=NZKvf1cXe8s) | Lecture slide 2 [[1]](#lidar-ref-1).

**Viewing question.** Which part of the display is a measurement of geometry, and which part is an interpretation of that geometry? A colored cluster or bounding box is not itself a raw optical time-of-flight measurement.

## 8.3 From light propagation to a distance

### 8.3.1 Round-trip time of flight

Let $\Delta t$ be the elapsed time between emission and reception of a return. Under the ideal propagation model used in the lecture,

$$
d=\frac{c\Delta t}{2}.
$$

Here $d$ is the one-way distance in metres and $c$ is the propagation speed in metres per second. In air, the following examples use $c\approx3\times10^8$ m/s. The factor of two is essential: the light travels to the target and back. Slides 4-7 and 34 connect the geometry with delayed transmitted and received pulses [[1]](#lidar-ref-1).

```{figure} ../assets/lidar-lecture/time-of-flight.png
:label: fig-lidar-time-of-flight
:alt: From a transmitted pulse to a delayed return; original media from the supplied LiDAR lecture
:width: 100%

**From a transmitted pulse to a delayed return.** Follow the transmitted and received pulse sequences; the delay measures an outward and return path. Source: lecture slide(s) 6 [[1]](#lidar-ref-1).
```

**Read the figure.** Match an emitted pulse to the corresponding received pulse. The horizontal separation is a travel-time measurement, not the interval between successive emitted pulses. A larger separation corresponds to a more distant target under this model.

**Worked examples.** A 20 ns delay gives $d=(3\times10^8)(20\times10^{-9})/2=3$ m. A 100 ns delay gives 15 m. Conversely, a target 0.8 m away has an ideal round-trip delay of approximately 5.33 ns. These are calculations, not measured data.

The lecture also shows a phase-shift drawing on slides 5 and 7. It illustrates comparing transmitted and received signals, but does not provide a complete phase-ranging algorithm, modulation-frequency specification, or ambiguity-resolution procedure. The numerical examples here therefore use the explicitly stated time-of-flight equation rather than treating all LiDAR architectures as identical.

### 8.3.2 Three different clocks

Keep the following intervals separate:

| Interval | Meaning | Role in this chapter |
|---|---|---|
| Optical round-trip delay $\Delta t$ | Travel to a target and back | Converts to distance |
| Time between rays or scans | Sampling the environment over time | Matters for motion distortion and data freshness |
| Neural encoding delay or response window | A software/model design parameter | Determines when encoded events are emitted or counted |

A neural encoder that emits an earlier spike for a nearer obstacle uses an **additional chosen latency rule**. Its millisecond-scale response is not the nanosecond optical flight time. Likewise, a 10 Hz scan update and a 40 Hz neural firing rate describe different processes.

## 8.4 Components and scanning mechanisms

### 8.4.1 Follow the signal through the hardware

The lecture separates four roles: the laser source produces the outgoing light; transmit optics direct it; receive optics and a detector collect the return; and timing/readout electronics convert that response into a measurement. Its block diagram distinguishes transmit optical paths, receive optical paths, and electrical connections [[1]](#lidar-ref-1), slides 15-17.

```{figure} ../assets/lidar-lecture/lidar-components.png
:label: fig-lidar-lidar-components
:alt: Transmitter, receiver, timing, and processing paths; original media from the supplied LiDAR lecture
:width: 100%

**Transmitter, receiver, timing, and processing paths.** Blue and red paths identify transmit and receive optics; green paths identify electrical connections. Source: lecture slide(s) 15, 16, 17 [[1]](#lidar-ref-1).
```

The transmit and receive apertures may share an optical path or use separate paths, as discussed under the lecture's monostatic/bistatic terminology. The important modeling question is what measurement and coordinate convention the complete instrument delivers. The neural encoder does not need to simulate every optical component, but it must respect that measurement contract.

### 8.4.2 Fixed-direction, planar, and multibeam measurements

A fixed-direction measurement reports distance along a particular line of sight. A planar scanner changes azimuth and produces a sequence of range-angle samples in a plane. A multibeam system additionally samples several elevation directions. The lecture's rotating mechanism and its labeled elevation channels make this distinction visible [[1]](#lidar-ref-1), slides 8-9 and 18-19.

```{figure} ../assets/lidar-lecture/planar-scan-animation.gif
:label: fig-lidar-planar-scan-animation
:alt: A planar scanner builds up angular range samples; original media from the supplied LiDAR lecture
:width: 50%

**A planar scanner builds up angular range samples.** Original animated GIF from the PowerPoint. Watch the beam direction and the accumulation of samples. Source: lecture slide(s) 8, 18 [[1]](#lidar-ref-1).
```

**Read the animation.** Follow the moving beam, its intersection with the scene, and the accumulating samples. A scan is assembled over time; the completed set of points should not automatically be treated as an instantaneous observation.

```{figure} ../assets/lidar-lecture/mechanical-and-multibeam.png
:label: fig-lidar-mechanical-and-multibeam
:alt: Mechanical scanning and multiple elevation channels; original media from the supplied LiDAR lecture
:width: 100%

**Mechanical scanning and multiple elevation channels.** The rotating mechanism and the separate elevation channels sample different directions. Source: lecture slide(s) 15, 18 [[1]](#lidar-ref-1). The multichannel illustration identifies a Hesai device.
```

The lecture also introduces two **chip-scale beam-steering approaches**. The silicon-photonic system illustrated below uses MEMS-actuated optical switches to select emission directions; the phased-array animation instead illustrates steering by changing the relative phase across emitters. These approaches differ in their physical mechanisms, even though both aim to direct light without a conventional spinning scanner [[1]](#lidar-ref-1), slides 20–21; [[4]](#lidar-ref-4).

```{figure} ../assets/lidar-lecture/silicon-photonics-lidar.png
:label: fig-lidar-silicon-photonics-lidar
:alt: Schematic and hardware illustration of a MEMS optical-switch-based silicon-photonic LiDAR
:width: 100%

**Silicon-photonic optical switching.** The illustrated MEMS optical-switch array selects beam directions. Source: lecture slides 20–21; Zhang *et al.*, *Nature*, 2022 [[4]](#lidar-ref-4).
```

```{figure} ../assets/lidar-lecture/phased-array-animation.gif
:label: fig-lidar-phased-array-animation
:alt: Animated optical phased-array illustration in which changing relative phases steers the beam
:width: 50%

**Phased-array beam steering.** The original lecture animation shows how phase relationships can change an emitted beam's direction. Source: lecture slide 21 [[1]](#lidar-ref-1).
```

Do not confuse the illustrated **hardware channels** with the **36 neural channels** used later. A hardware channel may correspond to an elevation beam; our neural channel corresponds to one selected 10-degree planar sector. A single planar scanner can supply all 36 neural inputs.

## 8.5 Survey applications, intensity, and multiple returns

### 8.5.1 Airborne, terrestrial, and mobile systems

The lecture organizes deployment into airborne surveying, ground-based terrestrial surveying, and mobile systems mounted on vehicles. Topographic applications describe terrain, buildings, and vegetation; terrestrial and mobile examples connect this geometry to nearby structures and driving scenes [[1]](#lidar-ref-1), slides 10-11, 22-23, and 29.

Airborne data collection combines a laser scanner with platform position and attitude information. The lecture names GPS and an inertial measurement unit (IMU). A range alone is insufficient to place a point in a common geographical frame: the beam direction, sensor pose, and acquisition time also matter.

```{figure} ../assets/lidar-lecture/aerial-data-collection.png
:label: fig-lidar-aerial-data-collection
:alt: Airborne scanning combines range, platform position, and attitude; original media from the supplied LiDAR lecture
:width: 100%

**Airborne scanning combines range, platform position, and attitude.** The original diagram preserves the flight direction, scan line, footprint label, and GPS reference. Source: lecture slide(s) 23 [[1]](#lidar-ref-1).
```

**Read the figure.** The scan line is swept while the aircraft moves forward. The labeled footprint is a particular lecture example, not a universal LiDAR spot size. Relate each return to the position and orientation of the platform when that measurement was acquired.

### 8.5.2 Return intensity is not range

Slide 24 describes return intensity as a measure associated with received reflected energy. Surface reflection and absorption affect the signal. Range describes **where** a return is; intensity describes an aspect of **how strongly** it was received. Intensity can help characterize surfaces, but the lecture does not define a calibrated material classifier or a universal intensity-to-material equation [[1]](#lidar-ref-1).

Do not map point-cloud display colors directly to neural firing rates without reading the visualization's legend. Color may represent elevation, intensity, return order, a semantic label, or another assigned quantity. It need not represent visible surface color.

### 8.5.3 Why a pulse can have multiple returns

A beam footprint can encounter leaves, branches, and ground at different depths. Some light returns from an upper surface while other light passes through gaps and returns later. The lecture illustrates the resulting peaks and discretized returns [[1]](#lidar-ref-1), slides 25-27; its linked NEON tutorial explains the same waveform interpretation [[5]](#lidar-ref-5).

```{figure} ../assets/lidar-lecture/multiple-return-waveforms.png
:label: fig-lidar-multiple-return-waveforms
:alt: A pulse can produce several return peaks; original media from the supplied LiDAR lecture
:width: 100%

**A pulse can produce several return peaks.** The original illustrations associate return peaks with different depths and show a threshold for discrete returns. Source: lecture slide(s) 26 [[1]](#lidar-ref-1). Lecture source: NEON LiDAR basics tutorial.
```

An earlier peak corresponds to a shorter optical path in this example. The tallest peak is not necessarily the nearest surface. Recording only the first, strongest, or last return changes the information available to an encoder; the selected return policy must therefore be stated.

```{figure} ../assets/lidar-lecture/tree-return-classes.png
:label: fig-lidar-tree-return-classes
:alt: Tree points colored by return order; original media from the supplied LiDAR lecture
:width: 100%

**Tree points colored by return order.** The point colors indicate first, second, and third returns, not visible surface color. Source: lecture slide(s) 27 [[1]](#lidar-ref-1).
```

**Read the figure.** The lecture labels red as the first return, yellow as the second, and green as the third. These are assigned return-order colors, not a measurement of the tree's visible colors. Multiple returns are possible; the slides do not establish that every instrument records all of them on every pulse.

### 8.5.4 Bathymetric sensing

Bathymetric LiDAR targets water depth and submerged terrain. The lecture diagram distinguishes a water-surface return from a bottom return and emphasizes attenuation in water [[1]](#lidar-ref-1), slide 28.

```{figure} ../assets/lidar-lecture/bathymetric-lidar.png
:label: fig-lidar-bathymetric-lidar
:alt: Water-surface and bottom returns in bathymetric surveying; original media from the supplied LiDAR lecture
:width: 100%

**Water-surface and bottom returns in bathymetric surveying.** The source diagrams distinguish water-surface and bottom returns; see the wavelength clarification in the text. Source: lecture slide(s) 28 [[1]](#lidar-ref-1).
```

**Technical clarification beyond the slide wording.** Slide 28 describes the penetrating channel as shorter-wavelength near-infrared. The linked MathWorks overview instead identifies an additional **green laser** for transmission through the water column. The illustration is retained, but its general near-infrared wording is not used as an instrument specification [[3]](#lidar-ref-3). The air-path equation by itself is also not a complete water-depth model: the propagation path and speed in each medium must be accounted for.

## 8.6 Parameters that determine what the encoder can see

### 8.6.1 Field of view and angular sampling

**Field of view (FOV)** describes angular coverage. **Angular sampling/resolution** concerns the separation of sampled directions and the angular detail that can be distinguished. A wide field of view does not guarantee fine sampling. The lecture distinguishes horizontal and vertical quantities in its range/FOV diagram [[1]](#lidar-ref-1), slides 30-32.

```{figure} ../assets/lidar-lecture/field-of-view.png
:label: fig-lidar-field-of-view
:alt: Field of view, angular spacing, and range are different quantities; original media from the supplied LiDAR lecture
:width: 100%

**Field of view, angular spacing, and range are different quantities.** Horizontal and vertical angular coverage, angular spacing, range, and range resolution are labeled separately. Source: lecture slide(s) 30, 32 [[1]](#lidar-ref-1).
```

For an ideal circular sweep with $N$ distinct uniformly spaced samples, $\Delta\theta=2\pi/N$. A 360-sample sweep has 1-degree spacing; a 36-sector representation has 10-degree sectors. Those sectors are a deliberate compression of the scan, not an improvement of its optical resolution.

```{figure} ../assets/lidar-lecture/angular-resolution.png
:label: fig-lidar-angular-resolution
:alt: Angular sampling changes the detail captured on a distant object; original media from the supplied LiDAR lecture
:width: 100%

**Angular sampling changes the detail captured on a distant object.** The source grid illustrates how angular sampling affects object detail at a distance. Source: lecture slide(s) 31 [[1]](#lidar-ref-1). Slide credit: LIDAR for Autonomous System Design: Object Classification or Object Detection?
```

**Worked geometric example.** For two rays separated by $\Delta\theta$, the separation of two points at the same radial distance $d$ is

$$
s=2d\sin(\Delta\theta/2)\approx d\Delta\theta
$$

for small angles expressed in radians. At 10 m, a 1-degree separation is about 0.175 m; a 10-degree separation is about 1.74 m. This calculation explains why a thin obstacle can occupy only a small part of a neural sector. It is not an assertion that each 10-degree sector is sampled by only one physical beam.

### 8.6.2 Range resolution, precision, and maximum range

Slide 34 writes range, range resolution, and maximum range in terms of different timing quantities. If two returns can be separated in time by $\delta t$, their ideal range separation is

$$
\delta d=\frac{c\,\delta t}{2}.
$$

A 1 ns separation corresponds to 0.15 m using the stated value of $c$. Whether a real receiver resolves those returns depends on its pulse/receiver response and processing. A reported distance's quantization, repeatability, and absolute error are not automatically the same as its ability to resolve two surfaces.

**Clarification of the lecture's timing terms.** Slide 32 groups pulse duration and repetition rate in the resolution discussion. Keep their roles separate. Pulse/receiver timing limits relate to separating returns. Under the simplified rule that a return must arrive before the next identical pulse, a pulse period $T_p$ would impose an unambiguous-range bound $cT_p/2$. A 1 microsecond period gives 150 m under that assumption, not a guarantee of detecting a target at 150 m. This is a derived example, not a measured specification.

The short-, medium-, and long-range categories on slide 33 are descriptive lecture categories. Use the selected sensor's documented limits in code instead of converting those broad categories into fixed universal thresholds.

```{figure} ../assets/lidar-lecture/blind-spots.png
:label: fig-lidar-blind-spots
:alt: Coverage and mounting geometry leave blind spots; original media from the supplied LiDAR lecture
:width: 100%

**Coverage and mounting geometry leave blind spots.** The two configurations show how placement and coverage affect unobserved regions. Source: lecture slide(s) 33 [[1]](#lidar-ref-1).
```

### 8.6.3 Wavelength and safe operation

Slides 12-14 compare wavelength groups and discuss repetition rate, detection, and eye safety. They motivate asking how wavelength interacts with detector technology and the environment, but their "eye-safe" wording is not a safety certification for a complete device [[1]](#lidar-ref-1).

**Safety clarification.** Wavelength or visible brightness alone does not establish safe exposure. Use the instrument's specified hazard class, manufacturer instructions, and applicable laboratory safety procedures; do not look into a laser beam or defeat its protective features. This qualification follows FDA laser-safety guidance rather than the slide's wavelength-only shorthand [[6]](#lidar-ref-6).

For the simulated encoder below, no real laser is operated. Simulating a short range or increasing a neural firing-rate parameter does not authorize changing a physical laser's power.

## 8.7 From samples to point clouds

### 8.7.1 Geometry and attributes

A point cloud is a collection of spatial points. The lecture lists coordinates $(X,Y,Z)$ and possible attributes such as intensity, return number, and positioning information [[1]](#lidar-ref-1), slide 35. A planar scan is a more restricted set of directions, even when plotted inside a three-dimensional viewer.

```{figure} ../assets/lidar-lecture/point-cloud-data.png
:label: fig-lidar-point-cloud-data
:alt: Planar mapping and a three-dimensional road point cloud; original media from the supplied LiDAR lecture
:width: 100%

**Planar mapping and a three-dimensional road point cloud.** A planar environment/trajectory view and a three-dimensional road view are different data representations. Source: lecture slide(s) 35 [[1]](#lidar-ref-1).
```

For a planar range $d$ at angle $\theta$ in the sensor frame,

$$
\mathbf p_s=\begin{bmatrix}d\cos\theta\\d\sin\theta\\0\end{bmatrix}.
$$

With azimuth $\theta$ and elevation $\phi$, an explicitly chosen spherical-coordinate convention is

$$
\mathbf p_s=\begin{bmatrix}
d\cos\phi\cos\theta\\
d\cos\phi\sin\theta\\
d\sin\phi
\end{bmatrix}.
$$

These equations are textbook geometry accompanying the lecture, not a claim about the packet layout of every LiDAR. A point cloud from a moving sensor must be transformed and aligned before successive observations can form a consistent map.

### 8.7.2 A ROS planar-scan contract

For the robot exercises, use the actual `LaserScan` metadata rather than assuming that an array index already equals a bearing. In the message frame, zero angle points along positive x and angles increase about positive z. The header timestamp refers to the first ray [[2]](#lidar-ref-2).

| Field | Meaning to preserve |
|---|---|
| `header.frame_id`, `header.stamp` | Measurement frame and first-ray acquisition time |
| `angle_min`, `angle_increment` | Starting bearing and angular step, radians |
| `time_increment`, `scan_time` | Inter-ray interval and inter-scan time, seconds |
| `range_min`, `range_max` | Accepted measurement limits, metres |
| `ranges` | Range samples, metres |
| `intensities` | Optional values in device-specific units |

For sample $i$, a corresponding calculation is $\theta_i=\theta_{\min}+i\Delta\theta$ and $t_i=t_0+i\Delta t_{\mathrm{ray}}$. Confirm the sensor mounting before calling these robot-body coordinates. Read the driver contract for special values; an invalid measurement is not automatically a confirmed empty ray.

## 8.8 Advantages, limitations, and failure modes

### 8.8.1 Geometry complements appearance

The lecture contrasts metric range geometry with a camera's two-dimensional image, wide horizontal coverage with a narrower illustrated camera view, and active ranging with a dark camera image [[1]](#lidar-ref-1), slides 36-38.

```{figure} ../assets/lidar-lecture/camera-and-lidar.png
:label: fig-lidar-camera-and-lidar
:alt: Image appearance and metric range geometry; original media from the supplied LiDAR lecture
:width: 100%

**Image appearance and metric range geometry.** Compare image appearance with the geometric samples shown in the source point-cloud view. Source: lecture slide(s) 36, 37 [[1]](#lidar-ref-1). Lecture image credits include KITTI, Apple, Cartographer, and NASA.
```

Read these as comparisons of the illustrated systems, not universal specifications. Not every LiDAR has a 360-degree view, and the slide's "no degradation at night" wording does not eliminate other sensing limitations. The practical benefit is that the sensor supplies its own illumination for ranging; acquisition still needs to be checked in the conditions of the intended task.

### 8.8.2 Reflective and transparent surfaces

Slide 39 warns about glass and reflective surfaces. Its own figure shows transmitted paths, reflected paths, and apparent points behind a glass surface [[1]](#lidar-ref-1). Thus "cannot detect" is better treated here as the slide's warning about **unreliable interpretation**, not as proof that every such surface always yields zero returns.

```{figure} ../assets/lidar-lecture/reflection-effects.png
:label: fig-lidar-reflection-effects
:alt: Glass can create transmitted, reflected, and misleading returns; original media from the supplied LiDAR lecture
:width: 100%

**Glass can create transmitted, reflected, and misleading returns.** Read the transmitted, reflected, and apparent paths instead of assuming that glass always produces no return. Source: lecture slide(s) 39 [[1]](#lidar-ref-1). Slide source label: Mapping with Reflection-Detection and Utilization of Reflection in 3D Lidar Scans.
```

For a neural controller, a spurious close return and a missing return have different consequences. The former may trigger avoidance; the latter should remain marked as unknown unless another validated measurement resolves it. Removing all unusual points without a documented rule can hide a real thin obstacle.

### 8.8.3 Weather and competing returns

The fog, snow, and target illustration shows how energy may return before the beam reaches the intended object. The lecture uses it to motivate weather-dependent attenuation and unwanted returns [[1]](#lidar-ref-1), slides 40-41.

```{figure} ../assets/lidar-lecture/weather-returns.png
:label: fig-lidar-weather-returns
:alt: Atmospheric particles can compete with the target return; original media from the supplied LiDAR lecture
:width: 100%

**Atmospheric particles can compete with the target return.** The figure contrasts returns from fog, snow, and the intended target; it is not a calibrated weather simulation. Source: lecture slide(s) 40 [[1]](#lidar-ref-1). Slide credit: Velodyne.
```

**Unit-reading note.** The printed wavelength on slide 40 is 1.5 mm, while the earlier wavelength discussion includes 1550 nm, which is 1.55 micrometres. Those values differ by roughly three orders of magnitude. This chapter uses the illustration qualitatively and does not turn the slide's particle-size statements or comparison table into a calibrated weather model.

In an evaluation, log the proportion of invalid sectors, unexpected near returns, and changes to the neural representation. A lower average firing rate alone does not prove improved perception: an encoder that discards difficult observations could simply be losing information.

### 8.8.4 Sequential acquisition and motion distortion

The lecture calls the within-scan timing problem a **rolling shutter effect**: early and late beams observe the scene at different times. The moving-object example shows two positions separated by 100 ms [[1]](#lidar-ref-1), slides 42-44.

```{figure} ../assets/lidar-lecture/scan-motion-distortion.png
:label: fig-lidar-scan-motion-distortion
:alt: The scene changes while a sequential scan is acquired; original media from the supplied LiDAR lecture
:width: 100%

**The scene changes while a sequential scan is acquired.** Original slide geometry and time labels are retained. The two object positions are separated by 100 ms. Source: lecture slide(s) 43 [[1]](#lidar-ref-1).
```

**Worked example.** At a constant 1 m/s, a platform translates 0.1 m during a 100 ms sweep. At a constant 90 degrees/s, it rotates 9 degrees during that interval. These are kinematic calculations, not values measured in the video. Assigning a single pose to every ray can therefore change reconstructed boundaries. Retain ray times and pose estimates when evaluating spatial representations.

## 8.9 Worked neural encoder: 36 angular sectors

### 8.9.1 State exactly what each channel represents

Retain the book's compact planar interface: **36 angular channels, each covering 10 degrees**. The number is a design choice for the robot model, not a claim about the number of biological border cells or the number of lasers in the instrument.

Wrap each body-relative angle into $[-\pi,\pi)$ and assign it to

$$
b(\theta)=\left\lfloor36\frac{\operatorname{wrap}(\theta)+\pi}{2\pi}\right\rfloor,
\qquad b\in\{0,\ldots,35\}.
$$

Sector $k$ covers $[-\pi+k\Delta\theta,-\pi+(k+1)\Delta\theta)$ with $\Delta\theta=2\pi/36$. Under this convention, sector 18 covers $[0,10^\circ)$; forward is a sector boundary, not a sector center. A centered-forward convention is also possible, but must be implemented consistently rather than silently shifting channel labels.

### 8.9.2 Aggregate valid measurements before encoding them

For each sector, select the minimum finite range within the configured limits:

$$
d_k=\min_{i\in S_k,\,\mathrm{valid}(i)}d_i.
$$

The minimum preserves the nearest observed return but discards the sector's remaining geometry and is sensitive to a single spurious close return. The median is less sensitive to an isolated outlier but can suppress a thin obstacle. Neither choice is universally correct.

A sector with no accepted return has $m_k=0$ and an unknown distance. Keep that validity mask separate from its neural activity. In the conservative implementation below, `NaN`, infinity, out-of-limit values, and nonfinite angles are excluded; a particular driver may justify a more specific interpretation of infinity, but that requires its documented contract.

### 8.9.3 The existing distance-to-rate map

For valid sectors, the teaching map remains

$$
r_k=5+45\left(1-\frac{d_k}{d_{\max}}\right)\ \mathrm{Hz},
\qquad d_{\max}=5\ \mathrm{m}.
$$

Unknown sectors receive a computational placeholder rate of zero **and retain $m_k=0$**. At valid distances of 0.8, 1.5, 3, and 4 m, prescribed rates are 42.8, 36.5, 23, and 14 Hz. A valid maximum-range observation gives 5 Hz, not the same state as unknown.

The nominal scale is 5-50 Hz; with a positive minimum accepted range, the maximum attainable valid rate is slightly below 50 Hz. For example, a 0.05 m minimum gives 49.55 Hz. These are prescribed rates, not measured LIF output rates and not photodetector intensities.

```python
import numpy as np


def sector_encode(ranges, angles, range_min=0.05, range_max=5.0, sectors=36):
    """Return nearest ranges (m), prescribed rates (Hz), and a validity mask."""
    r = np.asarray(ranges, dtype=float)
    a = np.asarray(angles, dtype=float)
    if r.ndim != 1 or a.shape != r.shape:
        raise ValueError("ranges and angles must be matching one-dimensional arrays")
    if isinstance(sectors, (bool, np.bool_)) or not isinstance(sectors, (int, np.integer)) or sectors < 1:
        raise ValueError("sectors must be a positive integer")
    if not (np.isfinite(range_min) and np.isfinite(range_max)
            and 0 <= range_min < range_max):
        raise ValueError("require finite 0 <= range_min < range_max")
    good = np.isfinite(r) & np.isfinite(a) & (r >= range_min) & (r <= range_max)
    distance = np.full(sectors, np.inf)
    # Bin only valid angles: never cast NaN or infinity to an integer.
    wrapped = np.remainder(a[good] + np.pi, 2 * np.pi)
    bins = np.floor(wrapped * sectors / (2 * np.pi)).astype(int)
    bins = np.clip(bins, 0, sectors - 1)
    np.minimum.at(distance, bins, r[good])
    valid = np.isfinite(distance)
    distance[~valid] = np.nan
    rates = np.zeros(sectors)
    rates[valid] = 5.0 + 45.0 * (1.0 - distance[valid] / range_max)
    return distance, rates, valid


distance, rates, valid = sector_encode([0.8, 3.0, np.nan], [0.0, np.pi / 2, 0.0])
assert np.isclose(distance[18], 0.8)
assert np.isclose(rates[18], 42.8)
assert np.isclose(rates[27], 23.0)
assert valid.sum() == 2
```

This function assumes angles already refer to the intended body frame. A sensor mounting translation changes both endpoint distance and bearing relative to the body origin; a simple angular offset alone is not a complete mounting transform.

```{figure} ../assets/sensor-course-lidar.png
:label: fig-sensor-lidar
:alt: Existing synthetic scan compressed into 36 body-relative sectors, prescribed firing rates, and an explicit missing-data mask
:width: 100%

**The existing 36-sector teaching experiment.** A nearer frontal obstacle, farther background, and missing angular sector illustrate the chosen distance-to-rate mapping. This is a synthetic textbook example, not a recording from the sensor hardware. Run [Laboratory 6](../notebooks/sensory_encoding.ipynb) to vary obstacle direction, sector count, and invalid samples.
```

### 8.9.4 From a prescribed rate to spike events

One possible implementation is a Poisson event generator. Under that explicit assumption, a rate $r_k$ over a window $T$ seconds gives an expected count $\mathbb E[N_k]=r_kT$. The count is not guaranteed on any one trial. For 42.8 Hz over 0.5 s, the expectation is 21.4 events; an observed count must be an integer.

For a bin of duration $\delta t$, the probability of at least one event is

$$
P(N_k\geq1)=1-\exp(-r_k\delta t).
$$

A Bernoulli approximation can discard multiple events in one bin. The code below instead samples **Poisson counts per bin**, so multiple events remain representable. It is a textbook implementation choice, not a biological claim established by the LiDAR lecture.

```python
def poisson_bin_counts(rates, valid, duration_s=0.5, dt_s=0.001, seed=8):
    """Sample event counts in each time bin, not a binary event raster."""
    r = np.asarray(rates, dtype=float)
    mask = np.asarray(valid, dtype=bool)
    if r.ndim != 1 or mask.shape != r.shape:
        raise ValueError("rates and valid must be matching one-dimensional arrays")
    if not np.isfinite(r).all() or np.any(r < 0):
        raise ValueError("rates must be finite and nonnegative")
    if not (np.isfinite(duration_s) and np.isfinite(dt_s) and duration_s > 0 and dt_s > 0):
        raise ValueError("duration and time step must be finite and positive")
    n = int(round(duration_s / dt_s))
    if n < 1 or not np.isclose(n * dt_s, duration_s, rtol=1e-10, atol=1e-12):
        raise ValueError("duration must be an integer multiple of dt_s")
    effective = np.where(mask, r, 0.0)
    rng = np.random.default_rng(seed)
    counts = rng.poisson(effective[:, None] * dt_s, size=(r.size, n))
    return counts, mask.copy()


counts, preserved_mask = poisson_bin_counts(rates, valid)
assert counts.shape == (36, 500)
assert np.all(counts[~preserved_mask] == 0)
```

A physical-unit LIF implementation instead requires a chosen current mapping and the membrane, threshold, reset, and refractory parameters from [Chapter 2](03-computational-neuron-models.md). Setting a numerical rate to 40 Hz does not imply that an arbitrary current of 40 pA produces 40 Hz. Compare count, first-spike latency, and steady firing rate before selecting a motor threshold.

## 8.10 Connect the encoder to spatial representations

For planar robot pose $(x_r,y_r,\psi)$ and a sensor aligned at the robot origin, a valid ray endpoint is

$$
x_w=x_r+d\cos(\theta+\psi),\qquad
 y_w=y_r+d\sin(\theta+\psi).
$$

For $(x_r,y_r)=(1,2)$ m, $\psi=90^\circ$, $\theta=0$, and $d=1$ m, the endpoint is $(1,3)$ m. A forward beam changes world direction when the robot turns.

With a real mounting offset and timestamp, the corresponding rigid-transform statement is

$$
\begin{bmatrix}\mathbf p_w\\1\end{bmatrix}
=T_{wb}(t_i)T_{bs}\begin{bmatrix}\mathbf p_s\\1\end{bmatrix}.
$$

$T_{bs}$ maps sensor coordinates into the body frame, and $T_{wb}(t_i)$ maps body coordinates into the world at ray time $t_i$. The transform is a modeling extension that makes the lecture's position, attitude, and timing requirements explicit.

A **36-channel sensory encoder is not itself a place-cell, grid-cell, or border-cell model**. Linking it to [Chapter 4: Spatial Cells and Their Models](02-spatial-cells.md) needs an explicit representation and test. For example, does a candidate border response stay tied to the same world boundary when the robot changes heading? Pose errors and scan distortion can imitate a changing spatial representation.

For a reproducible experiment, retain the raw scan and timestamps, mounting transform, validity mask, sector aggregation rule, prescribed activity, emitted events, and motor command. First test the sensor-to-neural mapping in replay; only then judge learning or navigation. A controller receiving simulator ground-truth object labels instead of the scan is solving a different problem.

## 8.11 Additional Reading Materials

Read lecture slides 2-9 for ranging and scanning; 12-21 for wavelength and hardware; 22-29 for survey applications and returns; 30-35 for parameters and point clouds; and 36-44 for strengths and failure modes [[1]](#lidar-ref-1). The embedded videos preserve the source lecture links, while their adjacent questions are teaching prompts rather than transcripts.

For implementation, read the complete `LaserScan` definition [[2]](#lidar-ref-2). For the specific clarifications used here, consult the MathWorks overview, the cited silicon-photonic LiDAR paper, NEON's waveform tutorial, and FDA laser guidance [[3]](#lidar-ref-3)-[[6]](#lidar-ref-6). The source PDF and PPTX share 56 slide positions; the filename says Topic 6 while the title slide says Topic 5. Citations in this chapter use **1-based slide order**, not the offset printed footer.

Continue to [Chapter 9](09-nengo-ros-gazebo.md) for simulator integration.

(85-exercises)=
## 8.12 Exercises

1. Compute the prescribed rate at 1.5 m and compare it with 4 m.
2. Compare minimum range with median range when one ray is an outlier.
3. Rotate the synthetic scan by 90 degrees. Which quantities should change in body and world coordinates?
4. Explain why `inf`, `nan`, and a valid maximum-range measurement may require different handling for a particular sensor.
5. Compute range from a 100 ns round-trip delay. Explain why dividing by two is necessary.
6. A receiver distinguishes two returns separated by 1 ns. Compute their ideal range separation and explain why this is not automatically its absolute range accuracy.
7. Identify the transmitter, receiver, scanner, and electrical processing path in the component figure. Distinguish hardware elevation channels from neural angular sectors.
8. Explain why the silicon-photonic MEMS switch array and the phased-array animation should not be described as the same architecture.
9. Interpret red, yellow, and green in the tree-return illustration. Explain why the strongest return need not be the first return.
10. Compare FOV with angular spacing. Compute the equal-range separation at 10 m for rays 1 degree apart and 10 degrees apart.
11. Determine the sector indices for $-180^\circ$, $-175^\circ$, $0^\circ$, $90^\circ$, $179^\circ$, and $180^\circ$ using the chapter's convention.
12. Feed ranges $[0.8,3.0,\mathrm{NaN},5.0]$ at angles $[0^\circ,90^\circ,0^\circ,179^\circ]$ into the encoder. Report the valid sectors and rates.
13. Compute the expected count in 500 ms at 42.8 Hz and the probability of at least one event in a 1 ms bin. Explain why an expected count need not be an integer.
14. A robot moves at 1 m/s and rotates at 90 degrees/s during a 100 ms scan. Calculate the translation and heading change; identify the metadata needed to account for acquisition time.
15. Transform the 1 m forward ray for the pose given in Section 8.10. Explain what changes when the LiDAR is mounted away from the body origin.
16. Design a replay test using a sequence of simulated LiDAR scans that separates missing returns, spurious close returns, and neural-encoding errors. State which information is available to the encoder and which simulator variables are used only for evaluation.

[Worked solutions](solutions-embodied.md#lidar-solutions) are provided at the end of the book.

## References

(lidar-ref-1)=

[1] Hongyu An, *Neuromorphic Robotic Systems: Introduction to LiDAR*, course lecture slides, Department of Electrical and Computer Engineering, Michigan Technological University, supplied files "Neuromorphic Robotic Systems-Topic 6 Introduction to LIDAR.pptx" and the matching PDF, 56 slides. Publication date not specified. Original images, animation frames, video identifiers, and source credits are recorded in the repository's `assets/lidar-lecture/manifest.json`.

(lidar-ref-2)=

[2] ROS 2 contributors, "LaserScan message," *sensor_msgs*, Jazzy distribution. [Official message definition](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/LaserScan.msg).

(lidar-ref-3)=

[3] The MathWorks, Inc., "Introduction to Lidar," *MATLAB and Simulink Documentation*. [Official overview](https://www.mathworks.com/help/pointcloud/gs/lidar-processing-overview.html). Accessed Nov. 13, 2026. The lecture's older LiDAR Toolbox URL redirects to this overview.

(lidar-ref-4)=

[4] Xiaosheng Zhang, Kyungmok Kwon, Johannes Henriksson, Jianheng Luo, and Ming C. Wu, "A large-scale microelectromechanical-systems-based silicon photonics LiDAR," *Nature*, vol. 603, no. 7900, pp. 253-258, 2022, doi: 10.1038/s41586-022-04415-8. [Open-access article](https://pmc.ncbi.nlm.nih.gov/articles/PMC8907073/).

(lidar-ref-5)=

[5] Leah A. Wasser, "The Basics of LiDAR - Light Detection and Ranging - Remote Sensing," *National Ecological Observatory Network*. [Tutorial linked by the lecture](https://www.neonscience.org/resources/learning-hub/tutorials/lidar-basics). Accessed Nov. 13, 2026.

(lidar-ref-6)=

[6] U.S. Food and Drug Administration, "Frequently Asked Questions About Lasers." [Official safety guidance](https://www.fda.gov/radiation-emitting-products/laser-products-and-instruments/frequently-asked-questions-about-lasers). Accessed Nov. 13, 2026.

