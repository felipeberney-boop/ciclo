"""CICLO — prueba con Reddit, según datasets/pruebas/prueba_reddit_preregistro.md.
Uso, desde la raíz del repo: python3 codigo/prueba_reddit.py   (sin dependencias)"""
import json, random

RDS = json.load(open('datasets_procesados/ciclo_series__anual_por_atributo.json'))['RDS']
ANIOS = list(range(2004, 2026))  # RDS: un valor por año, 2004–2025
PRUEBA = {  # atributo: (término de Reddit, etapa del modelo, congelada en el preregistro)
    'Jeans baggy': ('baggy jeans', 'En pico'), 'Jeans rectos': ('mom jeans', 'Saturada'),
    'Jeans skinny': ('skinny jeans', 'Saturada'), 'Buzo / hoodie': ('hoodie', 'Saturada'),
    'Floral': ('floral', 'Saturada'), 'Lunares': ('polka dot', 'En retorno'), 'Cuero': ('leather jacket', 'En retorno'),
    'Animal print': ('leopard', 'En retorno'), 'Kimono': ('kimono', 'Saturada'), 'Trench': ('trench', 'Saturada'),
    'Encaje': ('lace', 'En retorno'), 'Cuadros': ('plaid', 'En retorno'), 'Cargo': ('cargo pants', 'En pico'),
    'Y2K': ('y2k', 'En ascenso')}


def prom(serie, anios):
    return sum(serie[ANIOS.index(a)] for a in anios) / len(anios)


def momento(term):
    s = RDS[term]['i']
    return prom(s, [2023, 2024]) / prom(s, [2020, 2021]) - 1


def eta2(valores, grupos):
    media = sum(valores) / len(valores)
    total = sum((v - media) ** 2 for v in valores)
    entre = 0
    for g in set(grupos):
        vs = [v for v, h in zip(valores, grupos) if h == g]
        entre += len(vs) * (sum(vs) / len(vs) - media) ** 2
    return entre / total


atr = list(PRUEBA)
mom = [momento(PRUEBA[a][0]) for a in atr]
etapa = [PRUEBA[a][1] for a in atr]
obs = eta2(mom, etapa)
rnd, mayores, N = random.Random(2026), 0, 10_000
for _ in range(N):
    e = etapa[:]; rnd.shuffle(e); mayores += eta2(mom, e) >= obs - 1e-12
p = (mayores + 1) / (N + 1)

print('Atributo            Etapa del modelo   Momento en Reddit (2023–24 contra 2020–21)')
for a, m, e in sorted(zip(atr, mom, etapa), key=lambda x: -x[1]):
    print(f'  {a:17} {e:18} {m:+.0%}')
print('\nMomento medio por etapa:')
for g in ['En ascenso', 'En pico', 'En retorno', 'Saturada']:
    vs = [m for m, e in zip(mom, etapa) if e == g]
    print(f'  {g:11} {sum(vs) / len(vs):+.0%}  (n = {len(vs)})')
print(f'\nη² = {obs:.2f} · p = {p:.4f} ({N:,} barajadas)'.replace(',', '.'))
print('Veredicto según el preregistro:', 'SE SOSTIENE (p < 0,05)' if p < 0.05 else 'SE RECHAZA (p ≥ 0,05)')
