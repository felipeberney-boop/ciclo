# Decisiones

Registro fechado de lo que probamos, lo que descartamos y por qué.

---

## 2026-08-25 · Entrega 1

Hipótesis original: «Al cruzar señales tempranas provenientes de los desfiles con el crecimiento de
búsquedas online y datos históricos de consumo, sería posible identificar en qué etapa de su ciclo se
encuentra una tendencia».

Aprobada con 7,4. Lo que pidió la devolución y fuimos incorporando:

- La usuaria tenía que dejar de ser genérica: pasó a ser una forecaster independiente multi-cliente.
- Ida y vuelta con imágenes de prendas (hoy es la pantalla de Consulta, IA-6).
- Rastrear fast fashion contra marcas grandes.
- Referentes de UX menos obvios (Tagwalk).

## 2026-09-01 · La unidad de análisis

**Problema.** «Tendencia» no se puede contar. No hay una columna «tendencia» en ningún dataset.

**Decisión.** La unidad de análisis pasa a ser el **atributo**: un color, una estampa, un corte, un
material. Es lo único que aparece a la vez en la pasarela, en la búsqueda y en el catálogo.

## 2026-09-08 · Los tres datasets iniciales son sintéticos

**Qué probamos.** K-means y árboles de decisión sobre Zara 2018–22 (660 productos) y Mix de marcas 2025
(2.176 productos).

**Qué encontramos.** Correlación máxima entre variables numéricas: 0,099 en Zara y 0,018 en Mix. El
75,4 % del Mix comparte la misma fecha. El árbol de decisión predice al 50,8 % contra una base de 50,2 %:
no predice nada.

**Decisión.** Los dos quedan como demostración de método, no como fuente de conclusiones. Hay que salir
a buscar datos reales. Queda declarado en la pantalla de Método.

## 2026-09-15 · Reformulación de la hipótesis

**Hallazgo.** En Zara 2018–22 los atributos no varían por año (estampa×año p=0,37) pero sí por mes y muy
fuerte (estampa×mes chi²=832,9, p≈1,8e-139). Las estampas de nicho aparecen en un solo mes y se repiten
los cinco años: rayas solo en octubre, corazones solo en febrero, floral solo en junio.

**Decisión.** La huella del ciclo está en la **estructura del catálogo** —amplitud de paleta, aparición
de la versión barata, liquidación transversal— y se lee en un solo corte, sin serie temporal. Métrica
nueva: «meses con presencia sobre 60», el gemelo temporal de «cuántos colores tolera».

## 2026-09-15 · Las capas que faltaban

**Pasarela: resuelta.** `traopia/vogue-runway` en HuggingFace. 1,28 M de imágenes con diseñador,
temporada, año, ciudad y tags. El parquet de metadata pesa 99 MB, sin imágenes.

**Redes: parcialmente.** No existe dataset público con eje temporal. La armamos con Reddit vía Arctic
Shift (Pushshift está muerto). Pinterest y TikTok piden sesión iniciada.

**Instagram: descartado.** No existe serie histórica de hashtags a ningún precio. Sacaron la pestaña
cronológica en 2022 y limitaron a 5 hashtags por post en diciembre de 2025: el volumen de hashtag es
una señal que se degrada sola. Es un resultado negativo documentado.

**También descartados:** TikTok Research API (requiere institución en EE.UU./EEE/UK/Canadá/Suiza/Brasil,
Argentina no califica), Pinterest Trends API (solo agencias y Enterprise), pytrends (archivada en abril 2025).

## 2026-09-22 · La deriva de Google Trends

**Problema.** 33 de los 35 términos del mundo tocan su máximo histórico en el mismo mes: abril de 2026.
Incluso búsquedas sin relación entre sí. Sin corregirlo, todo parece estar en su pico.

**Decisión.** Es un salto en la medición de Google, no en la moda. Se detrenda cada término por la media
de los 35 de ese año y se excluye enero–septiembre de 2026 entero.

## 2026-09-22 · El modelo: por qué K-means y por qué k=4

**Qué probamos.** Regresión lineal, árbol de decisión y K-means, los tres modelos que vimos en clase.

**Por qué K-means.** No tenemos etiquetas de etapa. Etiquetarlas a mano sería contestar la pregunta
antes de hacerla. El no supervisado agrupa lo que se mueve parecido y recién después nosotros leemos.

**Por qué k=4.** Silhouette entre k=2 y k=5: 0,303 / 0,323 / **0,326** / 0,316. Con k=6 sube a 0,336 pero
aparecen grupos de uno o dos atributos que no se leen como etapa.

**Un error que corregimos.** Al agregar una tendencia nueva, el modelo se reentrenaba y la tendencia
nueva se volvía su propio grupo, cambiando los nombres de todos los demás. Ahora se entrena sobre las
filas base y las nuevas se asignan al centroide más cercano.

## 2026-09-23 · Los jeans por corte

**Problema.** Teníamos «denim», «mom jeans» y «ajustado» mezclados como si fueran la misma clase de cosa.

**Decisión.** Se agrupan por corte: **amplios** (baggy, wide leg, barrel, mom, slouchy), **medios**
(recto, bootcut, flare, tapered) y **ajustados** (skinny, slim, pitillo). Mom jeans no es un corte: es un
jean amplio, y se absorbe ahí.

**Lo que mostró el cambio.** Los ajustados eran el 73 % de la búsqueda de jeans en 2012; los amplios los
pasan en 2021; en 2025 es 55 / 22 / 23. Agregado como «denim» no se ve nada, porque las curvas se
cancelan. El K-means los separa: amplios y medios en pico, ajustados en saturada.

**Límite que apareció.** Vogue etiqueta «denim» y nada más: la pasarela no distingue cortes, así que
para los jeans el retraso entre capas no se puede medir corte por corte. Queda declarado en la ficha.

## 2026-09-23 · Contraste externo con Lyst

**Qué hicimos.** Cargamos 19 señales del informe anual de Lyst, con su porcentaje y su URL. No entraron
al modelo: se usan después, como un jurado que no vio nuestras cuentas.

**Resultado.** Coincide donde el modelo se la juega: +55 % en jeans anchos (2024), +56 % en cargo (2022),
+74 % en corset (2021) caen en los grupos que llamamos pico y ascenso.

**Lo que no usamos.** Las columnas de atributo de ese archivo son anotaciones de período repetidas en las
20 filas de cada marca, y los blancos significan «no relevado», no cero. Lo dice el propio README del
dataset. Sirve para contrastar una lectura; no para entrenar un clasificador.

**Dónde no coincide.** Lyst ve ballerinas (+75 %) y UGG Ultra Mini (+358 %) disparadas. Nosotros no
medimos calzado. Es el agujero más concreto que tenemos.

## 2026-10-05 · Entrega 2 · el prototipo

**Decisión de color.** El salmón que el grupo ya usaba como acento pasa a ser **el color de la IA**: lo
negro es medido, lo salmón es calculado o interpretado por un modelo. La misma regla rige adentro de la
app y adentro de la presentación.

**Baja contra alta fidelidad.** La consigna pedía baja fidelidad. Empezamos con wireframes esquemáticos
y los reemplazamos por pantallas con los gráficos dibujados a partir de los datos reales. El criterio:
un esquema decide qué información entra en cada pantalla; una pantalla real permite además discutir si
el dato se entiende.

**Mobile.** Se hizo una versión de teléfono que no es la de escritorio achicada: siete secciones en una
barra horizontal pasan a cinco pestañas abajo, las fichas van a una columna, y en Consulta los botones
son Cámara y Galería porque en un teléfono arrastrar un archivo no existe. El bump de Lyst bajó de seis
marcas a cuatro, porque a 306 píxeles de ancho seis líneas dejan de leerse.

## 2026-10-06 · Repositorio

Se arma el repositorio con la estructura de la cátedra. Los datasets originales no se suben: superan el
límite de GitHub o requieren cuenta. Van los links de descarga y la fecha en
`datasets/fuentes_y_descargas.md`.

## 2026-10-13 · Completar las fuentes hasta hoy

**Problema.** La pasarela termina en 2023 y Reddit en 2025. Varias capas no llegan a la fecha.

**Reddit: completado con dato real.** Bajamos los títulos de enero a octubre de 2026 de Arctic Shift. Para
empalmar con la serie probamos tres reglas de suavizado contra los valores del repo 2022–2025: la media
móvil centrada de 3 años los reproduce con 2,4 % de error mediano (hacia atrás: 17,5 %; sin suavizar:
37,2 %). Con esa regla, 2024 recalculado difiere 1,6 %. Corset, hoodie e Y2K marcan récord en 2026, con más
de 20 posts cada uno. Las caídas más grandes (cargo, crop top, chunky sneakers) son de términos con menos de
10 posts en el año: no alcanzan para leerse como tendencia, y lo dejamos dicho.

**Pasarela: proyectada, y lo decimos.** No existe dato público de looks etiquetados 2024–2026. Elegimos
el método por backtest entre 21 candidatos: ganó Holt amortiguado con 20,1 puntos de error sobre 100,
contra 20,9 de repetir el último año. Casi no mejora a no hacer nada. Queda como curva punteada con su
banda y **no entra al K-means**: clasificar con un número que el propio backtest no sostiene sería
contestar la pregunta con lo que no sabemos.

**Lo que no se completó.** H&M y Amazon no tienen ediciones más nuevas, y en el repo sólo hay sus métricas
resumidas: proyectarlos sería inventar. Google Trends 2026 sigue excluido por la deriva de abril. Lyst ya
llega a Q2-26.

Detalle y archivos: `datasets/completado_2026/`.

## 2026-10-13 · La consulta por imagen pasa a ser real

**Antes.** La pantalla de Consulta mostraba un resultado fijo (una campera de cuero dibujada).

**Ahora.** CLIP ViT-B/32 corre en el navegador: la foto no sale de la computadora. Hace dos cosas.
Clasifica la imagen contra los 18 atributos del K-means (zero-shot) y busca los looks más parecidos entre
14.000 looks reales de Vogue, usando los embeddings que ya trae el dataset.

**Por qué CLIP y no entrenar un clasificador.** No tenemos fotos etiquetadas por atributo propias, y las
etiquetas de Vogue sólo cubren 10 de los 18. CLIP no necesita entrenamiento y comparte espacio con los
embeddings del dataset: 25 de 25 fotos se encontraron a sí mismas en el primer puesto.

**Cuánto acierta.** Validado contra las etiquetas de Vogue en 150.000 looks: AUC mediano 0,90; el atributo
correcto queda entre los tres primeros entre el 67 % y el 92 % de las veces. Animal print es el punto débil
(20 %). Los seis atributos que Vogue no etiqueta quedan marcados «sin validar» en la interfaz.

