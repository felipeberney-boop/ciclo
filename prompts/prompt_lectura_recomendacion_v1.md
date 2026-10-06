# IA-5 · Lectura y recomendación · v1

**Fecha:** 22/09/2026
**Modelo:** Groq (Llama)
**Método de prompting:** RACE — Role, Action, Context, Expectation
**Estado:** en uso. Hoy corre con prompt fijo; falta conectarlo en vivo.

## Qué entra

Sólo métricas ya calculadas. Nunca una fila de la base.

- Centros del grupo: nivel y momento en pasarela, nivel y momento en búsqueda
- Validación: cambio en Google Shopping y en reseñas de Amazon
- Tipo de cliente y su plazo de producción

## El prompt

```
Contexto: sos analista de tendencias de CICLO. El cliente es una marca {tipo},
con {plazo} de producción.

Objetivo: decir si conviene entrar, esperar o salir de cada grupo.

Datos (calculados, no inventes otros): {centros del grupo: nivel y momento en
pasarela y búsqueda; cambio en Google Shopping}.

Estilo: dos frases, sin jerga. Tono: directo. Audiencia: diseñadores.

Respuesta: una acción (Entrar / Esperar / Salir) y una frase que la justifique
con un número de los datos.
```

## Qué sale

Una acción y una frase. Ejemplo real, con cliente premium y 6 meses de producción, sobre el grupo «en pico»:

> **ESPERAR.** Para una marca premium con seis meses de producción el pico ya pasó: cuando el producto
> llegue a la calle la búsqueda va a estar cayendo. La oportunidad está en el corte medio, el único de
> los tres que todavía no se movió — 22 % de la búsqueda de jeans y subiendo desde 2020.

## Por qué está así

- **El rol fija el registro.** Sin «sos analista de tendencias» el modelo escribe como folleto.
- **«No inventes otros» es la restricción que importa.** Sin eso completa con datos plausibles que no existen.
- **Pedir un número en la respuesta** obliga a anclar la recomendación en lo que recibió.
- **Dos frases** porque en la interfaz entra en una banda de 130 píxeles de alto.
