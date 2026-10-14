// Embeddings de texto CLIP (ViT-B/32) para el recorrido «Diseñar»: cortes, colores por prenda, estampas y público.
// Lee codigo/diseno_catalogo.json y escribe textos_diseno.json (intermedio, no se sube).
// Uso (desde la raíz del repo): node codigo/calcular_textos_diseno.mjs salida.json
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';
const C = JSON.parse(fs.readFileSync('codigo/diseno_catalogo.json'));
const sin = s => s.replace(/^(a|an) /, '');
const P = {};
for (const [k, t] of Object.entries(C.publico)) P['publico:' + k] = [t];
for (const pr of C.prendas) for (const c of pr.cortes) {
  P['corte:' + pr.id + ':' + c.id] = [`a runway photo of ${sin(c.en)}`, `a fashion photo of a model wearing ${sin(c.en)}`];
  const cols = pr.colores || C.colores_generales;
  for (const col of cols) P['color:' + pr.id + ':' + c.id + ':' + col.id] = pr.colores ? [`a runway photo of ${col.en}`] : [`a runway photo of a ${col.en} ${sin(c.en)}`];
}
for (const e of C.estampas) P['estampa:' + e.id] = [`a runway photo of clothing with ${sin(e.en)}`, `a fashion photo of ${sin(e.en)}`];
const tok = await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');
const model = await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32', { dtype: 'fp32' });
const norm = v => { const n = Math.hypot(...v); return v.map(x => x / n); };
const out = {};
for (const [k, frases] of Object.entries(P)) {
  const { text_embeds } = await model(tok(frases, { padding: true, truncation: true }));
  const [n, dim] = text_embeds.dims, m = new Array(dim).fill(0);
  for (let i = 0; i < n; i++) norm(Array.from(text_embeds.data.slice(i * dim, (i + 1) * dim))).forEach((x, j) => m[j] += x / n);
  out[k] = norm(m);
}
fs.writeFileSync(process.argv[2], JSON.stringify(out));
console.log(Object.keys(out).length, 'textos');
