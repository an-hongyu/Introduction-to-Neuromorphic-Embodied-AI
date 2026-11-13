# Textbook maintenance

This repository belongs to the SFN research project.

- Preserve the title **Introduction to Neuromorphic Embodied AI**, author, scientific content, and distinction between established evidence, teaching assumptions, and proposed research.
- Keep the directory structure, including `.github/workflows/deploy.yml`.
- Use a feature branch and pull request for future updates unless the owner explicitly requests a direct commit.
- Add new chapters to `myst.yml`; keep unfinished chapters labeled as planned.
- Validate with `python tools/fetch_spatial_figures.py`, `python tests/execute_notebook.py`, `BASE_URL=/Introduction-to-Neuromorphic-Embodied-AI jupyter book build --html --strict`, `python tools/publish_spatial_redirects.py`, `python tests/check_build.py`, and `python tests/check_spatial_merge.py`.
- Pull requests build and test the book. Merging to `main` automatically deploys GitHub Pages.
- Do not change other repositories.

- References throughout chapters, notebooks, interactive pages, and generators use one paragraph per numbered entry, full given names and surnames (retain published middle initials), and full journal titles. Keep IEEE-style bibliographic ordering and linked DOI/source records.
- Foundation order: Chapter 1 Neurons and Synapses; Chapter 2 Computational Models of Neurons; Chapter 3 Hebbian Learning and Synaptic Plasticity; Chapter 4 Spatial Cells and Their Models. Source filenames are stable for existing links.
- Keep each spatial cell's model next to its biological explanation in Chapter 4. The former separate Spatial Cell Models navigation group is intentionally removed. Preserve the grid-to-place legacy route and its fragment redirects, but do not restore a duplicate model chapter. Executable laboratories remain separately accessible.

- The former Neural Encoding/ANN-SNN bridge chapter was removed at the author's request. The retained sensor and robotics chapters are numbered 5-9 (Visual Perception, Inertial Sensing, LiDAR, Nengo/ROS/Gazebo, Capstone). Keep their existing source filenames and published URLs; keep the eight computational laboratories.
