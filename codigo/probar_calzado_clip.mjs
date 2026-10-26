// Prueba (25/10/2026): ¿CLIP lee el calzado en las fotos de pasarela que ya están en app/clip/? Ver decisiones.md.
// Puntúa 10 estilos de calzado contra los 14.000 looks embebidos (sin bajar imágenes), asigna cada look al estilo
// más parecido (softmax ×100 entre estilos) y escribe la cuota por año y los 10 looks más seguros de cada estilo.
// No alimenta la app. Uso (desde la raíz del repo): npm install @huggingface/transformers@3.0.2 &&
//   node codigo/probar_calzado_clip.mjs app <carpeta de salida>
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';
const APP=process.argv[2], S=process.argv[3];
const ATR={
 'Zapatillas':['sneakers','chunky sneakers'],
 'Botinetas':['ankle boots','short heeled ankle boots'],
 'Mocasines':['loafers','penny loafers'],
 'Chatitas':['ballet flats','flat ballerina shoes'],
 'Sandalias':['strappy sandals','flat sandals'],
 'Plataformas':['platform shoes','chunky platform heels'],
 'Guillerminas':['mary jane shoes','mary janes with a strap'],
 'Botas texanas':['cowboy boots','western boots'],
 'Botas altas':['knee-high boots','tall boots'],
 'Stilettos':['stiletto pumps','pointed high heels'],
};
const PL=['a photo of {}.','a runway look with {}.','a fashion photo of a model wearing {}.'];
const tok=await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');
const model=await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32',{dtype:'fp32'});
const norm=v=>{const n=Math.hypot(...v);return v.map(x=>x/n);};
const T=[];
for(const [n,d] of Object.entries(ATR)){const fr=d.flatMap(x=>PL.map(p=>p.replace('{}',x)));const {text_embeds}=await model(tok(fr,{padding:true,truncation:true}));
 const [k,dim]=text_embeds.dims,data=text_embeds.data,m=new Array(dim).fill(0);for(let i=0;i<k;i++){norm(Array.from(data.slice(i*dim,(i+1)*dim))).forEach((x,j)=>m[j]+=x/k);}T.push({n,e:norm(m)});}
const L=JSON.parse(fs.readFileSync(APP+'/clip/looks.json')),B=new Int8Array(fs.readFileSync(APP+'/clip/looks.bin').buffer.slice(0));
const N=L.n,D=L.dim;const sc=T.map(()=>new Float32Array(N));
for(let i=0;i<N;i++){let nq=0;for(let d=0;d<D;d++)nq+=B[i*D+d]**2;nq=Math.sqrt(nq);T.forEach((t,c)=>{let s=0;for(let d=0;d<D;d++)s+=t.e[d]*B[i*D+d];sc[c][i]=s/nq;});}
// softmax con escala 100 entre los estilos; asignación = argmax
const arg=new Int16Array(N),pmax=new Float32Array(N);
for(let i=0;i<N;i++){const z=T.map((_,c)=>100*sc[c][i]),mx=Math.max(...z),e=z.map(x=>Math.exp(x-mx)),s=e.reduce((a,b)=>a+b);let b=0;e.forEach((x,c)=>{if(x>e[b])b=c;});arg[i]=b;pmax[i]=e[b]/s;}
const out={estilos:T.map(t=>t.n),top:{},anual:{}};
T.forEach((t,c)=>{const idx=[...Array(N).keys()].filter(i=>arg[i]===c).sort((a,b)=>pmax[b]-pmax[a]);
 out.top[t.n]=idx.slice(0,10).map(i=>({f:L.f[i],y:L.y[i],d:L.disenadores[L.d[i]],p:+pmax[i].toFixed(2)}));
 out.anual[t.n]={};for(let y=2010;y<=2023;y++){const all=[...Array(N).keys()].filter(i=>L.y[i]===y);out.anual[t.n][y]=+(100*all.filter(i=>arg[i]===c).length/all.length).toFixed(1);}
 out.anual[t.n].n=idx.length;out.anual[t.n].seguros=idx.filter(i=>pmax[i]>=0.5).length;});
fs.writeFileSync(S+'/calzado.json',JSON.stringify(out));
for(const n of out.estilos){const a=out.anual[n];console.log(n.padEnd(14),'n',String(a.n).padStart(5),'p>=.5',String(a.seguros).padStart(5),' 2010',a[2010],' 2015',a[2015],' 2019',a[2019],' 2023',a[2023]);}
