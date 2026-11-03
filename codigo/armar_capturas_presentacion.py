# CICLO · pega las pantallas de la app (capturar_presentacion.js) en las capturas de la presentación (03/11/2026).
# Uso, desde la raíz del repo, después de node codigo/capturar_presentacion.js:
#   python3 codigo/armar_capturas_presentacion.py
# Los pares Figma | App conservan el lado Figma y el rótulo; sólo se reemplaza el panel de la app.
import os, tempfile
from PIL import Image

CRUDO = os.path.join(tempfile.gettempdir(), 'ciclo_presentacion')
DEST = 'app/presentacion/capturas'

def crudo(n): return Image.open(os.path.join(CRUDO, n + '.png')).convert('RGB')

def panel(par, app, caja):
    """caja = (x, y, ancho, alto) del panel de la app dentro del par; la captura se escala al ancho y se corta arriba"""
    x, y, w, h = caja
    im = Image.open(os.path.join(DEST, par + '.webp')).convert('RGB')
    a = crudo(app); a = a.resize((w, round(a.height * w / a.width)), Image.LANCZOS).crop((0, 0, w, h))
    im.paste(a, (x, y)); return im

def guardar(im, n): im.save(os.path.join(DEST, n + '.webp'), 'WEBP', quality=86); print('·', n)

guardar(panel('figma_par_portada', 'app_entrada', (740, 35, 720, 450)), 'figma_par_portada')
guardar(panel('figma_par_radar', 'app_tendencias', (740, 35, 720, 450)), 'figma_par_radar')
guardar(panel('figma_par_detalle', 'app_ficha', (740, 35, 720, 450)), 'figma_par_detalle')
cel = panel('figma_par_celular', 'app_celular_tendencias', (423, 50, 393, 852))
cel.paste(crudo('app_celular_menu').crop((0, 0, 393, 852)), (846, 50)); guardar(cel, 'figma_par_celular')
guardar(crudo('app_tendencias'), 'tendencias')
guardar(crudo('app_ficha_procedencia'), 'ficha_procedencia')
