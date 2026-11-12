---
title: Curriculum and Development Roadmap
---

# Curriculum and Development Roadmap

Ten numbered chapters, a detailed grid-to-place section, and eight computational laboratories are available. The [course-to-book map](course-reading-map.md) identifies the corresponding lecture topics. Available text and executed synthetic models are distinguished from simulator and hardware validation.

## Part I — Foundations: available

1. [Neuroscience Background](01-neuroscience-background.md)
2. [Spatial Cells](02-spatial-cells.md)
3. [Computational Models of Neurons](03-computational-neuron-models.md): LIF, HH, reduced models, and model selection
4. [Hebbian Learning](04-hebbian-learning.md): association, Oja, STDP, and eligibility traces

## Part II — Encoding and embodied learning: available

5. [Neural Encoding and the ANN–SNN Bridge](05-neural-encoding.md)
6. [Visual Perception and Cue Encoding](06-visual-perception.md)
7. [Inertial Sensing and Vibration Encoding](07-inertial-sensing.md)
8. [LiDAR and Thirty-Six-Channel Spatial Encoding](08-lidar-encoding.md)
9. [Nengo, ROS 2, and Gazebo Integration](09-nengo-ros-gazebo.md)
10. [Capstone: An Associative Learning Robot](10-associative-learning-robot.md)

The HH, conditioning, sensory, and single-neuron Nengo examples execute in Python. The ROS 2/Gazebo material is a staged integration guide, not a supplied and validated robot deployment. No neuromorphic hardware result is claimed by these teaching examples.

## Computational laboratories: available

See the [laboratory table](course-reading-map.md) for the complete sequence. The [neuron-model laboratory guide](computational-neuron-models-lab.md), [Place Cell guide](04-place-cells.md), and [closed-loop overview](01-introduction.md) remain available. All eight notebooks execute during the publishing workflow.

## Advanced spatial representations and networks: planned

- Learned place-cell models, remapping, and grid-to-place connectivity (the [fixed readout and interactive grid example](grid-to-place.md) are now available)
- Grid, head-direction, border/boundary, speed, and time-cell implementations
- Path integration and multimodal spatial representations
- Learning spatial representations and population decoding
- Associative memory capacity, interference, and consolidation
- Spike Flow Networks: explicit models and testable hypotheses
- Reward-guided navigation, goal relocation, and planning

## Embodied validation and hardware: planned

- A complete reproducible ROS 2/Gazebo robot package and recorded controlled trials
- Spatial-cell networks driven by robot measurements
- Neuromorphic hardware implementation and measured energy
- Calibration with rodent electrophysiology
- Benchmarks, ablations, failure cases, and open problems

## Writing and evidence conventions

Use IEEE-style numbered references in order of first citation within each chapter. Put each reference in a separate paragraph; write full author names and full journal titles, retaining middle initials as published. Citation numbers link to reference entries, and entries link to DOI records, publisher pages, or authoritative online texts. Define variables and units at their first use and distinguish biological observations from chosen model assumptions.

The neuroscience foundation uses *Principles of Neural Science*, fifth edition, as a reference. Original teaching figures and examples are created for this book. A chapter should distinguish prior experimental evidence, established modeling precedents, pedagogical assumptions, and proposed research. Planned material is not evidence of a completed model or validated robot.


(reference-book-reading-map)=
## Reference-book reading map

The following editions were supplied as course references. The reading selections connect biological explanation, mathematical abstraction, and reproducible experiments; each book has a different emphasis. The current online edition of a living textbook may differ from the supplied snapshot.

| Reference | Selected reading | Role in this textbook |
|---|---|---|
| *Principles of Neural Science*, 5th ed. [[1]](#reading-ref-1) | Chs. 2, 4, 6–8, and 10 | Biological foundations: neurons, membrane signaling, and synapses in Chapter 1 |
| *Neuroscience: Exploring the Brain*, 4th ed. [[2]](#reading-ref-2) | Chs. 2–5; Ch. 25 for learning | An accessible route from cellular structure to resting voltage, action potentials, transmission, and plasticity |
| *Computational Neuroscience: A First Course* [[3]](#reading-ref-3) | Ch. 1; Ch. 2; Secs. 4.3–4.4; Ch. 5 | Membrane equations and reduced models; tuning; association and Oja's rule; population representations |
| *Computational Cognitive Neuroscience*, 1st ed. [[4]](#reading-ref-4) | Chs. 2–4; Ch. 8 | The conceptual progression from neuron to network, learning mechanism, and memory |
| *Artificial Intelligence in the Age of Neural Networks and Brain Computing* [[5]](#reading-ref-5) | Ch. 1, “Nature's Learning Rule: The Hebbian-LMS Algorithm”; Ch. 6, “Evolving and Spiking Connectionist Systems for Brain-Inspired Artificial Intelligence” | Supplementary perspectives on learning algorithms, spike representations, and network design |

For beginners, read the cellular foundations first, then work through the neuron-model guide and LIF notebook. Compare the Place Cell notebook's imposed spatial rate with the dynamical LIF model. Only then study weight updates and their evaluation in the Hebbian laboratory. Learning-rule names should not conceal their differences: the Hebbian-LMS algorithm discussed in the edited volume is a specific construction, not a synonym for every Hebbian or STDP rule.

The explanations and teaching assets in this textbook are original. References support the relevant concepts; numerical teaching parameters and robot examples are explicitly chosen assumptions. Experimental spatial-cell findings continue to be linked to their primary research papers.

### Book references

(reading-ref-1)=
[1] Eric R. Kandel, James H. Schwartz, Thomas M. Jessell, Steven A. Siegelbaum, and Albert James Hudspeth, Eds., *Principles of Neural Science*, 5th ed. New York, NY, USA: McGraw-Hill, 2013. [Publisher](https://www.mheducation.com/highered/mhp/product/principles-neural-science-fifth-edition.html).

(reading-ref-2)=
[2] Mark F. Bear, Barry W. Connors, and Michael A. Paradiso, *Neuroscience: Exploring the Brain*, 4th ed. Philadelphia, PA, USA: Wolters Kluwer, 2016. [National Library of Medicine catalog](https://www.ncbi.nlm.nih.gov/nlmcatalog/101647616).

(reading-ref-3)=
[3] Hanspeter A. Mallot, *Computational Neuroscience: A First Course*. Cham, Switzerland: Springer, 2013, doi: 10.1007/978-3-319-00861-5. [Publisher](https://link.springer.com/book/10.1007/978-3-319-00861-5).

(reading-ref-4)=
[4] Randall C. O'Reilly, Yuko Munakata, Michael J. Frank, Thomas E. Hazy, and Contributors, *Computational Cognitive Neuroscience*, 1st ed. Wiki Book, 2012, supplied PDF snapshot generated Aug. 25, 2016. [Institutional publication record](https://experts.colorado.edu/display/pubid_85822); [current online edition](https://book.compcogneuro.org/).

(reading-ref-5)=
[5] Robert Kozma, Cesare Alippi, Yoonsuck Choe, and Francesco Carlo Morabito, Eds., *Artificial Intelligence in the Age of Neural Networks and Brain Computing*. London, U.K.: Academic Press, 2019. [Publisher](https://www.sciencedirect.com/science/book/9780128154809).