**Ejemplos sin elegir a mano.** Los botones de ejemplo usan el primer look del índice con cada etiqueta, aunque
el resultado no sea el esperado (el de cuero da encaje primero).

Detalle: `prompts/prompt_consulta_por_imagen_v2.md`.

## 2026-10-13 · Links compartibles

**Problema.** La app no cambiaba la dirección al navegar: no había forma de mandarle a un cliente el link a
un atributo puntual, y el botón «Atrás» del navegador salía de la app.

**Decisión.** Cada pantalla tiene su dirección: `#recorridos/cargo`, `#detalle/floral`, `#consulta`. El
cliente va como `?c=fast` o `?c=nicho` (premium es el valor por defecto y no se escribe). Cambiar de pantalla
crea una entrada en el historial; cambiar de atributo o de cliente actualiza la dirección sin crearla, para que
«Atrás» vuelva a la pantalla anterior y no recorra cada clic. Botón «Copiar link» en la barra del cliente.

## 2026-10-13 · Entrada en dos pasos: vínculo y categoría

**Devolución del profesor.** Antes de elegir el tipo de cliente hay que separar si quien diseña trabaja en
relación de dependencia o por su cuenta, porque cambia cómo lee la misma tendencia.

**Decisión.** Paso 1: «Trabajo para una marca» / «Trabajo por mi cuenta». Paso 2: tres categorías (high
fashion, fast fashion, nicho), con la pregunta y el texto según la rama. Se reusan las claves del modelo
(`premium`, `fast`, `nicho`), así que `CONSEJO` y los gráficos no cambian.

**Por qué el vínculo no mueve la lectura de la etapa.** El lead time y en qué etapa conviene entrar los fija
la categoría: dependen de cuánto tarda en llegar la prenda a la tienda, no de quién firma el contrato. Lo que
cambia el vínculo es el riesgo: quien trabaja por su cuenta no compromete producción ni stock, así que donde
a una marca le conviene «Esperar», a esa persona le conviene «Explorar» —empezar a diseñar sin comprometer
la serie—. Las demás acciones no cambian. Está implementado como una capa sobre `CONSEJO`, sin duplicar la
tabla. También cambia el tratamiento: «tu marca» o «tu cliente».

**Lo que no se mostró.** El pedido original incluía, en cada tarjeta, ventana, fecha límite de decisión y
error medido por categoría. Esta versión de la app no tiene esa validación, así que las tarjetas muestran
sólo lo que sí está: el lead time y las acciones de `CONSEJO` por etapa.

**De paso.** «Premium» pasa a llamarse «High fashion» en la barra, para usar el término de industria. Se
corrigió un error previo: el detalle de cuero no abría porque buscaba «Campera de cuero» en el modelo, donde
se llama «Cuero».

## 2026-10-13 · Gráficos legibles y hasta 2030

**Devolución del profesor.** La interfaz y los gráficos se ven caóticos: no se puede seguir una línea, hay
demasiados puntos, y el gráfico termina en 2026 cuando lo que quiere ver quien diseña es hacia dónde va.

**Hasta 2030, sin prometer el futuro.** Cada curva sigue con «lo habitual»: el último valor medido más el
cambio mediano histórico de su capa a esa distancia, con el rango real. Probado: no le gana a repetir el último
valor (pasarela 20,9 contra 20,9; búsqueda 11,4 contra 12,6). Por eso la leyenda dice «no es un pronóstico» y
las líneas quedan casi paralelas: a todas se les aplica el mismo movimiento mediano, y abrirlas sería dibujar
una divergencia que los datos no muestran. Reemplaza en la app a la proyección de Holt de pasarela, para que
las cuatro capas usen el mismo criterio.

**Cómo se separan las líneas sin inventar.** Etiqueta directa al final de cada línea (nombre y valor en 2030,
separadas al menos 14 px); un guión por capa, el mismo en el tramo medido y en el habitual; halo del color del
fondo en los cruces; clic o teclado en la leyenda para aislar una capa (las demás quedan al 15 %) y ver su
rango; medido 2,4 px, habitual 2 px, bandas al 5 % y 9 % sólo en la capa aislada. Se sacaron los puntos de pico
(están en el panel de al lado) y el tramo punteado de pasarela anterior a 2010. En teléfono, un gráfico chico
por capa.

**Código visual común.** Llena = medido · punteada = lo habitual · punto hueco = año incompleto · tenue = poco
dato o estimado. La curva de cascada del detalle, que es estimada, dejó de ser punteada y pasó a tenue.

**Tu prenda en tienda.** Una línea vertical en hoy + el lead time de la categoría. Se mueve poco (de noviembre
de 2026 a abril de 2027) porque los lead times son de semanas o meses; el pedido original hablaba de ventanas
de 2026, 2028 y 2030 por categoría, pero esa validación no existe en esta versión y no se inventó.

## 2026-10-13 · Verificación de licencias

**Qué hicimos.** Fuimos a la ficha de cada una de las cuatro fuentes que teníamos marcadas
«a verificar» desde septiembre.

**Qué encontramos.** Tres de las cuatro **no declaran licencia alguna**:

| Fuente | Resultado |
|---|---|
| Vogue Runway (`traopia/vogue-runway`) | Sin licencia. La ficha dice «scraped from Vogue on 2023-03-31», importado del Internet Archive, con las imágenes apuntando a servidores de Condé Nast |
| Amazon Reviews | Sin licencia; única condición, citar a Hou et al. (2024), arXiv:2403.03952 |
| Wish 2020 (Kaggle, jmmvutu) | Sin licencia, sin autor nombrado y sin procedencia declarada |
| Zara febrero 2024 (Kaggle) | No verificable: falta la URL exacta del dataset |

**La lectura.** «Sin licencia declarada» no es lo mismo que libre: es lo contrario. Nadie otorgó
permiso explícito, y en el caso de Vogue el contenido de origen es editorial de Condé Nast.

**Decisión.** Se declara tal cual en el readme y en `fuentes_y_descargas.md`, en vez de inventar una
licencia o dejar «a verificar» indefinidamente. En la práctica: uso académico, sin redistribuir
ningún dataset, citando cada fuente. Es la misma política que ya veníamos aplicando —los pesados no
se suben al repositorio— pero ahora está fundamentada.

**Pendiente concreto.** Quien bajó el dataset de Zara de febrero 2024 tiene que pegar la URL de
Kaggle en `fuentes_y_descargas.md` y repetir la verificación. Es la última que falta.

## 2026-10-13 · El Zara de febrero 2024 es el cuarto dataset sintético

**Qué probamos.** Al llegar el archivo lo testeamos como a los tres anteriores.

**Qué encontramos.** La columna `Sales Volume` no son ventas:

- correlación con el precio: **−0,07**
- media con promoción 1.827, sin promoción **1.821** — seis unidades de diferencia sobre 1.824
- desvío observado 696 contra 710, que es el de una uniforme sobre el mismo rango
- los diez deciles con la misma cantidad de productos

Las ventas reales de retail son muy asimétricas: unos pocos productos se llevan casi todo. Esto es
plano. `Promotion`, `Seasonal` y `Product Position` se reparten casi 50/50 o en tercios, como se
esperaría de columnas generadas al azar.

**Lo que sí es real** es lo scrapeado: `name`, `description`, `price`, `url`, `sku`, `terms`,
`section` y la fecha. Las descripciones son copy auténtico de Zara, y es exactamente la parte que
usamos para contar proporciones. O sea que el uso que le veníamos dando está bien; lo que hay que
no hacer es tocar las columnas de venta.

**Dos cosas que no sabíamos del archivo.** Es **86 % menswear** (218 contra 34), el desbalance
opuesto al que suponíamos para el resto del corpus. Y trae **31 productos de calzado**, todos de
hombre: es lo único de calzado que tenemos, y el calzado era el agujero declarado frente a Lyst.

## 2026-10-13 · Tres intentos de salvar la predicción, y un casi-hallazgo que no era

Después de que los cuatro métodos fallaran, probamos tres caminos distintos.

### 1 · Un modelo global en vez de uno por serie

**Qué es.** En vez de ajustar una curva por atributo, se entrena **una sola regla** sobre las 16
series juntas: dado el recorrido de los últimos 5 años, cuánto se mueve en los próximos h. Validado
dejando afuera la serie que se evalúa. Es la técnica por la que un panel más grande serviría.

**Resultado.** Tampoco le gana a repetir el último valor: −2,0 % a un año, +0,4 % a dos, −2,6 % a
tres, −5,8 % a cinco.

**Qué significa.** El problema no es que tengamos pocas series. Sumar los 19 términos que faltan no
iba a salvarlo, así que no vale la pena ir a buscarlos para esto.

### 2 · Predecir algo que no sea búsqueda

**Qué probamos.** Contra las dos únicas señales comerciales que tenemos por atributo: el cambio en
reseñas de Amazon 2019-2022 y el de Google Shopping 2022-2025.

| Predictor | Amazon (n=11) | Shopping (n=12) |
|---|---|---|
| Nivel de búsqueda | +0,13 | **+0,61** |
| Momento de búsqueda | −0,09 | +0,41 |
| Nivel de pasarela | −0,56 | **+0,67** |
| Momento de pasarela | −0,55 | +0,30 |

Con esos tamaños de muestra hace falta |r| > 0,6 para decir algo. Contra Amazon **no hay nada**.
Contra Shopping el nivel de búsqueda y el de pasarela pasan raspando.

**El límite honesto:** Google Shopping sigue siendo búsqueda, no venta. Que la búsqueda prediga la
búsqueda comercial no sorprende a nadie. Nos falta una serie de ventas de verdad.

### 3 · ¿La pasarela adelanta? El casi-hallazgo

**Qué hicimos.** Rehacer el test de la H5 **atributo por atributo** en vez de promediado, porque el
promedio puede tapar que adelante en unos y no en otros.

**Lo que apareció.** En niveles, espectacular: **7 de 13 atributos** con su correlación máxima en
rezago 3 o 4 años — jeans amplios +0,97, jeans medios +0,95, trench +0,93, buzo +0,89, cargo +0,82.
Parecía que la H5 se salvaba con un adelanto de cuatro años.

**Por qué no lo es.** Dos series que suben correlacionan alto aunque no tengan nada que ver. Al
repetir el test sobre los **cambios año a año** en vez de los niveles, se desarma: de 13 atributos
sólo **cargo** (k=2, r=+0,75) y **capa** (k=4, r=+0,74) superan el umbral. Y con 13 atributos por 5
rezagos son **65 pruebas**: por puro azar se esperan unas 3 que pasen. Dos no es más de lo que da
tirar una moneda.

**Decisión.** La H5 sigue rechazada a escala anual. Dejamos documentado el casi-hallazgo porque es
exactamente la clase de resultado que uno quiere creer, y el detrend es lo que lo descarta.

