# IA-8 · Preguntale a CICLO · v1

**Fecha:** 20/10/2026
**Modelo:** Groq, `openai/gpt-oss-120b` (o `gpt-oss-20b`, a elección), con `reasoning_effort: low`
**Método:** el de la V2 de la clase (system prompt + archivo .md como DATOS), con la salida en JSON de la V4
**Estado:** en uso, en la vista «Preguntar» de la app

## Cómo funciona

Como en la V2 de la clase, **corre entero en el navegador**: cada uno pega su API key de Groq, queda guardada
en ese navegador (`localStorage`, clave `groq_key`) y la página le pregunta directo a `api.groq.com`. No pasa
por ningún servidor nuestro y la clave no está en el repositorio.

La fuente de datos es un archivo Markdown, `app/llm/ciclo_datos.md`, con el formato de los ejemplos de la clase
(secciones y una línea por ítem con campos separados por `|`). No se escribe a mano: lo arma
`codigo/armar_datos_llm.js` con los datos de la app, así si cambia el K-means o una serie se vuelve a correr.

**Lo que cambia respecto de la V2, y por qué:**

- **No va el documento entero.** Pesa ~7.700 tokens y el plan gratis de Groq da 8.000 por minuto: entraría una
  pregunta por minuto. Va siempre lo general (cómo leer los números, etapas, el perfil y su fila de
  recomendaciones, el resumen de los 20 atributos y los límites) y, de las fichas detalladas, sólo las que
  nombra la conversación (hasta 3, por nombre o sinónimo: «pantalón ancho» encuentra jeans baggy), más hasta 6
  líneas de Diseñar. Queda en ~2.900 tokens por pregunta. Se eligen con las dos últimas preguntas, para que
  «¿y para hombre?» siga hablando de lo mismo.
- **La regla fija de CICLO va calculada.** En la primera prueba el modelo leyó la tabla y contestó «Entrar»
  para high fashion en pico, cuando la regla dice «Esperar». Ahora la página agrega a cada ficha
  «para vos (regla de CICLO): …» y, si el modelo decide otra cosa, la interfaz lo avisa.
- **Contesta un JSON** (`respuesta`, `accion`, `atributos`, `datos`, `fuera_de_datos`, `siguiente`) que la página
  valida: la acción tiene que ser una de las del perfil, los atributos tienen que existir en DATOS, los textos
  se recortan. Lo que muestra va en salmón, marcado como interpretación.
- **«Qué se le mandó al modelo»** muestra el system prompt completo de la última pregunta y qué fichas leyó,
  como el «ver prompt» de la V2.

## El prompt (system)

```
Sos el asistente de CICLO: ayudás a diseñadores a decidir qué atributos de moda usar según en qué etapa de su ciclo están.
Reglas:
- Usá únicamente la información de DATOS. Cada número que digas tiene que estar en DATOS, tal cual. No inventes cifras, marcas, temporadas, fuentes ni años.
- Si la respuesta no está en DATOS, poné "fuera_de_datos": true, decí qué no mide CICLO y, si sirve, qué sí mide que se acerque.
- Decí de qué capa sale cada dato (pasarela, búsqueda, Argentina, validación, CLIP) y si es medido o interpretación.
- Cuando hablás de un atributo con ficha, usá al menos dos números de capas distintas (por ejemplo búsqueda y pasarela, o búsqueda y Argentina).
- Recomendá según el perfil de quien pregunta. Si la ficha trae «para vos (regla de CICLO)», esa es la acción: usala y explicá su porqué. Sólo te apartás si un dato de DATOS lo justifica, y entonces lo decís.
- El perfil es el que eligió en la app. Si menciona otro, contestá con el suyo y decile que lo puede cambiar en «Cambiar perfil».
- Si recomendás o desaconsejás algo, completá "accion". Si comparás varios, la acción es la del que recomendás.
- CICLO no tiene calzado, no separa hombre y mujer en los datos, no detecta lo emergente y no pronostica: si te lo piden, decilo.
- Castellano rioplatense, sin jerga, tono directo, para diseñadores. De 2 a 4 oraciones. Se dice «estampa», no «estampilla».
- En "respuesta" va sólo el texto para leer: nada de nombres de campos ni JSON.
Respondé SOLO con un objeto JSON, sin texto antes ni después: { "respuesta", "accion", "atributos", "datos", "fuera_de_datos", "siguiente" }

Quien pregunta {trabaja para una marca | diseña por su cuenta}, {diseña para mujer | hombre | sin género}, perfil: {fast | medio | premium | nicho}.

=== DATOS ===
{las partes elegidas de ciclo_datos.md}
=== FIN DE DATOS ===
```

## Pruebas (20/10/2026, high fashion · para una marca · mujer, salvo aclaración)

| Pregunta | Qué pasó |
|---|---|
| ¿Meto wide leg en la colección de invierno? | Antes de calcular la regla: «Entrar» (mal). Después: **Esperar**, «con 6 meses de lead time llegarías al pico ya pasado», con búsqueda 91 % y pasarela 61 %. |
| ¿Las zapatillas chunky siguen de moda? | Fuera de los datos: «CICLO no mide calzado». |
| ¿Qué va a estar de moda en 2027? | Fuera de los datos: CICLO no pronostica; ofrece lo que sí mide. |
| ¿Qué cuello gana terreno en remeras? | Con la línea vieja («Halter 17 % (+7,8)») confundió el halter con el escote en V. Con «Halter: 17 %, +7,8 puntos» contesta bien: halter, +7,8 puntos, CLIP. |
| ¿Qué colores le van a un jean baggy? | Azul medio 48 % (+4,8), azul claro 17 %, marrón 11 %, gris 6 %, marcados como CLIP. |

## Límites

- Con el plan gratis, preguntas muy seguidas pueden dar error 429: la página dice que esperes un minuto.
- Si una pregunta no nombra ningún atributo, el modelo sólo tiene el resumen (etapa, búsqueda y terreno de los
  20): contesta, pero con menos detalle.
- Necesita abrir la app desde un servidor (Netlify, GitHub Pages o `python3 -m http.server`): con doble clic el
  navegador no deja leer `llm/ciclo_datos.md`.
