// Arma la fuente de datos del asistente (app/llm/ciclo_datos.md) a partir de las constantes de la app.
// Es el «datos.md» de las demos de la clase, pero para CICLO: no se escribe a mano, se genera, así si cambia
// el K-means o una serie, se vuelve a correr y el asistente queda al día.
// Uso, desde la raíz del repo: node codigo/armar_datos_llm.js
//
// Formato: secciones «## …» y una línea por ítem, con campos separados por « | », como el menú de la
// cafetería. Cada ficha detallada lleva «id:» y «busca:» (sinónimos); netlify/functions/asistente.mjs
// usa eso para mandar al modelo sólo las fichas que nombra la pregunta (el plan gratis de Groq da
// 8.000 tokens por minuto y el documento entero no entra en cada pregunta).

const fs = require('fs');
const s = fs.readFileSync('app/index.html', 'utf8');
const js = s.slice(s.indexOf('<script>') + 8, s.lastIndexOf('</script>'));

function grab(name) { // mismo parser que extraer_series_de_la_app.js
  const key = 'const ' + name + '=';
  const i = js.indexOf(key);
  if (i < 0) throw new Error('falta ' + name);
  let j = i + key.length, depth = 0, inS = false, q = '';
  const st = j;
  for (; j < js.length; j++) {
    const c = js[j];
    if (inS) { if (c === '\\') { j++; continue; } if (c === q) inS = false; continue; }
    if (c === "'" || c === '"' || c === '`') { inS = true; q = c; continue; }
    if (c === '[' || c === '{' || c === '(') depth++;
    else if (c === ']' || c === '}' || c === ')') depth--;
    else if (c === ';' && depth === 0) break;
  }
  return eval('(' + js.slice(st, j) + ')');
}
const [KM, REC, GREL, PERFIL, CONSEJO, DIS, JE, KPROTO, TAX, CALZ_PAS] =
  ['KM', 'REC', 'GREL', 'PERFIL', 'CONSEJO', 'DIS', 'JE', 'KPROTO', 'TAX', 'CALZ_PAS'].map(grab);

// etapa de cada atributo: el mismo código de la app (kClip … kName), con k=4 desde KM.cent
const KST = { asc: { n: 'En ascenso' }, pico: { n: 'Pico' }, sat: { n: 'Saturada' }, ret: { n: 'En retorno' }, emer: { n: 'Emergente' } };
const desde = js.indexOf('const kClip='), hasta = js.indexOf('const KPROTO=');
const nm = js.slice(js.indexOf('function kName('));
const etapas = new Function('KM', 'KST', 'KPROTO', js.slice(desde, hasta) + nm.slice(0, nm.indexOf('\n}\n') + 3) +
  'const P=KM.rows.map(kZ),F=kFit(P,4),N=kName(F.C,4);return KM.rows.map((r,i)=>N[F.L[i]].n);')(KM, KST, KPROTO);
const ETAPA = Object.fromEntries(KM.rows.map((r, i) => [r.n, etapas[i]]));
const ET_IDX = { Emergente: 0, 'En ascenso': 1, Pico: 2, Saturada: 3, 'En retorno': 4 };

