"""Reproduce REC[].v desde las etiquetas de Vogue y la recalcula dividiendo sólo por los looks etiquetados."""
import duckdb, json, itertools, sys
REPO = '/Users/felipe/Documents/Ciclo K576/ciclo/'
con = duckdb.connect()
con.execute("""create table c as select year, tags from 'datos/vogue_tags.parquet'
  where not (coalesce(designer,'') ilike '%bridal%' or coalesce(url,'') ilike '%bridal%')""")
print('looks', con.execute('select count(*) from c').fetchone())
C = {'denim': ['Denim', 'Jeans'], 'buzo': ['Sweatshirt', 'Hoodie', 'Hood'], 'cuero': ['Leather Jacket'], 'lunares': ['Polka Dot'],
     'floral': ['Flower', 'Floral Design', 'Flower Arrangement', 'Flower Bouquet'], 'animal print': ['Zebra', 'Giraffe', 'Cow', 'Animal'],
     'militar': ['Military', 'Military Uniform', 'Camouflage'], 'encaje': ['Lace'], 'kimono': ['Kimono'], 'capa': ['Cape', 'Cloak'],
     'trench': ['Trench Coat']}
Y = list(range(2010, 2024))
tot = dict(con.execute('select year, count(*) from c group by 1').fetchall())
etq = dict(con.execute('select year, count(*) from c where len(tags)>0 group by 1').fetchall())
def cuenta(combo):
    lst = ','.join("'" + t.replace("'", "''") + "'" for t in combo)
    return dict(con.execute(f'select year, count(*) from c where len(list_intersect(tags,[{lst}]))>0 group by 1').fetchall())
d = json.load(open(REPO + 'datasets_procesados/ciclo_series__anual_por_atributo.json'))
out = {}
for r in d['REC']:
    vk = r.get('vk')
    if not vk or vk in out: continue
    v = [r['v'][y - 2004] for y in Y]
    best = None
    for k in range(1, len(C[vk]) + 1):
        for combo in itertools.combinations(C[vk], k):
            n = cuenta(combo)
            sh = [n.get(y, 0) / tot[y] for y in Y]; m = max(sh); x = [100 * s / m for s in sh]
            err = sum(abs(a - b) for a, b in zip(x, v)) / len(Y)
            if best is None or err < best[0]: best = (err, combo, n)
    err, combo, n = best
    sh2 = [n.get(y, 0) / etq[y] for y in Y]; m2 = max(sh2); x2 = [round(100 * s / m2, 1) for s in sh2]
    out[vk] = {'combo': combo, 'err_repo': round(err, 2), 'antes': [round(a) for a in v], 'corregida': x2,
               'pk_antes': Y[v.index(max(v))], 'pk_corr': Y[x2.index(max(x2))], 'n': [n.get(y, 0) for y in Y]}
    print(f"{vk:13s} err {err:5.2f} {'+'.join(combo):30s} antes {out[vk]['antes'][-4:]} → corregida {[round(a) for a in x2[-4:]]}  pico {out[vk]['pk_antes']}→{out[vk]['pk_corr']}")
json.dump({'tot': tot, 'etiquetados': etq, 'series': out}, open('datos/pasarela_corregida.json', 'w'), indent=1)
print({y: round(100 * etq[y] / tot[y], 1) for y in Y})
