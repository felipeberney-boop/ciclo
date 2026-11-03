# CICLO · pasa la captura de la app (capturar_presentacion.js) a la presentación (03/11/2026).
# Uso, desde la raíz del repo, después de node codigo/capturar_presentacion.js:
#   python3 codigo/armar_capturas_presentacion.py
import os, tempfile
from PIL import Image

CRUDO = os.path.join(tempfile.gettempdir(), 'ciclo_presentacion')
DEST = 'app/presentacion/capturas'

Image.open(os.path.join(CRUDO, 'app_tendencias.png')).convert('RGB').save(os.path.join(DEST, 'tendencias.webp'), 'WEBP', quality=86)
print('· tendencias')
