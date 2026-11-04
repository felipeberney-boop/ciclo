# IA-5 · Lectura y recomendación · v5

**Fecha:** 04/11/2026
**Modelo:** Groq, `openai/gpt-oss-120b`, igual que v4 (`reasoning_effort: low`, 500 tokens, temperatura 0,3, JSON).
**Estado:** en uso, en `app/index.html` (`LV_SISTEMA`, `lvPrompt()`, `lvPedir()`). Reemplaza a v4.

## Qué cambió desde v4

Sólo la primera línea del mensaje de usuario. La entrada de la app dejó de preguntar si la persona trabaja para una
marca o por su cuenta y pregunta qué está por decidir (devolución de la Entrega 3, `decisiones.md`, 04/11). El sistema,
los números y la validación de la salida son los de v4.

| Qué está por decidir | Primera línea | Acciones válidas |
|---|---|---|
| Qué diseñar | `Cliente: Está decidiendo qué diseñar para una marca {categoría}: todavía no compromete producción ni stock, así que en vez de esperar puede explorar.` | Entrar, Explorar, Salir |
| Qué producir | `Cliente: Está decidiendo qué producir para una marca {categoría}.` | Entrar, Esperar, Salir |
| Si algo ya pasó | `Cliente: Está revisando si algo que ya hizo para una marca {categoría} sigue vigente.` | Entrar, Esperar, Salir |

El resto de la línea sigue igual: `Plazo de producción: … Decide para colecciones hasta ….`

## Sistema

Igual a v4, sin cambios:

```
Sos analista de tendencias de CICLO. Leés métricas ya calculadas sobre un atributo de moda (un color, una estampa, un corte o un material) y decís qué conviene hacer con él.
Reglas:
- Usá sólo los datos que te paso. No inventes cifras, marcas, temporadas ni fuentes.
- Escribí en castellano rioplatense, sin jerga, para diseñadores. Tono directo.
- La frase cita al menos un número de los datos, tal como aparece.
- Respondé sólo con JSON: {"accion": "...", "frase": "..."}.
```

## Sin probar en vivo

Esta versión no se probó contra Groq: se escribió sin una clave a mano. Cuando se pruebe, la prueba va acá.
