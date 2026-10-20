# IA-5 · Lectura y recomendación · v2

**Fecha:** 20/10/2026
**Modelo:** Groq, `llama-3.3-70b-versatile` (se cambia con la variable `GROQ_MODEL` en Netlify)
**Método de prompting:** RACE — Role, Action, Context, Expectation, igual que v1
**Estado:** en uso, en vivo. Corre en `netlify/functions/lectura.mjs`, en Recorridos, con el botón
«Pedir lectura en vivo». Reemplaza a v1, que corría con prompt fijo.

## Qué cambió desde v1

- **Un atributo, no un grupo.** v1 leía los centros de cada grupo del K-means; v2 lee las métricas del
  atributo que estás mirando en Recorridos, con su etapa como un dato más.
- **El prompt se arma en el servidor.** El navegador manda números y claves de una lista cerrada
  (cliente, vínculo, etapa); la función valida cada uno y arma el texto. Nadie puede mandarle texto
  libre al modelo desde la página.
- **Sin el pico de búsqueda en 2025.** Se usa el pico de volumen hasta 2024, el mismo que muestra la app
  (2025 tiene el salto de medición de Google). Si el máximo es 2024, se dice «sigue subiendo».
- **Por tu cuenta, «Explorar» en vez de «Esperar».** Igual que la recomendación fija de la app.
- **Salida en JSON** (`accion`, `frase`), validada: si la acción no es una de las pedidas o falta la
  frase, la app muestra un error y no la respuesta.

## Qué entra

Sólo métricas ya calculadas. Nunca una fila de la base.

- Etapa según el K-means (k=4)
- Pasarela: nivel y momento (0–1, las mismas variables del K-means), año de pico
- Búsqueda: nivel y momento, pico de volumen hasta 2024
- Peso en la búsqueda frente a otras de moda, 2023→2025
- Validación: cambio en Google Shopping 2022→2025 y en reseñas de Amazon 2019→2022
- Tipo de cliente, plazo de producción, año hasta el que decide, y si trabaja para una marca o por su cuenta

## El prompt

Sistema:

```
Sos analista de tendencias de CICLO. Leés métricas ya calculadas sobre un atributo de moda
(un color, una estampa, un corte o un material) y decís qué conviene hacer con él.
Reglas:
- Usá sólo los datos que te paso. No inventes cifras, marcas, temporadas ni fuentes.
- Escribí en castellano rioplatense, sin jerga, para diseñadores. Tono directo.
- La frase cita al menos un número de los datos, tal como aparece.
- Respondé sólo con JSON: {"accion": "...", "frase": "..."}.
```

Usuario (ejemplo armado por la función, Jeans baggy, high fashion, para una marca):

```
Cliente: Trabaja para una marca high fashion (prêt-à-porter de lujo). Plazo de producción: 6 meses.
Decide para colecciones hasta 2028.

Atributo: Jeans baggy
Etapa según el K-means: Pico
Pasarela (Vogue Runway, hasta 2023): nivel 0,61 sobre 1, momento -0,07, pico en 2021
Búsqueda (Google Trends mundo, hasta 2024): nivel 0,95 sobre 1, momento +0,21, sigue subiendo (máximo en 2024, el último año medido)
Peso en la búsqueda frente a otras de moda, 2023→2025: +13 puntos
Validación: Google Shopping 2022→2025 +95 %, reseñas de Amazon 2019→2022 +79 %

Objetivo: una acción (Entrar, Esperar o Salir) y una sola frase, de menos de 40 palabras, que la
justifique con un número de arriba.
```

Temperatura 0,3 y como máximo 200 tokens de salida.

## Qué sale

Una acción y una frase, que la app muestra en salmón, debajo de la recomendación fija y con la etiqueta
«interpretación · Groq en vivo», el modelo y la versión del prompt. La recomendación fija no se reemplaza:
las dos quedan a la vista para compararlas.

## Por qué está así

- **Lo de v1 sigue valiendo:** el rol fija el registro, «no inventes» es la restricción que importa y
  pedir un número ancla la respuesta.
- **Botón, no automático.** Cada llamada cuesta y tarda; la lectura se pide cuando interesa.
- **Límite conocido:** el momento de búsqueda del K-means todavía usa 2024–25 (pendiente de recalcular,
  declarado en Método). El modelo lo recibe como viene.
