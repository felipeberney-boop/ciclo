# Prueba del jurado · preregistro

Escrito y commiteado el 27/10/2026, **antes de juntar una sola respuesta**. La fecha del commit es la garantía de
que ni la hipótesis, ni el criterio, ni las etapas del modelo se ajustaron después de ver los resultados. Si algo de
este archivo cambia después de recibir respuestas, se agrega abajo como enmienda fechada; no se reescribe.

## La hipótesis, reformulada

La hipótesis de la Entrega 1 juntaba tres afirmaciones. Dos ya se probaron y se rechazaron: que la pasarela adelanta
a la búsqueda (a escala anual) y que se puede predecir (cuatro métodos y VISUELLE). La tercera nunca se puso a prueba,
porque no existe una etapa «correcta» con la cual comparar. Esta prueba la pone a prueba.

> **H.** Cruzando pasarela y búsqueda, un modelo sin etiquetas (K-means) ubica cada atributo de moda en una etapa de
> su ciclo que coincide con la que le asignan, sin ver el modelo, personas que trabajan en diseño de moda, más de lo
> que coincidiría por azar.

Lo que H **no** dice: que esa etapa sirva para predecir. Eso ya está rechazado y se mantiene como límite.

## Diseño

- **Atributos:** los 17 del K-means, los mismos de la app (sin calzado).
- **Momento:** «hacia fines de 2024», porque el modelo usa datos hasta 2024 (2025 y 2026 están contaminados).
- **Etapas:** emergente, en ascenso, en pico, saturada, en retorno, con la definición de la app, más «No sé».
- **Jurado:** entre 5 y 10 personas que trabajan o estudian diseño de moda. No participan Felipe ni Abril.
  Cada una responde sola, sin abrir CICLO, en `app/jurado/` (el orden de los atributos cambia en cada persona).
- **Etapas del modelo, congeladas hoy** (`kEtapaN()` de la app, commit de este archivo):

| Atributo | Etapa del modelo |
|---|---|
| Jeans baggy | En pico |
| Jeans rectos | Saturada |
| Jeans skinny | Saturada |
| Buzo / hoodie | Saturada |
| Floral | Saturada |
| Lunares | En retorno |
| Cuero | En retorno |
| Animal print | En retorno |
| Kimono | Saturada |
| Capa | Saturada |
| Trench | Saturada |
| Encaje | En retorno |
| Cuadros | En retorno |
| Piel | En retorno |
| Cargo | En pico |
| Y2K | En ascenso |
| Blazer oversize | Saturada |

## Análisis (fijado de antemano)

`codigo/evaluar_jurado.py`, sobre `datasets/jurado/respuestas.txt`.

1. **Acuerdo del modelo con el jurado.** Para cada persona, la proporción de atributos en los que su etapa coincide
   con la del modelo (sin contar los «No sé»). El estadístico es el promedio entre personas.
2. **Contra el azar.** Se barajan las etapas del modelo entre los 17 atributos 10.000 veces (se conserva cuántos hay
   de cada etapa) y se recalcula el promedio. p = proporción de barajadas con acuerdo igual o mayor que el observado.
3. **Acuerdo del jurado entre sí.** Promedio de la kappa de Cohen entre cada par de personas.

## Criterio de decisión (fijado de antemano)

- **El jurado no se pone de acuerdo** (kappa entre personas < 0,20): la prueba **no concluye**. Sin una referencia
  compartida entre expertos, no hay contra qué medir al modelo. Se informa así; no cuenta como refutación ni como
  confirmación.
- **El jurado se pone de acuerdo y p < 0,05:** H **se sostiene**.
- **El jurado se pone de acuerdo y p ≥ 0,05:** H **se rechaza**.

Se informa siempre el número, salga como salga, en `decisiones.md`, en la app (Método) y en la presentación.

## Lo que esta prueba no controla

- Las personas del jurado pueden conocer la app o haber escuchado lo que dice. Se les pide no abrirla antes.
- Un jurado de la cátedra y de compañeros no es «la industria»: es un jurado chico y argentino, y se dice así.
- El modelo y el jurado pueden coincidir por mirar la misma cosa (lo que se ve en las redes). Coincidir no prueba que
  los dos tengan razón: prueba que el modelo lee lo mismo que lee alguien que sabe.

## Respuestas

Cada persona copia un código del formulario (empieza con `CICLO-JURADO-1|`) y lo manda. Se pegan tal cual, uno por
línea, en `datasets/jurado/respuestas.txt`.
