#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La prueba que CICLO nunca pudo correr: ¿la búsqueda predice la VENTA?

Hasta ahora predecíamos búsqueda con búsqueda, que es un proxy. VISUELLE trae 5.577 productos de
Nunalie con sus ventas semanales reales y la serie de Google Trends del atributo correspondiente,
ya alineadas. Con eso se puede preguntar lo que el diseñador realmente pregunta.

Diseño de la prueba:
  - cada producto tiene 12 semanas de venta desde su salida; el objetivo es el total
  - los predictores salen de la búsqueda del atributo EN LAS SEMANAS ANTERIORES a la salida,
    nunca de las posteriores: si usáramos las de después sería hacer trampa
  - se entrena con las temporadas viejas y se prueba con las nuevas, nunca al revés
  - la base contra la que hay que ganar es «predecí el promedio de la categoría», que es lo que
    cualquiera haría sin modelo
"""
import csv
import math
import statistics as st
from datetime import date

BASE = '/home/claude/visuelle/'
SEM_ANTES = 12          # ventana de búsqueda previa a la salida
SEMANAS = [str(i) for i in range(12)]


def f(x):
    try:
        return float(x)
    except Exception:
        return None


def leer_fecha(s):
    s = s.strip()[:10].replace('/', '-')
    p = s.split('-')
    return date(int(p[0]), int(p[1]), int(p[2])) if len(p) == 3 else None


# ── búsqueda semanal por término ──
gr = list(csv.reader(open(BASE + 'gtrends.csv', encoding='utf-8')))
cab = [c.strip() for c in gr[0]]
fechas = [leer_fecha(r[0]) for r in gr[1:]]
series = {}
for j, nom in enumerate(cab[1:], start=1):
    if not nom:
        continue
    series[nom] = [f(r[j]) if j < len(r) else None for r in gr[1:]]

# ── productos ──
prods = []
for arch in ('train.csv', 'test.csv'):
    for r in csv.DictReader(open(BASE + arch, encoding='utf-8')):
        v = [f(r[k]) for k in SEMANAS]
        if any(x is None for x in v):
            continue
        fe = leer_fecha(r['release_date'])
        if not fe:
            continue
        prods.append(dict(total=sum(v), cat=r['category'].strip(), col=r['color'].strip(),
                          fab=r['fabric'].strip(), fecha=fe, temp=r['season'].strip()))

print(f'productos: {len(prods)}   ·   términos de búsqueda: {len(series)}')
print(f'ventas: mediana {st.median(p["total"] for p in prods):.3f}  '
      f'min {min(p["total"] for p in prods):.3f}  max {max(p["total"] for p in prods):.3f}')
cats = {p['cat'] for p in prods}
print(f'categorías con serie de búsqueda: {len(cats & set(series))} de {len(cats)}\n')


def rasgos(term, fe):
    """Nivel y pendiente de la búsqueda en las semanas ANTERIORES a la salida."""
    s = series.get(term)
    if not s:
        return None
    idx = [i for i, d in enumerate(fechas) if d and d < fe and s[i] is not None]
    if len(idx) < SEM_ANTES:
        return None
    ult = idx[-SEM_ANTES:]
    vals = [s[i] for i in ult]
    nivel = st.mean(vals)
    mitad = SEM_ANTES // 2
    pend = st.mean(vals[mitad:]) - st.mean(vals[:mitad])
    maxh = max(s[i] for i in idx) or 1.0
    return dict(nivel=nivel, pend=pend, rel=nivel / maxh)


for p in prods:
    p['r_cat'] = rasgos(p['cat'], p['fecha'])
    p['r_col'] = rasgos(p['col'], p['fecha'])
    p['r_fab'] = rasgos(p['fab'], p['fecha'])

usables = [p for p in prods if p['r_cat']]
print(f'productos con búsqueda previa utilizable: {len(usables)}\n')


def corr(x, y):
    n = len(x)
    if n < 5:
        return None
    mx, my = st.mean(x), st.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (sx * sy) if sx and sy else None


print('═══ 1 · ¿la búsqueda previa correlaciona con la venta? ═══')
for clave, nom in (('r_cat', 'categoría'), ('r_col', 'color'), ('r_fab', 'tejido')):
    sub = [p for p in usables if p[clave]]
    if len(sub) < 30:
        continue
    print(f'\n  búsqueda de {nom}  ·  n = {len(sub)}')
    for campo, et in (('nivel', 'nivel'), ('pend', 'pendiente'), ('rel', 'nivel sobre su máximo')):
        c = corr([p[clave][campo] for p in sub], [p['total'] for p in sub])
        crit = 1.96 / math.sqrt(len(sub) - 1)
        print(f'    {et:<24} r = {c:+.3f}   (umbral {crit:.3f})  {"✓" if abs(c) > crit else "·"}')

# ── 2 · prueba fuera de muestra, entrenando con lo viejo ──
print('\n═══ 2 · fuera de muestra: entrenar con temporadas viejas, predecir las nuevas ═══')
VIEJAS = {'SS17', 'AW17', 'SS18', 'AW18'}
NUEVAS = {'SS19', 'AW19'}
tr = [p for p in usables if p['temp'] in VIEJAS]
te = [p for p in usables if p['temp'] in NUEVAS]
print(f'  entrenamiento {len(tr)} productos · prueba {len(te)}')


def ols(X, Y):
    k = len(X[0]) + 1
    A = [[0.0] * (k + 1) for _ in range(k)]
    for xi, yi in zip(X, Y):
        v = [1.0] + list(xi)
        for a in range(k):
            for b in range(k):
                A[a][b] += v[a] * v[b]
            A[a][k] += v[a] * yi
    for c in range(k):
        pv = max(range(c, k), key=lambda r: abs(A[r][c]))
        if abs(A[pv][c]) < 1e-12:
            return None
        A[c], A[pv] = A[pv], A[c]
        for r in range(k):
            if r != c:
                fa = A[r][c] / A[c][c]
                for b in range(c, k + 1):
                    A[r][b] -= fa * A[c][b]
    return [A[r][k] / A[r][r] for r in range(k)]


X = [[p['r_cat']['nivel'], p['r_cat']['pend'], p['r_cat']['rel']] for p in tr]
Y = [p['total'] for p in tr]
coef = ols(X, Y)

med_cat = {}
for p in tr:
    med_cat.setdefault(p['cat'], []).append(p['total'])
med_cat = {k: st.mean(v) for k, v in med_cat.items()}
media_global = st.mean(Y)

em_mod, em_cat, em_glob = [], [], []
for p in te:
    r = p['r_cat']
    pred = coef[0] + coef[1] * r['nivel'] + coef[2] * r['pend'] + coef[3] * r['rel']
    em_mod.append(abs(pred - p['total']))
    em_cat.append(abs(med_cat.get(p['cat'], media_global) - p['total']))
    em_glob.append(abs(media_global - p['total']))

print(f'\n  {"EAM modelo con búsqueda":<34} {st.mean(em_mod):.4f}')
print(f'  {"EAM promedio de la categoría":<34} {st.mean(em_cat):.4f}')
print(f'  {"EAM promedio global":<34} {st.mean(em_glob):.4f}')
mejor_base = min(st.mean(em_cat), st.mean(em_glob))
print(f'\n  mejora sobre la mejor base: {100*(mejor_base-st.mean(em_mod))/mejor_base:+.1f} %')
print(f'  coeficientes: intercepto {coef[0]:+.4f} · nivel {coef[1]:+.5f} · '
      f'pendiente {coef[2]:+.5f} · nivel/máx {coef[3]:+.4f}')
