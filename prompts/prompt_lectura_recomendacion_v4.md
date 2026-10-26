# IA-5 · Lectura y recomendación · v4

**Fecha:** 25/10/2026
**Modelo:** Groq, `openai/gpt-oss-120b`, con `reasoning_effort: low`, sin devolver el razonamiento, máximo 500
tokens de salida, temperatura 0,3, respuesta en JSON.
**Estado:** en uso, en vivo, en `app/index.html` (`LV_SISTEMA`, `lvPrompt()`, `lvPedir()`). Reemplaza a v3.

## Qué cambió desde v3

- **Dónde corre.** v3 vivía en una función de Netlify con la clave del proyecto. Netlify se quedó sin créditos y
  en GitHub Pages el botón fallaba (POST → 405, «No se pudo leer.»). Ahora el navegador llama a Groq con la clave
  que pega cada usuario, la misma de «Preguntar» (`groq_key` en este navegador). La razón para tener servidor era
  no exponer una clave del proyecto; con la clave de cada uno, esa razón desaparece.
- **Una etiqueta corregida.** v3 decía «Peso en la búsqueda frente a otras de moda, 2023→2025», pero `terreno()`
  mide 2022→2024 desde el corte en 2024. v4 dice **2022→2024**. Es el único cambio de texto.
- **Lo que entra sigue siendo una lista cerrada.** El prompt se arma con texto fijo y números que calcula la app
  (`vivoDatos()`); quien usa la app no escribe nada que llegue al modelo. La salida se valida igual: la acción
  tiene que ser una de las tres permitidas y la frase no puede venir vacía.

## Sistema

```
Sos analista de tendencias de CICLO. Leés métricas ya calculadas sobre un atributo de moda (un color, una estampa, un corte o un material) y decís qué conviene hacer con él.
Reglas:
- Usá sólo los datos que te paso. No inventes cifras, marcas, temporadas ni fuentes.
- Escribí en castellano rioplatense, sin jerga, para diseñadores. Tono directo.
- La frase cita al menos un número de los datos, tal como aparece.
- Respondé sólo con JSON: {"accion": "...", "frase": "..."}.
```

## Usuario (ejemplo real: Jeans baggy, high fashion, para una marca)

```
Cliente: Trabaja para una marca high fashion (prêt-à-porter de lujo). Plazo de producción: 6 meses. Decide para colecciones hasta 2028.

Atributo: Jeans baggy
Etapa según el K-means: Pico
Pasarela (Vogue Runway, hasta 2023): nivel 0,61 sobre 1, momento -0,07, pico en 2021
Búsqueda (Google Trends mundo, hasta 2024): nivel 0,84 sobre 1, momento +1,61, sigue subiendo (máximo en 2024, el último año medido)
Peso en la búsqueda frente a otras de moda, 2022→2024: +50 puntos
Validación: Google Shopping 2022→2025 +95 %, reseñas de Amazon 2019→2022 +79 %

Objetivo: una acción (Entrar, Esperar o Salir) y una sola frase, de menos de 40 palabras, que la justifique con un número de arriba.
```

Si quien diseña lo hace por su cuenta, la primera línea cambia a «Diseña por su cuenta para un cliente …: no
compromete producción ni stock, así que en vez de esperar puede explorar.» y las acciones pasan a Entrar, Explorar
o Salir.

## Límite que queda a la vista

Google Shopping sigue midiendo 2022→2025, como en v3: es la capa de validación y la app ya avisa que su 2025 es
dudoso. No entra al K-means ni a la señal.