### Lo que sí falta, y es concreto

**VISUELLE** (github.com/HumaticsLAB/GTM-Transformer) tiene 5.577 productos de Nunalie 2016-2019 con
**ventas semanales y Google Trends ya alineados**. Es exactamente la serie de ventas que nos falta, y
ya lo teníamos identificado desde septiembre sin usarlo. Se baja llenando un formulario:
https://forms.gle/cVGQAmxhHf7eRJ937 — lo tiene que completar alguien del grupo. El repositorio es
MIT, pero la licencia del dataset no figura: hay que leerla en el formulario o en el paper
(arXiv:2109.09824).

## 2026-10-13 · La prueba contra ventas reales: VISUELLE

Conseguimos el dataset que nos faltaba y pudimos correr, por primera vez, la pregunta que el
proyecto siempre quiso contestar: **¿la búsqueda predice la venta?** Hasta ahora predecíamos
búsqueda con búsqueda, que es un proxy.

**Los datos.** VISUELLE: 5.577 productos de Nunalie con sus **ventas semanales reales** (12 semanas
desde la salida de cada uno) y 219 semanas de Google Trends para 96 términos —categorías, colores y
tejidos—, ya alineadas. Temporadas SS17 a AW19.

**El diseño.** Los predictores salen de la búsqueda del atributo **en las 12 semanas anteriores** a
la salida del producto, nunca de las posteriores. Se entrena con SS17–AW18 y se prueba con SS19 y
AW19. La base a vencer es «predecí el promedio de la categoría», que es lo que haría cualquiera sin
modelo.

### A nivel producto: no predice nada

| Predictor | r | n |
|---|---|---|
| Nivel de búsqueda de la categoría | **+0,036** | 5.577 |
| Pendiente de búsqueda de la categoría | +0,009 | 5.577 |
| Nivel de búsqueda del color | −0,121 | 5.577 |

Con 5.577 productos el umbral de significancia es 0,026, así que +0,036 «da significativo». Y no
sirve para nada: explica el **0,1 % de la variación** de las ventas. Es el ejemplo de manual de la
diferencia entre significativo y útil.

Fuera de muestra el modelo con búsqueda es **6,5 % peor** que predecir el promedio de la categoría
(EAM 0,3034 contra 0,2848).

### A nivel categoría × temporada: algo, pero poco

Agregando los 5.577 productos en 134 grupos de categoría × temporada —que es el test justo, porque
la venta de **un** producto depende del diseño, el precio y la góndola, no del atributo:

| Objetivo | Nivel de búsqueda | Pendiente |
|---|---|---|
| Venta total del grupo | **+0,184** | −0,076 |
| Venta media por producto | **+0,196** | −0,031 |

Con n=134 el umbral es 0,170, así que el nivel pasa raspando: explica cerca del **4 %**. Positivo y
en la dirección esperada, pero chico.

### Lo que esto significa para CICLO

**El momento no sirve.** El modelo del proyecto usa nivel y momento. El nivel tiene una señal débil;
el **momento no tiene ninguna** —a nivel producto +0,009, a nivel categoría −0,076, las dos veces
indistinguible de cero. Y el momento es justamente lo que sostiene la lectura de «en qué etapa está».

**Qué es CICLO entonces.** Un instrumento **descriptivo**: dice dónde está un atributo en su ciclo
cruzando capas, y eso está contrastado contra Lyst, que es un jurado externo que el modelo no vio.
No es un predictor de ventas, y ahora lo sabemos medido en vez de suponerlo. Es el mismo tipo de
corrección que hicimos en septiembre con los datasets sintéticos.

**Una lectura más incómoda.** La búsqueda tampoco predice bien cuántos productos lanza Nunalie de
cada categoría (r=+0,146, por debajo del umbral). Si la marca mirara las mismas señales que nosotros
y le funcionaran, esa correlación sería alta.

### Sobre el dataset

- Fuente: https://github.com/HumaticsLAB/GTM-Transformer · paper arXiv:2109.09824
- Descargado: 13/10/2026, por formulario
- **No se sube al repositorio**: son 2,3 GB, casi todo imágenes, y no es nuestro para redistribuir.
  El repositorio del código es MIT, pero eso cubre el código, no los datos: la licencia del dataset
  no figura. Queda como las otras tres: sin licencia declarada, uso académico, citando la fuente.
- Lo que usamos son tres CSV que suman 2 MB: `gtrends.csv`, `train.csv` y `test.csv`.

## 2026-10-13 · Unificar con la otra copia: 2025 fuera, el cono y la ventana

**Qué pasó.** Había dos copias del repositorio trabajando en paralelo desde el 6/10. Se compararon y se trajo de
la otra lo que estaba mejor resuelto, sobre la base de esta (que tiene CLIP, links, Reddit 2026 y la entrada
en dos pasos).

**2025 queda fuera de la búsqueda.** Lo encontró la otra copia y lo verificamos con nuestros datos: el cambio
medio anual de las 16 series es +3,2; en 2025 es +18,9, suben 15 de 16 y 12 tocan su máximo ese año. Es el salto
de medición de Google, empezado antes de 2026. La búsqueda se mide hasta 2024 y 2025 se dibuja tenue. Cambia
el panel «Cuándo tocó techo» y el gráfico de retrasos: lunares (pico 2019), animal print (2012), capa (2015) y
corset (2022) dejan de figurar como «sigue subiendo». Corrige también un error de esta copia: «lo habitual»
arrancaba de 2025, y por eso jeans amplios terminaba en 113; ahora termina en 70.

**El cono reemplaza a «lo habitual».** Mismo criterio —no es un pronóstico—, pero medido bien: búsqueda
detrendeada (cada año dividido por la mediana de los 16 atributos), sin 2025, 224 tramos. Lo calculó la otra
copia con un módulo que no se subió; `codigo/calcular_cono.py` lo reproduce cifra por cifra. Cada capa sigue
desde su último dato bueno con la mediana; la banda (percentiles 20–80 y 5–95) va sólo alrededor de la
búsqueda mundial, que es donde se midió el error.

**La ventana por categoría.** Cuánto tiempo la prenda tiene que seguir leyéndose actual: fast fashion 1 año,
contemporary 2, high fashion 3, diseño emergente 5. No es el lead time: una marca de nicho produce en tres meses
pero su apuesta tiene que aguantar cinco años. La ventana es un supuesto de diseño; el error a esa distancia
(±12, ±16, ±19, ±25) sí está medido. En el gráfico, «tu ventana» se mueve a 2026, 2027, 2028 o 2030 y la línea
sigue apagada más allá. Las tarjetas de la entrada muestran lead time, ventana, decide hasta y error.

**Contemporary vuelve al selector**, con su fila de `CONSEJO`, pero no a la entrada en dos pasos, que sigue con
tres categorías. Se adoptan los textos de la otra copia: lead time, high street, revival.

**Pendiente.** El K-means usa el momento de búsqueda 2024–25, contaminado por el salto. Recalcularlo con
2023–24 puede mover atributos de etapa; se hace aparte. También quedan textos de lectura escritos a mano que
citan 2025 como año de retorno (lunares, animal print).

## 2026-10-13 · La app como asistente de diseño: preguntas, Diseñar y la búsqueda corregida

**Devolución del profesor.** La interfaz es confusa: un mar de datos y gráficos. Pidió referencias visuales de
cada tendencia.

**La idea del grupo.** Que la app acompañe a quien diseña en vez de mostrarle todo: primero sabe quién es,
después lo lleva paso a paso —prenda, corte, color, estampa— y en cada paso le recomienda según lo que se
mueve afuera, pero la que decide es la persona.

**Las preguntas del principio.** País, público (mujer, hombre, sin género), si trabaja para una marca o por su
cuenta, y categoría. Con eso se filtra qué mostrar. El país importa por cómo funciona la moda: se crea afuera y
llega después. Para Argentina la app agrega «¿ya llegó acá?», comparando la búsqueda argentina con la mundial:
el jean skinny tocó techo afuera en 2012 y acá en 2016, el corset un año después, el cargo el mismo año. El
desfase va de 0 a 4 años, no es una regla. De otros países no hay datos locales y la app lo dice.

**Diseñar.** Es la pantalla principal después de las preguntas. Cada paso tiene tarjetas con una foto real de
pasarela (filtrada por público), la acción para el perfil y si gana o pierde terreno afuera; lo recomendado
queda marcado. Los cortes de jean se llaman como se llaman —baggy, wide leg, mom, barrel, recto, bootcut, flare,
tapered, skinny, slim— y para cada uno se usa su parte de todas las búsquedas de jeans. El color sale de leer con
CLIP la pasarela 2018–2023 (`prompts/prompt_disenar_referencias_y_colores_v1.md`): es interpretación de un
modelo, no venta, y así está marcado. Los gráficos siguen en «Recorridos» para quien quiera ver el detalle.

**La búsqueda, corregida en vez de recortada.** 2025 había quedado fuera por el salto de medición de Google. En
vez de perder el año, cada búsqueda se lee como peso frente a las otras búsquedas de moda (cada año dividido por
la mediana de los 16): 2025 vuelve a ser un año normal y queda lo que le importa a quien diseña, qué gana terreno
y qué lo pierde. Se usa desde 2010, porque antes había tan pocas búsquedas de moda que cualquier término pesaba
de más. El K-means ya usaba esta corrección (media de 35 términos): se verificó y no hizo falta recalcularlo.
Argentina no tuvo el salto y se usa tal cual. El cono se volvió a medir con 2025 adentro.

**Lo que se sacó de la vista.** La fila de cifras de Recorridos («1,28 M looks», «retraso 0 a +2», que además
contradecía que la pasarela no adelanta a la búsqueda) y la tira de estado de las fuentes del Radar. En su lugar:
la decisión para el perfil y qué gana y qué pierde terreno afuera.

**Siluetas en vez de sólo fotos (13/10/2026).** Una foto de pasarela trae lavado, modelo y fondo, y el corte se
pierde. En «Diseñar» los cortes de jean se muestran con un dibujo plano propio (`app/siluetas/`, todos con la
misma cintura: sólo cambia la pierna) y las estampas con una muestra de tela en el color que elegiste; la foto de
pasarela queda chica en una esquina, como referencia. En «Tu diseño» el jean se dibuja relleno con tu color y tu
estampa. Mom no es un corte (es tiro alto + pierna tapered) y se muestra así; el pied-de-poule quedó mal dibujado y
no se usa. Abrigos, buzo, cargo, corset y las estampas sin muestra (floral, encaje, gamuza) siguen con foto.
Fits, cuellos y mangas quedan guardados para cuando la app los pregunte como ejes aparte.

