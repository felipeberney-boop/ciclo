# Entrega 3 · guion de la presentación y de la demo (03/11/2026)

Con la devolución de Cristian del 03/11: primero el flujo de la app, y láminas simples. Son seis láminas, una por
criterio de la rúbrica, y la presentación termina en el Cierre.

Presentación: https://felipeberney-boop.github.io/ciclo/presentacion/ · App: https://felipeberney-boop.github.io/ciclo/
(en la presentación, la tecla N muestra las notas de cada lámina).

| Tiempo | Qué | Criterio |
|---|---|---|
| 1 min | 01 · Portada | — |
| 7 min | **Demo en vivo** | 1: la decisión que hoy no se toma bien |
| 1 min | 02 · La hipótesis | 1 |
| 1 min | 03 · Los datos | 2 |
| 1 min | 04 · La IA | 3 |
| 1 min | 05 · Del diseño al código | 4 |
| 1 min | 06 · Cierre: app, repositorio, Figma | 5 |
| 2 min | Preguntas | — |

## Antes de entrar

- Abrir dos pestañas: la presentación y la app en una **ventana privada** (así arranca en las tres preguntas, sin perfil guardado).
- En la app, abrir Preguntar → «Activar el chat» y pegar la clave de Groq. Después, volver a la entrada con «Cambiar perfil».
- Correr `node codigo/probar_demo.js` (o, con la clave, `GROQ_KEY=gsk_… node codigo/probar_demo.js`): hace los siete
  pasos de abajo y dice si alguno falla. El 03/11 pasaron los siete.

## 01 · Portada · 1 min

CICLO dice en qué etapa está cada atributo de moda —un color, una estampa, un corte, un material— y qué hacer con eso
según tu plazo. Que abran el QR. Y en seguida, para pasar a la app:

> «Ahora la demo, siete minutos. No es un paseo por la app: es ver a una diseñadora tomar hoy una decisión que antes no
> podía tomar bien. Diseña para una marca de high fashion y quiere saber si entrar con un jean ancho.»

## La demo · 7 min

**1 · Las tres preguntas de entrada** (0:40). Mujer → Para una marca → High fashion. «Cada tarjeta dice sólo lo que hay
que tocar. Lo que cambia cada respuesta —el plazo de producción, hasta qué año sirve el gráfico— está en Método.»

**2 · Tendencias** (1:00). «Esta es la pantalla principal: qué gana y qué pierde terreno afuera, medido en la búsqueda
mundial 2022→2024. Arriba dice con qué perfil estoy leyendo.» Señalar Jeans baggy +50 arriba de todo.

**3 · La ficha de un atributo** (1:20). Bajar y tocar **Amplio**. «Cada atributo tiene su serie: pasarela, búsqueda y
Reddit hasta 2024. La punteada no es un pronóstico, muestra la escala posible. Y cada número dice de dónde sale.»

**4 · «Diseñar con este corte · Baggy»** (0:30). «Del dato a la decisión en un clic: el corte queda fijo arriba y la
app sólo me pregunta lo que falta.»

**5 · Diseñar** (1:20). «Seguir sin elegir tiro» → **Denim rígido**. «Cada opción trae su señal —Entrar, Esperar o
Salir, siempre con la palabra— y su procedencia. Abajo se acumula lo que elegí.»

**6 · Preguntar** (1:50). Ir a Preguntar: «Tu diseño» ya trae pantalones, largo, baggy y denim rígido. Tocar el campo y
escribir la pregunta, exacta:

> **¿Qué color va con un jean baggy?**

Mientras contesta: «El modelo no ve ninguna fila de datos. Le llegan métricas ya calculadas.» Cuando contesta, abrir
**«Qué se le mandó al modelo»** (columna izquierda, abajo): «Esto es exactamente lo que recibió: el system prompt, mi
diseño y sólo las fichas que nombra la pregunta, unos 4.600 tokens. Lo que dice se puede auditar contra esto.»

Probada el 27/10 con el prompt v5, con el mismo diseño y el mismo perfil (`datasets/pruebas/asistente_v5_respuestas.md`).
Respondió: «Para un jean baggy, el color que más destaca es azul medio (48 % y +4,8 puntos), seguido de azul
claro/lavado (17 % y +1,8)…», con los tres datos citados como CLIP, es decir interpretación. Desde entonces no cambiaron ni el
prompt ni los datos, y el 03/11 la app arma el mismo contexto (4.603 tokens, las mismas fichas). El modelo no es
determinista: la redacción puede variar, los números tienen que ser esos.

**7 · Método** (0:20). Más → Método. «Todo lo que se ve en la app cae en una de dos columnas: medido o interpretado, y
cada fila dice cuál.» Volver a la presentación.

### Plan B

