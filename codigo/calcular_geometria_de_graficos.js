// Calcula la geometría de los gráficos de alta fidelidad para el prototipo de Figma.
const fs = require('fs');
const D = require('./datos_app.json');
const out = {};
const r2 = n => Math.round(n * 10) / 10;

function poly(pts) {
  return pts.map((p, i) => (i ? 'L ' : 'M ') + r2(p[0]) + ' ' + r2(p[1])).join(' ');
}
// segmenta una serie con nulls en tramos continuos
function segments(vals, X, Y) {
  const segs = []; let cur = [];
  vals.forEach((v, i) => {
    if (v == null) { if (cur.length > 1) segs.push(cur); cur = []; return; }
    cur.push([X(i), Y(v)]);
  });
  if (cur.length > 1) segs.push(cur);
  return segs;
}

/* ───────── 1 · DETALLE · jeans amplios, 4 capas ───────── */
{
  const o = D.REC.find(r => r.id === 'jamplio');
  const PX = 112, PY = 340, PW = 768, PH = 236;
  const X = i => PX + (i / 21) * PW;
  const Y = v => PY + (1 - v / 100) * PH;
  const series = [
    { k: 'Pasarela', src: 'Vogue Runway · «denim»', c: '#1F3A6E', vals: o.v },
    { k: 'Búsqueda mundo', src: 'Google Trends', c: '#B8503D', vals: o.g },
    { k: 'Búsqueda Argentina', src: 'Google Trends AR', c: '#B8503D', vals: o.a, dash: [6, 5] },
    { k: 'Reddit', src: 'r/femalefashionadvice', c: '#1E7A52', vals: o.r }
  ].filter(s => s.vals);
  out.det = {
    box: { PX, PY, PW, PH },
    grid: [0, 25, 50, 75, 100].map(v => ({ v, y: r2(Y(v)) })),
    xticks: [2004, 2009, 2014, 2019, 2025].map(y => ({ y, x: r2(X(y - 2004)) })),
    series: series.map(s => {
      const segs = segments(s.vals, X, Y);
      const last = s.vals.map((v, i) => v == null ? null : i).filter(i => i !== null).pop();
      const mx = Math.max(...s.vals.filter(v => v != null));
      const pk = s.vals.indexOf(mx);
      return {
        k: s.k, src: s.src, c: s.c, dash: s.dash || null,
        d: segs.map(poly), peak: { x: r2(X(pk)), y: r2(Y(mx)), year: 2004 + pk },
        end: { x: r2(X(last)), y: r2(Y(s.vals[last])) }
      };
    }),
    shade: { x: r2(X(0)), w: r2(X(6) - X(0)) }   // pasarela poco fiable antes de 2010
  };
}

/* ───────── 2 · EL CICLO · scatter k-means ───────── */
{
  const rows = D.KM.rows, sc = D.KM.sc, cent = D.KM.cent;
  const PX = 128, PY = 310, PW = 664, PH = 330;
  const xs = rows.map(r => r.bm), ys = rows.map(r => r.bn);
  const xmin = Math.min(...xs) - 0.08, xmax = Math.max(...xs) + 0.08;
  const ymin = Math.min(...ys) - 0.06, ymax = Math.max(...ys) + 0.06;
  const X = v => PX + (v - xmin) / (xmax - xmin) * PW;
  const Y = v => PY + (1 - (v - ymin) / (ymax - ymin)) * PH;
  // el índice de cluster viene del modelo; el nombre sale del contenido de cada grupo
  const CL = ['#2D5BA8', '#1E7A52', '#C08A1E', '#B8503D'];
  const NAMES = ['En ascenso', 'En pico', 'En retorno', 'Saturada'];
  out.ciclo = {
    box: { PX, PY, PW, PH },
    clusters: CL.map((c, i) => ({ c, n: NAMES[i] })),
    pts: rows.map(r => ({ n: r.n, x: r2(X(r.bm)), y: r2(Y(r.bn)), cl: r.cl, c: CL[r.cl] })),
    cents: cent.map((z, i) => ({
      x: r2(X(z[3] * sc.s[3] + sc.m[3])), y: r2(Y(z[2] * sc.s[2] + sc.m[2])), c: CL[i]
    })),
    xlab: ['cae', 'estable', 'sube'].map((t, i) => ({ t, x: r2(PX + (PW / 2) * i) })),
    ylab: ['lejos del pico', 'en su pico'].map((t, i) => ({ t, y: r2(PY + PH - (PH) * i) })),
    groups: [0, 1, 2, 3].map(i => ({
      n: NAMES[i], c: CL[i], items: rows.filter(r => r.cl === i).map(r => r.n)
    })),
    elbow: D.KM.elbow || null
  };
}

