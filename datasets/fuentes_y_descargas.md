# Fuentes y descargas

Los datasets originales **no están en el repositorio**: superan el límite de GitHub, requieren cuenta
para descargarlos, o se transcribieron a mano desde una publicación. Acá va de dónde sale cada uno, la
fecha en que lo bajamos y su licencia.

> **Verificación de licencias, 13/10/2026.** Fuimos a la ficha de cada fuente a buscar la licencia.
> El resultado es incómodo y conviene decirlo de entrada: **tres de las cuatro que teníamos pendientes
> no declaran ninguna licencia.** No significa que sean libres — significa lo contrario: nadie otorgó
> permiso explícito. Lo anotamos como «sin licencia declarada» en vez de inventar una o dejar
> «a verificar» para siempre.
>
> No somos abogados. Lo que sigue es lo que dice cada ficha, no una opinión legal.

---

## Pasarela

**Vogue Runway** — `traopia/vogue-runway` (HuggingFace)
- Link: https://huggingface.co/datasets/traopia/vogue-runway
- Descargado: 15/09/2026
- Archivo: `VogueRunway.parquet` · 99 MB de metadata, sin imágenes
- Archivo: `VogueRunway_image.npy` · 1,3 GB, embeddings CLIP de cada imagen (float16, 1.281.633 × 512, mismo
  orden que las filas del parquet). Lo usan `codigo/armar_diseno.py` y `codigo/armar_indice_clip.py`.
- **Los dos archivos crudos no están en este repo:** pesan más que el límite de GitHub (100 MB por archivo) y
  la fuente no tiene licencia para redistribuirlos. Se bajan del link de arriba. Lo que sí está en el repo es
  todo lo calculado a partir de ellos: `datasets_procesados/`, `app/clip/` y `app/diseno/diseno.json`.
- Contenido: 1.281.633 imágenes con diseñador, temporada, año, ciudad y tags
- Usado: 902.566 looks (filtro `section=Collection`, sin Bridal, 2000–2023)
- Licencia: **sin licencia declarada.** La ficha del dataset no tiene campo de licencia ni condiciones
  de uso. Dice que fue «scraped from Vogue on 2023-03-31» e importado del Internet Archive, y las URL
  de imagen apuntan a los servidores de Condé Nast. Los embeddings se hicieron con clip-retrieval
  (ViT-B/32).
- **Qué implica.** El contenido de origen es editorial de Vogue, no abierto. Lo usamos sólo para
  análisis académico, no redistribuimos el dataset ni las imágenes, y citamos la fuente. Si la cátedra
  necesita una licencia formal, esta fuente no la tiene.
- Los tags no los puso un editor: los generó un modelo de visión genérico.
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
- Link: https://amazon-reviews-2023.github.io
- Contenido: muestra de 1,1 M de reseñas de indumentaria, 2012 a abril 2023
- Descargado: 22/09/2026
- Licencia: **sin licencia declarada.** La página no fija términos de uso; su única condición es citar
  el trabajo original.
- **Cita exigida** (verificada el 13/10/2026):
  > Hou, Y., Li, J., He, Z., Yan, A., Chen, X., & McAuley, J. (2024). *Bridging Language and Items for
  > Retrieval and Recommendation.* arXiv:2403.03952.
- Nota: la versión 2023 cubre mayo 1996 a septiembre 2023. La categoría Clothing, Shoes and Jewelry
  tiene 66 M de reseñas sobre 7,2 M de artículos; nosotros usamos una muestra. La versión vieja (2018)
  pide otra cita —Ni, Li & McAuley, EMNLP 2019— y los propios autores recomiendan no usarla salvo para
  reproducir resultados anteriores.

## Catálogo

**Zara febrero 2024** (Kaggle)
- Contenido: 252 filas, 228 SKU únicos. Un solo scrape, el **2024-02-19**. Precios en USD.
- Descargado: 08/09/2026
- Licencia: **sin confirmar — falta la URL exacta del dataset.** Quien lo bajó tiene que pegar acá el
  link de Kaggle y repetir la verificación.
- **Mitad real, mitad sintético** (verificado el 13/10/2026). Hay que separar las columnas:
  - **Reales y usables:** `url`, `sku`, `name`, `description`, `price`, `scraped_at`, `terms`,
    `section`. Las descripciones son copy auténtico de Zara. Es la parte que usamos para la minería
    de texto de proporciones.
  - **Sintéticas, no usar:** `Sales Volume`, `Promotion`, `Seasonal`, `Product Position`.
    `Sales Volume` tiene correlación −0,07 con el precio; la media con promoción es 1.827 y sin
    promoción 1.821, una diferencia de **6 unidades** sobre 1.824; y su desvío observado (696) es
    casi idéntico al de una uniforme sobre su rango (710), con los diez deciles igual de poblados.
    Son columnas generadas al azar, no ventas.