// sinónimos para encontrar cada ficha desde la pregunta (en minúscula y sin tildes)
const BUSCA = {
  jamplio: 'baggy, wide leg, barrel, relaxed, jean ancho, jeans anchos, pantalon ancho, jean amplio',
  // mom y boyfriend: alias de búsqueda, no cortes (mom = straight de tiro alto relajado; boyfriend = tapered relajado)
  jmedio: 'jean recto, jeans rectos, straight, bootcut, flare, oxford, tapered, jean medio, mom, boyfriend',
  jajust: 'skinny, chupin, slim, jeggings, jean ajustado, jean al cuerpo',
  buzo: 'buzo, hoodie, canguro, capucha, athleisure, sudadera, sweatshirt',
  cuero: 'cuero, leather, campera de cuero, cuerina, eco cuero',
  lunares: 'lunares, polka dot, topos, puntos',
  floral: 'floral, flores, flor, estampado floral',
  animal: 'animal print, leopardo, leopard, cebra, zebra, serpiente, vaca',
  cargo: 'cargo, bolsillos, utilitario, militar, pantalon cargo',
  encaje: 'encaje, lace, puntilla, transparencia',
  kimono: 'kimono',
  capa: 'capa, cape, poncho',
  trench: 'trench, gabardina, piloto',
  corset: 'corset, corse, bustier',
  rayas: 'rayas, rayado, stripes, marinero, navy',
  gamuza: 'gamuza, suede, ante',
  cuadros: 'cuadros, plaid, tartan, escoces, pata de gallo, cuadrille',
  piel: 'piel, fur, tapado de piel, piel sintetica, peluche',
  y2k: 'y2k, dosmil, 2000, tiro bajo, baby tee, early 2000s',
  blazer: 'blazer, saco, sastrero, oversize, americana',
};
const KM_ID = { 'Jeans baggy': 'jamplio', 'Jeans rectos': 'jmedio', 'Jeans skinny': 'jajust', 'Buzo / hoodie': 'buzo', Floral: 'floral',
  Lunares: 'lunares', Cuero: 'cuero', 'Animal print': 'animal', Kimono: 'kimono', Capa: 'capa', Trench: 'trench', Encaje: 'encaje',
  Cuadros: 'cuadros', Piel: 'piel', Cargo: 'cargo', Y2K: 'y2k', 'Blazer oversize': 'blazer' };

const pct = v => v == null ? 'sin dato' : Math.round(v * 100) + ' %';
const sig = (v, u = '') => v == null ? 'sin dato' : (v > 0 ? '+' : '') + String(Math.round(v)) + u;
const sigp = v => v == null ? 'sin dato' : (v > 0 ? '+' : '') + Math.round(v * 100) + ' %';
const ANIO_BASE = 2024, Y0 = 2004;
const terreno = id => { const v = GREL[id]; return v && v[2024 - Y0] != null && v[2022 - Y0] != null ? v[2024 - Y0] - v[2022 - Y0] : null; };
function picoBusq(o) { // pico de volumen sin 2025, como en la app
  if (!o || !o.g) return null; let mi = -1, my = null;
  o.g.forEach((v, i) => { const y = Y0 + i; if (y <= ANIO_BASE && v != null && v > mi) { mi = v; my = y; } });
  return my == null ? null : (my === ANIO_BASE ? `sigue subiendo (máximo en ${my})` : `pico en ${my}`);
}
function argentina(o) {
  if (!o || !o.a) return null; let mi = -1, my = null;
  o.a.forEach((v, i) => { if (v != null && v > mi) { mi = v; my = Y0 + i; } });
  return my == null ? null : my === 2025 ? 'en Argentina todavía sube (máximo en 2025)' : `en Argentina tocó techo en ${my}`;
}
const recDe = n => REC.find(r => r.n.split(' /')[0] === n.split(' /')[0]);
const L = [];
const linea = (...c) => L.push('- ' + c.filter(Boolean).join(' | '));

