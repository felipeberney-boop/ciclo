// CICLO · «Preguntale a CICLO» sin pegar una clave (24/11/2026, devolución de la Entrega 4: «En Preguntale no funciona la IA»).
// La app le manda acá lo mismo que le mandaría a Groq (instrucciones, métricas ya calculadas y la pregunta) y esta función
// lo reenvía con la clave del proyecto, que vive en una variable de entorno de Netlify (GROQ_API_KEY), nunca en el repo.
// GET responde si hay clave configurada, para que la app sepa si puede usarla. Sin clave, 503 y la app contesta con reglas.
const GROQ = 'https://api.groq.com/openai/v1/chat/completions';
const MODELOS = new Set(['openai/gpt-oss-120b', 'openai/gpt-oss-20b']);
const ORIGENES = [/^https:\/\/felipeberney-boop\.github\.io$/, /^https:\/\/([a-z0-9-]+--)?ciclo-udesa\.netlify\.app$/, /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/];

const cors = origen => ({
  'access-control-allow-origin': ORIGENES.some(r => r.test(origen || '')) ? origen : 'https://ciclo-udesa.netlify.app',
  'access-control-allow-methods': 'GET, POST, OPTIONS',
  'access-control-allow-headers': 'content-type',
  'access-control-expose-headers': 'retry-after',
  vary: 'origin',
});
const json = (cuerpo, estado, h) => new Response(JSON.stringify(cuerpo), { status: estado, headers: { 'content-type': 'application/json', ...h } });

export default async req => {
  const origen = req.headers.get('origin'), h = cors(origen), clave = process.env.GROQ_API_KEY;
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
  if (origen && !ORIGENES.some(r => r.test(origen))) return json({ error: { message: 'Origen no permitido' } }, 403, h);
  if (req.method === 'GET') return json({ ok: true, clave: !!clave }, 200, h);
  if (req.method !== 'POST') return json({ error: { message: 'Sólo POST' } }, 405, h);
  if (!clave) return json({ error: { message: 'El servidor de CICLO no tiene clave configurada' }, sin_clave: true }, 503, h);

  let b; try { b = await req.json(); } catch { return json({ error: { message: 'Cuerpo inválido' } }, 400, h); }
  if (!MODELOS.has(b.model) || !Array.isArray(b.messages) || b.messages.length > 12) return json({ error: { message: 'Pedido inválido' } }, 400, h);
  if (JSON.stringify(b.messages).length > 60000) return json({ error: { message: 'Pedido demasiado largo' } }, 413, h);
  // sólo pasan los campos que usa la app, con tope de tokens: la clave es del proyecto
  const pedido = { model: b.model, messages: b.messages, temperature: Math.min(1, Math.max(0, +b.temperature || 0.3)), max_tokens: Math.min(900, +b.max_tokens || 700) };
  if (b.response_format && b.response_format.type === 'json_object') pedido.response_format = { type: 'json_object' };
  if (b.model.startsWith('openai/gpt-oss')) Object.assign(pedido, { reasoning_effort: 'low', include_reasoning: false });

  const r = await fetch(GROQ, { method: 'POST', headers: { 'content-type': 'application/json', authorization: 'Bearer ' + clave }, body: JSON.stringify(pedido) });
  const texto = await r.text(), ra = r.headers.get('retry-after');
  return new Response(texto, { status: r.status, headers: { 'content-type': 'application/json', ...h, ...(ra ? { 'retry-after': ra } : {}) } });
};

export const config = { path: '/api/preguntar' };
