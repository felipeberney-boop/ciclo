#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tres pruebas pedidas, con lo que realmente hay en el proyecto.

Qué se puede y qué no, dicho de entrada:

2 · PANEL MÁS GRANDE. No puedo sumar los 19 términos que faltan: están en el Drive del grupo y el
    conector no lista esa carpeta. Lo que sí puedo es construir y medir el MODELO GLOBAL —uno solo
    que aprende de las 16 series juntas en vez de una por serie— que es la técnica por la que un
    panel más grande serviría. Si el modelo global no le gana a nada con 16, sumar 19 más tampoco
    va a salvarlo; si le gana, es la evidencia para ir a buscarlos.

3 · UNA VARIABLE QUE NO SEA BÚSQUEDA. No hay serie temporal de ventas usable: la mensual del
    proyecto es del Zara 2018-22, que es sintético. Lo que sí hay es, por atributo, el cambio real
    en reseñas de Amazon 2019-2022 (`amz_19_22`) y en Google Shopping 2022-2025 (`shop_22_25`).
    Reseñas de Amazon es lo más cerca de compra que tenemos. Es una prueba transversal de 16 puntos,
    no una serie: chica, pero real.

5 · PASARELA MES A MES. No puedo: eso exige volver al parquet de Vogue, que no está en el proyecto.
    Lo que sí hago es la versión fuerte del test anual que ya habíamos corrido: ATRIBUTO POR
    ATRIBUTO en vez de promediado. El promedio puede estar tapando que la pasarela sí adelante en
    algunos y no en otros.
