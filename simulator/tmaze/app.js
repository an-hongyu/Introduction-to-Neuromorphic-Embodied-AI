/* Shared interface. Same-origin /api is optional and never inferred as connected. */
'use strict';
const $=id=>document.getElementById(id),{Engine,WALLS,raycast}=BrainX;
let engine=new Engine(7,600),state=engine.snapshot(),selected=0,speed=4,live=false,busy=false,lastFrame=performance.now(),lastPaint=0,lastPoll=0,frameCount=0,fps=0,lastFps=performance.now(),connectionFailed=false;
const canvases=['mazeCanvas','lidarCanvas','cameraCanvas','ratesCanvas','rasterCanvas'];
const fmt=t=>`${String(Math.floor(t/60)).padStart(2,'0')}:${(t%60).toFixed(1).padStart(4,'0')}`;
const colors={ink:'#23424a',muted:'#91a4ab',teal:'#07877f',line:'#e5edee',red:'#e34e4d',orange:'#e49c46'};
function canvas(id){const c=$(id),r=c.getBoundingClientRect(),ratio=Math.min(window.devicePixelRatio||1,2),w=Math.max(1,r.width),h=Math.max(1,r.height);if(c.width!==Math.round(w*ratio)||c.height!==Math.round(h*ratio)){c.width=Math.round(w*ratio);c.height=Math.round(h*ratio);}const ctx=c.getContext('2d');ctx.setTransform(ratio,0,0,ratio,0,0);ctx.clearRect(0,0,w,h);return {c,ctx,w,h};}
function line(ctx,x1,y1,x2,y2,color,width=1){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();}
function text(ctx,s,x,y,size=9,color=colors.muted,align='left'){ctx.fillStyle=color;ctx.font=`${size}px -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif`;ctx.textAlign=align;ctx.fillText(s,x,y);}
function toast(message){$('toast').textContent=message;$('toast').classList.add('show');setTimeout(()=>$('toast').classList.remove('show'),3000);}
function drawMaze(){
 const {ctx,w,h}=canvas('mazeCanvas'),scale=Math.min((w-55)/8.3,(h-53)/5.6),ox=w/2,oy=h-32-.85*scale,X=x=>ox+x*scale,Y=y=>oy-y*scale;
 document.querySelector('.map-scale span').style.width=scale+'px';
 for(let x=-4;x<=4;x+=.5)line(ctx,X(x),Y(-.85),X(x),Y(4.5),'#eaf0f0');
 for(let y=-.5;y<=4.5;y+=.5)line(ctx,X(-4),Y(y),X(4),Y(y),'#eaf0f0');
 ctx.fillStyle='#fff';ctx.fillRect(X(-.7),Y(4.2),1.4*scale,4.9*scale);ctx.fillRect(X(-3.7),Y(4.2),7.4*scale,1.4*scale);
 for(const c of state.cells||[]){if(c.visits>0){ctx.fillStyle='#c8e7dd';ctx.globalAlpha=.72;ctx.fillRect(X(c.x-.1),Y(c.y+.1),.2*scale,.2*scale);}}ctx.globalAlpha=1;
 for(const [x,y,sx,sy] of WALLS){ctx.fillStyle='#728b92';ctx.fillRect(X(x-sx/2),Y(y+sy/2),sx*scale,sy*scale);ctx.fillStyle='#a4b6ba';ctx.fillRect(X(x-sx/2),Y(y+sy/2),sx*scale,Math.min(2,sy*scale));}
 ctx.fillStyle=colors.red;ctx.fillRect(X(-.425),Y(4.2),.85*scale,Math.max(4,.04*scale));text(ctx,'RED CUE',X(0),Y(4.2)-10,8,colors.red,'center');
 ctx.fillStyle='#f7ecd0';ctx.strokeStyle='#d5b875';ctx.lineWidth=1;ctx.beginPath();ctx.arc(X(3),Y(3.5),.35*scale,0,Math.PI*2);ctx.fill();ctx.stroke();text(ctx,'✦',X(3),Y(3.5)+4,14,'#bd8c31','center');
 text(ctx,'LEFT ARM',X(-2.1),Y(3.5)+25,7,'#96a8ae','center');text(ctx,'RIGHT ARM',X(2.05),Y(3.5)+25,7,'#96a8ae','center');text(ctx,'START',X(0),Y(-.48),7,'#9babb0','center');
 if(state.route?.length){ctx.setLineDash([3,4]);let p=state.pose;for(const q of state.route){line(ctx,X(p[0]),Y(p[1]),X(q[0]),Y(q[1]),'#c0cece',1);p=q;}ctx.setLineDash([]);}
 const tr=state.trajectory||[];if(tr.length>1){ctx.strokeStyle='#128c85';ctx.lineWidth=1.5;ctx.globalAlpha=.7;ctx.beginPath();tr.forEach((p,i)=>i?ctx.lineTo(X(p[1]),Y(p[2])):ctx.moveTo(X(p[1]),Y(p[2])));ctx.stroke();ctx.globalAlpha=1;}
 const [x,y,yaw]=state.pose;if($('showRays').checked){state.ranges.forEach((d,i)=>{if(d===null)return;const a=yaw+i*Math.PI/18;line(ctx,X(x),Y(y),X(x+Math.cos(a)*d),Y(y+Math.sin(a)*d),i===selected?'#e7a041':'#78bfb134',i===selected?1.6:.65);});}
 if(state.target){ctx.strokeStyle='#86a99f';ctx.lineWidth=1;ctx.beginPath();ctx.arc(X(state.target[0]),Y(state.target[1]),4,0,Math.PI*2);ctx.stroke();}
 const bx=X(x),by=Y(y);ctx.save();ctx.translate(bx,by);ctx.rotate(-yaw);ctx.fillStyle='#176762';ctx.strokeStyle='white';ctx.lineWidth=1.2;ctx.beginPath();ctx.roundRect(-.1405*scale,-.153*scale,.281*scale,.306*scale,2);ctx.fill();ctx.stroke();ctx.fillStyle='#b2e5dc';ctx.beginPath();ctx.moveTo(.26*scale,0);ctx.lineTo(.07*scale,-.08*scale);ctx.lineTo(.07*scale,.08*scale);ctx.closePath();ctx.fill();ctx.restore();
 text(ctx,'x (m)',w-15,h-19,7,colors.muted,'right');for(let x=-3;x<=3;x++)text(ctx,x,X(x),h-18,7,colors.muted,'center');
}
function drawLidar(){
 const {ctx,w,h}=canvas('lidarCanvas'),cx=w/2,cy=h/2+2,r=Math.min(w/2-35,h/2-24),maxRange=4;
 for(const n of [1,2,3,4]){ctx.strokeStyle=colors.line;ctx.lineWidth=.8;ctx.beginPath();ctx.arc(cx,cy,r*n/4,0,Math.PI*2);ctx.stroke();text(ctx,`${n}m`,cx+3,cy-r*n/4+7,6,'#a9b8bd');}
 line(ctx,cx-r,cy,cx+r,cy,colors.line);line(ctx,cx,cy-r,cx,cy+r,colors.line);
 for(let i=0;i<36;i++){const a=-Math.PI/2-i*Math.PI/18,d=state.ranges[i],length=d===null?0:Math.min(d,maxRange)/maxRange*r,x=cx+Math.cos(a)*length,y=cy+Math.sin(a)*length;line(ctx,cx,cy,x,y,i===selected?colors.orange:'#309d8c80',i===selected?2:1);if(d!==null){ctx.beginPath();ctx.arc(x,y,i===selected?3.2:1.6,0,Math.PI*2);ctx.fillStyle=i===selected?colors.orange:'#65b6a3';ctx.fill();}}
 text(ctx,'FRONT 0°',cx,13,7,'#7e959d','center');text(ctx,'90°',14,cy+3,7,'#9babb1','center');text(ctx,'270°',w-16,cy+3,7,'#9babb1','center');text(ctx,'180°',cx,h-4,7,'#9babb1','center');ctx.fillStyle='#176762';ctx.beginPath();ctx.arc(cx,cy,5,0,Math.PI*2);ctx.fill();
}
let cameraImage=new Image(),lastCamera=null;
function drawCamera(){
 const {ctx,w,h}=canvas('cameraCanvas');
 if(live){if(state.camera&&state.camera!==lastCamera){lastCamera=state.camera;cameraImage.src=state.camera;}if(cameraImage.complete&&cameraImage.naturalWidth){ctx.drawImage(cameraImage,0,0,w,h);}else{ctx.fillStyle='#e0e7e7';ctx.fillRect(0,0,w,h);text(ctx,'Waiting for Gazebo camera',w/2,h/2,10,colors.muted,'center');}return;}
 ctx.fillStyle='#e3ebed';ctx.fillRect(0,0,w,h/2);ctx.fillStyle='#ccd8d7';ctx.fillRect(0,h/2,w,h/2);const [x,y,yaw]=state.pose,columns=160,cw=w/columns;
 for(let c=0;c<columns;c++){
  const a=(.5-(c+.5)/columns)*1.2,hit=raycast(x+.10*Math.cos(yaw),y+.10*Math.sin(yaw),yaw+a),d=Math.max(.08,hit.d*Math.cos(a)),top=h/2-(.60-.38)/d*h*.80,bottom=h/2+.38/d*h*.80;
  const shade=Math.round(170/(1+d*.10));ctx.fillStyle=`rgb(${shade},${shade+13},${shade+17})`;ctx.fillRect(c*cw,top,cw+1,bottom-top);
  if(hit.wall===3&&Math.abs(hit.x)<.425){const rt=h/2-(.56-.38)/d*h*.80,rb=h/2-(.16-.38)/d*h*.80;ctx.fillStyle=`rgb(${Math.round(222/(1+d*.05))},59,61)`;ctx.fillRect(c*cw,rt,cw+1,rb-rt);}
 }
 const rewardAngle=BrainX.wrap(Math.atan2(3.5-y,3-x)-yaw),rd=Math.hypot(3-x,3.5-y);if(Math.abs(rewardAngle)<.6&&rd>.15){const oc=raycast(x,y,yaw+rewardAngle);if(rd<oc.d+.1){ctx.fillStyle='#d7ad50';ctx.beginPath();ctx.arc(w*(.5-rewardAngle/1.2),h/2+.305/rd*h*.80,Math.max(1,.075/rd*h),0,Math.PI*2);ctx.fill();}}
 line(ctx,w/2-5,h/2,w/2+5,h/2,'#ffffff90');line(ctx,w/2,h/2-5,w/2,h/2+5,'#ffffff90');
}
function drawRates(){
 const {ctx,w,h}=canvas('ratesCanvas'),left=26,bottom=h-19,top=14,cw=(w-left-7)/36;
 for(const f of [0,50,100]){const y=bottom-f/110*(bottom-top);line(ctx,left,y,w-7,y,colors.line);text(ctx,f,left-7,y+3,7,colors.muted,'right');}
 for(let i=0;i<36;i++){
  const x=left+i*cw+cw*.13,bw=cw*.74,rate=Math.min(110,state.rates[i]||0),bh=rate/110*(bottom-top);ctx.fillStyle=i===selected?'#e8a348':'#42a895';ctx.fillRect(x,bottom-bh,bw,bh);
  const ty=bottom-state.targets[i]/110*(bottom-top);line(ctx,x-1,ty,x+bw+1,ty,i===selected?'#91641e':'#7e959c',1.1);
  if(i%3===0)text(ctx,`${i*10}°`,x+bw/2,bottom+14,6,colors.muted,'center');
 }
}
function drawRaster(){
 const {ctx,w,h}=canvas('rasterCanvas'),left=26,top=7,bottom=h-18,width=w-left-7,height=bottom-top,start=Math.max(0,state.time-4),end=start+4;
 for(let i=0;i<=4;i++){const x=left+i*width/4;line(ctx,x,top,x,bottom,colors.line);text(ctx,`${(start+i).toFixed(1)}s`,x,bottom+13,6,colors.muted,i===0?'left':(i===4?'right':'center'));}
 ctx.fillStyle='#f6e7cd';ctx.fillRect(left,top+selected*height/36,width,Math.max(2,height/36));
 for(const n of [0,9,18,27,35])text(ctx,n===35?'35':String(n),left-7,top+(n+.7)*height/36,6,colors.muted,'right');
 for(const [t,i] of state.spikes||[]){if(t<start||t>end)continue;ctx.fillStyle=i===selected?'#bc792b':'#178b7c';ctx.fillRect(left+(t-start)/4*width,top+i*height/36,1,Math.max(1.4,height/36*.7));}
}
function paint(){
 drawMaze();drawLidar();drawCamera();drawRates();drawRaster();drawSpatial();
 const running=state.status==='running',complete=state.status==='complete',error=state.status==='error';
 $('runLabel').textContent=complete?'Run complete':(running?'Pause exploration':(state.time>0?'Resume exploration':'Start exploration'));$('runIcon').textContent=running?'Ⅱ':'▶';$('runButton').disabled=complete||connectionFailed||state.status==='starting';
 $('statusPill').innerHTML=`<i></i> ${connectionFailed?'DISCONNECTED':(error?'ERROR':(complete?'COMPLETE':(running?'EXPLORING':(state.time?'PAUSED':'READY'))))}`;
 $('timeValue').textContent=fmt(state.time);$('timeCaption').textContent=`of ${fmt(state.duration).replace('.0','')}`;$('distanceValue').innerHTML=`${state.path.toFixed(2)} <em>m</em>`;$('coverageValue').innerHTML=`${(state.coverage*100).toFixed(1)} <em>%</em>`;$('coverageCaption').textContent=`${(state.cells||[]).filter(c=>c.visits>0).length} / ${(state.cells||[]).length} grid locations`;$('rewardValue').textContent=state.rewards;
 $('mazeHint').textContent=error?state.error:(complete?'Exploration finished · export or reset to begin again':(running?`Target ${state.targetsVisited+1} · coverage-biased random exploration`:(state.time?'Paused · robot and neural clock are held':'Press start to begin a new exploration')));
 $('neuronName').textContent=`N${String(selected).padStart(2,'0')}`;const names={0:'FRONT',9:'LEFT',18:'REAR',27:'RIGHT'};$('neuronAngle').textContent=`${selected*10}°${names[selected]?' · '+names[selected]:''}`;$('sectorBounds').textContent=`Sector ${selected*10-5}° to ${selected*10+5}°`;
 const d=state.ranges[selected];$('selectedRange').textContent=d===null?'No valid return':`${d.toFixed(2)} m`;$('selectedTarget').textContent=`${state.targets[selected].toFixed(1)} Hz`;$('selectedRate').textContent=`${state.rates[selected].toFixed(0)} Hz`;$('selectedStatus').textContent=state.time<.5?'WARMUP':(state.sectorStatus?.[selected]||state.scanStatus);$('spikeTotal').textContent=`${state.totalSpikes.toLocaleString()} total spikes`;
 $('frameRate').textContent=running?`${fps} display fps${live?' · 5 Hz telemetry':''}`:(complete?'Session complete':'Paused');
}
async function api(command,data={}){if(busy)return;busy=true;try{const r=await fetch('/api/control',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command,...data})});if(!r.ok)throw Error((await r.json()).error||`HTTP ${r.status}`);const d=await r.json();state=d;connectionFailed=false;}catch(e){toast(e.message);}finally{busy=false;paint();}}
$('runButton').onclick=()=>{if(live)api(state.status==='running'?'pause':'start');else{engine.running=!engine.running;state=engine.snapshot();paint();}};
function reset(){const seed=Number($('seedInput').value),duration=Number($('durationInput').value);if(!Number.isInteger(seed)||seed<0||seed>4294967295){toast('Seed must be an integer from 0 to 4294967295');return;}
 if(live)api('reset',{seed,duration});else{engine.reset(seed,duration);state=engine.snapshot();fieldCache.clear();paint();}}