// ---------- encabezado (va siempre) ----------
L.push(`# CICLO · datos para el asistente

CICLO es una app de la materia Sistemas generativos e IA para Diseño (UdeSA, 2026). Ubica **atributos** de moda —un color, una estampa, un corte o un material, nunca «una tendencia» entera ni una prenda— en una de cinco etapas de su ciclo de vida, cruzando lo que propone la pasarela con lo que la gente busca. Trabaja sobre todo con ropa; del calzado sólo mide zapatillas y mocasines en la búsqueda, y zapatillas y botas texanas en la pasarela.
Este documento se genera solo a partir de la app (codigo/armar_datos_llm.js). Última versión: ${new Date().toISOString().slice(0, 10)}.

## Cómo leer los números
- Pasarela | fuente: Vogue Runway, 1,28 millones de looks, 2010–2023 | medido | nivel: dónde está 2022–23 contra su propio máximo (100 % = en su pico) | momento: 2021–23 contra 2018–20
- Búsqueda | fuente: Google Trends mundo, dividido por el promedio de 35 términos de moda de cada año | medido | va hasta 2024: en 2025 Google cambió cómo mide y casi todo salta a la vez, 2026 se excluye | nivel: 2023–24 contra su máximo | momento: 2023–24 contra 2020–21
- Peso afuera 2022→2024 | fuente: Google Trends mundo, cada año dividido por la mediana de 16 búsquedas de moda | medido | cuántos puntos gana o pierde frente a las otras búsquedas; corrige el salto de 2025
- Argentina | fuente: Google Trends Argentina | medido | Argentina no tuvo el salto de 2025
- Validación | fuente: Google Shopping 2021–22→2024–25 y reseñas de Amazon 2019→2022 | medido | el modelo no las usa; sirven para ver si acertó
- Etapa | fuente: K-means (k=4) sobre los cuatro números de pasarela y búsqueda | calculado | los grupos los nombramos nosotros por el prototipo más cercano
- Colores, fits, cuellos y mangas | fuente: CLIP leyendo la pasarela 2018–19 contra 2022–23 | interpretación de un modelo, no venta
- Recomendación | fuente: regla fija de CICLO según etapa y perfil | interpretación

## Etapas
- Emergente | casi nadie lo busca todavía pero la pasarela lo empuja | CICLO no lo detecta: la pasarela pública termina en 2023
- En ascenso | sube en pasarela y en búsqueda
- Pico | búsqueda alta, cerca de su máximo, y la pasarela ya no acelera
- Saturada | búsqueda baja o cayendo y la pasarela también: ya lo tiene todo el mercado
- En retorno | vuelve a subir algo que ya tuvo su ciclo`);

// ---------- perfiles y recomendación (el servidor manda sólo la del perfil elegido) ----------
L.push('\n## Perfiles');
for (const [k, p] of Object.entries(PERFIL))
  linea(`${p.n}`, `perfil: ${k}`, p.d, `lead time: ${p.prod}`, `ventana: la prenda tiene que leerse actual ${p.vent} año${p.vent > 1 ? 's' : ''}`,
    `decide hasta: ${p.hasta}`, `error medido a esa distancia: ±${Math.round(p.banda)} puntos`);
L.push('\n## Qué conviene según etapa y perfil');
L.push('Si diseñás por tu cuenta (sin producción ni stock), «Esperar» pasa a ser «Explorar»: podés empezar a diseñarlo ya y decidir la serie cuando la señal se confirme.');
const ETN = ['Emergente', 'En ascenso', 'Pico', 'Saturada', 'En retorno'];
for (const [k, fila] of Object.entries(CONSEJO))
  for (const [e, [acc, por]] of Object.entries(fila)) linea(`${PERFIL[k].n} · ${ETN[e]}`, `perfil: ${k}`, `acción: ${acc}`, `por qué: ${por}`);

// ---------- resumen (va siempre) ----------
L.push('\n## Resumen: todos los atributos');
for (const r of KM.rows) {
  const o = recDe(r.n), d = o ? terreno(o.id) : null;
  linea(r.n, `id: ${KM_ID[r.n]}`, `etapa: ${ETAPA[r.n]}`, `búsqueda: ${pct(r.bn)} de su pico, momento ${sigp(r.bm)}`, d != null ? `afuera 2022→2024: ${sig(d)}` : null);
}
for (const o of REC.filter(o => !KM.rows.some(r => recDe(r.n) === o)))
  linea(o.n, `id: ${o.id}`, 'etapa: sin etapa (no entra al K-means: Vogue no lo etiqueta)', `afuera 2022→2024: ${sig(terreno(o.id))}`);

