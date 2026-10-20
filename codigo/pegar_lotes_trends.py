"""CICLO · pega los lotes de Google Trends del plan (datasets/plan_exportacion_trends.csv) a la serie anual mundial.
Uso: python3 codigo/pegar_lotes_trends.py   (lee datasets/trends_lotes/lote_01.csv … lote_09.csv)

Cada lote es el CSV que baja Google Trends desde «Interés a lo largo del tiempo» (multiTimeline): trench coat + 4 términos,
mundial, «2004 – presente». Trench coat es el ancla: ya está medido en trends_mundo__web_anual.csv.
1. Promedio anual 2004–2025 (2026 se excluye, como el resto). «<1» cuenta como 0,5.
2. El ancla valida el pegado: el trench del lote tiene que correlacionar ≥ 0,95 con el trench medido; si no, el lote no entra.
3. Cada término se lleva a la escala del ancla (mediana del cociente trench medido / trench del lote) y después a su propio
   máximo (0–100), igual que las 16 series que ya hay.
4. No entra si vuelve plano o con menos de 12 años útiles (≥ 1): queda prestado, y se anota en datasets/trends_lotes/informe.md.
Escribe las filas nuevas en trends_mundo__web_anual.csv con atributo_id = la hoja de la taxonomía (p. ej. «faldas_mini»).
La mediana de GREL sigue siendo la de las 16 series originales, para que sumar series no mueva las que ya estaban."""
import csv, glob, os, re, statistics as st

BASE = 'datasets_procesados/series_google_trends/trends_mundo__web_anual.csv'
PLAN = {r['termino']: r for r in csv.DictReader(open('datasets/plan_exportacion_trends.csv'))}
Y = list(range(2004, 2026))
filas = list(csv.DictReader(open(BASE)))
trench = {int(r['anio']): float(r['indice_0_100']) for r in filas if r['atributo_id'] == 'trench'}

def leer_lote(ruta):
    lineas = [l for l in open(ruta, encoding='utf-8-sig').read().splitlines() if l.strip()]
    i = next(k for k, l in enumerate(lineas) if re.match(r'^(Month|Mes|Semana|Week)', l, re.I))
    cab = next(csv.reader([lineas[i]]))
    nombres = [re.sub(r'\s*:\s*\(.*\)$', '', c).strip().lower() for c in cab[1:]]
    anual = {n: {} for n in nombres}
    for fila in csv.reader(lineas[i + 1:]):
        y = int(fila[0][:4])
        if y > 2025: continue
        for n, v in zip(nombres, fila[1:]):
            anual[n].setdefault(y, []).append(0.5 if v.strip() == '<1' else float(v or 0))
    return {n: {y: st.mean(v) for y, v in d.items()} for n, d in anual.items()}

informe, nuevas = [], []
for ruta in sorted(glob.glob('datasets/trends_lotes/lote_*.csv')):
    L = leer_lote(ruta); a = L.get('trench coat')
    if not a: informe.append(f'- {ruta}: sin columna «trench coat», no entra.'); continue
    ys = [y for y in Y if y in a and a[y] > 0]
    r = st.correlation([a[y] for y in ys], [trench[y] for y in ys])
    if r < 0.95: informe.append(f'- {ruta}: el ancla no pega (r = {r:.2f}), no entra.'); continue
    k = st.median(trench[y] / a[y] for y in ys)
    for termino, serie in L.items():
        if termino == 'trench coat': continue
        if termino not in PLAN: informe.append(f'- {termino} ({ruta}): no está en el plan, se ignora.'); continue
        v = {y: serie.get(y, 0) * k for y in Y}; mx = max(v.values()) or 1
        utiles = sum(1 for y in Y if serie.get(y, 0) >= 1)
        plana = st.pstdev(v.values()) / mx < 0.05
        if utiles < 12 or plana:
            informe.append(f'- {termino}: {"plana" if plana else f"{utiles} años útiles"}, no entra; sigue prestado.'); continue
        hoja = PLAN[termino]['hoja_taxonomia']; aid = hoja.split(':')[1].replace('/', '_')
        nuevas += [dict(atributo_id=aid, atributo=termino, termino_buscado=termino, anio=y, indice_0_100=round(v[y] / mx * 100, 1)) for y in Y]
        informe.append(f'- {termino} → {hoja}: entra ({utiles} años útiles, ancla r = {r:.2f}).')

ids = {f['atributo_id'] for f in nuevas}
filas = [f for f in filas if f['atributo_id'] not in ids] + nuevas
with open(BASE, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['atributo_id', 'atributo', 'termino_buscado', 'anio', 'indice_0_100']); w.writeheader(); w.writerows(filas)
os.makedirs('datasets/trends_lotes', exist_ok=True)
open('datasets/trends_lotes/informe.md', 'w').write('# Lotes de Google Trends: qué entró y qué no\n\n' + '\n'.join(informe) + '\n')
print('\n'.join(informe)); print(f'{len(ids)} series nuevas en {BASE}')
