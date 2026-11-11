# Introduction to Neuromorphic Embodied AI

An open, computational textbook on biological spatial cells, spiking models, associative learning and embodied robotics.

**Author:** Hongyu An · Michigan Technological University

## Current textbook structure

1. Neuroscience Background: neurons, spikes, membrane potential, and synapses; informed by *Principles of Neural Science*, fifth edition.
2. Spatial Cells: place, grid, head-direction, border/boundary, speed, and time-related activity.
3. Computational Models of Neurons: rate/count models, LIF, Hodgkin–Huxley-type models, adaptive exponential models, and model selection.
4. Hebbian Learning: association, constraints, Oja's rule, STDP, and eligibility traces.

References use IEEE-style numbered citations and hyperlinks. Original figures, defined units, worked examples, and exercises accompany the chapters. Existing introductory and Place Cell material remains available under supplementary reading and computational laboratories.

Three executable notebooks are included: `place_cells.ipynb`, `lif_neuron.ipynb`, and `hebbian_learning.ipynb`.

## Run the notebook

```bash
python -m pip install -r requirements.txt
jupyter lab notebooks/place_cells.ipynb
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

The `.github/workflows/deploy.yml` workflow executes all three notebooks, builds Jupyter Book,
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