// ---------- fichas detalladas (sólo las que nombra la pregunta) ----------
L.push('\n## Fichas de atributos');
for (const r of KM.rows) {
  const id = KM_ID[r.n], o = recDe(r.n);
  linea(r.n, `id: ${id}`, `busca: ${BUSCA[id]}`, `tipo: ${r.tipo}`, `etapa: ${ETAPA[r.n]}`,
    `pasarela: ${pct(r.pn)} de su pico, momento ${sigp(r.pm)}, pico en ${r.pico_pas}`,
    `búsqueda: ${pct(r.bn)} de su pico, momento ${sigp(r.bm)}, ${o ? picoBusq(o) : (r.pico_bus === 2024 ? 'sigue subiendo (máximo en 2024)' : 'pico en ' + r.pico_bus)}`,
    o && terreno(o.id) != null ? `afuera 2022→2024: ${sig(terreno(o.id))} puntos` : null, argentina(o),
    `Google Shopping: ${sigp(r.shop_22_25)}`, `reseñas de Amazon: ${sigp(r.amz_19_22)}`,
    o && o.lect ? `lectura: ${o.lect}` : null);
}
for (const o of REC.filter(o => !KM.rows.some(r => recDe(r.n) === o)))
  linea(o.n, `id: ${o.id}`, `busca: ${BUSCA[o.id]}`, `tipo: ${o.tipo}`, 'etapa: sin etapa', `búsqueda: ${picoBusq(o)}`,
    `afuera 2022→2024: ${sig(terreno(o.id))} puntos`, argentina(o), o.lect ? `lectura: ${o.lect}` : null);

// ---------- Diseñar: cortes, fits, cuellos, mangas y colores ----------
L.push('\n## Diseñar: qué conviene en cada prenda');
const Yi = y => JE.Y.indexOf(y), tot = y => Object.values(JE.terms).reduce((a, v) => a + (v[Yi(y)] || 0), 0);
const cuota = (t, y) => (JE.terms[t][Yi(y)] || 0) / tot(y) * 100;
const pts = v => `${v > 0 ? '+' : ''}${v.toFixed(1).replace('.', ',')} puntos`;
const colores = c => c && c.colores ? 'colores (CLIP, pasarela 2022–23 y cambio desde 2018–19): ' + c.colores.slice(0, 4).map(x => `${x.n}: ${Math.round(x.ahora)} %, ${pts(x.cambio)}`).join('; ') : null;
const opciones = (lista, que) => lista ? `${que} (CLIP, % de la pasarela 2022–23 y cambio desde 2018–19): ` +
  lista.map(x => `${x.n}${x.solo ? ' (sólo ' + x.solo + ')' : ''}: ${Math.round(x.ahora)} %, ${pts(x.cambio)}`).join('; ') : null;
// el jean es pantalón + denim; los cortes salen de la taxonomía, con sus alias de búsqueda sumados
const cuotaT = (ts, y) => ts.reduce((a, t) => a + (JE.terms[t] ? cuota(t, y) : 0), 0);
for (const c of TAX.cortes) {
  const busq = c.je ? `búsqueda: ${Math.round(cuotaT(c.je, 2024))} % de las búsquedas de jeans en 2024 (${sig(cuotaT(c.je, 2024) - cuotaT(c.je, 2022))} puntos desde 2022)` : 'sin serie de búsqueda';
  const dj = c.clip_jeans ? DIS.prendas.find(p => p.id === 'jeans').cortes.find(x => x.id === c.clip_jeans) : null;
  linea(`Pantalón largo · ${c.n}`, 'prenda: jeans', `corte: ${c.d}`, c.km ? `atributo: ${c.km} (etapa: ${ETAPA[c.km] || 'sin etapa'})` : null, busq, dj ? colores(dj.color) : null);
}
linea('Tiro', 'prenda: jeans', 'bajo, medio o alto: ninguna fuente de CICLO lo mide, se elige por diseño');
linea('Materiales', 'prenda: materiales', TAX.materiales.map(g => `${g.grupo}: ${g.items.map(i => i.n.toLowerCase()).join(', ')}`).join('; '),
  'con serie medida: cuero y gamuza; cuando el material es denim, la prenda se llama jean (short de jean = short + denim)');
