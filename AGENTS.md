# Textbook maintenance

This repository belongs to the SFN research project.

- Preserve the title **Introduction to Neuromorphic Embodied AI**, author, scientific content, and distinction between established evidence, teaching assumptions, and proposed research.
- Keep the directory structure, including `.github/workflows/deploy.yml`.
- Use a feature branch and pull request for future updates unless the owner explicitly requests a direct commit.
- Add new chapters to `myst.yml`; keep unfinished chapters labeled as planned.
- Validate with `python tests/execute_notebook.py`, `BASE_URL=/Introduction-to-Neuromorphic-Embodied-AI jupyter book build --html --strict`, and `python tests/check_build.py`.
- Pull requests build and test the book. Merging to `main` automatically deploys GitHub Pages.
- Do not change other repositories.

- References throughout chapters, notebooks, interactive pages, and generators use one paragraph per numbered entry, full given names and surnames (retain published middle initials), and full journal titles. Keep IEEE-style bibliographic ordering and linked DOI/source records.
- Foundation order: Chapter 1 Neuroscience Background; Chapter 2 Computational Models of Neurons; Chapter 3 Spatial Cells; Chapter 4 Hebbian Learning. Source filenames are stable for existing links.
