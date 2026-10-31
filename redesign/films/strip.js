// endless strip: three identical lengths; keep the view on the middle one.
// drag pulls the film like through a gate; a click without a drag opens the film
document.querySelectorAll('.strip').forEach(s=>{
  const set=s.querySelector('.set');
  let W=0;
  const measure=()=>{W=set.getBoundingClientRect().width;};
  const wrap=()=>{
    if(!W) return;
    if(s.scrollLeft<W*0.5){s.scrollLeft+=W;l0+=W}
    else if(s.scrollLeft>W*1.5){s.scrollLeft-=W;l0-=W}
  };
  let x0=0,l0=0,moved=false,down=false;
  const start=()=>{measure();s.scrollLeft=W;};
  if(document.readyState==='complete') start(); else addEventListener('load',start);
  addEventListener('resize',()=>{const r=W?s.scrollLeft/W:1;measure();s.scrollLeft=r*W;});
  s.addEventListener('scroll',wrap,{passive:true});
  s.addEventListener('wheel',e=>{if(Math.abs(e.deltaY)>Math.abs(e.deltaX)&&e.shiftKey){s.scrollLeft+=e.deltaY;e.preventDefault()}},{passive:false});
  s.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=false;x0=e.clientX;l0=s.scrollLeft});
  addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-x0;if(Math.abs(dx)>4)moved=true;s.scrollLeft=l0-dx});
  addEventListener('pointerup',()=>{down=false});
  s.addEventListener('click',e=>{if(moved){e.preventDefault();moved=false}});
  s.addEventListener('dragstart',e=>e.preventDefault());
});
