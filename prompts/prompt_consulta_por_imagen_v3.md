# IA-6 · Consulta por imagen · v3

**Fecha:** 20/10/2026
**Modelo:** el mismo de v2, CLIP ViT-B/32 (`Xenova/clip-vit-base-patch32`), en el navegador
**Estado:** en uso · reemplaza a la v2

## Qué cambió desde v2

Un solo cambio: **la clasificación zero-shot es contra 17 atributos, no 18.** Sale «Zapatilla chunky»,
porque CICLO deja el calzado afuera por decisión (la app trabaja con ropa) y el K-means también pasó a 17.
Se sacó de `codigo/calcular_textos_clip.mjs` y de `app/clip/atributos.json`; los otros 17 embeddings son
los mismos, byte a byte.

Todo lo demás —plantillas, frases, índice de 14.000 looks, años de los vecinos, umbral de 0,35, resumen
por reglas— sigue igual que en `prompt_consulta_por_imagen_v2.md`.

## Validación

La tabla de v2 se midió con 18 clases. Con una menos, la probabilidad de cada una se reparte entre 17:
el top 3 de los atributos validados sólo puede quedar igual o mejorar. No se volvió a medir.

Cuadros, piel, cargo, Y2K y blazer oversize siguen **sin validar**: Vogue no los etiqueta.
