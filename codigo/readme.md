# Código

Scripts de extracción, cálculo y render. Ninguno es parte del sitio: el sitio es sólo `app/index.html`.

| Archivo | Qué hace |
|---|---|
| `extraer_series_de_la_app.js` | Saca las constantes de datos del HTML de la app y las escribe como JSON |
| `calcular_geometria_de_graficos.js` | Convierte las series en coordenadas de píxeles para dibujar los gráficos |
| `generar_laminas_entrega_2.py` | Genera las 20 láminas de la presentación como SVG de 1920×1080 |
| `renderizar_laminas_a_png.js` | Pasa los SVG a PNG con Playwright |
| `capturar_pantallas_de_la_app.js` | Abre la app y guarda una captura de cada vista |

## Cómo correrlos

```bash
# Node
npm install playwright

node extraer_series_de_la_app.js        # necesita el HTML de la app al lado
node calcular_geometria_de_graficos.js  # necesita datos_app.json
node capturar_pantallas_de_la_app.js

# Python
pip install pillow
python3 generar_laminas_entrega_2.py
```

## Lo que no está acá

Los scripts de limpieza y agregación de los datasets originales (H&M, Vogue, Amazon) corrieron sobre
archivos que no están en el repositorio por tamaño. Las series que produjeron están en
`datasets_procesados/`, y el detalle de los filtros aplicados en `datasets/diccionario.md`.
