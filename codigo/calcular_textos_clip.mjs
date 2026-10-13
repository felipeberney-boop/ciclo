// Calcula los embeddings de texto CLIP (ViT-B/32) de los 18 atributos del K-means, para la clasificación
// zero-shot de la Consulta por imagen. Cada atributo promedia varias frases (prompt ensembling).
// Uso (desde la raíz del repo): npm install @huggingface/transformers@3.0.2 && node codigo/calcular_textos_clip.mjs
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';

// nombre exacto de KM.rows → descripciones en inglés (CLIP se entrenó en inglés)
const ATR = {
  'Jeans amplios': ['wide-leg baggy jeans', 'loose baggy denim pants'],
  'Jeans medios': ['straight-leg jeans', 'bootcut flared jeans'],
  'Jeans ajustados': ['skinny jeans', 'tight slim-fit jeans'],
  'Buzo / hoodie': ['a hoodie', 'a sweatshirt'],
  'Floral': ['a floral print', 'a dress with a flower pattern'],
  'Lunares': ['polka dots', 'a polka dot print'],
  'Cuero': ['a leather jacket', 'black leather clothing'],
  'Animal print': ['a leopard print', 'a zebra animal print'],
  'Kimono': ['a kimono jacket', 'a wrap kimono robe'],
  'Capa': ['a cape', 'a cloak worn over the shoulders'],
  'Trench': ['a trench coat', 'a beige belted trench coat'],
  'Encaje': ['lace', 'a sheer lace dress'],
  'Cuadros': ['a plaid check pattern', 'a tartan outfit'],
  'Piel': ['a fur coat', 'a faux fur jacket'],
  'Zapatilla chunky': ['chunky sneakers', 'big dad sneakers'],
  'Cargo': ['cargo pants with utility pockets', 'utilitarian military cargo clothing'],
  'Y2K': ['Y2K early 2000s style outfit', 'low-rise pants and a baby tee'],
  'Blazer oversize': ['an oversized blazer', 'a boxy oversized suit jacket'],
};
const PLANTILLAS = ['a photo of {}.', 'a runway look with {}.', 'a fashion photo of a model wearing {}.'];

const tok = await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');
const model = await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32', { dtype: 'fp32' });
const norm = v => { const n = Math.hypot(...v); return v.map(x => x / n); };
const out = { modelo: 'Xenova/clip-vit-base-patch32 (OpenAI CLIP ViT-B/32)', plantillas: PLANTILLAS, atributos: [] };
for (const [n, descs] of Object.entries(ATR)) {
  const frases = descs.flatMap(d => PLANTILLAS.map(p => p.replace('{}', d)));
  const { text_embeds } = await model(tok(frases, { padding: true, truncation: true }));
  const [k, dim] = text_embeds.dims, data = text_embeds.data, media = new Array(dim).fill(0);
  for (let i = 0; i < k; i++) { const v = norm(Array.from(data.slice(i * dim, (i + 1) * dim))); v.forEach((x, j) => media[j] += x / k); }
  out.atributos.push({ n, frases: descs, e: norm(media).map(x => +x.toFixed(5)) });
}
fs.mkdirSync('app/clip', { recursive: true });
fs.writeFileSync('app/clip/atributos.json', JSON.stringify(out));
console.log(out.atributos.length, 'atributos');
