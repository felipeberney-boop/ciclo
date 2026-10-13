# Fuentes y descargas

Los datasets originales **no están en el repositorio**: superan el límite de GitHub, requieren cuenta
para descargarlos, o se transcribieron a mano desde una publicación. Acá va de dónde sale cada uno, la
fecha en que lo bajamos y su licencia.

> **Pendiente antes de la entrega final:** verificar en la ficha de cada dataset la licencia exacta y la
> forma de atribución que pide. Las marcadas *a verificar* todavía no las confirmamos.

---

## Pasarela

**Vogue Runway** — `traopia/vogue-runway` (HuggingFace)
- Link: https://huggingface.co/datasets/traopia/vogue-runway
- Descargado: 15/09/2026
- Archivo: `VogueRunway.parquet` · 99 MB de metadata, sin imágenes
- Contenido: 1.281.633 imágenes con diseñador, temporada, año, ciudad y tags
- Usado: 902.566 looks (filtro `section=Collection`, sin Bridal, 2000–2023)
- Licencia: *a verificar en la ficha del dataset.* Los tags no los puso un editor: los generó un modelo
  de visión genérico.
- **Después de 2023 no hay dato.** Revisado el 13/10/2026: el archivo se scrapeó de Vogue el 31/03/2023 y
  no se actualizó. No encontramos reemplazo público con looks etiquetados de 2024–2026; el informe anual de
  Tagwalk es pago. 2024–2026 está **proyectado**, no medido: `datasets/completado_2026/`.

## Búsqueda y compra

**Google Trends** — búsqueda web
- Link: https://trends.google.com
- Exportado: 22/09/2026 · 49 términos (35 mundo + 14 Argentina), 2004–2025
- Licencia: términos de servicio de Google. Uso académico con atribución; no es dato abierto.

**Google Trends** — propiedad Shopping
- Exportado: 22/09/2026 · 25 términos, 2008–2025
- Misma licencia.

## Redes

**Reddit vía Arctic Shift**
- Link: https://arctic-shift.photon-reddit.com
- Consultado: 22/09/2026
- Contenido: 4.404 posts de r/femalefashionadvice cuyo título nombra alguno de los 25 términos,
  2012–2025, divididos por los 178.519 posts del subreddit en esos años
- Licencia: datos públicos de Reddit vía API de archivo. Atribuir a Arctic Shift y a Reddit.
- Nota: Pushshift está discontinuado. Intentamos sumar r/malefashionadvice y r/streetwear pero el
  servidor corta las consultas grandes.
- **Completado a 2026:** consultado el 13/10/2026, del 01/01/2026 al 12/10/2026, 14.495 posts. Para
  empalmarlo se bajaron también 2022–2025. Sólo se suben los conteos por término y año, no los títulos.
  Está en `datasets/completado_2026/reddit_2026.csv`.

## Marcas y cultura

**Lyst Index** — ranking trimestral
- Link: https://www.lyst.com/the-lyst-index/
- Transcrito a mano: 15/09/2026 · 34 trimestres (Q1-18 a Q2-26), 55 marcas en 640 puestos
- Licencia: contenido editorial de Lyst. Se cita la fuente y el trimestre; no se redistribuye el informe.
- Nota: las URL son inconsistentes por trimestre. La que funciona para 2018–2024 es
  `lyst.com/data/the-lyst-index/q{Q}{YY}/`.

**Lyst** — informes anuales (señales de crecimiento)
- 19 señales con porcentaje y URL, cargadas el 23/09/2026
- Licencia: contenido editorial. Cada señal lleva su link en la app.

**Launchmetrics** — Met Gala 2025
- Impacto mediático (MIV) por marca y por celebridad, ventana de 48 h post-evento
- Consultado: 15/09/2026
- Licencia: informe público de Launchmetrics, citado con atribución.

## Venta masiva

**H&M Personalized Fashion Recommendations** (Kaggle)
- Link: https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations
- Descargado: 22/09/2026
- Contenido: 31.788.324 transacciones, 2018-09-20 a 2020-09-22
- Usado: 30.570.975 compras de adulto (sin Baby/Children, 34.711 artículos)
- Licencia: reglas de la competencia de Kaggle — uso académico y no comercial. Requiere cuenta.

**Amazon Reviews**
- Contenido: muestra de 1,1 M de reseñas de indumentaria, 2012 a abril 2023
- Descargado: 22/09/2026
- Licencia: uso académico, citando el trabajo original de los autores del dataset. *A verificar la cita
  exacta antes de la entrega final.*

## Catálogo

**Zara febrero 2024** (Kaggle)
- Contenido: 252 filas, 228 SKU únicos, con descripciones reales scrapeadas
- Descargado: 08/09/2026
- Licencia: *a verificar en la ficha del dataset.*

**Wish 2020** (Kaggle) — `computed_insight_success_of_active_sellers`
- Contenido: 1.573 productos, 1.341 únicos
- Descargado: 22/09/2026
- Licencia: *a verificar en la ficha del dataset.*
- Nota: `retail_price` es inusable — 47 % sin descuento y 25 % con más de 72 %. Es solo de verano.

## Datasets revisados y descartados

| Dataset | Por qué se descartó |
|---|---|
| Zara 2018–2022 (Kaggle) | Sintético: correlación máxima 0,099 entre variables numéricas |
| Mix de marcas 2025 | Sintético: 75,4 % comparte la misma fecha; correlación máxima 0,018 |
| Fashion Trend Dataset (Kaggle) | Es el mismo archivo que «Zara 2018–22» |
| Fashion Dataset, 15.702 vestidos | Etiquetado por estampa pero sin fecha: no sirve para series |
| Runways since 2011 | 6.655 desfiles y 132.118 imágenes sin etiquetas; queda para medir color |
| Marcas argentinas | Fuera del alcance del proyecto |
