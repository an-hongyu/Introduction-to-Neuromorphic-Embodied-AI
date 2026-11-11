/* Numerical regression checks for the exact JavaScript embedded in the book. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(path.join(__dirname, '../assets/lif-interactive.html'), 'utf8');
const model = html.match(/<script id="lif-model">([\s\S]*?)<\/script>/)[1];
const ui = html.match(/<script id="lif-interface">([\s\S]*?)<\/script>/)[1];
new vm.Script(ui); // Validate UI syntax without mocking a browser.
const context = {window: {}};
vm.runInNewContext(model, context);
const {simulate, analyticalRate, defaults} = context.window.LIFModel;
const close = (a,b,tolerance=1e-9) => assert.ok(Math.abs(a-b)<=tolerance, `${a} != ${b}`);
const baseline = simulate(defaults);
close(baseline.spikes[0], 27.8);
close(baseline.intervalRate, 1000/29.8);
close(analyticalRate(defaults), 1000/(20*Math.log(4)+2));
assert.equal(baseline.spikes.length,16);
assert.equal(baseline.voltages.length,5001);
const quiet=simulate({...defaults,current:0});
assert.equal(quiet.spikes.length,0);
assert.ok(quiet.voltages.every(v=>v===-65));
for(const current of [100,150]) {
  assert.equal(simulate({...defaults,current}).spikes.length,0);
  assert.equal(analyticalRate({...defaults,current}),0);
}
const large=simulate({...defaults,capacitance:400});
close(large.spikes[0],55.5);
assert.ok(large.intervalRate<baseline.intervalRate);
const ref=simulate({...defaults,refractory:5});
close(ref.spikes[0],baseline.spikes[0]);
close(ref.spikes[1]-ref.spikes[0],32.8);
const fine=simulate(defaults,0.05);
assert.ok(Math.abs(fine.spikes[0]-20*Math.log(4)) < Math.abs(baseline.spikes[0]-20*Math.log(4)));
// A passive, subthreshold trace must match the RC analytical solution.
const sub=simulate({...defaults,current:100});
for(let k=0;k<sub.voltages.length;k+=13) close(sub.voltages[k],-55-10*Math.exp(-k*0.1/20));
// The full UI range must stay finite. First-spike/ISI errors are <= grid resolution.
let combinations=0;
for(const capacitance of [50,200,500]) for(const leak of [2,10,30])
for(const threshold of [-60,-50,-40]) for(const refractory of [0,2,10])
for(const current of [0,100,200,600]) for(const reset of [-80,-65,-61]) {
  const p={...defaults,capacitance,leak,threshold,refractory,reset};
  p.current=current;
  const r=simulate(p);
  assert.ok(r.voltages.every(Number.isFinite));
  assert.ok(r.voltages.every(v=>v<threshold));
  if(r.spikes.length>=2) {
    const exactPeriod=1000/analyticalRate(p);
    close(r.spikes[1]-r.spikes[0],exactPeriod,0.10000001);
  }
  combinations++;
}
assert.throws(()=>simulate({...defaults,leak:0}));
assert.throws(()=>simulate({...defaults,reset:-40}));
console.log(`Interactive LIF passed: Python-reference values, analytical RC, timing refinement, and ${combinations} parameter combinations.`);
