// CICLO · prueba de «Revisión» (antes «Preguntar») con seis preguntas reales (prompt v9, 10/11/2026; antes v7 y v5).
// Uso, desde la raíz del repo, con tu clave de Groq en una variable (no se guarda en ningún archivo):
//   GROQ_KEY=gsk_… IMAGEN=ruta/a/una/foto.jpg node codigo/probar_asistente.js   (sin IMAGEN, la sexta se saltea)
// Requiere: npm install playwright. Levanta su propio servidor sobre app/, abre la app real, hace cada pregunta como
// la haría una persona y escribe las respuestas en datasets/pruebas/asistente_v9_respuestas.md.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const KEY = process.env.GROQ_KEY;
if (!KEY) { console.error('Falta la clave: GROQ_KEY=gsk_… node codigo/probar_asistente.js'); process.exit(1); }
const PERFIL = '?c=premium&v=marca&pu=mujer';
const PREGUNTAS = [ // [pregunta, diseño armado antes de preguntar (estado de Diseñar en el link) o null, imagen]
  // las seis del pedido de Felipe del 10/11 (prompt v9): marcas, lo que sube, materiales, calzado y una con imagen
  ['¿Cómo están los jeans de Balenciaga?', null],
  ['¿Cómo está Prada?', null],
  ['¿Qué está subiendo más ahora?', null],
  ['¿Qué material está de moda?', null],
  ['¿Las botinetas están de moda?', null],
  ['', null, process.env.IMAGEN], // con imagen y sin pregunta: la app manda «Revisá este diseño: qué está bien y qué cambiarías.»
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
  const salida = ['# Revisión · prompt v9 · seis preguntas reales', '',
    `Corrido el ${new Date().toLocaleString('es-AR')} con \`codigo/probar_asistente.js\`, perfil high fashion · para una marca · mujer.`,
    'Cada respuesta es la del modelo, sin editar. Es interpretación: los datos que cita están en `app/llm/ciclo_datos.md`.', ''];
  for (const [i, [pregunta, diseno, imagen]] of PREGUNTAS.entries()) {
    if (!pregunta && !imagen) { console.log('· sin IMAGEN: se saltea la pregunta con imagen'); continue; }
    if (i) await new Promise(r => setTimeout(r, 65000)); // el plan gratis de Groq da 8.000 tokens por minuto
    const p = await b.newPage();
    await p.goto(base + (diseno ? `#disenar${PERFIL}&dz=${diseno}&paso=color` : `#tiza${PERFIL}`), { waitUntil: 'load' });
    await p.waitForTimeout(1200);
    if (diseno) { await p.click('#nav a[data-v="tiza"]'); await p.waitForTimeout(800); }
    await p.click('#asclaves'); // «Activar el chat»: el campo de la clave está adentro
    await p.fill('#askey', KEY);
    let leido = '';
    if (imagen) { await p.setInputFiles('#asfile', imagen); await p.waitForFunction(() => as.leido, null, { timeout: 300000 });
      leido = await p.evaluate(() => as.clip.map(c => c.n + ' ' + (c.p || 0).toFixed(2)).join(', ')); }
    await p.fill('#astexto', pregunta); await p.click('#asenviar');
    await p.waitForFunction(() => !as.ocupado && as.hist.length && as.hist[as.hist.length - 1].role === 'assistant', null, { timeout: 90000 });
    const m = await p.evaluate(() => { const u = as.hist[as.hist.length - 1]; return { r: u.r || null, error: u.error || null, modelo: $('#asmodelo').value, leyo: $('#astok').textContent }; });
    salida.push(`## ${pregunta || 'Con imagen, sin pregunta: «Revisá este diseño: qué está bien y qué cambiarías.»'}`, '', diseno ? `Diseño armado: \`${diseno}\`` : 'Sin diseño armado.', imagen ? `Imagen: \`${path.basename(imagen)}\` · CLIP leyó: ${leido || 'nada sobre el umbral'}` : '', '');
    if (m.error) salida.push(`**Error:** ${m.error}`, '');
    else {
      salida.push(`**${m.r.accion ? m.r.accion + ' · ' : ''}${m.r.conclusion}**`, '', m.r.respaldo || '(sin respaldo)', '', `Plegado: ${m.r.detalle || '(sin detalle)'}`, '');
      if (m.r.datos && m.r.datos.length) salida.push('Datos que cita: ' + m.r.datos.join(' · '), '');
      if (m.r.acciones && m.r.acciones.length) salida.push('Acciones: ' + m.r.acciones.map(a => a.texto).join(' · '), '');
      if (m.r.siguiente && m.r.siguiente.length) salida.push('Para seguir: ' + m.r.siguiente.join(' · '), '');
      salida.push(`fuera_de_datos: ${m.r.fuera} · palabras: ${m.r.conclusion.split(/\s+/).length} + ${(m.r.respaldo||'').split(/\s+/).length} · acción: ${m.r.accion || '—'} · ${m.leyo}`, '');
    }
    if (process.env.CAPTURAS) await p.locator('#aschat .asa').last().screenshot({ path: path.join(process.env.CAPTURAS, `respuesta_${i + 1}.png`) });
    console.log('·', pregunta); await p.close();
  }
  fs.mkdirSync('datasets/pruebas', { recursive: true });
  fs.writeFileSync('datasets/pruebas/asistente_v9_respuestas.md', salida.join('\n'));
  console.log('respuestas en datasets/pruebas/asistente_v9_respuestas.md');
  await b.close(); servidor.close();
})();