- **Groq no responde o no hay internet en Preguntar:** la app lo dice («No hubo conexión con api.groq.com…»). Abrir
  igual «Qué se le mandó al modelo»: el contexto se arma sin conexión, y eso es lo que importa mostrar. Leer en voz alta
  la respuesta del 27/10 de `asistente_v5_respuestas.md` diciendo que es de esa prueba.
- **Límite de Groq** (8.000 tokens por minuto en el plan gratis): esperar un minuto, o cambiar el modelo a
  `gpt-oss-20b (más rápido)` en «Activar el chat».
- **Sin internet en toda la sala:** la app es un único archivo. Servirla desde la compu (`cd app && python3 -m http.server 8000`)
  y abrir `localhost:8000`: todo anda menos Preguntar y las tipografías de Google.
- **Si no carga nada:** mostrar el recorrido en capturas en el readme (sección «El recorrido, paso a paso»), que son de hoy.

### Dónde cortar si vas justo

1. Saltar el paso 7 (Método): está en la lámina 03.
2. En el paso 5, no explicar las señales: ir directo a Denim rígido.
3. En el paso 3, no bajar hasta Reddit: alcanza con la primera serie.
4. Como último recurso, saltar el paso 4 y entrar a Diseñar por el menú. **Nunca cortar el 6**: es el criterio 3 en vivo.

## 02 · La hipótesis · 1 min

«Lo que acaban de ver, dicho en una frase: quien diseña ve en qué etapa está cada atributo y si llega a tiempo con su
plazo.» Qué se ajustó: la unidad es el atributo porque es lo que se puede contar en todas las fuentes, y el foco es leer
el presente porque pasarela y búsqueda se mueven juntas. La evidencia: el K-means agrupa los jeans ajustados en
«saturada» y los amplios en «pico», y en reseñas de Amazon 2019–2022 los ajustados caen 39 % y los amplios suben 79 %
(+95 % en Google Shopping). El modelo no vio ninguno de esos datos.

## 03 · Los datos · 1 min

Tres capas con su número: 1,28 M looks de Vogue Runway, 65 series de Google Trends, 30,6 M compras de H&M. Un cálculo:
la pasarela es la parte de los looks de cada año que lleva el atributo, y se rehace con `codigo/`. En la interfaz,
medido, interpretado o prestado. El límite: todo corta en 2024, porque desde 2025 Google mide distinto.

## 04 · La IA · 1 min

La regla: el modelo nunca ve una fila de datos, y por eso lo que dice se puede auditar. Leer en pantalla las dos
primeras reglas del system prompt. Recibe métricas ya calculadas (una línea real de DATOS) y devuelve un JSON con
respuesta, acción, atributos y datos. Corre con la API de Groq, gpt-oss-120b, desde el navegador.

## 05 · Del diseño al código · 1 min

Tres etapas: el prototipo de Figma de la Entrega 2 → Iván veía la interfaz «muy IA» y nos pasó la referencia del
sistema de Apple → cómo quedó. En el código, no en Figma: los estados, el celular a 393 px, la carga de CLIP y los errores.

## 06 · Cierre · 1 min

La app, el repositorio y el Figma en pantalla. «CICLO: en qué etapa está cada atributo de moda, y qué hacer con eso.»

## Si preguntan

Las láminas no tienen respaldo: las respuestas están en el proyecto, donde la rúbrica pide que estén documentadas.

| Pregunta probable | Dónde está |
|---|---|
| ¿Cómo saben que la etapa está bien? | Método, fila «¿La etapa coincide con afuera?» (Reddit, p = 0,0013) · `hipotesis.md` |
| ¿Qué decide exactamente el perfil? | Método, «La entrada: qué cambia cada respuesta» |
| ¿Por qué no predice? | Método, fila «Hasta 2030 · el cono» (cuatro métodos) |
| ¿Y con ventas reales? | `decisiones.md`, 13/10: VISUELLE |
| ¿Por qué no 2025 y 2026? | Método, fila «2025 y 2026 en la búsqueda» |
| ¿Y el calzado? | Método, fila «Calzado» · en la app, Diseñar → Calzado |
| ¿Cómo es el K-means? | Método, fila «Etapa del ciclo (K-means)» · en la app, Más → El modelo |
| ¿El prompt entero? ¿Qué recibe? | `prompts/prompt_asistente_v5.md` · en la app, Preguntar → «Qué se le mandó al modelo» |
| ¿Una respuesta real? | `datasets/pruebas/asistente_v5_respuestas.md` |
| ¿Qué tomaron de la referencia? ¿Qué cambió del Figma? | `entregas/entrega_3/figma_a_codigo.md` |

Más preguntas, con su respuesta: `entregas/entrega_3/preguntas_probables.md`. La presentación anterior, de catorce
láminas, quedó en `diseno/prototipos/versiones_de_la_presentacion/presentacion_2026-11-03_cba39cc_catorce_laminas.html`.
