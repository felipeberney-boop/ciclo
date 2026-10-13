"""Arma el índice de looks de pasarela que usa la Consulta por imagen (IA-6).

Toma 1.000 looks por año de Vogue Runway (sección Collection, sin Bridal, 2010–2023, muestra fija con
semilla 42) con su embedding CLIP ViT-B/32 tal como viene en el dataset, comprimido a 8 bits.
Escribe en app/clip/:
  looks.bin   N × 512 int8 (el vector real es valor / escala; la escala está en looks.json)
  looks.json  metadatos: diseñador, temporada, año, foto y qué atributos etiquetó Vogue en ese look

Uso (desde la raíz del repo; necesita numpy, pandas y pyarrow):
    python3 codigo/armar_indice_clip.py VogueRunway.parquet VogueRunway_image.npy
Los dos archivos se bajan de https://huggingface.co/datasets/traopia/vogue-runway y no se suben."""
import sys, json, os, numpy as np, pandas as pd

parquet, npy = sys.argv[1:3]
POR_ANIO, SEMILLA, ANIOS = 1000, 42, range(2010, 2024)
# etiquetas de Vogue verificadas contra REC[].v (ver datasets/verificacion.md); cargo queda afuera
ETIQ = {'denim': ['Denim', 'Jeans'], 'buzo': ['Sweatshirt'], 'cuero': ['Leather Jacket'], 'lunares': ['Polka Dot'],
        'floral': ['Flower', 'Floral Design'], 'animal': ['Zebra'], 'encaje': ['Lace'], 'kimono': ['Kimono'],
        'capa': ['Cape', 'Cloak'], 'trench': ['Trench Coat']}

df = pd.read_parquet(parquet, columns=['designer', 'season', 'year', 'category', 'section', 'tags', 'url'])
c = df[(df.section == 'Collection') & df.year.isin(ANIOS) & df.url.str.startswith('https://assets.vogue.com/photos/', na=False)]
c = c[~(c.designer.str.contains('Bridal', case=False, na=False) | c.url.str.contains('bridal', case=False, na=False))]
sel = c.groupby('year', group_keys=False).apply(lambda g: g.sample(min(POR_ANIO, len(g)), random_state=SEMILLA)).sort_index()

E = np.load(npy, mmap_mode='r')
X = np.asarray(E[sel.index.values], dtype=np.float32)
X /= np.linalg.norm(X, axis=1, keepdims=True)
escala = 127 / np.abs(X).max()
Q = np.clip(np.round(X * escala), -127, 127).astype(np.int8)

attrs = list(ETIQ)
def mascara(tags):
    s = set(tags) if tags is not None else set()
    return sum(1 << i for i, a in enumerate(attrs) if s & set(ETIQ[a]))
dis = sorted(sel.designer.unique())
dix = {d: i for i, d in enumerate(dis)}
# https://assets.vogue.com/photos/<id>/<archivo> → se guarda "<id>/<archivo>"; la miniatura es photos/<id>/master/w_320,c_limit/<archivo>
foto = sel.url.str.replace('https://assets.vogue.com/photos/', '', regex=False)
meta = {'fuente': 'Vogue Runway (traopia/vogue-runway, HuggingFace) · embeddings CLIP ViT-B/32 del dataset',
        'n': int(len(sel)), 'dim': 512, 'escala': float(escala), 'anios': [ANIOS.start, ANIOS.stop - 1], 'por_anio': POR_ANIO,
        'atributos': attrs, 'etiquetas': ETIQ, 'disenadores': dis,
        'd': [dix[x] for x in sel.designer], 'y': sel.year.astype(int).tolist(),
        's': [{'Spring': 'S', 'Fall': 'F', 'Resort': 'R', 'Pre-Fall': 'P'}.get(x, '?') for x in sel.season],
        'f': foto.tolist(), 'm': [mascara(t) for t in sel.tags]}
os.makedirs('app/clip', exist_ok=True)
Q.tofile('app/clip/looks.bin')
json.dump(meta, open('app/clip/looks.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(sel), 'looks ·', round(os.path.getsize('app/clip/looks.bin') / 1e6, 1), 'MB +', round(os.path.getsize('app/clip/looks.json') / 1e6, 1), 'MB')
print('looks con cada atributo:', {a: int(sum((m >> i) & 1 for m in meta['m'])) for i, a in enumerate(attrs)})
