// CICLO · capturas de la app para el readme y la entrega (26/10/2026).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/capturar_pantallas_de_la_app.js [http://localhost:8000/]
// Requiere: npm install playwright. Escribe en entregas/entrega_4/capturas/ (las del 03/11 quedaron en entrega_3/capturas/).
// No toca Groq ni baja el modelo CLIP: Buscar por imagen usa un look del índice, y Preguntar se captura sin respuesta
// (una respuesta simulada en una captura sería presentar como real algo que no lo es).
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = process.argv[2] || 'http://localhost:8000/';
const OUT = 'entregas/entrega_4/capturas';
const PERFIL = '?c=fast&v=marca&pu=mujer';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const abrir = async ({ ancho = 1400, alto = 900, tema = 'light', vista, perfil = true } = {}) => {
    const movil = ancho < 500;
    const ctx = await b.newContext({ viewport: { width: ancho, height: alto }, colorScheme: tema, deviceScaleFactor: movil ? 2 : 1, isMobile: movil, hasTouch: movil });
    const p = await ctx.newPage();
    await p.goto(BASE + (vista ? '#' + vista + (perfil ? PERFIL : '') : ''), { waitUntil: 'networkidle' });
    await p.waitForTimeout(700);
    return p;
  };
  const foto = async (p, nombre) => { await p.screenshot({ path: `${OUT}/${nombre}.png` }); console.log('·', nombre); await p.context().close(); };
  const hasta = async (p, sel, margen = 24) => { await p.evaluate(([s, m]) => { const e = document.querySelector(s); const mast = document.querySelector('.mast'); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - m - (mast ? mast.offsetHeight : 0)); /* el encabezado queda fijo arriba */ }, [sel, margen]); await p.waitForTimeout(300); };

  // la entrada: las tres preguntas
  await foto(await abrir(), 'captura_01_entrada');
  // Diseñar
  await foto(await abrir({ vista: 'disenar' }), 'captura_02_disenar_prenda');
  let p = await abrir({ vista: 'disenar' });
  await p.evaluate(() => { dz.prenda = 'remeras'; dz.tipo = 'remera'; dz.material = 'jersey'; dzIr('estampa'); });
  await p.waitForTimeout(400); await hasta(p, '.dzhead'); await foto(p, 'captura_03_disenar_estampa');
  p = await abrir({ vista: 'disenar' });
  await p.evaluate(() => { dz.prenda = 'pantalones'; dz.tipo = 'largo'; dz.corte = 'baggy'; dz.material = 'denimrigido'; dzIr('fin'); });
  await p.waitForTimeout(400); await hasta(p, '#dzcuerpo'); await foto(p, 'captura_04_tu_diseno');
  p = await abrir({ vista: 'disenar' });
  await p.evaluate(() => { dz.prenda = 'calzado'; dzIr('tipo'); });
  await p.waitForTimeout(400); await hasta(p, '.czint'); await foto(p, 'captura_05_calzado_dos_intentos');
  // El ciclo y el recorrido
  p = await abrir({ vista: 'recorridos' }); await hasta(p, '#ciclos', 60); await foto(p, 'captura_06_el_ciclo');
  p = await abrir({ vista: 'recorridos' }); await hasta(p, '.lys'); await foto(p, 'captura_07_recorrido_hasta_2030');
  // Tendencias, Buscar por imagen, Preguntar
  p = await abrir({ vista: 'radar' }); await hasta(p, '#terreno'); await p.waitForTimeout(2800); /* las curvas se dibujan */ await foto(p, 'captura_08_tendencias');
  // El brief (la pirueta desde el 10/11): el encargo y, después de tres toques, el veredicto
  p = await abrir({ vista: 'mover' }); await p.waitForTimeout(1200); await foto(p, 'captura_19_el_brief');
  p = await abrir({ vista: 'mover' }); await p.waitForTimeout(1200); await p.click('#bfok'); await p.waitForTimeout(600);
  for (const i of [0, 1, 0]) { await p.click('.bfop >> nth=' + i); await p.waitForTimeout(600); }
  await p.waitForTimeout(5200); await hasta(p, '#mv', 12); await foto(p, 'captura_20_el_brief_veredicto');
  p = await abrir({ vista: 'consulta' });
  await p.click('#qej .chip:nth-child(2)'); await p.waitForSelector('#qres .qrow2', { timeout: 60000 }); await p.waitForTimeout(2500);
  await hasta(p, '.qgrid, #qres', 120); await foto(p, 'captura_09_buscar_por_imagen');
  p = await abrir({ vista: 'asistente' });
  await p.evaluate(() => { dz.prenda = 'pantalones'; dz.tipo = 'largo'; dz.corte = 'baggy'; dz.material = 'denimrigido'; asPintar(); });
  await hasta(p, '#asdis', 140); await foto(p, 'captura_10_preguntar');
  // el método
  p = await abrir({ vista: 'etapas' }); await hasta(p, '.km'); await foto(p, 'captura_11_el_modelo');
  await foto(await abrir({ vista: 'retornos' }), 'captura_12_retornos');
  p = await abrir({ vista: 'racional' }); await hasta(p, '#metdatos'); await foto(p, 'captura_13_metodo_los_datos');
  // celular, y el panel «Más» con sus tarjetas
  p = await abrir({ ancho: 393, alto: 852, vista: 'disenar' });
  await p.evaluate(() => { dz.prenda = 'calzado'; dzIr('tipo'); }); await p.waitForTimeout(400); await foto(p, 'captura_14_celular_disenar');
  await foto(await abrir({ ancho: 393, alto: 852, vista: 'recorridos' }), 'captura_15_celular_el_ciclo');
  p = await abrir({ vista: 'radar' }); await p.click('#navmas'); await p.waitForTimeout(400); await foto(p, 'captura_16_menu_mas');
  // la pirueta: Adiviná vos, con un trazo dibujado y revelado
  p = await abrir({ vista: 'adivina' });
  const svg = await p.$('#v-adivina svg'); const bx = await svg.boundingBox();
  // el trazo arranca en el punto de 2019 y sube de a poco, como lo dibujaría alguien que cree que vuelve
  const pto = await p.$$eval('#v-adivina svg circle', cs => { const r = cs[cs.length - 1].getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; });
  const fin = bx.x + bx.width * 0.985, pasos = 14;
  await p.mouse.move(pto.x, pto.y); await p.mouse.down();
  for (let i = 1; i <= pasos; i++) await p.mouse.move(pto.x + (fin - pto.x) * i / pasos, pto.y - bx.height * 0.12 * i / pasos);
  await p.mouse.up(); await p.waitForTimeout(300);
  const ver = await p.$('#v-adivina button.kbtn, #v-adivina button[data-adv-ver]'); if (ver) { await ver.click(); await p.waitForTimeout(500); }
  await foto(p, 'captura_17_adivina_vos');

  await b.close();
  console.log('capturas listas en ' + OUT);
})();
