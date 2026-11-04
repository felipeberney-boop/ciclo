# CICLO · Racional

**Entrega 4 · 17/11/2026** · *Sistemas generativos e IA para Diseño* (K534/K576), UdeSA · Felipe Berney y Abril Dobler ·
Docentes: Cristian Reynaga e Iván Fardjoume

> **Borrador del 04/11.** Lo armó Claude a partir de los archivos del repositorio y lo tiene que revisar Felipe. Las
> marcas **[a confirmar]** son cosas que el repositorio no alcanza a sostener solo.

App: https://felipeberney-boop.github.io/ciclo/ · Repositorio: https://github.com/felipeberney-boop/ciclo ·
Figma: https://www.figma.com/design/4lvJEf2ZjBX87sXEySXqa7

Este documento no describe la interfaz: explica por qué es así. Cada sección dice de dónde sale lo que afirma, para que
alguien que no cursó pueda seguir el razonamiento y repetirlo.

---

## 1 · El problema y el contexto

**A quién le sirve.** A quien diseña ropa y tiene que comprometer una decisión antes de saber cómo le va a ir: qué
diseñar, qué mandar a producir o si algo que ya hizo sigue vigente. La decisión cambia según el tipo de marca: una de
fast fashion produce en seis semanas y su prenda tiene que leerse actual un año; una marca de autor produce en tres
meses, pero su apuesta tiene que aguantar cinco.

**Qué decisión necesita tomar.** Entrar, esperar o salir de un atributo: un color, una estampa, un corte o un material.
No «una tendencia», que no se puede contar en ningún dataset (`decisiones.md`, 01/09), ni una prenda entera.

**Cómo se decide hoy, con ejemplos reales.** La industria ya decide con informes, tableros y foros, casi todos pagos y
con métodos que no se ven desde afuera:

