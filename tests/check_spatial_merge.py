"""Regression checks for the single integrated spatial-cell/model chapter."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_build" / "html"
chapter = SITE / "chapters" / "spatial-cells" / "index.html"
html = chapter.read_text(encoding="utf-8")
source = (ROOT / "chapters" / "02-spatial-cells.md").read_text(encoding="utf-8")
config = (ROOT / "myst.yml").read_text(encoding="utf-8")
assert "Spatial Cells and Their Models" in html
assert "  - title: Spatial Cell Models\n" not in config
assert "    - file: chapters/grid-to-place.md\n" not in config

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.iframes = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "iframe":
            self.iframes.append(attrs.get("src", ""))

page = Page()
page.feed(html)
for anchor in ["place-cell-models", "place-gaussian-model", "place-spike-generation",
               "grid-place-readout", "grid-place-live-example", "place-model-notebooks",
               "learned-place-models", "grid-cell-models", "grid-cosine-model",
               "grid-spacing-geometry", "grid-phase-model", "grid-model-parameters",
               "head-direction-models", "border-cell-models", "speed-cell-models",
               "time-cell-models", "spatial-exercises"]:
    assert anchor in page.ids, f"Missing merged chapter anchor: {anchor}"
for name in ["hippocampal-circuit", "place-recordings", "grid-recordings",
             "head-direction", "border-recordings", "speed-recordings", "time-recordings"]:
    assert f"fig-spatial-{name}" in page.ids, f"Lost literature figure: {name}"
assert sum("grid-place-interactive.html" in src for src in page.iframes) == 1
assert sum("border-cell-maze.html" in src for src in page.iframes) == 0, "Chapter 4 should not embed a LiDAR robot lab"
assert sum("border-cell-guided.html" in src for src in page.iframes) == 0
assert "(interactive-border-maze)=" in source, "Retain old URL anchor as a pointer"
assert "interactive-border-maze" in page.ids, "Old Chapter 4 bookmark must resolve to the moved-model pointer"
assert "08-lidar-encoding.md#lidar-interactive-border-maze" in source
assert "### 4.6.3 Turning LiDAR-driven" not in source
assert "### 4.6.4 Interactive square and circular" not in source
assert "### 4.6.2 Biological interpretation and experimental controls" in source
assert "  bibliography:" not in config, "Legacy BibTeX block appends duplicate APA citations below the IEEE reference list"
exercises = source.split("## 4.10 Exercises", 1)[1].split("## References", 1)[0]
assert [int(n) for n in re.findall(r"^(\d+)\.", exercises, re.M)] == list(range(1, 17))
solutions = (ROOT / "chapters" / "solutions-foundations.md").read_text(encoding="utf-8")
answers = solutions.split("## Chapter 4", 1)[1]
assert [int(n) for n in re.findall(r"^(\d+)\.", answers, re.M)] == list(range(1, 17))
legacy = (SITE / "chapters" / "grid-to-place" / "index.html").read_text(encoding="utf-8")
assert "window.location.replace" in legacy
assert "#grid-place-readout" in legacy
assert "grid-place-live-example" in legacy
print("Spatial chapter passed: all biological cell classes, seven literature figures, grid/place app, biological border section with legacy pointer, 16 exercises/solutions, and legacy grid redirects.")
