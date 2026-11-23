# Preface

### Toward Robots That Learn from Experience

Over the past three years, I have taught the course *Neuromorphic Robotic Systems* at Michigan Technological University. This book grew out of those years of teaching, the development of computational laboratories, and my ongoing research into brain-inspired robotic intelligence.

However, this book is more than a collection of lecture notes. It also represents my personal vision for the future of artificial intelligence: **machines that can continuously learn, remember, and adapt through their own interactions with the physical world.**

## Why Do We Need Another Approach to Artificial Intelligence?

Artificial intelligence has advanced remarkably in recent years. Large language models, deep learning systems trained on extensive datasets, and reinforcement learning have demonstrated capabilities that once seemed far beyond the reach of machines.

These achievements are important, and I believe they will continue to shape the future of AI and robotics. Nevertheless, when we move AI from data centers into the physical world, we encounter challenges that cannot always be solved by larger models or more training data.

**The first challenge is the reliability of communication and cloud connectivity.**

Many AI applications benefit from cloud infrastructure, where powerful processors and large models can be accessed remotely. But what happens when a robot must operate somewhere with limited or unreliable communication?

Consider a robot exploring the Moon, an underwater vehicle investigating the deep ocean, or an autonomous system operating in a remote environment. Communication may be delayed, intermittent, severely bandwidth-limited, or completely unavailable for extended periods.

In these circumstances, a robot cannot depend on continuous access to a remote AI service. It must be able to perceive its surroundings, make decisions, and respond to unexpected events locally.

**The second challenge is the availability and quality of training data.**

Modern machine learning has benefited enormously from large datasets, including labeled data, self-supervised pretraining, and experience collected through reinforcement learning. However, collecting representative data can be difficult in unfamiliar or extreme environments.

For example, a robotic system deployed on another planet may encounter terrain or environmental conditions that differ substantially from those in its training data. An underwater robot may discover objects, biological organisms, or environmental situations that were not adequately represented during development.

Transfer learning and other adaptation methods can help, but their effectiveness is not guaranteed when the available data are limited or the environment changes significantly.

Ideally, we would like robots to continue improving their internal representations and behavior **after deployment**, using the experiences they acquire in the environment.

**The third challenge concerns privacy, energy, and long-term autonomy.**

Transmitting large amounts of sensory data to remote servers may be undesirable for privacy-sensitive applications. Continuous communication and intensive computation can also introduce energy and latency constraints.

These challenges motivate an important question:

*Can we build intelligent machines that learn from relatively limited experience, operate with modest computational resources, and remain functional without depending on continuous cloud connectivity?*

## What Can We Learn from the Brain?

One possible source of inspiration is biological intelligence.

Consider a rat exploring an unfamiliar maze.

The rat does not begin with a labeled dataset describing every possible location, obstacle, and reward. Instead, it moves through the environment, receives sensory information, forms spatial representations, and gradually learns relationships between locations, actions, and outcomes.

Despite the limited size and energy consumption of its nervous system, it can navigate, remember experiences, and adapt its behavior when environmental conditions change.

How does this happen?

Neuroscience has identified several types of neurons associated with spatial cognition and navigation. Place cells exhibit location-related activity. Grid cells show periodic spatial firing patterns. Head-direction cells encode heading-related information, while border-related cells respond to environmental boundaries. Synaptic plasticity and associative learning provide possible mechanisms through which experience can influence future behavior.

These discoveries do not mean that we fully understand how a rat learns, nor that simply reproducing neural firing patterns will create an intelligent robot. But they provide valuable experimental observations and computational hypotheses.

I believe that studying these biological mechanisms may help us develop a different approach to embodied artificial intelligence: one in which robots do not merely execute a model trained elsewhere, but can gradually acquire useful knowledge through interaction with their environment.

This is the central motivation behind my research in **Neuromorphic Embodied AI**.

My long-term goal is to investigate how spatial representation, associative learning, memory, and event-driven neural computation can be integrated into autonomous robotic systems capable of continuous adaptation.

Such systems are not intended to replace conventional deep learning, large language models, or reinforcement learning. Rather, I see brain-inspired learning as a complementary direction, particularly valuable when data, communication, and computational resources are constrained.

## Who Is This Book For?

This book is intended primarily for undergraduate and graduate students, researchers, and engineers interested in the intersection of neuroscience, neuromorphic AI, physical AI, and autonomous robotics.

It is particularly relevant to readers in electrical and computer engineering, robotics, computer science, biomedical engineering, and computational neuroscience.

Readers approaching the subject from engineering may be familiar with algorithms, programming, and electronic systems but have limited knowledge of biological neurons and neural circuits.

Readers from neuroscience may understand neural activity and animal behavior but have less experience translating those observations into computational models and robotic systems.

My intention is to help bridge these perspectives.

The book introduces relevant biological principles, develops simplified mathematical models, and then connects them to executable simulations and robotic applications. Familiarity with introductory Python, linear algebra, and elementary probability will be helpful, but advanced computational neuroscience experience is not required.

## How This Book Was Written and How to Use It

This book is based on three years of teaching *Neuromorphic Robotic Systems*, together with the computational examples, experimental designs, and research questions that have emerged from my laboratory.

It follows a progression from **biological observations to mathematical models, computational experiments, and robotic systems**.

The opening chapters introduce neurons, synapses, computational neuron models, synaptic plasticity, and spatial neural representations. Later chapters connect these foundations to visual perception, inertial sensing, LiDAR, neuromorphic simulation tools, and associative learning in robotics.

An important feature of this book is its emphasis on learning through computation.

Readers are encouraged not only to study equations but also to execute the accompanying Python notebooks, change model parameters, inspect neuronal responses, and question the results.

For example, changing the width of a place-cell firing field should lead to a predictable change in spatial activity. Changing the time constant of a spike-timing-dependent plasticity rule should alter its temporal learning window. Such experiments help connect mathematical expressions to observable computational behavior.

I recommend that readers begin with the foundational chapters and complete the corresponding laboratories before moving to the robotic applications. Readers with a neuroscience background may give particular attention to the computational neuron and robotics chapters, while engineering students may benefit from spending additional time on the biological foundations.

Because this is an online, evolving textbook, the material can be revised as new scientific evidence, computational tools, and teaching experiences become available. The goal is not simply to present working programs, but to teach readers to distinguish biological evidence, modeling assumptions, numerical results, and hypotheses that still require experimental validation.

## A Vision for the Future

I do not believe that the future of intelligent robotics will be defined solely by the size of a neural network or the amount of data used during training.

I believe that an equally important measure of intelligence will be **what a machine can learn after it encounters a world it has never seen before**.

Can it recognize unfamiliar surroundings? Can it remember useful experiences? Can it learn from rewards and mistakes? Can it adapt its behavior without constantly returning to a remote data center for new instructions or retraining?

These are open research questions. The computational models in this book represent introductory steps toward studying them, not completed solutions.

My hope is that the book will encourage students and researchers to explore these questions, challenge existing assumptions, and develop new forms of intelligent machines inspired by the remarkable learning capabilities of biological systems.

Ultimately, I envision a future in which robotic intelligence is not merely downloaded into a machine before deployment, but continues to develop through its experiences in the world.

---

## Acknowledgments

I would also like to thank Tinotenda Taderera for his initial review and constructive feedback on selected chapters and computational laboratories, and I look forward to his continued contributions as this textbook develops.

I also thank my students, research collaborators, and colleagues whose discussions and scientific work continue to inform my teaching and research.
