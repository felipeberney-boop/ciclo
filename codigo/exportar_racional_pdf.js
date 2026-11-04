// CICLO · el racional en PDF, para entregar o imprimir (04/11/2026).
// Uso, desde la raíz del repo: node codigo/exportar_racional_pdf.js
// Requiere: npm install playwright marked. Lee entregas/entrega_4/racional.md y escribe racional.pdf al lado.
// Las imágenes se resuelven desde la carpeta del racional, igual que en GitHub.
const { chromium } = require('playwright');
const { marked } = require('marked');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const DIR = path.resolve('entregas/entrega_4');
const md = fs.readFileSync(path.join(DIR, 'racional.md'), 'utf8');

// la misma tipografía y los mismos tonos que la app: tinta, gris perla y un solo azul para los links
const css = `
  @page { size: A4; margin: 18mm 16mm 18mm 16mm; }
  body { font: 10.5pt/1.5 -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", sans-serif; color: #1d1d1f; }
  h1 { font-size: 26pt; font-weight: 600; letter-spacing: -.02em; margin: 0 0 6pt; }
  h2 { font-size: 15pt; font-weight: 600; margin: 22pt 0 6pt; break-after: avoid; }
  p, li { orphans: 3; widows: 3; }
  a { color: #0066cc; text-decoration: none; word-break: break-word; }
  blockquote { margin: 8pt 0; padding: 8pt 12pt; background: #f5f5f7; border-radius: 10pt; }
  blockquote p { margin: 0; }
  hr { border: 0; border-top: 1px solid #d2d2d7; margin: 16pt 0; }
  code { font: 9pt ui-monospace, Menlo, monospace; background: #f5f5f7; padding: 0 3pt; border-radius: 4pt; }
  pre { background: #f5f5f7; padding: 8pt 10pt; border-radius: 10pt; line-height: 1.35; break-inside: avoid; white-space: pre; }
  pre code { background: none; padding: 0; font-size: 6.8pt; } /* los esquemas en ASCII entran enteros en el ancho de la hoja */
  table { border-collapse: collapse; width: 100%; font-size: 8.5pt; line-height: 1.35; margin: 8pt 0; }
  th, td { text-align: left; vertical-align: top; padding: 4pt 6pt; border-bottom: 1px solid #e8e8ed; }
  th { font-weight: 600; border-bottom: 1px solid #86868b; }
  tr { break-inside: avoid; }
  img { max-width: 100%; border-radius: 6pt; }
  td img { display: block; }
`;

(async () => {
  const html = `<!doctype html><html lang="es"><head><meta charset="utf-8"><base href="${pathToFileURL(DIR + '/').href}"><style>${css}</style></head><body>${marked.parse(md)}</body></html>`;
  const b = await chromium.launch();
  const p = await b.newPage();
  // desde about:blank Chromium no carga archivos locales: el HTML va a un archivo temporal y se abre desde ahí
  const tmp = path.join(require('os').tmpdir(), 'ciclo_racional.html');
  fs.writeFileSync(tmp, html);
  await p.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
  const rotas = await p.$$eval('img', a => a.filter(i => !i.naturalWidth).map(i => i.getAttribute('src')));
  if (rotas.length) throw new Error('imágenes que no cargan: ' + rotas.join(', '));
  const out = path.join(DIR, 'racional.pdf');
  await p.pdf({ path: out, format: 'A4', printBackground: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font:8px -apple-system,sans-serif;color:#86868b;width:100%;text-align:center">CICLO · Racional · <span class="pageNumber"></span> de <span class="totalPages"></span></div>' });
  await b.close();
  fs.unlinkSync(tmp);
  console.log('listo: ' + path.relative(process.cwd(), out));
})();
