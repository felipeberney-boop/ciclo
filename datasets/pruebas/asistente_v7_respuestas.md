# Preguntar · prompt v7 · seis preguntas reales

Corrido el 10/11/2026, 10:21:43 con `codigo/probar_asistente.js`, perfil high fashion · para una marca · mujer.
Cada respuesta es la del modelo, sin editar. Es interpretación: los datos que cita están en `app/llm/ciclo_datos.md`.

## ¿Qué material está de moda ahora?

Sin diseño armado.

**Gamuza, la que más sube.**

+29 puntos en la búsqueda mundial 2022→2024, señal

Plegado: (sin detalle)

Datos que cita: +29 puntos, señal, 2022→2024

fuera_de_datos: false · palabras: 5 + 8 · acción: — · Unos 4445 tokens de instrucciones y datos. Leyó: Material · Gamuza · Material · Lana · Material · Popelina · Material · Merino · Material · Bouclé · Material · Gasa · Material · Polar · Material · Tul.

## ¿Qué color va con un jean baggy?

Diseño armado: `prenda:pantalones,tipo:largo,corte:baggy,material:denimrigido`

**Azul medio, el que más aparece con jean baggy en pasarela.**

Azul medio 48 % de los looks (CLIP, pasarela); después azul claro/lavado 17 %.

Plegado: Es lo que CLIP leyó en looks de pasarela: interpretación, no búsqueda.

Datos que cita: Azul medio 48 % (CLIP, pasarela)

fuera_de_datos: false · palabras: 11 + 14 · acción: — · Unos 4978 tokens de instrucciones y datos. Leyó: Jeans baggy · Pantalones · Largo · Corte · Baggy · Material · Denim rígido · Pantalones · Short · Pantalones · Bermuda · Pantalones · Capri.

## ¿Las botinetas están de moda?

Sin diseño armado.

**No lo sé: CICLO no mide botinetas.**

En calzado sí se miden zapatillas (‑13 puntos en la búsqueda mundial 2022→2024) y mocasines (+16 puntos 2022→2024).

Plegado: (sin detalle)

Datos que cita: ‑13 puntos búsqueda mundial 2022→2024 (zapatillas) · +16 puntos búsqueda mundial 2022→2024 (mocasines)

Para seguir: ¿Cómo vienen las zapatillas? · ¿Qué sube en materiales?

fuera_de_datos: false · palabras: 7 + 18 · acción: — · Unos 4369 tokens de instrucciones y datos. Leyó: Calzado · Botinetas · Calzado · Zapatillas · Calzado · Mocasines.

## ¿Qué va a estar de moda en 2027?

Sin diseño armado.

**CICLO no pronostica; hasta 2024 el material que más subía era Gamuza.**

Gamuza +29 puntos en fuera 2022→2024, fuente: Materiales

Plegado: (sin detalle)

Datos que cita: +29 puntos, fuera 2022→2024, Materiales

Para seguir: ¿Qué material está subiendo más ahora? · ¿Qué prenda está en pico?

fuera_de_datos: false · palabras: 12 + 8 · acción: — · Unos 4029 tokens de instrucciones y datos. Leyó: sólo el resumen.

## ¿Conviene una falda de cuero para una marca high fashion?

Diseño armado: `prenda:faldas,tipo:mini,material:cuero`

**Esperar · La falda de cuero está en retorno y aún es temprano para comprometer producción.**

Cuero +1 puntos en la búsqueda mundial 2022→2024; etapa En retorno; regla para vos: Esperar.

Plegado: (sin detalle)

Datos que cita: +1 puntos en la búsqueda mundial 2022→2024 (material_cuero) · Etapa En retorno (material_cuero) · Regla para vos: Esperar (material_cuero)

Para seguir: ¿Qué color combina mejor con falda de cuero? · ¿Qué estampado es más adecuado para falda de cuero?

fuera_de_datos: false · palabras: 14 + 15 · acción: Esperar · Unos 4611 tokens de instrucciones y datos. Leyó: Cuero · Faldas · Mini · Material · Cuero · Faldas · Midi · Faldas · Maxi.

## ¿Los lunares están volviendo?

Sin diseño armado.

**Esperar · Todavía no: la etapa dice que vuelve, pero la búsqueda sigue cayendo.**

-3 puntos en la búsqueda mundial 2022→2024; etapa En retorno (K‑means).

Plegado: (sin detalle)

Datos que cita: -3 puntos en la búsqueda mundial 2022→2024 · etapa En retorno

Para seguir: ¿Qué color va con los lunares? · ¿Qué otra estampa está en retorno?

fuera_de_datos: false · palabras: 12 + 11 · acción: Esperar · Unos 4270 tokens de instrucciones y datos. Leyó: Lunares · Estampa · Lunares.
