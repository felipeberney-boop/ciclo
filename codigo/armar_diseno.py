"""Arma los datos del recorrido «Diseñar»: fotos de referencia y colores que ganan presencia en la pasarela.

Para cada corte, prenda y estampa del catálogo (codigo/diseno_catalogo.json):
- Referencias: los looks de Vogue 2018–2023 que CLIP encuentra más parecidos al texto del ítem (en los cortes
  de jean, más parecidos a ese corte que a los otros, porque Vogue sólo etiqueta «denim»), separados en
  mujer y hombre con CLIP, sin repetir desfile. Si Vogue tiene etiqueta para el ítem, se busca sólo entre los
  looks con esa etiqueta.
- Colores: para cada look de la prenda, CLIP elige el color más parecido de una lista fija. Se compara qué
  parte de los looks tenía cada color en 2018–2019 y en 2022–2023. Es una lectura de un modelo sobre la
  pasarela, no un dato de venta, y termina en 2023 como la pasarela.

Uso (desde la raíz del repo; numpy, pandas y pyarrow):
    python3 codigo/armar_diseno.py VogueRunway.parquet VogueRunway_image.npy textos_diseno.json
textos_diseno.json sale de codigo/calcular_textos_diseno.mjs. Escribe app/diseno/diseno.json."""
import sys, json, os, collections, numpy as np, pandas as pd

parquet, npy, textos = sys.argv[1:4]
C = json.load(open('codigo/diseno_catalogo.json'))
T = json.load(open(textos))
df = pd.read_parquet(parquet, columns=['designer', 'season', 'year', 'section', 'tags', 'url'])
c = df[(df.section == 'Collection') & df.year.between(2010, 2023) & df.url.str.startswith('https://assets.vogue.com/photos/', na=False)]
c = c[~(c.designer.str.contains('Bridal', case=False, na=False) | c.url.str.contains('bridal', case=False, na=False))]
idx = c.index.values
E = np.load(npy, mmap_mode='r')
claves = list(T); M = np.array([T[k] for k in claves], dtype=np.float32).T  # 512 × K
S = np.empty((len(idx), len(claves)), dtype=np.float16)
for a in range(0, len(idx), 50000):
    X = np.asarray(E[idx[a:a + 50000]], dtype=np.float32); X /= np.linalg.norm(X, axis=1, keepdims=True)
    S[a:a + 50000] = X @ M
col = {k: i for i, k in enumerate(claves)}
sim = lambda k: S[:, col[k]].astype(np.float32)
anio = c.year.values
tags = c.tags.apply(lambda t: set(t) if t is not None else set()).values
mujer = sim('publico:mujer') - sim('publico:hombre') > 0
foto = c.url.str.replace('https://assets.vogue.com/photos/', '', regex=False).values
dis = c.designer.values; temp = c.season.map({'Spring': 'S', 'Fall': 'F', 'Resort': 'R', 'Pre-Fall': 'P'}).fillna('?').values
print(len(idx), 'looks · mujer', int(mujer.sum()), '· hombre', int((~mujer).sum()))

def con_etiqueta(et):
    if not et: return np.ones(len(idx), bool)
    et = set(et); return np.array([bool(t & et) for t in tags])

def referencias(score, pool, n=6):
    out = {}
    for g, mask in (('mujer', mujer), ('hombre', ~mujer)):
        m = pool & mask & (anio >= 2018)
        orden = np.argsort(-np.where(m, score, -9))[:400]
        vistos, sel = set(), []
        for i in orden:
            if not m[i]: break
            k = (dis[i], temp[i], anio[i])
            if k in vistos: continue
            vistos.add(k); sel.append({'f': foto[i], 'd': dis[i], 's': temp[i], 'y': int(anio[i]), 'v': round(float(score[i]), 3)})
            if len(sel) == n: break
        out[g] = sel
    return out

def colores(prefijo, lista, pool, score, top=None):
    """Reparto de colores en la pasarela, 2018–19 contra 2022–23."""
    ks = [f'{prefijo}:{x["id"]}' for x in lista]
    Z = np.stack([sim(k) for k in ks], 1)
    elegido = Z.argmax(1)
    res, n = {}, {}
    for per, (a0, a1) in (('antes', (2018, 2019)), ('ahora', (2022, 2023))):
        m = pool & (anio >= a0) & (anio <= a1)
        if top:  # sin etiqueta de Vogue: los `top` looks más parecidos por año
            m2 = np.zeros(len(idx), bool)
            for y in range(a0, a1 + 1):
                cand = np.where(m & (anio == y))[0]
                m2[cand[np.argsort(-score[cand])[:top]]] = True
            m = m2
        cnt = collections.Counter(elegido[m]); tot = int(m.sum()); n[per] = tot
        res[per] = {lista[j]['id']: cnt.get(j, 0) / tot for j in range(len(lista))}
    filas = [{'id': x['id'], 'n': x['n'], 'hex': x['hex'], 'ahora': round(100 * res['ahora'][x['id']], 1),
              'cambio': round(100 * (res['ahora'][x['id']] - res['antes'][x['id']]), 1)} for x in lista]
    return {'n': n, 'colores': sorted(filas, key=lambda r: -r['ahora'])}

