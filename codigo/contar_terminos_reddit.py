"""Cuenta, por año, los posts de r/femalefashionadvice cuyo título nombra cada término (sin distinguir
mayúsculas), y el total de posts del año. Lee uno o más JSONL de reddit_fetch.py."""
import json, sys, datetime as dt, collections, csv

repo, out_csv, *fuentes = sys.argv[1:]
d = json.load(open(repo + '/datasets_procesados/ciclo_series__anual_por_atributo.json'))
terminos = set(d['RDS'])
for r in d['REC']:
    if r.get('rk'): terminos.update(t.strip() for t in r['rk'].split('+'))
terminos = sorted(terminos)

posts = {}
for fpath in fuentes:
    for l in open(fpath):
        p = json.loads(l)
        if 'id' in p: posts[p['id']] = p
tot = collections.Counter(); cnt = collections.Counter(); meses = collections.defaultdict(set)
for p in posts.values():
    f = dt.datetime.fromtimestamp(p['created_utc'], dt.timezone.utc)
    y = f.year; tot[y] += 1; meses[y].add(f.month)
    t = (p.get('title') or '').lower()
    for term in terminos:
        if term in t: cnt[(term, y)] += 1
with open(out_csv, 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['termino', 'anio', 'posts', 'posts_totales_anio', 'indice_por_mil', 'meses_cubiertos'])
    for term in terminos:
        for y in sorted(tot):
            w.writerow([term, y, cnt[(term, y)], tot[y], round(1000 * cnt[(term, y)] / tot[y], 3), len(meses[y])])
print({y: tot[y] for y in sorted(tot)}, len(terminos), 'términos')
