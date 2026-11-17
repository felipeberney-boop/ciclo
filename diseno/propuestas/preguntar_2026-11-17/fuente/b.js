window.ltVacio=function(){const W=Math.round(innerWidth<=640?innerWidth-32:innerWidth*0.68-48);
  const sel=ids=>ids.map(id=>REC.find(o=>o.id===id)).filter(o=>o&&GREL[o.id]).map(o=>({o,d:terreno(o.id)})).filter(x=>x.d!=null);
  const G=sel(MOVI_SEL.gana).sort((a,b)=>b.d-a.d).slice(0,3);
  const B=[[TZ_SUG[0],'Búsqueda mundial, 2016–2024','Los que más ganaron de 2022 a 2024',`<div class="movg" style="display:block">${moviPanel(G,'Gana terreno','+',W)}</div>`],
    [TZ_SUG[1],'Lyst Index, 2018–2026','Hoy #'+LYST.r.Prada[LYST.q.length-1]+' · fue #1 en 2022–23',tzLyst('Prada',W)],
    [TZ_SUG[2],'Catálogo de Zara, febrero de 2024','No está en Lyst: una foto, no una serie',zaraPieza(W).replace(/^[\s\S]*?(<div class="rvcurv)/,'$1')],
    [TZ_SUG[3],'Búsqueda mundial, 2010–2024','Jeans baggy',rvCurvas([{n:'Jeans baggy',g:'jamplio'}],W)]];
  return `<div class="pb">${B.map(([q,k,dato,g],i)=>`<div class="pb-b ltsugb" role="button" tabindex="0" data-q="${escH(q)}"><div class="pb-t"><span class="pk">0${i+1} · ${k}</span><span class="pb-q">${escH(q)}</span><span class="pk"><b>${dato}</b></span><span class="pb-ir">Preguntar →</span></div><div class="pb-g">${g}</div></div>`).join('')}</div>`;};
window.propPost=function(){$$('.pb-g polyline').forEach(p=>p.setAttribute('pathLength','1'));
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('anim');io.unobserve(e.target);}}),{threshold:.3});$$('.pb-g').forEach(g=>io.observe(g));};
