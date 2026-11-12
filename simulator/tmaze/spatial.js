/* Reimplementation of explicit tuning equations, not learned grid-to-place weights. */
(function(root){'use strict';
const PEAK=40,N=30,DT=.001;
function configuration(){const grid=[];[.6,1,1.6].forEach((s,m)=>{for(let p=0;p<4;p++)grid.push({spacing_m:s,orientation_rad:m*Math.PI/9,phase_m:[s*(p%2)/3,s*Math.floor(p/2)/3],kappa:.5,baseline:0});});const place=[];for(let i=0;i<11;i++)place.push({center_m:[Number((-3+.6*i).toFixed(10)),3.5],sigma_m:.3});for(let i=0;i<7;i++)place.push({center_m:[0,Number((.45*i).toFixed(10))],sigma_m:.3});return {grid,place,peak_hz:PEAK,n_grid:12,n_place:18,position_source:'privileged map position; no path integration',model_scope:'paper tuning equations; no learned grid-to-place mapping or multimodal gating'};}
const CONFIG=configuration();
function rates(p){if(p.length!==2||!p.every(Number.isFinite))throw Error('Finite x/y position required');const r=CONFIG.grid.map(g=>{const q=4*Math.PI/(Math.sqrt(3)*g.spacing_m),dx=p[0]-g.phase_m[0],dy=p[1]-g.phase_m[1];let sum=0;for(let a=0;a<3;a++){const t=g.orientation_rad+a*Math.PI/3;sum+=Math.cos(q*(dx*Math.cos(t)+dy*Math.sin(t)));}return PEAK*Math.max(0,g.kappa*sum+g.baseline)/(3*g.kappa+g.baseline);});for(const c of CONFIG.place)r.push(PEAK*Math.exp(-((p[0]-c.center_m[0])**2+(p[1]-c.center_m[1])**2)/(2*c.sigma_m**2)));return r;}

/* Fixed ridge-fit Grid -> Place synapses. This is an engineering decoder
   trained on Gaussian reference fields, NOT learned biological connectivity.
   Signed weights allow inhibitory contributions; the 13th coefficient is bias.
   The online place drive uses filtered PRESYNAPTIC SPIKES, not true position. */
const TRAIN_POINTS=[];
for(let y=-.2;y<=3.8+1e-9;y+=.1)TRAIN_POINTS.push([0,Number(y.toFixed(5))]);
for(let x=-3.3;x<=3.3+1e-9;x+=.1)TRAIN_POINTS.push([Number(x.toFixed(5)),3.5]);
function solve(A,b){
 const n=b.length,M=A.map((row,i)=>[...row,b[i]]);
 for(let c=0;c<n;c++){
  let k=c;for(let r=c+1;r<n;r++)if(Math.abs(M[r][c])>Math.abs(M[k][c]))k=r;
  if(Math.abs(M[k][c])<1e-12)throw Error('Singular grid mapping');
  [M[k],M[c]]=[M[c],M[k]];
  const d=M[c][c];for(let j=c;j<=n;j++)M[c][j]/=d;
  for(let r=0;r<n;r++)if(r!==c){const f=M[r][c];for(let j=c;j<=n;j++)M[r][j]-=f*M[c][j];}
 }
 return M.map(row=>row[n]);
}
function fitMapping(ridge=.03){
 if(!(ridge>0&&Number.isFinite(ridge)))throw Error('Positive ridge needed');
 const samples=TRAIN_POINTS.map(p=>rates(p).map(x=>x/PEAK));
 const X=samples.map(r=>[1,...r.slice(0,12)]);
 const gram=Array.from({length:13},()=>new Array(13).fill(0));
 for(const x of X)for(let a=0;a<13;a++)for(let b=0;b<13;b++)gram[a][b]+=x[a]*x[b];
 for(let a=1;a<13;a++)gram[a][a]+=ridge*X.length;
 const weights=Array.from({length:18},(_,j)=>{
  const rhs=new Array(13).fill(0);
  for(let n=0;n<X.length;n++)for(let a=0;a<13;a++)rhs[a]+=X[n][a]*samples[n][12+j];
  return solve(gram,rhs);
 });
 return {weights:weights.map(row=>row.slice(1)),bias:weights.map(row=>row[0]),ridge,training_samples:X.length,
  convention:'W[place][grid]; signed static ridge-fit coefficients; input filtered grid spikes / 40 Hz',
  supervision:'Gaussian place fields from privileged map position, offline only'};
}
const MAPPING=fitMapping();
function mappedRates(gridHz,mapping=MAPPING){
 if(!Array.isArray(gridHz)||gridHz.length!==12||!gridHz.every(v=>Number.isFinite(v)&&v>=0))throw Error('12 nonnegative grid firing rates required');
 return mapping.weights.map((w,j)=>Math.max(0,Math.min(PEAK,PEAK*(mapping.bias[j]+w.reduce((s,v,i)=>s+v*gridHz[i]/PEAK,0)))));
}


/* Tianze-inspired thresholded convergence: select K grid units with the
   strongest response at each specified place center. K-of-N coincidence is
   implemented as thresholded postsynaptic drive, with binary afferent weights.
   This is a fixed spatially anchored connection rule; it is NOT a reproduction
   of an undisclosed trained connectome, and it does NOT learn place centers. */
function coincidenceMapping(k=6, thresholdFraction=.72){
 if(!Number.isInteger(k)||k<1||k>12)throw Error('k in 1..12');
 if(!(thresholdFraction>0&&thresholdFraction<1))throw Error('threshold in (0,1)');
 const weights=[], thresholds=[], referenceDrives=[];
 for(const cell of CONFIG.place){
  const g=rates(cell.center_m).slice(0,12);
  const indices=Array.from({length:12},(_,i)=>i).sort((a,b)=>g[b]-g[a]||a-b).slice(0,k);
  const row=Array.from({length:12},(_,i)=>indices.includes(i)?1:0);
  const drive=g.reduce((sum,v,i)=>sum+v*row[i],0);
  weights.push(row);referenceDrives.push(drive);thresholds.push(drive*thresholdFraction);
 }
 return {weights,thresholds,referenceDrives,k,thresholdFraction,learning:'none',
  description:'Fixed top-k grid afferents selected at each reference place center; thresholded coincidence; no online weight learning'};
}
const COINCIDENCE=coincidenceMapping();
function coincidenceRates(gridHz,mapping=COINCIDENCE){
 if(!Array.isArray(gridHz)||gridHz.length!==12||!gridHz.every(v=>Number.isFinite(v)&&v>=0))throw Error('12 nonnegative grid rates required');
 return mapping.weights.map((row,j)=>{
  const drive=row.reduce((sum,w,i)=>sum+w*gridHz[i],0),low=mapping.thresholds[j],high=mapping.referenceDrives[j];
  if(high<=low)return 0;
  return PEAK*Math.pow(Math.max(0,Math.min(1,(drive-low)/(high-low))),2);
 });
}



/* 12/24/36 spatial grid populations share the ablation's deterministic
   scale/phase construction. Extra grids are new simulated LIF neurons. */
function populationGrids(n=12){
 if(![12,24,36].includes(n))throw Error('Grid population must be 12, 24 or 36');
 const gs=CONFIG.grid.map(g=>({...g,phase_m:[...g.phase_m]}));
 for(let tier=1;gs.length<n;tier++)for(let m=0;m<3;m++)for(let p=0;p<4;p++){
  const spacing=[.6,1,1.6][m]*(tier===1?1.13:.89),a=m*Math.PI/9+(tier===1?Math.PI/12:-Math.PI/11);
  gs.push({spacing_m:spacing,orientation_rad:a,phase_m:[spacing*((p%2)/3+.137*tier),spacing*(Math.floor(p/2)/3+.083*tier)],kappa:.5,baseline:0});
 }
 return gs.slice(0,n);
}
function gridPopulationRates(p,n=12){
 if(!Array.isArray(p)||p.length!==2||!p.every(Number.isFinite))throw Error('Finite position required');
 return populationGrids(n).map(g=>{
  const q=4*Math.PI/(Math.sqrt(3)*g.spacing_m),dx=p[0]-g.phase_m[0],dy=p[1]-g.phase_m[1];let sum=0;
  for(let a=0;a<3;a++){const th=g.orientation_rad+a*Math.PI/3;sum+=Math.cos(q*(dx*Math.cos(th)+dy*Math.sin(th)));}
  return PEAK*Math.max(0,g.kappa*sum+g.baseline)/(3*g.kappa+g.baseline);
 });
}

/* Corrected grid-pattern coincidence (12 -> 18):
   all 12 signed/push-pull pattern channels participate, rather than top-six
   excitatory sum. Synaptic template per place cell is the grid rate pattern
   at its anchor site. Place drive is a nonlinear feature-space radial basis:
   exp(-sum_i ((z_i/PEAK - template_ji)^2)/(2*width^2)).
   Only Grid LIF spike traces z_i are used ONLINE; anchor sites are supplied
   for OFFLINE model construction and reference comparison. No plasticity. */
function patternMapping(width=.4,nGrid=12){
 if(!(width>0&&Number.isFinite(width)))throw Error('Positive pattern width required');
 if(![12,24,36].includes(nGrid))throw Error('Invalid grid population');
 return {weights:CONFIG.place.map(c=>gridPopulationRates(c.center_m,nGrid).map(v=>v/PEAK)),
  width,learning:'none',input_count:nGrid,output_count:18,training_samples:18,
  description:'12-dimensional normalized grid spike-pattern template; squared mismatch provides opponent inhibition; fixed place anchors'};
}
const PATTERN=patternMapping();
function patternRates(gridHz,mapping=PATTERN){
 if(!Array.isArray(gridHz)||gridHz.length!==mapping.input_count||!gridHz.every(v=>Number.isFinite(v)&&v>=0))throw Error('Invalid grid firing vector');
 return mapping.weights.map(row=>PEAK*Math.exp(-row.reduce((sum,v,i)=>sum+(v-gridHz[i]/PEAK)**2,0)*12/mapping.input_count/(2*mapping.width**2)));
}

function bin(p){if(!(p[0]>=-4&&p[0]<4&&p[1]>=-1&&p[1]<4.6))throw Error('Position outside map bounds');return Math.floor((p[1]+1)/.1)*80+Math.floor((p[0]+4)/.1);}
class Bank{
 constructor(mode='reference',nGrid=12){if(!['reference','mapped','coincidence','pattern'].includes(mode))throw Error('Invalid place mode');if(![12,24,36].includes(nGrid))throw Error('Grid population must be 12/24/36');if(nGrid!==12&&mode!=='pattern')throw Error('Expanded grids require pattern mode');this.mode=mode;this.nGrid=nGrid;this.nTotal=nGrid+18;this.mapping=mode==='coincidence'?COINCIDENCE:mode==='pattern'?patternMapping(.4,nGrid):MAPPING;this.gridTrace=new Array(nGrid).fill(0);this.steps=0;this.targets=new Array(this.nTotal).fill(0);this.current=new Array(this.nTotal).fill(0);this.voltage=Array.from({length:this.nTotal},(_,i)=>i*.95/(this.nTotal-1));this.ref=new Array(this.nTotal).fill(0);this.counts=new Array(this.nTotal).fill(0);this.events=Array.from({length:this.nTotal},()=>[]);this.spikes=[];this.total=0;this.maps=new Map();this.heldBin=bin([0,0]);}
 hold(p){this.targets=[...gridPopulationRates(p,this.nGrid),...rates(p).slice(12)];this.current=this.targets.map((f,i)=>f>0&&!(this.mode!=='reference'&&i>=this.nGrid)?-1/Math.expm1((.002-1/f)/.020):0);this.heldBin=bin(p);}
 step(){this.steps++;const t=this.steps*DT;let row=this.maps.get(this.heldBin);if(!row){row=[this.heldBin,0,...new Array(this.nTotal).fill(0)];this.maps.set(this.heldBin,row);}row[1]+=DT;
  if(this.mode!=='reference'){
   // Decay the presynaptic exponential spike traces (tau=150 ms).
   const decay=Math.exp(-DT/(this.mode==='pattern'?.6:.15));
   for(let i=0;i<this.nGrid;i++)this.gridTrace[i]*=decay;
   const pred=this.mode==='pattern'?patternRates(this.gridTrace,this.mapping):this.mode==='coincidence'?coincidenceRates(this.gridTrace):mappedRates(this.gridTrace);
   for(let j=0;j<18;j++){const f=pred[j];this.targets[this.nGrid+j]=f;this.current[this.nGrid+j]=f>0?-1/Math.expm1((.002-1/f)/.020):0;}
  }
  for(let i=0;i<this.nTotal;i++){this.ref[i]-=DT;const delta=Math.max(0,Math.min(DT,DT-this.ref[i])),j=this.current[i];let v=this.voltage[i]-(j-this.voltage[i])*Math.expm1(-delta/.020);if(v>1){const sp=DT+.020*Math.log1p(-(v-1)/(j-1));this.ref[i]=.002+sp;v=0;this.counts[i]++;row[i+2]++;this.total++;if(this.mode!=='reference'&&i<this.nGrid)this.gridTrace[i]+=1/(this.mode==='pattern'?.6:.15);this.events[i].push(t);this.spikes.push([t,i]);}this.voltage[i]=Math.max(0,v);}}
 trim(){const t=this.steps*DT;for(const q of this.events)while(q.length&&q[0]<=t-.5+1e-9)q.shift();while(this.spikes.length&&this.spikes[0][0]<t-4)this.spikes.shift();}
 snapshot(){this.trim();return {config:{...CONFIG,grid:populationGrids(this.nGrid),n_grid:this.nGrid,n_place:18},targets_hz:this.targets,rates_hz:this.events.map(q=>q.length/.5),total_spikes:this.total,counts:this.counts,time_s:this.steps*DT,spikes:this.spikes,window_s:.5,maps:[...this.maps.values()],map_grid:{xmin:-4,ymin:-1,spacing_m:.1,nx:80,ny:56},map_definition:'counts / occupied seconds; unvisited bins are unknown; no smoothing',gating_enabled:false,learned_mapping:false,place_mode:this.mode,grid_to_place_mapping:this.mode!=='reference'?this.mapping:null,grid_trace_hz:this.mode!=='reference'?[...this.gridTrace]:null};}
}
const api={Bank,configuration,rates,bin,fitMapping,mappedRates,MAPPING,coincidenceMapping,coincidenceRates,COINCIDENCE,patternMapping,patternRates,PATTERN,populationGrids,gridPopulationRates};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.BrainXSpatial=api;
})(typeof window!=='undefined'?window:globalThis);
