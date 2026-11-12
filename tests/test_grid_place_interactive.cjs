'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync(path.join(__dirname,'../assets/grid-place-interactive.html'),'utf8');
const model=html.match(/<script id="grid-place-model">([\s\S]*?)<\/script>/)[1];
new vm.Script(html.match(/<script id="grid-place-interface">([\s\S]*?)<\/script>/)[1]);
const context={window:{}};vm.runInNewContext(model,context);const M=context.window.GridPlaceModel;
const near=(a,b,t=1e-9)=>assert.ok(Math.abs(a-b)<t,`${a} != ${b}`);
const c=M.makeCells()[0],x=c.phaseX,y=c.phaseY;
near(M.gridRate(x,y,c),30);near(M.gridRate(x+c.spacing,y,c),30);
for(const theta of [0,17,43]){
 const rotated={...c,orientation:theta},a=theta*Math.PI/180;
 near(M.gridRate(x+c.spacing*Math.cos(a),y+c.spacing*Math.sin(a),rotated),30);
 for(const [px,py] of [[0,0],[.21,-.31],[-.91,.37]]){
  near(M.gridRate(px,py,rotated),M.gridRate(px,py,{...rotated,orientation:theta+60}));
  near(M.gridRate(px,py,rotated),M.gridRate(2*px,2*py,{...rotated,spacing:2*c.spacing,phaseX:2*x,phaseY:2*y}));
  near(M.gridRate(px,py,rotated)*1.5,M.gridRate(px,py,{...rotated,kappa:.75}));
 }
}
const fixtures=JSON.parse(fs.readFileSync(path.join(__dirname,'grid_place_reference.json')));
for(const f of fixtures){const r=M.readout(f.x,f.y,f.cells,f.count,f.threshold);near(r.drive,f.drive);near(r.rate,f.rate);r.rates.forEach((v,j)=>near(v,f.rates[j]));near(r.contributions.reduce((a,b)=>a+b,0),r.drive);}
let cases=0;
for(const spacing of [.2,.38,1.8])for(const orientation of [0,29,60])for(const kappa of [0,.5,1])for(const zeta of [-1,0,1]){
 const cell={...c,spacing,orientation,kappa,zeta};for(const [px,py] of [[-1,-1],[.12,-.08],[.67,.23],[1,1]]){
  const v=M.gridRate(px,py,cell),n=M.normalized(px,py,cell);assert.ok(Number.isFinite(v)&&v>=0&&v<=M.maximum(cell)+1e-9);assert.ok(n>=0&&n<=1);cases++;
 }
}
const diverse=M.sample(M.makeCells(),6,.78),same=M.sample(M.makeCells('identical'),6,.78),one=M.sample(M.makeCells(),1,.78);
assert.equal(M.patches(diverse.place,diverse.n),1);assert.ok(M.patches(same.place,same.n)>10);assert.equal(M.patches(same.place,same.n),M.patches(one.place,one.n));
for(let i=0;i<same.place.length;i++)near(same.place[i],one.place[i]);
const zero=M.makeCells().map(c=>({...c,weight:0}));assert.equal(M.readout(0,0,zero,6,.78).rate,0);
const inactive=M.makeCells().map(c=>({...c,kappa:0,zeta:-1}));assert.equal(M.readout(0,0,inactive,6,.78).rate,0);
const raised=M.sample(M.makeCells(),6,.9);assert.ok(raised.place.filter(v=>v>0).length<diverse.place.filter(v=>v>0).length);
assert.throws(()=>M.gridRate(0,0,{...c,spacing:0}));assert.throws(()=>M.readout(0,0,M.makeCells(),6,1));
console.log(`Interactive grid/place passed: 24 NumPy comparisons, ${cases} parameter/position cases, lattice geometry, gain, alias controls, threshold support, and silent inputs.`);
