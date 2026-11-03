# Entrega 3 · guion de la presentación (03/11/2026)

Quince minutos en el orden de los criterios: la hipótesis (2), los datos (3), la IA (3), de Figma al código (3) y la
demo (4). Presentación: https://felipeberney-boop.github.io/ciclo/presentacion/ (la tecla N muestra estas mismas
notas). El texto de cada lámina sale de sus notas del orador; cada cifra está en el repo. La versión anterior (el
making of del 27/10) quedó en `diseno/prototipos/versiones_de_la_presentacion/`.

## Inicio

**01 · Portada** · `#portada`. CICLO ubica un atributo de moda —un color, una estampa, un corte, un material— en una de cinco etapas de su ciclo de vida. Quince minutos en cinco partes: la hipótesis (2), los datos (3), la IA (3), de Figma al código (3) y la demo (4). La app está online: el QR está en la lámina de la demo.


## 1 · Hipótesis

**02 · La hipótesis, ajustada** (2 min) · `#hipotesis`. La hipótesis original juntaba tres afirmaciones: que la pasarela adelanta a la búsqueda («señales tempranas»), que se puede predecir, y que se puede ubicar la etapa del presente. Las dos primeras se probaron y se cayeron; la tercera se sostiene. También cambió la unidad: «tendencia» no se puede contar, el atributo sí (01/09). Todo está en hipotesis.md, con la fecha de cada prueba.

**03 · Lo que sube, sube afuera** · `#reddit`. Por rangos, el control agregado después, p = 0,047. Límites: 14 atributos, uno solo en ascenso, y Reddit y Google reflejan en parte lo mismo. La otra prueba preregistrada, la pasarela por temporada (de 3 a 18 meses), dio que no adelanta: medianas entre −0,04 y +0,04, hacía falta p < 0,007.

**04 · La decisión que hoy no se toma bien** · `#decision`. El foco se movió de la forecaster a quien diseña porque la misma lectura sirve para las dos, pero quien diseña necesita que la app le diga qué hacer en su prenda, no un tablero. Lo que no puede hacer hoy: saber si un atributo está subiendo o ya pasó su pico, y si su plazo de producción llega a tiempo. Con CICLO: la etapa (K-means sobre pasarela y búsqueda) cruzada con su plazo (fast fashion 6 semanas, high fashion 6 meses, nicho 3 meses) da Entrar, Esperar o Salir, con el porqué.


## 2 · Datos

**05 · Las fuentes** (3 min) · `#fuentes`. Vogue Runway: 1,28 millones de looks con etiquetas, 2000–2023. Google Trends: 65 series mundiales y 14 términos para Argentina, hasta 2024. H&M: 30,6 millones de compras (2018–2020). Para validar, sin entrar al modelo: Reddit (r/femalefashionadvice), Lyst Index (34 trimestres), Amazon Reviews y Google Shopping. Zara 2018–22 y el mix de marcas son sintéticos: quedan como demostración y la app lo dice. Fuentes, fechas y licencias: datasets/fuentes_y_descargas.md.

**06 · Del dato al número** · `#calculos`. Pasarela: proporción de looks del año que llevan el atributo; nivel = 2022–23 contra su máximo, momento = 2021–23 contra 2018–20. Búsqueda: dividida por el promedio de 35 términos de moda de cada año, para sacar el crecimiento de Google; nivel = 2023–24 contra su máximo, momento = 2023–24 contra 2020–21. El K-means usa esos cuatro números en 17 atributos, k = 4 (silhouette 0,32), y arranca de centroides guardados: da siempre lo mismo. Una tendencia nueva se asigna al centroide más cercano, nunca reentrena.

**07 · Calculado contra inferido** · `#procedencia`. Medido: sale de una fuente con un cálculo en código. Interpretado: lo dijo un modelo (CLIP o el LLM), con borde punteado. Prestado: la hoja no tiene serie propia y usa la de un pariente, siempre diciendo cuál y por qué (hermano, después padre, nunca otra familia). Hoy, de 133 hojas: 74 con dato propio, 42 prestadas y 17 sin dato. Lo que no tiene dato queda neutro, no en rojo.

