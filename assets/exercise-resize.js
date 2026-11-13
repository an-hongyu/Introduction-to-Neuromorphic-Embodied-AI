/* Same-origin resizing for the self-contained exercise player. */
(()=>{'use strict';
 const select='iframe[src*="exercise-practice.html"]';
 function prepare(frame){if(frame.dataset.practiceSized)return;frame.dataset.practiceSized='true';frame.style.setProperty('width','100%','important');frame.style.setProperty('height','100%','important');frame.style.setProperty('border','1px solid #d9e4e9','important');frame.style.setProperty('border-radius','12px','important');const wrap=frame.parentElement;wrap.style.setProperty('width','100%','important');wrap.style.setProperty('padding-bottom','0','important');wrap.style.setProperty('height','1080px','important');frame.addEventListener('load',()=>frame.contentWindow?.postMessage({type:'neai-practice-measure'},location.origin));frame.contentWindow?.postMessage({type:'neai-practice-measure'},location.origin);}
 function scan(){document.querySelectorAll(select).forEach(prepare);}
 window.addEventListener('message',event=>{if(event.origin!==location.origin||event.data?.type!=='neai-practice-height')return;const h=event.data.height;if(!Number.isFinite(h)||h<100||h>5000)return;for(const f of document.querySelectorAll(select)){if(f.contentWindow===event.source){prepare(f);f.parentElement.style.setProperty('height',Math.max(380,Math.ceil(h))+'px','important');break;}}});
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',scan);else scan();new MutationObserver(scan).observe(document.documentElement,{childList:true,subtree:true});
})();