**Todo dibujo, sin mezcla con fotos (14/10/2026).** Tarjetas con foto y tarjetas con dibujo juntas eran «una
ensalada de frutas». Ahora cada opción de «Diseñar» es un dibujo plano: las siluetas de la carpeta del grupo más
las que faltaban (abrigos, cargo, corset, capucha, floral, encaje, gamuza, y lunares y rayas rehechas porque las
originales no repetían sin costura), dibujadas en el mismo estilo con `codigo/dibujar_siluetas.py`. Las fotos de
pasarela quedan plegadas al final de «Tu diseño», como referencia. Cada tarjeta dice una sola cosa: la acción y
un dato.

**Remeras y buzos: fit y cuello.** Remeras es prenda nueva; buzos pasó de «hoodie» a seis fits (al cuerpo,
regular, relaxed, oversized, boxy, cropped) y cinco cuellos con capucha. No hay búsqueda por fit ni por cuello:
qué gana presencia lo lee CLIP sobre la pasarela de la prenda (2018–19 contra 2022–23), como el color, y está
marcado como interpretación. El cuello es la lectura más débil: en una foto de pasarela entera se ve chico.

**La pregunta del país, afuera.** Con dos opciones (Argentina / otro país) quedaba raro, y una lista de países
prometería datos locales que no tenemos. La entrada es de tres preguntas. El dato argentino queda en
Recorridos, como «búsqueda local (AR)», para cualquiera.

**Mangas, más cuellos y los dibujos adentro de la página (14/10/2026).** Remeras y buzos suman el paso «Manga»
(corta y larga primero; después sin manga, tres cuartos, hombro caído, raglan, abullonada y globo), leído por CLIP
igual que fit y cuello. Remeras suma halter, cuello drapeado y mock neck. Halter, drapeado, abullonada y globo no
se muestran si diseñás para hombre. Los dibujos ahora viajan dentro de los datos (`DIS.svg`, lo arma
`codigo/armar_diseno.py`) y no como archivos aparte: así no hay tarjetas vacías mientras cargan ni diferencias
entre navegadores.

**Menú más corto.** Cuatro secciones a la vista —Diseñar, Tendencias (el radar), Recorridos y Buscar por imagen—
y el resto (El ciclo, Marcas, Retornos, Método) detrás de «Más».

## 2026-10-20 · Netlify como app oficial y Groq en vivo

**Problema.** IA-5 corría con un prompt fijo desde la Entrega 2. Llamar a Groq desde el navegador
expone la clave, y GitHub Pages sólo sirve archivos: no puede guardar un secreto.

**Decisión.** La app oficial pasa a Netlify (`ciclo-udesa.netlify.app`), con una función
(`netlify/functions/lectura.mjs`) que guarda la clave como `GROQ_API_KEY` y arma el prompt del lado del
servidor. GitHub Pages queda como espejo: ahí el botón avisa que la lectura en vivo sólo corre en la app
oficial.

**Cómo se usa.** En Recorridos, debajo de la recomendación fija, «Pedir lectura en vivo». El navegador
manda sólo métricas del atributo (nivel y momento en pasarela y búsqueda, picos, validación) y el tipo de
cliente; la función valida cada campo contra una lista cerrada, así que no entra texto libre al modelo.
La respuesta sale en salmón, marcada como interpretación, con el modelo y la versión del prompt.

**Lo que corregimos al armarlo.** La tabla del K-means guarda el pico de búsqueda de Jeans baggy en 2025,
el año del salto de medición. Mandarlo así contradecía un límite declarado; ahora la función recibe el
pico hasta 2024, el mismo que dibuja la app. El momento de búsqueda todavía usa 2024–25: sigue pendiente.

**Por qué un botón y no automático.** Cada lectura es una llamada que cuesta y tarda. La recomendación
fija sigue a la vista: las dos se pueden comparar.

## 2026-10-20 · El K-means sin 2025, y sin calzado

**Problema.** Desde el 13/10 estaba pendiente: el K-means medía la búsqueda con 2024–25, y 2025 es el año
del salto de medición de Google. Cuatro de las variables del modelo dependían de ese año: el nivel
(promedio 2024–25 sobre el máximo) y el momento (2024–25 contra 2021–22).

**Cómo lo recalculamos.** Encontramos el script original (`kmeans_ciclo.py`) y las 35 series mundiales
con las que se detrendea. Con la definición vieja se reproducen los 18 valores de la app con error menor a
0,001, así que la base es la misma. La nueva corre la ventana un año: nivel 2023–24 sobre el máximo hasta
2024, momento 2023–24 contra 2020–21. Pasarela y validación no cambian. Queda en
`codigo/recalcular_kmeans_sin_2025.py`.

**Calzado afuera.** La app trabaja con ropa: no va a haber calzado. «Zapatilla chunky» sale del K-means y
de la consulta por imagen (IA-6, `prompt_consulta_por_imagen_v3.md`). El modelo pasa a 17 atributos. Deja
de ser un pendiente y pasa a ser un límite declarado por decisión.

**Qué cambió.** Seis atributos cambian de etapa. Lunares, cuero, encaje, cuadros y piel pasan de «en
retorno» a «saturada»: su retorno era el salto de 2025. Capa pasa de «pico» a «saturada». «En retorno»
queda con un solo atributo, animal print. Pico (7), saturada (8) e Y2K en ascenso se mantienen. Los
movimientos más grandes del momento son cargo (−0,09 → +0,64) e Y2K (−0,07 → +0,81): con la base 2021–22
ya estaban arriba y la suba no se veía.

**k=4, con la silhouette en contra.** Sin 2025 la silhouette es 0,387 con k=2, 0,384 con k=3 y 0,373 con
k=4. Antes k=4 era el mejor; ahora los datos no lo piden, aunque la diferencia es chica. Nos quedamos con 4
porque con menos grupos no se separan etapas, y lo decimos en la pantalla del modelo: dos grupos tienen un
solo atributo (Y2K y animal print).

**Lo que no se tocó.** Los textos de Recorridos usan la búsqueda corregida por la mediana (13/10), donde
2025 sí cuenta: lunares sube de 37 a 64 en 2025 y su texto de «retorno cada seis años» se sostiene ahí,
aunque el K-means ahora lo ponga en «saturada». Son dos lecturas distintas: el K-means mira 2023–24 contra
2020–21. El de animal print decía «otra vez 2025» y la serie sube en 2024: se corrigió. La nota de
`prompt_lectura_recomendacion_v2.md` que dice que el momento usa 2024–25 ya no vale; no se edita porque los
prompts no se pisan.

**La clave, conectada (20/10/2026).** Con `GROQ_API_KEY` cargada en Netlify, Groq devolvió 404: ya no
ofrece Llama. La función pasa a `openai/gpt-oss-120b` (`prompt_lectura_recomendacion_v3.md`). La primera
lectura real ya muestra que el modelo y la recomendación fija pueden no coincidir (jeans baggy en high
fashion: «Entrar» contra «Esperar»), y eso es justamente lo que la interfaz deja comparar.

## 2026-10-20 · Preguntale a CICLO: el LLM de la clase, hecho para CICLO

**Qué pidió la cátedra.** Un LLM para la app como los de la clase. Por ahora, la versión que corre con la API
key de cada uno y en el navegador (V1/V2), no la de servidor (V3/V4).

**Cómo funciona.** Una vista nueva, «Preguntar». Se pega la API key de Groq (queda en el navegador) y se
pregunta en lenguaje natural. El modelo recibe el perfil elegido en la app y DATOS: un Markdown con el
formato de los ejemplos de la clase. Contesta un JSON que la página valida y muestra en salmón.

**La fuente de datos es nuestra y se genera.** `app/llm/ciclo_datos.md` lo arma `codigo/armar_datos_llm.js`
desde las constantes de la app: cómo leer cada número y de qué capa sale, etapas, perfiles, la regla fija
por etapa y perfil, un resumen de los 20 atributos, una ficha por atributo (pasarela, búsqueda hasta 2024,
peso afuera, Argentina, validación, lectura, sinónimos), lo de Diseñar (cortes, fits, cuellos, mangas,
colores leídos por CLIP) y lo que CICLO no puede responder. Escribirlo a mano lo habría desactualizado con
el primer cambio del modelo.

**Lo que no copiamos de los ejemplos.** El documento entero pesa ~7.700 tokens y el plan gratis da 8.000 por
minuto. Se manda lo general siempre y sólo las fichas que nombra la conversación: ~2.900 tokens por pregunta.

**Lo que corregimos al probarlo.** Contestó «Entrar» para high fashion en pico aunque la regla estaba en
DATOS: ahora la página calcula la regla y la pega en la ficha, y avisa si el modelo se aparta. Confundió dos
cuellos porque la línea decía «Halter 17 % (+7,8)»: ahora dice «Halter: 17 %, +7,8 puntos». Detalle y
pruebas en `prompts/prompt_asistente_v1.md`.

**IA-5 sigue igual.** La lectura de Recorridos usa la clave guardada en Netlify; «Preguntar» no depende de
ella.

## 2026-10-20 · El arranque, el color de la acción y la estética de revista

**El arranque.** La app podía abrir en la portada vieja. Dos causas. La portada y el radar no tenían
`hidden` en el HTML: si el script fallaba antes de arrancar, quedaban a la vista. Y con un perfil guardado, al
restaurar el selector de cliente se escribía `#portada?…` en la dirección (la vista inicial todavía era la
portada), y después el arranque leía esa misma dirección y volvía a la portada. Ahora todas las vistas
empiezan ocultas y sólo el arranque decide cuál se ve; restaurar el perfil no toca la dirección; el arranque
está protegido y, si falla —adentro o antes de llegar—, se muestra el gate con un aviso, nunca una pantalla
equivocada sin explicación. Las tres preguntas siguen siendo la entrada; si el perfil ya estaba guardado no
se saltea en silencio: arriba de cada vista dice «Diseñando para mujer · marca de fast fashion · cambiar».

**El color de la acción.** «Entrar» salía en rojo (era el salmón de la IA), justo al revés de lo que dice.
Pasa a semáforo: Entrar verde, Esperar y Explorar ámbar, Salir rojo, siempre con la palabra, para que se lea
en blanco y negro y por quien no distingue rojo de verde.

**La tesis de color, actualizada.** Decía «interfaz monocroma para que el único color de la pantalla sea el
de las prendas», y el semáforo la contradice. Queda así: **negro es medido, salmón es calculado o
interpretado por un modelo, y los tres colores de acción están reservados para la recomendación**, que es
una decisión y no un dato. Nada más lleva color. Para cumplirlo se sacaron colores que se habían colado: el
azul de las etiquetas «medido» y de los focos, el verde y rojo de «gana/pierde terreno» (ahora negro, el
signo lo dice), y los colores de las series en los gráficos, que pasan a grises (cada capa ya tenía su tipo
de línea). Cinco etiquetas «interpretación» que salían en rojo pasan a salmón. Está escrito igual en la
pantalla de Método.