**08 · Los límites** · `#limites`. Cómo afectan las conclusiones: CICLO lee el presente hasta 2024 y no detecta lo emergente (la pasarela pública llega a 2023). Lo que dice sobre la pasarela es lujo y casas grandes, no la calle. Hombre y mujer van mezclados: Vogue y H&M agregados no traen la columna, y no la simulamos. Todo esto está en la vista Método de la app y en el readme.

**09 · El trench pica en abril** · `#corte-2024`. El trench coat es el ancla con la que se pegan todos los lotes de Google Trends. Siempre picó entre octubre y diciembre; en 2026 pica en abril. 69 de 70 series saltan en 2026, mediana +99 %. En 2025 ya había empezado: 12 de 16 series tocaron su récord ese año. Consecuencia: CICLO no dice nada de 2025–26 y lo explica cuando se lo preguntan.

**10 · El calzado** · `#calzado`. Es la ausencia que más pesa: Lyst ve en calzado las señales más fuertes de 2023 y 2024, y ahí no podemos contrastar. Por eso el K-means es de 17 atributos sin calzado. Para medir botinetas, chatitas o guillerminas habría que recortar los pies de cada foto de pasarela. Un estilo de calzado nunca toma prestado el dato de otro.


## 3 · IA

**11 · Tres modelos** (3 min) · `#tres-modelos`. K-means: en el navegador, 17 atributos, 4 números cada uno. CLIP (Transformers.js, clip-vit-base-patch32): compara una foto con 14.000 looks de pasarela, también en el navegador; la foto no sale de la computadora. El LLM: gpt-oss-120b en Groq, llamado desde el navegador con la clave de cada usuario (el patrón V2 de la clase). Hay dos usos del LLM: «Preguntar» (el chat) y «Pedir lectura en vivo» en cada ficha.

**12 · El system prompt** · `#system-prompt`. Lo de la derecha es el prompt entero, el mismo texto que usa la app (AS_INSTR en app/index.html). En negrita, las reglas que importan: no inventar, contestar con lo más cercano diciendo qué se muestra en lugar de qué, el corte de 2024, la fuente de cada número por nombre, y responder sólo JSON. La v5 suma tres ejemplos con letras en vez de números, para que no los copie.

**13 · Qué recibe** · `#contexto`. DATOS es app/llm/ciclo_datos.md (62 KB), generado desde las constantes de la app con codigo/armar_datos_llm.js. No se manda entero: va lo general siempre y sólo las fichas que nombra la conversación, entre 3.600 y 4.600 tokens por pregunta. El plan gratis de Groq da 8.000 tokens por minuto. Lo que nunca se manda: una fila de Vogue, de Google Trends o de H&M. El modelo recibe «61 % de su pico, momento −7 %», no 1,28 millones de looks.

**14 · Qué devuelve** · `#devuelve`. Cómo se evita que invente: no ve filas, sólo métricas ya calculadas; cada número tiene que estar en DATOS tal cual; la acción (Entrar, Esperar, Salir) la calcula la página con la regla fija por etapa y perfil y la pega en la ficha, así que si el modelo se aparta se ve el aviso; y la respuesta trae «datos»: qué número usó y de dónde sale, para poder chequearlo. «acciones» son cambios sobre el diseño que se aplican con un botón, sólo con valores de OPCIONES.


## 4 · Figma → código

**15 · La app no salió del Figma** (3 min) · `#figma`. Lo que sí viajó del Figma, como idea: la etapa como posición en una pista y no como color, las fichas con la paleta de la prenda arriba, los filtros en pastillas y el selector de cliente. Los tokens (colores, radios, tipografía) viven en CSS y vienen del sistema de las páginas de producto de Apple, no del Figma. Documento completo: entregas/entrega_3/figma_a_codigo.md.

