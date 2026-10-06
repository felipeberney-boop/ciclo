const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.goto('file://' + process.cwd() + '/repo/index.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(700);
  fs.mkdirSync('capturas', { recursive: true });
  await p.screenshot({ path: 'capturas/captura_01_portada.png' });

  const vistas = [
    ['radar', 'captura_02_radar'],
    ['etapas', 'captura_03_el_ciclo'],
    ['recorridos', 'captura_04_recorridos'],
    ['marcas', 'captura_05_marcas'],
    ['racional', 'captura_06_metodo'],
  ];
  for (const [v, n] of vistas) {
    await p.evaluate((x) => document.querySelector('[data-v=' + x + ']').click(), v);
    await p.waitForTimeout(500);
    await p.screenshot({ path: 'capturas/' + n + '.png' });
  }
  await b.close();
  console.log('capturas listas');
})();
