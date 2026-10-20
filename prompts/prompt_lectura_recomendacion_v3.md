# IA-5 · Lectura y recomendación · v3

**Fecha:** 20/10/2026
**Modelo:** Groq, `openai/gpt-oss-120b`, con `reasoning_effort: low` y sin devolver el razonamiento
(se cambia con la variable `GROQ_MODEL` en Netlify)
**Estado:** en uso, en vivo, en `netlify/functions/lectura.mjs`. Reemplaza a v2.

## Qué cambió desde v2

- **El modelo.** v2 pedía `llama-3.3-70b-versatile`, que Groq ya no ofrece: al conectar la clave, la API
  devolvió 404. Hoy los modelos de lenguaje de Groq son `gpt-oss-120b`, `gpt-oss-20b` y Qwen. Elegimos el
  más grande. Es un modelo que razona antes de contestar; con esfuerzo bajo usa unos 60 tokens, por eso el
  máximo de salida sube de 200 a 500.
- **La búsqueda ya no usa 2025.** Desde el 20/10 el K-means mide nivel 2023–24 y momento 2023–24 contra
  2020–21, así que el límite que anotaba v2 (momento con 2024–25) ya no vale.

El texto del prompt —sistema y usuario— es el mismo de `prompt_lectura_recomendacion_v2.md`, igual que la
validación de lo que entra y lo que sale.

## Primeras respuestas reales (20/10/2026)

| Atributo · cliente | Acción | Frase |
|---|---|---|
| Jeans baggy · high fashion, para una marca | Entrar | El nivel de búsqueda 0,91 y el crecimiento +13 puntos indican que los jeans baggy están en auge, pese al bajo 0,61 en pasarela, es momento de incorporarlos. |
| Lunares · diseño emergente, por su cuenta | Explorar | Con un aumento de +20 puntos en peso de búsqueda y +24 % en validación, los lunares están listos para una nueva ola creativa. |
| Y2K · fast fashion, para una marca | Entrar | El nivel de búsqueda es 0,95 y el momento +0,81, indicando fuerte impulso del Y2K pese a la ligera caída de peso; es momento de incorporarlo. |

Los números que cita están en los datos que recibió. **No siempre coincide con la recomendación fija:**
para jeans baggy en high fashion la fija dice «Esperar» (el pico llega antes que la colección) y el modelo
dice «Entrar». Por eso las dos quedan a la vista, y la del modelo marcada como interpretación.
