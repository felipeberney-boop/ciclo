"""Dibuja las siluetas de la taxonomía nueva de Diseñar (20/10/2026): tipos de pantalón, tiros, faldas, vestidos,
tops, camisas, buzos y sweaters, abrigos y enteritos. Mismo estilo que codigo/dibujar_siluetas.py: trazo currentColor de
1,7, detalles de 1,02, y el primer <path> es el contorno cerrado (la app lo rellena con el color y la textura elegidos).
Pantalones en la caja de los jeans (200×340); el resto en la de los fits y abrigos (200×300).
Uso, desde la raíz del repo: python3 codigo/dibujar_taxonomia.py"""
import os
B = 'app/siluetas'

def prenda(nombre, ruta, w, h, contorno, detalles):
    g = f'<path d="{contorno}"/>\n' + ''.join(f'<path d="{d}" stroke-width="1.02"/>\n' if not d.startswith('<') else d + '\n' for d in detalles)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{nombre}">\n'
           f'<g fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round">\n{g}</g></svg>\n')
    os.makedirs(os.path.dirname(f'{B}/{ruta}'), exist_ok=True)
    open(f'{B}/{ruta}.svg', 'w').write(svg)

boton = lambda x, y, r=2.3: f'<circle cx="{x}" cy="{y}" r="{r}" stroke-width="1.02"/>'

# ---------- pantalones: el largo es lo único que cambia (misma cintura, misma pierna recta) ----------
def pantalon(nombre, ruta, ruedo, cintura=36, faja=12):
    lx = lambda y: 57 + (64 - 57) * (y - 132) / (330 - 132)          # costado de la pierna, recto
    c = (f'M 53 {cintura} C 52 {cintura+40} 55 106 57 132 L {lx(ruedo):.1f} {ruedo} L 96 {ruedo} L 100 148 L 104 {ruedo} '
         f'L {200-lx(ruedo):.1f} {ruedo} L 143 132 C 145 106 148 {cintura+40} 147 {cintura} Z')
    d = [f'M 53 {cintura-faja} L 147 {cintura-faja} L 147 {cintura} L 53 {cintura} Z', f'M 100 {cintura+44} L 100 148',
         f'M 60 {cintura-faja-3} L 60 {cintura+3}', f'M 140 {cintura-faja-3} L 140 {cintura+3}', boton(100, cintura - faja / 2),
         f'M 55 {cintura+3} C 59 {cintura+14} 66 {cintura+20} 73 {cintura+22}', f'M 145 {cintura+3} C 141 {cintura+14} 134 {cintura+20} 127 {cintura+22}']
    if ruedo < 320:  # ruedo dado vuelta en los cortos
        d += [f'M {lx(ruedo)+.5:.1f} {ruedo-8} L 96 {ruedo-8}', f'M 104 {ruedo-8} L {200-lx(ruedo)-.5:.1f} {ruedo-8}']
    prenda(nombre, ruta, 200, 340, c, d)

pantalon('Pantalón largo', 'pantalones/largo', 330)
pantalon('Short', 'pantalones/short', 196)
pantalon('Bermuda', 'pantalones/bermuda', 248)
pantalon('Capri', 'pantalones/capri', 292)
# tiros: el mismo pantalón con la cintura más arriba o más abajo; la entrepierna no se mueve
pantalon('Tiro alto', 'tiros/alto', 330, cintura=20)
pantalon('Tiro medio', 'tiros/medio', 330, cintura=36)
pantalon('Tiro bajo', 'tiros/bajo', 330, cintura=58, faja=10)

# ---------- faldas ----------
def falda(nombre, ruta, ruedo, vuelo):
    c = f'M 62 36 L 138 36 L {138+vuelo} {ruedo} L {62-vuelo} {ruedo} Z'
    d = ['M 62 24 L 138 24 L 138 36 L 62 36 Z', boton(100, 30), 'M 112 36 L 112 76', f'M {84-vuelo*.3:.1f} 60 L {80-vuelo*.6:.1f} {ruedo-4}',
         f'M {116+vuelo*.3:.1f} 60 L {120+vuelo*.6:.1f} {ruedo-4}']
    prenda(nombre, ruta, 200, 340, c, d)

falda('Falda mini', 'faldas/mini', 124, 16)
falda('Falda midi', 'faldas/midi', 226, 30)
falda('Falda maxi', 'faldas/maxi', 326, 44)

# ---------- vestidos (200×300) ----------
prenda('Vestido slip', 'vestidos/slip', 200, 300,
  'M 64 62 C 80 54 120 54 136 62 L 140 150 L 152 286 L 48 286 L 60 150 Z',
  ['M 70 62 L 74 18', 'M 130 62 L 126 18', 'M 66 70 C 84 80 116 80 134 70', 'M 52 270 C 80 276 120 276 148 270'])
