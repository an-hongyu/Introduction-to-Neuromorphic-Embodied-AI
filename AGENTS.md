# Textbook maintenance

This repository belongs to the SFN research project.

- Preserve the title **Introduction to Neuromorphic Embodied AI**, author, scientific content, and distinction between established evidence, teaching assumptions, and proposed research.
- Keep the directory structure, including `.github/workflows/deploy.yml`.
- Use a feature branch and pull request for future updates unless the owner explicitly requests a direct commit.
- Add new chapters to `myst.yml`; keep unfinished chapters labeled as planned.
- Validate with `python tests/execute_notebook.py`, `BASE_URL=/Introduction-to-Neuromorphic-Embodied-AI jupyter book build --html --strict`, and `python tests/check_build.py`.
- Pull requests build and test the book. Merging to `main` automatically deploys GitHub Pages.
- Do not change other repositories.
