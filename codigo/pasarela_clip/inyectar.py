"""Pasa a app/index.html la pasarela corregida (REC[].v 2010–2023, pv, vclip, vult) y el KM nuevo, y actualiza la exportación."""
import json, re, sys
REPO = '/Users/felipe/Documents/Ciclo K576/ciclo/'
P = json.load(open('datos/pasarela_2025.json')); KM = json.load(open('datos/KM_nuevo.json'))
p = REPO + 'app/index.html'; s = open(p).read()
def const(nombre):
    i = s.index('const ' + nombre + '='); j = s.index(';\n', i)
    return i, j, json.loads(s[i + len('const ' + nombre + '='):j])
i, j, REC = const('REC')
cambios = []
for r in REC:
    vk = r.get('vk')
    if not vk or vk not in P or not r.get('v'): continue
    v = P[vk]['v']; nuevo = list(r['v'])
    for a in range(2010, 2024): nuevo[a - 2004] = v[str(a)]
    for a in range(2024, 2026):
        if a - 2004 < len(nuevo): nuevo[a - 2004] = v.get(str(a))
    r['v'] = nuevo; r['vclip'] = 2022; r['vult'] = max(int(a) for a in v)
    pk = max(range(2010, r['vult'] + 1), key=lambda a: nuevo[a - 2004]); cambios.append((r['id'], r.get('pv'), pk)); r['pv'] = pk
s = s[:i] + 'const REC=' + json.dumps(REC, ensure_ascii=False, separators=(',', ':')) + s[j:]
i, j, _ = const('KM')
s = s[:i] + 'const KM=' + json.dumps(KM, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(p, 'w').write(s)
print('pico de pasarela (antes → ahora):', cambios)
e = REPO + 'datasets_procesados/ciclo_series__anual_por_atributo.json'; d = json.load(open(e))
d['REC'] = [x for x in REC if x['id'] in {r['id'] for r in d['REC']}] + [x for x in REC if x['id'] not in {r['id'] for r in d['REC']}][:0]
d['KM'] = KM
json.dump(d, open(e, 'w'), ensure_ascii=False)
print('exportación actualizada')
