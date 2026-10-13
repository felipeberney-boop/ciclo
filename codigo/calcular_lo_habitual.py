"""«Lo habitual» hasta 2030: cuánto se movieron históricamente las curvas de cada capa a 1, 2, 3… años.

No es un modelo ni un pronóstico. Para cada capa (pasarela, búsqueda mundo, búsqueda Argentina, Reddit) toma
todos los pares (año t, año t+h) de todas las curvas de REC y guarda la mediana y los percentiles 10, 25, 75 y
90 del cambio, en puntos del índice 0–100. En la app, la línea punteada es el último valor + la mediana, y las
bandas son el último valor + esos percentiles: cuánto se movieron de verdad las series a esa distancia.

Backtest: para cada año de origen se usan sólo los pares que terminan antes de ese año, y se compara contra
repetir el último valor (error absoluto medio) y contra acertar la dirección del cambio.

Uso (desde la raíz del repo): python3 codigo/calcular_lo_habitual.py
Escribe datasets/completado_2026/lo_habitual_hasta_2030.csv y app/clip/../ nada: la tabla va pegada en la app."""
import json, csv, statistics as st

d = json.load(open('datasets_procesados/ciclo_series__anual_por_atributo.json'))
Y0 = 2004
CAPAS = {'v': ('Pasarela', 2023), 'g': ('Búsqueda mundo', 2025), 'a': ('Búsqueda Argentina', 2025), 'r': ('Reddit', 2025)}
HMAX = 7

def serie(r, k):
    vals = r.get(k)
    return {Y0 + i: x for i, x in enumerate(vals or []) if x is not None}

def pct(xs, q):
    xs = sorted(xs); i = (len(xs) - 1) * q; lo = int(i); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)

filas, tabla, back = [], {}, {}
for k, (nombre, base) in CAPAS.items():
    S = [serie(r, k) for r in d['REC'] if serie(r, k)]
    hmax = min(HMAX, 2030 - base)
    tabla[k] = {'base': base, 'd': []}
    for h in range(1, hmax + 1):
        dl = [s[t + h] - s[t] for s in S for t in s if t + h in s]
        if len(dl) < 10: break
        q = [round(st.median(dl), 1)] + [round(pct(dl, p), 1) for p in (.10, .25, .75, .90)]
        tabla[k]['d'].append([h] + q)
        filas.append([k, nombre, base, h, base + h, len(dl)] + q)
    # backtest con orígenes 2012–2022: sólo pares que terminan antes del origen
    e_hab, e_rep, dir_ok, n = [], [], 0, 0
    for o in range(2012, 2023):
        for h in range(1, 4):
            dl = [s[t + h] - s[t] for s in S for t in s if t + h in s and t + h <= o]
            if len(dl) < 10: continue
            m = st.median(dl)
            for s in S:
                if o in s and o + h in s:
                    real = s[o + h] - s[o]
                    e_hab.append(abs(m - real)); e_rep.append(abs(real))
                    if real != 0: dir_ok += (m > 0) == (real > 0); n += 1
    back[k] = (round(sum(e_hab) / len(e_hab), 1), round(sum(e_rep) / len(e_rep), 1), round(100 * dir_ok / n, 1), len(e_hab))

with open('datasets/completado_2026/lo_habitual_hasta_2030.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['capa', 'nombre', 'ultimo_anio_medido', 'distancia_anios', 'anio', 'pares', 'mediana', 'p10', 'p25', 'p75', 'p90'])
    w.writerows(filas)
print('const HAB=' + json.dumps(tabla, separators=(',', ':')) + ';')
print('backtest (orígenes 2012–2022, h=1–3) · error «lo habitual» / error «repetir el último» / dirección acertada % / n:')
for k, v in back.items(): print(' ', CAPAS[k][0], v)
