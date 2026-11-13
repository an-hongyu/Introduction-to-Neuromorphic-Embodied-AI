/* Same-origin resizing for the self-contained exercise player. */
(()=>{'use strict';
 const select='iframe[src*="exercise-practice.html"]';
 const style=document.createElement('style');
 style.id='exercise-page-responsive';
 style.textContent=`
 /* Confine theme decorations to the viewport. Wide equations and code retain
    their own horizontal scroll containers; the page scrolls vertically. */
 html.practice-book-page,body.practice-book-page{max-width:100%;overflow-x:clip}
 .practice-book-page main,.practice-book-page article{min-width:0}
 .practice-book-page article h1,.practice-book-page article h2,.practice-book-page article h3,.practice-book-page article h4,.practice-book-page article p,.practice-book-page article li{overflow-wrap:anywhere}
 .practice-book-page article .katex-display{max-width:100%;overflow-x:auto;overflow-y:hidden}
 /* MyST wraps inline KaTeX in an extra span, so direct-child selectors miss it.
    Make each formula a wrapping unit and scroll only formulas wider than it. */
 .practice-book-page article .katex{position:relative;display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle}
 .practice-book-page article .katex-display>.katex{display:block}
 /* Preserve the accessible MathML, but prevent its hidden text from expanding
    the document if the external KaTeX stylesheet loads late or is unavailable. */
 .practice-book-page article .katex .katex-mathml{position:absolute!important;clip:rect(1px,1px,1px,1px)!important;clip-path:inset(50%)!important;width:1px!important;height:1px!important;padding:0!important;border:0!important;overflow:hidden!important;white-space:nowrap!important}
 .practice-book-page article pre{max-width:100%;overflow-x:auto}
 .practice-book-page .exercise-playground{min-width:0;max-width:100%}
 `;
 document.head.appendChild(style);
 function prepare(frame){
  if(frame.dataset.practiceSized)return;
  frame.dataset.practiceSized='true';
  frame.style.setProperty('width','100%','important');
  frame.style.setProperty('height','100%','important');
  frame.style.setProperty('border','1px solid #d9e4e9','important');
  frame.style.setProperty('border-radius','12px','important');
  const wrap=frame.parentElement;
  wrap.style.setProperty('width','100%','important');
  wrap.style.setProperty('min-width','0','important');
  wrap.style.setProperty('padding-bottom','0','important');
  wrap.style.setProperty('height','1080px','important');
  frame.addEventListener('load',()=>frame.contentWindow?.postMessage({type:'neai-practice-measure'},location.origin));
  frame.contentWindow?.postMessage({type:'neai-practice-measure'},location.origin);
 }
 function scan(){
  const isExercise=location.pathname.includes('/exercises/');
  document.documentElement.classList.toggle('practice-book-page',isExercise);
  document.body?.classList.toggle('practice-book-page',isExercise);
  document.querySelectorAll(select).forEach(prepare);
 }
 window.addEventListener('message',event=>{
  if(event.origin!==location.origin||event.data?.type!=='neai-practice-height')return;
  const h=event.data.height;if(!Number.isFinite(h)||h<100||h>5000)return;
  for(const f of document.querySelectorAll(select)){
   if(f.contentWindow===event.source){prepare(f);f.parentElement.style.setProperty('height',Math.max(380,Math.ceil(h))+'px','important');break;}
  }
 });
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();
 new MutationObserver(scan).observe(document.documentElement,{childList:true,subtree:true});
})();