prenda('Vestido camisero', 'vestidos/camisero', 200, 300,
  'M 72 30 L 50 44 L 34 112 L 52 116 L 62 76 L 62 150 L 54 286 L 146 286 L 138 150 L 138 76 L 148 116 L 166 112 L 150 44 L 128 30 C 116 40 84 40 72 30 Z',
  ['M 72 30 L 86 48 L 100 40 L 114 48 L 128 30', 'M 100 40 L 100 286', 'M 62 150 L 138 150', 'M 62 158 L 138 158',
   boton(104, 64), boton(104, 92), boton(104, 120), boton(104, 186), boton(104, 216)])
prenda('Vestido cruzado', 'vestidos/cruzado', 200, 300,
  'M 74 30 L 54 40 L 42 78 L 60 84 L 64 66 L 64 140 L 50 286 L 150 286 L 136 140 L 136 66 L 140 84 L 158 78 L 146 40 L 126 30 C 116 70 108 100 100 120 C 92 100 84 70 74 30 Z',
  ['M 74 30 L 120 132', 'M 126 30 L 96 108', 'M 64 140 C 90 146 112 146 136 140', 'M 136 140 L 156 176', 'M 136 140 L 148 186', 'M 120 132 L 132 286'])
prenda('Vestido tubo', 'vestidos/tubo', 200, 300,
  'M 76 30 L 60 40 L 56 70 L 66 72 L 70 56 C 66 100 64 130 68 150 C 64 200 66 250 70 286 L 130 286 C 134 250 136 200 132 150 C 136 130 134 100 130 56 L 134 72 L 144 70 L 140 40 L 124 30 C 114 40 86 40 76 30 Z',
  ['M 76 30 C 86 44 114 44 124 30', 'M 70 150 C 90 154 110 154 130 150', 'M 100 230 L 100 286'])
prenda('Vestido evasé', 'vestidos/evase', 200, 300,
  'M 76 30 L 60 38 L 54 70 L 66 72 L 70 54 L 68 120 L 36 286 L 164 286 L 132 120 L 130 54 L 134 72 L 146 70 L 140 38 L 124 30 C 114 42 86 42 76 30 Z',
  ['M 76 30 C 86 44 114 44 124 30', 'M 68 120 C 90 126 110 126 132 120', 'M 84 124 L 66 284', 'M 116 124 L 134 284'])

# ---------- remeras y tops ----------
prenda('Musculosa', 'tops/musculosa', 200, 300,
  'M 72 22 C 70 50 62 70 56 84 L 58 270 L 142 270 L 144 84 C 138 70 130 50 128 22 C 120 26 116 52 100 54 C 84 52 80 26 72 22 Z',
  ['M 80 24 C 82 44 90 58 100 60 C 110 58 118 44 120 24', 'M 58 262 L 142 262'])
prenda('Top', 'tops/top', 200, 300,
  'M 66 70 C 80 62 120 62 134 70 L 138 150 L 62 150 Z',
  ['M 72 66 L 76 22', 'M 128 66 L 124 22', 'M 64 80 C 84 88 116 88 136 80', 'M 62 142 L 138 142'])

# ---------- camisas ----------
def camisa(nombre, ruta, ancho=0, largo=270, hombro=0):
    a, h = ancho, hombro
    c = (f'M 76 32 L {54-a-h} {44+h} L {34-a} 210 L {54-a} 214 L {62-a} 92 L {62-a} {largo} L {138+a} {largo} L {138+a} 92 '
         f'L {146+a} 214 L {166+a} 210 L {146+a+h} {44+h} L 124 32 C 114 42 86 42 76 32 Z')
    d = ['M 76 32 L 88 52 L 100 42 L 112 52 L 124 32', f'M 100 42 L 100 {largo}', boton(104, 70), boton(104, 104), boton(104, 138)]
    if largo > 200: d += [boton(104, 172), boton(104, 206)]
    d += [f'M {36-a} 200 L {55-a} 204', f'M {164+a} 200 L {145+a} 204']
    prenda(nombre, ruta, 200, 300, c, d)