linea('Estampas por material', 'prenda: estampas', Object.entries(TAX.estampa_por_material).map(([g, L]) => `${g}: ${L.join(', ')}`).join('; '),
  'lo que no está en la lista no se produce en ese material (por ejemplo, lunares en denim) y CICLO no lo propone');
for (const p of DIS.prendas.filter(p => p.id !== 'jeans')) {
  for (const c of p.cortes) {
    const busq = p.id === 'jeans' && c.busq && JE.terms[c.busq]
      ? `búsqueda: ${Math.round(cuota(c.busq, 2024))} % de las búsquedas de jeans en 2024 (${sig(cuota(c.busq, 2024) - cuota(c.busq, 2022))} puntos desde 2022)` : null;
    const fit = c.ahora != null ? `fit en la pasarela (CLIP): ${Math.round(c.ahora)} %, ${pts(c.cambio)} desde 2018–19` : null;
    linea(`${p.n} · ${c.n}`, `prenda: ${p.id}`, c.grupo ? `atributo: ${c.grupo} (etapa: ${ETAPA[c.grupo] || 'sin etapa'})` : null, busq, fit, colores(c.color));
  }
  if (p.cuellos || p.mangas || p.color)
    linea(`${p.n} · cuellos, mangas y colores`, `prenda: ${p.id}`, opciones(p.cuellos, 'cuellos'), opciones(p.mangas, 'mangas'), colores(p.color));
}
linea('Estampas', 'prenda: estampas', DIS.estampas.map(e => `${e.n}${e.grupo ? ' (' + (ETAPA[e.grupo] || 'sin etapa') + ')' : ''}`).join(', '));

// ---------- señales de Diseñar: cada hoja de la taxonomía con su serie propia o prestada (sólo las que nombra la pregunta) ----------
L.push('\n## Señales de Diseñar');
L.push('Cada opción de Diseñar con su señal. «propia»: serie de esa hoja; «prestada de»: la de un pariente. id es lo que se usa en "atributos" y "acciones".');
const hojaDe = ref => { const i = ref.indexOf(':'), k = ref.slice(0, i), v = ref.slice(i + 1);
  if (k === 'tipo') { const [pr, t] = v.split('/'); const P = TAX.prendas.find(x => x.id === pr); return P && P.tipos.find(x => x.id === t); }
  if (k === 'corte') return TAX.cortes.find(x => x.id === v); if (k === 'tiro') return TAX.tiros.find(x => x.id === v);
  if (k === 'mat') return TAX.materiales.flatMap(g => g.items).find(x => x.id === v); if (k === 'estampa') return TAX.estampas.flatMap(f => f.items).find(x => x.id === v);
  if (k === 'det') return TAX.detalles.find(x => x.id === v); if (k === 'rec') return { rec: v, n: (REC.find(o => o.id === v) || { n: v }).n }; if (k === 'km') return { km: v, n: v }; return null; };
const serieDe = h => h && (h.serie || h.rec || (h.jeans ? 'jamplio' : null));
const senal = h => { if (h && h.je && h.je.length) { const d = cuotaT(h.je, 2024) - cuotaT(h.je, 2022); return { g: null, d, je: true, et: h.km ? ETAPA[h.km] : null }; }
  const g = serieDe(h); if (!g) return null; const d = h.jeans ? h.jeans.map(terreno).filter(x => x != null).reduce((a, b, _, A) => a + b / A.length, 0) : terreno(g);
  return d == null ? null : { g, d, et: h.km ? ETAPA[h.km] : null }; };
