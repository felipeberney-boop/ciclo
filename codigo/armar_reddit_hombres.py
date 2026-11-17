"""La serie de Reddit de hombres (r/malefashionadvice), con la misma regla que la de mujeres (RDS), para la app.
17/11/2026. Entrada: datasets_procesados/reddit_hombres_conteos.csv (sale de bajar_titulos_reddit.py con el subreddit
malefashionadvice y de contar_terminos_reddit.py). Salida: una línea `const RDH={...};` para app/index.html y
datasets_procesados/reddit_hombres.json.

Regla (la misma de RDS, verificada en datasets/completado_2026/readme.md): proporción de posts del año cuyo título
nombra el término, media móvil centrada de 3 años (en las puntas, ese año y el vecino), 2012–2025, llevada a 100 en su
máximo. Un término «a + b» suma los dos. Entran sólo los términos con 100 posts o más en 2012–2025.
«lace» queda afuera: en r/malefashionadvice nombra los cordones («laces», «shoelaces»), no el encaje."""
import csv, json, collections
n = collections.defaultdict(int); tot = {}
for r in csv.DictReader(open('datasets_procesados/reddit_hombres_conteos.csv')):
    n[(r['termino'], int(r['anio']))] = int(r['posts']); tot[int(r['anio'])] = int(r['posts_totales_anio'])
d = json.load(open('datasets_procesados/ciclo_series__anual_por_atributo.json'))
terminos = set(d['RDS']) | {r['rk'] for r in d['REC'] if r.get('rk')}
A = list(range(2012, 2026))
P = lambda t, y: sum(n[(x.strip(), y)] for x in t.split('+'))
out, fuera = {}, []
for t in sorted(terminos):
    total = sum(P(t, y) for y in A)
    if t.strip() == 'lace' or total < 100:
        fuera.append((t, total)); continue
    R = {y: P(t, y) / tot[y] for y in A}
    m = {y: sum(R[z] for z in (y - 1, y, y + 1) if z in R) / len([z for z in (y - 1, y, y + 1) if z in R]) for y in A}
    mx = max(m.values())
    i = [None] * (2012 - 2004) + [round(100 * m[y] / mx, 1) for y in A]
    out[t] = {'i': i, 'pk': max(A, key=lambda y: m[y]), 'n': total}
json.dump({'fuente': 'r/malefashionadvice vía Arctic Shift', 'posts_totales_2012_2025': sum(tot[y] for y in A),
           'regla': 'posts que nombran el término / posts del año, media centrada de 3 años, 100 = su máximo 2012–2025',
           'series': out, 'fuera': dict(fuera)}, open('datasets_procesados/reddit_hombres.json', 'w'), ensure_ascii=False, indent=1)
print('const RDH=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';')
print('fuera:', fuera)