"""
import json
import math
import statistics as st
import itertools

d = json.load(open('datos_app.json', encoding='utf-8'))
REC = [r for r in d['REC'] if r.get('g') and len(r['g']) == 22 and all(v is not None for v in r['g'])]
ANIOS = list(range(2004, 2026))


def corr(x, y):
    n = len(x)
    if n < 4:
        return None
    mx, my = st.mean(x), st.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (sx * sy) if sx and sy else None


def detrendar(series):
    n = len(series[0])
    med = [st.median(s[i] for s in series) for i in range(n)]
    out = []
    for s in series:
        rel = [s[i] / med[i] if med[i] else 0.0 for i in range(n)]
        m = max(rel) or 1.0
        out.append([100 * v / m for v in rel])
    return out


S = detrendar([[float(v) for v in r['g'][:21]] for r in REC])   # 2004-2024, sin el 2025 contaminado


# ══════════════════ 2 · modelo global ══════════════════
# Aprende UNA regla para las 16 series: dado el recorrido reciente (normalizado),
# ¿cuánto se mueve en h años? Se entrena con todas las series menos la que se evalúa.

V = 5   # ventana de entrada


def rasgos(seg):
    """Recorrido reciente, en forma: nivel relativo y tres pendientes."""
    base = seg[-1] or 1e-9
    return [
        seg[-1] / (max(seg) or 1e-9),                 # qué tan cerca está de su propio techo
        (seg[-1] - seg[-2]) / 100,                    # último cambio
        (seg[-1] - seg[-3]) / 200,                    # cambio a 2 años
        (st.mean(seg[-2:]) - st.mean(seg[:2])) / 100, # pendiente de la ventana
    ]


def muestras(series, h, excluir=None):
    X, Y = [], []
    for i, y in enumerate(series):
        if excluir is not None and i == excluir:
            continue
        for t in range(V, len(y) - h):
            X.append(rasgos(y[t - V:t]))
            Y.append(y[t + h] - y[t])        # el cambio a predecir
    return X, Y


def ols(X, Y):
    """Mínimos cuadrados con término independiente, resuelto por eliminación gaussiana."""
    k = len(X[0]) + 1
    A = [[0.0] * (k + 1) for _ in range(k)]
    for xi, yi in zip(X, Y):
        v = [1.0] + list(xi)
        for a in range(k):
            for b in range(k):
                A[a][b] += v[a] * v[b]
            A[a][k] += v[a] * yi
    for c in range(k):                                   # gauss con pivoteo
        p = max(range(c, k), key=lambda r: abs(A[r][c]))
        if abs(A[p][c]) < 1e-12:
            return None
        A[c], A[p] = A[p], A[c]
        for r in range(k):
            if r != c:
                f = A[r][c] / A[c][c]
                for b in range(c, k + 1):
                    A[r][b] -= f * A[c][b]
    return [A[r][k] / A[r][r] for r in range(k)]


def predecir(coef, xi):
    return coef[0] + sum(coef[j + 1] * xi[j] for j in range(len(xi)))


print('═══ 2 · modelo global: una regla aprendida de las 16 series juntas ═══')
print('   validación «dejando una serie afuera»: se entrena sin el atributo que se evalúa\n')
print(f'{"h":>2} {"EAM global":>11} {"EAM ingenua":>12} {"mejora":>8}   {"dirección":>10} {"base":>7}  n')
glob = {}
for h in (1, 2, 3, 5):
    em, ei, ok, tot, may = [], [], 0, 0, [0, 0]
    for i, y in enumerate(S):
        Xtr, Ytr = muestras(S, h, excluir=i)
        coef = ols(Xtr, Ytr)
        if not coef:
            continue
        for t in range(V, len(y) - h):
            pr = y[t] + predecir(coef, rasgos(y[t - V:t]))
            real = y[t + h]
            em.append(abs(pr - real))
            ei.append(abs(y[t] - real))
            dr, dp = real - y[t], pr - y[t]
            if abs(dr) >= 5:
                tot += 1
                ok += (dr > 0) == (dp > 0)
                may[dr > 0] += 1
    mej = 100 * (st.mean(ei) - st.mean(em)) / st.mean(ei)
    glob[h] = dict(eam=round(st.mean(em), 2), base=round(st.mean(ei), 2), mejora=round(mej, 1),
                   dir=round(100 * ok / tot, 1), base_dir=round(100 * max(may) / tot, 1), n=tot)
    print(f'{h:>2} {st.mean(em):>11.2f} {st.mean(ei):>12.2f} {mej:>+7.1f}%   '
          f'{100*ok/tot:>9.1f}% {100*max(may)/tot:>6.1f}%  {tot}')


# ══════════════════ 3 · ¿la búsqueda se relaciona con algo comercial? ══════════════════
print('\n═══ 3 · una variable que no es búsqueda: reseñas de Amazon y Google Shopping ═══')
KM = {r['n']: r for r in d['KM']['rows']}
NOMBRE = {r['id']: r['n'] for r in REC}

filas = []
for i, r in enumerate(REC):
    k = KM.get(r['n']) or KM.get(r['n'].replace('Buzo / athleisure', 'Buzo / hoodie'))
    if not k:
        continue
    g = S[i]
    filas.append(dict(
        id=r['id'], n=r['n'],
        nivel=g[-1],                                   # nivel de búsqueda 2024, detrendado
        momento=st.mean(g[-3:]) - st.mean(g[-6:-3]),   # momento de búsqueda
        pn=k.get('pn'), pm=k.get('pm'),
        amz=k.get('amz_19_22'), shop=k.get('shop_22_25')))

for objetivo, etiqueta in (('amz', 'reseñas de Amazon 2019-2022'), ('shop', 'Google Shopping 2022-2025')):
    sub = [f for f in filas if f[objetivo] is not None]
    print(f'\n  {etiqueta}  ·  n = {len(sub)} atributos')
    for pred, nom in (('nivel', 'nivel de búsqueda'), ('momento', 'momento de búsqueda'),
                      ('pn', 'nivel de pasarela'), ('pm', 'momento de pasarela')):
        xs = [f[pred] for f in sub if f[pred] is not None]
        ys = [f[objetivo] for f in sub if f[pred] is not None]
        c = corr(xs, ys)
        if c is None:
            continue
        # significancia aproximada: |r| que hace falta con n puntos, al 5 %
        n = len(xs)
        critico = 1.96 / math.sqrt(n - 1)
        marca = '✓' if abs(c) > critico else '·'
        print(f'    {nom:<22} r = {c:+.3f}   (hace falta |r| > {critico:.2f})  {marca}')


# ══════════════════ 5 · la pasarela, atributo por atributo ══════════════════
print('\n═══ 5 · ¿la pasarela adelanta? ahora atributo por atributo, no promediado ═══')
print(f'{"atributo":<12} ' + ' '.join(f'k={k}'.rjust(7) for k in range(0, 5)) + '   mejor')
mejores = []
for r in REC:
    v = r.get('v')
    if not v:
        continue
    fila, cs = [], {}
    for k in range(0, 5):
        idx = [i for i in range(len(v)) if v[i] is not None and i + k < 22]
        if len(idx) < 8:
            fila.append('   —')
            continue
        c = corr([v[i] for i in idx], [r['g'][i + k] for i in idx])
        cs[k] = c
        fila.append(f'{c:+7.2f}' if c is not None else '   —')
    if cs:
        mk = max(cs, key=lambda k: cs[k])
        mejores.append((r['id'], mk, cs[mk]))
        print(f'{r["id"]:<12} ' + ' '.join(fila) + f'   k={mk} ({cs[mk]:+.2f})')

print()
cnt = {}
for _, k, c in mejores:
    cnt[k] = cnt.get(k, 0) + 1
print('  rezago que maximiza la correlación, por atributo:',
      ', '.join(f'k={k}: {n}' for k, n in sorted(cnt.items())))
adelanta = [m for m in mejores if m[1] >= 2 and m[2] > 0.5]
print(f'  atributos donde la pasarela adelanta 2+ años con r > 0,5: {len(adelanta)} de {len(mejores)}')
if adelanta:
    print('   ', ', '.join(f'{a[0]} (k={a[1]}, r={a[2]:+.2f})' for a in adelanta))

json.dump({'global': glob,
           'comercial': filas,
           'pasarela_por_atributo': [{'id': a, 'mejor_rezago': b, 'r': round(c, 3)} for a, b, c in mejores]},
          open('tres_pruebas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nescrito: tres_pruebas.json')
