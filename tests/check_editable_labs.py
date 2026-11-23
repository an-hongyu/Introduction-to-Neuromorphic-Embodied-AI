"""Regression-check student-editable notebook experiments, not just default Run All.

The reference checks must stay fixed, while changed learning pairings, STDP tau,
and spike-bin DT must not produce stale-expected-value assertion failures.
"""
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"


def variant(notebook_name, edits, assertions, label):
    path = NOTEBOOKS / notebook_name
    nb = nbformat.read(path, as_version=4)
    for original, replacement in edits:
        matches = 0
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            src = cell.source
            if original in src:
                assert src.count(original) == 1, f"{label}: duplicate edit text"
                cell.source = src.replace(original, replacement, 1)
                matches += 1
        assert matches == 1, f"{label}: did not find unique parameter {original!r}"
    nb.cells.append(new_code_cell(assertions))
    NotebookClient(
        nb, timeout=180, kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}}
    ).execute()
    assert all(output.output_type != "error"
               for cell in nb.cells for output in cell.get("outputs", []))
    print(f"PASS {label}")


variant(
    "hebbian_learning.ipynb",
    [("paired_outputs = np.eye(2)", "paired_outputs = np.eye(2)[::-1]")],
    """
assert np.allclose(weights, [[0., 0.8, 0.8], [0.8, 0.8, 0.]])
assert np.allclose(scores, [[0., 0.8], [0.8, 0.], [0.8, 0.8]])
assert np.allclose(baseline_weights, [[0.8, 0.8, 0.], [0., 0.8, 0.8]])
""",
    "Lab 3 reversed output pairing without stale baseline failure",
)

variant(
    "hebbian_learning.ipynb",
    [("STDP_TAU_MS = 20.0", "STDP_TAU_MS = 10.0")],
    """
assert np.isclose(STDP_TAU_MS, 10.0)
assert np.isclose(pair_stdp(10, tau_ms=STDP_TAU_MS), 0.01*np.exp(-1))
assert np.allclose(weights, baseline_weights)
""",
    "Lab 3 STDP tau = 10 ms changes curve and preserves reference test",
)

variant(
    "place_cells.ipynb",
    [("DT = 0.02", "DT = 0.01"), ("sigma = 0.14", "sigma = 0.25")],
    """
assert np.isclose(DT, 0.01)
assert np.isclose(sigma, 0.25)
baseline_times = np.arange(int(round(DURATION/0.02)))*0.02
baseline_positions = sample_path(baseline_times, reference_times, reference_position)
assert np.allclose(position[::2], baseline_positions, atol=1e-12)
assert np.isclose(expected_total, np.sum(expected_rate*DT))
assert np.isclose(float(np.sum(fine_lambda)), fine_expected_total)
""",
    "Lab 2 smaller spike bin uses identical 20 ms path samples",
)
