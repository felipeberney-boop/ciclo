// CICLO · el recorrido paso a paso para el readme (03/11/2026; la entrada nueva, 04/11/2026).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/capturar_recorrido.js [http://localhost:8000/]
// Requiere: npm install playwright. Escribe en entregas/entrega_4/recorrido/ (el de la Entrega 3 queda en entrega_3/).
// Todo con clicks de verdad, en una sola pestaña y sin perfil guardado, como alguien que entra por primera vez.
// Preguntar se captura sin respuesta: una respuesta simulada sería presentar como real algo que no lo es.
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = process.argv[2] || 'http://localhost:8000/';
const OUT = 'entregas/entrega_4/recorrido';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const abrir = async (ancho, alto) => {
    const movil = ancho < 500;
    const ctx = await b.newContext({ viewport: { width: ancho, height: alto }, colorScheme: 'light', deviceScaleFactor: movil ? 2 : 1, isMobile: movil, hasTouch: movil });
    const p = await ctx.newPage();
    await p.goto(BASE, { waitUntil: 'networkidle' });
    await p.waitForTimeout(700);
    return p;
  };
  const foto = async (p, nombre) => { await p.mouse.move(2, 2); await p.waitForTimeout(900); await p.screenshot({ path: `${OUT}/${nombre}.png` }); console.log('·', nombre); };
  const tarjeta = (p, attr, v) => p.click(`#ggrid [${attr}="${v}"]`);
  const hasta = async (p, sel, margen = 24) => { await p.evaluate(([s, m]) => { const e = document.querySelector(s); const mast = document.querySelector('.mast'); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - m - (mast ? mast.offsetHeight : 0)); }, [sel, margen]); await p.waitForTimeout(300); };

  for (const [ancho, alto, suf] of [[1400, 900, ''], [393, 852, '_celular']]) {
    const p = await abrir(ancho, alto);
    // la entrada: qué estás por decidir, para quién, qué tipo de marca
    await foto(p, `paso_01_que_estas_por_decidir${suf}`);
    await tarjeta(p, 'data-dec', 'producir');
    await foto(p, `paso_02_para_quien_disenas${suf}`);
    await tarjeta(p, 'data-pub', 'mujer');
    await foto(p, `paso_03_tipo_de_marca${suf}`);
    await tarjeta(p, 'data-cli', 'fast');
    await foto(p, `paso_04_cae_en_tendencias_con_el_perfil${suf}`);
    if (!suf) {
      // el uso
      await hasta(p, '#terreno'); await foto(p, 'paso_05_tendencias');
      await p.click('#grid > .plate');
      await p.evaluate(() => window.scrollTo(0, 0)); await foto(p, 'paso_06_ficha_del_atributo');
      await p.focus('#v-detalle [data-dz]');
      await foto(p, 'paso_07_boton_disenar_con');
      await p.click('#v-detalle [data-dz]');
      await foto(p, 'paso_08_disenar_con_el_atributo_fijo');
      await p.click('#nav a[data-v="asistente"]');
      await foto(p, 'paso_09_preguntar');
    } else {
      await p.evaluate(() => { mostrar('radar'); });
      await p.click('#grid > .plate');
      await p.click('#v-detalle [data-dz]');
      await foto(p, 'paso_08_disenar_con_el_atributo_fijo_celular');
    }
    await p.context().close();
  }
  // las otras dos decisiones: adónde lleva cada una
  for (const [dec, nombre] of [['revisar', 'paso_10_si_algo_ya_paso'], ['disenar', 'paso_11_que_disenar_entra_a_disenar']]) {
    const p = await abrir(1400, 900);
    await tarjeta(p, 'data-dec', dec); await tarjeta(p, 'data-pub', 'mujer'); await tarjeta(p, 'data-cli', 'fast');
    if (dec === 'revisar') await hasta(p, '#grid');
    await foto(p, nombre);
    await p.context().close();
  }
  await b.close();
  console.log('recorrido listo en ' + OUT);
})();
