// Uso (desde la raíz del repo): npm install @huggingface/transformers@3.0.2 && node codigo/buscar_fotos_clip.mjs → candidatas.json (12 por atributo)
// CLIP texto→look sobre el índice de la app (14.000 looks de Vogue Runway, 2010–2023), para los atributos sin foto.
// Mismo método que FOTO_ATR: varias frases por atributo, promedio normalizado, coseno contra cada look; después, a ojo.
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';
const APP = 'app/clip/'; // desde la raíz del repo
const meta = JSON.parse(fs.readFileSync(APP + 'looks.json', 'utf8'));
const Q = new Int8Array(fs.readFileSync(APP + 'looks.bin').buffer.slice(0));
const { n, dim, escala } = meta;
const ATR = {
  encaje: ['a sheer lace dress', 'black lace fabric', 'a lace top'],
  corset: ['a corset top', 'a structured bustier corset', 'a corset belt over a dress'],
  calzado_zapatillas: ['white sneakers', 'chunky sneakers on the runway', 'athletic trainers shoes'],
  enteritos_jardinero: ['denim overalls', 'dungarees with bib and straps', 'a pinafore overall'],
  fleece: ['a fleece jacket', 'a polar fleece pullover', 'a fuzzy fleece zip-up'],
  poliester: ['a shiny polyester tracksuit', 'synthetic nylon technical fabric', 'a glossy polyester windbreaker'],
  elastano: ['a tight lycra bodysuit', 'stretch spandex leggings', 'a second-skin stretch catsuit'],
  neoprene: ['a neoprene scuba dress', 'a thick neoprene wetsuit-like top', 'bonded scuba fabric'],
  gasa: ['a flowing chiffon dress', 'sheer floaty chiffon', 'a chiffon blouse'],
  tul: ['a tulle skirt', 'a voluminous tulle gown', 'layers of sheer tulle'],
  organza: ['a stiff sheer organza dress', 'transparent organza layers', 'an organza blouse with volume'],
  bordado: ['heavy embroidery', 'an embroidered dress', 'floral embroidery on a jacket'],
  volados: ['ruffles', 'a ruffled dress', 'tiered ruffle flounces'],
  tachas: ['metal studs on a leather jacket', 'studded clothing', 'a studded belt and jacket'],
  flecos: ['fringe', 'a fringed dress', 'a jacket with long fringe'],
  pedreria: ['crystal embellishment', 'a beaded sequin embellished dress', 'rhinestone encrusted gown'],
  espiga: ['a herringbone tweed coat', 'herringbone wool pattern', 'a herringbone suit'],
};
const PL = ['a photo of {}.', 'a runway look with {}.', 'a fashion photo of a model wearing {}.'];
const tok = await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');
const model = await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32', { dtype: 'fp32' });
const norm = v => { const s = Math.hypot(...v); return v.map(x => x / s); };
const out = {};
for (const [id, descs] of Object.entries(ATR)) {
  const fr = descs.flatMap(d => PL.map(p => p.replace('{}', d)));
  const { text_embeds } = await model(tok(fr, { padding: true, truncation: true }));
  const [k, D] = text_embeds.dims, m = new Array(D).fill(0);
  for (let i = 0; i < k; i++) norm(Array.from(text_embeds.data.slice(i * D, (i + 1) * D))).forEach((x, j) => m[j] += x / k);
  const t = norm(m), sc = new Float32Array(n);
  for (let i = 0; i < n; i++) { let s = 0, q = 0; for (let d = 0; d < dim; d++) { const v = Q[i * dim + d] / escala; s += v * t[d]; q += v * v; } sc[i] = s / Math.sqrt(q); }
  const top = [...sc.keys()].sort((a, b) => sc[b] - sc[a]).slice(0, 12);
  out[id] = top.map(i => ({ f: meta.f[i], d: meta.disenadores[meta.d[i]], s: meta.s[i], y: meta.y[i], c: +sc[i].toFixed(4) }));
  console.log(id, out[id].slice(0, 3).map(x => `${x.d} ${x.y} ${x.c}`).join(' | '));
}
fs.writeFileSync('candidatas.json', JSON.stringify(out, null, 1));
