/* Five-stage textbook guided walkthrough and optional voltage sampling regression. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const M=require('../assets/border-cell-model.js');
const page=fs.readFileSync(path.join(__dirname,'../assets/border-cell-guided.html'),'utf8');
for (const id of ['shape','mode','wall','wallPicker','arena','map','voltage','advance','explore','reset','exTitle','exBody','d','i','hz','spikes']) assert.match(page,new RegExp('id="'+id+'"'));
for (const n of [1,2,3,4,5]) assert.match(page,new RegExp('data-stage="'+n+'"'));
assert.match(page,/360° LiDAR takes 36 measurements/);
assert.match(page,/value="all">All borders/);
assert.match(page,/M\.estimateBoundaryDistance\(s\.shape,s\.mode/);
assert.match(page,/occupancy-normalized firing-rate map/);
assert.match(page,/not a biological recording/);
assert.match(page,/s\.counts\[j\]\/s\.occ\[j\]/);
assert.match(page,/M\.stepLIF\(s\.neuron,s\.current,DT,\.001,\(v,fired,time\)=>/);
const n=M.newLIF();let samples=0,fired=0,first=null,last=null;
const count=M.stepLIF(n,M.wallCurrent(.25),.16,.001,(v,spike,t)=>{samples++;if(spike)fired++;if(first===null)first=t;last=t;assert.ok(v>=-.065-1e-9&&v<=-.05+1e-9);});
assert.equal(samples,160);assert.equal(fired,count);assert.ok(count>0);assert.ok(first>0);assert.ok(Math.abs(last-.16)<1e-12);
const noCallback=M.newLIF();
assert.equal(M.stepLIF(noCallback,M.wallCurrent(.25),.16,.001),count);
for(const shape of ['square','circle'])for(const wall of ['north','south','east','west']){const points=M.waypoints(shape);assert.ok(points.length>=40);for(const [x,y] of points)assert.ok(M.inside(x,y,shape));const rays=M.scan(shape,points[0][0],points[0][1],0);assert.equal(rays.length,36);assert.ok(Number.isFinite(M.estimateWallDistance(shape,wall,points[0][0],points[0][1],rays)));}
console.log('Guided border-cell walkthrough: five-stage markup, world-boundary model, LIF trace samples and unchanged spike-count behavior OK.');
