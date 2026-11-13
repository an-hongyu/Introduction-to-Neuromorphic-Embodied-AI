---
title: "Chapter 6 · Visual Perception and Encoding"
---

## 6.1 Learning objectives


This chapter follows the two supplied **Visual Perception** lecture decks: Part I develops robot perception, light, image formation, and camera sensors; Part II develops color perception, digital images, and image processing [[1]](#vision-ref-1), [[2]](#vision-ref-2). The final RGB-to-LIF experiment is retained from this textbook as an explicit application, rather than presented as an experiment reported in the slides.

By the end of this chapter, you should be able to:

- Locate visual perception within a robot's sense–plan–act loop.
- Explain the roles of illumination, reflection, optics, and an image sensor in image formation.
- Distinguish radiometric quantities from photometric quantities and identify their units.
- Explain pinhole-image inversion, the aperture tradeoff, CCD/CMOS readout, and Bayer color sampling.
- Interpret cone-response curves, tristimulus values, color matching, and RGB representations.
- Represent binary, grayscale, and RGB images as arrays with explicit shapes and value ranges.
- Apply point operations, thresholding, mean and Gaussian filters, and dyadic image operations.
- Trace a visual cue from pixels through a measured feature to current and LIF spikes, and test each stage separately.

## 6.2 Robot perception: from sensing to interpretation

### 6.2.1 The sense–plan–act loop

The lectures define robot perception as using sensors to obtain information about the environment, processing that information, and interpreting the surrounding world. A robot's **sensor** is the physical measurement device; **sensing/perception** processes its output; **planning** selects an action; and an **actuator** carries out that action. These roles form a loop because acting changes the next sensory observation [[1]](#vision-ref-1), slides 3–10 and 74.

For a mobile robot with a camera, the camera supplies an image, an image-processing stage detects a visual cue, a controller selects a response, and motors move the robot. The image itself is not yet a decision. The same distinction applies to the other sensors listed in the lectures: force/tactile sensors, inertial sensors, odometry, sonar, LiDAR, and GPS.

**Reading the lecture examples.** Image classification assigns an image-level category; object detection identifies objects and their locations; segmentation assigns labels to image regions or pixels; image retrieval finds similar images. These tasks produce different outputs. Detecting a colored landmark for navigation is a narrower problem than recognizing all objects in a scene [[1]](#vision-ref-1), slides 18–26.

```{figure} ../assets/visual-perception-slides/detection-and-segmentation.png
:label: fig-vision-slide-detection-and-segmentation
:alt: Different outputs from visual perception; original illustration from the supplied Visual Perception lectures
:width: 100%

**Different outputs from visual perception.** Left: object detections are shown as labeled boxes. Right: the lecture contrasts a photographed scene with region-level semantic labels. Compare what information each output preserves. Source: Part I, slide 26 [[1]](#vision-ref-1).
```

### 6.2.2 Biological motivation and computational vision

The biological introduction follows light into the retina and then through the visual pathway toward the lateral geniculate nucleus and primary visual cortex. Its orientation-selectivity example illustrates a useful principle: a neuron's response can depend on a feature of a stimulus, not simply on total light intensity. The subsequent slides connect feature extraction with edge-based recognition, part-based representations, backpropagation, and convolutional networks [[1]](#vision-ref-1), slides 14–26.

```{figure} ../assets/visual-perception-slides/visual-pathway.png
:label: fig-vision-slide-visual-pathway
:alt: From the eyes to visual cortex; original illustration from the supplied Visual Perception lectures
:width: 85%

**From the eyes to visual cortex.** Follow the colored pathways from the two visual fields through the optic nerves and optic chiasm toward the lateral geniculate nucleus and primary visual cortex. Source: Part I, slide 16 [[1]](#vision-ref-1).
```

This is a conceptual progression, not an assertion that a camera reproduces the retina or that a convolutional network is a complete model of visual cortex. In the experiment at the end of this chapter, the chosen feature is red contrast. Its simplicity makes the measurement-to-neural-response chain inspectable.

```{figure} ../assets/visual-perception-slides/orientation-selectivity.png
:label: fig-vision-slide-orientation-selectivity
:alt: Orientation-selective visual responses; original illustration from the supplied Visual Perception lectures
:width: 80%

**Orientation-selective visual responses.** The lecture figure combines a light-bar stimulus, recorded spike trains, and a tuning curve. The visual response varies with bar orientation, illustrating feature selectivity. Source: Part I, slide 17 [[1]](#vision-ref-1).
```

## 6.3 Light, surfaces, and image formation

### 6.3.1 Follow the light before interpreting the pixel

The lectures' image-formation sequence is **object → lens → sensor → data**. More explicitly, light leaves a source, interacts with a surface, and a portion enters the camera. Illumination has both intensity and a spectrum. Surface reflection changes the light reaching the observer; the camera's optics and sensor then determine the recorded values [[1]](#vision-ref-1), slides 28–35 and 57–70; [[2]](#vision-ref-2), slides 2–4 and 12–13.

```{figure} ../assets/visual-perception-slides/light-surface-camera.png
:label: fig-vision-slide-light-surface-camera
:alt: Illumination, surface reflection, and camera geometry; original illustration from the supplied Visual Perception lectures
:width: 100%

**Illumination, surface reflection, and camera geometry.** Trace the path from the light source to the surface, through the optics, and onto the sensor plane. The diagram connects scene illumination to the image-formation discussion. Source: Part II, slide 3 [[2]](#vision-ref-2).
```

Consequently, an RGB triplet is not a property of the object alone. A colored cue observed under one light source can produce different values under another. The course repeatedly returns to this interaction between illumination, surface reflectance, and measurement. It is the reason a robot should not interpret an arbitrary pixel threshold as an illumination-independent object label.

The spectrum diagrams place visible light within the much wider electromagnetic spectrum. Part I gives approximate visible ranges of 400–700 nm and 380–750 nm in different introductory slides, and a broader range in the photometry discussion. These are presented as the lecture's approximate conventions, not as one sharply defined universal visibility boundary [[1]](#vision-ref-1), slides 29–34.

```{figure} ../assets/visual-perception-slides/electromagnetic-spectrum.png
:label: fig-vision-slide-electromagnetic-spectrum
:alt: Visible light within the electromagnetic spectrum; original illustration from the supplied Visual Perception lectures
:width: 100%

**Visible light within the electromagnetic spectrum.** The expanded color band shows the visible region within a much wider range of wavelengths. Read the wavelength labels as the approximate convention used in the lecture. Source: Part I, slide 33 [[1]](#vision-ref-1).
```

### 6.3.2 Radiometry versus photometry

**Radiometry** measures electromagnetic radiation on a physical basis. **Photometry** weights visible radiation according to a model of human visual sensitivity. Equal physical power at different wavelengths need not correspond to equal photometric measurements [[1]](#vision-ref-1), slides 32–34 and 76.

| Quantity being described | Radiometric quantity and unit | Photometric counterpart and unit |
|---|---|---|
| Total power | Radiant flux, W | Luminous flux, lm |
| Power per solid angle | Radiant intensity, W/sr | Luminous intensity, cd = lm/sr |
| Incident flux per area | Irradiance, W/m² | Illuminance, lx = lm/m² |
| Directional flux per projected area | Radiance, W/(sr·m²) | Luminance, cd/m² |

This selection follows the units table in Part I, slide 76. A **steradian (sr)** measures solid angle. Do not interchange watts, lumens, and pixel values: they represent different quantities. An integer stored in an image is not automatically a calibrated measurement in either watts or lux.

## 6.4 From a pinhole camera to a digital image sensor

### 6.4.1 Why a pinhole forms an inverted image

The lecture first shows an unstructured collection of rays reaching a sensor: multiple scene points contribute to the same locations, so the image is blurred. Introducing a barrier with a small opening constrains the rays. Rays from the top of an object pass through the opening and reach the lower part of the image plane, and vice versa. This explains the inverted image in the pinhole demonstration [[1]](#vision-ref-1), slides 35–43.

```{figure} ../assets/visual-perception-slides/pinhole-image-inversion.png
:label: fig-vision-slide-pinhole-image-inversion
:alt: Why the pinhole image is inverted; original illustration from the supplied Visual Perception lectures
:width: 100%

**Why the pinhole image is inverted.** The original lecture diagram retains the object, the inverted image, and the crossing rays. Trace a ray from the top of the tree to the lower part of the image. Source: Part I, slide 41 [[1]](#vision-ref-1).
```

The existing textbook's ideal projection equations provide a mathematical companion to that ray diagram:

$$
x'=f\frac{X}{Z},\qquad y'=f\frac{Y}{Z}.
$$

Here $(X,Y,Z)$ is a point in the camera frame, $Z>0$ is depth, and $f$, $x'$, and $y'$ use the same length unit. This positive-sign convention uses a **virtual image plane in front of the pinhole**. A physical image plane behind the pinhole gives the inverted, negative-sign coordinates shown by the lecture's ray construction. Pixel coordinates require additional scale and origin conventions.

**Worked geometric example.** With $f=10$ mm, $X=200$ mm, and $Z=1000$ mm, $x'=2$ mm. Keeping $X$ fixed while doubling $Z$ reduces $x'$ to 1 mm. This is a calculation under the declared projection model, not a camera measurement supplied by the slides. Apparent image size alone cannot distinguish a small nearby object from a larger distant one.

### 6.4.2 Aperture size and the purpose of the lens

A small opening blocks much of the available light, so exposure can become long. Making the opening larger admits more light but also broadens the set of rays reaching each image location. Making it extremely small introduces diffraction. The lecture compares apertures from 2 mm down to 0.07 mm to illustrate why “smaller is always sharper” is not a sufficient design rule [[1]](#vision-ref-1), slides 44–49.

```{figure} ../assets/visual-perception-slides/pinhole-aperture-comparison.png
:label: fig-vision-slide-pinhole-aperture-comparison
:alt: Aperture size and image sharpness; original illustration from the supplied Visual Perception lectures
:width: 100%

**Aperture size and image sharpness.** The six source images compare the labeled apertures from 2 mm to 0.07 mm. The lecture highlights 0.35 mm in this example and marks diffraction at the smallest openings; this is not a universal optimum. Source: Part I, slide 49 [[1]](#vision-ref-1).
```

A lens provides a way to collect more light while forming an image. The lecture then contrasts photographic film with reusable silicon sensors. For this chapter, the important transition is from an optical image to a spatial array of electrical measurements, not the historical details of individual camera products [[1]](#vision-ref-1), slides 50–57.

### 6.4.3 CCD and CMOS readout

The slides describe a **charge-coupled device (CCD)** as an array in which accumulated charge is transferred between neighboring elements and eventually reaches sense amplifiers and an analog-to-digital converter. The **CMOS** discussion emphasizes local amplification and multiplexed readout. The later photodiode slide makes the light-to-electrical conversion explicit: absorbed light produces a photodetector response, and microlenses help direct light toward the sensitive region [[1]](#vision-ref-1), slides 58–68.

```{figure} ../assets/visual-perception-slides/ccd-cmos-readout.png
:label: fig-vision-slide-ccd-cmos-readout
:alt: CCD and CMOS image-sensor readout; original illustration from the supplied Visual Perception lectures
:width: 100%

**CCD and CMOS image-sensor readout.** The source illustration contrasts charge transfer in a CCD with charge-to-voltage conversion and active-pixel structure in CMOS. Keep the readout architecture separate from the later color-filter pattern. Source: Part I, slide 58 [[1]](#vision-ref-1).
```

These are architectural distinctions, not color encodings. A sensor technology and a color-filter arrangement answer different questions: the first concerns how a signal is acquired and read, whereas the second concerns which spectral components contribute to each sample.

### 6.4.4 Bayer sampling and RGB channels

The Bayer-filter slides show an array of photosites covered by red, green, or blue filters, with twice as many green-filtered sites as red or blue sites. A single filtered photosite measures its selected spectral band; it is not already a complete three-channel pixel. The lectures then contrast the color image we see with its separate RGB channels [[1]](#vision-ref-1), slides 63–67.

```{figure} ../assets/visual-perception-slides/bayer-filter-system.png
:label: fig-vision-slide-bayer-filter-system
:alt: Bayer color sampling; original illustration from the supplied Visual Perception lectures
:width: 100%

**Bayer color sampling.** The original diagram connects incoming light, the filter layer, the sensor array, and the resulting Bayer sequence. The colored photosites are samples used to form a color image, not complete RGB triplets. Source: Part I, slide 64 [[1]](#vision-ref-1).
```

A representative 2 × 2 Bayer arrangement is

$$
\begin{bmatrix}R&G\\G&B\end{bmatrix}.
$$

This is a sampling pattern, not four RGB triplets. Reconstruction of a full RGB image and a subsequent neural encoder are different processing stages. The synthetic cue experiment in Section 6.10 starts with RGB arrays and does **not** simulate sensor readout or color reconstruction.

The sensor-resolution example contains $4912\times3684=18{,}095{,}808$ photosites, approximately 18.1 megapixels. At a 1.25 μm pitch, the corresponding dimensions are approximately 6.14 mm × 4.61 mm. These values are arithmetic from the lecture diagram, not specifications for every camera [[1]](#vision-ref-1), slides 61 and 69.

## 6.5 Color perception and tristimulus measurement

### 6.5.1 Rods, cones, and overlapping spectral responses

Part II distinguishes rods, emphasized for sensitivity under low illumination, from cones, emphasized for color-sensitive daylight vision. It introduces three cone classes with long-, medium-, and short-wavelength sensitivity. The plotted curves overlap: the “red,” “green,” and “blue” labels used in the slides should be read together with these broad spectral responses, not as three nonoverlapping wavelength bins [[2]](#vision-ref-2), slides 5–9.

```{figure} ../assets/visual-perception-slides/cone-spectral-responses.png
:label: fig-vision-slide-cone-spectral-responses
:alt: Overlapping cone sensitivities; original illustration from the supplied Visual Perception lectures
:width: 85%

**Overlapping cone sensitivities.** The long-, medium-, and short-wavelength response curves overlap. Use the plotted wavelength axis rather than interpreting the color names as three disjoint spectral bands. Source: Part II, slide 9 [[2]](#vision-ref-2).
```

The lecture also distinguishes light's spectrum from an observer's representation of color. Three primary channels are useful because of the observer and the chosen representation; the physical spectrum itself need not contain only three wavelengths. The primary wavelengths quoted in the lecture are examples in its color-matching discussion, not the peak sensitivities of every cone or the filters of every camera.

### 6.5.2 The three response integrals

Following the lecture notation, let $L(\lambda)$ describe the spectrum reaching the observer, and let $M_r(\lambda)$, $M_g(\lambda)$, and $M_b(\lambda)$ describe the three spectral sensitivities. The responses are

$$
\rho=\int L(\lambda)M_r(\lambda)\,d\lambda,\qquad
\gamma=\int L(\lambda)M_g(\lambda)\,d\lambda,\qquad
\beta=\int L(\lambda)M_b(\lambda)\,d\lambda.
$$

The response vector $(\rho,\gamma,\beta)^\top$ is the lecture's **tristimulus** description [[2]](#vision-ref-2), slides 12–13. Each integral combines the same incoming spectrum with a different sensitivity function. These response coordinates are not automatically the 8-bit RGB values stored by a particular camera.

```{figure} ../assets/visual-perception-slides/tristimulus-light-path.png
:label: fig-vision-slide-tristimulus-light-path
:alt: From a reflected spectrum to three responses; original illustration from the supplied Visual Perception lectures
:width: 100%

**From a reflected spectrum to three responses.** The source figure places the illuminant, surface, and observer beside spectral plots and the three cone-response areas. It provides the visual counterpart to the response integrals above. Source: Part II, slide 12 [[2]](#vision-ref-2).
```

For sampled wavelengths, a numerical interpretation is $\rho\approx\sum_k L(\lambda_k)M_r(\lambda_k)\Delta\lambda$, with analogous sums for the other channels. The wavelength increment must be included; doubling the number of samples should not by itself double the predicted response. This discrete expression is a mathematical implementation of the slide's integral, not additional experimental data.

### 6.5.3 Matching a single-wavelength stimulus

The lecture treats a monochromatic stimulus as an impulse at $\lambda_s$. Writing that impulse explicitly as $L(\lambda)=L_s\delta(\lambda-\lambda_s)$ gives

$$
\begin{bmatrix}\rho\\\gamma\\\beta\end{bmatrix}
=L_s\begin{bmatrix}M_r(\lambda_s)\\M_g(\lambda_s)\\M_b(\lambda_s)\end{bmatrix}.
$$

The delta notation makes precise the impulse interpretation stated on slide 15. An ordinary function that is nonzero at only one point would not give the same finite integral.

Now combine three primary lights at $\lambda_r,\lambda_g,\lambda_b$ with amounts $R,G,B$. Define

$$
A=\begin{bmatrix}
M_r(\lambda_r)&M_r(\lambda_g)&M_r(\lambda_b)\\
M_g(\lambda_r)&M_g(\lambda_g)&M_g(\lambda_b)\\
M_b(\lambda_r)&M_b(\lambda_g)&M_b(\lambda_b)
\end{bmatrix}.
$$

The matching problem is

$$
A\begin{bmatrix}R\\G\\B\end{bmatrix}
=L_s\begin{bmatrix}M_r(\lambda_s)\\M_g(\lambda_s)\\M_b(\lambda_s)\end{bmatrix}.
$$

If $A$ is invertible, solving this system gives the primary amounts. The lecture calls the wavelength-dependent results **color-matching functions** [[2]](#vision-ref-2), slides 15–20. Matching the three responses does not mean the mixture and the test light have identical physical spectra.

```{figure} ../assets/visual-perception-slides/color-matching-functions.png
:label: fig-vision-slide-color-matching-functions
:alt: Color-matching functions; original illustration from the supplied Visual Perception lectures
:width: 90%

**Color-matching functions.** The original plot shows the three wavelength-dependent matching coefficients, including a negative portion of the red coefficient. This leads to the experimental interpretation in the next subsection. Source: Part II, slide 20 [[2]](#vision-ref-2).
```

### 6.5.4 Why a color-matching coefficient can be negative

The experimental diagram compares a test-light field with a mixture of primary lights. Some matches require a primary to be added to the **test-light side**. Moving that term to the other side of the matching equation produces a negative coefficient. It does not describe a source emitting negative optical power [[2]](#vision-ref-2), slides 21–24.

```{figure} ../assets/visual-perception-slides/color-matching-experiment.png
:label: fig-vision-slide-color-matching-experiment
:alt: The color-matching experiment; original illustration from the supplied Visual Perception lectures
:width: 100%

**The color-matching experiment.** An observer compares the test-light field with the primary-light mixture. Relate the two fields in this diagram to moving a primary-light contribution from one side of the matching equation to the other. Source: Part II, slide 22 [[2]](#vision-ref-2).
```

For example, a formal match $\mathbf t=-0.2\mathbf p_R+0.6\mathbf p_G+0.3\mathbf p_B$ can be rewritten as $\mathbf t+0.2\mathbf p_R=0.6\mathbf p_G+0.3\mathbf p_B$. The coefficients here are a chosen algebraic example; the rearrangement explains the lecture's negative-value interpretation.

## 6.6 Digital images and color representations

### 6.6.1 Images as arrays

The lectures move from a photographed scene to the values stored at pixel locations. Let $I[v,u,c]$ denote a channel value, where $u$ is the column, $v$ the row, and $c$ the channel. The indexing convention is explicit here because image coordinates and array indices are easy to confuse [[2]](#vision-ref-2), slides 25–39.

| Representation | Typical array shape | Meaning of one entry |
|---|---|---|
| Binary | $H\times W$ | A two-valued decision, such as foreground/background |
| Grayscale | $H\times W$ | An intensity value |
| RGB | $H\times W\times3$ | One of three color-channel values |

For the lecture's 8-bit RGB example, each channel is an integer from 0 to 255. Three 8-bit channels give $256^3=16{,}777{,}216$ possible triplets. An 800 × 600 × 3 uncompressed array contains 1,440,000 one-byte channel samples, before file headers or compression.

```{figure} ../assets/visual-perception-slides/rgb-pixels-and-values.png
:label: fig-vision-slide-rgb-pixels-and-values
:alt: A color image is an array of numbers; original illustration from the supplied Visual Perception lectures
:width: 100%

**A color image is an array of numbers.** The enlarged sample region connects a familiar color image with channel values stored at individual pixel locations. The numerical array and the displayed image are two representations of the same input. Source: Part II, slide 36 [[2]](#vision-ref-2).
```

**Reading note.** The caption on Part II, slide 35, describes all nonzero grayscale values as white. That statement conflicts with the same slide's description of intensity levels and its grayscale image. Here, zero denotes black and intermediate grayscale values remain intermediate; the two-valued foreground/background interpretation belongs to the binary example on slide 34.

```{figure} ../assets/visual-perception-slides/rgb-channel-decomposition.png
:label: fig-vision-slide-rgb-channel-decomposition
:alt: The image and its separate RGB channels; original illustration from the supplied Visual Perception lectures
:width: 100%

**The image and its separate RGB channels.** The full-color source image appears beside the lecture's red-, green-, and blue-channel views. Inspect how the same facial features contribute differently to the three channels. Source: Part I, slide 66 [[1]](#vision-ref-1).
```

JPEG, TIFF, PNG, and GIF are introduced as file formats. The lecture emphasizes that JPEG compression is lossy and trades stored size against image fidelity. The decoded pixel array and the file's compressed byte count are therefore different objects [[2]](#vision-ref-2), slides 37–38.

### 6.6.2 RGB, chromaticity, and HSV

RGB is an additive representation: varying its three components produces a range of colors. Part II also introduces normalized coordinates and HSV/HSL as alternative descriptions. Its chromaticity figures show mixtures along lines between two primaries and within the region bounded by several primaries [[2]](#vision-ref-2), slides 25–30 and 64–66.

```{figure} ../assets/visual-perception-slides/color-space-image-channels.png
:label: fig-vision-slide-color-space-image-channels
:alt: Alternative channel representations; original illustration from the supplied Visual Perception lectures
:width: 100%

**Alternative channel representations.** The source figure shows a color scene alongside hue, saturation, monochrome intensity, and two additional chromatic-channel views labeled in the original caption. Compare the structures retained by each representation. Source: Part II, slide 30 [[2]](#vision-ref-2).
```

For a nonzero RGB triplet, define the normalized ratios

$$
r_n=\frac{R}{R+G+B},\quad g_n=\frac{G}{R+G+B},\quad b_n=\frac{B}{R+G+B},\quad r_n+g_n+b_n=1.
$$

For the slide's $(R,G,B)=(0.5,0.2,0.9)$, these are $(0.3125,0.125,0.5625)$. Division is undefined for $(0,0,0)$, so code must handle that case explicitly.

**Coordinate note.** Slide 66 names these normalized RGB quantities $x,y,z$ while displaying a chromaticity diagram. This chapter uses $r_n,g_n,b_n$ to identify exactly what its arithmetic computes; the slide does not supply a calibrated RGB-to-CIE-XYZ transform, so these ratios are not asserted to be CIE $x,y,z$.

The same slide applies RGB-to-HSV conversion **after** normalization. Consequently, its reported value $V=0.5625$ corresponds to the normalized triplet; the maximum component of the original triplet is 0.9. The hue example is approximately $265.7143^\circ$ and the saturation is approximately 0.7778. Keep track of which triplet is passed to a conversion and whether a software interface expresses hue in degrees or as a normalized value.

## 6.7 Point processing and thresholding

A **point operation** changes each pixel using only that pixel's value. The lecture calls a one-input operation **monadic**:

$$
Y[v,u]=f\!\left(X[v,u]\right).
$$

The output retains the input's spatial size. Adding or subtracting a constant changes brightness, while a threshold converts an intensity decision into a binary image [[2]](#vision-ref-2), slides 40–43.

For 8-bit data, a safe arithmetic interpretation is

$$
Y[v,u,c]=\operatorname{clip}\bigl(X[v,u,c]+b,0,255\bigr).
$$

Convert to a signed or floating type before performing this calculation; clipping is part of the implementation specified here. With $b=30$, channel values $(240,100,20)$ become $(255,130,50)$.

```{figure} ../assets/visual-perception-slides/pixel-brightness-operations.png
:label: fig-vision-slide-pixel-brightness-operations
:alt: Point-wise changes in appearance; original illustration from the supplied Visual Perception lectures
:width: 100%

**Point-wise changes in appearance.** The embedded source image compares the original with darkening, lightening, and inversion. The lecture displays the darkening and lightening panels; the full extracted illustration also retains its labeled inversion panel. Source: Part II, slide 42 [[2]](#vision-ref-2).
```

The lecture's threshold example becomes

$$
B[v,u]=\begin{cases}1,&X[v,u]\geq180,\\0,&X[v,u]<180.\end{cases}
$$

For $X=[100,179,180,220]$, the output is $[0,0,1,1]$. The threshold has to use the same value convention as the image. On a normalized image, the equivalent threshold is $180/255$, not 180.

```{figure} ../assets/visual-perception-slides/threshold-and-intensity-transforms.png
:label: fig-vision-slide-threshold-and-intensity-transforms
:alt: Thresholding and intensity transformations; original illustration from the supplied Visual Perception lectures
:width: 100%

**Thresholding and intensity transformations.** The upper-right panel shows the binary thresholded image. Compare it with the original at upper left; the other panels and their transfer curves show additional intensity transformations included in the source illustration. Source: Part II, slide 43 [[2]](#vision-ref-2).
```

## 6.8 Neighborhood operations: mean and Gaussian filters

### 6.8.1 A kernel combines several input pixels

Unlike a point operation, a neighborhood operation uses a window around the output location. The lecture uses **mask**, **kernel**, and **filter** to describe this local weighting operation [[2]](#vision-ref-2), slides 44–48. A discrete convolution convention is

$$
Y[v,u]=\sum_{j=-h}^{h}\sum_{i=-h}^{h}K[j,i]X[v-j,u-i].
$$

Here the kernel has size $(2h+1)\times(2h+1)$. The indices and boundary handling are implementation choices that must be declared. With a symmetric mean or Gaussian kernel, the flipped-kernel distinction does not change the result, but it matters for a general asymmetric kernel.

```{figure} ../assets/visual-perception-slides/convolution-neighborhood.png
:label: fig-vision-slide-convolution-neighborhood
:alt: A neighborhood contributes to one output pixel; original illustration from the supplied Visual Perception lectures
:width: 100%

**A neighborhood contributes to one output pixel.** The highlighted input window contributes to the highlighted output location. This is the original lecture illustration of the mask, kernel, or filter operation. Source: Part II, slide 44 [[2]](#vision-ref-2).
```

### 6.8.2 Reproduce the lecture's mean-filter arithmetic

A 3 × 3 mean kernel gives all nine entries weight $1/9$. The first highlighted neighborhood on slide 49 is

$$
X_1=\begin{bmatrix}20&40&10\\10&20&30\\20&10&20\end{bmatrix},
\qquad \overline X_1=\frac{180}{9}=20.
$$

The highlighted neighborhood in the **right-hand matrix** is

$$
X_2=\begin{bmatrix}50&10&37\\20&30&72\\10&20&11\end{bmatrix},
\qquad \overline X_2=\frac{260}{9}\approx28.9.
$$

The printed `Mean(...)` list beneath that right-hand matrix contains different numbers. The calculation above explicitly follows the displayed matrix and reproduces its 28.9 output; it does not silently treat the inconsistent list as equivalent [[2]](#vision-ref-2), slide 49.

A normalized mean filter preserves a constant interior region. At an edge between regions, it combines values from both sides. The lecture's 21 × 21 averaging example makes the resulting loss of detail visible [[2]](#vision-ref-2), slide 50.

```{figure} ../assets/visual-perception-slides/mean-filter-comparison.png
:label: fig-vision-slide-mean-filter-comparison
:alt: The visual effect of averaging; original illustration from the supplied Visual Perception lectures
:width: 100%

**The visual effect of averaging.** The original and smoothed portraits illustrate the loss of fine detail. The lecture identifies the example as smoothing with a 21 by 21 averaging kernel. Source: Part II, slide 50 [[2]](#vision-ref-2).
```

### 6.8.3 Gaussian weighting

A Gaussian kernel assigns larger weights near its center. The two-dimensional expression on the lecture slide is

$$
G_\sigma(x,y)=\frac{1}{2\pi\sigma^2}
\exp\!\left[-\frac{x^2+y^2}{2\sigma^2}\right].
$$

```{figure} ../assets/visual-perception-slides/gaussian-kernel-views.png
:label: fig-vision-slide-gaussian-kernel-views
:alt: Three views of a Gaussian kernel; original illustration from the supplied Visual Perception lectures
:width: 100%

**Three views of a Gaussian kernel.** The source image shows the one-dimensional profile, the two-dimensional weighting surface, and an intensity view of the kernel. These are complementary views of the weighting discussed in this section. Source: Part II, slide 51 [[2]](#vision-ref-2).
```

For image filtering, $x,y$, and $\sigma$ are measured in pixel units. A finite discrete kernel should be normalized after sampling:

$$
K[j,i]=\frac{\exp[-(i^2+j^2)/(2\sigma^2)]}
{\sum_{a=-h}^{h}\sum_{b=-h}^{h}\exp[-(a^2+b^2)/(2\sigma^2)]}.
$$

Thus $\sum K=1$. For $h=1$ and $\sigma=1$, the center coefficient is approximately 0.2042; its four side neighbors are approximately 0.1238 each and the four corners approximately 0.0751 each. These are computed examples of the normalized kernel, not measured biological responses.

The lecture shows increased blurring with broader Gaussian smoothing and emphasizes that applying the same kernel everywhere also blurs across edges [[2]](#vision-ref-2), slides 51–57. **Parameter distinction:** increasing $\sigma$ broadens the weighting; enlarging an already sufficient window at fixed $\sigma$ mainly changes truncation. Kernel width and $\sigma$ should therefore be reported separately rather than treated as identical controls.

```{figure} ../assets/visual-perception-slides/gaussian-blur-progression.png
:label: fig-vision-slide-gaussian-blur-progression
:alt: Increasing the Gaussian scale; original illustration from the supplied Visual Perception lectures
:width: 100%

**Increasing the Gaussian scale.** The lecture pairs broader weighting curves with progressively smoother images, labeled with sigma values of 4, 8, 16, and 32. Observe the loss of edge detail rather than treating smoothing as uniformly beneficial. Source: Part II, slide 57 [[2]](#vision-ref-2).
```

### 6.8.4 A minimal executable implementation

The following NumPy example implements the lecture's averaging and Gaussian ideas. `edge` padding and the chosen kernel size are explicit textbook implementation choices.

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def gaussian_kernel(size=5, sigma=1.0):
    if not isinstance(size, int) or size < 1 or size % 2 == 0:
        raise ValueError("size must be a positive odd integer")
    if not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("sigma must be finite and positive")
    axis = np.arange(size, dtype=float) - size // 2
    yy, xx = np.meshgrid(axis, axis, indexing="ij")
    kernel = np.exp(-(xx * xx + yy * yy) / (2 * sigma * sigma))
    return kernel / kernel.sum()


def convolve_gray(image, kernel):
    image = np.asarray(image, dtype=float)
    kernel = np.asarray(kernel, dtype=float)
    if image.ndim != 2 or image.size == 0:
        raise ValueError("expected a nonempty grayscale image")
    if kernel.ndim != 2 or any(n < 1 or n % 2 == 0 for n in kernel.shape):
        raise ValueError("kernel dimensions must be positive and odd")
    if not np.isfinite(image).all() or not np.isfinite(kernel).all():
        raise ValueError("image and kernel must contain finite values")
    pad = tuple((n // 2, n // 2) for n in kernel.shape)
    windows = sliding_window_view(np.pad(image, pad, mode="edge"), kernel.shape)
    return np.einsum("ijab,ab->ij", windows, kernel[::-1, ::-1])


patch = np.array([[20, 40, 10], [10, 20, 30], [20, 10, 20]])
assert np.isclose(convolve_gray(patch, np.ones((3, 3)) / 9)[1, 1], 20)
kernel = gaussian_kernel(3, 1.0)
assert np.isclose(kernel.sum(), 1.0)
assert np.allclose(convolve_gray(np.ones((5, 5)), kernel), 1.0)
```

## 6.9 Dyadic operations and chroma keying

A **dyadic operation** combines two input images of the same spatial size:

$$
Z[v,u]=f\!\left(X[v,u],Y[v,u]\right).
$$

```{figure} ../assets/visual-perception-slides/dyadic-image-operation.png
:label: fig-vision-slide-dyadic-image-operation
:alt: Combining two corresponding pixels; original illustration from the supplied Visual Perception lectures
:width: 100%

**Combining two corresponding pixels.** Two input images contribute to one output image. The highlighted rows and columns identify the corresponding pixel locations used in the dyadic operation. Source: Part II, slide 58 [[2]](#vision-ref-2).
```

The lectures list addition, subtraction, element-wise multiplication, minimum, and maximum. Chroma keying provides a concrete example: use pixel values to distinguish a subject from a blue or green background and combine that subject with another image [[2]](#vision-ref-2), slides 58–59.

If $M[v,u]=1$ denotes the retained foreground, the compositing calculation is

$$
Z[v,u,c]=M[v,u]F[v,u,c]+(1-M[v,u])B[v,u,c].
$$

$F$ and $B$ are the foreground and replacement-background images. The formula makes the lecture's selection operation explicit. A reliable result requires a useful mask; compositing does not repair errors in the color-based classification used to create that mask. A robot's colored-cue detector faces the same separation between measuring a feature and deciding what it means.

```{figure} ../assets/visual-perception-slides/chroma-keying-example.png
:label: fig-vision-slide-chroma-keying-example
:alt: From a green-screen image to a composite; original illustration from the supplied Visual Perception lectures
:width: 100%

**From a green-screen image to a composite.** The four original panels show the subject, a channel histogram, a mask, and the composite. Connect the white foreground region of the mask to the selection equation above. Source: Part II, slide 59 [[2]](#vision-ref-2).
```

(vision-pipeline)=
## 6.10 From visual pixels to a neural cue

### 6.10.1 The boundary between the lectures and this experiment

The preceding sections follow the supplied imaging and image-processing lectures. The lectures do not specify a calibrated RGB-to-spike equation, neural current gain, or validated robot detection accuracy. The following **existing textbook experiment** supplies one transparent encoding choice and connects it to [Chapter 2](03-computational-neuron-models.md), [Chapter 3](04-hebbian-learning.md), and [Laboratory 6](../notebooks/sensory_encoding.ipynb).

The processing sequence is **RGB image → selected region → preprocessing → red feature → input current → LIF response**. It is useful precisely because every step can be inspected. It is not a model of retinal phototransduction, a learned visual classifier, or a complete navigation system.

### 6.10.2 A measurable red-contrast feature

Let normalized channels $R_p,G_p,B_p\in[0,1]$ describe pixel $p$ in a region of interest (ROI) containing $N$ pixels. Define

$$
z_R=\frac{1}{N}\sum_{p=1}^{N}
\operatorname{clip}\!\left(R_p-\frac{G_p+B_p}{2},0,1\right),
\qquad I_{\mathrm{in}}=50+250z_R\ \mathrm{pA}.
$$

Pure red produces $z_R=1$ and 300 pA. Ideal white and blue produce $z_R=0$ and 50 pA. Dim red $(0.4,0,0)$ produces 0.4 and 150 pA. A pure-red patch filling one quarter of the ROI on a zero-red-contrast background produces 0.25 and 112.5 pA. Thus the pooled feature combines color contrast and spatial coverage; it does not preserve cue position.

```python
def red_feature(rgb):
    rgb = np.asarray(rgb, dtype=float)
    if rgb.ndim < 1 or rgb.shape[-1] != 3 or rgb.size == 0:
        raise ValueError("expected a nonempty RGB array")
    if not np.isfinite(rgb).all() or np.any((rgb < 0) | (rgb > 1)):
        raise ValueError("expected finite RGB values in [0, 1]")
    contrast = rgb[..., 0] - 0.5 * (rgb[..., 1] + rgb[..., 2])
    return float(np.clip(contrast, 0, 1).mean())

# Import NumPy as np; divide uint8 camera samples by 255 before calling.
z = red_feature(np.array([[[0.8, 0.2, 0.2]]]))
assert np.isclose(z, 0.6)
assert np.isclose(50 + 250 * z, 200.0)
```

### 6.10.3 A larger feature does not automatically mean a spike

Laboratory 6 applies each current for 500 ms to the Chapter 2 LIF neuron. Under that experiment's parameters, 50 pA is below rheobase; 150 pA reaches the passive threshold only asymptotically and does not cross it in finite time in the ideal constant-current model. Full red supplies a larger current and produces repeated events. These are results of a declared encoder and neuron model, **not camera detection accuracies**.

```{figure} ../assets/sensor-course-vision.png
:label: fig-sensor-vision
:alt: Existing synthetic red, white, blue, and dim-red patch experiment and the resulting LIF spike counts under a declared current mapping
:width: 100%

**A textbook application of visual cue encoding.** The synthetic patches drive the stated red-feature-to-current map and LIF model. This figure belongs to the executable textbook laboratory; it is not an experimental figure from the supplied lecture slides.
```

### 6.10.4 Test perception before testing associative learning

Record the original frame, ROI, feature value, input current, spike times, and downstream decision. Change illumination, cue size, cue location, noise, and red distractors independently. Hold preprocessing and thresholds fixed on the test set. A missed cue is different from a failed association, and an appropriate neural response is different from a successful motor action.

Processing order matters. Smoothing before nonlinear red clipping need not equal smoothing after clipping. Even without spatial filtering, clipping each pixel before averaging differs from clipping the mean contrast: for contrasts $(-0.4,0.8)$, the two outputs are 0.4 and 0.2. The implemented definition uses **clip first, average second**.

Finally, red contrast is not an allocentric position code. Connecting it to [Chapter 4's spatial representations](02-spatial-cells.md) requires a specified geometry, pose estimate, or learned mapping. For the association experiment, retain the measured graded cue or convert it into an event using a declared threshold; do not substitute a simulator's hidden object label for the image-derived measurement.

## 6.11 Additional Reading Materials

Review Part I slides 3–26 for the perception context, 28–51 for light and image formation, 54–70 for digital sensors, and 76 for measurement units [[1]](#vision-ref-1). Review Part II slides 5–24 for color perception and matching, 25–43 for digital images and point operations, 44–59 for filtering and dyadic operations, and 64–66 for chromaticity and the MATLAB example [[2]](#vision-ref-2).

The course decks are the basis of this revision. *Robotics, Vision and Control* remains the book's supplementary camera and image-processing reference [[3]](#vision-ref-3); its presence here does not mean every slide caption was independently verified against that book. Continue to [Chapter 7](07-inertial-sensing.md) for the second sensor input used in the association experiment.

(66-exercises)=
## 6.12 Exercises

1. Calculate $z_R$ for $(0.8,0.2,0.2)$ and the resulting input current.
2. Explain how shrinking a red cue inside a fixed ROI changes the response.
3. Design a held-out lighting test without retraining the detector on the test images.
4. Compare clipping before averaging with clipping the mean contrast.
5. For a mobile robot, identify the sensor, perception output, planning decision, and actuator. Explain why an RGB frame is not already an action.
6. Contrast radiant flux with luminous flux, and irradiance with illuminance. Explain why an 8-bit pixel is not automatically a lux measurement.
7. With $f=8$ mm, $X=150$ mm, and $Z=600$ mm, compute the virtual-plane image coordinate. What changes when depth doubles? What changes for a physical image plane behind the pinhole?
8. Count the red, green, and blue sites in the representative Bayer block. Compute the number of photosites in the lecture's 4912 × 3684 array.
9. Write the three-primary matching system and explain a negative red coefficient without invoking negative emitted power.
10. Normalize $(0.5,0.2,0.9)$ by its component sum. Explain the difference between the maximum original component and the maximum normalized component, and why black requires a special case.
11. Apply the threshold 180 to $[100,179,180,220]$. Give the equivalent threshold for values divided by 255.
12. Recalculate both highlighted 3 × 3 neighborhoods in Section 6.8.2. Identify the inconsistency in the slide's second printed list.
13. Construct the normalized 3 × 3 Gaussian kernel with $\sigma=1$. Verify its sum and explain why a constant image should remain constant with the specified padding.
14. Explain the difference between a point operation and a neighborhood filter. Predict a failure of excessive smoothing for a small colored landmark.
15. Use the mask equation to composite one foreground pixel and one background pixel. Explain what happens when the foreground mask is wrong.
16. Design a logged experiment that distinguishes a camera/perception failure, a feature-to-spike encoding failure, and an associative-learning failure.

[Worked solutions](solutions-embodied.md#vision-solutions) are provided at the end of the book.

## References

(vision-ref-1)=

[1] Hongyu An, *Neuromorphic Robotic Systems—Visual Perception, Part I*, course lecture slides, Department of Electrical and Computer Engineering, Michigan Technological University, supplied teaching file “Neuromorphic Robotic Systems-Topic 4-1 Visual Perception.pptx,” 79 slides. Publication date not specified in the supplied file; slide numbers in this chapter refer to slide order, not occasionally offset printed page labels.

(vision-ref-2)=

[2] Hongyu An, *Neuromorphic Robotic Systems—Visual Perception, Part II*, course lecture slides, Department of Electrical and Computer Engineering, Michigan Technological University, supplied teaching file “Neuromorphic Robotic Systems-Topic 4-2 Visual Perception.pptx,” 66 slides. The title slide labels this material “Topic 5: Visual Perception”; Part II here identifies the supplied file without changing its internal title.

(vision-ref-3)=

[3] Peter Corke, *Robotics, Vision and Control: Fundamental Algorithms in Python*, 3rd ed. Cham, Switzerland: Springer, 2023, doi: 10.1007/978-3-031-06469-2. [Publisher](https://link.springer.com/book/10.1007/978-3-031-06469-2).
