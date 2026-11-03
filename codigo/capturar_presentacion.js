// CICLO · las capturas de la app que usa la presentación (03/11/2026).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/capturar_presentacion.js [http://localhost:8000/]
//   python3 codigo/armar_capturas_presentacion.py
// Requiere: npm install playwright, pip install pillow.
// Este script saca las pantallas de la app en crudo (PNG, en la carpeta temporal del sistema, ciclo_presentacion/);
// el de Python las pega en el lado «App» de cada par y escribe los .webp de app/presentacion/capturas/.
// Los lados «Figma» y las referencias (revista_antes, referencia_apple, figma_tarjeta_estados) no se tocan: son historia.
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = process.argv[2] || 'http://localhost:8000/';
const OUT = require('path').join(require('os').tmpdir(), 'ciclo_presentacion');
const PERFIL = '?c=premium&v=marca&pu=mujer';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const abrir = async ({ ancho = 1400, alto = 900, escala = 1, vista } = {}) => {
    const movil = ancho < 500;
    const ctx = await b.newContext({ viewport: { width: ancho, height: alto }, colorScheme: 'light', deviceScaleFactor: escala, isMobile: movil, hasTouch: movil });
    const p = await ctx.newPage();
    await p.goto(BASE + (vista ? '#' + vista + PERFIL : ''), { waitUntil: 'networkidle' });
    await p.waitForTimeout(800);
    return p;
  };
  const foto = async (p, nombre, clip) => { await p.mouse.move(2, 2); await p.waitForTimeout(500); await p.screenshot({ path: `${OUT}/${nombre}.png`, clip }); console.log('·', nombre); await p.context().close(); };

  // la entrada, como la ve alguien que llega por primera vez
  await foto(await abrir(), 'app_entrada');
  // Tendencias, con el perfil aplicado
  await foto(await abrir({ vista: 'radar' }), 'app_tendencias');
  // la ficha de Amplio, arriba y en el detalle de la procedencia
  let p = await abrir({ vista: 'radar' });
  await p.evaluate(() => abrirDetalle('amplio')); await foto(p, 'app_ficha');
  p = await abrir({ ancho: 1440, vista: 'radar', escala: 1.25 });
  await p.evaluate(() => abrirDetalle('amplio'));
  const r = await p.evaluate(() => { const d = document.querySelector('#v-detalle .dcols'); window.scrollTo(0, d.getBoundingClientRect().top + scrollY - 120); const q = d.getBoundingClientRect(); return { x: q.left, y: q.top + 8 }; });
  await foto(p, 'app_ficha_procedencia', { x: r.x, y: r.y, width: 1280, height: 640 });
  // el celular: Tendencias y el menú abierto
  await foto(await abrir({ ancho: 393, alto: 852, vista: 'radar' }), 'app_celular_tendencias');
  p = await abrir({ ancho: 393, alto: 852, vista: 'radar' });
  await p.click('#navmenu');
  await foto(p, 'app_celular_menu');

  await b.close();
  console.log('crudo listo en ' + OUT);
})();
