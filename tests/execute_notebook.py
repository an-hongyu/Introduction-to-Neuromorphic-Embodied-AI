"""Execute every laboratory; verify expected figures and fail on cell errors."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
expected_figures = {'place_cells.ipynb': 4, 'lif_neuron.ipynb': 1, 'hebbian_learning.ipynb': 1}
for name, minimum in expected_figures.items():
    path = root / 'notebooks' / name
    notebook = nbformat.read(path, as_version=4)
    NotebookClient(notebook, timeout=180, kernel_name='python3',
                   resources={'metadata': {'path': str(path.parent)}}).execute()
    assert all(output.output_type != 'error'
               for cell in notebook.cells for output in cell.get('outputs', []))
    figures = sum('image/png' in output.get('data', {})
                  for cell in notebook.cells for output in cell.get('outputs', []))
    assert figures >= minimum, f'{name}: expected {minimum} figures, found {figures}'
    nbformat.write(notebook, path)
    print(f'{name}: executed {len(notebook.cells)} cells; verified {figures} figures.')
