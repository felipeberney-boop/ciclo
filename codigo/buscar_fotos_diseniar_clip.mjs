// CLIP texto→look para las opciones de Diseñar sin foto (vuelta M, punto 6). Mismo método que FOTO_ATR (buscar_fotos_clip.mjs).
// Escribe candidatas_diseniar.json con 8 por opción; se eligen a ojo en hojas de contacto. Necesita @huggingface/transformers.
import { AutoTokenizer, CLIPTextModelWithProjection } from '@huggingface/transformers';
import fs from 'fs';
const APP = '/Users/felipe/Documents/Ciclo K576/ciclo/app/clip/';
const meta = JSON.parse(fs.readFileSync(APP + 'looks.json', 'utf8'));
const Q = new Int8Array(fs.readFileSync(APP + 'looks.bin').buffer.slice(0));
const { n, dim, escala } = meta;
const ATR = {
  jersey: ['a soft cotton jersey t-shirt dress', 'draped jersey knit top', 'a fluid jersey outfit'],
  rib: ['a ribbed knit top', 'a rib knit dress', 'ribbed knitwear'],
  frenchterry: ['a french terry sweatshirt', 'a cotton sweatshirt and sweatpants', 'a loopback terry sweat set'],
  pique: ['a pique polo shirt', 'a cotton pique polo', 'a polo shirt with collar'],
  gabardina: ['gabardine twill trousers', 'a twill suit', 'a gabardine trench coat'],
  lona: ['a canvas work jacket', 'heavy cotton canvas workwear', 'a canvas chore coat'],
  denimrigido: ['raw rigid dark denim jeans', 'stiff raw selvedge denim', 'an indigo raw denim jacket'],
  denimelastano: ['tight stretch denim jeans', 'skinny stretch jeans', 'stretch denim leggings'],
  denimlavado: ['light washed denim', 'acid wash jeans', 'faded stonewashed denim jacket'],
  cashmere: ['a soft cashmere sweater', 'a cashmere knit', 'a camel cashmere coat and knit'],
  pano: ['a wool melton overcoat', 'a heavy wool coat', 'a wool felt coat'],
  cuerina: ['a shiny faux leather jacket', 'vinyl pleather pants', 'a glossy faux leather skirt'],
  nylon: ['a nylon windbreaker', 'a shiny nylon jacket', 'technical nylon outfit'],
  acrilico: ['a fuzzy acrylic knit sweater', 'a chunky synthetic knit', 'a colorful acrylic jumper'],
  neoprene: ['a neoprene scuba dress', 'a sculpted scuba fabric dress', 'a thick neoprene top'],
  crepe: ['a fluid crepe dress', 'crepe trousers and blouse', 'a matte crepe gown'],
  liso: ['a plain solid color outfit', 'a minimalist monochrome look', 'a solid color dress with no print'],
  breton: ['a breton striped shirt', 'navy and white horizontal stripes', 'a sailor striped top'],
  pinstripe: ['a pinstripe suit', 'pinstriped trousers', 'a pinstripe blazer'],
  bengal: ['a bengal striped shirt', 'bold vertical candy stripes shirt', 'a striped poplin shirt'],
  awning: ['wide awning stripes', 'bold wide vertical stripes', 'a dress with broad stripes'],
  pindot: ['a tiny pin dot print', 'micro polka dots', 'a pin dot blouse'],
  cuadros: ['a tartan plaid', 'a red tartan skirt', 'a plaid coat'],
  gingham: ['a gingham check dress', 'a gingham shirt', 'small check gingham'],
  pow: ['a prince of wales check suit', 'a glen check blazer', 'a glen plaid coat'],
  windowpane: ['a windowpane check suit', 'a windowpane check coat', 'large windowpane checks'],
  argyle: ['an argyle sweater', 'argyle knit vest', 'argyle diamond pattern'],
  cebra: ['a zebra print', 'a zebra stripe dress', 'zebra print coat'],
  piton: ['a python snakeskin print', 'a snakeskin print dress', 'python print leather'],
  vaca: ['a cow print', 'cow print coat', 'black and white cow spots print'],
  paisley: ['a paisley print', 'a paisley print dress', 'a paisley shirt'],
  toile: ['a toile de jouy print', 'a pastoral toile print dress', 'a monochrome toile print'],
  chevron: ['a chevron zigzag pattern', 'a chevron stripe knit', 'a zigzag print dress'],
  espiga: ['a herringbone tweed coat', 'herringbone wool', 'a herringbone suit'],
  'pantalones/largo': ['full length tailored trousers', 'long straight trousers', 'wide long pants'],
  'pantalones/bermuda': ['bermuda shorts', 'knee length shorts', 'tailored bermuda shorts'],
  'pantalones/capri': ['capri pants', 'cropped capri trousers', 'calf length pants'],
  'faldas/midi': ['a midi skirt', 'a calf length skirt', 'a pleated midi skirt'],
  'remeras/top': ['a crop top', 'a cropped top', 'a strappy top'],
  'camisas/clasica': ['a classic button-down shirt', 'a crisp white shirt', 'a tailored dress shirt'],
  'camisas/oversize': ['an oversized shirt', 'a big boxy oversized shirt', 'an oversized shirt dress'],
  'camisas/cropped': ['a cropped shirt', 'a short cropped button shirt', 'a cropped blouse showing the waist'],
  'buzos/hoodie': ['a hoodie', 'a hooded sweatshirt', 'an oversized hoodie'],
  'buzos/zip': ['a zip-up hoodie', 'a zip sweatshirt jacket', 'a full zip hooded sweatshirt'],
  'buzos/redondo': ['a crewneck sweatshirt', 'a plain crewneck sweatshirt', 'a round neck sweatshirt'],
  'sweaters/redondo': ['a crewneck sweater', 'a round neck knit sweater', 'a knit jumper'],
  'sweaters/cuello_v': ['a v-neck sweater', 'a v neck knit jumper', 'a v-neck cardigan'],
  'abrigos/blazer': ['a blazer', 'a tailored blazer jacket', 'an oversized blazer'],
  'abrigos/tapado': ['a long wool overcoat', 'a long tailored coat', 'a maxi coat'],
  'abrigos/piel': ['a fur coat', 'a faux fur coat', 'a shearling fur coat'],
  'abrigos/puffer': ['a puffer jacket', 'a quilted down puffer coat', 'an oversized puffer'],
  'calzado/botinetas': ['ankle boots', 'leather ankle boots', 'chelsea boots'],
  'calzado/chatitas': ['ballet flats', 'flat ballerina shoes', 'pointed flats'],
  'calzado/sandalias': ['sandals', 'strappy flat sandals', 'leather sandals'],
  'calzado/plataformas': ['platform shoes', 'chunky platform heels', 'platform boots'],
  'calzado/guillerminas': ['mary jane shoes', 'mary janes with strap', 'patent mary jane flats'],
  'calzado/texanas': ['cowboy boots', 'western boots', 'pointed cowboy boots'],
  'accesorios/piluso': ['a bucket hat', 'a fabric bucket hat', 'a wide bucket hat'],
  'accesorios/gorra': ['a baseball cap', 'a cap', 'a baseball hat'],
  'accesorios/cinturon': ['a leather belt', 'a wide belt at the waist', 'a belted look'],
  'accesorios/anteojos': ['sunglasses', 'dark sunglasses', 'oversized sunglasses'],
};
const PL = ['a photo of {}.', 'a runway look with {}.', 'a fashion photo of a model wearing {}.'];
const tok = await AutoTokenizer.from_pretrained('Xenova/clip-vit-base-patch32');
const model = await CLIPTextModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32', { dtype: 'fp32' });
const norm = v => { const s = Math.hypot(...v); return v.map(x => x / s); };
// la norma de cada look, una vez
const nq = new Float32Array(n); for (let i = 0; i < n; i++) { let q = 0; for (let d = 0; d < dim; d++) { const v = Q[i * dim + d] / escala; q += v * v; } nq[i] = Math.sqrt(q); }
const out = {};
for (const [id, descs] of Object.entries(ATR)) {
  const fr = descs.flatMap(d => PL.map(p => p.replace('{}', d)));
  const { text_embeds } = await model(tok(fr, { padding: true, truncation: true }));
  const [k, D] = text_embeds.dims, m = new Array(D).fill(0);
  for (let i = 0; i < k; i++) norm(Array.from(text_embeds.data.slice(i * D, (i + 1) * D))).forEach((x, j) => m[j] += x / k);
  const t = norm(m), sc = new Float32Array(n);
  for (let i = 0; i < n; i++) { let s = 0; for (let d = 0; d < dim; d++) s += (Q[i * dim + d] / escala) * t[d]; sc[i] = s / nq[i]; }
  const top = [...sc.keys()].sort((a, b) => sc[b] - sc[a]).slice(0, 8);
  out[id] = top.map(i => ({ f: meta.f[i], d: meta.disenadores[meta.d[i]], s: meta.s[i], y: meta.y[i], c: +sc[i].toFixed(4) }));
}
fs.writeFileSync('candidatas_diseniar.json', JSON.stringify(out, null, 1));
console.log(Object.keys(out).length, 'listos');
