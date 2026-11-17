/* Arma GATE_FOTOS, las fotos de la entrada (17/11). Correr desde la raíz del repo: node codigo/armar_fotos_entrada.js
   1) separa mujer/hombre con una dirección CLIP: promedio de los looks cuyo archivo dice «menswear» (o casa Men/Homme/Uomo)
      menos el de los que dicen women/ready-to-wear/resort/pre-fall; arriba del percentil 93 = hombre, abajo del 45 = mujer
   2) arma cada grupo por casa (una foto por casa, la más reciente) según listas de casas por escala
   3) saca las fotos que vimos a ojo como malas (FUERA: borrosas, láminas de lookbook, una de mujer que caía en hombre)
   Escribe datasets_procesados/entrada_fotos.json; su contenido va en const GATE_FOTOS= de app/index.html */
const fs=require('fs');const R='app/clip/';
const d=JSON.parse(fs.readFileSync(R+'looks.json'));const B=fs.readFileSync(R+'looks.bin');
const N=d.n,K=d.dim;const E=new Float32Array(N*K);for(let i=0;i<N*K;i++)E[i]=B.readInt8(i);
for(let i=0;i<N;i++){let s=0;for(let k=0;k<K;k++)s+=E[i*K+k]**2;s=Math.sqrt(s);for(let k=0;k<K;k++)E[i*K+k]/=s;}
const D=d.disenadores;const des=i=>D[d.d[i]];
const isMen=i=>/mens|menswear|-men-|_men_/i.test(d.f[i])&&!/women/i.test(d.f[i])||/\b(Men|Homme|Uomo)\b/.test(des(i));
const isWom=i=>/women|-rtw-|ready-to-wear|couture|resort|pre-fall/i.test(d.f[i])&&!/men'?s?wear/i.test(d.f[i].replace(/women/ig,''));
const mean=ix=>{const m=new Float32Array(K);ix.forEach(i=>{for(let k=0;k<K;k++)m[k]+=E[i*K+k]});return m.map(v=>v/ix.length)};
const all=[...Array(N).keys()];const M=all.filter(isMen),W=all.filter(isWom);
const mm=mean(M),mw=mean(W);const dir=mm.map((v,k)=>v-mw[k]);
const sc=all.map(i=>{let s=0;for(let k=0;k<K;k++)s+=E[i*K+k]*dir[k];return s});
const sc4=sc.map(v=>+v.toFixed(4));
const S=[...sc4].sort((a,b)=>a-b),q=p=>S[Math.floor(N*p)];
const MUJ=q(0.45),HOM=q(0.93);
const casas={
 lujo:['Prada','Miu Miu','Loewe','Bottega Veneta','Gucci','Chanel','Christian Dior','Valentino','Saint Laurent','Balenciaga','Louis Vuitton','Fendi','Celine','Givenchy','Hermès','Alexander McQueen','Dior Men','Jil Sander','Versace','Burberry'],
 contemp:['Ganni','Acne Studios','Tibi','Sandro','Maje','Theory','Rag & Bone','Vince','Zadig & Voltaire','Staud','Nanushka','A.P.C.','Lacoste','Tommy Hilfiger','Sézane','Rejina Pyo','Proenza Schouler White Label','Our Legacy','Ami','Sies Marjan','Joseph','Paul Smith'],
 fast:['H&M Studio','Topshop Unique','Gap','H&M'],
 street:['Off-White','Fear of God','Palm Angels','Heron Preston','Kith','Martine Rose','A-Cold-Wall','Alyx','Aries','Marcelo Burlon County of Milan','Ambush','Heliot Emil','Kenzo','GmbH','Pyer Moss','Telfar'],
 autor:['Bode','Ahluwalia','Chopova Lowena','Molly Goddard','Collina Strada','Wales Bonner','Simone Rocha','Marine Serre','Ludovic de Saint Sernin','Eckhaus Latta','Vaquera','Charles Jeffrey Loverboy','Craig Green','Kiko Kostadinov','Christopher John Rogers','Rokh','Peter Do','Bianca Saunders','Dilara Findikoglu','Conner Ives','S.S. Daley','Nensi Dojaka','Supriya Lele','Richard Quinn','Paolina Russo','Jacquemus','Kwaidan Editions','Ottolinger'],
 singen:['Telfar','Eckhaus Latta','Ludovic de Saint Sernin','Collina Strada','Marine Serre','Rick Owens','Comme des Garçons','Yohji Yamamoto','Vaquera','Charles Jeffrey Loverboy','Palomo Spain','Gypsy Sport','Craig Green','Maison Margiela','Sunnei','Botter','Y/Project','Marni','Jil Sander','Gucci']};
