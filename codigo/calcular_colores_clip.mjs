// Embeddings de texto CLIP (ViT-B/32) de los 10 colores de Diseñar, para que Revisión lea el color dominante de una
// imagen (app/clip/colores.json). Mismo modelo que la app; cada color promedia tres frases (prompt ensembling).
// Los vectores del 10/11/2026 se calcularon con este mismo modelo y estas frases en el navegador (transformers.js 3.0.2).
// Uso (desde la raíz del repo): npm install @huggingface/transformers@3.0.2 && node codigo/calcular_colores_clip.mjs
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';

const PLANTILLAS = ['a runway photo of a {} outfit.', 'a model wearing {} clothes.', 'a fashion photo of an all {} look.'];
const COLORES = JSON.parse(fs.readFileSync('codigo/diseno_catalogo.json', 'utf8')).colores_generales;
const prev = JSON.parse(fs.readFileSync('app/clip/colores.json', 'utf8'));
const tok = await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');
const model = await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32', { dtype: 'fp32' });
const out = { ...prev, plantillas: PLANTILLAS, colores: [] };
for (const c of COLORES) {
  const fr = PLANTILLAS.map(t => t.replace('{}', c.en)), { text_embeds } = await model(tok(fr, { padding: true, truncation: true }));
  const d = text_embeds.dims[1], a = new Array(d).fill(0);
  for (let i = 0; i < fr.length; i++) { const v = Array.from(text_embeds.data.slice(i * d, (i + 1) * d)), n = Math.hypot(...v); v.forEach((x, j) => a[j] += x / n); }
  const n = Math.hypot(...a);
  out.colores.push({ id: c.id, n: c.n, en: c.en, hex: c.hex, e: a.map(x => +(x / n).toFixed(5)) });
}
fs.writeFileSync('app/clip/colores.json', JSON.stringify(out));
console.log('escrito app/clip/colores.json ·', out.colores.length, 'colores');
