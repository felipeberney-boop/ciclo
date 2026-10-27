# Prueba con Reddit · preregistro

Escrito y commiteado el 27/10/2026, **antes de calcular el resultado**. Reemplaza al jurado como prueba principal
(el jurado queda disponible, pero depende de conseguir personas). Declarado: al revisar si había datos se vieron por
arriba los últimos valores de Reddit; por eso la métrica no se elige ahora sino que es la misma que el modelo ya usa.

**Hipótesis.** La etapa que el K-means le asigna a cada atributo (con pasarela y búsqueda hasta 2024) se corresponde
con cómo se mueve ese atributo en las conversaciones de Reddit, una fuente que el modelo no usó.

**Datos.** Reddit vía Arctic Shift: posts de r/femalefashionadvice que nombran el término, divididos por el total del
sub cada año (`RDS` en la app). 14 de los 17 atributos tienen término propio. Quedan afuera Capa y Piel (sin término)
y Blazer oversize («oversized» nombra cualquier prenda amplia, no el blazer).

| Atributo | Término de Reddit | Etapa del modelo |
|---|---|---|
| Jeans baggy | baggy jeans | En pico |
| Jeans rectos | mom jeans | Saturada |
| Jeans skinny | skinny jeans | Saturada |
| Buzo / hoodie | hoodie | Saturada |
| Floral | floral | Saturada |
| Lunares | polka dot | En retorno |
| Cuero | leather jacket | En retorno |
| Animal print | leopard | En retorno |
| Kimono | kimono | Saturada |
| Trench | trench | Saturada |
| Encaje | lace | En retorno |
| Cuadros | plaid | En retorno |
| Cargo | cargo pants | En pico |
| Y2K | y2k | En ascenso |

**Métrica (la misma del modelo).** Momento en Reddit = promedio 2023–24 / promedio 2020–21 − 1.

**Prueba.** ¿La etapa del modelo explica el momento en Reddit? Estadístico: proporción de la variación del momento
que explican los grupos de etapa (η²). Contra el azar: barajar las etapas entre los 14 atributos 10.000 veces.
**Criterio:** p < 0,05 → la hipótesis se sostiene; si no, se rechaza. Se informa también el momento medio por etapa,
para ver si va en la dirección esperada (ascenso y pico arriba, saturada abajo).

Script: `codigo/prueba_reddit.py`. Se informa el resultado salga como salga.

## Resultado (27/10/2026, después del commit de arriba)

**Se sostiene: η² = 0,88, p = 0,0013.** Los tres atributos que el modelo pone arriba (Y2K en ascenso; cargo y jeans
baggy en pico) son exactamente los tres que más crecen en Reddit (+258 %, +187 %, +130 %). Que los tres de arriba
caigan justo en los tres primeros lugares de 14 pasa por azar 1 vez en 364.

**Controles agregados después, y marcados como tales (no estaban en el preregistro):**
- Por rangos en vez de valores, para que un número extremo no infle el resultado: η² = 0,51, p = 0,047. Pasa, más
  justo.
- Retorno contra saturada: η² = 0,00, p = 0,88. **Reddit no distingue esas dos etapas** (−17 % y −14 % de media).
  El modelo separa bien lo que sube de lo que no, pero la diferencia entre «en retorno» y «saturada» no tiene respaldo
  en esta fuente.

**Límites.** 14 atributos; «en ascenso» tiene uno solo. Reddit y la búsqueda no son del todo independientes: las dos
reflejan qué le interesa a la gente. Lo que prueba es que el modelo lee lo mismo que muestra una fuente que no usó,
no que exista una etapa «verdadera».
