/* Chapter 6 interactive visual ensemble model. Synthetic 3D projected shapes only.
 * Pipeline: rendered pixels -> nonoverlapping RF pooling -> coarse RF-level contour
 * -> convex hull -> 3-vs-4-sided geometric decision -> explanatory edge/corner proxies.
 * NOT an SNN; no learned weights; not an empirical object-recognition result.
 * The source shape is used ONLY by project(), not by classify().
 * Code and text: MIT / CC BY 4.0 as applicable to textbook.
 */
(function(root){
  "use strict";
  var model=(function createModel(){
 const N=60, clamp=(v,a,b)=>Math.max(a,Math.min(b,v)), radians=d=>d*Math.PI/180;
 function project(s){
  const src=s.shape==="square"?[[-.658,-.658],[.658,-.658],[.658,.658],[-.658,.658]]:s.shape==="scalene"?[[-1.2,-.65],[1.1,-.65],[.55,1.1]]:[[-1,-.57735],[1,-.57735],[0,1.1547]];
  const r=radians(s.roll||0),p=radians(s.pitch||0),y=radians(s.yaw||0),cr=Math.cos(r),sr=Math.sin(r),cp=Math.cos(p),sp=Math.sin(p),cy=Math.cos(y),sy=Math.sin(y);
  return src.map(([X,Y])=>{let a=X*cr-Y*sr,b=X*sr+Y*cr;let v=b*cp,z=b*sp;let xx=a*cy+z*sy,zz=-a*sy+z*cy;let q=80/((s.distance||4)+zz);return {x:30+(s.x||0)+xx*q,y:30+(s.y||0)-v*q,z:zz};});
 }
 function inside(x,y,P){let hit=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const a=P[i],b=P[j];if((a.y>y)!==(b.y>y)&&x<(b.x-a.x)*(y-a.y)/(b.y-a.y)+a.x)hit=!hit;}return hit;}
 function raster(P){let im=new Float32Array(N*N);for(let y=0;y<N;y++)for(let x=0;x<N;x++){let hit=0;for(let dy of [.25,.75])for(let dx of [.25,.75])hit+=+inside(x+dx,y+dy,P);im[y*N+x]=hit/4;}return im;}
 function makeRF(im,size){let n=N/size,means=new Float32Array(n*n),cells=[];for(let j=0;j<n;j++)for(let i=0;i<n;i++){let total=0;for(let v=0;v<size;v++)for(let u=0;u<size;u++)total+=im[(j*size+v)*N+i*size+u];means[j*n+i]=total/(size*size);}
  const m=(i,j)=>means[clamp(j,0,n-1)*n+clamp(i,0,n-1)];
  for(let j=0;j<n;j++)for(let i=0;i<n;i++){let gx=m(i+1,j)-m(i-1,j),gy=m(i,j+1)-m(i,j-1);cells.push({x:i*size,y:j*size,cx:(i+.5)*size,cy:(j+.5)*size,mean:m(i,j),edge:clamp(Math.hypot(gx,gy)/1.15,0,1),angle:Math.atan2(gy,gx)});}return {n,size,means,cells};}
 function convexHull(points){let cross=(a,b,c)=>(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);points.sort((a,b)=>a.x-b.x||a.y-b.y);let lo=[],up=[];for(let p of points){while(lo.length>=2&&cross(lo[lo.length-2],lo[lo.length-1],p)<=0)lo.pop();lo.push(p);}for(let i=points.length-1;i>=0;i--){let p=points[i];while(up.length>=2&&cross(up[up.length-2],up[up.length-1],p)<=0)up.pop();up.push(p);}return lo.slice(0,-1).concat(up.slice(0,-1));}
 function area(p){let a=0;for(let i=0;i<p.length;i++){let b=p[(i+1)%p.length];a+=p[i].x*b.y-p[i].y*b.x;}return Math.abs(a)/2;}
 function recover(r){let {n,size,means}=r,m=(i,j)=>means[clamp(j,0,n-1)*n+clamp(i,0,n-1)];
  function f(x,y){let u=x/size-.5,v=y/size-.5,i=Math.floor(u),j=Math.floor(v),a=u-i,b=v-j;return (1-a)*(1-b)*m(i,j)+a*(1-b)*m(i+1,j)+(1-a)*b*m(i,j+1)+a*b*m(i+1,j+1);}
  const mask=new Uint8Array(N*N);let touching=false;
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){let yes=f(x+.5,y+.5)>=.48;mask[y*N+x]=yes?1:0;if(yes&&(x===0||y===0||x===N-1||y===N-1))touching=true;}
  const border=[];for(let y=0;y<N;y++)for(let x=0;x<N;x++)if(mask[y*N+x]&&(x===0||y===0||x===N-1||y===N-1||!mask[y*N+x-1]||!mask[y*N+x+1]||!mask[(y-1)*N+x]||!mask[(y+1)*N+x]))border.push({x:x+.5,y:y+.5});
  return {hull:convexHull(border),touching};}
 function bestTri(h){let max=0,verts=[];for(let i=0;i<h.length-2;i++)for(let j=i+1;j<h.length-1;j++)for(let k=j+1;k<h.length;k++){let a=area([h[i],h[j],h[k]]);if(a>max){max=a;verts=[h[i],h[j],h[k]];}}return {max,verts};}
 function bestQuad(h){let p=h.slice();while(p.length>4){let best=Infinity,idx=0;for(let i=0;i<p.length;i++){let a=p[(i+p.length-1)%p.length],b=p[i],c=p[(i+1)%p.length],loss=Math.abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x));if(loss<best){best=loss;idx=i;}}p.splice(idx,1);}return p;}
 function classify(im,size){let rf=makeRF(im,size),hdata=recover(rf),h=hdata.hull,ha=area(h);
  if(h.length<3||ha<18)return {rf,hull:h,triangle:0,square:0,ratio:0,decision:"uncertain",edges:[],corners:[],touching:hdata.touching};
  const t=bestTri(h),ratio=t.max/ha,decision=hdata.touching?"uncertain":ratio>=.63?"triangle":ratio<=.585?"square":"uncertain";
  const cornersRaw=decision==="square"?bestQuad(h):t.verts,edges=[];
  for(let i=0;i<cornersRaw.length;i++){let a=cornersRaw[i],b=cornersRaw[(i+1)%cornersRaw.length],dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy),w=0;
   for(let c of rf.cells){let q=clamp(((c.cx-a.x)*dx+(c.cy-a.y)*dy)/(len*len),0,1),dist=Math.hypot(c.cx-(a.x+q*dx),c.cy-(a.y+q*dy));if(dist<=size*1.2)w+=c.edge*Math.exp(-dist*dist/(size*size));}
   edges.push({a,b,strength:clamp(w/(len/size)*1.45,0,1)});}
  const corners=cornersRaw.map(v=>{let w=0;for(let c of rf.cells){let d=Math.hypot(c.cx-v.x,c.cy-v.y);w=Math.max(w,c.edge*Math.exp(-d*d/(2*size*size)));}return {x:v.x,y:v.y,strength:clamp(w*1.8,0,1)};});
  return {rf,hull:h,ratio,decision,triangle:clamp((ratio-.585)/.17,0,1),square:clamp((.63-ratio)/.17,0,1),edges,corners,touching:hdata.touching};}
 function evaluate(s){let projected=project(s),image=raster(projected),out=classify(image,s.rf||3);return {...out,projected,image};}
 return {project,raster,makeRF,recover,classify,evaluate,N};
})();
  root.SFNVisualModel=model;
  if(typeof module!=="undefined" && module.exports)module.exports=model;
})(typeof window!=="undefined"?window:globalThis);
