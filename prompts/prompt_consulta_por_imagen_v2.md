# IA-6 · Consulta por imagen · v2

**Fecha:** 13/10/2026
**Modelo:** CLIP ViT-B/32 (OpenAI), versión ONNX cuantizada `Xenova/clip-vit-base-patch32`, corre en el navegador
**Estado:** en uso · reemplaza a la v1, que mostraba un resultado fijo

## Qué entra

Una foto, un dibujo o una captura. No sale de la computadora de la usuaria: el modelo (89 MB) se baja una
vez y calcula en el navegador.

## Qué sale

1. **Atributos.** Clasificación zero-shot contra los 18 atributos del K-means. Cada atributo es el promedio
   de 6 frases en inglés (2 descripciones × 3 plantillas, en `app/clip/atributos.json`). Se muestran los
   tres más probables con su etapa según el K-means.
2. **Looks parecidos.** Los 8 más cercanos entre 14.000 looks de Vogue 2010–2023 (1.000 por año), con los
   embeddings CLIP que trae el dataset.
3. **Cuándo se vio en la pasarela.** Años de los 100 vecinos, contra el reparto al azar (7,1 por año).
4. **Resumen** armado con reglas a partir de 1–3. No es un LLM.

## Validación

- **Compatibilidad.** 25 fotos del índice, bajadas del CDN de Vogue y pasadas por el modelo del navegador,
  se encontraron a sí mismas en el primer puesto entre los 14.000.
- **Atributos.** 150.000 looks de Vogue fuera del índice, con la etiqueta de Vogue como respuesta correcta:

| Atributo | AUC | En el top 3 | Al azar |
|---|---|---|---|
| Jeans (grupo; Vogue no separa cortes) | 0,91 | 86 % | 12 % |
| Buzo | 0,92 | 76 % | 5 % |
| Cuero | 0,93 | 84 % | 12 % |
| Lunares | 0,96 | 92 % | 11 % |
| Floral | 0,74 | 67 % | 25 % |
| Animal print | 0,80 | 20 % | 4 % |
| Encaje | 0,89 | 84 % | 17 % |
| Kimono | 0,87 | 87 % | 18 % |
| Capa | 0,82 | 77 % | 30 % |
| Trench | 0,91 | 89 % | 26 % |

Cuadros, piel, zapatilla chunky, cargo, Y2K y blazer oversize no tienen etiqueta en Vogue: **sin validar**,
y la interfaz lo dice en cada fila.

## Límites declarados

- Por debajo de 0,35 de probabilidad la app dice «no determinado» y muestra los tres más cercanos sólo
  para orientar.
- Los jeans se validan como grupo: CLIP no fue evaluado para distinguir amplio, medio y ajustado.
- El índice termina en 2023, igual que la pasarela medida.
- Las fotos de los looks se muestran desde el CDN de Vogue; no se copian al repositorio.

## Cómo se reproduce

`codigo/armar_indice_clip.py` (índice) y `codigo/calcular_textos_clip.mjs` (textos).
