---
title: "Chapter 6 · Visual Perception and Visual Cue Encoding"
---

## 6.1 Learning objectives

You will connect image formation to a measured visual feature, implement a simple red-cue encoder, explain lighting and camera limitations, and evaluate a visual cue independently of the learning rule. This chapter follows the course's camera, color, and image-processing lectures [[1]](#vision-ref-1).

## 6.2 From scene to pixels

For an ideal pinhole camera, a point $(X,Y,Z)$ in the camera frame projects to $x=fX/Z$ and $y=fY/Z$. Here $f$, $x$, and $y$ have the same length unit. Pixel coordinates additionally require calibration and a principal point. A larger object in the image may be nearer, physically larger, or both. Brightness alone does not establish distance.

CCD and CMOS describe sensor technologies, while color-filter arrangements and demosaicing determine how a color image is formed. Exposure, white balance, lens distortion, and motion blur affect the values delivered to the neural encoder. The synthetic example below begins with normalized RGB values; it does not simulate a camera sensor or demosaicing [[1]](#vision-ref-1).

## 6.3 Worked example — a red cue

Let normalized channels $R,G,B\in[0,1]$. Define a simple red-contrast feature over a chosen region of interest (ROI),

$$
z_R=\frac{1}{N}\sum_{p=1}^{N}\operatorname{clip}\!\left(R_p-\frac{G_p+B_p}{2},0,1\right).
$$

It is a deliberately transparent detector, not a learned classifier. A pure red patch gives 1; ideal white and blue patches give 0. Dim red $(0.4,0,0)$ gives 0.4. If a red patch fills only one quarter of the ROI against a white background, the feature is 0.25: the averaging step loses object size and location.

```python
import numpy as np

def red_feature(rgb):
    rgb = np.asarray(rgb, dtype=float)  # normalize uint8 images by 255 first
    if rgb.shape[-1] != 3 or np.any((rgb < 0) | (rgb > 1)):
        raise ValueError("Expected normalized RGB.")
    return np.clip(rgb[..., 0] - .5*(rgb[..., 1]+rgb[..., 2]), 0, 1).mean()

z = red_feature(np.array([[[1., 0., 0.]]]))
current_pa = 50 + 250*z
print(z, current_pa)  # 1.0, 300.0 pA
```

[Laboratory 6](../notebooks/sensory_encoding.ipynb) applies each current for 500 ms to the Chapter 2 LIF neuron. The baseline is below rheobase. Dim red in this example reaches exactly 150 pA and remains below the event threshold over a finite run; full red elicits repeated events. These are encoding results under chosen parameters, not camera detection accuracies.

```{figure} ../assets/sensor-course-vision.png
:label: fig-sensor-vision
:alt: Synthetic red, white, blue and dim red patches compared with LIF spike counts under a declared current mapping
:width: 100%

Original generated color-patch experiment. Change patch color, occupied ROI fraction, or current gain in the notebook before connecting a learned motor response.
```

## 6.4 Filtering and robust tests

A normalized Gaussian kernel $G_\sigma$ smooths an image by convolution, $\widetilde I=G_\sigma*I$. The parameter $\sigma$ is measured in pixels. Smoothing can reduce high-frequency noise but blur a small cue into its background. Specify boundary handling, kernel size, ROI, and whether filtering occurs before nonlinear clipping. The two orders generally give different results.

A useful exercise adds noise to the synthetic patches and compares the detector with and without smoothing. Keep a held-out set of cue sizes and brightness levels. Report true detections, missed cues, and false positives on red distractors. A red floor or a nearby red object can trigger the same feature as a red wall. Learning must not receive a hidden scene label in place of the actual image-derived cue.

## 6.5 Connect to association and spatial representations

For the Chapter 10 association experiment, threshold a calibrated feature into a CS event or retain its graded value with a declared rule. Log the raw feature so a failed trial can be traced to perception, encoding, learning, or control. Red contrast alone does not encode allocentric position. Spatial-cell experiments additionally need geometry, pose, or an explicitly learned representation.

## 6.6 Exercises

1. Calculate $z_R$ for $(0.8,0.2,0.2)$ and the resulting input current.
2. Explain how shrinking a red cue inside a fixed ROI changes the response.
3. Design a held-out lighting test without retraining the detector on the test images.
4. Compare clipping before averaging with clipping the mean contrast.

## References

(vision-ref-1)=

[1] Peter Corke, *Robotics, Vision and Control: Fundamental Algorithms in Python*, 3rd ed. Cham, Switzerland: Springer, 2023, doi: [10.1007/978-3-031-06469-2](https://link.springer.com/book/10.1007/978-3-031-06469-2).

## Additional Reading Materials

Read the camera and image-processing material in [[1]](#vision-ref-1). Compare the course's Visual Perception I/II material on imaging, color, and Gaussian filtering with the narrower cue-detector contract used here. Continue to [Chapter 7](07-inertial-sensing.md) to construct the second input to the association experiment.