const usados=new Set();const FUERA=new Set(["62b4992c57e02992012fcf0d/00029-acne-studios-spring-2023-mens-credit-brand.jpg","62a9a7ccd4f5b7cd6aa83fca/00006-staud-resort-2023-credit-brand.jpg","6320c73f563d9de75791b134/00008-parsons-mfa-spring-2023-ready-to-wear-credit-gorunway.jpg","631077bc1c979041e1d8d2a5/00039-hyke-spring-2023-ready-to-wear-tokyo-credit-jun-okada.jpg","5f71ea03c8fe6f7396ad2c5b/00012-Marine-Serre-RTW-SPring-21.jpg","634d6190a4c3c2f8762671c7/00028-heron-preston-spring-2023-ready-to-wear-credit-brand.jpg","6023a66aca559aee6f74a9bf/00007-heron-preston-NEW-FALL-21.jpg"]);
function pool(nom,{casas:cs,gen,ymin=2018,n=14,porCasa=1}){
 const ok=[...Array(N).keys()].filter(i=>d.y[i]>=ymin&&(!cs||cs.includes(des(i)))&&(gen==='m'?sc4[i]<=MUJ:gen==='h'?sc4[i]>=HOM:gen==='x'?(sc4[i]>MUJ&&sc4[i]<HOM):true)&&!usados.has(i)&&!FUERA.has(d.f[i]));
 // diversidad: por casa, el más reciente
 ok.sort((a,b)=>d.y[b]-d.y[a]);const cnt={},out=[];
 for(const i of ok){const c=des(i);if((cnt[c]||0)>=porCasa)continue;cnt[c]=(cnt[c]||0)+1;out.push(i);if(out.length>=n)break;}
 // si faltan, segunda vuelta
 if(out.length<n)for(const i of ok){if(out.includes(i))continue;out.push(i);if(out.length>=n)break;}
 return out.map(i=>[d.f[i],des(i),d.s[i],d.y[i],+sc4[i].toFixed(3)]);
}

const G={m:'m',h:'h',x:null};
const ESC={marca:{premium:casas.lujo,medio:casas.contemp,fast:casas.fast,nicho:casas.autor},propia:{premium:casas.lujo,medio:casas.contemp,fast:casas.street,nicho:casas.autor}};
const T=a=>a.map(x=>[x[0],x[1],x[2],x[3]]);
function pg(o){let r=pool('',o);if(r.length<10&&o.gen){r=r.concat(pool('',{...o,gen:null})).filter((x,i,a)=>a.findIndex(y=>y[0]===x[0])===i).slice(0,o.n||12)}return T(r)}
const P={var:T(pool('',{casas:[...casas.lujo,...casas.autor,...casas.contemp],ymin:2021,n:14})),pub:{},vinc:{},esc:{}};
P.pub.mujer=pg({gen:'m',ymin:2021,n:14});P.pub.hombre=pg({gen:'h',ymin:2019,n:14});P.pub.todos=pg({casas:casas.singen,ymin:2019,n:14,porCasa:2});
for(const g in G){const a=pg({casas:casas.lujo,gen:G[g],ymin:2019,n:5}),b=pg({casas:casas.contemp,gen:G[g],ymin:2019,n:5}),c=pg({casas:casas.fast,gen:G[g],ymin:2010,n:4,porCasa:2});const mz=[];for(let i=0;i<5;i++)[a,b,c].forEach(L=>L[i]&&mz.push(L[i]));
 P.vinc[g]={marca:mz,propia:pg({casas:casas.autor,gen:G[g],ymin:2019,n:14})};
 P.esc[g]={};for(const v in ESC){P.esc[g][v]={};for(const e in ESC[v])P.esc[g][v][e]=pg({casas:ESC[v][e],gen:G[g],ymin:e==='fast'&&v==='marca'?2010:2018,n:12,porCasa:e==='fast'&&v==='marca'?6:1})}}
fs.writeFileSync('datasets_procesados/entrada_fotos.json',JSON.stringify(P));
console.log(JSON.stringify(P).length);
for(const g in G)for(const v in ESC)for(const e in ESC[v])console.log(g,v,e,P.esc[g][v][e].length);