**La estética.** La portada tenía la vibra de revista y el resto no. Ahora todas las vistas: Bodoni Moda de
80 a 116 px en los títulos contra IBM Plex Mono de 10–11 px en mayúsculas para las etiquetas, sin tamaños
intermedios; márgenes anchos; grilla asimétrica (la etiqueta de sección a la izquierda, título y bajada en
la columna ancha); texto en columnas de 60–70 caracteres; reglas de 1 px; sin esquinas redondeadas, sombras
ni botones con relleno (de línea fina o texto subrayado); numeración de sección como sumario, en el orden del
menú (01 · Diseñar … 09 · Método, igual en el índice de la portada); paleta negro, crema #F6F0EB y blanco. Se
hizo como un bloque al final del CSS que pisa lo anterior, para no reescribir 480 líneas.

**Los gráficos vuelven a tener color (20/10/2026).** Pasar las series a grises hacía que el K-means y
Recorridos se leyeran peor: cuatro grupos en cuatro grises no se distinguen. Vuelven sus colores de serie, que
sirven sólo para separar líneas y grupos. Gana/pierde terreno sigue en negro: está en dos columnas con su
signo, y en verde y rojo se confundía con Entrar y Salir. Los subtítulos de sección (Bodoni) suben a 36–60 px
y llevan una regla de 1 px arriba: abren sección en vez de ser un tamaño intermedio.

## 2026-10-20 · Siete frentes: entrada, señal, taxonomía, materiales, combinaciones, dos capas y la barra

**La entrada, siempre.** La app abre en las tres preguntas aunque haya respuestas guardadas: vienen marcadas y
alcanza con «Continuar». Sólo un link que trae el perfil (`c`, `v`, `pu`) la saltea. Se borra `perfilListo`
y sale la barra de perfil del header: cambiar de cliente a mitad de camino recalculaba todo y hacía sentir la
app inestable. «Cambiar perfil» queda al final del menú. La categoría suma contemporary.

**La tesis de color, otra vez y con arquitectura.** Una tarjeta podía decir «recomendado» con borde rojo, y
«gana presencia» salía en rojo: el borde, el texto y el ícono decidían su color cada uno por su lado. Ahora una
sola función, `señal(atributo, perfil)`, devuelve estado, palabra, porqué, clase e ícono, con cuatro estados:
entrar (verde), esperar (ámbar), salir (rojo) y **sin-dato (neutro, no rojo)**. En el CSS el color sale sólo de
la clase `s-<estado>`. La regla queda: **negro = medido, salmón = interpretado por un modelo, los tres de
semáforo reservados para la señal**, siempre con la palabra y un ícono.

