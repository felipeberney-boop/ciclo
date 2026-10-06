# -*- coding: utf-8 -*-
"""Genera las 20 laminas de la Entrega 2 de CICLO como SVG 1920x1080,
en el sistema visual de la Entrega 1 (Instrument Sans, negro/crema/blanco,
salmon = IA)."""
import os, html

W, H, M = 1920, 1080, 100
BLACK, CREAM, WHITE = '#000000', '#F6F0EB', '#FFFFFF'
SALMON, INK2, WIRE, WIRE2 = '#FFAFA3', '#5C5955', '#C9C4BE', '#E6E1DB'
SALMON_T, GREY_D = '#B8503D', '#8A857E'   # salmon legible sobre crema · gris sobre negro
FONT = "Instrument Sans, Helvetica Neue, Arial, sans-serif"
OUT = 'entrega2_svg'
os.makedirs(OUT, exist_ok=True)

def esc(s): return html.escape(s, quote=True)

def wrap(text, width, size, weight=400):
    f = 0.545 if weight < 600 else 0.565
    mx = max(1, int(width / (size * f)))
    out = []
    for para in text.split('\n'):
        if not para.strip():
            out.append('')
            continue
        line = ''
        for w in para.split(' '):
            t = (line + ' ' + w).strip()
            if len(t) <= mx:
                line = t
            else:
                if line: out.append(line)
                line = w
        out.append(line)
    return out

def txt(x, y, size, weight, color, content, width=None, lh=1.3, ls=0, align='start'):
    """y = borde superior del bloque de texto."""
    lines = wrap(content, width, size, weight) if width else content.split('\n')
    anchor = {'start': 'start', 'middle': 'middle', 'end': 'end'}[align]
    ax = x if align == 'start' else (x + width / 2 if align == 'middle' else x + width)
    parts = [f'<text x="{ax:.0f}" y="{y + size*0.80:.0f}" font-family="{FONT}" '
             f'font-size="{size}" font-weight="{weight}" fill="{color}" '
             f'text-anchor="{anchor}"'
             + (f' letter-spacing="{ls}"' if ls else '') + '>']
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else size * lh
        parts.append(f'<tspan x="{ax:.0f}" dy="{dy:.1f}">{esc(ln) or "&#160;"}</tspan>')
    parts.append('</text>')
    return ''.join(parts), y + size * 0.80 + (len(lines) - 1) * size * lh + size * 0.35

def t(*a, **k): return txt(*a, **k)[0]
def tend(*a, **k): return txt(*a, **k)[1]

def rect(x, y, w, h, fill, r=0, stroke=None, sw=2):
    s = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{fill}"'
    if r: s += f' rx="{r}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + '/>'

def line(x1, y1, x2, y2, color, w=2):
    return (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
            f'stroke="{color}" stroke-width="{w}"/>')