$('resetButton').onclick=reset;$('seedInput').onchange=reset;$('durationInput').onchange=reset;$('speedInput').onchange=()=>{speed=Number($('speedInput').value);};$('showRays').onchange=paint;
$('exportButton').onclick=async()=>{let exportState=state;if(live){try{const r=await fetch('/api/export',{cache:'no-store'});if(!r.ok)throw Error('Export unavailable');exportState=await r.json();}catch(e){toast(e.message);return;}}const record={schema:'brainx-interactive-36-v1',source:state.source,exportedAt:new Date().toISOString(),model:{neurons:36,lidar_neurons:36,grid_neurons:12,place_neurons:18,sectorDegrees:10,tauM:.020,tauRef:.002,dt:.001,rateWindow:.5,rangeRateGain:20,distanceOffset:.05,rateCap:100},...exportState,rasterScope:'Most recent 4 simulated seconds only; full trajectory, aggregate totals and final rates included.'};const blob=new Blob([JSON.stringify(record)],{type:'application/json'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`brainx-${state.source}-seed-${state.seed}-${Math.floor(state.time)}s.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);toast('Session exported · current 4 s raster included');};
$('lidarCanvas').onclick=e=>{const r=e.currentTarget.getBoundingClientRect(),dx=e.clientX-r.left-r.width/2,dy=e.clientY-r.top-r.height/2-2;selected=((Math.round((-Math.atan2(dy,dx)-Math.PI/2)/(Math.PI/18))%36)+36)%36;paint();};
$('ratesCanvas').onclick=e=>{const r=e.currentTarget.getBoundingClientRect();selected=Math.max(0,Math.min(35,Math.floor((e.clientX-r.left-26)/(r.width-33)*36)));paint();};
for(const id of ['lidarCanvas','ratesCanvas'])$(id).onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();selected=(selected+(e.key==='ArrowRight'?1:35))%36;paint();}};
$('methodButton').onclick=()=>$('methodsDialog').showModal();$('closeMethods').onclick=$('closeMethodsBottom').onclick=()=>$('methodsDialog').close();
async function detectBackend(){try{const r=await fetch('/api/state',{cache:'no-store'});if(!r.ok)return;const d=await r.json();if(d.source!=='gazebo')return;live=true;state=d;$('placeSource').disabled=true;$('gridCount').disabled=true;connectionFailed=false;document.title='BrainX · Live Gazebo Neural Lab';$('sourceTitle').textContent='Live Gazebo + ROS';$('sourceDetail').textContent='Actual LaserScan + Nengo LIF';$('sourceNotice').textContent='Connected to the companion Gazebo server. Controls affect this simulation; ranges, camera and spikes come from ROS/Nengo.';$('cameraCaption').textContent='Actual Gazebo camera · 5 Hz';$('footerSource').textContent='Gazebo + ROS 2 + Nengo · 36 sector neurons · known-map navigation';$('speedInput').value='1';$('speedInput').disabled=true;$('speedInput').title='Gazebo physics uses its configured real-time factor; browser playback speed is disabled.';paint();}catch(e){/* Standalone site: browser simulation remains available. */}}
async function poll(){if(!live||busy)return;try{const r=await fetch('/api/state',{cache:'no-store'});if(!r.ok)throw Error('Disconnected');state=await r.json();connectionFailed=false;}catch(e){connectionFailed=true;$('sourceDetail').textContent='Connection lost · controls held';}paint();}
function frame(now){const delta=Math.min(.1,Math.max(0,(now-lastFrame)/1000));lastFrame=now;frameCount++;if(now-lastFps>1000){fps=Math.round(frameCount*1000/(now-lastFps));frameCount=0;lastFps=now;}
 if(!live){engine.advance(delta*speed);state=engine.snapshot();}if(now-lastPaint>65){paint();lastPaint=now;}if(live&&now-lastPoll>200){lastPoll=now;poll();}requestAnimationFrame(frame);}
const spatialConfig=BrainXSpatial.configuration();
$('gridCount').onchange=()=>{if(live){toast('Population switching is available in browser mode only');$('gridCount').value='12';return;}const n=Number($('gridCount').value);engine.setGridCount(n);if(n!==12)$('placeSource').value='pattern';state=engine.snapshot();gridIndex=Math.min(gridIndex,n-1);fieldCache.clear();refreshGridOptions();paint();};
function refreshGridOptions(){const n=state.spatial?.config?.n_grid||12;const el=$('gridCellSelect');el.textContent='';for(let i=0;i<n;i++){const o=document.createElement('option');o.value=i;o.textContent=`G${String(i).padStart(2,'0')}`;el.append(o);}el.value=String(Math.min(gridIndex,n-1));}

$('placeSource').onchange=()=>{if(live){toast('Mapped mode is currently available in the browser model only');$('placeSource').value='reference';return;}if(engine.gridCount!==12&&$('placeSource').value!=='pattern'){toast('24/36 Grid inputs currently use pattern mode');$('placeSource').value='pattern';}engine.setPlaceMode($('placeSource').value);state=engine.snapshot();fieldCache.clear();paint();};let gridIndex=4,placeIndex=5;const fieldCache=new Map();
refreshGridOptions();
for(let i=0;i<18;i++){const o=document.createElement('option');o.value=i;o.textContent=`P${String(i).padStart(2,'0')}`;$('placeCellSelect').append(o);}
$('gridCellSelect').value='4';$('placeCellSelect').value='5';
function fieldColor(value,dim=1){const t=Math.max(0,Math.min(1,value/40)),stops=[[231,242,238],[128,199,163],[23,136,121],[200,164,70]],j=Math.min(2,Math.floor(t*3)),a=t*3-j;return `rgb(${stops[j].map((c,i)=>Math.round(247*(1-dim)+(c+(stops[j+1][i]-c)*a)*dim)).join(',')})`;}
function drawField(id,index){
 const {ctx,w,h}=canvas(id),scale=Math.min((w-45)/8,(h-30)/5.6),ox=(w-8*scale)/2,oy=(h-5.6*scale)/2,X=x=>ox+(x+4)*scale,Y=y=>oy+(4.6-y)*scale,observed=$('spatialMapMode').value==='observed',sp=state.spatial;
 const key=`${id}:${index}:${w}:${h}:${sp?.config?.n_grid||12}:${sp?.place_mode||'reference'}:${observed?Math.floor(state.time*2):'reference'}`;let field=fieldCache.get(key);
 if(!field){field=document.createElement('canvas');field.width=Math.max(1,Math.round(w));field.height=Math.max(1,Math.round(h));const c=field.getContext('2d');c.fillStyle='#f7fafa';c.fillRect(0,0,w,h);
  if(observed){for(const row of sp?.maps||[]){if(row[1]<.05)continue;const ix=row[0]%80,iy=Math.floor(row[0]/80),x=-4+ix*.1,y=-1+iy*.1;c.fillStyle=fieldColor(row[index+2]/row[1]);c.fillRect(X(x),Y(y+.1),.1*scale+.4,.1*scale+.4);}}
  else{for(let iy=0;iy<56;iy++)for(let ix=0;ix<80;ix++){const x=-4+(ix+.5)*.1,y=-1+(iy+.5)*.1,inside=(Math.abs(x)<=.7&&y>=-.7&&y<=4.2)||(Math.abs(x)<=3.7&&y>=2.8&&y<=4.2),ref=BrainXSpatial.rates([x,y]),ng=sp?.config?.n_grid||12,gr=BrainXSpatial.gridPopulationRates([x,y],ng),rate=index<ng?gr[index]:sp?.place_mode==='reference'?ref[index-ng+12]:(sp?.place_mode==='pattern'?BrainXSpatial.patternRates(gr,BrainXSpatial.patternMapping(.4,ng)):sp?.place_mode==='coincidence'?BrainXSpatial.coincidenceRates(gr.slice(0,12)):BrainXSpatial.mappedRates(gr.slice(0,12)))[index-ng];c.fillStyle=fieldColor(rate,inside?1:.24);c.fillRect(X(x-.05),Y(y+.05),.1*scale+.4,.1*scale+.4);}}
  for(const [x,y,sx,sy] of WALLS){c.fillStyle='#819799';c.fillRect(X(x-sx/2),Y(y+sy/2),sx*scale,sy*scale);}
  text(c,'x (m)',w-8,h-5,7,colors.muted,'right');for(const x of [-3,0,3])text(c,x,X(x),h-5,7,colors.muted,'center');
  if(index>=(sp?.config?.n_grid||12)){const p=spatialConfig.place[index-(sp?.config?.n_grid||12)].center_m;c.strokeStyle='#a87826';c.lineWidth=1;const x=X(p[0]),y=Y(p[1]);c.beginPath();c.arc(x,y,5,0,Math.PI*2);c.stroke();line(c,x-8,y,x+8,y,'#a87826');line(c,x,y-8,x,y+8,'#a87826');}
  if(fieldCache.size>12)fieldCache.clear();fieldCache.set(key,field);
 }
 ctx.drawImage(field,0,0,w,h);const [x,y,yaw]=state.pose;ctx.fillStyle='#123c40';ctx.strokeStyle='white';ctx.lineWidth=1;ctx.beginPath();ctx.arc(X(x),Y(y),3.5,0,Math.PI*2);ctx.fill();ctx.stroke();line(ctx,X(x),Y(y),X(x+.23*Math.cos(yaw)),Y(y+.23*Math.sin(yaw)),'#123c40',1.4);
}
function drawMapping(){
 const box=$('mappingPanel');box.style.display=state.spatial?.place_mode!=='reference'?'block':'none';if(box.style.display==='none')return;
 const map=state.spatial?.place_mode==='pattern'?BrainXSpatial.patternMapping(.4,state.spatial.config.n_grid):state.spatial?.place_mode==='coincidence'?BrainXSpatial.COINCIDENCE:BrainXSpatial.MAPPING,{ctx,w,h}=canvas('mappingCanvas'),left=37,top=13,cw=(w-left-8)/(map.weights[0].length),ch=(h-top-25)/18;
 let mx=0;for(const row of map.weights)for(const value of row)mx=Math.max(mx,Math.abs(value));
 for(let p=0;p<18;p++){text(ctx,'P'+String(p).padStart(2,'0'),5,top+(p+.7)*ch,9);for(let g=0;g<map.weights[p].length;g++){const v=map.weights[p][g]/mx,a=Math.abs(v);ctx.fillStyle=v>=0?`rgba(16,130,105,${.12+.88*a})`:`rgba(65,100,210,${.12+.88*a})`;ctx.fillRect(left+g*cw+.5,top+p*ch+.5,cw-1,ch-1);}}
 for(let g=0;g<map.weights[0].length;g++)text(ctx,'G'+String(g).padStart(2,'0'),left+(g+.5)*cw,h-5,8,colors.muted,'center');
 $('mappingInfo').textContent=state.spatial.place_mode==='pattern'?`Full 12-grid template · σ=${map.width} normalized feature units · P${String(placeIndex).padStart(2,'0')} template: ${map.weights[placeIndex].map(v=>v.toFixed(2)).join(', ')} · Offline fixed anchors, no plasticity`:state.spatial.place_mode==='coincidence'?`Thresholded grid coincidence · top ${map.k} afferents per Place cell · selected P${String(placeIndex).padStart(2,'0')} inputs: ${map.weights[placeIndex].map((v,i)=>v?`G${i}`:null).filter(Boolean).join(', ')} · drive threshold ${map.thresholds[placeIndex].toFixed(1)} Hz`:`${map.training_samples} synthetic training points · ridge ${map.ridge} · selected P${String(placeIndex).padStart(2,'0')} weights: ${map.weights[placeIndex].map(v=>v.toFixed(2)).join(', ')} · bias ${map.bias[placeIndex].toFixed(2)}`;
}
function drawSpatial(){
 drawMapping();
 const sp=state.spatial,ng=sp?.config?.n_grid||12,observed=$('spatialMapMode').value==='observed';drawField('gridFieldCanvas',gridIndex);drawField('placeFieldCanvas',ng+placeIndex);
 const g=(sp?.config?.grid||spatialConfig.grid)[gridIndex],p=spatialConfig.place[placeIndex],fmtRate=(a,i)=>`${(a?.[i]||0).toFixed(1)} Hz`;
 $('gridParams').textContent=`Spacing ${g.spacing_m.toFixed(2)} m · axes ${(g.orientation_rad*180/Math.PI).toFixed(0)}° + 0/60/120°`;$('placeParams').textContent=`Center (${p.center_m.map(v=>v.toFixed(2)).join(', ')}) m · σ ${p.sigma_m.toFixed(2)} m`;
 $('gridTarget').textContent=fmtRate(sp?.targets_hz,gridIndex);$('gridObserved').textContent=fmtRate(sp?.rates_hz,gridIndex);$('placeTarget').textContent=fmtRate(sp?.targets_hz,ng+placeIndex);$('placeObserved').textContent=fmtRate(sp?.rates_hz,ng+placeIndex);$('gridName').textContent=`G${String(gridIndex).padStart(2,'0')}`;$('placeName').textContent=`P${String(placeIndex).padStart(2,'0')}`;
 $('spatialMapNote').textContent=observed?'Measured spike count / occupied seconds; gray bins are unvisited or < 0.05 s.':(sp?.place_mode==='reference'?'Gaussian reference field; outside-maze dimmed.':'Predicted mapping from ideal grid rates, not measured spiking; switch to Observed for real spike maps.');$('spatialTotal').textContent=`${(sp?.total_spikes||0).toLocaleString()} spatial spikes`;
 const {ctx,w,h}=canvas('spatialRatesCanvas'),left=30,bottom=h-24,top=9,cw=(w-left-16)/(ng+18);
 for(const rate of [0,20,40]){const y=bottom-rate/50*(bottom-top);line(ctx,left,y,w-13,y,colors.line);text(ctx,rate,left-8,y+3,7,colors.muted,'right');}
 for(let i=0;i<ng+18;i++){const x=left+i*cw+cw*.15,bw=cw*.7,bh=Math.min(50,sp?.rates_hz[i]||0)/50*(bottom-top);ctx.fillStyle=i===gridIndex||i===ng+placeIndex?'#daa04c':(i<ng?'#4a9f9a':'#8bbba7');ctx.fillRect(x,bottom-bh,bw,bh);if(i%3===0||i===ng)text(ctx,(i<ng?'G':'P')+String(i<ng?i:i-ng).padStart(2,'0'),x+bw/2,bottom+14,6,colors.muted,'center');}
}
$('gridCellSelect').onchange=()=>{gridIndex=Number($('gridCellSelect').value);paint();};$('placeCellSelect').onchange=()=>{placeIndex=Number($('placeCellSelect').value);paint();};$('spatialMapMode').onchange=()=>{fieldCache.clear();paint();};$('spatialJump').onclick=()=>$('spatialPanel').scrollIntoView({behavior:'smooth'});

window.addEventListener('resize',paint);document.addEventListener('visibilitychange',()=>{lastFrame=performance.now();if(document.hidden&&!live&&engine.running){engine.running=false;state=engine.snapshot();paint();}});
window.BrainXLab={getState:()=>state,getSelected:()=>selected,engine};paint();detectBackend();requestAnimationFrame(frame);
