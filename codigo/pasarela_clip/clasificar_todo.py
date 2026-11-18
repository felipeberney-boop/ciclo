"""La pasarela 2010–2025 con CLIP, sobre todos los looks de colección.
1. Entrena, por atributo, una regresión logística sobre el vector CLIP de los looks etiquetados de 2010–2021 (todos los
   positivos y 80.000 negativos al azar, con peso para conservar la proporción real).
2. Estima la proporción de cada año como la probabilidad media de todos los looks de ese año (también los que Vogue no
   etiquetó en 2022–2023).
3. Valida contra la proporción de las etiquetas en 2010–2021 (correlación y error relativo).
4. Aplica el mismo clasificador a una muestra de 1.000 looks por año de 2022–2025 del dataset nuevo (fotos bajadas sólo
   para calcular su vector) y compara 2022–2023 contra la población del dataset original.
Escribe datos/pasarela_clip.json."""
import json, numpy as np, torch, duckdb
torch.manual_seed(0); rng = np.random.default_rng(0)
E = np.load('datos/VogueRunway_image.npy', mmap_mode='r')
print('vectores', E.shape, E.dtype)
con = duckdb.connect()
rows = con.execute("""select i, year, tags, coalesce(len(tags),0)>0 as et from 'datos/vogue_todo.parquet'
  where section='Collection' and year between 2010 and 2023
  and not (coalesce(designer,'') ilike '%bridal%' or coalesce(url,'') ilike '%bridal%')""").fetchall()
I = np.array([r[0] for r in rows]); Y = np.array([r[1] for r in rows]); ET = np.array([bool(r[3]) for r in rows])
TG = [set(r[2] or []) for r in rows]
print('looks de colección 2010–2023', len(I))
def vec(ix):
    X = np.asarray(E[np.sort(ix)], dtype=np.float32); o = np.argsort(np.argsort(ix))
    X = X[o]; return X / np.linalg.norm(X, axis=1, keepdims=True)
Xall = None
COMBO = {k: v['combo'] for k, v in json.load(open('datos/pasarela_corregida.json'))['series'].items()}
COMBO.update({'cuadros': ['Plaid', 'Tartan'], 'piel': ['Fur'], 'blazer': ['Blazer'], 'y2k': ['Miniskirt']})  # las cuatro filas del K-means sin serie en El ciclo
A = list(range(2010, 2024))
import csv, os
U, EN, meta = [], [], {}
for npz, mc in (('datos/emb_2022_2025.npz', 'datos/muestra_2022_2025.csv'), ('datos/emb2.npz', 'datos/muestra2.csv'), ('datos/emb3.npz', 'datos/muestra3.csv')):
    if not os.path.exists(npz): continue
    z = np.load(npz, allow_pickle=True); U += z['u'].tolist(); EN.append(z['e'])
    meta.update({r['u'].strip('"'): int(r['y']) for r in csv.DictReader(open(mc))})
EN = np.concatenate(EN)
YN = np.array([meta.get(u, 0) for u in U])
print('muestra nueva con vector', len(U), {y: int((YN == y).sum()) for y in range(2022, 2026)})
# todos los vectores de colección en memoria (≈1,8 GB en float32 sería mucho: se predice por bloques)
bloques = np.array_split(np.arange(len(I)), 40)
res = {}
for vk, combo in COMBO.items():
    cs = set(combo)
    pos = np.array([bool(t & cs) for t in TG])
    tr = ET & (Y <= 2021)
    ip = np.where(tr & pos)[0]; ineg = np.where(tr & ~pos)[0]
    nn = min(80000, len(ineg)); sn = rng.choice(ineg, nn, replace=False); wneg = len(ineg) / nn
    idx = np.concatenate([ip, sn]); t = np.concatenate([np.ones(len(ip)), np.zeros(nn)]).astype(np.float32)
    wt = np.concatenate([np.ones(len(ip)), np.full(nn, wneg)]).astype(np.float32)
    X = torch.tensor(vec(I[idx])); T = torch.tensor(t); Wt = torch.tensor(wt / wt.mean())
    w = torch.zeros(512, requires_grad=True); b = torch.zeros(1, requires_grad=True)
    opt = torch.optim.LBFGS([w, b], max_iter=400, line_search_fn='strong_wolfe')
    def f():
        opt.zero_grad(); zz = X @ w * 30 + b
        l = (torch.nn.functional.binary_cross_entropy_with_logits(zz, T, reduction='none') * Wt).mean() + 1e-4 * (w ** 2).sum()
        l.backward(); return l
    opt.step(f)
    w_, b_ = w.detach(), b.detach()
    P = np.zeros(len(I), np.float32)
    with torch.no_grad():
        for bl in bloques: P[bl] = torch.sigmoid(torch.tensor(vec(I[bl])) @ w_ * 30 + b_).numpy()
        PN = torch.sigmoid(torch.tensor(EN) @ w_ * 30 + b_).numpy()
    clip = {a: float(P[Y == a].mean()) for a in A}
    tag = {a: float(pos[(Y == a) & ET].mean()) for a in A}
    nueva = {a: float(PN[YN == a].mean()) for a in range(2022, 2026)}
    bs = {}
    for a in range(2022, 2026):
        pa = PN[YN == a]; m = [float(pa[rng.integers(0, len(pa), len(pa))].mean()) for _ in range(400)]
        bs[a] = (float(np.percentile(m, 5)), float(np.percentile(m, 95)))
    V = [a for a in A if a <= 2021]
    r = float(np.corrcoef([clip[a] for a in V], [tag[a] for a in V])[0, 1])
    k = sum(tag[a] for a in V if a >= 2016) / sum(clip[a] for a in V if a >= 2016)
    res[vk] = {'w': w_.numpy().tolist(), 'b': float(b_), 'n_nueva': {a: int((YN == a).sum()) for a in range(2022, 2026)}, 'combo': combo, 'positivos': int(len(ip)), 'r_2010_2021': round(r, 3), 'k': k, 'clip': clip, 'tag': tag, 'nueva': nueva, 'nueva_ic90': bs}
    print(f"{vk:13s} pos {len(ip):6d} r {r:+.3f} k {k:.2f} | tag 21–23 {[round(1000*tag[a],1) for a in (2021,2022,2023)]} clip·k {[round(1000*k*clip[a],1) for a in (2021,2022,2023)]} nueva·k {[round(1000*k*nueva[a],1) for a in range(2022,2026)]}", flush=True)
json.dump(res, open('datos/pasarela_clip_grande.json', 'w'), indent=1)