**Taxonomía.** El jean no es una prenda: es pantalón + denim. Prenda › tipo › corte › tiro, y material,
detalle y estampa como ejes aparte (`codigo/taxonomia.py`). Mom, boyfriend y jeggings dejan de ser cortes y
quedan como alias de búsqueda: sus series suman a straight, tapered y skinny. En Recorridos y el K-means los
grupos agregados siguen como se midieron en septiembre (las dos búsquedas viejas dentro de «amplios");
recalcularlos es un pendiente declarado.

**Materiales y detalles.** 35 materiales en ocho grupos; el encaje pasa a detalles. Sólo se ofrece lo que se
produce en cada prenda. 16 texturas dibujadas (no fotografiadas: las fotos no tienen licencia).

**Recomendaciones que no pueden ser falsas.** Las combinaciones imposibles no se ofrecen (lunares en denim,
camuflado en satén, toile en punto). La ficha recomienda sólo si el corte o tipo, la estampa y el detalle
tienen serie, con al menos una serie medida —CLIP solo no alcanza, es interpretación—, y escribe de dónde sale
cada número. Si no puede escribir esa línea, dice «Sin recomendación».

**Dos capas a la vista.** Todo el vocabulario (117 atributos) aparece con dibujo y definición; cada panel
cuenta «x de n con dato medido». Lo que no tiene serie se ve neutro, no rechazado.

**La barra.** Lo elegido se acumula en chips en una barra fija abajo; cada chip vuelve a su paso sin perder el
resto, y «Armar la ficha» junta todas las señales.

**Un bug viejo.** Las muestras de estampa nunca se habían visto: `url("…")` dentro de un `style` con comillas
dobles cortaba el atributo.

## 2026-10-20 · Los jeans reagrupados y el K-means otra vez

**Qué cambió.** Mom y boyfriend dejan de contar como «amplios» y pasan a «medios», como dice la taxonomía.
`codigo/regrupar_jeans.py` reconstruye la serie mundial de cada grupo: el volumen total de jeans sale de
serie ÷ participación en cada grupo, y el grupo nuevo es participación × total. Control: los ajustados, que
no cambian de términos, se reproducen con un error máximo de 0,3 sobre 100. Se regeneran JE, REC, GREL y el
CSV, y el K-means con `codigo/recalcular_kmeans_sin_2025.py`.

**Qué movió.** Mom tuvo su pico en 2020–21 y después cayó: sin él, los amplios suben +161 % en el momento
de búsqueda y los medios bajan −34 %. Jeans amplios y cargo quedan juntos en «pico»; los medios pasan a
«saturada»; lunares, cuero, encaje, cuadros, piel y animal print forman «en retorno». Silhouette con k=4:
0,320 (no es la mejor; se queda en 4 por lo mismo de siempre).

**Un error de nombre que salió con esto.** El nombrador era goloso: el par grupo–etapa más cercano primero.
Al último grupo le quedaba la etapa sobrante, y Y2K —subiendo +81 %— salía «saturada». Ahora los cuatro
centros toman juntos la combinación de etapas con menor distancia total. Y2K vuelve a «en ascenso».

## 2026-10-20 · Cajas, procedencia sin color, dato prestado, «El ciclo»

**El rojo, por última vez.** Había dos reglas peleando por el canal color: el salmón y su terracota (`--ia`,
`--ia-t`) marcaban «interpretado por un modelo», y las recomendaciones son interpretadas, así que salían
rojizas. La procedencia sale del canal color: se marca con texto, ícono y línea punteada (● medido,
◇ interpretado, ↪ prestado). El color queda sólo para la señal, con cuatro estados. **Se retira la regla del
salmón** que venía de la Entrega 2.

**Cajas cerradas.** Toda opción elegible es una caja de cuatro lados, de al menos 44 px, con hover, foco
visible y un estado elegido que se distingue sin color (borde doble).

**Dato por cercanía.** Las hojas sin serie propia toman la de un pariente y lo dicen en la tarjeta: hermano de
la misma familia, después el padre, después el atributo suelto (el color en toda la pasarela). Nunca se salta
a otra familia sin parentesco. El pantalón largo pasa a tener dato propio: las tres series de jean. Las 34
búsquedas nuevas que llevarían a ~50 hojas con dato propio no se exportaron: el plan
(`plan_exportacion_trends.csv`) no está en el repositorio y Google Trends se baja a mano.

**«El ciclo».** Recorridos no se entendía. Ahora contesta una pregunta: cuándo picó y cuánto tardó en volver.
Cada atributo dice su último pico, si sube o baja, los años desde el pico y, si hay dos picos, la distancia
entre ellos, en una frase. El K-means pasa a llamarse «El modelo». El gráfico arranca en el primer año con dos
capas y marca dónde entra cada fuente.

**Dos bugs viejos que salieron al dibujar.** Las barras de color de Tendencias nunca se habían visto (dentro
de un `<button>` flex un bloque vacío queda de ancho cero), y las muestras de estampa tampoco (un `url("…")`
dentro de un `style` con comillas dobles).

**Dos decisiones (20/10/2026).**
- **k = 4, y se queda.** La silhouette prefiere k=2 (0,361) y después k=6 y k=5, pero con dos grupos el modelo
  sólo diría «sube o baja», que ya lo dice la señal; y con 5 o 6 aparecen grupos de un atributo. El K-means está
  para nombrar etapas, y cuatro es lo mínimo que las separa. Queda declarado en la pantalla del modelo.
- **La bermuda toma el dato del pantalón largo, no del cargo.** El cargo no es su pariente en el árbol (está en
  detalles), y el préstamo salta de familia, que es justo lo que la regla prohíbe. Hermano primero, como short y capri.

**Cuántas hojas tienen dato.** Sobre 128 hojas (tipos, cortes, tiros, materiales, detalles, estampas y los 12
colores del vocabulario): **26 directo, 39 prestado, 63 sin dato**. El plan para salir a buscar lo que falta está
en `datasets/plan_exportacion_trends.csv` (36 términos en 9 lotes con trench coat de ancla) y se pega con
`codigo/pegar_lotes_trends.py`.

**Las 36 búsquedas nuevas, pegadas (20/10/2026).** Entraron 32 de 36 (el ancla pega en los nueve lotes). Las hojas
con dato directo pasan de 26 a 58; quedan 36 prestadas y 34 sin dato. Las nuevas se leen como las 16 de antes
(peso frente a las otras búsquedas de moda, con la mediana de las 16 originales, para que sumar series no mueva las
que ya estaban), pero no entran al K-means: no tienen pasarela medida. Cable knit, tweed, capri y bermuda no
alcanzaron (pocos años útiles o serie plana) y siguen prestadas.

## 2026-10-20 · 2026 contaminado: todo corta en 2024, y el segundo plan de Trends

**El corte.** 69 de 70 series de Google Trends saltan en 2026 (mediana +99 %), y el ancla, trench coat, pica en
abril cuando siempre picó entre septiembre y febrero. Es la medición, no la moda. Ya se sacaba 2025 del pico y del
K-means; ahora todo el análisis termina en 2024: la señal (2022→2024), la cuota de cada corte de jean, El ciclo,
el pegado de series nuevas (cada una a su máximo hasta 2024) y lo que lee el asistente. 2025 y 2026 se dibujan
apagados, con punto hueco. `ANIO_F` no existe en el repositorio; la constante vigente es `ANIO_BASE = 2024`, y
`ANIO_G` (último año de la búsqueda) pasa de 2025 a 2024.

**Qué entró y qué no.** 19 de 34 términos del segundo plan; los descartes y por qué están en
`datasets/fuentes_y_descargas.md` para que se vea que se probaron. «bermudas» y «toile» quedan afuera porque miden
otra cosa, no por poco volumen: mejor poco dato correcto que mucho dato de otra cosa.

**Conteo.** Sobre 128 hojas: **75 directo, 40 prestado, 13 sin dato** (antes 58 · 36 · 34). Sin dato quedan el
tiro medio, ocho materiales (jersey, rib, french terry, piqué, lona, nylon, acrílico, crepe), toile de jouy, chevron
y los colores naranja y amarillo.

## 2026-10-20 · Nombres de taller, buzos partidos y el chat como herramienta

**La regla de nombres.** Si un diseñador no puede decir el nombre en voz alta en un taller y que le entiendan, no va
en la interfaz. Cada material lleva tres cosas: el nombre rioplatense (el título), el término de industria en
inglés (chico abajo) y una línea de qué es: «Frisa · french terry · Punto afelpado por dentro, la tela del buzo».
Corderoy, Polar, Crepé, Satén, Morley, Punto trenzado, Lycra. El jersey va sólo en remeras y vestidos y el crepé
sólo en vestidos y blusas: la tabla los dejaba pasar a pantalones (estaba mal cargada, no mal aplicada). Blazer,
capa y kimono tienen su propia lista.

**Fuera los contadores.** «4 cortes con dato» era contabilidad interna. Se quedan las etiquetas de procedencia de
cada tarjeta («mostrando: …»), que son la honestidad del dato.

**Buzos y Sweaters, por separado.** Buzos: hoodie, canguro con cierre, cuello redondo; los tres toman prestada la
serie «hoodie», que mide los buzos en general. Sweaters: cuello redondo, en V, polera y cardigan. Capa y kimono
quedan como secundarias de Abrigos, con su definición.

**El chat, herramienta de diseño.** Recibe el diseño armado, lee una imagen con CLIP y muestra lo que leyó para que
se corrija, trae el dato y la serie en cada respuesta y termina en cambios que se aplican con un botón
(`prompts/prompt_asistente_v2.md`).

**Accesorios y calzado.** No entran sin dato. El calzado sigue afuera por la decisión del 20/10 («no va a haber
calzado»). Para accesorios está el plan en `datasets/plan_exportacion_trends_3.csv` (gorra, piluso, tote,
cinturón de cuero, anteojos de sol), junto con «toile de jouy» para reemplazar a «toile».

## 2026-10-21 · Accesorios y calzado no entran, y el filtro de estación

**Se deshace la vuelta del calzado.** Lo probamos con 14 términos de accesorios y calzado (plan 3). Pasan 2, y son
demasiado genéricos para ser una decisión de diseño: «tote bag» y «sneakers». Los estilos concretos —guillerminas,
plataformas, chatitas, botinetas, botas texanas— están por debajo de la resolución de Google Trends a escala mundial,
y los que sí miden algo, como «sandals» y «sunglasses», miden la estación. Dos categorías con un término genérico cada
una son peores que no tenerlas: no entran a la app.

**El camino para medir el calzado es la pasarela, no la búsqueda.** El índice CLIP (`app/clip/`) ya tiene 14.000
looks embebidos: sumar un atributo es escribir sus frases y puntuarlo contra esos looks, sin bajar nada. Eso da
frecuencia en pasarela por temporada, que para calzado es mejor dato: un zapato de pasarela es una decisión de
diseño; una búsqueda de «sandals» en junio es alguien que quiere comprar sandalias. Pendiente: botas texanas,
botinetas, plataformas, mocasines, chatitas, guillerminas, zapatillas, piluso, gorra, cinturón ancho.

**Filtro nuevo: sólo estación.** Una serie que se mueve más dentro de cada año que entre años (amplitud estacional
media > 1,5 × rango del nivel anual, 2004–2024) mide el verano o el invierno, no la moda. Sandals pasaba todos los
filtros anteriores (máximo 46, 252 meses con señal) pero se mueve 20 puntos dentro del año y 11,6 entre años. Corrido
sobre todo lo incorporado, se caen tres: **capris** (8,6 contra 2,9), **cashmere** (10,0 contra 4,6) y **wool coat**
(7,1 contra 4,0). Capris parecía un ciclo completo, pero su forma es el verano repetido; vuelve a prestado del pantalón
largo. Cashmere y paño toman la serie de lana.

**Toile, otra vez.** «toile de jouy» volvió en cero absoluto en los 21 años, lo que confirma que «toile» (máximo 83)
medía tela y moldes de costura, no la estampa. Ya estaba afuera desde el plan 2; la hoja toma prestado del floral.
Studded se revisó con el mismo criterio: salta +104 % en 2026 como el resto y no es estacional (0,42); se queda.
Bermudas ya estaba afuera.

**Conteo.** Sobre 131 hojas: **71 directo, 48 prestado, 12 sin dato**.

**Calzado y accesorios, en Diseñar, sin inventar (21/10/2026).** A pedido del grupo, Calzado (zapatillas, botinetas,
mocasines, chatitas, sandalias, plataformas, guillerminas, botas texanas) y Accesorios (tote, piluso, gorra,
cinturón, anteojos de sol) aparecen como prendas en Diseñar, con dibujo y definición. Tienen dato propio sólo los que
pasan todos los filtros: **zapatillas, mocasines y tote**. Piluso quedó en 11 años útiles; sandalias y anteojos los saca
el filtro de estación; el resto es ruido o no tiene señal. Esos se ven como «sin dato directo»: se pueden explorar,
no se recomiendan, y no toman prestado de un hermano porque un estilo de calzado no dice nada de otro. El camino
para medirlos sigue siendo la pasarela (CLIP).

**Todas las series, en los gráficos.** El ciclo, las barras de Tendencias y el recorrido usaban sólo las 16 series
originales. Ahora suman cada hoja con serie propia (65 en total), con un filtro por grupo en El ciclo. Las nuevas
sólo tienen búsqueda: el recorrido lo dice.

## 2026-10-21 · GitHub Pages pasa a ser la app oficial

La cuenta gratuita de Netlify se quedó sin créditos y rechaza los deploys (automáticos y directos) desde el commit
`e2c4e4b`. GitHub Pages publica lo mismo en cada push y pasa a ser la URL oficial:
https://felipeberney-boop.github.io/ciclo/. Netlify queda como espejo, y es el único lugar donde corre la lectura en
vivo de IA-5 (necesita la función con la clave guardada); vuelve cuando se renueven los créditos o se pase a un plan
pago. «Preguntar» no depende de Netlify: usa la clave de cada uno desde el navegador.


## 2026-10-25 · IA-5 en vivo desde el navegador, y Netlify pausado

**Problema.** El pase a GitHub Pages había dejado roto el botón «Pedir lectura en vivo» de Recorridos. La app
seguía llamando a `/api/lectura`, la función de Netlify. En Pages ese POST devuelve 405, no 404, así que el aviso
previsto no aparecía y se veía «No se pudo leer.». La lectura en vivo, que es lo que separa la app de una
maqueta, no andaba en la URL oficial.

**Decisión.** IA-5 pasa a funcionar como «Preguntar», el patrón V2 de la clase: el navegador llama a Groq con la
clave que pega cada uno (`groq_key`, la misma en las dos pantallas). Si no hay clave, el botón la pide ahí mismo.
El servidor existía para no exponer una clave del proyecto; con la clave de cada usuario esa razón ya no aplica.
Lo que importaba de la función se conserva: el prompt se arma con texto fijo y números de la app, sin texto libre
de quien la usa, y la salida se valida (una de las tres acciones permitidas y una frase no vacía). Prompt nuevo:
`prompts/prompt_lectura_recomendacion_v4.md`.

**Lo que corregimos al pasarlo.** v3 decía que el peso en la búsqueda se medía «2023→2025», y el subtítulo de
«Qué gana y qué pierde terreno» decía «de 2023 a 2025». `terreno()` mide 2022→2024 desde el corte en 2024. Los dos
dicen ahora 2022→2024. La respuesta en vivo también suma el ícono de la señal, que le faltaba.

**Netlify.** `netlify.toml` y `netlify/functions/lectura.mjs` quedan en el repo con un aviso arriba: están
pausados, el deploy vivo es GitHub Pages y la app no los usa. Se dejan por si algún día hace falta un servidor.

**Cómo se probó.** Playwright en escritorio (1280) y teléfono (390), con Groq simulado: sin clave aparece el campo,
la clave se guarda y pasa a «Preguntar», la respuesta sale con su marca de interpretación, modelo y versión de
prompt, y un 401 muestra el aviso de clave rechazada. No hubo errores de JavaScript ni scroll horizontal. Con una
clave real falta probarlo una vez desde la URL publicada.

## 2026-10-25 · El K-means ya cortaba en 2024: verificado

El pendiente «recalcular el K-means sin el momento 2024–25» seguía apareciendo en las listas, aunque se había hecho
el 20/10. Lo verificamos: `codigo/recalcular_kmeans_sin_2025.py`, corrido con el CSV de capas de `datos_limpios/`
(nivel 2023–24, momento 2023–24 contra 2020–21, máximo hasta 2024, k=4 reentrenado), da **exactamente** las 17 filas
de `const KM=` de la app: nivel, momento y grupo, con diferencia 0. No hay nada que recalcular. El CSV de entrada no
está en el repo; vive en `datos_limpios/` de la carpeta de Drive del grupo, y hace falta para repetir esta prueba.

## 2026-10-25 · Calzado por pasarela con CLIP: la prueba chica

**Qué probamos.** Antes de sumar el calzado a Diseñar, una prueba sin tocar la app (`codigo/probar_calzado_clip.mjs`):
10 estilos (los 8 de Diseñar más botas altas y stilettos), dos frases y tres plantillas cada uno, puntuados contra los
14.000 looks ya embebidos. Cada look va al estilo más parecido. Después miramos a mano los 8 looks más seguros de
cada estilo.

**Qué vimos.** CLIP no mira el zapato: mira el look entero y adivina el zapato por el estilo de la ropa.

| Estilo | Los 8 más seguros | Qué está leyendo |
|---|---|---|
| Zapatillas | 8 de 8 con zapatillas | streetwear (buzos, camperas deportivas) |
| Botas texanas | 7 de 8 | el look western (sombrero, flecos, denim) |
| Botas altas | 6 de 8 | botas, pero también pantalón de cuero |
| Botinetas | 5 de 8, con confianza muy baja (7 looks ≥ 0,5 en 14.000) | botas de cualquier altura |
| Mocasines | 5 de 8 | sastrería de hombre |
| Sandalias | 4 de 8 | ropa de verano y piel a la vista |
| Chatitas | ninguna | «ballet»: tutús y bailarinas |
| Plataformas | ninguna; se queda con 21–31 % de los looks sin seguridad | es el cajón de lo que no encaja |
| Guillerminas | ninguna | ruido |
| Stilettos | no se ven los pies | vestidos de noche |

**Qué significa.** Para los estilos atados a una forma de vestir (zapatillas, botas texanas, botas altas), la
frecuencia en pasarela es usable, siempre como *interpretado*. La de zapatillas, por ejemplo, va de 2,7 % de los looks
en 2010 a 9,7 % en 2019 y 11 % en 2021, y baja a 8,9 % en 2023. Pero lo que mide es «looks de estilo deportivo», no
«zapatillas», y hay que decirlo así. Para chatitas, plataformas, guillerminas y stilettos, CLIP sobre el look entero
no sirve: haría falta recortar los pies de cada foto, y eso sí obliga a bajar las imágenes.

**Pendiente de decidir, no de programar.** La señal exige al menos una serie medida y CLIP es interpretación, así que
el calzado leído por pasarela saldría igual como «Sin recomendación». Las opciones son: (a) mostrarlo sólo como
frecuencia en pasarela, sin señal; (b) cambiar la regla para el calzado; (c) dejarlo afuera. Hasta decidir, no
entra a la app.

## 2026-10-26 · Calzado: la pasarela como frecuencia, sin señal

**Decisión del grupo.** De las tres opciones que quedaron abiertas el 25/10, el calzado se muestra como
**frecuencia en pasarela, sin señal**, y se queda en la app. Cada tarjeta de calzado en Diseñar suma una línea
«Pasarela», marcada como *interpretado · CLIP*:

- **Zapatillas y botas texanas**, los dos estilos que pasaron la revisión a mano, muestran la parte de los looks de cada
  año (2010–2023) con una curva punteada, la convención de lo interpretado. Dicen qué está leyendo CLIP: looks
  deportivos y el look western. Zapatillas: 2,7 % en 2010, máximo 11,0 % en 2021, 8,9 % en 2023. Botas texanas: entre
  0,2 % y 3,0 %, es decir, entre 2 y 30 looks por año, y hay que leerlo con eso en mente.
- **Los otros seis** dicen por qué la pasarela no los puede medir, en lugar de dejar el lugar vacío.

La señal no cambia: sigue saliendo sólo de la búsqueda (zapatillas y mocasines). Los datos están en
`const CALZ_PAS=` y en `datasets_procesados/ciclo_calzado__pasarela_clip.json`, y salen de
`codigo/probar_calzado_clip.mjs`.

**Lo que había que alinear.** El chat tenía una regla que decía «CICLO no tiene calzado ni accesorios» y, a la vez,
recibía las fichas de calzado en DATOS. Ahora tiene prompt v3 (`prompts/prompt_asistente_v3.md`) y un
`app/llm/ciclo_datos.md` regenerado, con la línea de pasarela de cada estilo. La vista Método y el readme dejan de
decir que el calzado queda afuera y explican cuánto se mide.

## 2026-10-26 · Zoe Dottori Greco deja el grupo

Se saca su nombre de los materiales vigentes: la lista de integrantes del readme, el pie de la portada de la app y el
readme de las series, que la nombraba como contacto de la carpeta de Drive. Las láminas de la Entrega 2 y las copias de
versiones anteriores de la app quedan como se entregaron, porque registran quién hizo esas entregas. No era
colaboradora del repositorio de GitHub ni autora de ningún commit, así que ahí no había nada que sacar.

## 2026-10-26 · El Zara de febrero 2024 tiene fuente: MIT

Era la única fuente sin verificar, porque nadie del grupo guardó el link. «DATASETS LINKS», en el Drive, no lo tiene.
Las fichas de Kaggle se arman en el navegador y no se pueden leer automáticamente, así que consultamos la API pública
(`/api/v1/datasets/view` y `/list`) de los cinco datasets de Zara con columnas parecidas. Coincide uno solo:
«ZARA Sales» (`xontoloyo/data-penjualan-zara`). Es un `zara.csv` de 83.147 bytes, el mismo tamaño (81 kB) que «FEB
2024 - ZARA» en el Drive, subido el 27/02/2024, ocho días después del scrape del 19/02. Licencia **MIT**. Los otros
cuatro son de 2025 y traen un CSV de 6,5 MB o sólo tableros de Power BI y PDF. Después lo confirmamos con la copia del
Drive: 83.147 bytes exactos, 252 filas, 228 SKU y todas del 19/02/2024. Con esto, las fuentes del proyecto tienen
todas su licencia revisada.

## 2026-10-26 · Fuera la portada vieja; CICLO abre el cambio de perfil

**El síntoma.** «Calzado y accesorios no aparecen en prendas». En Diseñar sí aparecen: los 8 de calzado y los 5 de
accesorios, con dibujo, definición y «sin dato directo», en los tres públicos y a 1400 y 393 px (verificado con
Playwright, local y en GitHub Pages). `dzVisible` no mira el dato: sólo esconde lo marcado `solo: 'mujer'` cuando se
diseña para hombre. Lo que no tenía calzado era la **portada vieja** («Empezá por una prenda / El índice»): un menú
escrito a mano en septiembre con siete prendas, al que se llegaba tocando la marca CICLO y del que no se podía salir
sin el botón atrás del navegador (ni `abrirGate` ni `leerLink` la aceptaban como destino).

**Decisión.** La marca CICLO abre el cambio de perfil, igual que «Cambiar perfil» en el menú: dos entradas al mismo
lugar, y al confirmar vuelve a la vista donde estabas. `v-portada` sale del HTML, del CSS y de la lista de vistas; un
link viejo a `#portada` cae en las tres preguntas. Lo que la portada decía y no estaba en otro lado se muda: la bajada
(«Cruzamos 1,28 millones de looks…», ahora con veintiún años de búsqueda, 2004–2024, por el corte) y la firma de la
materia, los autores y los docentes van al pie del gate; la materia y los autores, también al colofón de cada vista.
La versión anterior quedó en `diseno/prototipos/versiones_de_la_app/app_2026-10-26_d589243.html`.

## 2026-10-26 · El calzado, contado como resultado

Probamos dos caminos independientes y el calzado sigue casi sin medir. Eso dejó de ser un pendiente: es un resultado,
y Diseñar es el lugar donde lo encuentra quien quiere diseñar unas botas texanas.

- **En cada tarjeta** de calzado y accesorios, debajo de «sin dato directo», va por qué no entra la búsqueda
  (`const CALZ_BUSQ=`, de `datasets/trends_lotes/informe.md`) y, en calzado, por qué no la mide la pasarela.
- **Al pie del paso**, «Lo intentamos dos veces»: estilo por estilo, qué dijo Google Trends (21/10), qué acertó CLIP
  en sus 8 looks más seguros (25/10) y qué queda. Señal para zapatillas y mocasines; frecuencia interpretada para
  zapatillas y botas texanas; cinco estilos (botinetas, sandalias, chatitas, plataformas, guillerminas) que no mide
  ninguna de las dos fuentes. Con los criterios del filtro y el camino que falta: recortar los pies de cada foto.
- **Método** suma una fila «Calzado · dos intentos» con los números, en lugar de una frase al final.
- El chat recibe el motivo de la búsqueda en cada ficha de calzado y accesorios (`codigo/armar_datos_llm.js`).

Corrección de paso: el título de cada panel de Diseñar se pisaba con el borde superior de las tarjetas cuando no había
bajada; ahora hay aire entre los dos.

## 2026-10-26 · El semáforo, otra vez: la tendencia en negro y la señal con su palabra

**Lo que quedaba.** No había ninguna recomendación ni ningún «gana presencia» en rojo, y ningún color de estado escrito
a mano (grep limpio). Pero `señal()`, cuando un atributo no tiene etapa del K-means, devolvía verde o rojo con la
palabra «Gana/Pierde presencia»: las 65 tarjetas de El ciclo, las barras de «Qué gana y qué pierde terreno» y la mitad
de las tarjetas de Diseñar se pintaban con el color de la decisión para decir un dato. En la misma fila de estampas
convivían «▼ Salir» y «▼ Pierde presencia» en el mismo rojo. Es lo que el 20/10 ya habíamos sacado.

**Decisión.** Dos funciones, dos cosas. `tendencia(d)` describe: ▲ gana, ■ estable, ▼ pierde, en tinta; la usan El
ciclo y Tendencias. `señal()` decide: sin etapa del K-means, la tendencia decide y lo dice con la palabra de acción
(Entrar, Esperar o Explorar, Salir), y el porqué lo aclara («sin etapa en el K-means: decide si gana o pierde terreno
afuera»). Si la tendencia la leyó CLIP, describe y no recomienda: es interpretación, y la regla de evidencia ya decía que
CLIP solo no alcanza.

**El oscuro.** El bloque editorial apagaba `--accent`, `--alert` y `--ok` con `:root`, pero el oscuro original los
definía con `:root:not([data-theme="light"])`, que pesa más: en oscuro volvían el lavanda (links, rótulos, el punto de
la pista de etapa, el logo al pasar el mouse), el rosa (bordes de las notas) y el verde. Ahora los dos bloques oscuros
del final los redefinen. Los links sin clase dejan el azul del navegador y los campos tienen foco en tinta.

**Cómo se verificó.** Playwright en las 11 vistas, 1400 y 393, claro y oscuro: todo elemento con color fuera de un
`s-<estado>` es una serie de gráfico, un punto del K-means o la paleta de una prenda.

## 2026-10-26 · Retornos hasta 2024, una sola etapa por atributo y las cifras que no coincidían

**Retornos se apoyaba en 2025.** «Lunares vuelve cada seis años: 2013, 2019, 2025» salía de `const RETS=`, una serie
cruda normalizada al máximo de 2025: justo el año que el resto de la app declara contaminado por el salto de medición
de Google. Además contradecía a El ciclo, que con la serie corregida decía «siete años» para lunares. Ahora Retornos
se calcula en vivo con la misma serie (`GREL`, 2010–2024), la misma regla de pico (`cicloDe`: un máximo que se despega
15 puntos de lo que lo rodea) y una condición más: los dos picos tienen que caer dentro de la serie, porque un pico en
el primer año corregido pudo ser anterior. Resultado: 10 de 65 atributos con retorno medido, uno con tres picos
(plisado, 2012 · 2015 · 2020); lunares 2012 → 2019, animal print 2012 → 2020. Corset y kimono, que estaban en la lista,
tienen un solo pico hasta 2024: salen. 2025 se dibuja apagado, con punto hueco, como en el resto. `RETS` deja de existir.

**Dos etapas para el mismo atributo.** La pista de las fichas de Tendencias mostraba la etapa estimada sobre el
catálogo sintético de Zara: lunares «saturada», cuero «pico», mientras El modelo los pone «en retorno». Ahora, si el
atributo está en el K-means, la pista muestra esa etapa; si no, la estimada; y debajo dice cuál es («K-means · pasarela
× búsqueda» o «estimada · catálogo sintético»). En la ficha abierta, el K-means va primero.

**Cifras.** Método decía silhouette 0,37 (la de antes de reagrupar los jeans; la vigente es 0,32 con k=4) y «35 términos
… 2004–2025» para la búsqueda (son 65 series, cortadas en 2024). El pie decía «Google Trends · 49 términos» y
«Reddit · 4.857 menciones», una cifra sin origen: la documentada es 4.404 posts, 2012–2025. Buscar por imagen decía
«ninguno de los 18»; CLIP lee 17. «Última lectura» pasa del 23/09 al 21/10, el día del último lote de Google Trends.

## 2026-10-26 · CLIP en Preguntar: el mismo umbral que Buscar por imagen, y el progreso a la vista

**Una foto, dos respuestas.** Para la misma foto, Buscar por imagen decía «No determinado: ningún atributo pasa 0,35»,
y Preguntar armaba cuatro chips desde 0,12 y se los pasaba al modelo como «CLIP leyó… confirmado por el diseñador»,
aunque nadie había confirmado nada. Ahora las dos vistas usan `CLIP_UMBRAL = 0,35` (el de la validación,
`prompts/prompt_consulta_por_imagen_v2.md`). Por debajo, Preguntar dice cuál fue el más cercano y no le pasa nada al
modelo. Cada chip muestra su probabilidad, y el prompt dice lo que pasó de verdad: «más de 0,35; el diseñador lo vio y
no lo sacó».

**La espera.** La primera consulta baja 7 MB de índice y 89 MB de modelo: con 4G lento son unos 40 s y unos 7
minutos, y sólo se veía un texto fijo. En Preguntar, durante el índice no se veía nada, porque el aviso se escribía en
la otra vista. Ahora las dos bajadas cuentan megas («Bajando el modelo CLIP: 34 de 89 MB»), en la vista que las pidió, y
Preguntar avisa el peso antes de elegir la foto, como ya hacía Buscar por imagen. Al abrir la app no se baja nada de
`clip/`: se midió en la URL publicada (1,7 s hasta poder usarla con 4G lento, 3,8 s con 3G).

**«El dato».** Los atributos que nombraba la respuesta y no tenían serie desaparecían sin aviso, y la columna de la
señal salía vacía, porque el resumen de DATOS trae `etapa` y `afuera`, no `señal`. Ahora hay una fila por atributo:
mini-gráfico con sus años, o «sin serie de búsqueda», y la etapa del K-means con el número afuera.

**Cómo se probó.** Playwright de punta a punta, con CLIP real en el navegador y Groq simulado: un trench del índice da
Trench 0,50 y Blazer oversize 0,42, que llegan como chips y al prompt; una foto ambigua (Y2K 0,33) no le pasa nada al
modelo; la respuesta trae palabra, serie y una acción que cambia el diseño y abre la ficha. Con una clave real de Groq
falta probarlo una vez desde la URL publicada.

## 2026-10-26 · El celular, en serio

Lo revisamos a 393 px en las once vistas, claro y oscuro. No había scroll horizontal y los botones daban para el
pulgar, pero:

- **Gráficos ilegibles.** Marcas, el retraso y los jeans por corte (El ciclo), el K-means y la curva de Retornos se
  achicaban al ancho del teléfono y sus rótulos quedaban en 3 a 7 px reales. En el celular ahora conservan un ancho
  donde ningún rótulo baja de unos 9 px y se deslizan de costado dentro de su caja, con un aviso «Deslizá el gráfico
  →». Hizo falta `min-width: 0` en sus contenedores de grilla: sin eso, la página entera se ensanchaba a 958 px.
- **El ciclo medía 22.000 px** (26 pantallas) antes de llegar al gráfico, y abajo repetía los 65 atributos como botones.
  Ahora muestra doce tarjetas y «Ver los 65 atributos»; la lista repetida queda plegada en «Ver otro atributo». La
  tarjeta elegida queda marcada al tocarla (antes la marca no se movía). Pasa a 10.200 px en el celular y a 6.000 en
  escritorio.
- **El menú** era un carril de 762 px en 361 que escondía Preguntar, Más y Cambiar perfil sin ningún aviso. Ahora va en
  dos renglones, todo a la vista, con links de 44 px de alto.
- **Los pasos de Diseñar** ocupaban tres renglones con flechas sueltas (una pantalla entera antes del contenido). En el
  celular van en una fila que se desliza, con el paso actual centrado; en escritorio entran los diez en una fila.
- **La tabla de El modelo** medía 552 px en una caja de 517 con scroll invisible: la columna Grupo parecía cortada
  («Saturac», «En reto»). Ahora entra.
- Tres textos decían «2004–2025» para la búsqueda (el epígrafe del retraso, la lista de capas y el detalle de
  Tendencias); dicen «hasta 2024».

Verificado con Playwright: ancho de página igual al del teléfono en las 44 combinaciones (11 vistas × 2 anchos × 2
temas), sin errores de JavaScript.

## 2026-10-26 · Las hojas sin dato: cuatro préstamos y ninguna tarjeta vacía

**El conteo estaba viejo.** El 21/10 decía 131 hojas: 71 directo, 48 prestado, 12 sin dato. Con calzado y accesorios en
Diseñar, contado con la misma función de la app (`dzSeñal`), eran 133: 74 medidas, 38 prestadas y 21 sin dato. Diez de
esas 21 son calzado y accesorios, que no piden prestado por decisión (un estilo de calzado no dice nada de otro) y
ahora cuentan sus dos intentos.

**Cuatro préstamos con pariente razonable**, con el precedente de la gabardina, que se lee con el trench:
- chevron ← espiga: el mismo zigzag sin el corte en el vértice; «chevron print» fue ruido.
- frisa ← buzos: es la tela del buzo.
- jersey ← remera: es la tela de la remera.
- acrílico ← lana: la imita en el punto, como el cashmere y el paño.

**Quedan sin dato, con dibujo y definición:** tiro medio, morley, piqué, lona, nylon y crepé. Ninguno tiene un pariente
que diga algo de él. El morley es la tela del puño y de la musculosa; pedirle prestado a la musculosa sería elegir una
de sus dos prendas.

**Ninguna tarjeta vacía.** Las 24 estampas no tenían definición (el campo no existía) y «Liso» era un rectángulo de
color sin texto. Ahora todas dicen qué son (`DEF_ESTAMPA` en `codigo/taxonomia.py`). Liso sigue siendo la muestra
lisa en tu color, porque eso es.

**Conteo nuevo:** 133 hojas, 74 medidas, 42 prestadas, 17 sin dato (10 de calzado y accesorios).

## 2026-10-26 · Los jeans por corte, hasta 2024 y con el reagrupado

Al regenerar las capturas apareció que «Los jeans, por corte» seguía con números de antes del reagrupado del 20/10 y
con 2025 adentro. El gráfico llegaba a 2025 («Amplios 47 %») y marcaba a mano «2021: el amplio pasa al ajustado». Los
textos decían que los amplios pasan «del 13 % en 2012 al 55 % en 2025» y que «adentro de los amplios» el recto de tiro
alto ya cae, pero desde el reagrupado ese término cuenta en los medios.

Con `JE` vigente y el corte en 2024: los amplios pasan del 5 % (2012) al 41 % (2024) y cruzan al ajustado en 2024 en la
web y en 2021 en Google Shopping. El cruce ahora se calcula. Adentro de los amplios suben los cuatro (baggy, wide leg,
barrel y relaxed tienen su máximo en 2024). La historia de «mirar adentro del grupo» pasó a los medios: el recto de tiro
alto picó en 2021 y cae (17 → 10), mientras straight, bootcut y flare están en su máximo. Los tres gráficos chicos
también cortan en 2024, y la leyenda del recorrido dice «2010–2024, 2025 apagado».

## 2026-10-26 · Tendencias pasa a ser la pantalla principal

**Decisión del grupo.** Lo principal de CICLO es ver qué está en tendencia y moviéndose; Diseñar es una función de la
app, no la puerta. El menú queda Tendencias · Diseñar · El ciclo · Buscar por imagen · Preguntar (numeradas 01, 02, 03 en
ese orden). La app sigue abriendo en las tres preguntas, porque el perfil decide qué recomendar, y al contestarlas lleva
a Tendencias. La marca CICLO lleva a Tendencias desde cualquier vista (en las tres preguntas no saltea nada); «Cambiar
perfil» sigue volviendo a las preguntas. La versión anterior quedó en
`diseno/prototipos/versiones_de_la_app/app_2026-10-26_2b2e1f1.html`.

**El espejo de Netlify.** Seguía mostrando la versión de octubre, con la portada vieja sin calzado, y es fácil entrar
por error. Netlify rechaza los deploys por falta de créditos y no se puede actualizar desde acá; `netlify.toml` suma una
redirección 301 de todo a la app oficial, que se aplica en el próximo deploy que Netlify acepte.

## 2026-10-26 · La ficha de Tendencias recomendaba con datos de demostración

**El problema.** Con Tendencias como pantalla principal, la ficha abierta de cada atributo recomendaba con
`consejo(cliente, t.et)`: la etapa estimada sobre el catálogo sintético de Zara 2018–22. El cuero decía «K-means: en
retorno» arriba y «Entrar: está en pico, es el último tren» abajo, para fast fashion. Ahora la recomendación sale de
`señal()`, como en el resto de la app: la etapa del K-means y la regla de tu perfil (cuero, fast fashion: Esperar; nicho:
Entrar); si no está en el modelo, la tendencia de su serie (rayas y gamuza: Entrar); si no tiene ninguna de las dos,
«Sin recomendación» (corazones, punto, geométrico, liso). Verificado en las doce fichas con dos perfiles. La «Lectura»
de cada ficha es un texto que escribimos nosotros: dejó de llamarse «Lectura de la IA».

**Cifras que se presentaban como medidas.** En Método, la paleta de cada atributo y el chi² estampa × color (782,6) salen
de Zara 2018–22, el archivo que el 08/09 declaramos sintético: pasan a «demostración». «Grupo en liquidación: 1.814
productos de 8 marcas» no tiene fuente en ningún documento del repo: pasa a «sin verificar». El subtítulo de Tendencias
decía «doce atributos leídos en los catálogos de nueve marcas»; ahora dice qué parte es medida y cuál de demostración.
El guion de la presentación (`entregas/entrega_3/presentacion_guion.md`) sale con estas correcciones.

## 2026-10-27 · Una sola presentación: la web

La presentación de la Entrega 3 existía en dos formatos: la web (`app/presentacion/`) y 22 láminas en Figma Slides,
con un prototipo navegable en Figma para embeber. La referencia que dio la cátedra (el making of de Valonia) es una
página web, y mantener dos formatos a una semana de la entrega duplica el trabajo.

**Queda la web como única presentación.** Las Slides y el prototipo de Figma salen del readme y del historial. El
prototipo no se actualiza: ya no coincidía con la app, y una réplica en Figma vuelve a quedar vieja con el próximo cambio. El prototipo navegable es la app publicada. Los
archivos de Figma de las Entregas 1 y 2 siguen enlazados como registro de esas entregas.
