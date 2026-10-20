"""Texturas de material para Diseñar (20/10/2026), en el mismo formato que las estampas de app/siluetas/estampas:
fichas de 120×120 que repiten sin costura, dibujadas en currentColor (con opacidad cuando hace falta un segundo valor,
nunca un segundo color). Dibujadas y no fotografiadas: las fotos de tela que tenemos no tienen licencia.
Escribe app/siluetas/materiales/*.svg. Uso, desde la raíz del repo: python3 codigo/estampas.py"""
import os, random
B = 'app/siluetas/materiales'
os.makedirs(B, exist_ok=True)

def textura(nombre, ruta, cuerpo):
    open(f'{B}/{ruta}.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120" role="img" aria-label="Muestra de {nombre}">'
        f'<defs><clipPath id="c"><rect width="120" height="120"/></clipPath></defs><g clip-path="url(#c)" fill="none" stroke="currentColor">{cuerpo}</g></svg>\n')

def rep(f, n, borde=12):
    """n figuras al azar; cada una se repite en la ficha vecina sólo si toca un borde, así repite sin costura sin pesar de más.
    f(x, y) dibuja una figura con su origen en (x, y)."""
    out = []
    for _ in range(n):
        x, y = random.uniform(0, 120), random.uniform(0, 120)
        dxs = [0] + ([120] if x < borde else []) + ([-120] if x > 120 - borde else [])
        dys = [0] + ([120] if y < borde else []) + ([-120] if y > 120 - borde else [])
        semilla = random.random()
        for dx in dxs:
            for dy in dys:
                random.seed(semilla); out.append(f(x + dx, y + dy))
        random.seed(semilla * 7919)
    return ''.join(out)

# denim: la sarga, diagonales finas y apretadas (período 6, divide 120)
textura('denim', 'denim', ''.join(f'<path d="M {x} 0 L {x+120} 120" stroke-width="1.6" opacity=".55"/>' for x in range(-120, 120, 6)) +
        ''.join(f'<path d="M {x} 0 L {x+120} 120" stroke-width=".6" opacity=".9"/>' for x in range(-117, 120, 12)))
# corduroy: las costillas verticales, anchas, con su sombra
textura('corduroy', 'corduroy', ''.join(f'<rect x="{x}" y="-1" width="6" height="122" fill="currentColor" stroke="none" opacity=".45"/><path d="M {x+1.5} 0 L {x+1.5} 120" stroke-width=".8"/>' for x in range(0, 120, 10)))
# cuero: el grano, celdas irregulares
random.seed(7)
textura('cuero', 'cuero', rep(lambda x, y: f'<path d="M {x:.1f} {y:.1f} q {random.uniform(-5,5):.1f} {random.uniform(-5,5):.1f} {random.uniform(6,11):.1f} {random.uniform(-3,3):.1f}" stroke-width=".9" opacity=".6"/>', 46))
# punto jersey: hileras de V chiquitas
textura('punto jersey', 'jersey', ''.join(f'<path d="M 0 {y}' + ' l 3 6 l 3 -6' * 20 + '" stroke-width=".9" opacity=".7"/>' for y in range(2, 120, 8)))
# rib: costillas de punto, verticales y finas
textura('rib', 'rib', ''.join(f'<path d="M {x} 0 L {x} 120" stroke-width="2.2" opacity=".5"/>' for x in range(2, 120, 6)))
# tweed: hebras cortas en todas direcciones, de dos intensidades
random.seed(3)
textura('tweed', 'tweed', rep(lambda x, y: f'<path d="M {x:.1f} {y:.1f} l {random.uniform(-7,7):.1f} {random.uniform(-7,7):.1f}" stroke-width="{random.choice([.7,1.3])}" opacity="{random.choice([.35,.75])}"/>', 90))
# gasa: transparencia, una trama muy abierta y suave
textura('gasa', 'gasa', ''.join(f'<path d="M 0 {y} L 120 {y}" stroke-width=".5" opacity=".35"/>' for y in range(0, 120, 4)) +
        ''.join(f'<path d="M {x} 0 L {x} 120" stroke-width=".5" opacity=".25"/>' for x in range(0, 120, 4)))
