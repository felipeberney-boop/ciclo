"""CICLO — evalúa la prueba del jurado, con el análisis y el criterio fijados en datasets/jurado/preregistro.md.

Uso, desde la raíz del repo:  python3 codigo/evaluar_jurado.py [datasets/jurado/respuestas.txt]
Cada línea de respuestas es un código del formulario app/jurado/: CICLO-JURADO-1|nombre|rol|años|17 letras
(e emergente, a ascenso, p pico, s saturada, r retorno, x no sé), en el orden de ATR de abajo.
Sin dependencias: sólo la biblioteca estándar."""
import random, sys, itertools

# mismo orden que ATR en app/jurado/index.html; etapas del modelo congeladas en el preregistro (27/10/2026)
MODELO = {'Jeans baggy': 'p', 'Jeans rectos': 's', 'Jeans skinny': 's', 'Buzo / hoodie': 's', 'Floral': 's',
          'Lunares': 'r', 'Cuero': 'r', 'Animal print': 'r', 'Kimono': 's', 'Capa': 's', 'Trench': 's',
          'Encaje': 'r', 'Cuadros': 'r', 'Piel': 'r', 'Cargo': 'p', 'Y2K': 'a', 'Blazer oversize': 's'}
ATR = list(MODELO)
ETAPA = {'e': 'emergente', 'a': 'en ascenso', 'p': 'en pico', 's': 'saturada', 'r': 'en retorno', 'x': 'no sé'}
PERMUTACIONES, SEMILLA = 10_000, 2026


def leer(ruta):
    jurado, vistos = [], set()
    for n, linea in enumerate(open(ruta, encoding='utf8'), 1):
        linea = linea.strip()
        if not linea or linea.startswith('#'):
            continue
        partes = linea.split('|')
        if len(partes) != 5 or partes[0] != 'CICLO-JURADO-1' or len(partes[4]) != len(ATR) or set(partes[4]) - set(ETAPA):
            print(f'  línea {n} ignorada: no es un código válido'); continue
        if partes[1] != '-' and partes[1].lower() in vistos:
            print(f'  línea {n} ignorada: «{partes[1]}» ya respondió'); continue
        vistos.add(partes[1].lower())
        jurado.append({'nombre': partes[1], 'rol': partes[2], 'anios': partes[3], 'r': dict(zip(ATR, partes[4]))})
    return jurado


def acuerdo(persona, modelo):
    """proporción de coincidencias con el modelo, sin contar los «no sé»"""
    pares = [(persona[a], modelo[a]) for a in ATR if persona[a] != 'x']
    return sum(x == y for x, y in pares) / len(pares) if pares else None


def kappa(r1, r2):
    """kappa de Cohen entre dos personas, sobre los atributos que las dos respondieron"""
    pares = [(r1[a], r2[a]) for a in ATR if r1[a] != 'x' and r2[a] != 'x']
    if len(pares) < 5:
        return None
    n = len(pares); po = sum(x == y for x, y in pares) / n
    pe = sum((sum(x == k for x, _ in pares) / n) * (sum(y == k for _, y in pares) / n) for k in 'eapsr')
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else 'datasets/jurado/respuestas.txt'
    jurado = leer(ruta)
    print(f'Jurado: {len(jurado)} personas')
    if len(jurado) < 5:
        print('El preregistro pide al menos 5 personas. Todavía no se puede concluir.')
        if not jurado:
            return
    # 1 · acuerdo del modelo con cada persona
    ac = [acuerdo(p['r'], MODELO) for p in jurado]
    ac = [x for x in ac if x is not None]
    obs = sum(ac) / len(ac)
    # 2 · contra el azar: barajar las etapas del modelo entre los atributos
    rnd = random.Random(SEMILLA); etiquetas = list(MODELO.values()); mayores = 0
    for _ in range(PERMUTACIONES):
        rnd.shuffle(etiquetas); m = dict(zip(ATR, etiquetas))
        v = [acuerdo(p['r'], m) for p in jurado]; v = [x for x in v if x is not None]
        mayores += sum(v) / len(v) >= obs - 1e-12
    p = (mayores + 1) / (PERMUTACIONES + 1)
    # 3 · acuerdo del jurado entre sí
    ks = [k for a, b in itertools.combinations(jurado, 2) if (k := kappa(a['r'], b['r'])) is not None]
    kj = sum(ks) / len(ks) if ks else None
    print(f'Acuerdo del modelo con el jurado: {obs:.1%} (promedio entre personas)')
    print(f'Contra el azar ({PERMUTACIONES:,} barajadas): p = {p:.4f}'.replace(',', '.'))
    print(f'Acuerdo del jurado entre sí (kappa promedio): {kj:.2f}' if kj is not None else 'Acuerdo del jurado entre sí: no se puede calcular')
    # el detalle, atributo por atributo
    print('\nAtributo            Modelo       Jurado (etapa más votada, votos)')
    for a in ATR:
        votos = [p['r'][a] for p in jurado if p['r'][a] != 'x']
        top = max(set(votos), key=votos.count) if votos else 'x'
        print(f'  {a:18} {ETAPA[MODELO[a]]:12} {ETAPA[top]} ({votos.count(top)} de {len(votos)})')
    # criterio del preregistro
    print('\nVeredicto según el preregistro:')
    if len(jurado) < 5:
        print('  Faltan personas (mínimo 5).')
    elif kj is None or kj < 0.20:
        print('  NO CONCLUYE: el jurado no se pone de acuerdo entre sí (kappa < 0,20).')
    elif p < 0.05:
        print('  H SE SOSTIENE: el modelo coincide con el jurado más de lo que daría el azar (p < 0,05).')
    else:
        print('  H SE RECHAZA: el modelo no coincide con el jurado más que por azar (p ≥ 0,05).')


if __name__ == '__main__':
    main()
