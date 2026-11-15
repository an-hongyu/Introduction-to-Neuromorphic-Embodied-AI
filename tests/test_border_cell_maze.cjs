/* Numerical checks for the textbook's square/circle LiDAR -> world boundary -> LIF lab. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const M = require('../assets/border-cell-model.js');
const html = fs.readFileSync(require('node:path').join(__dirname, '../assets/border-cell-maze.html'), 'utf8');
assert.match(html, /border-cell-model\.js/);
assert.match(html, /id="mazeCanvas"/);
assert.match(html, /id="mapCanvas"/);
assert.match(html, /id="rotate"/);
assert.match(html, /id="batch"/);
assert.match(html, /occupancy-normalized/i);
assert.match(html, /not a learned synaptic weight map/i);
assert.match(html, /for\(let i=0;i<100;i\+\+\)nextStep\(\)/);
assert.equal(M.SECTORS, 36);
assert.equal(M.waypoints('square').length, 40);
assert.ok(M.waypoints('circle').length > 150);
function near(a,b,tol=1e-7) { assert.ok(Math.abs(a-b)<=tol, `${a} != ${b}`); }
for(const shape of ['square','circle']) {
  near(M.rayDistance(shape,0,0,0),2);
  near(M.rayDistance(shape,0,0,Math.PI/2),2);
  near(M.rayDistance(shape,0,1.5,Math.PI/2),.5);
  assert.ok(M.inside(1.5,.1,shape));
  assert.ok(!M.inside(2.2,0,shape));
  for(const wall of ['north','east','south','west']) {
    const p=M.probe(shape,wall);
    near(p.worldBefore,p.worldAfter,1e-7);
    near(p.rateBefore,p.rateAfter,1e-7);
    near(p.bodyBefore,.38,1e-7);
    near(p.bodyAfter,3.62,1e-7);
    near(p.worldBefore,.38,1e-7);
    assert.ok(p.rateBefore>35 && p.rateBefore<60);
  }
  // Changing heading should permute world points but preserve selected-world distance.
  for(const [x,y] of [[0,0],[.5,.3],[-1.1,.4],[0,1.55]]) {
    const a=M.scan(shape,x,y,.23), b=M.scan(shape,x,y,.23+Math.PI);
    assert.equal(a.length,36);assert.equal(b.length,36);
    for(const wall of ['north','east','south','west']) {
      const d0=M.estimateWallDistance(shape,wall,x,y,a);
      const d1=M.estimateWallDistance(shape,wall,x,y,b);
      near(d0,d1,1e-7);
      // Selected world-distance is close to ideal geometry despite finite angular sampling.
      assert.ok(Math.abs(d0-M.trueWallDistance(shape,wall,x,y))<.26, `${shape} ${wall} at ${x},${y}: ${d0}`);
    }
  }
  for(const [x,y] of M.waypoints(shape)) assert.ok(M.inside(x,y,shape,.1));
}
const d=[.2,.5,1,2];
const currents=d.map(x=>M.wallCurrent(x,.55));
const rates=currents.map(M.lifRate);
assert.ok(currents[0]>currents[1] && currents[1]>currents[2] && currents[2]>currents[3]);
assert.ok(rates[0]>rates[1] && rates[1]>=rates[2]);
assert.equal(rates[3],0);
const n=M.newLIF();let total=0;
for(let i=0;i<10;i++)total+=M.stepLIF(n,M.wallCurrent(.2),.1);
assert.ok(total >= 45 && total <= 70, `Unexpected 1-second spike count ${total}`);
const silent=M.newLIF();assert.equal(M.stepLIF(silent,M.wallCurrent(2),1),0);
assert.equal(M.wallCurrent(NaN),0);
assert.equal(M.sensorCurrent(NaN,false),0);
assert.throws(()=>M.stepLIF(n,-1),/Invalid/);

// Seeded random trajectories must be repeatable, different across seeds,
// collision-free, and cover substantially more than a simple line.
for(const shape of ['square','circle']){
  const a=M.createExplorer(shape,23),b=M.createExplorer(shape,23),c=M.createExplorer(shape,24);
  const bins=new Set();let closeBoundary=0,different=false,largeTurns=0;
  for(let i=0;i<1400;i++){
    const prev={x:a.x,y:a.y,heading:a.heading};
    const x=M.exploreStep(a),y=M.exploreStep(b),z=M.exploreStep(c);
    near(x.x,y.x,1e-12);near(x.y,y.y,1e-12);near(x.heading,y.heading,1e-12);
    assert.ok(M.inside(x.x,x.y,shape,.15),'explorer must keep a modeled .15 m clearance');
    near(Math.hypot(x.x-prev.x,x.y-prev.y),.107,1e-10);
    if(Math.hypot(x.x-z.x,x.y-z.y)>1e-4)different=true;
    const ix=Math.floor((x.x+2)/4*25),iy=Math.floor((x.y+2)/4*25);
    bins.add(iy*25+ix);
    if(shape==='circle'?Math.hypot(x.x,x.y)>1.5:Math.max(Math.abs(x.x),Math.abs(x.y))>1.5)closeBoundary++;
    if(Math.abs(M.wrap(x.heading-prev.heading))>.02)largeTurns++;
  }
  assert.ok(different,'different seeds should generate different paths');
  assert.ok(bins.size>290,shape+' stochastic coverage too narrow: '+bins.size);
  assert.ok(closeBoundary>120,shape+' random path does not sample near walls');
  assert.ok(largeTurns>150,shape+' path did not turn and explore');
}
assert.throws(()=>M.createExplorer('square',0),/Seed/);
const sigma=.55,cutoff=sigma*Math.sqrt(2*Math.log(180/50));
near(cutoff,.8803209508494894,1e-8);
near(M.wallCurrent(.38)*1e12,241.78046346549058,1e-5);
assert.ok(M.lifRate(M.wallCurrent(.88))>0);
assert.equal(M.lifRate(M.wallCurrent(.89)),0);
assert.match(html,/id="seed"/);
assert.match(html,/id="newPath"/);
assert.match(html,/id="longBatch"/);
assert.match(html,/M\.exploreStep\(state\.explorer\)/);

console.log('Border-cell maze passed: ray-casting, 36 channels, wall/arc invariance for 180-degree rotations, source distance, physical LIF, deterministic navigation, and UI controls.');