camisa('Camisa clásica', 'camisas/clasica')
camisa('Camisa oversize', 'camisas/oversize', ancho=12, largo=280, hombro=6)
camisa('Camisa cropped', 'camisas/cropped', largo=170)
prenda('Blusa', 'camisas/blusa', 200, 300,
  'M 78 34 C 60 34 40 46 34 74 C 32 92 44 104 58 100 L 62 92 L 64 230 L 136 230 L 138 92 L 142 100 C 156 104 168 92 166 74 C 160 46 140 34 122 34 C 112 46 88 46 78 34 Z',
  ['M 78 34 C 88 48 112 48 122 34', 'M 100 46 L 92 70', 'M 100 46 L 108 70', 'M 46 70 C 44 84 48 92 58 96', 'M 154 70 C 156 84 152 92 142 96',
   'M 64 222 C 88 228 112 228 136 222'])

# ---------- buzos y sweaters ----------
prenda('Buzo con capucha', 'buzos/capucha', 200, 300,
  'M 80 40 C 62 40 42 50 36 70 L 24 206 L 48 210 L 58 118 L 56 270 L 144 270 L 142 118 L 152 210 L 176 206 L 164 70 C 158 50 138 40 120 40 C 132 26 128 4 100 4 C 72 4 68 26 80 40 Z',
  ['M 80 40 C 84 56 116 56 120 40', 'M 92 48 L 90 92', 'M 108 48 L 110 92', 'M 70 170 L 130 170 L 136 214 L 64 214 Z', 'M 100 170 L 100 214',
   'M 56 258 L 144 258', 'M 26 194 L 49 198', 'M 174 194 L 151 198'])
prenda('Sweater', 'buzos/sweater', 200, 300,
  'M 80 36 C 62 38 42 48 36 70 L 24 206 L 48 210 L 58 118 L 56 270 L 144 270 L 142 118 L 152 210 L 176 206 L 164 70 C 158 48 138 38 120 36 C 112 46 88 46 80 36 Z',
  ['M 80 36 C 88 52 112 52 120 36', 'M 84 42 C 92 56 108 56 116 42', 'M 56 254 L 144 254', 'M 26 194 L 49 198', 'M 174 194 L 151 198',
   'M 70 262 L 70 268', 'M 86 262 L 86 268', 'M 100 262 L 100 268', 'M 114 262 L 114 268', 'M 130 262 L 130 268'])
prenda('Cárdigan', 'buzos/cardigan', 200, 300,
  'M 82 34 C 62 38 42 48 36 70 L 24 206 L 48 210 L 58 118 L 56 270 L 144 270 L 142 118 L 152 210 L 176 206 L 164 70 C 158 48 138 38 118 34 L 100 120 Z',
  ['M 100 120 L 100 270', 'M 56 254 L 144 254', boton(106, 140), boton(106, 172), boton(106, 204), boton(106, 236), 'M 26 194 L 49 198', 'M 174 194 L 151 198'])
prenda('Polera', 'buzos/polera', 200, 300,
  'M 82 40 C 62 42 42 50 36 72 L 24 206 L 48 210 L 58 118 L 56 270 L 144 270 L 142 118 L 152 210 L 176 206 L 164 72 C 158 50 138 42 118 40 L 118 10 L 82 10 Z',
  ['M 82 20 L 118 20', 'M 82 30 L 118 30', 'M 56 254 L 144 254', 'M 26 194 L 49 198', 'M 174 194 L 151 198'])

# ---------- camperas y abrigos ----------
prenda('Tapado', 'abrigos/tapado', 200, 300,
  'M 82 34 C 76 44 62 42 52 48 L 30 196 L 50 200 L 60 110 L 54 290 L 146 290 L 140 110 L 150 200 L 170 196 L 148 48 C 138 42 124 44 118 34 C 108 44 92 44 82 34 Z',
  ['M 82 34 L 72 58 L 86 66 L 100 104', 'M 118 34 L 128 58 L 114 66 L 100 104', 'M 104 104 L 104 290', boton(94, 130), boton(94, 170), boton(94, 210),
   'M 62 186 L 82 186', 'M 118 186 L 138 186'])
prenda('Puffer', 'abrigos/puffer', 200, 300,
  'M 76 30 C 60 32 44 42 36 62 C 26 110 22 160 20 210 L 50 214 L 58 120 L 54 236 L 146 236 L 142 120 L 150 214 L 180 210 C 178 160 174 110 164 62 C 156 42 140 32 124 30 L 124 12 L 76 12 Z',
  ['M 100 12 L 100 236', 'M 56 82 C 80 88 120 88 144 82', 'M 56 122 C 80 128 120 128 144 122', 'M 55 162 C 80 168 120 168 145 162', 'M 54 200 C 80 206 120 206 146 200',
   'M 30 104 L 50 108', 'M 26 150 L 48 154', 'M 170 104 L 150 108', 'M 174 150 L 152 154'])

