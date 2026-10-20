// IA-5 · Lectura y recomendación en vivo (prompts/prompt_lectura_recomendacion_v3.md).
// Recibe sólo métricas ya calculadas por la app, nunca una fila de la base. El prompt se arma acá,
// no en el navegador: el cliente manda números y claves de una lista cerrada, no texto libre.
// La clave vive en Netlify como GROQ_API_KEY; GROQ_MODEL es opcional.

const MODELO = process.env.GROQ_MODEL || 'openai/gpt-oss-120b';

const CLIENTES = {
  fast: { n: 'fast fashion (high street: Zara, H&M, Shein)', prod: '6 semanas', hasta: 2026 },
  medio: { n: 'contemporary (bridge: COS, Massimo Dutti, Arket)', prod: '4 meses', hasta: 2027 },
  premium: { n: 'high fashion (prêt-à-porter de lujo)', prod: '6 meses', hasta: 2028 },
  nicho: { n: 'diseñador emergente (marca de autor)', prod: '3 meses', hasta: 2030 },
};
const ETAPAS = ['Emergente', 'En ascenso', 'Pico', 'Saturada', 'En retorno'];

const num = (v, lo, hi) => (typeof v === 'number' && Number.isFinite(v) && v >= lo && v <= hi ? v : null);
const anio = v => (Number.isInteger(v) && v >= 2000 && v <= 2030 ? v : null);
const pct = v => (v == null ? 'sin dato' : (v > 0 ? '+' : '') + Math.round(v * 100) + ' %');
const dec = v => (v == null ? 'sin dato' : v.toFixed(2).replace('.', ','));
const sig = v => (v == null ? 'sin dato' : (v > 0 ? '+' : '') + v.toFixed(2).replace('.', ','));

const SISTEMA = `Sos analista de tendencias de CICLO. Leés métricas ya calculadas sobre un atributo de moda \
(un color, una estampa, un corte o un material) y decís qué conviene hacer con él.
Reglas:
- Usá sólo los datos que te paso. No inventes cifras, marcas, temporadas ni fuentes.
- Escribí en castellano rioplatense, sin jerga, para diseñadores. Tono directo.
- La frase cita al menos un número de los datos, tal como aparece.
- Respondé sólo con JSON: {"accion": "...", "frase": "..."}.`;

function armarPrompt(d) {
  const c = CLIENTES[d.cliente];
  const acciones = d.vinculo === 'propia' ? 'Entrar, Explorar o Salir' : 'Entrar, Esperar o Salir';
  const quien = d.vinculo === 'propia'
    ? `Diseña por su cuenta para un cliente ${c.n}: no compromete producción ni stock, así que en vez de esperar puede explorar.`
    : `Trabaja para una marca ${c.n}.`;
  return `Cliente: ${quien} Plazo de producción: ${c.prod}. Decide para colecciones hasta ${c.hasta}.

Atributo: ${d.atributo}
Etapa según el K-means: ${d.etapa ?? 'sin etapa'}
Pasarela (Vogue Runway, hasta 2023): nivel ${dec(d.pn)} sobre 1, momento ${sig(d.pm)}, pico en ${d.pico_pas ?? 'sin dato'}
Búsqueda (Google Trends mundo, hasta 2024): nivel ${dec(d.bn)} sobre 1, momento ${sig(d.bm)}, ${d.bus_abierto ? `sigue subiendo (máximo en ${d.pico_bus}, el último año medido)` : `pico en ${d.pico_bus ?? 'sin dato'}`}
Peso en la búsqueda frente a otras de moda, 2023→2025: ${d.terreno == null ? 'sin dato' : (d.terreno > 0 ? '+' : '') + Math.round(d.terreno) + ' puntos'}
Validación: Google Shopping 2022→2025 ${pct(d.shop)}, reseñas de Amazon 2019→2022 ${pct(d.amz)}

Objetivo: una acción (${acciones}) y una sola frase, de menos de 40 palabras, que la justifique con un número de arriba.`;
}

function leer(b) {
  if (!b || typeof b !== 'object') return null;
  const atributo = typeof b.atributo === 'string' ? b.atributo.trim() : '';
  if (!/^[\p{L}\p{N} /\-]{1,40}$/u.test(atributo)) return null;
  if (!CLIENTES[b.cliente] || !['marca', 'propia'].includes(b.vinculo)) return null;
  return {
    atributo,
    cliente: b.cliente,
    vinculo: b.vinculo,
    etapa: ETAPAS.includes(b.etapa) ? b.etapa : null,
    pn: num(b.pn, -1, 2), pm: num(b.pm, -2, 2), bn: num(b.bn, -1, 2), bm: num(b.bm, -2, 2),
    pico_pas: anio(b.pico_pas), pico_bus: anio(b.pico_bus) <= 2024 ? anio(b.pico_bus) : null,
    bus_abierto: b.bus_abierto === true,
    shop: num(b.shop, -1, 20), amz: num(b.amz, -1, 20),
    terreno: num(b.terreno, -100, 100),
  };
}

const json = (o, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });

export default async req => {
  if (req.method !== 'POST') return json({ error: 'Usá POST.' }, 405);
  const clave = process.env.GROQ_API_KEY;
  if (!clave) return json({ error: 'Falta GROQ_API_KEY en Netlify.' }, 503);
  let d;
  try { d = leer(await req.json()); } catch { d = null; }
  if (!d) return json({ error: 'Datos inválidos.' }, 400);

  const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: { authorization: `Bearer ${clave}`, 'content-type': 'application/json' },
    body: JSON.stringify({
      model: MODELO,
      temperature: 0.3,
      max_tokens: 500,
      reasoning_effort: 'low',
      include_reasoning: false,
      response_format: { type: 'json_object' },
      messages: [{ role: 'system', content: SISTEMA }, { role: 'user', content: armarPrompt(d) }],
    }),
  }).catch(() => null);
  if (!r || !r.ok) return json({ error: 'Groq no respondió.', status: r?.status ?? null }, 502);

  let out;
  try { out = JSON.parse((await r.json()).choices[0].message.content); } catch { out = null; }
  const validas = d.vinculo === 'propia' ? ['Entrar', 'Explorar', 'Salir'] : ['Entrar', 'Esperar', 'Salir'];
  const accion = typeof out?.accion === 'string' ? out.accion.trim().replace(/^\w/, ch => ch.toUpperCase()) : '';
  const frase = typeof out?.frase === 'string' ? out.frase.trim().slice(0, 400) : '';
  if (!validas.includes(accion) || !frase) return json({ error: 'La respuesta no tuvo la forma pedida.' }, 502);
  return json({ accion, frase, modelo: MODELO, prompt: 'v3' });
};

export const config = { path: '/api/lectura' };