def reparto(claves, pool, score, top):
    """Qué parte de los looks de una prenda eligió CLIP para cada opción (fit o cuello), 2018–19 contra 2022–23."""
    Z = np.stack([sim(k) for k in claves], 1); elegido = Z.argmax(1); res, n = {}, {}
    for per, (a0, a1) in (('antes', (2018, 2019)), ('ahora', (2022, 2023))):
        m = pool & (anio >= a0) & (anio <= a1)
        if top:
            m2 = np.zeros(len(idx), bool)
            for y in range(a0, a1 + 1):
                cand = np.where(m & (anio == y))[0]; m2[cand[np.argsort(-score[cand])[:top]]] = True
            m = m2
        cnt = collections.Counter(elegido[m]); n[per] = int(m.sum()); res[per] = [cnt.get(j, 0) / n[per] for j in range(len(claves))]
    return n, [(round(100 * a, 1), round(100 * (a - b), 1)) for a, b in zip(res['ahora'], res['antes'])]

salida = {'nota': 'Referencias y colores leídos por CLIP en la pasarela de Vogue, 2018–2023. Es interpretación de un modelo, no venta.',
          'prendas': [], 'estampas': []}
for pr in C['prendas']:
    P = {'id': pr['id'], 'n': pr['n'], 'cortes': []}
    for co in pr['cortes']:
        pool = con_etiqueta(co.get('vogue') or pr.get('vogue'))
        score = sim(f'corte:{pr["id"]}:{co["id"]}')
        if pr.get('vogue'):  # cortes de una misma prenda (jeans): lo que se parece a ESTE corte más que a los otros
            otros = [sim(f'corte:{pr["id"]}:{x["id"]}') for x in pr['cortes'] if x['id'] != co['id']]
            score = score - np.mean(otros, axis=0)
        tieneEt = bool(co.get('vogue') or pr.get('vogue'))
        lista = pr.get('colores') or C['colores_generales']
        item = {k: co[k] for k in co if k not in ('en', 'vogue')}
        item['refs'] = referencias(score, pool)
        item['color'] = colores(f'color:{pr["id"]}:{co["id"]}', lista, pool, score, top=None if tieneEt else 150)
        item['fuente_refs'] = 'etiqueta de Vogue + CLIP' if tieneEt else 'CLIP'
        P['cortes'].append(item)
        print(f'{pr["n"]:10s} {co["n"]:16s} refs {len(item["refs"]["mujer"])}/{len(item["refs"]["hombre"])} · colores ahora:',
              ', '.join(f'{x["n"]} {x["ahora"]}% ({x["cambio"]:+.1f})' for x in item['color']['colores'][:3]), '· n', item['color']['n'])
        if pr.get('cuellos'): item['color'] = None  # el color de remeras y buzos se calcula una vez para la prenda, abajo
    P.update({k: pr[k] for k in ('sil', 'rec', 'grupo', 'nota_cortes') if k in pr})
    if pr.get('cuellos'):  # remeras y buzos: fit y cuello leídos por CLIP en la pasarela de la prenda
        pool = con_etiqueta(pr.get('vogue')); score = sim(f'prenda:{pr["id"]}'); top = None if pr.get('vogue') else 300
        n, r = reparto([f'corte:{pr["id"]}:{x["id"]}' for x in pr['cortes']], pool, score, top)
        for item, (a, d) in zip(P['cortes'], r): item['ahora'], item['cambio'] = a, d
        P['n_fit'] = n
        n, r = reparto([f'cuello:{pr["id"]}:{x["id"]}' for x in pr['cuellos']], pool, score, top)
        P['cuellos'] = [dict({k: x[k] for k in ('id', 'n', 'sil', 'solo') if k in x}, ahora=a, cambio=d) for x, (a, d) in zip(pr['cuellos'], r)]
        P['n_cuello'] = n
        n, r = reparto([f'manga:{pr["id"]}:{x["id"]}' for x in pr['mangas']], pool, score, top)
        P['mangas'] = [dict({k: x[k] for k in ('id', 'n', 'sil', 'solo') if k in x}, ahora=a, cambio=d) for x, (a, d) in zip(pr['mangas'], r)]
        P['n_manga'] = n
        print('   manga', [(x['n'], x['ahora'], x['cambio']) for x in P['mangas']])
        P['color'] = colores(f'color:{pr["id"]}:{pr["cortes"][1]["id"]}', pr.get('colores') or C['colores_generales'], pool, score, top=top)
        print(pr['n'], 'fit', [(x['n'], x['ahora'], x['cambio']) for x in P['cortes']], '\n   cuello', [(x['n'], x['ahora'], x['cambio']) for x in P['cuellos']], n)
    salida['prendas'].append(P)
for e in C['estampas']:
    pool = con_etiqueta(e.get('vogue'))
    item = {k: e[k] for k in e if k not in ('en', 'vogue')}
    item['refs'] = referencias(sim(f'estampa:{e["id"]}'), pool)
    item['fuente_refs'] = 'etiqueta de Vogue + CLIP' if e.get('vogue') else 'CLIP'
    salida['estampas'].append(item)
# las ilustraciones van adentro de los datos: la app las dibuja sin bajar archivos aparte
import re
usadas = {pr['sil'] for pr in salida['prendas'] if pr.get('sil')} | {x['sil'] for pr in salida['prendas'] for k in ('cortes', 'cuellos', 'mangas') for x in pr.get(k, []) if x.get('sil')} \
         | {e['sil'] for e in salida['estampas'] if e.get('sil')}
salida['svg'] = {u: re.sub(r'\s+', ' ', re.sub(r'<svg([^>]*?) width="\d+" height="\d+"', r'<svg\1', open(f'app/siluetas/{u}.svg').read())).strip() for u in sorted(usadas)}
os.makedirs('app/diseno', exist_ok=True)
json.dump(salida, open('app/diseno/diseno.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('escrito app/diseno/diseno.json ·', round(os.path.getsize('app/diseno/diseno.json') / 1e3), 'KB')