# ---------- enteritos ----------
prenda('Mono largo', 'enteritos/largo', 200, 340,
  'M 76 30 L 56 40 L 50 86 L 64 88 L 66 66 L 64 150 C 60 170 58 200 58 240 L 64 330 L 96 330 L 100 196 L 104 330 L 136 330 L 142 240 C 142 200 140 170 136 150 L 134 66 L 136 88 L 150 86 L 144 40 L 124 30 C 114 46 86 46 76 30 Z',
  ['M 76 30 L 100 70 L 124 30', 'M 64 150 C 88 156 112 156 136 150', 'M 100 70 L 100 196'])
prenda('Mono corto', 'enteritos/corto', 200, 340,
  'M 76 30 L 56 40 L 50 86 L 64 88 L 66 66 L 64 150 C 60 170 58 190 60 214 L 96 214 L 100 196 L 104 214 L 140 214 C 142 190 140 170 136 150 L 134 66 L 136 88 L 150 86 L 144 40 L 124 30 C 114 46 86 46 76 30 Z',
  ['M 76 30 L 100 70 L 124 30', 'M 64 150 C 88 156 112 156 136 150', 'M 100 70 L 100 196', 'M 61 206 L 96 206', 'M 104 206 L 139 206'])
prenda('Jardinero', 'enteritos/jardinero', 200, 340,
  'M 70 90 L 130 90 L 134 150 C 140 170 144 200 142 240 L 136 330 L 104 330 L 100 196 L 96 330 L 64 330 L 58 240 C 56 200 60 170 66 150 Z',
  ['M 74 90 L 70 30', 'M 126 90 L 130 30', 'M 82 104 L 118 104 L 118 128 L 82 128 Z', boton(74, 96), boton(126, 96), 'M 66 150 C 88 156 112 156 134 150'])
print('listo')

# ---------- buzos y sweaters, partidos (20/10/2026) ----------
cuerpo_buzo = 'C 62 42 42 50 36 70 L 24 206 L 48 210 L 58 118 L 56 270 L 144 270 L 142 118 L 152 210 L 176 206 L 164 70 C 158 50 138 42 120 40'
prenda('Canguro con cierre', 'buzos/zip', 200, 300,
  'M 80 40 ' + cuerpo_buzo + ' C 132 26 128 4 100 4 C 72 4 68 26 80 40 Z',
  ['M 80 40 C 84 56 116 56 120 40', 'M 100 50 L 100 270', 'M 97 52 L 97 270', 'M 103 52 L 103 270', 'M 70 176 L 92 176 L 92 214 L 66 214 Z', 'M 108 176 L 130 176 L 134 214 L 108 214 Z',
   'M 56 258 L 144 258', 'M 26 194 L 49 198', 'M 174 194 L 151 198'])
prenda('Buzo cuello redondo', 'buzos/redondo', 200, 300,
  'M 80 38 ' + cuerpo_buzo.replace('120 40', '120 38') + ' C 112 50 88 50 80 38 Z',
  ['M 80 38 C 88 54 112 54 120 38', 'M 82 46 C 90 60 110 60 118 46', 'M 56 250 L 144 250', 'M 56 262 L 144 262', 'M 26 186 L 49 190', 'M 26 196 L 49 200', 'M 174 186 L 151 190', 'M 174 196 L 151 200'])
prenda('Sweater cuello en V', 'sweaters/cuello_v', 200, 300,
  'M 80 36 C 62 38 42 48 36 70 L 24 206 L 48 210 L 58 118 L 56 270 L 144 270 L 142 118 L 152 210 L 176 206 L 164 70 C 158 48 138 38 120 36 L 100 96 Z',
  ['M 86 40 L 100 84 L 114 40', 'M 56 254 L 144 254', 'M 26 194 L 49 198', 'M 174 194 L 151 198',
   'M 70 262 L 70 268', 'M 86 262 L 86 268', 'M 100 262 L 100 268', 'M 114 262 L 114 268', 'M 130 262 L 130 268'])

# ---------- calzado y accesorios (21/10/2026), en la caja de 200×200, vistos de costado ----------
prenda('Zapatillas', 'calzado/zapatillas', 200, 200,
  'M 24 132 C 24 112 30 98 46 92 L 92 78 C 104 74 114 80 122 90 C 136 104 160 108 176 114 C 184 118 186 128 184 140 L 24 140 Z',
  ['M 24 140 L 184 140 L 184 150 L 24 150 Z', 'M 70 86 L 84 110', 'M 82 82 L 96 104', 'M 94 80 L 106 100', 'M 46 112 C 80 118 130 120 176 124'])
