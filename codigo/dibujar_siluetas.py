"""Dibuja las siluetas que faltaban en app/siluetas (abrigos, cargo, corset, capucha y tres estampas), con el
mismo estilo que las de la carpeta: trazo currentColor de 1,7, detalles de 1,02, el primer <path> es el contorno
cerrado (la app lo rellena con el color y la estampa elegidos). Uso: python3 codigo/dibujar_siluetas.py"""
import os, random
B = 'app/siluetas'

def prenda(nombre, ruta, w, h, contorno, detalles):
    g = f'<path d="{contorno}"/>\n' + ''.join(f'<path d="{d}" stroke-width="1.02"/>\n' if not d.startswith('<') else d + '\n' for d in detalles)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{nombre}">\n'
           f'<g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round">\n{g}</g></svg>\n')
    os.makedirs(os.path.dirname(f'{B}/{ruta}'), exist_ok=True); open(f'{B}/{ruta}.svg', 'w').write(svg)

boton = lambda x, y, r=2.3: f'<circle cx="{x}" cy="{y}" r="{r}" stroke-width="1.02"/>'
# ---------- abrigos (200×300, misma caja que los fits) ----------
prenda('Trench', 'abrigos/trench', 200, 300,
  'M 83 40 C 77 48 62 44 52 50 L 30 196 L 50 200 L 60 110 L 54 286 L 146 286 L 140 110 L 150 200 L 170 196 L 148 50 C 138 44 123 48 117 40 C 107 50 93 50 83 40 Z',
  ['M 83 40 L 70 62 L 84 70 L 100 112', 'M 117 40 L 130 62 L 116 70 L 100 112', 'M 106 112 L 106 286',
   'M 58 148 L 142 148', 'M 58 158 L 142 158', 'M 94 146 L 106 146 L 106 160 L 94 160 Z',
   'M 64 58 L 80 92', 'M 136 58 L 120 92', 'M 37 176 L 55 180', 'M 163 176 L 145 180',
   boton(90, 124), boton(114, 124), boton(90, 138), boton(114, 138), boton(90, 180), boton(114, 180)])
prenda('Campera de cuero', 'abrigos/cuero', 200, 300,
  'M 83 40 C 77 48 60 46 50 52 L 32 196 L 52 198 L 60 112 L 60 200 L 140 200 L 140 112 L 148 198 L 168 196 L 150 52 C 140 46 123 48 117 40 C 107 50 93 50 83 40 Z',
  ['M 83 40 L 64 70 L 82 86 L 92 70', 'M 117 40 L 136 70 L 122 80', 'M 92 70 L 118 120 L 112 200',
   'M 60 186 L 140 186', 'M 68 146 L 86 132', 'M 124 156 L 134 142', 'M 38 180 L 54 182', 'M 162 180 L 146 182'])
prenda('Capa', 'abrigos/capa', 200, 300,
  'M 83 40 C 72 46 58 50 50 60 C 38 120 26 210 20 272 L 180 272 C 174 210 162 120 150 60 C 142 50 128 46 117 40 C 107 50 93 50 83 40 Z',
  ['M 100 52 L 100 272', 'M 54 170 L 62 212', 'M 146 170 L 138 212', 'M 83 40 C 86 56 114 56 117 40', boton(100, 64, 3), 'M 22 262 L 178 262'])
prenda('Kimono', 'abrigos/kimono', 200, 300,
  'M 80 40 L 20 54 L 20 132 L 58 132 L 60 270 L 140 270 L 142 132 L 180 132 L 180 54 L 120 40 C 110 48 90 48 80 40 Z',
  ['M 80 40 L 94 270', 'M 88 43 L 100 270', 'M 120 40 L 106 270', 'M 58 60 L 58 132', 'M 142 60 L 142 132', 'M 20 120 L 58 120', 'M 180 120 L 142 120'])
prenda('Blazer oversize', 'abrigos/blazer', 200, 300,
  'M 83 40 L 44 50 L 30 206 L 50 208 L 58 108 L 56 226 L 144 226 L 142 108 L 150 208 L 170 206 L 156 50 L 117 40 C 107 48 93 48 83 40 Z',
  ['M 83 40 L 70 62 L 80 70 L 73 76 L 98 150', 'M 117 40 L 130 62 L 120 70 L 127 76 L 102 150', 'M 100 150 L 100 226',
   'M 64 182 L 86 182', 'M 114 182 L 136 182', 'M 118 110 L 134 108', boton(100, 168), boton(100, 190)])
random.seed(7)
pelo = []
for _ in range(70):  # mechones cortos dentro del tapado
    x, y = random.uniform(62, 138), random.uniform(60, 262)
    if abs(x - 100) < 5: continue
    pelo.append(f'M {x:.1f} {y:.1f} l {random.uniform(-3, 3):.1f} {random.uniform(4, 7):.1f}')
prenda('Tapado de piel', 'abrigos/piel', 200, 300,
  'M 82 40 C 60 40 40 50 34 70 L 22 200 L 46 206 L 56 120 L 52 270 L 148 270 L 144 120 L 154 206 L 178 200 L 166 70 C 160 50 140 40 118 40 C 108 50 92 50 82 40 Z',
  ['M 82 40 C 70 70 80 110 100 132 C 120 110 130 70 118 40', 'M 100 132 L 100 270', 'M 22 186 C 30 192 40 194 48 192', 'M 178 186 C 170 192 160 194 152 192']
  + [f'<path d="{" ".join(pelo)}" stroke-width=".8" opacity=".6"/>'])
