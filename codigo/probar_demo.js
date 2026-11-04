// CICLO · la demo de la Entrega 3, paso por paso, como se hace en clase (03/11/2026).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/probar_demo.js [http://localhost:8000/]                → los siete pasos; Preguntar sin llamar a Groq
//   GROQ_KEY=gsk_… node codigo/probar_demo.js [url]                    → además hace la pregunta de verdad
// Requiere: npm install playwright. Sin clave, la llamada a Groq se corta a propósito: así se prueba el plan B (sin
// conexión), y lo que se le mandó al modelo igual queda armado en pantalla. Nunca muestra una respuesta simulada.
// Capturas de cada paso en la carpeta temporal del sistema, ciclo_demo/.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');

const BASE = process.argv[2] || 'http://localhost:8000/';
const KEY = process.env.GROQ_KEY;
const PREGUNTA = '¿Qué color va con un jean baggy?'; // probada con el prompt v5: datasets/pruebas/asistente_v5_respuestas.md
const OUT = path.join(os.tmpdir(), 'ciclo_demo');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1400, height: 900 } })).newPage();
  const errores = []; p.on('pageerror', e => errores.push(e.message));
  if (!KEY) await p.route('**/api.groq.com/**', r => r.abort('internetdisconnected'));
  let n = 0; const ok = [];
  const paso = async (titulo, fn) => {
    n++;
    try { const dice = await fn(); await p.waitForTimeout(400); await p.screenshot({ path: `${OUT}/paso_${n}.png` }); ok.push(true); console.log(`✓ ${n} · ${titulo}${dice ? ' — ' + dice : ''}`); }
    catch (e) { ok.push(false); console.log(`✗ ${n} · ${titulo} — ${e.message.split('\n')[0]}`); }
  };
  await p.goto(BASE, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);

  await paso('Las tres preguntas de entrada', async () => {
    const t = [];
    for (const [sel, v] of [['data-dec', 'producir'], ['data-pub', 'mujer'], ['data-cli', 'premium']]) {
      t.push((await p.$$eval('#ggrid .gt', a => a.map(x => x.textContent))).join(' / '));
      if (await p.$$eval('#ggrid .gd, #ggrid dl', a => a.length)) throw new Error('hay texto de más en las tarjetas');
      await p.click(`#ggrid [${sel}="${v}"]`);
    }
    return t.join(' · ');
  });
  await paso('Tendencias: qué se está moviendo', async () => {
    await p.waitForSelector('#v-radar:not([hidden]) #terreno .tfila, #v-radar:not([hidden]) #terreno', { timeout: 5000 });
    return (await p.textContent('#perfilrad')).replace('Cambiar', '').trim();
  });
  await paso('La ficha de un atributo con el gráfico de su serie', async () => {
    await p.click('#grid >> text=Amplio'); await p.waitForSelector('#v-detalle:not([hidden]) svg');
    return (await p.$$eval('#v-detalle svg', a => a.length)) + ' gráficos';
  });
  await paso('«Diseñar con este…»: el salto con el atributo fijo', async () => {
    const t = (await p.textContent('#v-detalle [data-dz]')).trim();
    await p.click('#v-detalle [data-dz]'); await p.waitForSelector('#dzfijo:not([hidden])');
    return `${t} → ${(await p.textContent('#dzfijo b')).trim()} fijo arriba`;
  });
  await paso('Diseñar: el recorrido con lo elegido acumulado', async () => {
    await p.click('#dzcuerpo >> text=Seguir sin elegir tiro');
    await p.click('#dzcuerpo >> text=Denim rígido');
    await p.waitForTimeout(300);
    return 'barra: ' + (await p.textContent('#dzbarra')).replace(/\s+/g, ' ').trim().slice(0, 90);
  });
  await paso('Preguntar: la pregunta y lo que se le mandó al modelo', async () => {
    await p.click('#nav a[data-v="asistente"]'); await p.waitForTimeout(500);
    const diseno = (await p.textContent('#asdis')).replace(/\s+/g, ' ').trim();
    await p.click('#asclaves'); await p.fill('#askey', KEY || 'gsk_prueba_sin_clave');
    await p.fill('#astexto', PREGUNTA); await p.click('#asenviar');
    await p.waitForFunction(() => !as.ocupado && as.hist.length && as.hist[as.hist.length - 1].role === 'assistant', null, { timeout: 90000 });
    const r = await p.evaluate(() => { const u = as.hist[as.hist.length - 1]; return { r: u.r && u.r.respuesta, error: u.error, enviado: $('#asprompt').textContent.length, leyo: $('#astok').textContent }; });
    await p.click('.asver summary'); // «Qué se le mandó al modelo», abierto
    if (!r.enviado) throw new Error('no se armó lo que se le manda al modelo');
    return `diseño: ${diseno} · ${r.leyo} · ` + (r.r ? 'respuesta: ' + r.r : 'sin Groq, la app dice: ' + r.error);
  });
  await paso('Método: medido contra interpretado', async () => {
    await p.click('#navmas'); await p.click('#nav a[data-v="racional"]').catch(() => p.evaluate(() => mostrar('racional')));
    await p.waitForSelector('#v-racional:not([hidden])');
    return (await p.$$eval('#v-racional .tag', a => [...new Set(a.map(x => x.textContent))].slice(0, 6))).join(' · ');
  });

  console.log(errores.length ? 'errores en la página: ' + errores.join(' | ') : 'sin errores en la página');
  console.log(`${ok.filter(Boolean).length} de ${ok.length} pasos · capturas en ${OUT}`);
  await b.close();
  process.exit(ok.every(Boolean) && !errores.length ? 0 : 1);
})();
