"""Proyección de la serie de pasarela (REC[].v, Vogue Runway, 2010–2023) a 2024–2026.
Elige el método por backtest: origen en 2016..2020, horizontes 1..3, error absoluto medio sobre todos
los atributos. El intervalo sale de los errores del backtest del método elegido (percentiles 10 y 90)."""
import json, sys, csv, statistics as st

repo, out_csv, out_json = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(repo + '/datasets_procesados/ciclo_series__anual_por_atributo.json'))
Y0 = 2004
series = {}
for r in d['REC']:
    v = r.get('v')
    if not v: continue
    pts = [(Y0 + i, x) for i, x in enumerate(v) if x is not None]
    series[r['id']] = (r['n'], r.get('vk'), dict(pts))

def naive(h, H): return [h[-1]] * H
def media3(h, H): return [sum(h[-3:]) / 3] * H
def lineal5(h, H):
    y = h[-5:]; n = len(y); xm = (n - 1) / 2; ym = sum(y) / n
    b = sum((i - xm) * (v - ym) for i, v in enumerate(y)) / sum((i - xm) ** 2 for i in range(n))
    return [ym + b * (n - 1 - xm + k) for k in range(1, H + 1)]
def holt(alpha, beta, phi):
    def f(h, H):
        l, b = h[0], h[1] - h[0]
        for y in h[1:]:
            l0 = l; l = alpha * y + (1 - alpha) * (l + phi * b); b = beta * (l - l0) + (1 - beta) * phi * b
        out, s = [], 0
        for k in range(1, H + 1):
            s += phi ** k; out.append(l + s * b)
        return out
    return f
metodos = {'ingenuo (último año)': naive, 'media de los últimos 3': media3, 'tendencia lineal 5 años': lineal5}
for a in (.3, .5, .7):
    for b in (.1, .3):
        for p in (.6, .8, .9):
            metodos[f'Holt amortiguado a={a} b={b} phi={p}'] = holt(a, b, p)

def clip(x): return max(0.0, min(100.0, x))
def backtest(f):
    errs = {1: [], 2: [], 3: []}
    for _, _, s in series.values():
        for o in range(2016, 2021):
            h = [s[y] for y in sorted(s) if y <= o]
            if len(h) < 5: continue
            for k, p in enumerate(f(h, 3), 1):
                if o + k in s: errs[k].append(clip(p) - s[o + k])
    return errs
res = {}
for n, f in metodos.items():
    e = backtest(f); todos = [abs(x) for k in e for x in e[k]]
    res[n] = (sum(todos) / len(todos), e)
orden = sorted(res, key=lambda n: res[n][0])
mejor = orden[0]
print('MAE backtest (puntos sobre 100):')
for n in orden[:5] + ['ingenuo (último año)']: print(f'  {res[n][0]:5.1f}  {n}')

def pct(xs, q):
    xs = sorted(xs); i = (len(xs) - 1) * q; lo = int(i); return xs[lo] + (xs[min(lo + 1, len(xs) - 1)] - xs[lo]) * (i - lo)
errs = res[mejor][1]
banda = {k: (pct(errs[k], .1), pct(errs[k], .9)) for k in errs}

f = metodos[mejor]
filas, js = [], {}
for rid, (n, vk, s) in series.items():
    h = [s[y] for y in sorted(s)]
    for y in sorted(s):
        filas.append([rid, n, vk, y, round(s[y], 1), '', '', 'medido', 'Vogue Runway'])
    pr = f(h, 3); js[rid] = {}
    for k, p in enumerate(pr, 1):
        lo, hi = banda[k]
        # el error es (proyectado − real): real ≈ proyectado − error
        fila = [rid, n, vk, 2023 + k, round(clip(p), 1), round(clip(p - hi), 1), round(clip(p - lo), 1), 'proyectado', mejor]
        filas.append(fila); js[rid][2023 + k] = fila[4:7]
with open(out_csv, 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['id', 'atributo', 'tag_vogue', 'anio', 'valor', 'min_80', 'max_80', 'tipo', 'fuente_o_metodo'])
    w.writerows(filas)
json.dump({'metodo': mejor, 'mae_backtest': round(res[mejor][0], 1), 'mae_ingenuo': round(res['ingenuo (último año)'][0], 1),
           'n_errores': sum(len(v) for v in errs.values()),
           'ranking': [[n, round(res[n][0], 2)] for n in orden], 'proyeccion': js}, open(out_json, 'w'), ensure_ascii=False, indent=1)
print('elegido:', mejor)
for rid, v in js.items(): print(f'  {series[rid][0]:18s}', series[rid][2][2023], '→', v)
