// CICLO · el recorrido paso a paso para el readme (03/11/2026; rehecho el 24/11/2026 para el home y los proyectos;
// al día con la vuelta P: el selector del recorrido, «¿Lo viste venir?», el premio, Tu archivo, el aviso sin proyecto,
// Mis ciclos con el gráfico en un desplegable (abierto en la primera visita) y «Paso n de 9» fijo en Diseñar).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/capturar_recorrido.js [http://localhost:8000/]
// Requiere: npm install playwright. Escribe en entregas/entrega_4/recorrido/ (el de la Entrega 3 queda en entrega_3/).
// Todo con clicks de verdad, en una sola pestaña y sin nada guardado, como alguien que entra por primera vez.
// Preguntale a CICLO se captura sin respuesta escrita: una respuesta simulada sería presentar como real algo que no lo es.
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = process.argv[2] || 'http://localhost:8000/';
const OUT = 'entregas/entrega_4/recorrido';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  // las capturas de la entrada vieja de tres preguntas (hasta el 24/11) ya no corresponden a la app
  for (const f of fs.readdirSync(OUT)) if (f.endsWith('.png')) fs.unlinkSync(`${OUT}/${f}`);
  const b = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  const abrir = async (ancho, alto) => {
    const movil = ancho < 500;
    const ctx = await b.newContext({ viewport: { width: ancho, height: alto }, colorScheme: 'light', deviceScaleFactor: movil ? 2 : 1, isMobile: movil, hasTouch: movil });
    const p = await ctx.newPage();
    // «load» y no «networkidle»: las fotos de Vogue a veces tardan y dejaban la carga colgada (24/11)
    await p.goto(BASE, { waitUntil: 'load', timeout: 60000 });
    await p.waitForTimeout(2500);
    return p;
  };
  const foto = async (p, nombre) => { await p.mouse.move(2, 2); await p.waitForTimeout(1200); await p.screenshot({ path: `${OUT}/${nombre}.png` }); console.log('·', nombre); };
  const hasta = async (p, sel, margen = 16) => { await p.evaluate(([s, m]) => { const e = document.querySelector(s); const mast = document.querySelector('.mast'); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - m - (mast ? mast.offsetHeight : 0)); }, [sel, margen]); await p.waitForTimeout(900); };
  const ir = async (p, v) => { if (await p.isVisible('#navmenu')) await p.click('#navmenu'); await p.click(`#nav a[data-v="${v}"]`); await p.waitForTimeout(1200); };
  const crear = async (p, vinculo, cliente) => {
    await p.fill('#inform input[id^=pn-]', 'Invierno'); await p.fill('#inform input[id^=pe-]', 'recorrido@ejemplo.com');
    for (const t of ['Mujer', vinculo, cliente]) await p.click(`#inform .seg label:has-text("${t}")`);
  };

  for (const [ancho, alto, suf] of [[1400, 900, ''], [393, 852, '_celular']]) {
    const p = await abrir(ancho, alto);
    // el home: qué es, cómo funciona, y «Creá tu proyecto» al final
    await foto(p, `paso_01_home${suf}`);
    await p.click('#v-inicio .hbaja'); await p.waitForTimeout(1200);
    await foto(p, `paso_02_como_funciona${suf}`);
    await hasta(p, '#crear'); await crear(p, 'Para una marca', 'Fast fashion');
    await hasta(p, '#inform', 60); await foto(p, `paso_03_crear_tu_proyecto${suf}`);
    await p.click('#inform button[type=submit]'); await p.waitForSelector('#v-radar:not([hidden]) #mctend .mcf');
    // Mis ciclos: la gráfica y Mis tendencias
    await foto(p, `paso_04_mis_ciclos${suf}`);
    await p.click('#mcgraf .mcdet summary'); await p.waitForTimeout(400); // como queda desde la segunda visita: el gráfico cerrado
    await hasta(p, '#mcsec2'); await foto(p, `paso_05_mis_tendencias${suf}`);
    await p.click('#mctend .mcf:has-text("Jeans baggy")'); await p.waitForSelector('#v-detalle:not([hidden]) svg');
    await p.evaluate(() => window.scrollTo(0, 0)); await foto(p, `paso_06_ficha_del_atributo${suf}`);
    await p.click('#v-detalle [data-dz]');
    await foto(p, `paso_07_disenar_con_el_atributo_fijo${suf}`);
    // Explorar: el buscador, las categorías y el recorrido de cualquier atributo
    await ir(p, 'recorridos'); await foto(p, `paso_08_explorar${suf}`);
    // el título es el selector: abre un panel con buscador y las cuatro familias
    await hasta(p, '#rtitulo'); await p.click('#rtbtn'); await p.fill('#rtq', 'sat'); await foto(p, `paso_09_explorar_selector${suf}`);
    await p.click('#rtlista [data-r="satenseda"]'); await hasta(p, '#rtitulo'); await foto(p, `paso_10_explorar_recorrido${suf}`);
    await ir(p, 'lectura'); await foto(p, `paso_11_preguntar${suf}`);
    await ir(p, 'mover'); await foto(p, `paso_12_el_brief${suf}`);
    // «¿Lo viste venir?»: se juega de verdad hasta acertar tres seguidas, que es lo que da una pieza de archivo
    await p.click('#bfmodos [data-modo="viste"]'); await p.waitForTimeout(800); await foto(p, `paso_13_lo_viste_venir${suf}`);
    let premio = false;
    for (let i = 0; i < 300 && !premio; i++) {
      await p.click('#mv [data-vv="bajo"]'); await p.waitForTimeout(300);
      premio = !!(await p.$('#mv .bfpremio'));
      if (!premio) await p.click('#vvotro');
    }
    await p.waitForTimeout(1800); await foto(p, `paso_14_pieza_de_archivo${suf}`);
    if (premio) { await p.click('#mv [data-arch]'); await p.waitForTimeout(1200); await foto(p, `paso_15_tu_archivo${suf}`); }
    await p.context().close();
  }
  // la otra rama: por tu cuenta, donde la marca espera, vos explorás
  {
    const p = await abrir(1400, 900);
    await hasta(p, '#crear'); await crear(p, 'Por mi cuenta', 'High fashion');
    await p.click('#inform button[type=submit]'); await p.waitForSelector('#v-radar:not([hidden]) #mctend .mcf');
    await hasta(p, '#mctend .mcgrcab h3.s-esperar'); await foto(p, 'paso_16_por_tu_cuenta_explorar');
    await p.context().close();
  }
  // y quien sólo mira: Explorar le recuerda que no tiene proyecto
  for (const [ancho, alto, suf] of [[1400, 900, ''], [393, 852, '_celular']]) {
    const p = await abrir(ancho, alto);
    await hasta(p, '#crear'); await p.click('[data-mirar]'); await p.waitForSelector('#v-recorridos:not([hidden]) #exsinpy:not([hidden])');
    await p.evaluate(() => window.scrollTo(0, 0)); await foto(p, `paso_17_solo_mirando${suf}`);
    await p.context().close();
  }
  await b.close();
  console.log('recorrido listo en ' + OUT);
})();