**16 · Las diferencias** · `#diferencias`. Con las flechas (o ↑ ↓) se pasan los cinco pares. Detalle de cada uno en entregas/entrega_3/figma_a_codigo.md. Lo curioso: la versión de Apple (27/10, por la devolución «muy IA») quedó más cerca del Figma —sans serif, pastillas, tarjetas blancas— que la revista en Bodoni que hubo en el medio. Los nombres de taller («Frisa · french terry») tampoco estaban en Figma: la regla del 20/10 es que si no se puede decir en voz alta en un taller, no va.

**17 · Lo que Figma no pregunta** · `#fuera-de-figma`. El Figma muestra cada pantalla en un solo estado: con datos, sin errores, ya cargada. Estados: hover sin sombra, foco visible con teclado, lo elegido con borde azul y aria-pressed. Celular: verificado con Playwright, ancho de página igual al del teléfono. CLIP: 89 MB de modelo más 8 MB de índice, sólo en la primera consulta y con el avance a la vista. El modo oscuro existió, se auditó el 26/10 y se apagó el 27/10: la capa nueva es siempre clara.


## 5 · Demo

**18 · Ahora, en vivo** (4 min) · `#demo`. Plan B: si Groq no responde o no está la clave, Preguntar muestra «Primero activá el chat» y se pasa a Buscar por imagen con un look del índice (no necesita el modelo de 89 MB). Si se va el tiempo, saltar Diseñar. Guion en entregas/entrega_3/presentacion_guion.md.

**19 · Gracias** · `#gracias`. Repositorio: github.com/felipeberney-boop/ciclo. Sistemas generativos e IA para Diseño · K534/K576 · UdeSA · 2026. Docentes: Cristian Reynaga e Iván Fardjoume.

---

# Guion de la demo en vivo (4 minutos)

App: https://felipeberney-boop.github.io/ciclo/
Recorrido verificado con Playwright el 03/11/2026 contra la app publicada, en un contexto limpio (como una ventana de
incógnito), a 1400 y a 393 px: los cinco pasos pasan y no hay errores de JavaScript. El paso 4 se probó sin clave, con
una clave inválida y sin conexión a Groq (los tres dan un mensaje claro), no con una respuesta real del modelo.

**Antes de empezar.** Tener la app abierta en una pestaña y la API key de Groq en el portapapeles. Si se va a usar
una foto propia, subirla una vez antes de la clase: la primera vez se bajan el modelo y el índice de CLIP (unos 96 MB)
y después quedan guardados en el navegador. Los looks de ejemplo de Buscar por imagen sólo bajan el índice (8 MB).

## Paso 1 — La entrada (0:00–0:20)

Abrir la app. Aparecen tres preguntas, en este orden.

> «Antes de mostrarte nada la app necesita saber para quién diseñás,
> porque el mismo dato puede decir "entrá" a un fast fashion
> y "esperá" a una marca high fashion.»

Elegir: **Mujer** → **Para una marca** → **High fashion / couture**.
La app va directo a **Tendencias**.

---

## Paso 2 — Tendencias y una ficha (0:20–1:10)

> «Esta es la pantalla principal. Arriba, qué gana y qué pierde terreno en la búsqueda mundial.
> Abajo, cada tarjeta es un atributo —un corte, una estampa, un material— con su etapa.»

Las tarjetas dicen la etapa en palabras (Pico, Saturada); el color aparece recién en la recomendación de la ficha.

Hacer click en la tarjeta **Amplio** (corte). La ficha dice: K-means **Pico**, recomendación **■ Esperar**.

> «El modelo lo ubicó en Pico: +50 puntos en la búsqueda mundial de 2022 a 2024, frente a las otras búsquedas
> de moda. Con seis meses de lead time llegarías al pico ya pasado: para high fashion, Esperar.»

(Si preguntan por validación: en reseñas de Amazon los amplios suben 79 % entre 2019 y 2022 mientras los
ajustados caen 39 %. Está en Más → El modelo, no en la ficha.)

> «El dato no cambia. Lo que cambia es la recomendación: para fast fashion la misma ficha dice Entrar,
> y para una marca emergente, Salir.»

