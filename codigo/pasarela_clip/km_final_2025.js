// K-means con la pasarela hasta 2025 (18/11). Reescala, busca el mejor de 50 arranques (semilla 42) y lo guarda como
// los centroides fijos de k=4: arrancar de los centroides viejos dejaba un óptimo peor (inercia 27,7 contra 23,1).
// Uso (app servida en :8000, cwd con datos/): S=<carpeta con pw/node_modules/playwright> node km_final_2025.js datos/km_C.json
const {chromium}=require(process.env.S+'/pw/node_modules/playwright');const fs=require('fs');
const N=JSON.parse(fs.readFileSync(process.argv[2]));
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('http://localhost:8000/#etapas?c=fast&v=marca&pu=mujer',{waitUntil:'networkidle'});await p.waitForTimeout(800);
const r=await p.evaluate(N=>{
  const antes=(()=>{const P=KM.rows.map(kZ),F=kFit(P,4),Nm=kName(F.C,4);return KM.rows.map((r,i)=>Nm[F.L[i]].n)})();
  KM.rows.forEach(r=>{if(N[r.n])Object.assign(r,N[r.n]);});
  ['pn','pm','bn','bm'].forEach((k,i)=>{const x=KM.rows.map(r=>kClip(r[k],i)),m=x.reduce((a,b)=>a+b,0)/x.length;KM.sc.m[i]=m;KM.sc.s[i]=Math.sqrt(x.reduce((a,b)=>a+(b-m)**2,0)/x.length);});
  const P=KM.rows.map(kZ);
  let B=null;const rnd=kRand(42);for(let i=0;i<50;i++){const f=kLloyd(P,kInit(P,4,rnd));if(!B||f.inertia<B.inertia)B=f}
  KM.cent=B.C.map(c=>c.map(v=>+v.toFixed(4)));
  const F=kFit(P,4);KM.rows.forEach((r,i)=>{r.cl=F.L[i]});const Nm=kName(F.C,4);
  const sil=F=>{const n=P.length;let t=0;for(let i=0;i<n;i++){const own=P.filter((_,j)=>F.L[j]===F.L[i]&&j!==i);const a=own.length?own.reduce((s,q)=>s+Math.sqrt(kD(P[i],q)),0)/own.length:0;let bb=1e9;F.C.forEach((_,g)=>{if(g===F.L[i])return;const o=P.filter((_,j)=>F.L[j]===g);if(o.length)bb=Math.min(bb,o.reduce((s,q)=>s+Math.sqrt(kD(P[i],q)),0)/o.length)});t+=own.length?(bb-a)/Math.max(a,bb):0}return +(t/n).toFixed(3)};
  const old=JSON.parse(JSON.stringify(KM.elbow));const el={};[2,3,4,5,6].forEach(k=>{const f=kFit(P,k);el[k]={inercia:+f.inertia.toFixed(2),sil:sil(f)};});KM.elbow=el;
  return {KM,etapas:KM.rows.map((r,i)=>[r.n,antes[i],Nm[F.L[i]].n]),old,inercia:F.inertia};},N);
fs.writeFileSync('datos/KM_nuevo.json',JSON.stringify(r.KM));
r.etapas.forEach(e=>console.log(e[0].padEnd(16),e[1],e[1]!==e[2]?'→ '+e[2]+' ◀':''));console.log('inercia',r.inercia,'\nelbow viejo',JSON.stringify(r.old),'\nnuevo',JSON.stringify(r.KM.elbow));await b.close();})();
