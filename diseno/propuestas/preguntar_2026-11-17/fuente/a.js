window.ltVacio=function(){const idx=CLIP.idx;
  return `<div class="pa"><div class="pa-g" id="pa-g"></div>
  <div class="pa-p"><span class="pk">Preguntale por un atributo, una marca o un diseño tuyo · tocá una curva y preguntale por ella</span>${TZ_SUG.map((t,i)=>`<button type="button" class="ltsugb" data-q="${escH(t)}"><i>0${i+1}</i>${escH(t)}</button>`).join('')}</div>
  <div class="pa-l"><span class="pk">O soltá una imagen en cualquier parte · probá con un look de pasarela</span>${LT_EJ.map(([n,k])=>`<button type="button" class="ltejb" data-i="${QEJ[k]}" data-n="${n}">${idx?`<img alt="" src="${vogueFoto(idx.f[QEJ[k]],320)}">`:''}<span>${n}</span></button>`).join('')}</div></div>`;};
window._ter=window._ter||document.getElementById('terreno');
window.propPost=function(){const g=$('#pa-g');if(!g)return;const t=window._ter;if(t&&t.parentNode!==g){g.appendChild(t);}pintarTerreno();moviAnimar();};
