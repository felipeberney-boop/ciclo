// Compara las etapas del K-means con la pasarela de antes y la nueva, usando el código de la app.
// Uso: S=... node kmeans_comparar.js nuevos.json   (nuevos.json: {nombre_fila:{pn,pm,pico_pas}})
const {chromium}=require(process.env.S+'/pw/node_modules/playwright');const fs=require('fs');
const N=JSON.parse(fs.readFileSync(process.argv[2]));
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('http://localhost:8000/#etapas?c=fast&v=marca&pu=mujer',{waitUntil:'networkidle'});await p.waitForTimeout(800);
const r=await p.evaluate(N=>{
  const etapas=()=>{const P=KM.rows.map(kZ),F=kFit(P,4),Nm=kName(F.C,4);return {e:KM.rows.map((r,i)=>Nm[F.L[i]].n),C:F.C};};
  const antes=etapas().e;
  const rows0=JSON.parse(JSON.stringify(KM.rows)),sc0=JSON.parse(JSON.stringify(KM.sc));
  KM.rows.forEach(r=>{if(N[r.n])Object.assign(r,N[r.n]);});
  const cl=(v,i)=>(i===1||i===3)?Math.max(-1,Math.min(1.5,v)):v;
  ['pn','pm','bn','bm'].forEach((k,i)=>{const x=KM.rows.map(r=>cl(r[k],i)),m=x.reduce((a,b)=>a+b,0)/x.length;KM.sc.m[i]=m;KM.sc.s[i]=Math.sqrt(x.reduce((a,b)=>a+(b-m)**2,0)/x.length);});
  const des=etapas();
  return {filas:KM.rows.map((r,i)=>({n:r.n,pn0:rows0[i].pn,pm0:rows0[i].pm,pn:r.pn,pm:r.pm,antes:antes[i],ahora:des.e[i]})),sc:KM.sc,cent:des.C};
},N);
r.filas.forEach(f=>console.log(`${f.n.padEnd(18)} pn ${f.pn0}→${f.pn}  pm ${f.pm0}→${f.pm}  ${f.antes}${f.antes!==f.ahora?'  →  '+f.ahora+'  ◀':''}`));
fs.writeFileSync(process.argv[2].replace('.json','_km.json'),JSON.stringify(r));await b.close();})();