| Qué usan | Quién lo produce | Qué dice que da | Fuente |
|---|---|---|---|
| **Informes y briefs de tendencia** para comprar | WGSN · *Fashion Buying* (lanzado el 08/08/2024) | «Product direction, the key trends to back next, and how deeply to invest in specific styles»; briefings de materiales, estampas y color, y una proyección de color a dos años | [Comunicado de WGSN](https://wgsn.com/en/wgsn/press/press-releases/wgsn-launches-fashion-buying-dedicated-intelligence-and-forecast-led). La precisión que promete es del vendedor, sin validación pública |
| **Tablero que lee redes con visión por computadora** | Heuritech | Unos tres millones de imágenes de redes por día. Dior lo usó para una nueva versión del bolso Miss Dior, y Rabanne para ver cómo respondía el público a su bolso de 1969 | [Wallpaper, 30/12/2023](https://www.wallpaper.com/fashion-beauty/is-ai-the-future-of-fashion-trend-forecasting) |
| **Tablero de predicción sobre pasarela** | Tagwalk (lanzado en diciembre de 2024) | Colores, materiales y temas hasta un año antes, sobre etiquetas de más de 400.000 imágenes de 1.000 marcas | [Tagwalk](https://www2.tag-walk.com/fr/news/tagwalk-s-trends-prediction-dashboard-part-of-the-time-s-best-inventions-of-2025) |
| **Foros de materiales y color** | Première Vision | Las direcciones de color y tela se arman 18 a 24 meses antes de que la colección llegue a la tienda | [Première Vision](https://www.premierevision.com/articles/78f85898-1079-f111-b337-000d3a3a1397/how-are-premiere-vision-trends-created-) |
| **Tableros de surtido y precio** | EDITED | Surtido, precios, fechas de lanzamiento y tendencias de la competencia | [Harvard D3](https://d3.harvard.edu/platform-rctom/submission/data-driven-dress-dealing/index.html) y los casos de clientes de EDITED (material del vendedor) |
| **El circuito tienda → diseño** | Zara | Los encargados de tienda pasan a diario lo que piden los clientes; el diseño responde en semanas | Ferdows, Lewis y Machuca, «Rapid-Fire Fulfillment», *Harvard Business Review* 82(11), noviembre de 2004 (leído en resúmenes; conviene citar el original) |

**Por qué importa equivocarse.** BoF y McKinsey ponen el inventario en lo más alto de la agenda de la industria para
2025: sobrestock y quiebres de stock a la vez ([resumen del CFDA de *The State of Fashion 2025*](https://cfda.com/resources/sustainability-resource-hub/library-lexicon-annex/the-state-of-fashion-report-2025-mckinsey-company-and-bof-insights/)).
Una lectura de tendencias que se equivoca no queda en un informe: se convierte en prendas que nadie compra.

**El hueco que ocupa CICLO.** Esas herramientas son pagas (un informe de temporada de Tagwalk cuesta entre 2.500 y
6.000 euros según el tamaño de la empresa, según [su página de informes](https://www.tag-walk.com/en/spring-summer-2024-catwalk-report)) y muestran el resultado, no el cálculo. CICLO
trabaja con datos públicos, dice de dónde sale cada número y dice lo que no puede hacer: no predice.

**[a confirmar] Lo que falta para que este punto sea evidencia del negocio y no sólo del mercado.** No hay en el
proyecto una conversación con alguien que diseñe para una marca. Dos o tres entrevistas cortas (¿con qué decidiste tu
última colección? ¿qué mirás? ¿cuánto antes?) cerrarían este punto mejor que cualquier informe.

---

## 2 · La hipótesis, en una frase

> **Cruzando lo que propone la pasarela con lo que busca la gente, se puede ubicar cada atributo de moda en su etapa del
> ciclo y distinguir lo que está subiendo de lo que no; esa lectura coincide con fuentes que el modelo nunca vio.**

**Qué asumimos.** Que la etapa de un atributo se ve en dos capas a la vez: cuánto aparece en los desfiles y cuánto lo
busca la gente. Que «gana terreno» se mide contra las otras búsquedas de moda, no en valores absolutos, porque Google
crece y cambia cómo mide. Que el tipo de marca cambia qué conviene hacer con una misma etapa.

**Qué no podemos afirmar.** Que CICLO prediga: cuatro métodos de predicción no le ganan a repetir el último valor
(`hipotesis.md`). Que la pasarela adelante a la búsqueda: no lo hace ni por año ni por temporada; la prueba por
temporada se registró antes de tener los datos y se rechazó (27/10). Que la búsqueda prediga la venta: contra 5.577
productos con venta real (VISUELLE), explica el 0,1 %. Y que distinga «en retorno» de «saturada»: contra Reddit, no
lo hace (p = 0,88).

**Lo que sí está probado.** Lo que el K-means pone en ascenso o en pico es lo que más crece en Reddit, una fuente que no
usa: p = 0,0013, con el criterio fijado antes de calcular (27/10). El detalle, prueba por prueba, está en `hipotesis.md`.

**De dónde salió.** La hipótesis de la Entrega 1 prometía anticipar: «señales tempranas de los desfiles». Las pruebas
la corrigieron dos veces. La unidad pasó de «tendencia» a atributo, y el foco, de anticipar a leer el presente.

---

## 3 · Los datos y su trazabilidad

**Qué datos, para qué y cómo conviven.** La app lo muestra en un esquema arriba de todo en Método, y en la hoja 12 del
papel:

```
CUATRO FUENTES                      SE CRUZAN POR                  QUÉ SALE
Pasarela · Vogue Runway  ──┐                                    ┌─ La etapa (un lugar en la pista)
Búsqueda · Google Trends ──┼──►  atributo × año  ──► K-means ──┼─ La señal (Entrar / Esperar / Salir)
Redes · Reddit           ··┤     (17 atributos,                 └─ El cono (hasta la ventana, con su error)
Venta y marcas           ··┘      4 rasgos, k = 4)
                         ·· = valida después, no entra al modelo
```

**Las fuentes** (completas, con fechas de descarga y licencias, en `datasets/fuentes_y_descargas.md`):

| Fuente | Quién la produce | Cada cuánto se actualiza | Cubre | Licencia | Limitación |
|---|---|---|---|---|---|
| Vogue Runway (`traopia/vogue-runway`) | Condé Nast; el dataset lo armó un tercero en HuggingFace | No se actualiza: se scrapeó el 31/03/2023 | 1.281.633 imágenes; usamos 902.566 looks de colección, 2000–2023 | Sin licencia declarada; uso académico, sin redistribuir | Después de 2023 no hay dato; las etiquetas las puso un modelo de visión genérico |
| Google Trends | Google | Continua; exportado el 22/09 y el 20–21/10 | 65 series, mundo y 14 términos de Argentina, 2004–2024 | Términos de servicio de Google | Índice relativo, no volumen; salto de medición desde 2025, por eso se corta en 2024 |
| Reddit (Arctic Shift) | Usuarios de r/femalefashionadvice | Continua; consultado el 22/09 y el 13/10 | 4.404 posts que nombran los términos, 2012–2025 | Datos públicos, con atribución | Un solo subreddit, en inglés, sobre todo de mujeres |
| H&M, Amazon, Google Shopping | H&M (Kaggle), Amazon (McAuley Lab), Google | Fijos | 30,6 M de compras 2018–2020; 1,1 M de reseñas 2012–2023 | Kaggle académico; Amazon sin licencia declarada | Validan después; no entran al modelo |
| Lyst Index | Lyst | Trimestral | 34 trimestres, Q1-18 a Q2-26, 55 marcas | Editorial, citado | Cambió la fórmula en Q1-26: se calcula dentro de cada tramo |
| Zara 2018–22 y Mix de marcas | Kaggle | Fijos | 660 y 2.176 productos | Kaggle | **Sintéticos**: sólo muestran el método |

**La clave.** Todo se cruza por **atributo × año**. Cada atributo tiene un nombre de taller («jeans amplios») y, por
cada fuente, el término con el que se lo busca (la etiqueta de Vogue, el término de Google, la palabra en Reddit). Están
en `REC` (`app/index.html`), uno por atributo.

**Las variables que calcula CICLO.** El diccionario de las columnas crudas está en `datasets/diccionario.md`. Estas son
las que salen del cálculo:

| Variable | Qué es | Unidad y rango | Cómo se calcula |
|---|---|---|---|
| Nivel de pasarela (`pn`) | Dónde está hoy contra su propio máximo | 0 a 1 (1 = en su pico) | Proporción de looks con la etiqueta en 2022–23, sobre su máximo histórico |
| Momento de pasarela (`pm`) | Cuánto cambió | Proporción, puede ser negativa | 2021–23 contra 2018–20 |
| Nivel de búsqueda (`bn`) | Igual, en la búsqueda mundial | 0 a 1 | 2023–24 sobre el máximo hasta 2024, con la búsqueda corregida por el crecimiento general de Google |
| Momento de búsqueda (`bm`) | Igual | Proporción | 2023–24 contra 2020–21 |
| Gana o pierde terreno | Cuánto peso ganó dentro de las búsquedas de moda | Puntos, de −31 a +50 en los datos de hoy | Peso del término frente a las otras búsquedas de moda, 2022→2024 |
| Etapa | En qué punto del ciclo está | Una de cinco | K-means (abajo) |
| Ventana | Cuánto tiene que seguir actual la prenda | 1, 2, 3 o 5 años, según la categoría | Supuesto de diseño (`decisiones.md`, 13/10) |
| Error a la ventana | Cuánto se movió de verdad la búsqueda a esa distancia | ±14, ±17, ±21 o ±26 puntos | Error absoluto medio del cono, medido en 224 tramos (`codigo/calcular_cono.py`) |
| Señal | Qué conviene hacer | Entrar, Esperar o Explorar, Salir, Sin dato | Regla fija (abajo) |

**Cómo se construye cada índice.**
- **El K-means.** 17 atributos que existen a la vez en Vogue y en Google Trends (sin calzado). Cuatro rasgos: nivel y
  momento de pasarela y de búsqueda, estandarizados (z-score) para que ninguno pese más por su escala. k = 4, que
  arranca de los centroides guardados para que el resultado sea siempre el mismo. Los grupos se nombran por el
  prototipo de etapa más cercano. Una tendencia nueva se asigna al centroide más cercano y nunca reentrena el modelo:
  hacerlo convertía a cada tendencia nueva en su propio grupo y les cambiaba el nombre a los demás (22/09). Con la
  búsqueda hasta 2024, la silhouette ya no prefiere k = 4 (0,373 contra 0,387 con k = 2); nos quedamos con 4 porque
  con menos grupos las etapas no se separan, y la pantalla del modelo lo dice (20/10).
- **La señal.** Si el atributo tiene etapa del K-means, decide la regla de CICLO para la categoría (`CONSEJO`): con un
  atributo en pico, fast fashion entra y una marca de autor sale. Si no tiene etapa pero tiene serie, decide si gana o
  pierde terreno (más de 3 puntos). Si no tiene nada, queda sin dato: es neutro, porque «no tengo datos» no es lo
  mismo que «está cayendo». Si la decisión es «qué diseñar», donde la regla dice Esperar dice Explorar.
- **El cono.** Desde el último dato bueno, cada curva sigue la mediana de lo que pasó en la historia a esa distancia,
  con una banda donde cayó el 60 % y el 90 % de los casos. No es un pronóstico: en las pruebas empata con repetir el
  último valor en la pasarela (20,9 contra 20,9) y apenas mejora en la búsqueda (11,4 contra 12,6), y por eso la
  pantalla lo dice (13/10).

**Cómo se interpretan los colores.** El color dice una sola cosa: si conviene avanzar o frenar. Verde es Entrar, ámbar
es Esperar o Explorar, rojo es Salir, siempre con la palabra y un ícono (▲ ■ ▼), y lo que no tiene dato queda en gris.
La etapa no tiene color: es una posición en la pista. De dónde sale un dato tampoco tiene color: ● medido, ◇
interpretado, ↪ prestado de un pariente. El azul significa sólo «se puede tocar». Los grupos del K-means usan tonos que
no se confunden con la señal.

**El repositorio.** Decisiones fechadas en `decisiones.md`, versiones en `historial.md`, fuentes en
`datasets/fuentes_y_descargas.md`, diccionario en `datasets/diccionario.md`, prompts versionados en `prompts/`. Los
datos crudos no están (pesan demasiado o necesitan cuenta); están los links y lo calculado.

---

## 4 · El modelo: qué entra, qué se calcula, qué sale

```
ENTRA                                   SE CALCULA                                  SALE
Pasarela por atributo y año  ─┐         nivel y momento (4 rasgos)                  la etapa
Búsqueda por atributo y año  ─┼──────►  z-score → K-means k=4 → nombre de etapa ──► la señal, con la categoría
Tu perfil (decisión,          │         regla CONSEJO × categoría × decisión        el cono, con el error a tu ventana
  público, categoría)        ─┘         mediana histórica a h años
Una foto (opcional)          ────────►  CLIP: parecido con 14.000 looks            atributos que ve y looks parecidos
Una pregunta (opcional)      ────────►  LLM con métricas ya calculadas             una lectura marcada ◇ interpretación
```

**La IA, dónde entra y dónde no.** CLIP (ViT-B/32) lee imágenes: etiquetó la pasarela y, en el navegador, compara la
foto que sube la persona con 14.000 looks; acierta el atributo entre los tres primeros entre el 67 % y el 92 % de las
veces según el atributo, en 150.000 looks que no vio. El modelo de lenguaje (Groq, `gpt-oss-120b`) **nunca ve una fila
de datos**: recibe métricas ya calculadas y las traduce, y lo que dice aparece marcado como interpretación. La etapa y
la señal no las decide la IA: las deciden el K-means y una regla fija.

**Qué quedó afuera y por qué.**
- **La predicción.** Se probó de cuatro maneras y con un modelo global; ninguna le gana a repetir el último valor.
- **2025 y 2026 en la búsqueda.** Google cambió la medición: en 2025, 15 de 16 series suben y 12 tocan su máximo.
- **El calzado.** Dos de ocho estilos tienen señal en la búsqueda; CLIP lee la ropa, no el zapato. Está contado como
  resultado, no escondido (26/10).
- **Pasarela y venta por género.** Vogue y los agregados de H&M no traen esa columna; está declarado en Método.
- **Lo emergente.** Ningún atributo del set está empezando: haría falta pasarela posterior a 2023.

---

## 5 · El usuario y el flujo

**El perfil.** En la Entrega 1 la cátedra pidió que dejara de ser genérico; pasó a ser una forecaster independiente
que asesora a varias marcas. Desde el 13/10 es quien diseña, porque la app dejó de mostrar todo y pasó a acompañar una
decisión de diseño.

**El recorrido.** Tres preguntas → Tendencias o Diseñar → la ficha de un atributo → «Diseñar con…» → Preguntar. Está
paso a paso, con capturas, en el readme, y en papel, una pantalla por hoja, en
`entregas/entrega_4/disenos_en_papel/`.

**Por qué la ramificación es así.** La primera versión preguntaba «¿trabajás para una marca o por tu cuenta?». La
devolución de la Entrega 3 marcó que eso pregunta por el vínculo laboral, no por lo que la persona vino a hacer. Al
mirar qué cambiaba de verdad en la lectura, el vínculo movía una sola cosa: Esperar pasaba a Explorar porque «no
comprometés stock». Eso no depende de dónde trabajás, sino de en qué punto de la decisión estás. Se evaluaron tres
variantes (`decisiones.md`, 04/11):

| Variante | La pregunta | Por qué no o por qué sí |
|---|---|---|
| El alcance | Una colección · Una prenda · Si algo sigue vigente | Colección o prenda no cambia ningún número: habría que inventar ventanas |
| **El compromiso** | **Qué diseñar · Qué producir · Si algo ya pasó** | **Elegida.** Es el objetivo de la persona, conserva todo lo que la lectura usa y agrega mirar hacia atrás |
| El plazo | ¿Para cuándo en tienda? · ¿Cuánto tiene que durar? | Da la ventana directo, pero pierde el posicionamiento y obliga a reescribir las reglas |

**La categoría se queda**, y esto no era obvio: se pensó que el lead time la podía reemplazar. No puede. La categoría
lleva dos cosas que el lead time no tiene: la ventana (de la que depende el error medido, porque los lead times son
todos menores a un año y el error se mide año a año) y el posicionamiento (en pico, fast fashion entra y una marca de
autor sale, aunque la de autor tenga un lead time más corto que high fashion).

Cada respuesta lleva a un lugar distinto: Qué diseñar entra a Diseñar; Qué producir, a Tendencias; Si algo ya pasó, a
Tendencias con la pregunta «¿Sigue vigente?» y lo que ya hay que dejar primero.

---

## 6 · Las decisiones de diseño

**Lo más importante de cada pantalla.**

| Pantalla | Lo primero que se ve | Por qué |
|---|---|---|
| La entrada | Una pregunta y sus opciones, nada más | Cada respuesta cambia la lectura; lo que cambia está en Método |
| Tendencias | Qué gana y qué pierde terreno, en el único bloque oscuro | Es lo que se mueve hoy, medido; después, cada atributo con su etapa y su señal |
| La ficha | La señal grande, con una línea de por qué | Es la decisión. El gráfico la sostiene; el detalle está en el «?» |
| Diseñar | La pregunta del paso | Un paso, una decisión; lo elegido queda en una barra abajo |
| Método | El esquema de los datos | La devolución lo marcó como fundamental |

**Cómo se jerarquizó.** Tres grupos para cada bloque de texto: lo que se necesita para decidir se queda; lo que aclara
cómo usar la app pasa a un «?» que se abre si lo tocan; lo que no aporta se borra (`decisiones.md`, 04/11).

**Tipografía.** Había 31 tamaños de letra y 49 combinaciones de tamaño y peso (medido). Quedan cinco, con un peso por
tamaño: Título 48, Subtítulo 24 y Dato 34 en Semi Bold; Cuerpo 17 y Etiqueta 13 en Regular. Es la tipografía del
sistema (SF Pro en Apple, Inter en el resto), porque la referencia que pasó la cátedra (el sistema de diseño de Apple)
hace que la interfaz se corra y la ropa hable. Cinco estilos hacen que el tamaño signifique algo: si es grande, decide.

**Color.** El de las prendas, que es el dato que la persona vino a ver; la señal, con su palabra; y un solo azul para lo
que se toca. Nada más tiene color, y por eso la señal se ve.

**Grilla.** El contenido va hasta 1.360 px, con un margen que va de 16 px en el celular a 80 px en la compu, y las
tarjetas se acomodan solas, de 268 px como mínimo. En el celular todo va en una columna y los gráficos anchos se
deslizan. **[a confirmar]** No hay una grilla de columnas escrita: es la que resultó del código y hay que decidir si se
fija.

---

## 7 · El recorte de alcance

Ropa, no calzado ni accesorios (sin señal medible). Leer el presente, no predecir (refutado). Mundo y Argentina sólo en
la búsqueda (no hay pasarela local). Sin separar por género (las fuentes no lo traen). **[a confirmar]** Si se acepta la
propuesta del 04/11, también El modelo pasa a Método, Retornos entra en El ciclo y Marcas sale del menú.

---

## 8 · El proceso y el uso de IA

**[a confirmar] Los bocetos previos.** La consigna pide bocetos anteriores a cualquier interacción con la IA. El material
humano más temprano que tiene el proyecto, con fecha, es la **presentación de la Entrega 1 (25/08/2026)**, en Figma
Slides (https://www.figma.com/slides/naASEKNbarWxFM4GKZFUuY): la pregunta, la hipótesis, el perfil de usuario, los
datasets y los referentes (Pinterest, Google Trends, Spotify). No tiene pantallas. Las propuestas de pantalla del
13/10 (`diseno/prototipos/prototipo_felipe_1/` y `prototipo_abril_1/`) son posteriores a la app, que ya estaba escrita
con Claude Code, y la de Abril se generó con IA de imágenes. *Si hay bocetos a mano anteriores, van acá con su fecha.*

**Las etapas.**

| Fecha | Qué | Hecho por **[a confirmar]** |
|---|---|---|
| 25/08 | Entrega 1: pregunta, hipótesis, usuario, datasets, referentes | El grupo |
| 01/09 → 23/09 | La unidad pasa a ser el atributo; los datasets iniciales resultan sintéticos; K-means con k = 4 | El grupo, con Claude en el análisis |
| 05/10 | Entrega 2: prototipo navegable en Figma y láminas | El grupo; las láminas, con un script |
| 06/10 → 03/11 | La app, en código, con Claude Code; las devoluciones de la cátedra la cambian tres veces (13/10, 27/10, 03/11) | Decisiones del grupo, código con Claude |
| 03/11 | Del diseño al código, en un Figma de tres etapas | El grupo, con el MCP de Figma |
| 04/11 | La entrada por la decisión, el papel, cinco estilos de texto, la curaduría | Decisiones de Felipe sobre propuestas de Claude |

**Qué propuso la IA, qué decidimos y por qué.** **[a confirmar fila por fila]**

| Tema | La IA propuso | Lo que decidimos | Por qué |
|---|---|---|---|
| Mom y boyfriend | Contarlos como cortes amplios | Sacarlos de los cortes: son tiro alto y pierna tapered | Un corte es una silueta, no un nombre comercial (23/09, 20/10) |
| El calzado | Medirlo como la ropa | Primero afuera; después dos pruebas; contado como resultado | Lo que no se mide se dice, no se esconde (20/10, 21/10, 25/10, 26/10) |
| El estilo visual | Revista, revista suave, estudio | Ninguna: «el profe sigue diciendo que es muy IA». La referencia de Iván | Tres variantes no convencieron (27/10) |
| El semáforo | Color por tendencia; salmón para la IA | Tres correcciones: el color es sólo la señal, la tendencia en negro, siempre con la palabra | El color tiene que decir una sola cosa (20/10, 26/10, 27/10) |
| La portada | Un menú de texto | Afuera: la app abre en las preguntas | No llevaba a ninguna decisión (26/10) |
| La ramificación | Tres variantes; recomendó «el compromiso» | Esa, con «Si algo ya pasó» en vez de «Si algo sigue vigente» | Más corta, y dice que mira hacia atrás (04/11) |
| Las pantallas de «Más» | El modelo a Método, Retornos en El ciclo, Marcas fuera del menú | Pendiente | — |

**Qué modelos usamos.**

| Para qué | Modelo |
|---|---|
| Escribir el código, analizar los datos, redactar | Claude, en Claude Code |
| Leer imágenes: etiquetar la pasarela y Buscar por imagen | CLIP ViT-B/32 (en el navegador, sin servidor) |
| Preguntar y la lectura en vivo | Groq, `openai/gpt-oss-120b` (antes Llama, hasta que Groq lo dio de baja) |
| Propuestas de pantalla del 13/10 (Abril) | La herramienta integrada de imágenes (prompts en `prototipo_abril_1/prompts.md`) |
| Figma: el sistema implementado y el papel | El MCP de Figma |

**Cómo gestionamos el system prompt.** Cada prompt vive en `prompts/` con su versión. Nunca se pisa una versión: si
cambia, se agrega la siguiente con qué cambió y por qué (la lectura va por la v5, Preguntar por la v6). La regla que los
atraviesa a todos es que el modelo no ve una fila de datos: los datos que recibe se generan con
`codigo/armar_datos_llm.js` a partir de la app, y van sólo las fichas que nombra la pregunta. Las claves no están en el
repositorio: cada persona pega la suya y queda en su navegador.

**La pirueta: «Adiviná vos».** En «Más» y desde el cono, en Método. La persona dibuja cómo sigue una curva real de
búsqueda desde 2019 y la compara con lo que pasó, con el cono de CICLO y con repetir el último valor. En las 65 series,
el último valor gana 45 a 18. El LLM no juega: tendría que ver la serie, y en CICLO no ve filas de datos
(`decisiones.md`, 04/11).

**Dónde frenamos a la IA.** No decide la etapa ni la señal. No inventa respuestas en las capturas: Preguntar se muestra
vacío. No predice: el cono dice «no es un pronóstico». Y no es la autora de las decisiones: propone variantes, y la
elección, con su porqué, queda registrada.
