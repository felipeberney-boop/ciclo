"""CICLO — ¿la pasarela adelanta a la búsqueda a escala de temporada? Según datasets/pruebas/prueba_temporada_preregistro.md.

Uso (desde la raíz del repo; necesita pandas y pyarrow):
    python3 codigo/prueba_temporada.py ruta/a/VogueRunway.parquet
El parquet se baja de https://huggingface.co/datasets/traopia/vogue-runway y no se sube al repo. La búsqueda mensual sale
de los lotes de Google Trends de datasets/trends_lotes/. Escribe el resultado en datasets/pruebas/prueba_temporada_resultado.json."""
import csv, json, sys
import numpy as np, pandas as pd

# atributo: (etiquetas de Vogue, término de búsqueda, lote)  — la tabla del preregistro, con la enmienda 1
ATR = {
    'Trench': (['Trench Coat'], 'trench coat', 'plan4/lote23.csv'),
    'Cuero': (['Leather Jacket'], 'leather jacket', 'plan4/lote23.csv'),
    'Encaje': (['Lace'], 'lace dress', 'plan4/lote23.csv'),
    'Lunares': (['Polka Dot'], 'polka dot dress', 'plan4/lote23.csv'),
    'Cuadros': (['Plaid', 'Tartan'], 'plaid skirt', 'plan4/lote24.csv'),
    'Kimono': (['Kimono'], 'kimono jacket', 'plan4/lote24.csv'),
    'Capa': (['Cape', 'Cloak'], 'cape coat', 'plan4/lote24.csv'),
    'Animal print': (['Zebra', 'Giraffe', 'Cow', 'Animal'], 'leopard', 'plan4/lote24.csv'),
    'Buzo': (['Sweatshirt', 'Hoodie'], 'hoodie', 'plan4/lote25.csv'),
    'Piel': (['Fur'], 'fur coat', 'plan4/lote25.csv'),
    'Denim': (['Denim', 'Jeans'], 'jeans', 'plan4/lote25.csv'),
    'Cardigan': (['Cardigan'], 'cardigan', 'multiTimeline-7.csv'),
    'Blusa': (['Blouse'], 'blouse', 'multiTimeline-9.csv'),
    'Lino': (['Linen'], 'linen', 'multiTimeline-5.csv'),
    'Minifalda': (['Miniskirt'], 'mini skirt', 'multiTimeline-8.csv'),
}
# cada temporada, en el mes de su desfile: (desplazamiento de año, mes)
MES = {'Fall': (0, 3), 'Spring': (-1, 9), 'Resort': (-1, 6), 'Pre-Fall': (-1, 12)}
REZAGOS = [0, 3, 6, 9, 12, 15, 18]
PERMUTACIONES, SEMILLA, ALFA = 10_000, 2026, 0.05 / 7
FIN = (2024, 12)  # la búsqueda corta en 2024

# ---------- pasarela: proporción de looks con la etiqueta, por temporada ----------
df = pd.read_parquet(sys.argv[1], columns=['designer', 'season', 'year', 'section', 'tags', 'url'])
df['year'] = pd.to_numeric(df.year, errors='coerce')
c = df[(df.section == 'Collection') & df.year.between(2003, 2023) & df.season.isin(list(MES))]
c = c[~(c.designer.str.contains('Bridal', case=False, na=False) | c.url.str.contains('bridal', case=False, na=False))]
tags = c.tags.apply(lambda t: set(t) if t is not None else set())
total = c.groupby(['season', 'year']).size()

# ---------- búsqueda: mensual, cambio contra el mismo mes del año anterior ----------
def serie(lote, termino):
    filas = list(csv.reader(open('datasets/trends_lotes/' + lote, encoding='utf8')))
    h = next(i for i, r in enumerate(filas) if r and r[0] == 'Mes')
    col = next(j for j, x in enumerate(filas[h]) if x.split(':')[0].strip() == termino)
    v = {}
    for r in filas[h + 1:]:
        if not r: continue
        y, m = map(int, r[0].split('-')); x = r[col].strip()
        v[(y, m)] = 0.5 if x == '<1' else float(x)
    return v

