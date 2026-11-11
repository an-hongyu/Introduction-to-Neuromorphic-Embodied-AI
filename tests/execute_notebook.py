"""Execute the unchanged scientific notebook and fail on any cell error."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

path = Path(__file__).resolve().parents[1] / 'notebooks/place_cells.ipynb'
notebook = nbformat.read(path, as_version=4)
NotebookClient(notebook, timeout=180, kernel_name='python3',
               resources={'metadata': {'path': str(path.parent)}}).execute()
assert all(output.output_type != 'error'
           for cell in notebook.cells for output in cell.get('outputs', []))
figures = sum('image/png' in output.get('data', {})
              for cell in notebook.cells for output in cell.get('outputs', []))
assert figures >= 4, f'Expected the four laboratory figures, found {figures}'
nbformat.write(notebook, path)
print(f'Executed {len(notebook.cells)} cells; verified {figures} figures.')
