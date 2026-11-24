// CLIP texto→look con filtro de años y diseñador (24/11, vuelta M; desde ciclo/, con transformers.js instalado): node codigo/buscar_look_clip.mjs "<frase>" 2015 2017 [diseñador]
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';
const APP='/Users/felipe/Documents/Ciclo K576/ciclo/app/clip/';
const meta=JSON.parse(fs.readFileSync(APP+'looks.json','utf8'));const Q=new Int8Array(fs.readFileSync(APP+'looks.bin').buffer.slice(0));
const {n,dim,escala}=meta;const [,,fr,y0,y1,dis]=process.argv;
const tok=await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');const model=await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32',{dtype:'fp32'});
const {text_embeds}=await model(tok(['a runway look with '+fr+'.','a photo of '+fr+'.'],{padding:true}));const D=text_embeds.dims[1];const t=new Array(D).fill(0);
for(let k=0;k<2;k++){const v=Array.from(text_embeds.data.slice(k*D,(k+1)*D));const s=Math.hypot(...v);v.forEach((x,j)=>t[j]+=x/s/2);}
const res=[];for(let i=0;i<n;i++){const y=meta.y[i];if(y<+y0||y>+y1)continue;const dn=meta.disenadores[meta.d[i]];if(dis&&!dn.toLowerCase().includes(dis.toLowerCase()))continue;let s=0,q=0;for(let d=0;d<dim;d++){const v=Q[i*dim+d]/escala;s+=v*t[d];q+=v*v;}res.push({f:meta.f[i],d:dn,s:meta.s[i],y,c:s/Math.sqrt(q)});}
res.sort((a,b)=>b.c-a.c);const out=res.slice(0,12);fs.writeFileSync('candidatas_look.json',JSON.stringify({q:out},null,1));console.log(out.map(x=>x.d+' '+x.s+x.y).join(' | '));
