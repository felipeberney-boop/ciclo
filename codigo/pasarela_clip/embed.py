"""Calcula el vector CLIP ViT-B/32 (pesos openai) de una lista de fotos de Vogue (url por línea).
Uso: embed.py lista.txt salida.npz [ancho]  · reanudable: guarda cada 200."""
import sys, os, io, numpy as np, requests, torch, open_clip
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
lista, out = sys.argv[1], sys.argv[2]; W = int(sys.argv[3]) if len(sys.argv) > 3 else 400
urls = [l.strip() for l in open(lista) if l.strip()]
model, _, prep = open_clip.create_model_and_transforms('ViT-B-32-quickgelu', pretrained='openai'); model.eval()
hechos = {}
if os.path.exists(out):
    z = np.load(out, allow_pickle=True); hechos = dict(zip(z['u'].tolist(), z['e']))
def ajustar(u):  # misma foto, más chica
    import re
    return re.sub(r'/master/w_\d+,[^/]*/', f'/master/w_{W},c_limit/', u)
def bajar(u):
    for _ in range(3):
        try:
            r = requests.get(ajustar(u), timeout=30, headers={'User-Agent': 'ciclo-investigacion/1.0'})
            if r.ok: return u, Image.open(io.BytesIO(r.content)).convert('RGB')
        except Exception: pass
    return u, None
pend = [u for u in urls if u not in hechos]
print('pendientes', len(pend), 'hechos', len(hechos), flush=True)
def guardar():
    np.savez(out, u=np.array(list(hechos.keys()), dtype=object), e=np.array(list(hechos.values()), dtype=np.float32))
with ThreadPoolExecutor(32) as ex:
    for i in range(0, len(pend), 200):
        lote = [x for x in ex.map(bajar, pend[i:i + 200]) if x[1] is not None]
        if lote:
            with torch.no_grad():
                X = torch.stack([prep(im) for _, im in lote])
                E = model.encode_image(X).float(); E = E / E.norm(dim=-1, keepdim=True)
            for (u, _), e in zip(lote, E.numpy()): hechos[u] = e
        guardar(); print(i + len(lote), '/', len(pend), flush=True)
guardar(); print('fin', len(hechos))
