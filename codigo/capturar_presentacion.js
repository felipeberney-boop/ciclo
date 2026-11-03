// CICLO · la captura de la app que usa la presentación: Tendencias, en «Del diseño al código» (03/11/2026).
// Uso, desde la raíz del repo, con la app servida (cd app && python3 -m http.server 8000):
//   node codigo/capturar_presentacion.js [http://localhost:8000/]
//   python3 codigo/armar_capturas_presentacion.py
// Requiere: npm install playwright, pip install pillow.
// Este script saca la pantalla en crudo (PNG, en la carpeta temporal del sistema, ciclo_presentacion/); el de Python
// la pasa a .webp en app/presentacion/capturas/. Las otras dos imágenes de esa lámina no salen de la app:
// figma_original_radar (el prototipo de Figma de la Entrega 2) y referencia_apple (la referencia de la cátedra).
const { chromium } = require('playwright');
const fs = require('fs');

const BASE = process.argv[2] || 'http://localhost:8000/';
const OUT = require('path').join(require('os').tmpdir(), 'ciclo_presentacion');
const PERFIL = '?c=premium&v=marca&pu=mujer';

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1400, height: 900 }, colorScheme: 'light' })).newPage();
  await p.goto(BASE + '#radar' + PERFIL, { waitUntil: 'networkidle' });
  await p.mouse.move(2, 2); await p.waitForTimeout(1300);
  await p.screenshot({ path: `${OUT}/app_tendencias.png` });
  await b.close();
  console.log('crudo listo en ' + OUT);
})();
