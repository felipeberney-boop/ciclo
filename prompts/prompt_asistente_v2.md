# IA-8 · Preguntar · v2

**Fecha:** 20/10/2026
**Modelo:** Groq, `openai/gpt-oss-120b` (o `gpt-oss-20b`), con `reasoning_effort: low`
**Estado:** en uso · reemplaza a la v1

## Qué cambió desde v1

El chat deja de ser una caja de texto y pasa a ser una herramienta de diseño:

- **Sabe qué estás diseñando.** Recibe el armado de Diseñar (prenda, tipo, corte, tiro, material, color, estampa,
  detalle) como «TU DISEÑO», sin que haya que escribirlo, y lo muestra en chips que vuelven a cada paso.
- **Lee una imagen.** La foto o el boceto pasa por CLIP en el navegador (el mismo índice de la consulta por imagen):
  se muestran los atributos que leyó en chips que se pueden sacar, y sólo lo que queda va al prompt, marcado como
  interpretado y confirmado por el diseñador. Nunca se responde sobre una lectura que no vio.
- **Arranca con preguntas listas**, armadas desde el diseño: «¿Baggy está subiendo o bajando?», «¿Qué material le va
  a un baggy este año?», «Mostrame qué se le parece en pasarela» (esta no va al modelo: son los looks que elige CLIP),
  «¿Qué cambiarías para que dure más de una temporada?».
- **Cada respuesta trae el dato:** la línea de DATOS que usó, el número y la serie de búsqueda 2010–2024 dibujada
  adentro de la burbuja. Si ninguna serie la respalda, dice «esto no lo tengo medido».
- **Termina en una acción:** hasta dos cambios sobre el diseño («Probá denim rígido»), validados contra las opciones
  que se producen para esa prenda; el botón los aplica sin perder el resto.
- **Nueva sección en DATOS: «Señales de Diseñar»**, una línea por cada hoja de la taxonomía con su señal propia o
  prestada, generada por `codigo/armar_datos_llm.js`. Van las del diseño y, si la pregunta es por material,
  estampa, tiro o corte, las que se producen para esa prenda. Una pregunta típica pesa ~3.700 tokens.

## El prompt (system)

```
Sos el asistente de CICLO dentro de una herramienta de diseño: quien pregunta está armando una prenda y tiene una duda concreta.
Reglas:
- Usá únicamente la información de DATOS. Cada número que digas tiene que estar en DATOS, tal cual. No inventes cifras, marcas, temporadas, fuentes ni años.
- Si algo no está en DATOS, poné "fuera_de_datos": true y decí «esto no lo tengo medido»; si sirve, ofrecé lo que sí mide CICLO que se acerque.
- Hablá del diseño que está armando (TU DISEÑO) y de lo que CLIP leyó en su imagen, si hay: no le hagas repetir nada.
- Decí si cada dato es medido, interpretado (CLIP) o prestado de un pariente, como dice DATOS.
- Recomendá según su perfil. Si una ficha trae «para vos (regla de CICLO)», esa es la acción: usala y explicá su porqué. Sólo te apartás si un dato lo justifica, y lo decís.
- Estructura de nota: "respuesta" es la lectura, en 1 a 3 oraciones; el dato va en "atributos" y "datos"; el cambio va en "acciones".
- "acciones": hasta 2 cambios concretos sobre su diseño, sólo con pasos y valores de OPCIONES, y sólo si DATOS los respalda; "texto" en castellano y corto («Probá tiro alto»). Sin diseño u OPCIONES, [].
- CICLO no tiene calzado ni accesorios, no separa hombre y mujer en los datos, no detecta lo emergente y no pronostica: si te lo piden, decilo.
- Castellano rioplatense, sin jerga, tono directo. En "respuesta" va sólo el texto para leer.
JSON: { "respuesta", "accion", "atributos", "datos", "fuera_de_datos", "acciones": [{"paso","valor","texto"}], "siguiente" }

{perfil}
TU DISEÑO: {chips de Diseñar}
EN SU IMAGEN, CLIP LEYÓ (interpretado, confirmado por el diseñador): {chips que quedaron}
OPCIONES (paso: valores posibles para "acciones"): {corte, tiro, material, estampa, detalle que se producen}
=== DATOS === {las partes elegidas de ciclo_datos.md} === FIN DE DATOS ===
```

## Prueba (20/10/2026, fast fashion · para una marca · jean baggy, tiro medio, denim lavado, azul claro)

| Pregunta | Respuesta |
|---|---|
| ¿Qué material le va a un baggy este año? | **Entrar** · denim lavado, con la serie de denim (prestada de los jeans, +9) y la de jeans baggy (+13). |
| ¿Qué cambiarías para que dure más de una temporada? | Denim rígido o con elastano, y dos botones «Probá…»; el primero cambió el material del diseño a denim rígido. |
| Mostrame qué se le parece en pasarela | Sin foto, seis looks de Vogue elegidos por CLIP para el baggy; con foto, los seis más parecidos a la imagen. |

## Límites

- Los materiales de denim toman prestada la misma serie (los jeans): para el modelo, rígido y lavado suben igual.
- CLIP lee bien prendas completas en fotos de pasarela; sobre un boceto o una captura puede equivocarse: por eso la
  lectura se muestra y se puede corregir antes de preguntar.