def slide(name, bg, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">{rect(0,0,W,H,bg)}{body}</svg>')
    open(f'{OUT}/{name}.svg', 'w', encoding='utf-8').write(svg)
    return name

def eyebrow(label, color=INK2, y=M):
    return t(M, y, 30, 400, color, label, ls=6)

def title(s, color=BLACK, y=160, size=110, width=1500):
    return t(M, y, size, 500, color, s, width=width, lh=1.0)

# ───────────────────────── 01 PORTADA ─────────────────────────
b = (eyebrow('CICLO', WHITE)
     + t(1040, M, 32, 400, WHITE, 'Abril Dobler · Felipe Berney · Zoe Dottori Greco',
         width=780, align='end')
     + t(M, 430, 148, 500, WHITE, 'PROTOTIPO\nDE BAJA\nFIDELIDAD', lh=0.98)
     + t(1320, 880, 32, 400, WHITE, 'ENTREGA N2\n06/10/2026', width=500, align='end', lh=1.35)
     + line(M, 1000, 600, 1000, WHITE, 3))
slide('01-portada', BLACK, b)

# ───────────────────────── 02 QUÉ CAMBIÓ ─────────────────────────
b = eyebrow('DESDE EL 25 DE AGOSTO') + title('QUÉ CAMBIÓ\nDESDE LA ENTREGA 1', y=170, size=104)
camb = [('La hipótesis', 'Pasó de «cruzar señales» a algo que se puede medir: en qué etapa está cada atributo, sin que nadie etiquete las etapas a mano.'),
        ('La usuaria', 'Dejó de ser «un diseñador» y es una forecaster independiente que asesora a tres clientes con tres plazos distintos.'),
        ('Los datos', 'De 3 datasets a 9 fuentes. 1,28 M de looks de pasarela, 30,6 M de compras y 22 años de búsquedas.'),
        ('El modelo', 'Ya corre. K-means sobre 18 atributos, cuatro grupos, validado contra capas que el modelo nunca vio.')]
for i, (k, v) in enumerate(camb):
    x = M + i * 430
    b += (rect(x, 500, 380, 3, BLACK)
          + t(x, 522, 24, 400, INK2, '0%d' % (i + 1), ls=8)
          + t(x, 572, 44, 500, BLACK, k, width=380, lh=1.1)
          + t(x, 650, 27, 400, INK2, v, width=380, lh=1.45))
slide('02-que-cambio', CREAM, b)

# ───────────────────────── 03 HIPÓTESIS ─────────────────────────
b = (eyebrow('HIPÓTESIS')
     + t(M, 230, 76, 500, BLACK,
         'Cruzando lo que la pasarela propone con lo que la gente busca y lo que el mercado masivo vende, se puede ubicar cada atributo de moda en una de cinco etapas de su ciclo de vida.',
         width=1720, lh=1.18)
     + t(M, 700, 38, 400, INK2, 'Y se puede hacer sin que nadie etiquete las etapas a mano: el modelo agrupa, nosotros leemos.', width=1300, lh=1.35))
et = ['EMERGENTE', 'EN ASCENSO', 'EN PICO', 'SATURADA', 'EN RETORNO']
for i, e in enumerate(et):
    x = M + i * 346
    b += rect(x, 880, 320, 3, BLACK) + t(x, 902, 24, 500, BLACK, e, ls=6)
slide('03-hipotesis', CREAM, b)

# ───────────────────────── 04 LA USUARIA ─────────────────────────
b = (eyebrow('PERFIL DE USUARIO') + title('LA USUARIA', y=165)
     + t(M, 330, 32, 400, INK2,
         'Una forecaster independiente que asesora a varias marcas a la vez. La misma lectura vale distinto para cada una: lo que para una marca de nicho es una oportunidad, para una premium con medio año de producción ya es tarde.\n\nPor eso toda recomendación de la app pasa por un selector de tipo de cliente.',
         width=720, lh=1.5))
cli = [('FAST FASHION', '6 semanas', 'Puede entrar incluso en el pico: produce más rápido de lo que cae la búsqueda.'),
       ('PREMIUM', '6 meses', 'Necesita el aviso en el ascenso. En el pico ya llega tarde.'),
       ('NICHO', '3 meses', 'Vive de lo emergente y de lo que vuelve, no del volumen.')]
for i, (n, p, d) in enumerate(cli):
    y = 300 + i * 215
    b += (rect(980, y, 840, 3, BLACK)
          + t(980, y + 26, 48, 500, BLACK, n, width=520, lh=1.1)
          + t(1360, y + 30, 44, 400, BLACK, p, width=460, align='end', lh=1.1)
          + t(980, y + 100, 27, 400, INK2, d, width=840, lh=1.45))
slide('04-usuaria', CREAM, b)

# ───────────────────────── 05 UNIDAD DE ANÁLISIS ─────────────────────────
b = (eyebrow('UNIDAD DE ANÁLISIS', GREY_D)
     + t(M, 250, 190, 500, WHITE, 'EL ATRIBUTO', lh=1.0)
     + t(M, 500, 40, 400, WHITE,
         'No la prenda, no la marca, no «la tendencia». Un atributo es un color, una estampa, un corte o un material: lo único que se puede contar en las cinco capas a la vez.',
         width=1100, lh=1.4))
ej = [('COLOR', 'rojo cereza'), ('ESTAMPA', 'lunares'), ('CORTE', 'jeans amplios'), ('MATERIAL', 'gamuza')]
for i, (k, v) in enumerate(ej):
    x = M + i * 430
    b += (rect(x, 820, 380, 3, GREY_D)
          + t(x, 842, 24, 400, GREY_D, k, ls=6)
          + t(x, 886, 36, 500, WHITE, v, width=380, lh=1.1))
b += t(1280, 500, 27, 400, GREY_D,
       'Por qué importa: si se mira «denim» agregado, los jeans amplios y los ajustados se cancelan entre sí y no se ve nada. Separados, uno está en pico y el otro saturado.',
       width=540, lh=1.5)
slide('05-unidad-de-analisis', BLACK, b)

# ───────────────────────── 06 EL SISTEMA ─────────────────────────
b = eyebrow('DE PUNTA A PUNTA') + title('EL SISTEMA', y=160, size=96)
bands = [
    ('A · DATOS', 320, ['Vogue Runway', 'Google Trends', 'Google Shopping', 'Reddit', 'Lyst Index',
                        'Launchmetrics', 'H&M', 'Amazon', 'Zara + Wish'], BLACK),
    ('B · PREPARACIÓN', 460, ['Limpieza y filtrado', 'IA-1  Etiquetado de imagen',
                              'IA-2  Enlace de registros', 'Matriz atributo × año × capa'], None),
    ('C · MODELO', 600, ['IA-3  K-means k=4', 'Nombrado por prototipo', 'Validación con capas no vistas'], None),
    ('D · EN VIVO', 740, ['IA-4  Ubicar una tendencia nueva', 'IA-5  Leer y recomendar (LLM)',
                          'IA-6  Consulta por imagen'], None),
    ('E · PANTALLAS', 880, ['Portada', 'Radar', 'Detalle', 'El ciclo', 'Recorridos', 'Marcas',
                            'Retornos', 'Consulta', 'Método'], BLACK),
]
for lbl, y, items, _ in bands:
    b += t(M, y - 42, 22, 500, INK2, lbl, ls=8)
    b += line(M, y - 10, 1820, y - 10, WIRE, 2)
    gap, x = 14, M
    n = len(items)
    cw = (1720 - gap * (n - 1)) / n
    for i, it in enumerate(items):
        ia = it.startswith('IA-')
        x = M + i * (cw + gap)
        b += rect(x, y, cw, 76, SALMON if ia else WIRE2, 4)
        b += t(x + 14, y + 16, 19, 600 if ia else 400, BLACK, it, width=cw - 28, lh=1.25)
    if y < 880:
        b += t(930, y + 86, 26, 400, INK2, '↓', width=60, align='middle')
b += t(1240, 160, 26, 400, INK2,
       'En salmón, los seis momentos en que interviene la IA. Tres corren una sola vez, en batch. Tres se disparan con el usuario.',
       width=580, lh=1.45)
slide('06-sistema', CREAM, b)

# ───────────────────────── 07 LAS NUEVE FUENTES ─────────────────────────
b = eyebrow('LOS DATOS') + title('NUEVE FUENTES', y=160, size=96)
fs = [('Vogue Runway', '1.281.633 imágenes', 'Qué propone la pasarela · 2000–2023'),
      ('Google Trends', '49 términos', 'Qué busca la gente · 2004–2025'),
      ('Google Shopping', '25 términos', 'Qué busca para comprar · 2008–2025'),
      ('Reddit', '4.404 menciones', 'De qué se habla · 2012–2025'),
      ('Lyst Index', '34 trimestres', 'Qué marca manda · Q1-18 a Q2-26'),
      ('Launchmetrics', 'Met Gala 2025', 'Qué amplifica la alfombra roja'),
      ('H&M', '30.570.975 compras', 'Qué se vende de verdad · 2018–2020'),
      ('Amazon', '1,1 M de reseñas', 'Qué se compró y comentó · 2012–2023'),
      ('Zara + Wish', '1.593 productos', 'Cómo está armado el catálogo hoy')]
for i, (n, v, d) in enumerate(fs):
    col, rw = i % 3, i // 3
    x, y = M + col * 580, 330 + rw * 230
    b += (rect(x, y, 540, 3, BLACK)
          + t(x, y + 24, 40, 500, BLACK, n, width=540, lh=1.1)
          + t(x, y + 84, 30, 500, BLACK, v, width=540, lh=1.2)
          + t(x, y + 128, 25, 400, INK2, d, width=540, lh=1.35))
slide('07-fuentes', CREAM, b)

# ───────────────────────── 08 LEYENDA / LA IA ─────────────────────────
b = (eyebrow('CÓMO LEER ESTA PRESENTACIÓN', SALMON)
     + t(M, 230, 96, 500, WHITE, 'TODO LO QUE TOCA\nLA MÁQUINA VA EN\nSALMÓN.', lh=1.05)
     + t(M, 600, 34, 400, WHITE,
         'Lo negro es medido. Lo salmón es calculado o interpretado por un modelo. Es la misma regla adentro de la app: lo que sale del modelo de lenguaje siempre aparece marcado.',
         width=820, lh=1.45))
pts = [('IA-1', 'Etiquetado de pasarela', 'batch'), ('IA-2', 'Enlace de registros', 'batch'),
       ('IA-3', 'K-means, k=4', 'batch'), ('IA-4', 'Ubicar una tendencia nueva', 'en vivo'),
       ('IA-5', 'Leer y recomendar', 'en vivo'), ('IA-6', 'Consulta por imagen', 'en vivo')]
for i, (c, n, w) in enumerate(pts):
    y = 250 + i * 118
    b += (rect(1020, y, 800, 2, '#2A2A2A')
          + t(1020, y + 24, 34, 600, SALMON, c)
          + t(1130, y + 26, 32, 400, WHITE, n, width=520, lh=1.2)
          + t(1560, y + 30, 24, 400, GREY_D if w == 'batch' else SALMON, w, width=260, align='end'))
slide('08-leyenda-ia', BLACK, b)

# ───────────────────────── 09 IA DE PREPARACIÓN ─────────────────────────
b = eyebrow('CORREN UNA SOLA VEZ, EN BATCH') + title('IA DE PREPARACIÓN', y=160, size=92)
cards = [('IA-1', 'Etiquetado de pasarela', 'Modelo de visión',
          'Entra  la foto de un desfile\nSale  los atributos de ese look\n\n1.281.633 imágenes etiquetadas. De ahí salen los 902.566 looks que usamos: sólo las fotos de colección, sin Bridal, entre 2000 y 2023.',
          'Límite declarado: el modelo etiqueta «denim» pero no distingue amplio de ajustado. La pasarela no puede validar los cortes.'),
         ('IA-2', 'Enlace de registros', 'Comparación de pares + clasificación',
          'Entra  cómo se llama el mismo atributo en 8 fuentes\nSale  pares clasificados en match, potencial y no-match\n\n21 atributos × 8 fuentes = 168 pares. 78 match, 20 potenciales, 70 no-match.',
          'Los 20 potenciales pasaron por revisión manual: 13 aceptados, 2 corregidos, 5 descartados. Está documentado quién decidió qué.')]
for i, (c, n, tec, d, lim) in enumerate(cards):
    x = M + i * 880
    b += (rect(x, 330, 840, 6, SALMON)
          + t(x, 360, 48, 600, SALMON_T, c)
          + t(x, 430, 54, 500, BLACK, n, width=840, lh=1.1)
          + t(x, 510, 27, 400, INK2, tec, width=840, lh=1.3)
          + t(x, 570, 28, 400, BLACK, d, width=840, lh=1.5)
          + rect(x, 830, 840, 2, WIRE)
          + t(x, 854, 25, 400, INK2, lim, width=840, lh=1.45))
slide('09-ia-preparacion', CREAM, b)

# ───────────────────────── 10 IA DEL MODELO ─────────────────────────
b = (eyebrow('EL CORAZÓN DEL PROTOTIPO')
     + t(M, 160, 48, 600, SALMON_T, 'IA-3')
     + title('K-MEANS\nNO SUPERVISADO', y=225, size=86, width=900)
     + t(M, 440, 30, 400, INK2,
         'Nadie le dice al modelo qué es un «pico». Le damos cuatro variables estandarizadas y agrupa los atributos que se mueven parecido. Recién después nosotros leemos qué etapa es cada grupo, comparándolo con cinco prototipos.',
         width=800, lh=1.5))
vv = ['Nivel en pasarela', 'Momento en pasarela', 'Nivel en búsqueda', 'Momento en búsqueda']
b += t(M, 660, 22, 500, INK2, 'LAS CUATRO VARIABLES', ls=8)
for i, v in enumerate(vv):
    b += rect(M, 700 + i * 58, 760, 46, WIRE2, 4) + t(M + 16, 710 + i * 58, 25, 400, BLACK, v)
grp = [('EN ASCENSO', '1 atributo', 'Y2K'),
       ('EN PICO', '8 atributos', 'Jeans amplios · Jeans medios · Buzo · Floral · Capa · Trench · Cargo · Blazer oversize'),
       ('SATURADA', '2 atributos', 'Jeans ajustados · Kimono'),
       ('EN RETORNO', '7 atributos', 'Lunares · Cuero · Animal print · Encaje · Cuadros · Piel · Zapatilla chunky')]
b += t(1000, 300, 22, 500, INK2, 'LOS CUATRO GRUPOS QUE ENCONTRÓ', ls=8)
for i, (n, c, items) in enumerate(grp):
    y = 345 + i * 158
    b += (rect(1000, y, 820, 3, BLACK)
          + t(1000, y + 22, 38, 500, BLACK, n, width=560, lh=1.1)
          + t(1400, y + 26, 30, 400, INK2, c, width=420, align='end')
          + t(1000, y + 76, 24, 400, INK2, items, width=820, lh=1.35))
b += t(M, 960, 25, 400, INK2,
       'k = 4 porque es el que mejor silhouette da (0,326) entre k = 2 y k = 5. 18 atributos que existen a la vez en la pasarela y en Google Trends.',
       width=800, lh=1.4)
slide('10-ia-modelo', CREAM, b)

# ───────────────────────── 11 IA EN VIVO ─────────────────────────
b = eyebrow('SE DISPARAN CON EL USUARIO') + title('IA EN VIVO', y=160, size=92)
liv = [('IA-4', 'Ubicar una tendencia nueva', 'Asignación al centroide más cercano',
        'La usuaria carga un atributo que no está en la base con sus cuatro métricas. Se estandariza con el mismo escalador y se asigna al grupo más cercano.',
        'El modelo no se reentrena: si lo hiciera, la tendencia nueva se volvería su propio grupo y cambiarían los nombres de todos los demás.'),
       ('IA-5', 'Leer y recomendar', 'LLM vía Groq API · prompt con método RACE',
        'Entra: los centros del grupo, la validación y el tipo de cliente con su plazo. Sale: una acción —Entrar, Esperar o Salir— y una frase que la justifica con un número de los datos.',
        'Nunca recibe una fila de la base. Sólo métricas ya calculadas.'),
       ('IA-6', 'Consulta por imagen', 'Clasificador de imagen',
        'La usuaria sube la foto de una prenda. El clasificador extrae sus atributos y la app los busca en el mapa del ciclo.',
        'Responde a la devolución de la Entrega 1: «ida y vuelta con imágenes de prendas».')]
for i, (c, n, tec, d, nota) in enumerate(liv):
    x = M + i * 580
    b += (rect(x, 320, 540, 6, SALMON)
          + t(x, 350, 44, 600, SALMON_T, c)
          + t(x, 414, 42, 500, BLACK, n, width=540, lh=1.12)
          + t(x, 500, 25, 400, INK2, tec, width=540, lh=1.3)
          + t(x, 560, 27, 400, BLACK, d, width=540, lh=1.5)
          + rect(x, 820, 540, 2, WIRE)
          + t(x, 844, 24, 400, INK2, nota, width=540, lh=1.45))
slide('11-ia-en-vivo', CREAM, b)

# ───────────────────────── 12 LA REGLA ─────────────────────────
b = (eyebrow('LA REGLA QUE ATRAVIESA TODO', SALMON)
     + t(M, 230, 104, 500, WHITE,
         'El modelo de lenguaje\nnunca ve una fila\nde datos.', lh=1.08))
steps = [('LOS DATOS', '30,6 M de compras\n1,28 M de looks', WHITE, False),
         ('MÉTRICAS CALCULADAS', 'nivel, momento,\ncrecimiento, distancia al pico', WHITE, False),
         ('EL MODELO DE LENGUAJE', 'lee sólo esos números\ny el tipo de cliente', SALMON, True),
         ('LA PANTALLA', 'una acción y una frase,\nmarcadas como interpretación', SALMON, True)]
for i, (n, d, col, ia) in enumerate(steps):
    x = M + i * 440
    b += (rect(x, 680, 400, 150, '#141414' if not ia else '#2A1D1B', 6)
          + rect(x, 680, 400, 5, col)
          + t(x + 22, 706, 21, 600, col, n, width=356, lh=1.2)
          + t(x + 22, 760, 24, 400, '#9A958E' if not ia else SALMON, d, width=356, lh=1.35))
    if i < 3:
        b += t(x + 400, 740, 30, 400, INK2, '→', width=40, align='middle')
b += t(M, 880, 27, 400, '#9A958E',
       'Lo que devuelve es opinión, no dato, y en la interfaz siempre aparece con esa marca. Es la diferencia entre una app que calcula y una que inventa.',
       width=1000, lh=1.45)
slide('12-la-regla', BLACK, b)

# ───────────────────────── 13 EL FLUJO ─────────────────────────
b = eyebrow('CÓMO SE RECORRE') + title('EL FLUJO DE LA APP', y=160, size=92)
b += rect(M, 340, 300, 110, BLACK, 4) + t(M + 20, 362, 30, 500, CREAM, 'PORTADA', width=260)
b += t(M + 20, 400, 21, 400, '#9A958E', 'lo primero que se ve', width=260)
b += t(410, 378, 28, 400, INK2, '→', width=40, align='middle')
# camino A
b += (rect(470, 300, 420, 96, WIRE2, 4)
      + t(488, 318, 24, 600, BLACK, 'A · EMPEZÁ POR UNA PRENDA', width=384)
      + t(488, 352, 21, 400, INK2, 'Denim · Pantalones · Abrigos · Tejidos · Remeras · Estampas · Materiales', width=384, lh=1.25))
b += (rect(470, 414, 420, 96, WIRE2, 4)
      + t(488, 432, 24, 600, BLACK, 'B · EL ÍNDICE', width=384)
      + t(488, 466, 21, 400, INK2, 'las siete secciones, en orden', width=384, lh=1.25))
b += t(905, 378, 28, 400, INK2, '→', width=40, align='middle')
scr = [('RADAR', 'qué se está moviendo'), ('EL CICLO', 'en qué etapa está cada una'),
       ('RECORRIDOS', 'de la pasarela a la calle'), ('MARCAS', 'quién manda'),
       ('RETORNOS', 'lo que vuelve'), ('CONSULTA', 'pegá una prenda'),
       ('MÉTODO', 'por qué podés creerle')]
for i, (n, d) in enumerate(scr):
    col, rw = i % 4, i // 4
    x, y = 960 + col * 220, 300 + rw * 112
    b += (rect(x, y, 200, 96, WIRE2, 4)
          + t(x + 14, y + 16, 22, 600, BLACK, n, width=172)
          + t(x + 14, y + 46, 18, 400, INK2, d, width=172, lh=1.25))
# acciones de IA
b += t(M, 620, 22, 500, INK2, 'LO QUE LA IA RESPONDE EN CADA PUNTO', ls=8)
act = [('Desde Detalle', 'IA-5', 'la recomendación según el tipo de cliente'),
       ('Desde El ciclo', 'IA-4', 'probar un atributo que no está en la base'),
       ('Desde Consulta', 'IA-6', 'subir una foto y recibir la etapa')]
for i, (d, c, w) in enumerate(act):
    x = M + i * 580
    b += (rect(x, 670, 540, 6, SALMON)
          + t(x, 696, 26, 400, INK2, d, width=540)
          + t(x, 736, 40, 600, SALMON_T, c)
          + t(x, 792, 26, 400, BLACK, w, width=540, lh=1.4))
b += t(M, 900, 26, 400, INK2,
       'La portada no es decorativa: es la primera decisión de diseño. Obliga a la usuaria a declarar qué quiere descubrir antes de ver un número, porque la app no tiene una respuesta única — tiene una por atributo.',
       width=1720, lh=1.45)
slide('13-flujo', CREAM, b)

# ───────────────────────── 14 y 15 WIREFRAMES ─────────────────────────
def wire(x, y, w, h, title_, blocks, caption, src):
    """Dibuja una pantalla esquemática."""
    s = rect(x, y, w, h, WHITE, 4, WIRE, 2)
    s += rect(x, y, w, 34, WIRE2)
    s += t(x + 12, y + 8, 16, 600, BLACK, title_, width=w - 24)
    for (bx, by, bw, bh, kind, lab) in blocks:
        ax, ay = x + bx, y + 34 + by
        if kind == 'box':
            s += rect(ax, ay, bw, bh, WIRE2, 3)
        elif kind == 'ia':
            s += rect(ax, ay, bw, bh, SALMON, 3)
        elif kind == 'dark':
            s += rect(ax, ay, bw, bh, BLACK, 3)
        elif kind == 'line':
            s += rect(ax, ay, bw, 3, WIRE)
        if lab:
            col = CREAM if kind == 'dark' else BLACK
            s += t(ax + 8, ay + 7, 13, 500, col, lab, width=max(10, bw - 16), lh=1.2)
    s += t(x, y + h + 14, 24, 500, BLACK, caption, width=w, lh=1.2)
    s += t(x, y + h + 46, 19, 400, INK2, src, width=w, lh=1.35)
    return s

b = eyebrow('PROTOTIPO DE BAJA FIDELIDAD · 1 DE 2') + title('LAS PANTALLAS', y=160, size=92)
WX, WY, WW, WH_ = M, 340, 400, 300
scr1 = [
  ('PORTADA', [(24,30,352,54,'dark','CICLO'), (24,100,168,16,'line',None), (208,100,168,16,'line',None),
               (24,128,168,26,'box','Denim'), (208,128,168,26,'box','01 Radar'),
               (24,162,168,26,'box','Estampas'), (208,162,168,26,'box','02 El ciclo'),
               (24,196,168,26,'box','Materiales'), (208,196,168,26,'box','03 Recorridos')],
   'Portada', 'Dos entradas: por prenda o por el índice. Nada de datos todavía.'),
  ('RADAR', [(24,24,352,18,'line',None), (24,56,110,70,'box','paleta'), (144,56,110,70,'box','paleta'),
             (264,56,110,70,'box','paleta'), (24,136,110,70,'box','paleta'), (144,136,110,70,'box','paleta'),
             (264,136,110,70,'box','paleta'), (24,218,352,10,'line',None)],
   'Radar', 'Una ficha por atributo, con su paleta medida y su posición en el ciclo. H&M + Zara.'),
  ('DETALLE', [(24,24,160,60,'box','paleta medida'), (196,24,180,60,'box','etapa'),
               (24,96,352,80,'box','curva por capa · 2004–2025'),
               (24,188,352,44,'ia','IA-5 · recomendación según cliente')],
   'Detalle del atributo', 'Vogue Runway + Google Trends + Reddit. Abajo, la lectura del modelo.'),
  ('EL CICLO', [(24,24,230,150,'box','scatter de los 4 grupos'), (264,24,112,34,'box','k = 4'),
                (264,66,112,34,'box','silhouette'), (264,108,112,66,'box','validación'),
                (24,186,352,46,'ia','IA-4 · probar una tendencia nueva')],
   'El ciclo · K-means', 'Las 18 filas del modelo, los centroides y la validación con Amazon y Shopping.'),
]
for i, (tt, bl, cap, src) in enumerate(scr1):
    b += wire(WX + i * 440, WY, WW, WH_, tt, bl, cap, src)
b += t(M, 800, 26, 400, INK2,
       'Son esquemas, no diseño final: lo que se decide acá es qué información entra en cada pantalla y en qué orden, no cómo se ve. En salmón, los bloques donde interviene la IA.',
       width=1720, lh=1.45)
slide('14-wireframes-1', CREAM, b)

b = eyebrow('PROTOTIPO DE BAJA FIDELIDAD · 2 DE 2') + title('LAS PANTALLAS', y=160, size=92)
scr2 = [
  ('RECORRIDOS', [(24,24,352,26,'box','chips agrupados por prenda'),
                  (24,62,352,110,'box','pasarela · búsqueda · Reddit'),
                  (24,184,230,48,'box','cuándo tocó techo cada capa'), (264,184,112,48,'box','retraso')],
   'Recorridos', 'La cadena completa de un atributo, cada curva llevada a su propio máximo.'),
  ('MARCAS', [(24,24,352,130,'box','34 trimestres del Lyst Index'),
              (24,166,168,66,'box','historias'), (202,166,174,66,'box','corte de Q1-26')],
   'Marcas', 'Lyst Q1-18 a Q2-26. Declara el corte metodológico de 2026.'),
  ('CONSULTA', [(24,24,352,80,'box','arrastrá una foto'),
                (24,116,352,44,'ia','IA-6 · atributos detectados'),
                (24,172,352,60,'box','en qué etapa está cada uno')],
   'Consulta por imagen', 'Responde a la devolución de la Entrega 1: ida y vuelta con imágenes.'),
  ('MÉTODO', [(24,24,352,18,'line',None), (24,52,352,60,'box','tabla de fuentes y estado'),
              (24,124,352,60,'box','límites declarados'), (24,196,352,36,'box','cómo se calculó cada número')],
   'Método', 'Todo número lleva su fuente. Es la pantalla que hace citable a la app.'),
]
for i, (tt, bl, cap, src) in enumerate(scr2):
    b += wire(M + i * 440, 340, 400, 300, tt, bl, cap, src)
b += t(M, 800, 26, 400, INK2,
       'Falta Retornos, que repite la plantilla de Recorridos con el eje puesto en los ciclos cerrados. Nueve pantallas en total, contando el detalle.',
       width=1720, lh=1.45)
slide('15-wireframes-2', CREAM, b)

# ───────────────────────── 16 CASO ─────────────────────────
b = (eyebrow('EL PROTOTIPO, PROBADO CON UNA PREGUNTA REAL')
     + t(M, 160, 86, 500, BLACK, '«¿Me subo al jean baggy\no ya llegué tarde?»', width=1500, lh=1.1))
pasos = [('01', 'Portada → Denim', 'La usuaria declara qué quiere descubrir.'),
         ('02', 'Recorridos', 'Los amplios pasan a los ajustados en 2021. En 2025 la búsqueda es 55 % amplios, 23 % ajustados, 22 % medios.'),
         ('03', 'El ciclo', 'El K-means pone «jeans amplios» en PICO y «ajustados» en SATURADA. El modelo no vio ninguna etiqueta.'),
         ('04', 'Validación', 'En las reseñas de Amazon, entre 2019 y 2022, los ajustados caen 39 % y los amplios suben 79 %.'),
         ('05', 'IA-5 · la respuesta', 'Cliente premium, 6 meses: ESPERAR. El pico ya pasó para ese plazo. La oportunidad está en el corte medio, el único que todavía no se movió.')]
for i, (n, tt, d) in enumerate(pasos):
    x = M + i * 346
    ia = i == 4
    b += (rect(x, 420, 320, 6, SALMON if ia else BLACK)
          + t(x, 446, 24, 400, SALMON_T if ia else INK2, n, ls=8)
          + t(x, 486, 32, 500, SALMON_T if ia else BLACK, tt, width=320, lh=1.15)
          + t(x, 556, 24, 400, INK2, d, width=320, lh=1.45))
b += t(M, 880, 28, 400, BLACK,
       'La app no dice «el baggy está de moda». Dice en qué etapa está, con qué dato lo sabe, y qué significa eso para el plazo de producción de quien pregunta.',
       width=1300, lh=1.45)
slide('16-caso', CREAM, b)

# ───────────────────────── 17 y 18 FUNDAMENTACIÓN ─────────────────────────
fund = [
 ('La paleta se abre cuando el atributo se masifica.',
  'En H&M, la correlación entre el logaritmo de artículos distintos y la cantidad de colores es 0,90. Los mom jeans pasan de 1 a 7,6 por mil mientras sus colores van de 5 a 15 (r = 0,96). El skinny se parte a la mitad y pierde colores.',
  'La ficha del Radar muestra la paleta medida como dato, no como adorno. Y el residuo entre colores observados y esperados correlaciona −0,55 con el crecimiento: una paleta adelantada es señal de saturación.'),
 ('Dentro de un mismo atributo hay ciclos opuestos.',
  'Los jeans ajustados eran el 73 % de la búsqueda de jeans en 2012. Los amplios los pasan en 2021. Si se mira «denim» agregado, las dos curvas se cancelan y no se ve nada.',
  'La app se entra por prenda y por corte. La unidad de análisis es el atributo, y la portada es un menú de departamentos en vez de un buscador de tendencias.'),
 ('Hay cinco etapas y el color ya está ocupado por la ropa.',
  'Codificar la etapa con color obligaría a competir con el color de la prenda, que es el dato que la usuaria vino a ver.',
  'La etapa se codifica como posición en una pista, no como color — la posición es el canal perceptual más preciso (Munzner). La interfaz es monocroma para que el único color de la pantalla sea el de las prendas.'),
 ('El retraso pasarela → búsqueda existe, pero no es constante.',
  'En los ciclos cerrados va de 0 a +2 años. En los jeans es de cuatro años o más.',
  'Recorridos muestra el intervalo medido atributo por atributo y no predice. El retraso se declara caso por caso, nunca como una constante global.'),
 ('La pasarela no distingue cortes.',
  'El modelo de visión etiqueta «denim» y nada más. No hay forma de validar amplio contra ajustado desde Vogue.',
  'Cada ficha declara qué capa puede y qué capa no puede responder. Ningún número aparece sin su fuente.'),
 ('Google Trends tiene deriva.',
  '33 de los 35 términos del mundo tocan su máximo histórico en el mismo mes, abril de 2026. Sin corregirlo, todo parece estar en su pico.',
  'Se detrenda por la media de los 35 términos y se excluye 2026 entero. Queda escrito en la pantalla de Método, no en una nota al pie.'),
 ('Una fuente externa coincide con el modelo donde el modelo se la juega.',
  'Lyst reporta +55 % en búsquedas de jeans anchos en 2024, +56 % en cargo en 2022 y +74 % en corset en 2021. Los tres caen en los grupos que el K-means llamó pico y ascenso.',
  'Hay una pantalla de validación con fuente y link para cada señal, porque una forecaster necesita poder citar lo que afirma delante de un cliente.'),
]
for part in (0, 1):
    sel = fund[0:4] if part == 0 else fund[4:7]
    b = (eyebrow('DEL DATO A LA DECISIÓN DE DISEÑO · %d DE 2' % (part + 1))
         + title('POR QUÉ LA APP\nES ASÍ', y=160, size=86, width=900))
    b += t(1100, 175, 26, 400, INK2,
           'Ninguna pantalla existe porque quedaba linda. Cada una responde a algo que encontramos en los datos.',
           width=720, lh=1.45)
    y0 = 400
    for i, (hall, ev, dec) in enumerate(sel):
        y = y0 + i * 160
        b += (rect(M, y, 1720, 2, WIRE)
              + t(M, y + 20, 30, 500, BLACK, hall, width=520, lh=1.2)
              + t(660, y + 24, 23, 400, INK2, ev, width=540, lh=1.4)
              + t(1250, y + 24, 23, 400, BLACK, dec, width=570, lh=1.4))
        if i == 0:
            b += (t(M, y - 34, 20, 500, INK2, 'HALLAZGO MEDIDO', ls=8)
                  + t(660, y - 34, 20, 500, INK2, 'LA EVIDENCIA', ls=8)
                  + t(1250, y - 34, 20, 500, BLACK, 'LA DECISIÓN DE DISEÑO', ls=8))
    slide('%d-fundamentacion-%d' % (17 + part, part + 1), CREAM, b)

# ───────────────────────── 19 LÍMITES ─────────────────────────
b = (eyebrow('LO QUE ESTA VERSIÓN NO PUEDE HACER', SALMON)
     + t(M, 170, 96, 500, WHITE, 'LÍMITES\nDECLARADOS', lh=1.05))
lim = [('No detectamos lo emergente', 'La pasarela llega hasta 2023. Para ver lo que recién aparece hace falta la temporada actual, y el corpus público no la tiene.'),
       ('No separamos menswear de womenswear', 'El corpus los mezcla. Separarlo exige volver a agregar desde el archivo original.'),
       ('No medimos calzado', 'Es donde Lyst ve las señales más fuertes de 2023 y 2024, y nosotros no tenemos ni un término.'),
       ('Pinterest y TikTok piden sesión', 'No hay serie histórica accesible sin una cuenta abierta en el navegador.'),
       ('Dos datasets son sintéticos', 'Zara 2018–22 y Mix de marcas tienen correlación casi nula entre variables. Sirven para mostrar el método, no para concluir.'),
       ('Instagram quedó afuera', 'No existe serie histórica de hashtags a ningún precio. Es un resultado negativo documentado, no un olvido.')]
for i, (n, d) in enumerate(lim):
    col, rw = i % 3, i // 3
    x, y = M + col * 580, 480 + rw * 260
    b += (rect(x, y, 540, 3, SALMON)
          + t(x, y + 22, 34, 500, WHITE, n, width=540, lh=1.15)
          + t(x, y + 110, 25, 400, '#9A958E', d, width=540, lh=1.45))
slide('19-limites', BLACK, b)

# ───────────────────────── 20 ENTREGA 3 ─────────────────────────
b = eyebrow('LO QUE SIGUE') + title('PARA LA ENTREGA 3', y=160, size=92)
nxt = [('Groq API en vivo', 'Hoy IA-5 corre con un prompt fijo. Falta conectarla para que la recomendación se calcule en el momento, con el cliente y el plazo que elija la usuaria.'),
       ('Pasarela y venta por género', 'Volver a agregar el corpus separando menswear de womenswear, que es la división con la que trabaja la industria.'),
       ('Calzado', 'Sumar los términos que hoy faltan y que son justamente donde las señales externas son más fuertes.'),
       ('La página de racional', 'Ya existe como pantalla de Método. Falta llevarla al nivel que pide la consigna: hipótesis, procesamiento y rol de la IA, en una sola lectura.')]
for i, (n, d) in enumerate(nxt):
    x = M + i * 430
    b += (rect(x, 380, 380, 3, BLACK)
          + t(x, 402, 24, 400, INK2, '0%d' % (i + 1), ls=8)
          + t(x, 446, 40, 500, BLACK, n, width=380, lh=1.15)
          + t(x, 560, 26, 400, INK2, d, width=380, lh=1.45))
b += (rect(M, 830, 1720, 3, BLACK)
      + t(M, 856, 30, 400, INK2, 'El prototipo funcional ya está online y se puede recorrer hoy. Lo que falta no es construirlo: es conectarle la IA en tiempo real y declarar bien lo que no sabe.', width=1300, lh=1.4))
slide('20-entrega-3', CREAM, b)

print('listo:', len(os.listdir(OUT)), 'archivos en', OUT)
for f in sorted(os.listdir(OUT)): print(' ', f)
