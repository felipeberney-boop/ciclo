# Código

Scripts de extracción, cálculo y render. Ninguno es parte del sitio: el sitio es sólo `app/index.html`.

| Archivo | Qué hace |
|---|---|
| `extraer_series_de_la_app.js` | Saca las constantes de datos del HTML de la app y las escribe como JSON |
| `calcular_geometria_de_graficos.js` | Convierte las series en coordenadas de píxeles para dibujar los gráficos |
| `generar_laminas_entrega_2.py` | Genera las 20 láminas de la presentación como SVG de 1920×1080 |
| `renderizar_laminas_a_png.js` | Pasa los SVG a PNG con Playwright |
| `capturar_pantallas_de_la_app.js` | Abre la app y guarda una captura de cada vista |
| `bajar_titulos_reddit.py` | Baja los títulos de r/femalefashionadvice de un año vía Arctic Shift |
| `contar_terminos_reddit.py` | Cuenta, por año, los posts cuyo título nombra cada término |
| `proyectar_pasarela.py` | Elige un método por backtest y proyecta la pasarela a 2024–2026 |
| `empalmar_reddit_2026.py` | Lleva Reddit 2026 a la escala de la serie y escribe `datasets/completado_2026/` |
| `verificar_pasarela.py` | Recalcula la pasarela desde el parquet original de Vogue y la compara con el repo |
| `tres_pruebas_panel_objetivo_y_adelanto.py` | Modelo global, objetivo comercial y el test de adelanto de la pasarela atributo por atributo |

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