prenda('Botinetas', 'calzado/botinetas', 200, 200,
  'M 60 40 L 104 40 L 106 110 C 126 116 160 122 172 134 L 172 150 L 46 150 L 46 128 C 50 110 56 80 60 40 Z',
  ['M 46 150 L 46 160 L 72 160 L 72 150', 'M 104 40 L 104 104', 'M 60 48 L 104 48'])
prenda('Mocasines', 'calzado/mocasines', 200, 200,
  'M 30 140 C 26 124 32 112 48 108 L 108 102 C 132 100 160 112 176 124 C 182 130 182 138 178 140 Z',
  ['M 30 140 L 178 140 L 178 148 L 30 148 Z', 'M 96 104 C 110 112 140 114 158 114', 'M 112 108 L 140 108 L 140 116 L 112 116 Z'])
prenda('Chatitas', 'calzado/chatitas', 200, 200,
  'M 30 140 C 26 128 34 118 50 116 C 80 112 104 118 124 120 C 150 120 170 126 178 134 L 178 140 Z',
  ['M 30 140 L 178 140 L 178 145 L 30 145 Z', 'M 120 122 C 126 116 132 116 136 122'])
prenda('Sandalias', 'calzado/sandalias', 200, 200,
  'M 26 140 L 180 140 L 180 148 L 26 148 Z',
  ['M 60 140 C 64 116 84 108 100 118', 'M 110 140 C 116 112 146 108 158 132', 'M 40 140 C 44 124 50 118 58 116'])
prenda('Plataformas', 'calzado/plataformas', 200, 200,
  'M 30 118 C 28 104 36 96 52 94 L 112 92 C 140 92 164 104 176 114 L 178 118 Z',
  ['M 30 118 L 178 118 L 178 152 L 30 152 Z', 'M 30 134 L 178 134'])
prenda('Guillerminas', 'calzado/guillerminas', 200, 200,
  'M 30 140 C 26 126 34 116 50 114 C 82 110 108 116 128 118 C 152 118 170 126 178 134 L 178 140 Z',
  ['M 30 140 L 178 140 L 178 146 L 30 146 Z', 'M 84 114 C 90 98 106 96 112 116', boton(106, 104), 'M 30 146 L 30 152 L 50 152 L 50 146'])
prenda('Botas texanas', 'calzado/texanas', 200, 200,
  'M 62 14 L 112 14 L 108 104 C 130 112 160 118 174 130 L 176 150 L 50 150 L 52 132 C 56 96 58 50 62 14 Z',
  ['M 50 150 L 50 162 L 74 162 L 72 150', 'M 66 30 C 76 44 98 44 106 30', 'M 70 60 C 80 74 96 74 104 60', 'M 62 14 L 52 4', 'M 112 14 L 120 4'])
prenda('Tote', 'accesorios/tote', 200, 200,
  'M 40 70 L 160 70 L 166 180 L 34 180 Z',
  ['M 70 70 C 70 30 130 30 130 70', 'M 80 70 C 80 42 120 42 120 70', 'M 40 82 L 160 82'])
prenda('Piluso', 'accesorios/piluso', 200, 200,
  'M 62 60 C 62 40 138 40 138 60 L 146 112 L 54 112 Z',
  ['M 54 112 C 30 116 24 136 36 140 C 70 150 130 150 164 140 C 176 136 170 116 146 112', 'M 58 100 L 142 100'])
prenda('Gorra', 'accesorios/gorra', 200, 200,
  'M 40 120 C 40 70 70 50 104 50 C 138 50 160 76 160 120 Z',
  ['M 40 120 C 80 112 120 112 160 120', 'M 154 118 C 176 120 192 128 190 136 C 170 140 150 132 140 124', 'M 104 50 L 104 120', boton(104, 54, 3)])
prenda('Cinturón', 'accesorios/cinturon', 200, 200,
  'M 10 86 L 190 86 L 190 114 L 10 114 Z',
  ['M 120 80 L 152 80 L 152 120 L 120 120 Z', 'M 126 100 L 160 100', boton(40, 100), boton(60, 100), boton(80, 100)])
prenda('Anteojos de sol', 'accesorios/anteojos', 200, 200,
  'M 20 90 C 20 80 26 76 36 76 L 86 76 C 94 76 96 82 94 92 C 90 120 78 128 56 128 C 34 128 22 116 20 90 Z',
  ['M 106 92 C 104 82 106 76 114 76 L 164 76 C 174 76 180 80 180 90 C 178 116 166 128 144 128 C 122 128 110 120 106 92', 'M 94 86 C 98 82 102 82 106 86',
   'M 20 82 L 6 78', 'M 180 82 L 194 78'])
