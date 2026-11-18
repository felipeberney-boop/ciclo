# La pasarela corregida con CLIP (18/11/2026)

Desde 2022 Vogue dejó de etiquetar los looks (2022: 76 % con etiquetas; 2023: 48 %; Fall 2023: ninguno), y la serie de
pasarela, que divide por todos los looks, caía por falta de etiquetas. Estos scripts la corrigen. Corren desde una
carpeta de trabajo con una subcarpeta `datos/` (los archivos grandes no se suben) y un entorno con torch, open_clip y duckdb.

1. `serie_tags.py` — reproduce `REC[].v` desde las etiquetas (VogueRunway.parquet, traopia) y mide la cobertura por año.
2. `clasificar_todo.py` — una regresión logística por atributo sobre el vector CLIP de cada look (VogueRunway_image.npy),
   entrenada con las etiquetas de 2010–2021; estima la proporción de cada año sobre todos los looks y la valida contra
   las etiquetas. Aplica lo mismo a una muestra del dataset 2022–2025 (tonyassi/vogue933k-embedding: sólo links; el
   vector se calcula con `embed.py`, CLIP ViT-B/32-quickgelu, pesos openai, coseno 0,988 contra el del dataset).
3. `armar_serie.py` — la serie: etiquetas hasta 2021, CLIP 2022–2023; 2024–2025 sólo si el intervalo de 90 % es
   angosto (por ahora, no: esperan la muestra grande).
4. `km_nuevos.py`, `kmeans_comparar.js`, `km_final.js` — nivel y momento de pasarela para el K-means, con las mismas
   ventanas de antes, y el `KM` nuevo calculado con el código de la app.
5. `inyectar.py` — pasa la serie y el `KM` a `app/index.html` y a la exportación.
6. `prueba_reddit_modelo_corregido.py` — la prueba de Reddit con las etapas nuevas (no preregistrada; la original sigue
   en `codigo/prueba_reddit.py`).
Resultados en `datasets_procesados/pasarela_clip/`.