// calzado en la pasarela (CALZ_PAS): frecuencia leída por CLIP, interpretación; nunca da señal
const pasCalzado = id => { const L = CALZ_PAS.lee[id], Y = CALZ_PAS.anios, f = v => v.toFixed(1).replace('.', ',');
  if (!L) return CALZ_PAS.no[id] ? `pasarela: no se puede medir con CLIP (${CALZ_PAS.no[id]})` : null;
  const v = L.v, mx = Math.max(...v);
  return `pasarela (interpretado, CLIP, sin señal): ${f(v[v.length - 1])} % de los looks en ${Y[Y.length - 1]}, ${f(v[0])} % en ${Y[0]}, máximo ${f(mx)} % en ${Y[v.indexOf(mx)]}; lee ${L.lee}`; };
const hojas = [...TAX.prendas.flatMap(p => p.tipos.map(t => ({ eje: 'tipo', paso: 'tipo', prenda: p, h: t, nombre: `${p.n} · ${t.n}` }))),
  ...TAX.cortes.map(h => ({ eje: 'corte', paso: 'corte', h, nombre: `Corte · ${h.n}` })), ...TAX.tiros.map(h => ({ eje: 'tiro', paso: 'tiro', h, nombre: h.n })),
  ...TAX.materiales.flatMap(g => g.items.map(h => ({ eje: 'material', paso: 'material', h, nombre: `Material · ${h.n}` }))),
  ...TAX.detalles.map(h => ({ eje: 'detalle', paso: 'detalle', h, nombre: `Detalle · ${h.n}` })),
  ...TAX.estampas.flatMap(f => f.items.filter(i => i.id !== 'liso').map(h => ({ eje: 'estampa', paso: 'estampa', h, nombre: `Estampa · ${h.n}` })))];
for (const x of hojas) {
  const h = x.h, propia = senal(h), lender = !propia && h.presta_de ? hojaDe(h.presta_de) : null, prest = lender ? senal(lender) : null, q = propia || prest;
  const id = `${x.eje}_${x.prenda ? x.prenda.id + '_' : ''}${h.id}`;
  linea(x.nombre, `id: ${id}`, `busca: ${[h.n, h.en, x.prenda && x.prenda.n].filter(Boolean).join(', ').toLowerCase()}`, `paso: ${x.paso}`, `valor: ${h.id}`,
    q ? `señal: ${sig(q.d)} puntos ${q.je ? 'en su parte de las búsquedas de jeans' : 'en la búsqueda mundial'} 2022→2024` : 'sin dato: ni serie propia ni de un pariente',
    q && q.et ? `etapa: ${q.et}` : null, propia ? 'dato: propio' : prest ? `dato: prestado de ${lender.n.toLowerCase()} (${h.presta_porque})` : null, q && q.g ? `serie: ${q.g}` : null,
    x.prenda && x.prenda.id === 'calzado' ? pasCalzado(h.id) : null);
}

// ---------- límites (va siempre) ----------
L.push(`
## Lo que CICLO no puede responder
- No detecta lo emergente: la pasarela pública llega hasta 2023.
- Calzado: sólo zapatillas y mocasines tienen serie de búsqueda. La pasarela de calzado la lee CLIP (interpretación, sin señal), y sólo sirve para zapatillas y botas texanas.
- No separa hombre y mujer: Vogue y las ventas de H&M mezclan menswear y womenswear.
- No pronostica: de 2025 en adelante sólo muestra la mediana de la historia, con su error.
- La búsqueda llega hasta 2024 (2025 tiene el salto de medición de Google; 2026 se excluye).
- Lyst cambió su fórmula en Q1-26: no se compara a través de ese corte.
- Zara 2018–22 y el mix de marcas son datos sintéticos: sirven para mostrar el método, no para concluir.
- No tiene precios, ventas por marca ni datos de Pinterest, TikTok o Instagram.`);

fs.mkdirSync('app/llm', { recursive: true });
const md = L.join('\n') + '\n';
fs.writeFileSync('app/llm/ciclo_datos.md', md);
console.log('escrito app/llm/ciclo_datos.md ·', md.length, 'caracteres · ~' + Math.round(md.length / 3.5), 'tokens');