# ---------- cargo (200×340, misma cintura que los jeans) ----------
prenda('Pantalón cargo', 'pantalones/cargo', 200, 340,
  'M 44 36 C 43 80 46 110 44 132 L 48 326 L 96 326 L 100 148 L 104 326 L 152 326 L 156 132 C 154 110 157 80 156 36 Z',
  ['M 42 24 L 158 24 L 158 36 L 42 36 Z', 'M 100 80 L 100 148', 'M 103.5 36 C 105 56 104 70 101 80',
   'M 44 39 C 48 50 55 56 62 58', 'M 156 39 C 152 50 145 56 138 58',
   'M 45 168 L 72 168 L 72 222 L 46 222', 'M 45 176 L 72 176', 'M 155 168 L 128 168 L 128 222 L 154 222', 'M 155 176 L 128 176',
   'M 48 312 L 96 312', 'M 104 312 L 152 312', boton(58.5, 172, 1.6), boton(141.5, 172, 1.6)])
# ---------- corset ----------
lazo = ' '.join(f'M 96 {y} L 104 {y + 8} M 104 {y} L 96 {y + 8}' for y in range(96, 230, 16))
prenda('Corset', 'tops/corset', 200, 300,
  'M 50 72 C 66 62 86 66 100 82 C 114 66 134 62 150 72 C 146 110 136 140 138 170 C 140 200 148 222 150 244 L 50 244 C 52 222 60 200 62 170 C 64 140 54 110 50 72 Z',
  ['M 62 66 L 72 22', 'M 138 66 L 128 22', 'M 78 68 C 82 120 74 180 80 244', 'M 122 68 C 118 120 126 180 120 244', lazo])
# ---------- cuello: capucha (200×140, mismo recorte que los otros cuellos) ----------
prenda('Capucha', 'cuellos/cuello_capucha', 200, 140,
  'M 22 140 L 26 52 C 30 44 50 40 64 40 C 62 16 80 4 100 4 C 120 4 138 16 136 40 C 150 40 170 44 174 52 L 178 140 Z',
  ['M 72 46 C 72 24 86 14 100 14 C 114 14 128 24 128 46 C 118 58 82 58 72 46 Z', 'M 92 56 L 90 92', 'M 108 56 L 110 92'])
# ---------- estampas (120×120, repiten sin costura) ----------
def estampa(nombre, ruta, cuerpo):
    open(f'{B}/estampas/{ruta}.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120" role="img" aria-label="Muestra de estampa {nombre}">'
        f'<defs><clipPath id="c"><rect width="120" height="120"/></clipPath></defs><g clip-path="url(#c)" fill="currentColor" stroke="currentColor">{cuerpo}</g></svg>\n')
import math
def flor(cx, cy, r):
    p = ''.join(f'<ellipse cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" rx="{r * .62:.1f}" ry="{r * .42:.1f}" transform="rotate({math.degrees(a):.0f} {cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f})" stroke="none" opacity=".85"/>'
                for a in [k * 2 * math.pi / 5 - math.pi / 2 for k in range(5)])
    return p + f'<circle cx="{cx}" cy="{cy}" r="{r * .38:.1f}" stroke="none" opacity=".45"/>'
hoja = lambda x, y, a: f'<ellipse cx="{x}" cy="{y}" rx="6" ry="2.6" transform="rotate({a} {x} {y})" stroke="none" opacity=".5"/>'
estampa('Floral', 'estampa_floral', flor(30, 32, 9) + flor(90, 88, 9) + flor(92, 24, 5) + flor(26, 92, 5)
        + hoja(48, 44, 30) + hoja(72, 76, 30) + hoja(108, 40, -40) + hoja(12, 76, -40) + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" stroke="none" opacity=".6"/>' for x, y in [(60, 12), (58, 108), (112, 62), (6, 20), (60, 60)]))
red = ''.join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="none" stroke-width=".7" opacity=".45"/>' for y in range(0, 121, 10) for x in range(0 if y % 20 == 0 else 5, 121, 10))
motivo = lambda x, y: (f'<circle cx="{x}" cy="{y}" r="13" fill="none" stroke-width="1.6"/><circle cx="{x}" cy="{y}" r="7" fill="none" stroke-width="1.2"/>'
                       + ''.join(f'<circle cx="{x + 18 * math.cos(k * math.pi / 4):.1f}" cy="{y + 18 * math.sin(k * math.pi / 4):.1f}" r="3.2" stroke="none"/>' for k in range(8)))
estampa('Encaje', 'estampa_encaje', red + ''.join(motivo(x, y) for x, y in [(0, 0), (120, 0), (0, 120), (120, 120), (60, 60)]))
random.seed(3)
gam = ''.join(f'<circle cx="{random.uniform(0, 120):.1f}" cy="{random.uniform(0, 120):.1f}" r="{random.uniform(.5, 1.3):.2f}" stroke="none" opacity="{random.uniform(.15, .45):.2f}"/>' for _ in range(420))
gam += ''.join(f'<path d="M {x:.0f} {y:.0f} q 8 -3 16 0" fill="none" stroke-width="1.4" opacity=".14"/>' for x, y in [(random.uniform(0, 104), random.uniform(4, 116)) for _ in range(14)])
estampa('Gamuza', 'estampa_gamuza', gam)
print('listo')
# lunares y rayas: las de la carpeta (polka-dot, breton) tienen período 26 y 22, que no divide 120, y en la app se
# ve la costura al repetir. Estas repiten exacto.
estampa('Lunares', 'estampa_lunares', ''.join(f'<circle cx="{x}" cy="{y}" r="5.5" stroke="none"/>' for y in range(0, 121, 30) for x in range(0 if y % 60 == 0 else 15, 136, 30)))
estampa('Rayas', 'estampa_rayas', ''.join(f'<rect x="-2" y="{y}" width="124" height="8" stroke="none"/>' for y in range(6, 120, 20)))
