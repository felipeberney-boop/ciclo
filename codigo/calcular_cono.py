"""El cono de 2030: cuánto se movió realmente la búsqueda a cada distancia. No es un pronóstico.

Reproduce, sin dependencias, el cono de datasets_procesados/ciclo_cono__incertidumbre_medida.json
(calculado en la otra copia del repo con un módulo `proyeccion` que no se subió). Mismo método:

1. Las 16 series de búsqueda mundial (REC[].g), 2004–2024. 2025 y 2026 quedan fuera: salto de medición
   de Google (en 2025 el cambio medio es +18,9 contra +3,2 histórico y 12 de 16 series tocan su máximo).
2. Detrend: cada año se divide por la mediana de los 16 atributos de ese año, para sacar la deriva
   común de Google, y cada serie se lleva a su propio máximo (0–100).
3. Para cada distancia h = 1…6 se toman todos los tramos (t, t+h) con origen desde 2010 y se guardan
   los percentiles 5, 20, 50, 80 y 95 del cambio y el error absoluto medio de repetir el último valor.

Uso (desde la raíz del repo): python3 codigo/calcular_cono.py
Compara su resultado con el JSON guardado y avisa si alguna cifra difiere en más de 0,1."""
import json, statistics as st

d = json.load(open('datasets_procesados/ciclo_series__anual_por_atributo.json'))
guardado = json.load(open('datasets_procesados/ciclo_cono__incertidumbre_medida.json'))
ids = list(guardado['attr'])
R = {r['id']: r for r in d['REC']}
Y = list(range(2004, 2025))
raw = {i: [R[i]['g'][y - 2004] for y in Y] for i in ids}
med = [st.median(raw[i][k] for i in ids) for k in range(len(Y))]
X = {}
for i in ids:
    x = [raw[i][k] / med[k] for k in range(len(Y))]
    m = max(x); X[i] = [100 * v / m for v in x]

def pct(xs, p):
    xs = sorted(xs); k = (len(xs) - 1) * p / 100; lo = int(k); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)

ok = True
for h in range(1, 7):
    dl = [X[i][k + h] - X[i][k] for i in ids for k in range(len(Y)) if Y[k] >= 2010 and k + h < len(Y)]
    q = {p: round(pct(dl, p), 1) for p in (5, 20, 50, 80, 95)}
    eam = round(st.mean(abs(v) for v in dl), 2)
    g = guardado['cono'][str(h)]
    igual = len(dl) == g['n'] and abs(eam - g['eam']) < .02 and all(abs(q[p] - g['q'][str(p)]) <= .11 for p in q)
    ok &= igual
    print(f'h={h} ({2024 + h})  n={len(dl)}  mediana {q[50]:+.1f}  20–80: {q[20]:+.1f} a {q[80]:+.1f}  error ±{eam}  {"= guardado" if igual else "DIFIERE"}')
print('el cono guardado se reproduce' if ok else 'ATENCIÓN: el cono guardado no se reproduce')
