# IA-7 · Diseñar: referencias y colores · v1

**Fecha:** 13/10/2026
**Modelo:** CLIP ViT-B/32 (OpenAI), en batch, sobre los embeddings de Vogue Runway que trae el dataset
**Estado:** en uso

## Para qué

El recorrido «Diseñar» (prenda → corte → color → estampa) necesita, en cada paso, una referencia visual
real y, en el paso de color, qué colores ganan presencia en la pasarela. Ninguna fuente trae eso.

## Qué hace

- **Referencias.** Para cada corte, prenda y estampa del catálogo (`codigo/diseno_catalogo.json`), los looks
  de Vogue 2018–2023 más parecidos al texto del ítem. Si Vogue tiene etiqueta (Trench Coat, Leather Jacket,
  Polka Dot, Denim…), se busca sólo entre los looks con esa etiqueta. En los cortes de jean, que Vogue no
  distingue, se elige lo que se parece **más a ese corte que a los otros**. Mujer y hombre se separan con
  CLIP («a photo of a woman / man wearing clothes»). Un look por desfile.
- **Colores.** Para cada look de la prenda, CLIP elige el color más parecido de una lista fija («a runway
  photo of a black trench coat»…). Se compara qué parte de los looks tenía cada color en 2018–2019 y en
  2022–2023. En prendas sin etiqueta de Vogue se toman los 150 looks más parecidos de cada año.

Los textos exactos están en `codigo/diseno_catalogo.json` y `codigo/calcular_textos_diseno.mjs`.

## Límites declarados

- Las referencias **pueden fallar**: se revisaron a ojo y los cortes de jean son lo más débil (en bootcut
  aparecen camperas de jean). La interfaz dice que las eligió CLIP.
- El color es **lectura de un modelo sobre la pasarela**, no venta, y termina en 2023. No se validó contra
  etiquetas de color, porque Vogue no las tiene.
- En jeans el color se mide para todos los jeans juntos: la pasarela no distingue el corte.
- La separación mujer / hombre es de CLIP, no de Vogue, y la pasarela mezcla menswear y womenswear.

## Cómo se reproduce

`node codigo/calcular_textos_diseno.mjs textos.json` y después
`python3 codigo/armar_diseno.py VogueRunway.parquet VogueRunway_image.npy textos.json` → `app/diseno/diseno.json`.
