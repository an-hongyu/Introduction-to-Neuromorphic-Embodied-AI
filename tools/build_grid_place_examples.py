"""Create the self-contained grid/place laboratory and NumPy reference fixtures."""
from pathlib import Path
import json
import nbformat
ROOT=Path(__file__).resolve().parents[1]
MODEL=r'''
import numpy as np
import matplotlib.pyplot as plt

def grid_rate(x,y,cell):
    """x,y,spacing,phase: m; orientation: deg; output: declared Hz proxy."""
    angles=np.deg2rad(cell['orientation'])+np.pi/6+np.arange(3)*np.pi/3
    k=4*np.pi/(np.sqrt(3)*cell['spacing'])
    phase=k*(np.asarray(x)[...,None]-cell['phaseX'])*np.cos(angles)
    phase+=k*(np.asarray(y)[...,None]-cell['phaseY'])*np.sin(angles)
    return 20*np.maximum(0,cell['kappa']*np.cos(phase).sum(axis=-1)+cell['zeta'])

def make_cells(identical=False):
    return [dict(spacing=.38 if identical else spacing,
                 orientation=0 if identical else j*7,phaseX=.12,phaseY=-.08,
                 kappa=.5,zeta=0.,weight=1.)
            for j,spacing in enumerate([.38,.47,.59,.73,.89,1.09])]

def grid_to_place(x,y,cells,count=6,threshold=.78):
    rates=np.stack([grid_rate(x,y,c) for c in cells],axis=-1)
    maxima=np.array([20*max(0,3*c['kappa']+c['zeta']) for c in cells])
    normalized=np.divide(rates,maxima,out=np.zeros_like(rates),where=maxima>0)
    weights=np.array([c['weight'] for c in cells[:count]])
    total=weights.sum()
    drive=(normalized[...,:count]*weights).sum(axis=-1)/total if total>0 else np.zeros_like(rates[...,0])
    return rates,drive,25*np.maximum(0,(drive-threshold)/(1-threshold))

cells=make_cells()
axis=np.linspace(-1,1,121)
X,Y=np.meshgrid(axis,axis)
rates,drive,place=grid_to_place(X,Y,cells)
'''
PLOT=r'''
# EDIT one cell, e.g. cells[0]['spacing']=.76 or cells[0]['orientation']=30.
# Then rerun grid_to_place below. Changing the model-definition cell resets cells.
rates,drive,place=grid_to_place(X,Y,cells)
fig,axes=plt.subplots(2,3,figsize=(10,6.4),constrained_layout=True)
for j,ax in enumerate(axes.flat):
    image=ax.imshow(rates[...,j],origin='lower',extent=(-1,1,-1,1),vmin=0,vmax=80,cmap='viridis')
    ax.set(title=f"G{j+1}: spacing {cells[j]['spacing']:.2f} m, angle {cells[j]['orientation']}°",xlabel='x (m)',ylabel='y (m)')
fig.colorbar(image,ax=axes.ravel().tolist(),label='Grid rate proxy (Hz)')
plt.show()
'''
COMPARE=r'''
fig,axes=plt.subplots(1,3,figsize=(12,3.7),constrained_layout=True)
for ax,(label,population,count) in zip(axes,[('One grid',make_cells(),1),('Six identical grids',make_cells(True),6),('Six diverse grids',cells,6)]):
    _,_,output=grid_to_place(X,Y,population,count=count,threshold=.78)
    image=ax.imshow(output,origin='lower',extent=(-1,1,-1,1),vmin=0,vmax=25,cmap='viridis')
    ax.set(title=label,xlabel='x (m)',ylabel='y (m)')
fig.colorbar(image,ax=axes.tolist(),label='Place-like rate proxy (Hz)')
plt.show()

# Mechanism checks use an independent default population, so edits remain valid.
c=make_cells()[0]
assert np.isclose(grid_rate(c['phaseX'],c['phaseY'],c),30)
assert np.isclose(grid_rate(c['phaseX']+c['spacing'],c['phaseY'],c),30)
assert np.isclose(grid_rate(.21,-.31,c),grid_rate(.21,-.31,{**c,'orientation':60}))
for point in [(0.,0.),(.4,-.5),(-.7,.8)]:
    assert np.isclose(grid_rate(*point,c),grid_rate(2*point[0],2*point[1],{**c,'spacing':2*c['spacing'],'phaseX':2*c['phaseX'],'phaseY':2*c['phaseY']}))
zero=[{**v,'weight':0} for v in make_cells()]
assert grid_to_place(.1,.2,zero)[2]==0
assert np.isclose(grid_to_place(.12,-.08,make_cells())[2],25)
print('Grid/place checks passed: lattice spacing, 60-degree symmetry, scaling, aligned peak, and zero-weight output.')
'''
if __name__=='__main__':
    intro='''# Laboratory 8 — Grid Cells to Place-Like Fields

Companion to the Grid Cells and Grid-to-Place Mapping chapter. This is a fully specified feedforward teaching construction based on Liu et al.'s interference and threshold-sum framework. The phases are deliberately aligned; weights are fixed. No Gaussian place field is inserted, and no synaptic learning or spike generation is claimed.

[Run in Colab](https://colab.research.google.com/github/an-hongyu/Introduction-to-Neuromorphic-Embodied-AI/blob/main/notebooks/grid_to_place.ipynb)

## Model conventions

Spacing is the nearest-neighbor lattice distance in metres. The angular frequency is $k=4\\pi/(\\sqrt3\\lambda)$ in rad/m. Wave axes are $\\theta+30^\\circ+m60^\\circ$, making $\\theta$ a real-space lattice axis. Phase is a translation in metres. Gain and additive offset are dimensionless, followed by a chosen 20 Hz scale.

Grid activities are normalized by their theoretical maxima before weighted averaging. This removes pure multiplicative gain changes when offset is zero. A chosen threshold and rectifier map the pooled drive into a 0–25 Hz proxy. See the chapter for the paper/version distinctions and complete equations.'''
    nb=nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell(intro),nbformat.v4.new_code_cell(MODEL),nbformat.v4.new_markdown_cell('## Change one grid parameter and inspect all input fields'),nbformat.v4.new_code_cell(PLOT),nbformat.v4.new_markdown_cell('## Compare repeated versus localized outputs\n\nChange `threshold` or `count` in the examples. Field uniqueness is assessed only within the sampled arena. A fixed readout does not demonstrate learned place-field formation.'),nbformat.v4.new_code_cell(COMPARE),nbformat.v4.new_markdown_cell('''## References and further reading

[1] Tianze Liu, Kang Jun Bai, and Hongyu An, “Replicating associative learning of rodents with a neuromorphic robot in an open-field arena,” *Frontiers in Neuroscience*, vol. 19, Art. no. 1565780, 2025, doi: [10.3389/fnins.2025.1565780](https://doi.org/10.3389/fnins.2025.1565780).

[2] Tianze Liu, Zihan Jin, Dong Song, and Hongyu An, “A Neuromorphic Robot as a Digital Twin for Rodent Spatial Representation in Dynamic Environment Navigation,” *IEEE Journal on Emerging and Selected Topics in Circuits and Systems*, 2026, doi: [10.1109/JETCAS.2026.3733540](https://doi.org/10.1109/JETCAS.2026.3733540).

**Model provenance.** The cosine form was checked against the available author manuscript, sec. III-D, eq. (8).

Read the chapter before treating an imposed peak alignment as learned spatial coding. The notebook's normalization, 20 Hz scale, weights, and threshold are explicit teaching choices.''')])
    nb.metadata.kernelspec={'display_name':'Python 3','language':'python','name':'python3'}
    nb.metadata.language_info={'name':'python'}
    nbformat.write(nb,ROOT/'notebooks/grid_to_place.ipynb')
    scope={};exec(MODEL,scope)
    cases=[]
    for mode in [False,True]:
        pop=scope['make_cells'](mode)
        for count in [1,3,6]:
            for x,y,t in [(0.,0.,.78),(.12,-.08,.78),(-.71,.39,.3),(.41,-.55,.95)]:
                raw,drive,place=scope['grid_to_place'](x,y,pop,count,t)
                cases.append(dict(cells=pop,count=count,threshold=t,x=x,y=y,rates=raw.tolist(),drive=float(drive),rate=float(place)))
    (ROOT/'tests/grid_place_reference.json').write_text(json.dumps(cases,indent=2)+'\n')
    exec(PLOT,scope);scope['fig'].savefig('/tmp/grid-input-review.png',dpi=140)
    exec(COMPARE,scope);scope['fig'].savefig('/tmp/grid-place-review.png',dpi=140)
    print('Created grid/place laboratory and 24 independent NumPy reference cases.')
