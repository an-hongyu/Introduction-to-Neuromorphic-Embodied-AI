# Introduction to Neuromorphic Embodied AI

An open, computational textbook on biological spatial cells, spiking models, associative learning and embodied robotics.

**Author:** Hongyu An

## Current textbook structure

1. Neuroscience Background: neurons, spikes, membrane potential, and synapses; informed by *Principles of Neural Science*, fifth edition.
2. Spatial Cells: place, grid, head-direction, border/boundary, speed, and time-related activity.
3. Computational Models of Neurons: rate/count models, LIF, Hodgkin–Huxley-type models, adaptive exponential models, and model selection.
4. Hebbian Learning: association, constraints, Oja's rule, STDP, and eligibility traces.

5. Neural Encoding and the ANN–SNN Bridge.
6. Visual Perception and Visual Cue Encoding.
7. Inertial Sensing and Vibration Encoding.
8. LiDAR and Thirty-Six-Channel Spatial Encoding.
9. Nengo, ROS 2, and Gazebo Integration (single-cell notebook plus integration guide).
10. Capstone: An Associative Learning Robot (synthetic learning experiment plus robot validation protocol).

References use IEEE-style numbered citations and hyperlinks. Original figures, defined units, worked examples, and exercises accompany the chapters. Existing introductory and Place Cell material remains available under supplementary reading and computational laboratories.

The computational laboratories begin with a **Computational Models of Neurons** guide and follow this sequence: Laboratory 1, LIF neuron (`lif_neuron.ipynb`); Laboratory 2, Place Cells (`place_cells.ipynb`); Laboratory 3, Hebbian learning (`hebbian_learning.ipynb`); Laboratory 4, Hodgkin–Huxley; Laboratory 5, Conditioning; Laboratory 6, Sensory Encoding; Laboratory 7, One Neuron in Nengo; Laboratory 8, Grid Cells to Place-Like Fields. See `chapters/course-reading-map.md`.

## Run the notebook

```bash
python -m pip install -r requirements.txt
jupyter lab notebooks/lif_neuron.ipynb
```

## Preview the book locally

Install Python 3.12 and Node.js 24 LTS, then run:

```bash
python -m pip install -r requirements.txt
jupyter book start
```

## Published textbook

- Website: https://an-hongyu.github.io/Introduction-to-Neuromorphic-Embodied-AI/
- Repository: https://github.com/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI
- The left sidebar follows the curriculum; each page has a section table of contents.
- Equations, Python code, executed notebook figures, and notebook download links are included.
- Run the Place Cell notebook locally or via the Google Colab link in the chapter.

## Validation and deployment

```bash
python tests/execute_notebook.py
BASE_URL=/Introduction-to-Neuromorphic-Embodied-AI jupyter book build --html --strict
python tests/check_build.py
```

The `.github/workflows/deploy.yml` workflow executes all eight notebooks, builds Jupyter Book,
checks generated pages and local links, and deploys to GitHub Pages on `main`.
Repository Settings → Pages must use **GitHub Actions** as the source.
Pull requests run the build and checks without deploying.

## Future updates with ChatGPT

Ask ChatGPT to work in this repository, create a branch, update the requested material,
and open a pull request. Review the diff and green Actions checks, then merge to publish.
The GitHub connection must include this repository with contents, pull-request, and
workflow permissions appropriate to the requested changes; update the connection's
selected repositories if it cannot write to a newly created repository.
See `AGENTS.md` for scientific preservation and validation requirements.

## Scientific scope

Synthetic demonstrations illustrate mathematical assumptions; they do not establish biological validity or autonomous robot performance. Later SFN chapters are planned and should be labeled as proposals until evaluated.

## License

Text: Creative Commons Attribution 4.0 International (CC BY 4.0). Code: MIT. See `LICENSE-TEXT.md` and `LICENSE-CODE.md`.

## Reproduce original teaching assets

```bash
python tools/build_teaching_assets.py
```

This regenerates the original neuron/synapse schematic, synthetic spatial tuning figure, LIF figure, Hebbian-learning figure, and the two new laboratory source notebooks. It does not copy images or pages from the neuroscience reference textbook. The reference PDF is not distributed with this repository.

## Course-aligned experiments

Run `python tools/build_course_assets.py` to regenerate the four course notebooks and eight original figures. The generator checks HH rest/gates/ablation/time-step refinement, association controls, sensory masks, and the Nengo analytical firing rate. It supplements existing generators. Python 3.12 with Nengo 4.0.0 and NumPy 1.26.4 is the tested publishing environment.

The ROS 2 Jazzy / Gazebo Harmonic integration chapter is a guide. A complete Gazebo world, controller package, physical robot, or neuromorphic hardware experiment is not supplied or validated by these notebooks.

## Interactive grid-to-place laboratory

`chapters/grid-to-place.md` specifies Liu et al.'s source conventions, lattice spacing/frequency conversion, cosine fields, and a fixed normalized weighted readout. `assets/grid-place-interactive.html` runs the experiment without external dependencies. Laboratory 8 reproduces it in Python. Generate its notebook/reference fixtures with `python tools/build_grid_place_examples.py`; `node tests/test_grid_place_interactive.cjs` compares the embedded JavaScript to NumPy and checks grid geometry and alias controls. This teaching readout does not claim learned place-field formation.
