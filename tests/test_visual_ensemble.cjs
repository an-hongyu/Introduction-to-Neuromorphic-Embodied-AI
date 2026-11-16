'use strict';
// Synthetic visual ensemble regression: NO learned weights or SFN training.
const assert=require('node:assert/strict');
const M=require('../assets/visual-ensemble-model.js');
const counts={};
function close(x,y,tol=1e-7){assert.ok(Math.abs(x-y)<tol,`${x} vs ${y}`);}
for(const rf of [3,5]){
 for(const shape of ['triangle','square']){
  let correct=0,incorrect=0,uncertain=0,excluded=0;
  for(let roll=0;roll<360;roll+=15)
   for(const yaw of [-50,-25,0,25,50])
    for(const pitch of [-40,0,40])
     for(const x of [-5,0,5]){
      const s={rf,shape,roll,yaw,pitch,x,y:0,distance:4};
      const vertices=M.project(s);
      // Test fully visible, sufficiently large projected targets.
      if(vertices.some(v=>v.x<2||v.x>58||v.y<2||v.y>58)){excluded++;continue;}
      const result=M.evaluate(s);
      // Ensure the generated source label is not passed to the classifier:
      const standalone=M.classify(M.raster(vertices),rf);
      assert.equal(result.decision,standalone.decision);
      close(result.ratio,standalone.ratio);
      if(result.decision===shape)correct++;
      else if(result.decision==='uncertain')uncertain++;
      else incorrect++;
      assert.ok(result.ratio>=0&&result.ratio<=1.001);
      assert.equal(result.rf.cells.length,rf===3?400:144);
     }
  counts[rf+'_'+shape]={correct,incorrect,uncertain,excluded};
  assert.equal(incorrect,0,`Wrong class for ${rf}/${shape}`);
  assert.equal(uncertain,0,`Unexpected abstentions for ${rf}/${shape} benchmark`);
  assert.ok(correct>=1000);
 }
}
for(const rf of [3,5]){
 const tri=M.evaluate({rf,shape:'triangle',roll:0,yaw:0,pitch:0,distance:4});
 const sq=M.evaluate({rf,shape:'square',roll:0,yaw:0,pitch:0,distance:4});
 assert.equal(tri.decision,'triangle');
 assert.equal(sq.decision,'square');
 assert.equal(tri.edges.length,3);
 assert.equal(sq.edges.length,4);
 assert.equal(tri.corners.length,3);
 assert.equal(sq.corners.length,4);
 const cropped=M.evaluate({rf,shape:'square',x:23,y:23,distance:3});
 assert.equal(cropped.decision,'uncertain','Clipped source should not be assigned a confident class');
}
console.log(JSON.stringify(counts,null,2));
console.log('Visual RF two-shape synthetic benchmark passed.');