- **Es 86 % menswear:** 218 filas MAN contra 34 WOMAN. El resto del corpus del proyecto
  —Vogue, r/femalefashionadvice, los atributos tipo corset o encaje— se inclina a womenswear. Es el
  desbalance opuesto al que suponíamos.
- **Trae calzado:** 31 productos con `terms = shoes`, todos de hombre. Es lo único de calzado que
  tenemos medido, y el calzado era el agujero declarado contra Lyst.

**Wish 2020** (Kaggle) — `computed_insight_success_of_active_sellers`
- Link: https://www.kaggle.com/datasets/jmmvutu/summer-products-and-sales-in-ecommerce-wish
- Contenido: 1.573 productos, 1.341 únicos
- Descargado: 22/09/2026
- Licencia: **sin licencia declarada.** La ficha no tiene campo de licencia, no nombra autor más allá
  del usuario de Kaggle (jmmvutu) y no dice de dónde salieron los datos ni cómo pueden usarse.
- **Qué implica.** Sin procedencia declarada no podemos afirmar que sea redistribuible. Lo usamos
  sólo como demostración de método —ya estaba descartado para conclusiones por el problema de
  `retail_price`— y citamos la ficha de Kaggle.
- Nota: `retail_price` es inusable — 47 % sin descuento y 25 % con más de 72 %. Es solo de verano.

## Ventas reales

**VISUELLE** — Nunalie, vía HumaticsLAB
- Link: https://github.com/HumaticsLAB/GTM-Transformer · paper arXiv:2109.09824
- Descargado: 13/10/2026, llenando el formulario que pide el repositorio
- Contenido: 5.577 productos con 12 semanas de ventas reales cada uno (SS17 a AW19) y 219 semanas de
  Google Trends para 96 términos, ya alineadas. El paquete completo pesa 2,3 GB porque incluye las
  fotos de cada producto; nosotros usamos sólo tres CSV que suman 2 MB.
- Licencia: **sin licencia declarada.** El repositorio es MIT, pero eso cubre el código. Uso
  académico, sin redistribuir, citando el paper.
- Para qué lo usamos: es la única fuente del proyecto con **ventas reales**. Con ella probamos si la
  búsqueda predice la venta. El resultado está en `decisiones.md`: a nivel producto no predice nada
  (r=+0,036, y fuera de muestra 6,5 % peor que el promedio de la categoría); a nivel categoría ×
  temporada el nivel de búsqueda da r=+0,19, apenas por encima del umbral.

## Datasets revisados y descartados

| Dataset | Por qué se descartó |
|---|---|
| Zara 2018–2022 (Kaggle) | Sintético: correlación máxima 0,099 entre variables numéricas |
| Mix de marcas 2025 | Sintético: 75,4 % comparte la misma fecha; correlación máxima 0,018 |
| Fashion Trend Dataset (Kaggle) | Es el mismo archivo que «Zara 2018–22» |
| Fashion Dataset, 15.702 vestidos | Etiquetado por estampa pero sin fecha: no sirve para series |
| Runways since 2011 | 6.655 desfiles y 132.118 imágenes sin etiquetas; queda para medir color |
| Marcas argentinas | Fuera del alcance del proyecto |

## Google Trends · 36 términos nuevos (20/10/2026)

Exportados a mano desde Google Trends, mundial, «2004 – presente», mensual, todas las categorías, el 20/10/2026.
Nueve comparaciones de trench coat (ancla) + 4 términos; los links y la hoja de la taxonomía de cada término están
en `datasets/plan_exportacion_trends.csv`, los CSV tal como se bajaron en `datasets/trends_lotes/`. Se pegan con
`codigo/pegar_lotes_trends.py`: promedio anual 2004–2025, escala del ancla (el trench de cada lote correlaciona 1,00
con el ya medido) y cada serie a su propio máximo. Entraron 32; quedaron afuera cable knit (8 años útiles), tweed
(plana), capri pants (0) y bermuda shorts (7), que siguen con dato prestado. Uso bajo los términos de Google, con
atribución y sin redistribuir el export.