/* ───────── 3 · RECORRIDOS · participación de los jeans por corte ───────── */
{
  const Y_ = D.JE.Y, w = D.JE.web;
  const PX = 112, PY = 300, PW = 760, PH = 280;
  const X = i => PX + (i / (Y_.length - 1)) * PW;
  const YY = p => PY + (1 - p / 100) * PH;
  const share = Y_.map((_, i) => {
    const t = w.amplio[i] + w.medio[i] + w.ajustado[i];
    return { a: w.amplio[i] / t * 100, m: w.medio[i] / t * 100, j: w.ajustado[i] / t * 100 };
  });
  // apilado: ajustado abajo, medio, amplio arriba
  const cum = share.map(s => ({ j: s.j, jm: s.j + s.m, all: 100 }));
  function band(lo, hi, color, name) {
    const top = Y_.map((_, i) => [X(i), YY(cum[i][hi])]);
    const bot = Y_.map((_, i) => [X(i), YY(lo === 0 ? 0 : cum[i][lo])]).reverse();
    return { name, c: color, d: poly(top.concat(bot)) + ' Z' };
  }
  out.rec = {
    box: { PX, PY, PW, PH },
    bands: [
      band(0, 'j', '#B8503D', 'Ajustados'),
      band('j', 'jm', '#C9BFAE', 'Medios'),
      band('jm', 'all', '#1F3A6E', 'Amplios')
    ],
    xticks: [2004, 2009, 2014, 2019, 2025].map(y => ({ y, x: r2(X(Y_.indexOf(y))) })),
    cross: { x: r2(X(Y_.indexOf(2021))), label: '2021 · los amplios pasan a los ajustados' },
    end: {
      a: Math.round(share[share.length - 1].a), m: Math.round(share[share.length - 1].m),
      j: Math.round(share[share.length - 1].j)
    },
    start: { j: Math.round(share[Y_.indexOf(2012)].j) }
  };
}

/* ───────── 4 · MARCAS · bump chart del Lyst Index ───────── */
{
  const q = D.LYST.q, R = D.LYST.r;
  const PX = 128, PY = 300, PW = 716, PH = 330;
  const X = i => PX + (i / (q.length - 1)) * PW;
  const Y = r => PY + ((r - 1) / 19) * PH;
  const pick = [
    ['Off-White', '#B8503D'], ['Gucci', '#1F3A6E'], ['Loewe', '#1E7A52'],
    ['Miu Miu', '#C08A1E'], ['Prada', '#6B4A8F'], ['Balenciaga', '#8A8578']
  ];
  out.marcas = {
    box: { PX, PY, PW, PH },
    rows: [1, 5, 10, 15, 20].map(r => ({ r, y: r2(Y(r)) })),
    xticks: ['Q1-18', 'Q1-20', 'Q1-22', 'Q1-24', 'Q2-26'].map(l => ({ l, x: r2(X(q.indexOf(l))) })),
    lines: pick.map(([b, c]) => {
      const vals = R[b];
      const segs = segments(vals, X, Y);
      const firstI = vals.findIndex(v => v != null);
      const lastI = vals.length - 1 - [...vals].reverse().findIndex(v => v != null);
      return {
        b, c, d: segs.map(poly),
        first: { x: r2(X(firstI)), y: r2(Y(vals[firstI])) },
        last: { x: r2(X(lastI)), y: r2(Y(vals[lastI])) }
      };
    })
  };
}

