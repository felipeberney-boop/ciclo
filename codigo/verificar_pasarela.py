"""Recalcula la curva de pasarela de cada atributo desde el VogueRunway.parquet original y la compara con
REC[].v del repositorio. Prueba las combinaciones de etiquetas candidatas y se queda con la de menor error.

Uso (desde la raíz del repo; necesita pandas y pyarrow):
    python3 codigo/verificar_pasarela.py ruta/a/VogueRunway.parquet
El parquet se baja de https://huggingface.co/datasets/traopia/vogue-runway y no se sube al repo."""
import sys, json, itertools, pandas as pd, numpy as np

df = pd.read_parquet(sys.argv[1], columns=['designer', 'year', 'section', 'tags', 'url'])
c = df[(df.section == 'Collection') & df.year.between(2000, 2023)]
c = c[~(c.designer.str.contains('Bridal', case=False, na=False) | c.url.str.contains('bridal', case=False, na=False))]
print('looks después del filtro:', len(c))
d = json.load(open('datasets_procesados/ciclo_series__anual_por_atributo.json'))
C = {'denim': ['Denim', 'Jeans'], 'buzo': ['Sweatshirt', 'Hoodie', 'Hood'], 'cuero': ['Leather Jacket'], 'lunares': ['Polka Dot'],
     'floral': ['Flower', 'Floral Design', 'Flower Arrangement', 'Flower Bouquet'], 'animal print': ['Zebra', 'Giraffe', 'Cow', 'Animal'],
     'militar': ['Military', 'Military Uniform', 'Camouflage'], 'encaje': ['Lace'], 'kimono': ['Kimono'], 'capa': ['Cape', 'Cloak'],
     'trench': ['Trench Coat']}
tagsets = c.tags.apply(lambda t: set(t) if t is not None else set())
den = c.groupby('year').size()
yrs = list(range(2010, 2024))
vistos = set()
for r in d['REC']:
    vk = r.get('vk')
    if not vk or vk in vistos: continue
    vistos.add(vk)
    v = np.array([r['v'][y - 2004] for y in yrs], float)
    best = None
    for k in range(1, len(C[vk]) + 1):
        for combo in itertools.combinations(C[vk], k):
            num = c[tagsets.apply(lambda s: bool(s & set(combo)))].groupby('year').size().reindex(range(2000, 2024), fill_value=0)
            sh = (num / den).fillna(0)
            x = np.array([sh[y] for y in yrs]) / max(sh[y] for y in yrs) * 100
            err = np.abs(x - v)
            cand = (err.mean(), combo, err.max(), np.corrcoef(x, v)[0, 1], yrs[int(np.argmax(x))])
            if best is None or cand[0] < best[0]: best = cand
    print(f"{vk:13s} error medio {best[0]:5.2f} · máx {best[2]:5.1f} · r={best[3]:.3f} · pico {best[4]} (repo {r['pv']}) · {'+'.join(best[1])}")
