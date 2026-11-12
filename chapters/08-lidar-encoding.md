---
title: "Chapter 8 · LiDAR and Thirty-Six-Channel Spatial Encoding"
---

## 8.1 Learning objectives

You will derive a time-of-flight range, compress rays into 36 ten-degree sectors, preserve unknown-data masks, and distinguish body-relative sensing from spatial-cell representations. The example follows the course's LiDAR sensing topic and provides a small input interface for later spatial models.

## 8.2 Range and coordinate conventions

For ideal round-trip time $\Delta t$, range is $d=c\Delta t/2$. The factor two accounts for outward and return travel. A 3 m target gives approximately 20 ns when $c\approx3\times10^8$ m/s. A software encoder that emits earlier spikes for nearer targets uses an additional chosen latency rule: its millisecond spike delay is not the physical optical flight time.

A ROS LaserScan gives angular samples, range limits, timestamps, and timing metadata. Angles increase counterclockwise around the positive z axis, with zero forward along x [[1]](#lidar-ref-1). Confirm the actual sensor mounting and transform before applying that convention to a robot body frame.

## 8.3 Worked example — 36 sectors

Wrap each body-relative angle into $[-\pi,\pi)$ and assign

$$
b(\theta)=\left\lfloor36\frac{\operatorname{wrap}(\theta)+\pi}{2\pi}\right\rfloor.
$$

For each sector, choose the minimum finite range within the sensor limits. This nearest-obstacle feature discards the rest of the sector's geometry. Keep a validity mask. A sector with no valid return is **unknown**, and must not silently become measured free space.

```python
import numpy as np

def sector_encode(ranges, angles, range_min=.05, range_max=5., sectors=36):
    r, a = np.asarray(ranges), np.asarray(angles)
    bins = np.floor(((a+np.pi) % (2*np.pi)) * sectors/(2*np.pi)).astype(int)
    good = np.isfinite(r) & np.isfinite(a) & (r >= range_min) & (r <= range_max)
    distance = np.full(sectors, np.nan)
    for k in range(sectors):
        values = r[good & (bins == k)]
        if values.size:
            distance[k] = values.min()
    valid = np.isfinite(distance)
    rates = np.zeros(sectors)
    rates[valid] = 5 + 45*(1-distance[valid]/range_max)
    return distance, rates, valid
```

This prescribed-rate mapping uses a 5–50 Hz scale, a 5 m maximum range, and zero input for unknown sectors **together with their mask**. Valid 0.8 m and 3 m measurements prescribe 42.8 and 23 Hz. These are not guaranteed LIF output rates; to produce LIF spikes, calibrate a separate rate-to-current mapping.

```{figure} ../assets/sensor-course-lidar.png
:label: fig-sensor-lidar
:alt: Thirty-six body-relative range sectors and their prescribed firing rates, including an explicitly missing sector
:width: 100%

Original synthetic scan: a nearer frontal obstacle, farther background, and a missing angular sector. Run [Laboratory 6](../notebooks/sensory_encoding.ipynb) to change sector count, obstacle angle, or invalid samples.
```

## 8.4 From a ray to a spatial representation

For planar robot pose $(x_r,y_r,\psi)$ and an aligned sensor at the robot origin, a valid endpoint is

$$
x_w=x_r+d\cos(\theta+\psi),\qquad
y_w=y_r+d\sin(\theta+\psi).
$$

A real mounting offset adds a rigid transform. For $(x_r,y_r)=(1,2)$ m, $\psi=90^\circ$, $\theta=0$, and $d=1$ m, the endpoint is $(1,3)$ m. A forward beam becomes a different world direction when the robot turns.

A 36-channel sensory encoder is not itself a place-cell, grid-cell, or border-cell model. Connecting it to [Chapter 3](02-spatial-cells.md) requires an explicit representation and a test: for example, does activity remain tied to a world boundary across changes in heading? Robot pose error and scan distortion can produce apparent remapping. Retain raw timestamps, frame transforms, and occupancy information when testing that claim.

## 8.5 Exercises

1. Compute the prescribed rate at 1.5 m and compare it with 4 m.
2. Compare minimum range with median range when one ray is an outlier.
3. Rotate the synthetic scan by 90 degrees. Which quantities should change in body and world coordinates?
4. Explain why `inf`, `nan`, and a valid maximum-range measurement may require different handling for a particular sensor.

## References

(lidar-ref-1)=

[1] ROS 2 contributors, “LaserScan message,” *sensor_msgs*, Jazzy distribution. [Official message definition](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/LaserScan.msg).

## Additional Reading Materials

Read the course's LiDAR ranging material and the complete message fields in [[1]](#lidar-ref-1), especially scan and per-ray timing. Compare this compact encoder with Chapter 3's distinction between sensory input and an environment-relative spatial firing field. More detailed learned spatial networks remain on the [research roadmap](roadmap.md).