/* ───────── 5 · RETORNOS · línea de tiempo de picos ───────── */
{
  const PX = 180, PW = 1140;
  const X = y => PX + (y - 2004) / 21 * PW;
  const items = [
    { n: 'Lunares', picos: [2008, 2024], int: '16 años' },
    { n: 'Cuero', picos: [2006, 2015, 2024], int: '9 años' },
    { n: 'Animal print', picos: [2007, 2016, 2025], int: '9 años' },
    { n: 'Encaje', picos: [2011, 2024], int: '13 años' },
    { n: 'Corset', picos: [2012, 2021], int: '9 años' },
    { n: 'Kimono', picos: [2013, 2022], int: '9 años' }
  ];
  out.ret = {
    PX, PW,
    xticks: [2004, 2009, 2014, 2019, 2025].map(y => ({ y, x: r2(X(y)) })),
    items: items.map((it, i) => ({
      n: it.n, int: it.int, y: 320 + i * 72,
      dots: it.picos.map(p => ({ x: r2(X(p)), year: p })),
      line: { x1: r2(X(it.picos[0])), x2: r2(X(it.picos[it.picos.length - 1])) }
    }))
  };
}

/* ───────── 6 · RADAR · paletas medidas y pista del ciclo ───────── */
{
  const C = D.COL;
  const cards = [
    { n: 'Jeans amplios', k: 'Corte', sw: ['denim', 'marino', 'celeste', 'gris'], et: 'En pico', p: 0.62, meta: '411 artículos en H&M · 15 colores' },
    { n: 'Jeans ajustados', k: 'Corte', sw: ['negro', 'denim', 'gris'], et: 'Saturada', p: 0.80, meta: '1.500 artículos · la paleta se cierra' },
    { n: 'Lunares', k: 'Estampa', sw: ['blanco', 'negro', 'rojo', 'beige'], et: 'En retorno', p: 0.95, meta: '168 prendas en 8 colores' },
    { n: 'Cuero', k: 'Material', sw: ['cuero', 'negro', 'marron'], et: 'En retorno', p: 0.95, meta: '87 % de las compras es sintético' },
    { n: 'Cargo', k: 'Pantalón', sw: ['verde', 'beige', 'gris'], et: 'En pico', p: 0.62, meta: 'Lyst: +56 % en búsquedas, 2022' },
    { n: 'Y2K', k: 'Estampa', sw: ['rosa', 'celeste', 'blanco'], et: 'En ascenso', p: 0.35, meta: '+203 % en búsquedas de compra' },
    { n: 'Encaje', k: 'Material', sw: ['blanco', 'negro', 'rosa'], et: 'En retorno', p: 0.95, meta: 'pico de pasarela 2011, vuelve 2024' },
    { n: 'Floral', k: 'Estampa', sw: ['celeste', 'amarillo', 'blanco'], et: 'En pico', p: 0.62, meta: 'sólo aparece en junio, los 5 años' }
  ];
  out.radar = cards.map(c => ({ ...c, hex: c.sw.map(k => C[k]) }));
}

fs.writeFileSync('geom.json', JSON.stringify(out));
const s = JSON.stringify(out);
console.log('geom.json escrito ·', (s.length / 1024).toFixed(1), 'KB');
console.log('det series:', out.det.series.map(x => x.k + '(' + x.d.length + ' tramos)').join(', '));
console.log('ciclo pts:', out.ciclo.pts.length, '| grupos:', out.ciclo.groups.map(g => g.n + ':' + g.items.length).join(' '));
console.log('rec end:', JSON.stringify(out.rec.end), 'start ajustado', out.rec.start.j);
console.log('marcas lines:', out.marcas.lines.map(l => l.b + '(' + l.d.length + ')').join(' '));