def mas(ym, k):
    y, m = ym; n = y * 12 + (m - 1) + k
    return (n // 12, n % 12 + 1)

def dbus(v, ym):
    a, b = v.get(ym), v.get(mas(ym, -12))
    if a is None or b is None or ym > FIN: return None
    return np.log(a + 1) - np.log(b + 1)

def ranks(x):
    return pd.Series(x).rank().to_numpy()

res, incluidos, datos = {}, [], {}
for nom, (et, termino, lote) in ATR.items():
    con = c[tags.apply(lambda s: bool(s & set(et)))].groupby(['season', 'year']).size()
    sh = (con.reindex(total.index, fill_value=0) / total)
    principales = con.reindex(total.index, fill_value=0).loc[['Fall', 'Spring']]
    principales = principales[principales.index.get_level_values('year') >= 2004]
    medio = float(principales.mean())
    if medio < 20:
        res[nom] = {'entra': False, 'looks_por_temporada': round(medio, 1)}; continue
    v = serie(lote, termino)
    obs = []  # (cambio de pasarela, mes del desfile)
    for (s, y), x in sh.items():
        if y < 2004 or (s, y - 1) not in sh.index: continue
        dy, m = MES[s]
        obs.append((x - sh[(s, y - 1)], (y + dy, m)))
    datos[nom] = {L: [(dr, b) for dr, t in obs if (b := dbus(v, mas(t, L))) is not None] for L in REZAGOS}
    incluidos.append(nom); res[nom] = {'entra': True, 'looks_por_temporada': round(medio, 1), 'pares': {L: len(datos[nom][L]) for L in REZAGOS}}

def mediana_rho(perm=None):
    out = {}
    for L in REZAGOS:
        rs = []
        for nom in incluidos:
            p = datos[nom][L]
            if len(p) < 10: continue
            a, b = ranks([x for x, _ in p]), ranks([y for _, y in p])
            if perm is not None: a = perm.permutation(a)
            rs.append(np.corrcoef(a, b)[0, 1])
        out[L] = float(np.median(rs)) if rs else None
    return out

obs = mediana_rho()
rnd = np.random.default_rng(SEMILLA)
mayores = {L: 0 for L in REZAGOS}
for _ in range(PERMUTACIONES):
    m = mediana_rho(rnd)
    for L in REZAGOS:
        if obs[L] is not None and m[L] is not None and m[L] >= obs[L] - 1e-12: mayores[L] += 1
p = {L: (mayores[L] + 1) / (PERMUTACIONES + 1) for L in REZAGOS}
for nom in incluidos:
    res[nom]['rho'] = {}
    for L in REZAGOS:
        q = datos[nom][L]
        res[nom]['rho'][L] = round(float(np.corrcoef(ranks([x for x, _ in q]), ranks([y for _, y in q]))[0, 1]), 3) if len(q) >= 10 else None

print('Atributos que entran:', len(incluidos), '·', ', '.join(incluidos))
print('Quedan afuera (menos de 20 looks por temporada):', ', '.join(f"{n} ({r['looks_por_temporada']})" for n, r in res.items() if not r['entra']) or 'ninguno')
print('\nRezago   mediana de rho   p (10.000 barajadas)')
for L in REZAGOS: print(f'{L:4d} m   {obs[L]:+.3f}          {p[L]:.4f}{"  *" if p[L] < ALFA else ""}')
pasa = [L for L in REZAGOS if L >= 3 and obs[L] is not None and obs[L] > 0 and p[L] < ALFA and obs[L] > (obs[0] or 0)]
if len(incluidos) < 6: veredicto = 'NO CONCLUYE: quedan menos de 6 atributos con datos suficientes.'
elif pasa: veredicto = f'H SE SOSTIENE: la pasarela adelanta a la búsqueda {", ".join(f"{L} meses" for L in pasa)} (p < {ALFA:.3f}, por encima del rezago 0).'
else: veredicto = 'H SE RECHAZA: ningún rezago de 3 a 18 meses pasa el criterio.'
print('\nVeredicto según el preregistro:', veredicto)
json.dump({'rezagos': REZAGOS, 'mediana_rho': obs, 'p': p, 'alfa': ALFA, 'veredicto': veredicto, 'atributos': res},
          open('datasets/pruebas/prueba_temporada_resultado.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
