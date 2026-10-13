# Verificación contra los datos crudos

Hecha el 13/10/2026. Para cada fuente: si se pudo volver al dato original, cómo se comparó y qué dio.
Ningún archivo crudo se subió al repositorio.

## Resumen

| Fuente | ¿Se pudo verificar? | Resultado | Llega hasta |
|---|---|---|---|
| Vogue Runway (pasarela) | Sí, archivo original completo | 8 de 11 series exactas; 2 cercanas; 1 no reproducible | 2023 medido · 2024–26 proyectado |
| Reddit (redes) | Sí, 2022–2026 completo | Reproduce la serie con 2,4 % de error mediano | octubre 2026 |
| Lyst Index (marcas) | Sí, contra informes publicados | Todo lo contrastado coincide | Q2-26 (Q3-26 no salió) |
| Google Trends (búsqueda) | No | Sin API pública: la librería pytrends se archivó en abril de 2025 | 2025 (2026 excluido a propósito) |
| H&M · Amazon · Zara · Wish | No | Requieren cuenta de Kaggle o pesan decenas de GB | 2020 · 2023 · 2024 · 2020 |

---

## Vogue Runway

**Archivo.** `VogueRunway.parquet` bajado de nuevo de HuggingFace (99.124.491 bytes, 1.281.633 imágenes).

**El filtro.** Sección `Collection`, años 2000–2023, sin Bridal (por diseñador o URL): **902.966 looks**. El
repo declara 902.566: 400 de diferencia (0,04 %), seguramente por cómo se detectó Bridal. No cambia ninguna
curva.

**Las curvas.** Para cada atributo recalculamos qué parte de los looks de cada año lleva la etiqueta,
llevada al máximo de 2010–2023, y la comparamos año por año con `REC[].v`:

| Atributo | Etiquetas de Vogue | Error medio (sobre 100) | Correlación | Pico crudo / repo |
|---|---|---|---|---|
| Jeans (los 3 cortes) | Denim + Jeans | 0,04 | 1,000 | 2021 / 2021 |
| Buzo | Sweatshirt | 0,03 | 1,000 | 2021 / 2021 |
| Cuero | Leather Jacket | 0,04 | 1,000 | 2018 / 2018 |
| Lunares | Polka Dot | 0,04 | 1,000 | 2015 / 2015 |
| Floral | Flower + Floral Design | 0,16 | 1,000 | 2018 / 2018 |
| Kimono | Kimono | 0,02 | 1,000 | 2021 / 2021 |
| Capa | Cape + Cloak | 0,02 | 1,000 | 2021 / 2021 |
| Trench | Trench Coat | 0,04 | 1,000 | 2021 / 2021 |
| Encaje | Lace (exacto, no «Necklace») | 1,52 | 0,999 | 2016 / 2016 |
| Animal print | Zebra + Cow (la más cercana) | 2,75 | 0,99 | 2019 / 2019 |
| **Cargo (militar)** | **ninguna combinación** | **13,5** | **0,81** | 2021 / 2021 |

**Lo que hay que revisar.**
- **Cargo.** Ninguna etiqueta ni combinación de etiquetas reproduce la serie de «militar» (probamos
  Military, Military Uniform, Camouflage, Army y todas las etiquetas con 100 looks o más). El año de pico
  coincide, pero la forma no. El script que la generó no está en el repo: **hay que documentar qué
  etiquetas se usaron**, o rehacer la serie con una lista declarada.
- **Animal print.** La ficha dice «Vetements, 82 de 117 looks» en 2019. En el crudo, «Zebra» da 89 looks en
  2019, 81 de Vetements. La lectura se sostiene (un solo desfile explica el pico), pero los números exactos
  no salen: falta la lista de etiquetas.
- **«Zebra Crossing»** (cruce peatonal) es una etiqueta del modelo de visión que confunde rayas. Si se
  buscan animales por subcadena entra sola y rompe la serie. Hay que excluirla a mano.
- **2024.** El archivo trae 35 looks con año 2024. Son demasiado pocos para medir ese año.

## Reddit

Bajamos los 80.074 títulos de r/femalefashionadvice de 2022 a octubre de 2026. Los totales por año
coinciden con el conteo oficial de Arctic Shift: 14.097 contra 14.102 en 2023, 17.947 contra 17.950 en 2024,
14.495 contra 14.495 en 2026. Con la media móvil centrada de 3 años, la serie del repo se reproduce con
**2,4 % de error mediano** en 26 términos (detalle en `completado_2026/readme.md`).

No re-verificamos 2012–2021: son unos 113.000 títulos más, y el tramo 2022–2025 ya confirma el método.

## Lyst Index

lyst.com bloquea la lectura automática, así que contrastamos con la prensa que publica cada ranking:

| Trimestre | Publicado | En el repo |
|---|---|---|
| Q2-26 | Chanel, Miu Miu, Dior, Saint Laurent, Gucci, Prada (1–6) | igual |
| Q1-26 | Chanel 1º; Gucci entra al top 5 por primera vez desde Q4-22 | Chanel 1º, Gucci 5º |
| Q3-25 | Saint Laurent 1º, Miu Miu 2º, COS 3º, The Row 4º, Prada 6º, Stone Island 19º; Burberry sube 4 puestos | igual; Burberry 17º → 13º |

Fuentes: [Milano Finanza](https://www.milanofinanza.it/fashion/lyst-index-2026-chanel-si-riconferma-l-hottest-brand-del-secondo-trimestre-202608031246419206),
[Complex](https://www.complex.com/style/a/tracewilliamcowen/chanel-hottest-brand-lyst-index),
[Jing Daily](https://jingdaily.com/intels/2025-11/06/saint-laurent-tops-lyst-index-in-q3-2025),
[Journal du Luxe](https://www.journalduluxe.fr/fr/mode/marques-tendance-2025-maisons-ysl-miumiu-cos-lyst-classement).

## Lo que no se pudo verificar

- **Google Trends.** No hay API pública y la librería que se usaba (pytrends) está archivada. Para
  verificar hay que volver a exportar a mano desde trends.google.com los 49 términos. Ojo: Google reescala
  cada exportación, así que los valores van a diferir en nivel. Lo que hay que comparar es la forma y el año
  de pico.
- **H&M, Wish, Zara** piden cuenta de Kaggle. **Amazon Reviews 2023** pesa decenas de GB en la categoría de
  ropa. En el repo sólo hay métricas resumidas de estas fuentes (`JE.hm`, `KM.amz_19_22`), no las series.
  Para verificarlas hace falta subir, aunque sea, los conteos agregados que salieron de cada una.

## ¿Está todo al día?

Sí, hasta donde existe dato: Reddit llega a octubre de 2026 y Lyst al último trimestre publicado. Pasarela,
H&M y Amazon no tienen ediciones públicas más nuevas: la pasarela está proyectada (y declarada así), y H&M
y Amazon quedan donde están. Google Trends 2026 existe, pero sigue excluido por el salto de medición de
abril.