# satén: el brillo, ondas largas y suaves
textura('satén', 'saten', ''.join(f'<path d="M -10 {y} C 20 {y-10} 40 {y+10} 60 {y} S 100 {y-10} 130 {y}" stroke-width="{w}" opacity="{o}"/>'
                                  for y, w, o in [(15, 6, .18), (45, 3, .3), (75, 6, .18), (105, 3, .3)]))
# lino: el slub, hilos horizontales con engrosamientos irregulares
random.seed(11)
textura('lino', 'lino', ''.join(f'<path d="M 0 {y} L 120 {y}" stroke-width=".7" opacity=".5"/>' for y in range(0, 120, 5)) +
        rep(lambda x, y: f'<path d="M {x:.1f} {round(y/5)*5} l {random.uniform(6,16):.1f} 0" stroke-width="1.8" opacity=".55"/>', 16, borde=18))
# lana / paño: fieltro, puntitos densos
random.seed(5)
textura('lana', 'lana', rep(lambda x, y: f'<circle cx="{x:.1f}" cy="{y:.1f}" r=".9" fill="currentColor" stroke="none" opacity="{random.uniform(.2,.5):.2f}"/>', 110, borde=2))
# cable knit: trenzas
textura('cable knit', 'cable', ''.join(f'<path d="M {x} 0 C {x+10} 10 {x+10} 20 {x} 30 S {x-10} 50 {x} 60 S {x+10} 80 {x} 90 S {x-10} 110 {x} 120" stroke-width="1.6" opacity=".7"/>'
                                       f'<path d="M {x+10} 0 C {x} 10 {x} 20 {x+10} 30 S {x+20} 50 {x+10} 60 S {x} 80 {x+10} 90 S {x+20} 110 {x+10} 120" stroke-width="1.6" opacity=".7"/>'
                                       for x in (10, 70)) + ''.join(f'<path d="M {x} 0 L {x} 120" stroke-width="1" opacity=".4"/>' for x in (2, 38, 42, 62, 98, 102)))
