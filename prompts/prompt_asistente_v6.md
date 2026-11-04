# IA-8 · Preguntar · v6

**Fecha:** 04/11/2026
**Modelo:** Groq, `openai/gpt-oss-120b` (o `gpt-oss-20b`), igual que v5.
**Estado:** en uso · reemplaza a la v5

## Qué cambió desde v5

Sólo la línea que dice quién pregunta (`asQuien()` en `app/index.html`). La entrada dejó de preguntar por el vínculo
laboral y pregunta qué está por decidir (`decisiones.md`, 04/11):

- Qué diseñar → `Quien pregunta está decidiendo qué diseñar (todavía sin producción ni stock), …`. Las acciones
  válidas son Entrar, Explorar y Salir, y un «Esperar» que llegue se cambia por «Explorar».
- Qué producir → `Quien pregunta está decidiendo qué producir, …`
- Si algo ya pasó → `Quien pregunta está revisando si algo que ya hizo sigue vigente, …`

El system prompt, los DATOS (`app/llm/ciclo_datos.md`) y la validación de la respuesta son los de
`prompt_asistente_v5.md`, sin cambios.

## Sin probar en vivo

No se corrió `codigo/probar_asistente.js` con esta versión: hace falta una clave de Groq. Cuando se pruebe, la prueba va acá.
