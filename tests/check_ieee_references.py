"""Keep all chapter bibliography entries consistently numbered and IEEE formatted.

This checks presentation and citation integrity only; it does not claim a new
metadata audit of third-party publisher records.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "01-introduction.md": 4,
    "01-neuroscience-background.md": 7,
    "02-spatial-cells.md": 22,
    "03-computational-neuron-models.md": 5,
    "04-hebbian-learning.md": 9,
    "06-visual-perception.md": 3,
    "07-inertial-sensing.md": 1,
    "08-lidar-encoding.md": 5,
    "09-nengo-ros-gazebo.md": 3,
    "10-associative-learning-robot.md": 1,
    "computational-neuron-models-lab.md": 3,
    "roadmap.md": 5,
}

# The legacy full-author format must not be reintroduced in bibliography lines.
FULL_AUTHOR = (
    "Hongyu An", "Wulfram Gerstner", "Eric R. Kandel", "Alan L. Hodgkin",
    "Xiaosheng Zhang", "Noah Zins", "Randall C. O'Reilly", "Peter Corke",
)
total = 0
for filename, expected in EXPECTED.items():
    source = (ROOT / "chapters" / filename).read_text(encoding="utf-8")
    heading = "### Book references" if filename == "roadmap.md" else "## References"
    assert source.count(heading) == 1, (filename, "reference heading changed")
    bib = source.split(heading, 1)[1]
    records = re.findall(r"^\[(\d+)\] ([^\n]+)$", bib, flags=re.MULTILINE)
    assert len(records) == expected, (filename, len(records), expected)
    assert [int(n) for n, _ in records] == list(range(1, expected + 1)), filename
    for n, entry in records:
        assert entry.endswith("."), (filename, n, "missing terminal period")
        assert "Art. no. no." not in entry and ".[Online]" not in entry, (filename, n)
        assert not re.search(r"doi:\s+10\.", entry), (filename, n, "unlinked DOI")
        if "doi:" in entry:
            assert re.search(r"doi: \[10\.[^]]+\]\(https://[^)]+\)", entry), (filename, n)
        if "[Online]" in entry:
            assert "[Online]. Available:" in entry, (filename, n)
        # Organizational authors (ROS 2, MathWorks, FDA etc.) are exempt.
        for full in FULL_AUTHOR:
            assert full not in entry.split("“", 1)[0].split("*", 1)[0], (filename, n, full)
    # All individually linked chapter reference anchors must survive the edit.
    if filename != "01-introduction.md":
        labels = re.findall(r"^\([\w-]+-ref-\d+\)=$", bib, flags=re.MULTILINE)
        assert len(labels) == expected, (filename, "citation anchors changed", len(labels))
    total += expected

assert total == 68
print(f"IEEE reference consistency passed: {total} numbered entries across {len(EXPECTED)} book sections.")
