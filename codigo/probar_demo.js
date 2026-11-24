// CICLO · la demo de la Entrega 4, paso por paso (24/11: arranca en el home y crea un proyecto), como se hace en clase (16/11/2026; la de la Entrega 3 está en git).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/probar_demo.js [http://localhost:8000/]            → sin clave: Preguntale a CICLO tiene que decir clara la falta de clave
//   GROQ_KEY=gsk_… node codigo/probar_demo.js [url]                → además hace la pregunta de verdad y la lectura escrita
//   IMAGEN=ruta/a/una/foto.jpg …                                   → suelta esa foto (si no, usa el look de ejemplo «Denim»)
//   ANCHO=393 …                                                    → la misma demo en el celular
// Requiere: npm install playwright. Nunca muestra una respuesta simulada. Capturas de cada paso en <tmp>/ciclo_demo/.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');

const BASE = process.argv[2] || 'http://localhost:8000/';
const KEY = process.env.GROQ_KEY, IMAGEN = process.env.IMAGEN, ANCHO = +(process.env.ANCHO || 1400);
const PREGUNTA = '¿Qué material le va a un jean baggy?'; // una de las sugerencias fijas: se toca, no se tipea
const OUT = path.join(os.tmpdir(), 'ciclo_demo');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const p = await (await b.newContext({ viewport: { width: ANCHO, height: ANCHO < 600 ? 852 : 900 } })).newPage();
  const errores = []; p.on('pageerror', e => errores.push(e.message));
  let n = 0; const ok = [];
  const paso = async (titulo, fn) => {
    n++; const t0 = Date.now();
    try { const dice = await fn(); await p.waitForTimeout(400); await p.screenshot({ path: `${OUT}/paso_${n}.png` }); ok.push(true); console.log(`✓ ${n} · ${titulo} (${((Date.now() - t0) / 1000).toFixed(1)} s)${dice ? ' — ' + dice : ''}`); }
    catch (e) { ok.push(false); await p.screenshot({ path: `${OUT}/paso_${n}_falla.png` }).catch(() => {}); console.log(`✗ ${n} · ${titulo} — ${e.message.split('\n')[0]}`); }
  };
  const ir = async v => { if (ANCHO < 760 && await p.isVisible('#navmenu')) await p.click('#navmenu'); await p.click(`#nav a[data-v="${v}"]`); };
  await p.goto(BASE, { waitUntil: 'networkidle' }); await p.waitForTimeout(600);

  // desde el 24/11 la app abre en el home y las tres preguntas están en «Crear tu proyecto», en una sola pantalla
  await paso('El home y «Crear tu proyecto»: mujer, para una marca, fast fashion', async () => {
    await p.waitForSelector('#v-inicio:not([hidden])');
    // 24/11 vuelta K: la primera pantalla sólo define y avisa que se baja; «Crear tu proyecto» va al final
    await p.click('#v-inicio .hbaja'); await p.waitForTimeout(400); await p.locator('#crear').scrollIntoViewIfNeeded(); await p.waitForTimeout(500);
    await p.fill('#inform input[id^=pn-]', 'Demo de clase'); await p.fill('#inform input[id^=pe-]', 'demo.ciclo@ejemplo.com');
    for (const t of ['Mujer', 'Para una marca', 'Fast fashion']) await p.click(`#inform .seg label:has-text("${t}")`);
    await p.click('#inform button[type=submit]');
    await p.waitForSelector('#v-radar:not([hidden])'); return (await p.textContent('#perfilrad')).replace('Editar', '').replace(/\s+/g, ' ').trim();
  });
  // 24/11 (rediseño D): Mis ciclos es Tendencias (tarjetas por señal) | Gráfica (un gráfico por vez)
  await paso('Mis ciclos: las tarjetas por señal y «Gana y pierde terreno»', async () => {
    await p.waitForSelector('#v-radar:not([hidden]) #mctend .mcf', { timeout: 8000 });
    // 24/11 vuelta K: dos secciones a la vista, la gráfica arriba y «Mis tendencias» abajo; sin selector
    const n = await p.$$eval('#mctend .mcf', a => a.length), gr = await p.$$eval('#mctend .mcgrcab h3', h => h.map(x => x.textContent.trim()).join(' · '));
    await p.waitForSelector('#mcgraf .movp svg');
    const c = (await p.textContent('#mcgraf .mcconc')).trim();
    return `${n} tarjetas (${gr}) · ${c.slice(0, 70)}…`;
  });
  await paso('La ficha de Jeans baggy', async () => {
    await p.click('#mctend .mcf:has-text("Jeans baggy")'); await p.waitForSelector('#v-detalle:not([hidden]) svg');
    return (await p.textContent('#v-detalle h1, #v-detalle h2')).trim().slice(0, 60);
  });
  await paso('Diseñar con este corte', async () => {
    await p.click('#v-detalle [data-dz]'); await p.waitForSelector('#dzfijo:not([hidden])');
    return (await p.textContent('#dzfijo')).replace(/\s+/g, ' ').trim().slice(0, 80);
  });
  await paso('Preguntar: soltar una imagen; CLIP la lee adentro del hilo', async () => {
    await ir('lectura'); await p.waitForSelector('#v-lectura:not([hidden]) .ltvacio');
    if (KEY) await p.evaluate(k => { $('#askey').value = k; asGuardar('groq_key', k); asEstadoClave(); }, KEY);
    if (IMAGEN) await p.setInputFiles('#asfile', IMAGEN); else await p.click('.ltejb >> text=Denim');
    await p.waitForFunction(() => as.hist.some(m => m.tipo === 'lectura' && !m.leyendo), null, { timeout: 120000 });
    await p.waitForFunction(() => !as.ocupado, null, { timeout: 90000 });
    const m = await p.evaluate(() => { const u = as.hist.find(x => x.tipo === 'lectura'); return { clip: u.clip.map(a => a.n), fallo: u.fallo, r: u.r && u.r.conclusion, error: u.error, looks: (u.looks || []).length }; });
    if (m.fallo) throw new Error(m.fallo);
    return `leyó: ${m.clip.join(', ') || 'nada'} · ${m.looks} looks · ` + (m.r ? 'devolución: ' + m.r : m.error ? 'Groq: ' + m.error : 'devolución con reglas');
  });
  await paso('Preguntar: la pregunta, con la pieza de datos adentro', async () => {
    await p.click(`#assug [data-q="${PREGUNTA}"]`).catch(async () => { await p.fill('#astexto', PREGUNTA); await p.click('#asenviar'); });
    await p.waitForFunction(() => !as.ocupado && as.hist[as.hist.length - 1].tipo === 'resp', null, { timeout: 90000 });
    const r = await p.evaluate(() => { const u = as.hist[as.hist.length - 1]; return { r: u.r && [u.r.conclusion, u.r.respaldo].join(' / '), error: u.error, sin: !!u.sinClave || !$('#askey').value, tok: u.tok, pieza: u.P && (u.P.titulo || u.P.t) }; });
    if (KEY && !r.r) throw new Error(r.error || 'sin respuesta');
    if (KEY) { await p.locator('.ltver summary').last().click(); }
    return r.r ? `${r.r} · pieza: ${r.pieza} · ${r.tok}` : `sin clave, la burbuja dice: ${await p.locator('.ltcic').last().locator('.ltsin, .ltact').first().textContent()}`;
  });
  await paso('El brief, la pirueta: tres elecciones y el veredicto', async () => {
    if (ANCHO < 760 && await p.isVisible('#navmenu')) await p.click('#navmenu');
    if (await p.isVisible('#navmas')) await p.click('#navmas'); // en el celular, El brief ya está a la vista en el menú
    await p.click('#nav a[data-v="mover"]');
    await p.click('#bfok');
    for (let i = 0; i < 3; i++) { await p.click('.bfop >> nth=0'); await p.waitForTimeout(400); }
    await p.waitForSelector('.bfver', { timeout: 8000 }); await p.waitForTimeout(4500);
    return (await p.textContent('.bftit')).trim() + ' · ' + (await p.$$eval('.bfcasa b', a => a.map(x => x.textContent).join(' / ')));
  });
  await paso('Método: medido contra interpretado', async () => {
    await p.evaluate(() => mostrar('racional')); await p.waitForSelector('#v-racional:not([hidden])');
    return (await p.$$eval('#v-racional .tag', a => [...new Set(a.map(x => x.textContent))].slice(0, 6))).join(' · ');
  });

  console.log(errores.length ? 'errores en la página: ' + errores.join(' | ') : 'sin errores en la página');
  console.log(`${ok.filter(Boolean).length} de ${ok.length} pasos · capturas en ${OUT}`);
  await b.close();
  process.exit(ok.every(Boolean) && !errores.length ? 0 : 1);
})();
