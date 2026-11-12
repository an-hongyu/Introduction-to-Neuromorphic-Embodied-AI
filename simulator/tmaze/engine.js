/* Browser engineering model: kinematic robot, synthetic ray casts, actual LIF steps.
 * No Gazebo, ROS, Nengo runtime, or associative learning runs in this browser mode.
 */
(function(root){'use strict';
const Spatial=typeof module!=='undefined'&&module.exports?require('./spatial.js'):root.BrainXSpatial;
const TAU=.020, REF=.002, DT=.001, TWO=Math.PI*2;
const SAFE_CENTERS=[[-3.1999999999999997,3.4],[-3.1999999999999997,3.6],[-3.1999999999999997,3.8],[-2.9999999999999996,3.4],[-2.9999999999999996,3.6],[-2.9999999999999996,3.8],[-2.7999999999999994,3.4],[-2.7999999999999994,3.6],[-2.7999999999999994,3.8],[-2.599999999999999,3.4],[-2.599999999999999,3.6],[-2.599999999999999,3.8],[-2.399999999999999,3.4],[-2.399999999999999,3.6],[-2.399999999999999,3.8],[-2.199999999999999,3.4],[-2.199999999999999,3.6],[-2.199999999999999,3.8],[-1.9999999999999987,3.4],[-1.9999999999999987,3.6],[-1.9999999999999987,3.8],[-1.7999999999999985,3.4],[-1.7999999999999985,3.6],[-1.7999999999999985,3.8],[-1.5999999999999983,3.4],[-1.5999999999999983,3.6],[-1.5999999999999983,3.8],[-1.3999999999999981,3.4],[-1.3999999999999981,3.6],[-1.3999999999999981,3.8],[-1.199999999999998,3.4],[-1.199999999999998,3.6],[-1.199999999999998,3.8],[-0.9999999999999978,3.4],[-0.9999999999999978,3.6],[-0.9999999999999978,3.8],[-0.7999999999999976,3.4],[-0.7999999999999976,3.6],[-0.7999999999999976,3.8],[-0.5999999999999974,3.4],[-0.5999999999999974,3.6],[-0.5999999999999974,3.8],[-0.39999999999999725,3.4],[-0.39999999999999725,3.6],[-0.39999999999999725,3.8],[-0.19999999999999707,-0.2],[-0.19999999999999707,0.0],[-0.19999999999999707,0.2],[-0.19999999999999707,0.4000000000000001],[-0.19999999999999707,0.6000000000000001],[-0.19999999999999707,0.8],[-0.19999999999999707,1.0000000000000002],[-0.19999999999999707,1.2000000000000002],[-0.19999999999999707,1.4000000000000001],[-0.19999999999999707,1.6],[-0.19999999999999707,1.8],[-0.19999999999999707,2.0],[-0.19999999999999707,2.2],[-0.19999999999999707,2.4],[-0.19999999999999707,2.6],[-0.19999999999999707,2.8],[-0.19999999999999707,3.0],[-0.19999999999999707,3.2],[-0.19999999999999707,3.4],[-0.19999999999999707,3.6],[-0.19999999999999707,3.8],[3.1086244689504383e-15,-0.2],[3.1086244689504383e-15,0.0],[3.1086244689504383e-15,0.2],[3.1086244689504383e-15,0.4000000000000001],[3.1086244689504383e-15,0.6000000000000001],[3.1086244689504383e-15,0.8],[3.1086244689504383e-15,1.0000000000000002],[3.1086244689504383e-15,1.2000000000000002],[3.1086244689504383e-15,1.4000000000000001],[3.1086244689504383e-15,1.6],[3.1086244689504383e-15,1.8],[3.1086244689504383e-15,2.0],[3.1086244689504383e-15,2.2],[3.1086244689504383e-15,2.4],[3.1086244689504383e-15,2.6],[3.1086244689504383e-15,2.8],[3.1086244689504383e-15,3.0],[3.1086244689504383e-15,3.2],[3.1086244689504383e-15,3.4],[3.1086244689504383e-15,3.6],[3.1086244689504383e-15,3.8],[0.2000000000000033,-0.2],[0.2000000000000033,0.0],[0.2000000000000033,0.2],[0.2000000000000033,0.4000000000000001],[0.2000000000000033,0.6000000000000001],[0.2000000000000033,0.8],[0.2000000000000033,1.0000000000000002],[0.2000000000000033,1.2000000000000002],[0.2000000000000033,1.4000000000000001],[0.2000000000000033,1.6],[0.2000000000000033,1.8],[0.2000000000000033,2.0],[0.2000000000000033,2.2],[0.2000000000000033,2.4],[0.2000000000000033,2.6],[0.2000000000000033,2.8],[0.2000000000000033,3.0],[0.2000000000000033,3.2],[0.2000000000000033,3.4],[0.2000000000000033,3.6],[0.2000000000000033,3.8],[0.40000000000000346,3.4],[0.40000000000000346,3.6],[0.40000000000000346,3.8],[0.6000000000000036,3.4],[0.6000000000000036,3.6],[0.6000000000000036,3.8],[0.8000000000000038,3.4],[0.8000000000000038,3.6],[0.8000000000000038,3.8],[1.000000000000004,3.4],[1.000000000000004,3.6],[1.000000000000004,3.8],[1.2000000000000042,3.4],[1.2000000000000042,3.6],[1.2000000000000042,3.8],[1.4000000000000044,3.4],[1.4000000000000044,3.6],[1.4000000000000044,3.8],[1.6000000000000045,3.4],[1.6000000000000045,3.6],[1.6000000000000045,3.8],[1.8000000000000047,3.4],[1.8000000000000047,3.6],[1.8000000000000047,3.8],[2.000000000000005,3.4],[2.000000000000005,3.6],[2.000000000000005,3.8],[2.200000000000005,3.4],[2.200000000000005,3.6],[2.200000000000005,3.8],[2.4000000000000052,3.4],[2.4000000000000052,3.6],[2.4000000000000052,3.8],[2.6000000000000054,3.4],[2.6000000000000054,3.6],[2.6000000000000054,3.8],[2.8000000000000056,3.4],[2.8000000000000056,3.6],[2.8000000000000056,3.8],[3.0000000000000058,3.4],[3.0000000000000058,3.6],[3.0000000000000058,3.8],[3.200000000000006,3.4],[3.200000000000006,3.6],[3.200000000000006,3.8]];
const WALLS=[[-.76,1.05,.12,3.5],[.76,1.05,.12,3.5],[0,-.76,1.64,.12],[0,4.26,7.64,.12],[-2.2,2.74,3,.12],[2.2,2.74,3,.12],[-3.76,3.5,.12,1.64],[3.76,3.5,.12,1.64]];
const wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
const targetRate=d=>Number.isFinite(d)&&d>=.08&&d<=8?Math.min(100,20/(d+.05)):0;
function inside(p){return (p[0]>=-.7&&p[0]<=.7&&p[1]>=-.7&&p[1]<=4.2)||(p[0]>=-3.7&&p[0]<=3.7&&p[1]>=2.8&&p[1]<=4.2);}
function segmentFree(a,b,margin=.10){
 if(!inside(a)||!inside(b))return false;
 const r=.30+margin;
 for(const [cx,cy,sx,sy] of WALLS){
  let lo=0,hi=1;
  for(let axis=0;axis<2;axis++){
   const c=axis?cy:cx,s=axis?sy:sx,min=c-s/2-r,max=c+s/2+r,delta=b[axis]-a[axis];
   if(Math.abs(delta)<1e-12){if(a[axis]<min||a[axis]>max){lo=2;break;}}
   else {let u=(min-a[axis])/delta,v=(max-a[axis])/delta;if(u>v)[u,v]=[v,u];lo=Math.max(lo,u);hi=Math.min(hi,v);if(lo>hi)break;}
  }
  if(lo<=hi&&lo<=1&&hi>=0)return false;
 }
 return true;
}
function raycast(x,y,angle){
 const dx=Math.cos(angle),dy=Math.sin(angle);let nearest=8,hit=null;
 for(let i=0;i<WALLS.length;i++){
  const [cx,cy,sx,sy]=WALLS[i];let lo=0,hi=8;
  for(const [p,d,c,s] of [[x,dx,cx,sx],[y,dy,cy,sy]]){
   if(Math.abs(d)<1e-12){if(p<c-s/2||p>c+s/2){lo=9;break;}}
   else {let a=(c-s/2-p)/d,b=(c+s/2-p)/d;if(a>b)[a,b]=[b,a];lo=Math.max(lo,a);hi=Math.min(hi,b);}
  }
  if(lo<=hi&&lo<nearest){nearest=lo;hit=i;}
 }
 return {d:nearest,wall:hit,x:x+dx*nearest,y:y+dy*nearest};
}
class Engine{
 constructor(seed=7,duration=600){this.gridCount=12;this.placeMode='reference';this.reset(seed,duration);}
 setGridCount(count){if(![12,24,36].includes(count))throw Error('Grid population must be 12/24/36');this.gridCount=count;if(count!==12)this.placeMode='pattern';this.spatial=new Spatial.Bank(this.placeMode,count);this.spatial.hold([this.x,this.y]);}
 setPlaceMode(mode){if(!['reference','mapped','coincidence','pattern'].includes(mode))throw Error('Invalid place mode');this.placeMode=mode;if(this.gridCount!==12&&mode!=='pattern')throw Error('Expanded grid populations require pattern mode');this.spatial=new Spatial.Bank(mode,this.gridCount);this.spatial.hold([this.x,this.y]);}
 reset(seed=7,duration=600){
  this.seed=Number(seed)>>>0;this.rng=this.seed||0x9e3779b9;this.duration=duration;this.t=0;this.steps=0;this.running=false;this.complete=false;
  this.x=0;this.y=0;this.yaw=Math.PI/2;this.path=0;this.rewards=0;this.rewardInside=false;this.route=[];this.target=null;this.targetsVisited=0;this.armEndsVisited=0;this.armEndArrival=[];
  this.cells=SAFE_CENTERS.map(([x,y])=>({x,y,visits:0,targets:0}));
  this.lastCoverage=null;this.voltage=Array.from({length:36},(_,i)=>i*.95/35);this.refractory=new Array(36).fill(0);this.currents=new Array(36).fill(0);
  this.ranges=new Array(36).fill(null);this.targets=new Array(36).fill(0);this.counts=new Array(36).fill(0);this.windowEvents=Array.from({length:36},()=>[]);this.spikes=[];this.totalSpikes=0;
  this.spatial=new Spatial.Bank(this.placeMode||'reference',this.gridCount||12);this.spatial.hold([0,0]);
  this.trajectory=[[0,0,0,Math.PI/2]];this.coverageHistory=[];this.observeCoverage();this.scan();this.newRoute();return this;
 }
 random(){let a=this.rng+=0x6D2B79F5;a=Math.imul(a^(a>>>15),a|1);a^=a+Math.imul(a^(a>>>7),a|61);return ((a^(a>>>14))>>>0)/4294967296;}
 sample(){for(let i=0;i<10000;i++){const p=[-3.3+6.6*this.random(),-.2+4*this.random()];if(segmentFree(p,p))return p;}throw Error('No safe sample');}
 nearestCell(p){let best=0,cost=Infinity;this.cells.forEach((c,i)=>{const d=distance(p,[c.x,c.y]);if(d<cost){cost=d;best=i;}});return best;}
 newRoute(){
  // Visit both actual arm ends before coverage-biased random exploration.
  // +/-3.25 m leaves clearance for the robot and the end walls at +/-3.76 m.
  if(this.armEndsVisited<2){
   const side=this.armEndsVisited===0?'left':'right';
   const goal=[side==='left'?-3.25:3.25,3.5];
   this.target=goal;
   this.route=[[0,3.5],goal].filter((p,i)=>i>0||distance([this.x,this.y],p)>.08);
   return;
  }
  const start=[this.x,this.y];let candidates=[];for(let i=0;i<48;i++){let p=this.sample();if(distance(start,p)>=1.2){let idx=this.nearestCell(p),c=this.cells[idx];candidates.push({p,idx,score:c.visits+2*c.targets});}}
  if(!candidates.length)return;const min=Math.min(...candidates.map(c=>c.score)),ties=candidates.filter(c=>c.score===min),chosen=ties[Math.floor(this.random()*ties.length)];
  const target=chosen.p,nodes=[start,target];
  for(const y of [.7,1.7,2.6,3.5])nodes.push([-.18+.36*this.random(),y-.12+.24*this.random()]);
  for(const x of [-2.6,-1.5,1.5,2.6])nodes.push([x-.15+.3*this.random(),3.32+.36*this.random()]);
  for(let i=0;i<36;i++)nodes.push(this.sample());
  const costs=new Array(nodes.length).fill(Infinity),prev=new Array(nodes.length).fill(-1),used=new Set();costs[0]=0;
  for(let k=0;k<nodes.length;k++){
   let i=-1;for(let j=0;j<nodes.length;j++)if(!used.has(j)&&(i<0||costs[j]<costs[i]))i=j;
   if(i<0||!Number.isFinite(costs[i]))break;if(i===1)break;used.add(i);
   for(let j=0;j<nodes.length;j++)if(!used.has(j)&&segmentFree(nodes[i],nodes[j],i===0||j===0?.01:.10)){
    const c=costs[i]+distance(nodes[i],nodes[j]);if(c<costs[j]){costs[j]=c;prev[j]=i;}}
  }
  if(prev[1]<0){this.route=[];return;}
  const route=[];for(let i=1;i!==0;i=prev[i])route.unshift(nodes[i]);this.route=route;this.target=target;this.cells[chosen.idx].targets++;
 }
 observeCoverage(){
  if(this.lastCoverage&&distance([this.x,this.y],this.lastCoverage)<.05)return;
  for(const c of this.cells)if(distance([this.x,this.y],[c.x,c.y])<=.2)c.visits++;
  this.lastCoverage=[this.x,this.y];
 }
 scan(){
  for(let i=0;i<36;i++){
   let d=Infinity;for(let offset=-5;offset<5;offset++){const hit=raycast(this.x,this.y,this.yaw+(i*10+offset)*Math.PI/180);if(hit.wall!==null)d=Math.min(d,hit.d);}
   this.ranges[i]=d>=.08&&d<=8?d:null;const f=targetRate(this.ranges[i]);this.targets[i]=f;this.currents[i]=f>0?-1/Math.expm1((REF-1/f)/TAU):0;
  }
 }
 neuralStep(){
  const t=this.steps*DT;
  for(let i=0;i<36;i++){
   this.refractory[i]-=DT;const delta=Math.max(0,Math.min(DT,DT-this.refractory[i])),j=this.currents[i];
   let v=this.voltage[i]-(j-this.voltage[i])*Math.expm1(-delta/TAU);
   if(v>1){const spikeTime=DT+TAU*Math.log1p(-(v-1)/(j-1));this.refractory[i]=REF+spikeTime;v=0;this.counts[i]++;this.totalSpikes++;this.windowEvents[i].push(t);this.spikes.push([t,i]);}
   this.voltage[i]=Math.max(0,v);
  }
 }
 advance(seconds){
  if(!this.running||this.complete)return;
  const n=Math.min(Math.round(seconds/DT),Math.max(0,Math.round((this.duration-this.t)/DT)));
  for(let k=0;k<n;k++){
   if(this.steps%10===0){
    if(!this.route.length)this.newRoute();
    while(this.route.length&&distance([this.x,this.y],this.route[0])<.08){this.route.shift();if(!this.route.length){
      this.targetsVisited++;
      if(this.armEndsVisited<2){
       const side=this.armEndsVisited===0?'left':'right';
       this.armEndArrival.push({side,x:this.x,y:this.y,t:this.steps*DT});
       this.armEndsVisited++;
      }
      this.newRoute();
     }}
    if(this.route.length){const p=this.route[0],error=wrap(Math.atan2(p[1]-this.y,p[0]-this.x)-this.yaw),w=Math.max(-1.3,Math.min(1.3,2.2*error)),v=Math.abs(error)<.30?Math.min(.22,.8*distance([this.x,this.y],p)):0;
     this.yaw=wrap(this.yaw+w*.01);const nx=this.x+Math.cos(this.yaw)*v*.01,ny=this.y+Math.sin(this.yaw)*v*.01;
     if(segmentFree([this.x,this.y],[nx,ny],.02)){this.path+=Math.hypot(nx-this.x,ny-this.y);this.x=nx;this.y=ny;}else this.route=[];
    }
    this.observeCoverage();const r=Math.hypot(this.x-3,this.y-3.5);if(r<.35&&!this.rewardInside){this.rewards++;this.rewardInside=true;}if(r>.5)this.rewardInside=false;
   }
   if(this.steps%100===0)this.scan();if(this.steps%50===0)this.spatial.hold([this.x,this.y]);this.steps++;this.neuralStep();this.spatial.step();this.t=this.steps*DT;
   if(this.steps%50===0)this.trajectory.push([this.t,this.x,this.y,this.yaw]);
   if(this.steps%1000===0)this.coverageHistory.push([this.t,this.coverage()]);
  }
  for(const q of this.windowEvents)while(q.length&&q[0]<=this.t-.5+1e-9)q.shift();
  while(this.spikes.length&&this.spikes[0][0]<this.t-4)this.spikes.shift();
  if(this.t>=this.duration-1e-9){this.complete=true;this.running=false;}
 }
 coverage(){return this.cells.filter(c=>c.visits>0).length/this.cells.length;}
 snapshot(){return {spatial:this.spatial.snapshot(),source:'browser',status:this.complete?'complete':(this.running?'running':'paused'),seed:this.seed,time:this.t,duration:this.duration,pose:[this.x,this.y,this.yaw],path:this.path,rewards:this.rewards,target:this.target,route:this.route,targetsVisited:this.targetsVisited,armEndsVisited:this.armEndsVisited,armEndArrival:this.armEndArrival,coverage:this.coverage(),cells:this.cells,trajectory:this.trajectory,ranges:this.ranges,targets:this.targets,rates:this.windowEvents.map(q=>q.filter(t=>t>this.t-.5+1e-9).length/.5),spikes:this.spikes,totalSpikes:this.totalSpikes,coverageHistory:this.coverageHistory,nNeurons:36,window:.5,scanStatus:'SYNTHETIC',scanAge:0,camera:null};}
}
const api={Engine,WALLS,raycast,segmentFree,targetRate,wrap};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.BrainX=api;
})(typeof window!=='undefined'?window:globalThis);
