# Introduction to Neuromorphic Embodied AI

An open, computational textbook on biological spatial cells, spiking models, associative learning and embodied robotics.

**Author:** Hongyu An · Michigan Technological University

## Contents of this initial release

- Cover, landing page, chapter table of contents
- Chapter 1: What Is Neuromorphic Embodied AI?
- Chapter 4: Place Cell Models
- Executable notebook: `notebooks/place_cells.ipynb`
- GitHub Actions builds and deploys Jupyter Book 2; pull requests run the same build and notebook checks

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

The `.github/workflows/deploy.yml` workflow executes the notebook, builds Jupyter Book,
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