# bouclé: rulos
random.seed(9)
textura('bouclé', 'boucle', rep(lambda x, y: f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(2,4):.1f}" stroke-width=".9" opacity=".55"/>', 60, borde=5))
# piqué: panal chico
textura('piqué', 'pique', ''.join(f'<path d="M 0 {y}' + ' l 4 -4 l 4 4' * 15 + f' M 0 {y}' + ' l 4 4 l 4 -4' * 15 + '" stroke-width=".8" opacity=".6"/>' for y in range(4, 120, 8)))
# popelina / algodón liso: tafetán, la trama más simple
textura('algodón liso', 'tafetan', ''.join(f'<path d="M 0 {y} L 120 {y}" stroke-width=".7" opacity=".35"/>' for y in range(0, 120, 3)) +
        ''.join(f'<path d="M {x} 0 L {x} 120" stroke-width=".7" opacity=".25"/>' for x in range(0, 120, 3)))
# sintético / nylon: brillo plano en franjas
textura('sintético', 'sintetico', ''.join(f'<rect x="-1" y="{y}" width="122" height="10" fill="currentColor" stroke="none" opacity="{o}"/>' for y, o in [(0, .08), (30, .16), (60, .08), (90, .16)]))
# encaje y acolchado, como detalle (no material): acolchado en rombos
textura('acolchado', 'acolchado', ''.join(f'<path d="M {x} 0 L {x+120} 120" stroke-width="1.2" opacity=".6"/><path d="M {x} 120 L {x+120} 0" stroke-width="1.2" opacity=".6"/>' for x in range(-120, 120, 30)))
print('listo:', len(os.listdir(B)), 'texturas')

# ---------- detalles y aplicaciones (app/siluetas/detalles) y dos estampas que faltaban ----------
def ficha(carpeta, nombre, ruta, cuerpo):
    os.makedirs(f'app/siluetas/{carpeta}', exist_ok=True)
    open(f'app/siluetas/{carpeta}/{ruta}.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120" role="img" aria-label="Muestra de {nombre}">'
        f'<defs><clipPath id="c"><rect width="120" height="120"/></clipPath></defs><g clip-path="url(#c)" fill="none" stroke="currentColor">{cuerpo}</g></svg>\n')
# bordado: florcitas de puntada, en grilla corrida
flor_b = lambda x, y: ''.join(f'<path d="M {x} {y} l {dx} {dy}" stroke-width="1.6" stroke-linecap="round" opacity=".85"/>' for dx, dy in [(0,-7),(6,-3),(6,4),(0,7),(-6,4),(-6,-3)]) + f'<circle cx="{x}" cy="{y}" r="1.6" fill="currentColor" stroke="none"/>'
ficha('detalles', 'bordado', 'bordado', ''.join(flor_b(x, y) for y in (15, 75) for x in (15, 75)) + ''.join(flor_b(x, y) for y in (45, 105) for x in (45, 105)) +
      ''.join(f'<path d="M {x} {y} l 4 0" stroke-width="1" opacity=".5"/>' for y in range(0, 120, 30) for x in range(26, 120, 60)))
# volados: hileras de ondas superpuestas
ficha('detalles', 'volados', 'volados', ''.join(f'<path d="M 0 {y}' + ''.join(f' q 7.5 {9} 15 0' for _ in range(8)) + f'" stroke-width="1.4" opacity=".8"/><path d="M 0 {y-6} L 120 {y-6}" stroke-width=".7" opacity=".4"/>' for y in range(14, 125, 20)))
# cut-outs: aberturas en gota, con su contorno
ficha('detalles', 'cut-outs', 'cutouts', ''.join(f'<path d="M {x} {y-12} C {x+9} {y-2} {x+9} {y+8} {x} {y+12} C {x-9} {y+8} {x-9} {y-2} {x} {y-12} Z" fill="currentColor" fill-opacity=".85" stroke-width="1"/>' for y in (30, 90) for x in (30, 90)))
# tachas: pirámides de metal
ficha('detalles', 'tachas', 'tachas', ''.join(f'<path d="M {x-5} {y} L {x} {y-5} L {x+5} {y} L {x} {y+5} Z" fill="currentColor" fill-opacity=".75" stroke-width=".8"/><path d="M {x-5} {y} L {x+5} {y} M {x} {y-5} L {x} {y+5}" stroke-width=".6" opacity=".5"/>' for y in range(10, 120, 20) for x in range(10 if (y // 20) % 2 == 0 else 20, 120, 20)))
# plisado: pliegues verticales con su sombra
ficha('detalles', 'plisado', 'plisado', ''.join(f'<rect x="{x}" y="-1" width="5" height="122" fill="currentColor" stroke="none" opacity=".22"/><path d="M {x} 0 L {x} 120" stroke-width="1.2"/>' for x in range(0, 120, 12)))
# flecos: hileras de tiras colgando
ficha('detalles', 'flecos', 'flecos', ''.join(f'<path d="M 0 {y} L 120 {y}" stroke-width="2" opacity=".8"/>' + ''.join(f'<path d="M {x} {y} L {x+1} {y+26}" stroke-width=".9" opacity=".75"/>' for x in range(1, 120, 4)) for y in (4, 64)))
# pedrería: cristales facetados
ficha('detalles', 'pedrería', 'pedreria', ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="currentColor" fill-opacity=".25" stroke-width="1"/><path d="M {x-4} {y} L {x+4} {y} M {x} {y-4} L {x} {y+4} M {x-2.8} {y-2.8} L {x+2.8} {y+2.8}" stroke-width=".5" opacity=".7"/>' for y in range(12, 120, 24) for x in range(12 if (y // 24) % 2 == 0 else 24, 120, 24)))
# corazones y geométrico (estampas que Tendencias nombraba sin dibujo)
cor = lambda x, y, r=7: f'<path d="M {x} {y+r} C {x-r*1.6} {y} {x-r} {y-r*1.1} {x} {y-r*.35} C {x+r} {y-r*1.1} {x+r*1.6} {y} {x} {y+r} Z" fill="currentColor" stroke="none"/>'
ficha('estampas', 'corazones', 'estampa_corazones', ''.join(cor(x, y) for y in range(15, 120, 30) for x in range(15 if (y // 30) % 2 == 0 else 30, 135, 30)))
ficha('estampas', 'geométrico', 'estampa_geometrico', ''.join(f'<path d="M {x} {y} l 15 -15 l 15 15 l -15 15 Z" fill="currentColor" fill-opacity="{.85 if (x // 30 + y // 30) % 2 else .25}" stroke="none"/>' for y in range(15, 135, 30) for x in range(0, 120, 30)))
print('listo: detalles y estampas nuevas')
