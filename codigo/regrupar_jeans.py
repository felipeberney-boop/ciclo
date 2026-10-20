"""CICLO · reagrupa los jeans según la taxonomía (20/10/2026): mom y boyfriend dejan de ser «amplios" y pasan a «medios",
porque mom es un straight de tiro alto relajado y boyfriend un tapered relajado. Uso: python3 codigo/regrupar_jeans.py

Qué recalcula, en este orden:
1. JE.defs y JE.web (suma de las participaciones de cada término, como antes).
2. La serie mundial de amplios y medios (trends_mundo__web_anual.csv, jamplio y jmedio). No hay volumen absoluto de cada
   término, pero sí la participación (JE.terms) y la serie de cada grupo normalizada a 100: el volumen total de jeans sale
   de serie / participación en cada grupo (llevado a su máximo y promediado entre los tres), y el grupo nuevo es
   participación nueva × total, otra vez llevado a 100. Ajustados no cambia (mismos términos) y sirve de control.
3. REC[jamplio|jmedio].g y GREL de los 16 (cada año dividido por la mediana de los 16, sobre su máximo desde 2010:
   la mediana cambia, así que se regeneran todos).
Después hay que correr codigo/recalcular_kmeans_sin_2025.py y codigo/armar_datos_llm.js."""
import csv, json, re, statistics as st

H = 'app/index.html'
CSV = 'datasets_procesados/series_google_trends/trends_mundo__web_anual.csv'
h = open(H).read()

def const(n):  # el JSON de `const n=…;` (puede haber un comentario después del punto y coma)
    i = h.index('\nconst ' + n + '=') + 1 + len('const ' + n + '=')
    v, j = json.JSONDecoder().raw_decode(h, i)
    return i, j, v

def poner(n, v):
    global h
    i, j, _ = const(n); h = h[:i] + json.dumps(v, ensure_ascii=False, separators=(',', ':')) + h[j:]

_, _, JE = const('JE'); _, _, REC = const('REC'); _, _, GREL = const('GREL')
Y = JE['Y']
NUEVO = {'ajustado': ['skinny', 'slim', 'jeggings'], 'medio': ['straight leg', 'bootcut', 'flare', 'tapered', 'mom', 'boyfriend'],
         'amplio': ['baggy', 'wide leg', 'barrel', 'relaxed fit']}
suma = lambda ts: [round(sum(JE['terms'][t][i] for t in ts), 1) for i in range(len(Y))]
viejo = {g: JE['web'][g] for g in JE['web']}

filas = list(csv.DictReader(open(CSV)))
W = {}
for r in filas: W.setdefault(r['atributo_id'], {})[int(r['anio'])] = float(r['indice_0_100'])
ID = {'amplio': 'jamplio', 'medio': 'jmedio', 'ajustado': 'jajust'}

# volumen total de jeans, a escala, desde cada grupo
est = []
for g, aid in ID.items():
    e = [W[aid][y] / viejo[g][i] if viejo[g][i] > 0 else None for i, y in enumerate(Y)]
    mx = max(x for x in e if x is not None); est.append([x / mx if x is not None else None for x in e])
T = [st.mean([e[i] for e in est if e[i] is not None]) for i in range(len(Y))]
nuevo = {g: suma(ts) for g, ts in NUEVO.items()}
def serie(g):
    v = [T[i] * nuevo[g][i] for i in range(len(Y))]; mx = max(v); return [round(x / mx * 100, 1) for x in v]
control = serie('ajustado')
err = max(abs(a - W['jajust'][y]) for a, y in zip(control, Y))
print(f'control: ajustados reconstruidos contra la serie medida, error máximo {err:.1f} puntos sobre 100')
assert err < 8, 'la reconstrucción del total no cierra'
for g in ('amplio', 'medio'):
    for v, y in zip(serie(g), Y): W[ID[g]][y] = v

# 1. JE
JE['defs'] = NUEVO; JE['web'] = {g: nuevo[g] for g in ('ajustado', 'medio', 'amplio')}
poner('JE', JE)
# 2. el CSV
for r in filas:
    if r['atributo_id'] in ('jamplio', 'jmedio'): r['indice_0_100'] = W[r['atributo_id']][int(r['anio'])]
with open(CSV, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0].keys())); w.writeheader(); w.writerows(filas)
# 3. REC.g y GREL
for o in REC:
    if o['id'] in ('jamplio', 'jmedio'): o['g'] = [W[o['id']][y] for y in Y]
poner('REC', REC)
med = {y: st.median(W[k][y] for k in W) for y in Y}
for k in GREL:
    rel = {y: W[k][y] / med[y] for y in Y}; mx = max(rel[y] for y in Y if y >= 2010)
    GREL[k] = [round(rel[y] / mx * 100, 1) if y >= 2010 else GREL[k][i] for i, y in enumerate(Y)]
poner('GREL', GREL)
open(H, 'w').write(h)
print('2025 · amplios', JE['web']['amplio'][-1], '(antes', viejo['amplio'][-1], ') · medios', JE['web']['medio'][-1], '(antes', viejo['medio'][-1], ')')
