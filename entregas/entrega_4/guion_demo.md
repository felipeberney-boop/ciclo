# Entrega 4 · guion de la demo (17/11/2026)

**Borrador del 16/11.** El paso 5 (Lectura) depende de la sección nueva: se cierra cuando esté construida y probada con
`codigo/probar_demo.js`. La pregunta al modelo todavía **no está probada con el prompt v9** (ver abajo).

10 minutos. El centro es la app funcionando; el making of (`app/presentacion/`) se abre sólo para los criterios 2, 3 y 4.

| Tiempo | Qué | Criterio |
|---|---|---|
| 0:45 | Qué es CICLO y para quién; QR | 1 |
| 6:15 | **Demo en vivo** (pasos 1 a 6) | 1 y 3 |
| 2:30 | Making of: los datos (1:15), la IA (0:45), del diseño al código (0:30) | 2, 3, 4 |
| 0:30 | Links: app, repositorio, racional | 5 |

## Antes de entrar

- Dos pestañas: la app en **ventana privada** (arranca en las tres preguntas) y `…/ciclo/presentacion/#datos`.
- En la app, Lectura → «Activar la respuesta escrita» y pegar la clave de Groq. Volver con «Cambiar perfil».
- Una foto de un look en el escritorio, para soltarla (la de prueba: `entregas/entrega_4/demo/look.jpg`, por elegir).
- Correr `GROQ_KEY=gsk_… node codigo/probar_demo.js`: hace los pasos de abajo y dice si alguno falla.

## 0 · Qué es CICLO · 0:45

> «CICLO le dice a quien diseña ropa en qué momento está un atributo —un corte, un material, una estampa— y si le
> conviene entrar, esperar o salir, según para quién diseña. Escaneen el QR y síganlo en el celular.»

## La demo · 6:15

**1 · La entrada** (0:30). Mujer → Para una marca → Fast fashion.
> «Tres preguntas, nada más. Con eso la app ya sabe qué plazo tengo y qué le conviene a mi tipo de marca.»

**2 · Tendencias** (1:00). Dejar correr una vuelta del gráfico; señalar Jeans baggy arriba.
> «Lo que gana y pierde terreno en la búsqueda mundial, 2022 a 2024. Cada tarjeta trae su etapa y su señal: verde es
> entrar, siempre con la palabra.»

**3 · La ficha de Jeans baggy** (1:00). Tocar la tarjeta.
> «Pasarela y búsqueda, cada una con su fuente. La punteada no es un pronóstico: es el margen de lo que pasó otras
> veces. Cada número dice si es medido, interpretado o prestado.»

**4 · Diseñar** (0:45). «Diseñar con este corte» → elegir un material con señal verde.
> «Del dato a la decisión: cada opción trae su señal, y lo que elijo se acumula abajo.»

**5 · Lectura** (1:45). Ir a Lectura.
- Soltar la foto en la pantalla. > «CLIP la lee en mi navegador, la foto no sale de la compu. Lo que leyó son
  chips: si se equivoca, lo corrijo.» Tocar × en un chip mal leído.
- Tocar la sugerencia **«¿Qué material le va a un jean baggy?»** (no hay que tipear).
  > «El modelo no ve ninguna fila de datos: recibe métricas ya calculadas. Primero la respuesta, después el número que
  > la sostiene.» Abrir **«Qué se le mandó al modelo»**: > «Esto es todo lo que recibió.»

**6 · El brief, la pirueta** (1:15). Más → El brief. Elegir silueta, material y estampa; ver el veredicto.
> «Un brief de una casa real. Cada elección se juzga con su serie de búsqueda: si estás entrando o llegás tarde. Los
> puntos son una regla de juego, y la pantalla lo dice.»

## Making of · 2:30

Abrir la pestaña de la presentación (← → avanza; N muestra las notas).
- **Los datos** (1:15): láminas 01 y 02. «Dos fuentes entran, cuatro comprueban; se cruzan por atributo y año.» La 05:
  «lo que el modelo pone arriba es lo que más crece en Reddit, que no vio».
- **La IA** (0:45): lámina 06 y la 07 con el prompt en pantalla. «Nunca ve una fila.»
- **Del diseño al código** (0:30): 09 → 10 → 11. «El prototipo, la devolución de Iván con la referencia de Apple, y hoy.»
- **Links** (0:30): lámina 12.

## La pregunta al modelo

**«¿Qué material le va a un jean baggy?»** Es una de las sugerencias fijas, así que se toca, no se tipea.

**Estado: falta probarla con v9.** En esta sesión no hay clave de Groq. La última respuesta real guardada es de v5
(`datasets/pruebas/asistente_v5_respuestas.md`, «¿Qué color va con un jean baggy?»). Para dejarla probada hoy:
`GROQ_KEY=gsk_… node codigo/probar_demo.js`. Guardar la respuesta en `datasets/pruebas/asistente_v9_respuestas.md`. El
modelo no es determinista: la redacción cambia, los números tienen que ser los de DATOS.

## Plan B

- **Groq no responde o la clave falla:** la burbuja se arma igual con todo lo medido, y dice «Groq no respondió». Abrir
  «Qué se le mandó al modelo» (se arma sin conexión) y leer la respuesta guardada, diciendo que es de la prueba.
- **Límite de Groq** (8.000 tokens por minuto en el plan gratis): esperar un minuto o pasar a `gpt-oss-20b`.
- **Sin internet en la sala:** `cd app && python3 -m http.server 8000` y abrir `localhost:8000`. Anda todo menos la
  respuesta escrita, las fotos de Vogue (se ven los dibujos) y la tipografía de Google. CLIP necesita el modelo
  descargado: abrir Lectura una vez con internet antes de clase, así queda en caché.
- **No carga nada:** el recorrido en capturas del readme.

## Dónde cortar si vas justo

1. El paso 4 (Diseñar): ir de la ficha directo a Lectura.
2. En el making of, la lámina 05 (Reddit).
3. **Nunca cortar el 5 ni el 6**: son la IA en tiempo real y la pirueta, que pide la consigna.
