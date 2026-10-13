"""Calcula el índice de Reddit 2026 en la misma escala que la serie del repositorio y lo escribe junto con
la proyección de pasarela (sólo los años que faltan).

Regla de la serie existente, verificada contra 2022–2025: media móvil centrada de 3 años de
posts/posts_totales; en el último año la media usa sólo ese año y el anterior. Se empalma en 2025:
escala = índice_2025_del_repo / media(2024, 2025), e índice_2026 = media(2025, 2026) × escala.

Uso: python3 empalmar_reddit_2026.py conteos.csv reddit_2026.csv pasarela.csv pasarela_proyeccion.csv
(conteos.csv sale de contar_terminos_reddit.py; pasarela.csv de proyectar_pasarela.py)."""
import json, csv, sys, statistics as st

cont, out_r, pas_in, out_p = sys.argv[1:]
d = json.load(open('datasets_procesados/ciclo_series__anual_por_atributo.json'))
n, tot, mes = {}, {}, {}
for r in csv.DictReader(open(cont)):
    k = (r['termino'], int(r['anio'])); n[k] = int(r['posts']); tot[k[1]] = int(r['posts_totales_anio']); mes[k[1]] = int(r['meses_cubiertos'])
def R(t, y): return sum(n[(x.strip(), y)] for x in t.split('+')) / tot[y]
def P(t, y): return sum(n[(x.strip(), y)] for x in t.split('+'))

ser = {k: v['i'] for k, v in d['RDS'].items()}
for r in d['REC']:
    if r.get('rk') and r.get('r') and r['rk'] not in ser: ser[r['rk']] = r['r']
i25 = 2025 - 2004
filas, errs = [], []
for t, s in sorted(ser.items()):
    base = (R(t, 2024) + R(t, 2025)) / 2
    idx26 = err = None
    if s[i25] not in (None, 0) and base:
        sc = s[i25] / base
        idx26 = round((R(t, 2025) + R(t, 2026)) / 2 * sc, 1)
        # control: 2024 recalculado con la misma regla, contra el valor que ya estaba en el repo
        rec24 = (R(t, 2023) + R(t, 2024) + R(t, 2025)) / 3 * sc
        if s[i25 - 1]:
            err = round(100 * (rec24 - s[i25 - 1]) / s[i25 - 1], 1); errs.append(abs(err))
    filas.append([t, 2026, P(t, 2026), tot[2026], round(1000 * R(t, 2026), 3), idx26, s[i25], err,
                  f'{mes[2026]} meses (01/01–12/10/2026)', 'medido', 'Reddit vía Arctic Shift'])
with open(out_r, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['termino', 'anio', 'posts', 'posts_totales_anio', 'posts_por_mil', 'indice', 'indice_2025_en_repo',
                'control_2024_error_pct', 'cobertura', 'tipo', 'fuente'])
    w.writerows(filas)
print('reddit: error mediano del control 2024 = %.1f %%, n=%d' % (st.median(errs), len(errs)))

rows = list(csv.reader(open(pas_in)))
with open(out_p, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(rows[0]); w.writerows(r for r in rows[1:] if r[7] == 'proyectado')
