"""Arma REC[].v 2010–2025: etiquetas hasta 2021, CLIP desde 2022 (ver clasificar_todo.py). Escribe datos/pasarela_2025.json
y calcula cómo cambiarían pn/pm del K-means."""
import json, numpy as np
REPO = '/Users/felipe/Documents/Ciclo K576/ciclo/'
C = json.load(open('datos/pasarela_clip.json'))
d = json.load(open(REPO + 'datasets_procesados/ciclo_series__anual_por_atributo.json'))
out = {}
filas = [(r.get('vk'), {2004 + i: x for i, x in enumerate(r['v']) if x is not None}) for r in d['REC'] if r.get('vk')]
for vk in ('cuadros', 'piel', 'blazer', 'y2k'):  # sin serie en El ciclo: la de etiquetas, sobre su máximo de 2010–2021
    t = {int(a): x for a, x in C[vk]['tag'].items()}; mx = max(t[a] for a in range(2010, 2022))
    filas.append((vk, {a: 100 * t[a] / mx for a in range(2010, 2024)}))
for vk, R in filas:
    if not vk or vk in out: continue
    c = C[vk]
    clip = {int(a): v for a, v in c['clip'].items()}; nue = {int(a): v for a, v in c['nueva'].items()}
    A = range(2016, 2022)
    f = sum(R[a] * clip[a] for a in A) / sum(clip[a] ** 2 for a in A)   # R ≈ f·clip en 2016–2021
    puente = (clip[2022] + clip[2023]) / (nue[2022] + nue[2023])       # dataset nuevo → original
    S = {a: R[a] for a in range(2010, 2022)}
    S.update({a: f * clip[a] for a in (2022, 2023)})
    ic = {int(a): v for a, v in c.get('nueva_ic90', {}).items()}
    # ancho del intervalo de 90 %, en puntos del índice (antes de renormalizar), sobre el valor medido de su pico
    ancho = {a: f * puente * (ic[a][1] - ic[a][0]) / max(R.values()) * 100 for a in (2024, 2025)} if ic else {2024: 0, 2025: 0}
    extiende = False  # 2024–2025 esperan la muestra grande (ver decisiones.md)
    if extiende: S.update({a: f * puente * nue[a] for a in (2024, 2025)})
    mx = max(S.values()); S = {a: round(100 * v / mx, 1) for a, v in S.items()}
    ajuste = float(np.mean([abs(R[a] - f * clip[a]) for a in A]))
    out[vk] = {'v': S, 'f': f, 'puente': puente, 'err_2016_2021': round(ajuste, 1), 'r': c['r_2010_2021'],
               'antes': {a: round(R[a]) for a in range(2018, 2024)}, 'n_nueva': c.get('n_nueva'), 'ancho_ic90': {a: round(x, 1) for a, x in ancho.items()}, 'extiende': extiende}
    print(f"{vk:13s} {'EXT' if extiende else 'no '} ic {[round(ancho[a]) for a in (2024,2025)]} r {c['r_2010_2021']:+.2f} err {ajuste:4.1f} puente {puente:.2f} | antes 21–23 {[round(R[a]) for a in (2021,2022,2023)]} → ahora 21–25 {[round(S[a]) if a in S else None for a in range(2021,2026)]}  pico {max(S, key=S.get)}")
json.dump(out, open('datos/pasarela_2025.json', 'w'), indent=1)
