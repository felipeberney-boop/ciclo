// CICLO · prueba del chat «Preguntar» con seis preguntas reales (prompt v5, 27/10/2026).
// Uso, desde la raíz del repo, con tu clave de Groq en una variable (no se guarda en ningún archivo):
//   GROQ_KEY=gsk_… node codigo/probar_asistente.js
// Requiere: npm install playwright. Levanta su propio servidor sobre app/, abre la app real, hace cada pregunta como
// la haría una persona y escribe las respuestas en datasets/pruebas/asistente_v5_respuestas.md.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const KEY = process.env.GROQ_KEY;
if (!KEY) { console.error('Falta la clave: GROQ_KEY=gsk_… node codigo/probar_asistente.js'); process.exit(1); }
const PERFIL = '?c=premium&v=marca&pu=mujer';
const PREGUNTAS = [ // [pregunta, diseño armado antes de preguntar (estado de Diseñar en el link) o null]
  ['¿Qué material está de moda ahora?', null],
  ['¿Qué color va con un jean baggy?', 'prenda:pantalones,tipo:largo,corte:baggy,material:denimrigido'],
  ['¿Las botinetas están de moda?', null],
  ['¿Qué va a estar de moda en 2027?', null],
  ['¿Conviene una falda de cuero para una marca high fashion?', 'prenda:faldas,tipo:mini,material:cuero'],
  ['¿Los lunares están volviendo?', null],
];

const TIPOS = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.md': 'text/markdown', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.bin': 'application/octet-stream' };
const raiz = path.resolve('app');
const servidor = http.createServer((q, r) => {
  const f = path.join(raiz, decodeURIComponent(q.url.split('?')[0]).replace(/\/$/, '/index.html'));
  if (!f.startsWith(raiz) || !fs.existsSync(f)) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'content-type': TIPOS[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r);
}).listen(0);

(async () => {
  const base = `http://localhost:${servidor.address().port}/`;
  const b = await chromium.launch();
  const salida = ['# Preguntar · prompt v5 · seis preguntas reales', '',
    `Corrido el ${new Date().toLocaleString('es-AR')} con \`codigo/probar_asistente.js\`, perfil high fashion · para una marca · mujer.`,
    'Cada respuesta es la del modelo, sin editar. Es interpretación: los datos que cita están en `app/llm/ciclo_datos.md`.', ''];
  for (const [i, [pregunta, diseno]] of PREGUNTAS.entries()) {
    if (i) await new Promise(r => setTimeout(r, 65000)); // el plan gratis de Groq da 8.000 tokens por minuto
    const p = await b.newPage();
    await p.goto(base + (diseno ? `#disenar${PERFIL}&dz=${diseno}&paso=color` : `#asistente${PERFIL}`), { waitUntil: 'load' });
    await p.waitForTimeout(1200);
    if (diseno) { await p.click('#nav a[data-v="asistente"]'); await p.waitForTimeout(800); }
    await p.click('#asclaves'); // «Activar el chat»: el campo de la clave está adentro
    await p.fill('#askey', KEY);
    await p.fill('#astexto', pregunta); await p.click('#asenviar');
    await p.waitForFunction(() => !as.ocupado && as.hist.length && as.hist[as.hist.length - 1].role === 'assistant', null, { timeout: 90000 });
    const m = await p.evaluate(() => { const u = as.hist[as.hist.length - 1]; return { r: u.r || null, error: u.error || null, modelo: $('#asmodelo').value, leyo: $('#astok').textContent }; });
    salida.push(`## ${pregunta}`, '', diseno ? `Diseño armado: \`${diseno}\`` : 'Sin diseño armado.', '');
    if (m.error) salida.push(`**Error:** ${m.error}`, '');
    else {
      salida.push(`> ${m.r.respuesta}`, '');
      if (m.r.datos && m.r.datos.length) salida.push('Datos que cita: ' + m.r.datos.join(' · '), '');
      if (m.r.acciones && m.r.acciones.length) salida.push('Acciones: ' + m.r.acciones.map(a => a.texto).join(' · '), '');
      if (m.r.siguiente && m.r.siguiente.length) salida.push('Para seguir: ' + m.r.siguiente.join(' · '), '');
      salida.push(`fuera_de_datos: ${m.r.fuera_de_datos} · acción: ${m.r.accion || '—'} · ${m.leyo}`, '');
    }
    console.log('·', pregunta); await p.close();
  }
  fs.mkdirSync('datasets/pruebas', { recursive: true });
  fs.writeFileSync('datasets/pruebas/asistente_v5_respuestas.md', salida.join('\n'));
  console.log('respuestas en datasets/pruebas/asistente_v5_respuestas.md');
  await b.close(); servidor.close();
})();
