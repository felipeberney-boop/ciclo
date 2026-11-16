# Entrega 4 · guion de la demo (17/11/2026)

**16/11, probado.** `codigo/probar_demo.js` hizo los ocho pasos con Groq de verdad y una foto subida: 8 de 8, sin errores
(también sin clave, y a 393 px).

10 minutos. El centro es la app funcionando; el making of (`app/presentacion/`) se abre sólo para los criterios 2, 3 y 4.

| Tiempo | Qué | Criterio |
|---|---|---|
| 0:45 | Qué es CICLO y para quién; QR | 1 |
| 6:15 | **Demo en vivo** (pasos 1 a 6) | 1 y 3 |
| 2:30 | Making of: los datos (0:20), el system prompt (0:30), el prototipo, «Muy IA» y cómo quedó (1:10), la pirueta (0:30) | 2, 3, 4 y la pirueta |
| 0:30 | Links: app, repositorio, racional | 5 |

## Antes de entrar

- Dos pestañas: la app en **ventana privada** (arranca en las tres preguntas) y `…/ciclo/presentacion/#datos`.
- En la app, Preguntar → «Activar la respuesta escrita» y pegar la clave de Groq. Volver con «Cambiar perfil».
- Una foto de un look tuyo en el escritorio, para soltarla. Si no hay, el plan es el look de ejemplo «Denim».
- **Abrir Preguntar y soltar una foto una vez antes de clase**, con internet: baja el modelo de imágenes (una sola vez) y
  queda en caché. En clase lee en 2 a 4 segundos.
- Correr `GROQ_KEY=gsk_… IMAGEN=tu_foto.jpg node codigo/probar_demo.js`: hace los pasos de abajo y dice si alguno falla.
- **Después de correrlo, esperar un minuto** antes de empezar: el plan gratis de Groq deja 8.000 tokens por minuto y
  cada llamada usa unos 6.000.

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

**5 · Preguntale a CICLO** (1:45). Ir a Preguntar. Primero la pregunta, después la imagen: así las dos llamadas a Groq quedan
separadas por un minuto y no hay espera.
- Tocar la sugerencia **«¿Qué material le va a un jean baggy?»** (no hay que tipear; ya sabe que estoy diseñando un baggy).
  > «El modelo no ve ninguna fila de datos: recibe métricas ya calculadas. Primero la respuesta, después el número que
  > la sostiene, y adentro la curva de lo que nombra.» Abrir **«Qué se le mandó al modelo»**: > «Esto es todo lo que
  > recibió. Lo que dice se puede auditar contra esto.»
- Soltar la foto en la pantalla. > «CLIP la lee en mi navegador, la foto no sale de la compu. Lo que leyó son chips:
  si se equivoca, lo corrijo.» Tocar × en un chip mal leído: > «Y la misma respuesta se rehace.»

**6 · El brief, la pirueta** (1:15). Más → El brief. Elegir silueta, material y estampa; ver el veredicto.
> «Un brief de una casa real. Cada elección se juzga con su serie de búsqueda: si estás entrando o llegás tarde. Los
> puntos son una regla de juego, y la pantalla lo dice.»

## Making of · 2:30

Abrir la pestaña de la presentación (← → avanza; N muestra las notas).
Siete láminas. Salvo la primera y la última, cada una es un giro: el antes a la izquierda, qué pasó en el medio, el
después a la derecha.
- **Los datos** (0:30): lámina 01. «Dos fuentes entran, cuatro comprueban; se cruzan por atributo y año.»
- **El system prompt** (0:30): lámina 02. «La misma pregunta, antes y después de la devolución de Cristian: ahora
  contesta primero.»
- **El prototipo original** (0:30): lámina 03, con ↓ para pasar los tres pares. «Lo que corregí con el oficio: el jean es
  un material, el jersey es tela de remera.»
- **«Muy IA»** (0:25): lámina 04. «Iván dijo que se veía muy IA; elegí Apple como referencia; la misma pantalla, antes y
  después.»
- **Cómo quedó** (0:20): lámina 05. «Una app, no una entrega.»
- **El brief, la pirueta** (0:30): lámina 06, con ↓ para el segundo par. «La pirueta que vio la cátedra se miraba; ésta se
  juega. Las cartas pedían leer curvas; ahora diseñás y te enterás si tuviste ojo.» Si ya se jugó en la demo, sólo el
  giro.
- **Links**: lámina 07, con el QR.

## La pregunta al modelo

**«¿Qué material le va a un jean baggy?»** Es una de las sugerencias fijas, así que se toca, no se tipea.

**Probada el 16/11 con v9** (`datasets/pruebas/asistente_v9_respuestas.md`): «Gamuza, el material que más sube, le va a
un jean baggy.» · «Gamuza +29 puntos fuera 2022→2024». Adentro de la respuesta, la foto y la curva de la gamuza. El
modelo no es determinista: la redacción cambia, los números tienen que ser los de DATOS.

## Plan B

- **Groq no responde o la clave falla:** la burbuja se arma igual con todo lo medido y dice por qué no hay texto
  («No hubo conexión con api.groq.com…» o «Groq rechazó la API key…»). Con una imagen, la devolución la arman reglas, y lo
  dice. Leer la respuesta guardada en `asistente_v9_respuestas.md`, diciendo que es de la prueba de ayer.
- **Límite de Groq** (8.000 tokens por minuto en el plan gratis): la burbuja dice «Groq pide esperar… Reintento en N s»
  y reintenta sola. Mientras, explicar los chips o la curva. Si hace falta, pasar a `gpt-oss-20b` (tiene su propio límite).
- **Sin internet en la sala:** `cd app && python3 -m http.server 8000` y abrir `localhost:8000`. Anda todo menos la
  respuesta escrita, las fotos de Vogue (se ven los dibujos) y la tipografía de Google. CLIP necesita el modelo
  descargado: abrir Preguntar una vez con internet antes de clase, así queda en caché.
- **No carga nada:** el recorrido en capturas del readme.

## Dónde cortar si vas justo

1. El paso 4 (Diseñar): ir de la ficha directo a Preguntar.
2. En el making of, los pares 2 y 3 de la lámina 03 (quedarse con el primero).
3. **Nunca cortar el 5 ni el 6**: son la IA en tiempo real y la pirueta, que pide la consigna.