No cambiar el perfil en vivo: no hay selector en la ficha, y «Cambiar perfil» vuelve a las tres preguntas.
Si se quiere mostrar, tener abiertos de antemano dos links:
`#detalle/amplio?c=fast&v=marca&pu=mujer` (▲ Entrar) y `#detalle/amplio?c=nicho&v=marca&pu=mujer` (▼ Salir).

---

## Paso 3 — Diseñar con este corte (1:10–2:00)

En la ficha de Amplio, tocar el botón azul **Diseñar con este corte · Baggy →**. Entra a Diseñar con el baggy fijo
(«Diseñando con Baggy (corte), desde Tendencias. Sólo te preguntamos lo que falta.») y arranca en el tiro.

> «De mirar a diseñar en un clic: la app ya sabe el corte y pregunta sólo lo que falta.»

En el tiro, señalar las señales en la misma pantalla: tiro bajo ▲ Entrar (prestado del Y2K), tiro medio ○ Sin dato
directo, tiro alto ▼ Salir. Elegir **Tiro bajo** → **Denim rígido** y tocar **Armar la ficha →**. La ficha dice:
**Jean baggy, tiro bajo · ■ Esperar**, con de dónde sale cada dato (medido o prestado).

---

## Paso 4 — Preguntar (2:00–3:00)

Ir a **Preguntar** desde el menú. Arriba aparece el diseño que se armó en el paso 3.
Pegar la API key de Groq en el campo de la izquierda (si no está, la app no llama a nada: abre «Activar el chat» y dice «Primero activá el chat: son tres pasos…»).

> «Este es el único lugar donde entra un modelo de lenguaje.
> Y nunca ve una fila de datos: lee métricas que ya calculamos.»

Escribir: *«Estoy diseñando un jean baggy para una marca high fashion, ¿qué me recomendás para la próxima temporada?»*
o tocar una de las preguntas sugeridas.

Esperar la respuesta (suele tardar 3–5 segundos; con gpt-oss-20b, menos).

> «La respuesta llega marcada como interpretación.
> El dato —la etapa Pico, los +13 puntos del baggy— es nuestro.
> La lectura es del modelo.»

---

## Paso 5 — Buscar por imagen (3:00–3:40)

Ir a **Buscar por imagen** y tocar el look de ejemplo **Denim**. Sólo baja el índice de 8 MB (en la prueba tardó menos
de un segundo); el modelo CLIP de 89 MB baja recién con una foto propia, y la pantalla lo avisa antes.

> «CLIP corre en el navegador: la foto no sale de la computadora. Y dice cuánto acierta: el atributo correcto queda
> entre los tres primeros del 67 al 92 % de las veces.»

---

## Cierre (3:40–4:00)

> «Lo que construimos no predice el futuro. Describe el presente
> con más resolución que «esto está de moda».
> Y es honesto sobre lo que no sabe.»

Mostrar la URL en pantalla: **felipeberney-boop.github.io/ciclo**

---

## Plan B

| Problema | Qué hacer |
|----------|-----------|
| Groq no responde o la key no funciona | Saltar Paso 4. Ir a **Buscar por imagen** en su lugar: subir la foto de prueba, mostrar cómo CLIP identifica el atributo. Decir: «El LLM funciona igual; lo dejamos para que lo prueben ustedes después.» |
| La app no carga (GitHub Pages caído) | Abrir la copia local: `cd app && python3 -m http.server 8000`, usar `localhost:8000`. Tenerla instalada antes. |
| CLIP no devuelve resultado | Usar un look de ejemplo (Trench, Denim…) en vez de una foto propia: sólo baja el índice. Si tampoco anda, mostrar la pantalla de **Método** (Más → Método) en su lugar y recorrer la tabla de qué está medido y qué interpretado. Dura lo mismo y muestra la honestidad del proyecto. |
| Se va el tiempo en Paso 2 | Saltar Paso 3 (Diseñar). Pasar directo a Preguntar o al cierre. |
