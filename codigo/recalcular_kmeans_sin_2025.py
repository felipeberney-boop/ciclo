"""CICLO — recalcula las variables de búsqueda del K-means sin 2025 (salto de medición de Google) y reentrena k=2..6.

Uso: python3 codigo/recalcular_kmeans_sin_2025.py capas_temporales_vogue_trends_reddit.csv km.json
El CSV de capas (35 términos mundiales de Google Trends, promedio anual) no está en el repo: es el de
`datos_limpios/` de la carpeta de Drive del grupo. Lee `const KM=` de app/index.html y escribe rows, sc, cent
y elbow listos para reemplazarlo. Pasarela (pn, pm), validación (amz, shop) y tipo no se tocan.

Antes: nivel = promedio 2024–25 / máximo; momento = promedio 2024–25 / promedio 2021–22 − 1.
Ahora: nivel = promedio 2023–24 / máximo hasta 2024; momento = promedio 2023–24 / promedio 2020–21 − 1.
Cada búsqueda se divide por el promedio de los 35 términos de ese año, como antes. Se saca el calzado."""
import csv, json, re, sys
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

KM = json.loads(re.search(r'const KM=(\{.*?\});\n', open('app/index.html').read()).group(1))
W, R = {}, {}
for r in csv.DictReader(open(sys.argv[1])):
    if r['capa'] == 'busqueda_mundo': W.setdefault(r['termino'], {})[int(r['anio'])] = float(r['valor'])
for r in csv.DictReader(open('datasets_procesados/series_google_trends/trends_mundo__web_anual.csv')):
    R.setdefault(r['atributo_id'], {})[int(r['anio'])] = float(r['indice_0_100'])
Y = list(range(2004, 2026))
ref = np.array([np.mean([W[t][y] for t in W]) for y in Y])  # índice general de moda por año
SRC = {'Jeans baggy': R['jamplio'], 'Jeans rectos': R['jmedio'], 'Jeans skinny': R['jajust'], 'Buzo / hoodie': W['hoodie'],
       'Floral': W['floral dress'], 'Lunares': W['polka dot dress'], 'Cuero': W['leather jacket'], 'Animal print': W['leopard print'],
       'Kimono': W['kimono jacket'], 'Capa': W['cape coat'], 'Trench': W['trench coat'], 'Encaje': W['lace dress'],
       'Cuadros': W['plaid skirt'], 'Piel': W['fur coat'], 'Zapatilla chunky': W['dad sneakers'], 'Cargo': W['cargo pants'],
       'Y2K': W['y2k fashion'], 'Blazer oversize': W['oversized blazer']}

def busqueda(n, antes, ahora, ultimo):
    t = dict(zip(Y, np.array([SRC[n][y] for y in Y]) / ref)); ok = [y for y in Y if y <= ultimo]
    mx = max(t[y] for y in ok); ahora_m = np.mean([t[y] for y in ahora])
    return ahora_m / mx, ahora_m / np.mean([t[y] for y in antes]) - 1, max(ok, key=lambda y: t[y])

def variables(rows):
    F = np.array([[r['pn'], r['pm'], r['bn'], r['bm']] for r in rows])
    F[:, 1] = np.clip(F[:, 1], -1, 1.5); F[:, 3] = np.clip(F[:, 3], -1, 1.5); return F

# control: los atributos que no son jeans tienen que salir igual que hoy en la app (los jeans cambian si se reagruparon)
for r in KM['rows']:
    if r['n'].startswith('Jeans') or r['tipo'] == 'Calzado': continue
    bn, bm, _ = busqueda(r['n'], (2020, 2021), (2023, 2024), 2024)
    assert abs(bn - r['bn']) < 2e-3 and abs(bm - r['bm']) < 2e-3, (r['n'], bn, r['bn'], bm, r['bm'])

rows = []
for r in KM['rows']:
    if r['tipo'] == 'Calzado': continue
    bn, bm, pico = busqueda(r['n'], (2020, 2021), (2023, 2024), 2024)
    rows.append({**r, 'bn': round(float(bn), 3), 'bm': round(float(bm), 3), 'pico_bus': int(pico)})
sc = StandardScaler().fit(variables(rows)); Z = sc.transform(variables(rows))
elbow = {}
for k in range(2, 7):
    km = KMeans(k, n_init=50, random_state=42).fit(Z)
    elbow[str(k)] = dict(sil=round(float(silhouette_score(Z, km.labels_)), 3), inercia=round(float(km.inertia_), 2))
km = KMeans(4, n_init=50, random_state=42).fit(Z)
for r, l in zip(rows, km.labels_): r['cl'] = int(l)
nuevo = dict(rows=rows, sc=dict(m=sc.mean_.tolist(), s=sc.scale_.tolist()), cent=km.cluster_centers_.tolist(), elbow=elbow)
json.dump(nuevo, open(sys.argv[2], 'w'), ensure_ascii=False, separators=(',', ':'))
if '--app' in sys.argv:  # escribe const KM= en app/index.html
    h = open('app/index.html').read(); m = re.search(r'const KM=(\{.*?\});\n', h)
    h = h[:m.start()] + 'const KM=' + json.dumps(nuevo, ensure_ascii=False, separators=(',', ':')) + ';\n' + h[m.end():]
    open('app/index.html', 'w').write(h); print('escrito const KM= en app/index.html')
print(elbow)
