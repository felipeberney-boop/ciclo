const fs = require('fs');
const s = fs.readFileSync('app_recuperada.html', 'utf8');
const js = s.slice(s.indexOf('<script>') + 8, s.lastIndexOf('</script>'));

function grab(name) {
  const key = 'const ' + name + '=';
  const i = js.indexOf(key);
  if (i < 0) return null;
  let j = i + key.length;
  const st = j;
  let depth = 0, inS = false, q = '';
  for (; j < js.length; j++) {
    const c = js[j];
    if (inS) { if (c === '\\') { j++; continue; } if (c === q) inS = false; continue; }
    if (c === "'" || c === '"' || c === '`') { inS = true; q = c; continue; }
    if (c === '[' || c === '{' || c === '(') depth++;
    else if (c === ']' || c === '}' || c === ')') depth--;
    else if (c === ';' && depth === 0) break;
  }
  return js.slice(st, j);
}

const out = {};
for (const n of ['REC', 'JE', 'KM', 'LYST', 'COL', 'RDS', 'SERIE', 'HIST', 'KST', 'KPROTO']) {
  const src = grab(n);
  if (!src) { console.log('falta', n); continue; }
  try { out[n] = eval('(' + src + ')'); }
  catch (e) { console.log('ERR', n, e.message.slice(0, 70)); }
}
fs.writeFileSync('datos_app.json', JSON.stringify(out));
console.log('OK:', Object.keys(out).join(' '));
if (out.REC) console.log('REC:', out.REC.map(r => r.id + '/' + r.tipo).join(', '));
if (out.KM) console.log('KM keys:', Object.keys(out.KM).join(','), '| rows:', out.KM.rows && out.KM.rows.length);
if (out.JE) console.log('JE keys:', Object.keys(out.JE).join(','));
