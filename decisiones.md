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

## 2026-10-27 · La capa de uso: navegar como una herramienta profesional

Referencia: stytrix.com (diseño de ropa con IA). Lo que la hace fácil de navegar no es el color sino el orden: un
encabezado de una línea, el menú en letra legible, cada herramienta en una tarjeta con lo que hace y un dato, y un
solo botón oscuro. CICLO tenía el menú en mayúsculas espaciadas de 10,5 px, cuatro vistas escondidas detrás de «Más»
que se desplegaban en la misma línea, y el menú visible durante las tres preguntas de entrada.

**Qué se tomó.** Encabezado fijo de una línea (CICLO, secciones, «Cambiar perfil» como botón negro). Lo que se toca
—menú, botones, filtros— pasa a Archivo de 14 px en minúscula; la mono chiquita queda para etiquetas y datos. «Más»
abre un panel de cuatro tarjetas (qué hace cada vista, un dato con su fuente, «Abrir →»). En el celular, un botón
«Menú» abre la lista entera a pantalla completa. Tarjetas con esquinas y una sombra al pasar el mouse. Una línea
de lectura arriba y un botón para volver. Método pasa de tabla de 26 filas a acordeón: la tabla sigue en el HTML.
Durante la entrada no se ve el menú: un solo camino a la vez.

**Qué no se tomó.** El naranja: en CICLO el color es sólo la señal (Entrar, Esperar, Salir), y unas pastillas o
botones naranjas competirían con ella. Las cifras de marketing sin fuente («80 % más productividad»): cada pastilla
de CICLO lleva un dato real y de dónde sale. Testimonios, precios y newsletter no aplican. La estética de revista
(Bodoni en los títulos, crema, negro y blanco) se queda: el cambio es de uso, no de identidad.

Se desestimó rediseñar todo a lo Stytrix: a una semana de la Entrega 3 dejaba la app y la presentación a medias. La
versión anterior quedó en `diseno/prototipos/versiones_de_la_app/app_2026-10-27_7e5ebfd.html`.

## 2026-10-27 · La presentación pasa a ser un making of

La presentación web tomaba la estética de la referencia de la cátedra (el making of de Valonia) pero no su
estructura: era una presentación de resultados. Ahora cuenta el proceso, alrededor de tres preguntas, cada una con
lo que pedimos, el pivot y lo que quedó en pie: **¿Se puede predecir?** (no: cuatro métodos y VISUELLE; queda leer el
presente), **¿Qué se puede medir?** (2026 contaminado, el trench en abril, toile y el filtro de estación) y **¿Cómo lo
usa un diseñador?** (el paso a paso, la ensalada de frutas, el rojo que volvía, el calzado y la capa de uso).

**Las citas son textuales.** Salen de las transcripciones de Claude Code del 13/10 al 27/10, con la ortografía
corregida y las palabras intactas; «(…)» marca un corte. Las de septiembre no existen: el repositorio y las
transcripciones arrancan en octubre. Lo que no tiene cita va como texto, en tercera persona, sin comillas. Algunos
pedidos son textos largos que se pegaron en la conversación; van como pedidos de Felipe porque así se enviaron.

**Dos correcciones de contenido.** «Validado contra Amazon, Google Shopping y Lyst» no se sostiene: atributo por
atributo, contra Amazon no hay correlación (n = 11). La lámina dice «coincide con Lyst», y los casos de Amazon van a
las notas. «26 términos descartados» tampoco se pudo reconstruir con un criterio único; la lámina habla de toile y
de las sandalias, con sus números.

**Así de simple.** Una idea por lámina, cuerpo de 25 palabras como máximo, tres números como máximo; el resto, en las
notas del orador (tecla N). Monocroma: el color sólo aparece en la lámina que explica la señal.

**Para la Entrega 4.** Todo el contenido es una lista (`LAMINAS`) que se dibuja con los mismos componentes
(encabezado, fila de diálogo, imágenes, visual). Sumar una lámina es agregar un objeto: la numeración, los puntos de
la barra y los links (`#id`) salen solos, y el id no cambia aunque cambie el orden. La versión anterior quedó en
`diseno/prototipos/versiones_de_la_presentacion/`.

## 2026-10-27 · «Gana presencia», en verde

A pedido de Felipe, la palabra y la flecha de «▲ Gana presencia» van en el verde de Entrar, para que se lea de un
vistazo que es buena noticia. Es una excepción acotada a la regla del 26/10 (la tendencia describe en tinta y el
color es de la decisión): sólo cambia el texto de «gana presencia» (El ciclo, las fichas de Diseñar leídas por CLIP).
El mismo día, también a su pedido, «▼ Pierde presencia» pasa al rojo de Salir. «■ Estable» sigue en tinta, y las barras de «Qué gana y qué pierde terreno», también. Verificado
en claro y oscuro. La versión anterior quedó en `diseno/prototipos/versiones_de_la_app/app_2026-10-27_ecf1ad7.html`.

## 2026-10-27 · La hipótesis, reformulada, y la prueba del jurado

**Por qué no se comprobaba.** La hipótesis de la Entrega 1 juntaba tres afirmaciones. Que la pasarela adelanta a la
búsqueda: rechazada a escala anual (13/10). Que se puede predecir: rechazada (cuatro métodos, VISUELLE). Que se puede
identificar la etapa: nunca se puso a prueba, porque no existe una etapa «correcta» con la cual comparar. Las
coincidencias con Lyst eran ejemplos elegidos después de ver el modelo, no una prueba.

**Lyst como prueba formal (B): descartada antes de correrla.** Las 19 señales son todas de subida, sólo dos o tres
corresponden sin interpretación a atributos del K-means (cargo, jeans baggy), las elegimos nosotros y son de años
distintos al corte del modelo (2024), que no se puede recalcular a 2021 o 2022 sin el CSV del Drive. Un p-valor sobre
dos casos sería maquillaje. Lyst queda como ilustración.

**La prueba del jurado (A).** Hipótesis reformulada: el K-means ubica cada atributo en una etapa que coincide con la
que le asignan, a ciegas, personas que trabajan en diseño de moda, más de lo que daría el azar. No dice que sirva
para predecir. Diseño, etapas del modelo congeladas y criterio de decisión en `datasets/jurado/preregistro.md`,
commiteado **antes** de juntar respuestas: si el jurado no se pone de acuerdo entre sí (kappa < 0,20) la prueba no
concluye; si se pone de acuerdo, H se sostiene con p < 0,05 (permutación de las etapas del modelo) y se rechaza si no.
Formulario en `app/jurado/` (no muestra nada de CICLO, orden al azar por persona); evaluación en
`codigo/evaluar_jurado.py`, probada con dos jurados inventados (uno parecido al modelo: se sostiene, p = 0,0001; uno al
azar: no concluye). Las respuestas de prueba no están en el repo.

## 2026-10-27 · La hipótesis, con Reddit: se sostiene para lo que sube

Las entrevistas del jurado dependían de conseguir personas; se buscó un testigo que no las necesitara. Reddit no entra
en el K-means y tiene serie para 14 de los 17 atributos. Preregistro y script commiteados antes de calcular
(`datasets/pruebas/prueba_reddit_preregistro.md`, `codigo/prueba_reddit.py`, commit `0fa8956`); el momento en Reddit
se mide con la misma fórmula que el modelo usa para la búsqueda. Declarado: al buscar los datos se vieron por arriba.

**Resultado: se sostiene (η² = 0,88, p = 0,0013).** Los tres atributos que el modelo pone en ascenso o pico (Y2K,
cargo, jeans baggy) son los tres que más crecen en Reddit. Robustez por rangos, agregada después: p = 0,047. Lo que
**no** se sostiene: retorno y saturada no se distinguen en Reddit (p = 0,88).

**Hipótesis, como queda.** Cruzando pasarela y búsqueda, CICLO distingue los atributos que suben de los que no, y esa
lectura coincide con una fuente que el modelo no vio. No distingue con respaldo externo entre «saturada» y «en
retorno», y no predice. El formulario del jurado, su preregistro y su script se borraron el mismo día (quedan en el historial de git, commit `47b0d61`): la prueba con Reddit los reemplaza.

La prueba con Reddit se suma el mismo día al making of (lámina «Lo que sube, sube afuera», al cierre del arco ¿Se puede
predecir?) y a Método (fila «¿La etapa coincide con afuera?», con lo que se sostiene y lo que no).

## 2026-10-27 · Como si Apple vendiera ropa

**Por qué.** Iván Fardjoume, docente de la cátedra, seguía viendo la interfaz «muy IA». Tres variantes (revista,
revista suave y estudio) no convencieron. Iván nos pasó como referencia https://www.shadcn.io/blocks?page=2, el sitio
donde está el DESIGN.md con el sistema de diseño de Apple (https://www.shadcn.io/design/apple). Sobre esa referencia
Felipe definió qué tenía que ser CICLO: «como si Apple vendiese ropa y un software de hacer ropa encontrando
tendencias, que es lo que es CICLO». Encaja con la tesis de siempre: la interfaz se corre para que hablen las prendas.

> **Atribución corregida el 03/11/2026.** Esta entrada decía «Felipe eligió el sistema visual de las páginas de
> producto de Apple». La referencia vino de la cátedra (Iván), y lo nuestro es la adaptación: qué se tomó, qué no y cómo
> se implementó. Las capturas de la referencia están en `diseno/referencias/`.

**Qué cambió.** Una capa nueva al final del CSS («capa Apple»): tipografía del sistema (SF Pro en Mac e iPhone, Inter
en el resto), lienzo gris perla #f5f5f7, tarjetas blancas de 18 px sin sombra, títulos centrados en semibold con
bajada como tagline, ningún rótulo en mayúsculas espaciadas, píldoras, encabezado fino y translúcido, Diseñar como un
configurador (lo elegido, con borde azul) y un bloque oscuro para «qué gana y qué pierde terreno». Las fichas de
Tendencias pasan a ser tarjetas separadas. Siempre en claro: `data-theme="light"` apaga el oscuro automático. La
presentación toma el mismo estilo y suma una lámina con este pivot.

**La regla de color, ampliada.** Hasta hoy el único color de interfaz era la señal. Ahora hay uno más, el azul
(#0066cc), y significa una sola cosa: «se puede tocar». Verde, ámbar y rojo siguen siendo sólo la señal, con su palabra.

**Lo que no se tomó.** Ni el logo ni el nombre de Apple: es su sistema, no su marca. Ni su fotografía de producto: las
fotos de pasarela no tienen licencia, así que las prendas siguen dibujadas.

Versiones anteriores: `diseno/prototipos/versiones_de_la_app/app_2026-10-27_c639966_antes_de_apple.html` y
`diseno/prototipos/versiones_de_la_presentacion/`. Capturas regeneradas; la del modo oscuro se reemplaza por el panel «Más».

## 2026-10-27 · De Tendencias a Diseñar, en un clic

Tendencias era para mirar; ahora es la puerta a diseñar. Todo lo que muestra abre su ficha con el gráfico de su
serie: las 12 fichas, las barras de «qué gana y qué pierde terreno» (llevan al recorrido de El ciclo) y los colores de
cada ficha. Arriba del gráfico, un botón «Diseñar con este corte / material / estampa / color · nombre →».

**Cómo entra.** El botón arma el mismo estado `dz` que el recorrido a mano y entra por `mostrar('disenar')`; nada de
camino paralelo. Lo clickeado queda como atributo fijo (`dz.fijo`), con una línea arriba de los pasos y «Quitar ×».
Un corte abre en pantalones → largo → ese corte y sigue desde el tiro; un material, una estampa o un color abren en el
paso de prenda, con sólo las prendas (y los tipos) que lo admiten, y su propio paso se saltea. Al cambiar de prenda,
el fijo se vuelve a aplicar. El link de Diseñar ahora lleva el estado (`dz`, `paso`, `fijo`): se comparte igual que
el de una ficha.

**De qué hoja sale cada cosa.** Las 65 series encuentran su hoja por los campos que ya tenía la taxonomía (`rec`,
`serie`, `km`, `clip_jeans`); «Buzo / athleisure» va a la prenda Buzos. Los tres grupos de corte de Tendencias (amplio,
recto, ajustado) abren en su corte más buscado (baggy, straight, skinny) y el botón lo nombra. «Corazones» y
«Geométrico» no están en el vocabulario de Diseñar: su ficha lo dice en lugar del botón.

## 2026-10-27 · El chat no se queda en el «no lo tengo medido» (prompt v4)

A «¿qué material está de moda ahora?» el chat contestaba que no lo tenía medido y ahí terminaba. Dos causas, y se
arreglaron las dos.

**Los datos no le llegaban.** Las señales de materiales sólo entraban si ya había una prenda armada, y la sección de
colores por corte de `ciclo_datos.md` no entraba nunca. Ahora, ante una pregunta general por material, estampa, corte,
tiro o detalle sin diseño, recibe los cinco que más suben y los tres que más caen con dato propio; y recibe los colores
del corte o la prenda que nombra. `ciclo_datos.md` se regeneró: el corte de 2024 trae sus números (69 de 70 series, el
trench en abril), y de paso recogió el arreglo de los jeans por corte del 26/10, que no había llegado al archivo.

**El prompt lo mandaba a decir que no.** v4 (`prompts/prompt_asistente_v4.md`): nunca decir que se tiene un dato que
no se tiene (cada número tal cual, con su unidad: si DATOS dice puntos, son puntos); y nunca quedarse en el «no»: decir
qué falta y contestar con lo más cercano con la jerarquía de préstamo de la app (hermano → padre → atributo suelto),
diciendo qué se muestra en lugar de qué. «Ahora» o después de 2024: el corte en una frase y lo último medido. Siempre
termina en algo accionable. Sólo sin nada cercano dice que no y ofrece una pregunta parecida.

**Prueba.** `codigo/probar_asistente.js` hace seis preguntas reales a la app (material ahora, color para un jean
baggy, botinetas, 2027, falda de cuero, lunares). Necesita una clave de Groq; las respuestas van a
`datasets/pruebas/asistente_v4_respuestas.md`.

## 2026-10-27 · El estado de la hipótesis, en un solo lugar

`hipotesis.md` ordena en tres columnas lo que nos van a preguntar: verificado (Reddit con prueba formal y CLIP; Amazon,
Google Shopping y Lyst como casos coherentes sin prueba formal, y por qué no alcanzan), refutado (los cuatro métodos, el
modelo global, VISUELLE, el adelanto anual de la pasarela) y sin probar (el adelanto por temporada). Al armarlo se
corrigió una afirmación: el corset de Lyst coincidía con el modelo de septiembre, de 18 atributos; el K-means de hoy no
lo tiene. La prueba por temporada no puede ser mes a mes del lado de la pasarela: Vogue trae temporada y año, no la
fecha del desfile.

## 2026-10-27 · La primera impresión de un diseñador: ocho detalles

Recorrido con Playwright como alguien que entra por primera vez. Se arreglaron los ocho, en orden de impacto:

1. **La clave de Groq ya no aparece en el medio.** En Preguntar es «Activar el chat · 1 minuto», arriba de todo, con
   tres pasos (entrar a console.groq.com con Google, crear la clave, pegarla); con la clave puesta queda en una línea.
   Si preguntás sin clave, se abre sola. En el recorrido, «Pedir lectura en vivo» es un solo botón y los pasos aparecen
   recién al tocarlo.
2. **Las tarjetas de Tendencias, sin jerga.** Dibujo, paleta, nombre, tipo y la pista de la etapa con su fuente; las
   cifras, la mini-serie y «5/60 meses» quedan en la ficha. Que la paleta es de un catálogo de demostración se dice una
   vez, en la nota de abajo de la grilla, en vez de en cada tarjeta.
3. **La bajada de Tendencias dice qué hacer:** «Tocá cualquiera para ver su recorrido y diseñar con él».
4. **Diseñar:** el título más chico, para que «¿Qué prenda?» quede a la vista.
5. **Marcas:** las tres dimensiones nuevas de Lyst, en tres tarjetas (estaban sueltas, renglón por renglón).
6. **Método:** «Cómo leer los colores» decía «negro, crema y blanco». Ahora explica el azul y el verde y rojo de
   gana y pierde presencia.
7. **El modelo:** los grupos del K-means usaban el verde, el naranja y el ámbar de los gráficos, y «Pico» en verde se
   confundía con «Entrar». Ahora tienen tonos propios que no son ni la señal ni el azul (violeta, rosa, pizarra, marrón).
8. **La entrada:** las tres opciones, centradas bajo la pregunta.

Capturas del readme e imágenes de la presentación regeneradas.

## 2026-10-27 · El chat, probado con seis preguntas reales: v4 no alcanzó, v5 sí

Con la clave de Groq del grupo se corrieron seis preguntas reales sobre la app (`codigo/probar_asistente.js`, con un
minuto entre preguntas por el límite del plan gratis). v4 usaba bien los datos pero ignoraba la mitad de las reglas:
no explicaba el corte de 2024, a botinetas y a 2027 contestaba «no tengo datos» y ahí terminaba, decía «48 % de las
búsquedas» de un color que es el 48 % de los looks de pasarela leídos por CLIP, y ordenaba mal lo que más cae.

**v5** (`prompts/prompt_asistente_v5.md`): la respuesta con un orden explícito (qué falta o el corte → lo más cercano
con su número y su fuente → qué sube y qué cae → qué hacer), tres ejemplos con letras en vez de números, la fuente de
cada número por nombre y sin ids, y el calzado sin préstamo entre estilos (se ofrece preguntar por los que sí se miden).
Y en los datos, no en el prompt: una sección «Qué sube y qué cae» ya ordenada (el modelo lee el orden en vez de
ordenar) y la etiqueta de los colores que dice que son looks de pasarela, no búsquedas.

**Resultado** (`datasets/pruebas/asistente_v5_respuestas.md`, sin editar): las seis contestan con un dato real y su
fuente o explican por qué no lo hay y ofrecen una alternativa; ninguna inventa un número. Quedan dos imperfecciones: un
id que se cuela en una respuesta y un «vuelve» con −3 puntos que exagera lo que dice el dato. El modelo no es
determinista: la prueba se puede repetir con el mismo script.

## 2026-10-27 · La pasarela, temporada a temporada: tampoco adelanta

La última afirmación de la hipótesis original que seguía viva. A escala anual la pasarela no adelantaba a la búsqueda,
pero un adelanto de seis a nueve meses cabe adentro de un año y con datos anuales no se podía ver. Se probó por
temporada, con el diseño, las etiquetas y el criterio commiteados antes de tener la búsqueda mensual
(`datasets/pruebas/prueba_temporada_preregistro.md`, commit `613352c`; enmienda 1 con los lotes bajados y antes de
calcular, `751c22d`).

**Cómo.** Vogue Runway (903.000 looks, 2003–2023) agregado por temporada; cada temporada ubicada en el mes de su desfile
por calendario, porque Vogue no trae la fecha. Búsqueda mensual de Google Trends (plan 4: tres lotes nuevos, más cinco
términos que ya estaban). Todo contra el mismo momento del año anterior, para que la estación no parezca un adelanto.
Spearman por atributo a 0, 3, 6, 9, 12, 15 y 18 meses; la mediana entre atributos contra 10.000 barajadas; Bonferroni
por siete rezagos (α ≈ 0,007).

**Resultado: se rechaza.** Entraron 14 atributos (Lunares, afuera por pocos looks; Floral no se exportó). De 3 a 18
meses las medianas van de −0,04 a +0,04, con p entre 0,13 y 0,86, y atributo por atributo no hay patrón. Sólo asoma el
rezago 0 (+0,08, p = 0,026, no pasa la corrección): las capas se mueven juntas. Con esto, la hipótesis queda cerrada:
CICLO lee el presente cruzando capas y distingue lo que sube de lo que no (Reddit); no predice y la pasarela no
adelanta, ni por año ni por temporada. Está en `hipotesis.md`, en Método y en el making of (lámina «Tampoco por
temporada»).

## 2026-11-03 · De Figma al código, dicho como fue

El criterio 4 de la Entrega 3 pide presentar el Figma pasado a código. **La app no se construyó leyendo el Figma**: se
escribió directo en código con Claude Code, y el prototipo de Figma del 05/10 ya era distinto de la app de ese día (sans
serif y pastillas contra la revista en Bodoni). En vez de reconstruir un proceso que no pasó, `entregas/entrega_3/figma_a_codigo.md`
cuenta qué había en Figma, que el MCP de Figma se usó recién el 03/11 y sólo para leer el archivo y sacar capturas, qué se
decidió en el código sin pasar por Figma (estados, celular, carga de CLIP, once casos de error, el oscuro apagado) y ocho
diferencias con la devolución o el dato que provocó cada una. Cinco pares de capturas, Figma a la izquierda y la app a la
derecha, en `entregas/entrega_3/figma_a_codigo/`.

Dos cosas que salieron al escribirlo: CLIP no pesa 8 MB sino 89 (el índice es el de 8), y el registro no dice cómo se armó
el Figma; los nombres de capa (`screen:*`, `go:*`) sugieren un script, y así queda dicho, sin afirmarlo.

## 2026-11-03 · La presentación, en el orden de los criterios

El criterio 5 pide presentar en 15 minutos la app y los puntos 2, 3 y 4. El making of estaba armado alrededor de tres
preguntas (predecir, medir, usar) y no tenía ni el system prompt en pantalla ni lo de Figma. Se mantiene el diseño (a
Felipe le gusta tal como está) y se reordena el contenido en cinco bloques con su tiempo: hipótesis 2, datos 3, IA 3,
Figma al código 3, demo 4. «Making of» sale del título.

**Lo que tiene que verse y no sólo decirse.** El system prompt entero, como texto (el mismo de `prompts/prompt_asistente_v5.md`
y de `AS_INSTR` en la app, verificado línea por línea), con las reglas clave en negrita; qué recibe, con una línea real
de `ciclo_datos.md`; qué devuelve, con una respuesta real sin editar de la prueba del 27/10. Los límites como cobertura,
sesgos y ausencias, cada uno con cómo afecta, y dos ejemplos: el corte en 2024 (el trench) y el calzado.

**Firma.** La presentación la firma sólo Felipe, que presenta solo. El QR y el link quedan en la lámina de la demo.

**En el celular** las láminas con texto y un bloque a la derecha se encimaban, y una ruta larga ensanchaba la página:
ahora cada lámina es una columna que se desliza. Verificado con Playwright, 19 láminas a 1440 y a 393, sin errores.

## 2026-11-03 · Verificación antes de la entrega

Contra la app publicada, con Playwright, en un contexto limpio (sin caché ni localStorage, como incógnito):

- **El QR** (`entregas/entrega_3/ciclo_qr.png`, leído con jsQR) apunta a https://felipeberney-boop.github.io/ciclo/, que
  responde 200. La presentación publicada ya es la nueva. El repositorio es público y el readme tiene arriba la app, la
  presentación, el QR y el repositorio.
- **La demo entera**, a 1400 y a 393 px: entrada (mujer, marca, high fashion) → Tendencias → ficha de Amplio (Pico,
  ■ Esperar) → «Diseñar con este corte» (entra con el baggy fijo, en el tiro) → la ficha (Esperar) → Preguntar →
  Buscar por imagen con el look Denim. Los cinco pasos pasan, sin errores de JavaScript ni scroll horizontal.
- **La carga.** Primer pintado con contenido a 0,7 s en escritorio y 0,25 s en el celular emulado; al abrir hay 3
  pedidos y 266 KB. **CLIP no se baja al abrir**: el índice (8 MB) baja con la primera consulta y el modelo (89 MB) sólo
  con una foto propia. No hubo nada que arreglar. (El pedido decía «los 8 MB de CLIP»: son 89 de modelo más 8 de índice.)
- **El chat sin clave** no llama a Groq: abre «Activar el chat» y dice «Primero activá el chat: son tres pasos…». Con
  una clave inválida, «Groq rechazó la API key…»; sin conexión, «No hubo conexión con api.groq.com…». No se probó una
  respuesta real: no había clave en esta máquina.

El guion de la demo pasa a 4 minutos y cinco pasos, con el salto de Tendencias a Diseñar y el mensaje real sin clave.

## 2026-11-03 · El criterio 4, en un Figma de tres etapas, y la referencia de Iván

**La atribución, corregida.** La entrada «Como si Apple vendiera ropa» (27/10) decía que Felipe había elegido el sistema
de Apple. No fue así: Iván Fardjoume vio la interfaz «muy IA» y pasó como referencia https://www.shadcn.io/blocks?page=2,
el sitio donde está el DESIGN.md de Apple (https://www.shadcn.io/design/apple). La referencia es de la cátedra; la
adaptación (qué se tomó, qué no y cómo quedó en el código) es nuestra. Se corrigió la entrada con una nota fechada, y
también historial, readme, la nota del CSS y CLAUDE.md. La devolución del 13/10 («un mar de datos») fue de Cristian
Reynaga. Las capturas de las dos páginas de la referencia quedaron en `diseno/referencias/`, como fuente. Coinciden
valor por valor con la capa: #f5f5f7, #0066cc, #0071e3, #272729, #7a7a7a, #e0e0e0, #f0f0f0, 18 px, 17 px, Inter de
respaldo.

**El archivo de Figma.** «CICLO · Del diseño al código» (https://www.figma.com/design/4lvJEf2ZjBX87sXEySXqa7), una página
por etapa. La 1 es el diseño original, con capturas del prototipo de la Entrega 2, láminas y propuestas, cada una con su
fecha. La 2 tiene la devolución, la referencia capturada, las tres variantes que no convencieron y lo que se tomó y lo
que no. La 3 es el sistema implementado, generado desde `app/index.html` con el MCP de Figma: 16 colores y 3 radios como
variables, 24 estilos de texto, los componentes y Tendencias, Diseñar y Preguntar a 1400 y 393 armadas con instancias.

**Tres cosas que no salieron como se pidieron, y por qué.**
- El «salmón de interpretado» no existe desde el 20/10: la variable lleva el valor real, gris, con esa nota.
- El texto va en Inter y no en SF Pro, porque SF Pro es local y no se ve en otras computadoras; es también el respaldo
  de la app.
- Las tarjetas de estampas y materiales llevan el color de la tela en vez de su dibujo; la de rayas sí está dibujada.

**Sobre el MCP de Figma.** Las sobrescrituras de tamaño y posición dentro de una instancia se ignoran sin error. Por
eso la etapa de la tarjeta de Tendencias es una propiedad de variante (5 etapas × 2 dibujos), y la barra de la fila
oscura es una variante por valor, que escala con el ancho de la fila.

**La presentación.** El bloque de Figma pasa a ser el recorrido de las tres etapas, con el link al archivo, la
referencia y los pares. Los límites quedan en una sola lámina corta con sus dos ejemplos (el corte en 2024 y el
calzado), y en la hipótesis va primero lo que se sostiene.

## 2026-11-03 · Netlify, otra vez

La cátedra acepta Netlify o Vercel. Netlify, pausado desde octubre por falta de créditos, volvió a aceptar deploys en
noviembre, así que no hizo falta pasar a Vercel. `netlify.toml` deja de redirigir a GitHub Pages: publica la carpeta
`app/` tal cual. https://ciclo-udesa.netlify.app sirve el mismo HTML que GitHub Pages (más un comentario y un script que
Netlify agrega). GitHub Pages sigue siendo la URL oficial, la del QR. El deploy de Netlify es a mano:
`npx netlify-cli deploy --prod --dir app`.

## 2026-11-03 · La hipótesis, contada por lo que funciona, y sólo lo que pide la consigna

**La hipótesis ajustada, en positivo.** «Cruzando lo que propone la pasarela con lo que busca la gente, CICLO ubica cada
atributo de moda en su etapa del ciclo y distingue lo que está subiendo de lo que no. Esa lectura coincide con fuentes
que el modelo nunca vio.» La lámina pone adelante lo comprobado: Reddit (p = 0,0013), Lyst, Amazon, CLIP (AUC 0,90) y
116 de 133 opciones de Diseñar con serie. Lo que cambió se dice en una línea: de «tendencia» a atributo, y de anticipar
a leer el presente. Lo refutado sigue completo en `hipotesis.md` y en las notas, por si lo preguntan. Lo mismo en
`hipotesis.md` y el readme.

**Fuera lo que no pide la consigna.** Salen «Lo que sube, sube afuera» (la prueba de Reddit queda dentro de la lámina
de la hipótesis), «Tres modelos» (pasa a las notas del system prompt), «Lo que Figma no pregunta» (queda una línea en
«Del diseño al código» y el detalle en `figma_a_codigo.md`) y la lámina de cierre (el repositorio y el QR ya están en la
demo). Quedan 14 láminas. Abril vuelve a la firma: sigue en el grupo.

## 2026-11-03 · La entrada, sólo con lo que se clickea, y el recorrido en el readme

**Devolución de la presentación.** El profesor dijo que las primeras pantallas tenían demasiado texto y confundían.
Regla para las tres preguntas: cada tarjeta muestra sólo lo que hay que clickear. Salen las bajadas de cada pregunta,
las explicaciones de cada tarjeta («en relación de dependencia…», «freelance, por encargo…», «Womenswear»…), los
ejemplos de marcas, la ficha de lead time, ventana, error y señales de cada categoría, y el párrafo de los 1,28
millones de looks. Las etiquetas quedan en cuatro palabras o menos («High fashion / couture» pasa a «High fashion»,
«Emergente / de autor» a «De autor», «Streetwear / fast fashion» a «Streetwear»).

**No se borra: se mueve.** Todo eso está ahora en Método, en «La entrada: qué cambia cada respuesta», con las dos
tablas de categorías (para una marca y por tu cuenta) calculadas de `PERFIL` y `consejo()`, las mismas fuentes que
usaba el gate.

**El readme.** El recorrido completo, una captura por paso: las tres preguntas (con las dos ramas de la categoría),
dónde cae, Tendencias, la ficha, «Diseñar con…», Diseñar con el atributo fijo y Preguntar; el gate y Diseñar también a
393 px. Las saca `codigo/capturar_recorrido.js` con clicks de verdad, sin perfil guardado. Arriba de todo, la app, la
presentación y el QR (criterio 5).

**Después, dos arreglos que salieron del recorrido.** Tendencias dice debajo del título con qué perfil está leyendo
(«Tu perfil: Mujer · Para una marca · Fast fashion · Cambiar»): antes el perfil recién se veía en la ficha. Y Preguntar
leía como vacío un diseño que llega desde una ficha («Diseñar con esta estampa · Rayas»), porque todavía no tiene
prenda; ahora toma el atributo fijo como diseño y le dice al modelo que falta la prenda.

**Las capturas de la presentación, al día.** El lado «App» de los pares Figma | App (entrada, Tendencias, ficha,
celular), la portada (`tendencias`) y la ficha con su procedencia se rehicieron con la app de hoy: la entrada ya sin
bajadas y Tendencias con el perfil. El lado Figma y las referencias de antes (revista, Apple, la tarjeta en Figma) no se
tocan, porque cuentan la historia. Las saca `codigo/capturar_presentacion.js` y las arma
`codigo/armar_capturas_presentacion.py`.

## 2026-11-03 · La presentación, una lámina por criterio, y la demo primero

**Devolución de Cristian en la presentación.** Mostrar primero el flujo de la app, y láminas más simples: confundían.

**Qué queda.** Seis láminas, una por criterio de la rúbrica: portada (con el QR), la hipótesis (1), los datos (2), la IA
(3), del diseño al código (4) y el cierre con la app, el repositorio y el Figma (5). La demo en vivo, de siete minutos,
va entre la portada y la hipótesis, y es la prueba del criterio 1: una diseñadora toma una decisión que antes no podía
tomar bien. Regla: una idea por lámina, hasta 25 palabras de cuerpo y tres números, sin achicar la tipografía; la de la
IA es la excepción, porque el system prompt tiene que leerse.

**La evidencia de la hipótesis.** El K-means pone los jeans ajustados en «saturada» y los amplios en «pico» sólo con
pasarela y búsqueda; en reseñas de Amazon 2019–2022 los ajustados caen 39 % y los amplios suben 79 % (+95 % en Google
Shopping). Son los mismos números de `app/llm/ciclo_datos.md`.

**La IA ya no está repartida en tres láminas.** Una sola muestra la regla del system prompt, una línea real de lo que
recibe y el JSON que devuelve, con la regla grande: el modelo nunca ve una fila de datos.

**Todo lo demás pasa a Respaldo**, después del cierre: Reddit, la decisión, los cuatro métodos de predicción, VISUELLE,
2025 y 2026, el calzado, el K-means, las fuentes, la procedencia, el prompt entero, lo que recibe, una respuesta real, la
referencia, las diferencias con el Figma, lo que Figma no pregunta y cómo se hizo. La versión de catorce láminas quedó en
`diseno/prototipos/versiones_de_la_presentacion/presentacion_2026-11-03_cba39cc_catorce_laminas.html`.

**El guion.** `presentacion_guion.md` pasa a ser `guion_demo.md`: el reparto (1 + 7 + 5 + 2 minutos), qué decir en cada
paso de la demo, la pregunta exacta (¿Qué color va con un jean baggy?, probada el 27/10 con el mismo diseño), el plan B y
dónde cortar. `codigo/probar_demo.js` hace los siete pasos con clicks de verdad; el 03/11 pasaron los siete, con la
llamada a Groq cortada a propósito para probar el plan B.

## 2026-11-03 · La presentación termina en el Cierre

La sección «Respaldo» no se usaba: sale entera, con su navegación, su CSS, los visuales que sólo dibujaba ella y las
20 capturas que ya no muestra ninguna lámina (siguen en el historial de git). Quedan seis láminas exactas: Portada, La
hipótesis, Los datos, La IA, Del diseño al código y Cierre; el contador termina en 06 / 06 y la última flecha se queda
en el Cierre. `codigo/capturar_presentacion.js` saca ahora sólo la captura de Tendencias, la única de la app que usa.

Antes de borrar se revisó que cada dato de esas láminas siguiera en el proyecto: en Método (Reddit, los cuatro métodos,
2025 y 2026, el calzado, el K-means, las fuentes), en este registro (VISUELLE, el conteo 74 / 42 / 17 de las opciones de
Diseñar, los valores de la referencia), en `figma_a_codigo.md` (las diferencias con el Figma, lo que se decidió en el
código), en `prompts/` y `datasets/pruebas/` (el prompt y una respuesta real) y en `preguntas_probables.md` (los tokens
por pregunta). Lo único que estaba sólo en las láminas era el tamaño del documento que lee el modelo, y queda acá:
`app/llm/ciclo_datos.md` pesa 62 KB (62.382 bytes), pero no viaja entero: por pregunta van lo general y las fichas que
nombra la conversación, entre 3.600 y 4.600 tokens. El gráfico de commits por día del making of salía de `git log`.

## 2026-11-04 · La entrada pregunta por la decisión, no por el vínculo

**Devolución de la Entrega 3 (Cristian).** «Trabajo para una marca / soy independiente» puede no representar los
objetivos reales del usuario: hay que pensar si son las mejores palabras para la ramificación.

**Lo que miramos antes de elegir.** En la app, el vínculo cambia una sola cosa: donde la regla dice Esperar, «por mi
cuenta» dice Explorar, porque no compromete stock (`consejo()`). La categoría cambia dos cosas que el lead time no cubre:
la ventana (cuánto tiene que seguir actual la prenda: 1, 2, 3 o 5 años) y el posicionamiento (en pico, fast fashion entra
y la marca de autor sale, aunque tenga un lead time más corto que high fashion). El error medido depende de la ventana, no
del lead time: todos los lead times caen en menos de un año y el error se mide año a año.

**Tres variantes, y la que elegí.**
1. *El alcance* · «¿Qué estás por decidir?» → Una colección · Una prenda · Si algo sigue vigente. Descartada: colección
   o prenda no mueve ningún número; habría que inventar ventanas que chocan con la categoría.
2. *El compromiso* · «¿Qué estás por decidir?» → Qué diseñar · Qué producir · Si algo ya pasó, y «¿Para qué tipo de
   marca?» con las cuatro categorías para todos. **Elegida.** Explorar pasa a colgar de «Qué diseñar» (un diseñador en
   relación de dependencia que busca ideas también explora); «Si algo ya pasó» mira hacia atrás, con los mismos datos
   ordenados por lo que ya pasó; la categoría queda en una sola pregunta en vez de dos ramas. `CONSEJO`, `PERFIL` y el
   error no cambian.
3. *El plazo* · «¿Para cuándo lo necesitás en tienda?» y «¿Cuánto tiene que durar?». Descartada: da la ventana directo,
   pero pierde el posicionamiento y obliga a reescribir `CONSEJO`.

La propuesta de las tres variantes y la recomendación fueron de Claude; la elección es mía, con un cambio de palabras
(«Si algo sigue vigente» pasa a «Si algo ya pasó»).

**Primero en papel.** Antes de tocar el código, las pantallas del flujo nuevo, una por hoja A4, para corregir en clase:
página «4 · En papel · Entrega 4» del Figma de tres etapas y
`entregas/entrega_4/disenos_en_papel/ciclo_disenos_en_papel_entrega_4.pdf`. Trece hojas: el mapa del recorrido, las
tres preguntas, Tendencias para «Qué producir», «¿Sigue vigente?» para «Si algo ya pasó», la ficha, un paso de Diseñar
con Explorar, Tu diseño, El ciclo, Buscar por imagen, Preguntar y una hoja nueva, «Los datos», que responde al «qué
datos, para qué y cómo conviven»: cuatro fuentes, la clave atributo × año, el K-means y lo que sale (etapa, señal, cono).
Cada hoja dice de dónde viene y adónde va.

**Ya con cinco estilos de texto.** El Figma tenía 24 estilos; las hojas usan sólo cinco, nuevos: Título (56), Subtítulo
(28) y Dato (40), en Semi Bold, y Cuerpo (20) y Etiqueta (15), en Regular. Un peso por tamaño. Es la propuesta para la
auditoría tipográfica de la app, que viene después. El contenido es real: los números salen de `REC`, `PERFIL`,
`CONSEJO` y de las capturas de la app. Preguntar no muestra una respuesta inventada: tiene líneas grises donde va.

**Ya en la app, el mismo día.** Las tres preguntas están en `app/index.html` (`DECISION`, `GATE_CAT`, `decision` en vez de
`vinculo`). Qué diseñar entra a Diseñar y convierte Esperar en Explorar; Qué producir entra a Tendencias; Si algo ya pasó
entra a Tendencias con el título «¿Sigue vigente?» y las tarjetas en dos grupos, «Ya pasó» (las que dan Salir) y
«Todavía vigente». Las tarjetas de Tendencias muestran ahora su señal, que antes sólo estaba en la ficha. Los links y
los perfiles guardados de antes siguen andando: `v=propia` se lee como Qué diseñar y `v=marca` como Qué producir. Los
dos prompts que nombraban el vínculo pasan a versiones nuevas (`prompt_lectura_recomendacion_v5.md`,
`prompt_asistente_v6.md`); sólo cambia la línea de quién pregunta, y no se probaron en vivo porque no había una clave a
mano. Método explica las tres preguntas con dos tablas: para producir o revisar, y para diseñar.

## 2026-11-04 · Qué datos, para qué y cómo conviven, en un esquema

**Devolución (Cristian, «fundamental»).** Tiene que quedar claro qué datos usamos, para qué y cómo conviven en el modelo.
Estaba repartido entre Método, la ficha, el readme y este registro.

**Decisión.** Método abre con un esquema de tres columnas, el mismo de la hoja 12 del papel: cuatro fuentes y qué aporta
cada una; la clave con la que se cruzan (atributo × año) y el K-means; lo que sale (la etapa, la señal y el cono). Las
fuentes que no entran al modelo (Reddit, la venta y Lyst) van con borde gris en vez de relleno, para que se vea de un
vistazo qué alimenta al K-means y qué sólo valida. Sin color nuevo: el color sigue siendo sólo la señal. En el celular,
las columnas se apilan y las flechas apuntan hacia abajo.

## 2026-11-04 · Cinco estilos de texto

**Devolución (Cristian).** Las pantallas tienen múltiples estilos y tamaños tipográficos, y eso confunde.

**Lo medido.** Con Playwright, el tamaño y el peso calculados de cada texto visible de las once vistas, con los
desplegables abiertos: **31 tamaños distintos** (de 8,5 a 64 px), 49 combinaciones de tamaño y peso, cuatro pesos (400,
500, 600 y 700) y 13 combinaciones más en los gráficos. El Figma del sistema tenía 24 estilos de texto.

**Lo que queda.** Cinco estilos, un peso por tamaño:

| Estilo | Tamaño | Peso | Qué va |
|---|---|---|---|
| Título | 48 (34 en el celular) | 600 | Uno por pantalla: la pregunta o el nombre de la vista |
| Subtítulo | 24 | 600 | Nombre de tarjeta, de bloque, de atributo |
| Dato | 34 | 600 | Números y la palabra de la señal cuando va grande |
| Cuerpo | 17 | 400 | Lo que se lee para decidir, las opciones, los botones |
| Etiqueta | 13 | 400 | Rótulos, procedencia, menú, tablas, ejes de los gráficos |

En el papel (página 4 del Figma) van un 15 % más grandes para que se lean impresos: 56, 28, 40, 20 y 15.

**Cómo se hizo.** Una quinta capa de CSS, la última, que pisa a las otras cuatro. Sus selectores no salen de leer el
CSS sino de medir la app: cada texto se asignó a un estilo por su tamaño y su rol (lo de 44 o más que es h1 o la pregunta
de Diseñar es Título; los números y la señal grande son Dato; lo de 16,5 o más en Semi Bold es Subtítulo; lo de 15,5 o
más, Cuerpo; el resto, Etiqueta). El `<b>` dentro de un párrafo hereda el peso del párrafo: un énfasis en negrita era
una combinación más. Los gráficos son SVG que se escalan con su `viewBox`, así que un rótulo de 9,5 se veía de 8 o de
16 según el ancho; `etiquetasSvg()` lo deja en 13 px de pantalla, recalculado cuando cambia la vista o el ancho.

**Medido después.** 5 estilos en el texto y 1 en los gráficos, en escritorio y en el celular. La única excepción es el
logo CICLO (19, Semi Bold), que es una marca y no un estilo de texto.

**Lo que esto no arregla.** El tamaño ya no compite, pero el texto sigue siendo mucho: eso es la curaduría, aparte.

## 2026-11-04 · Curar el texto: lo que decide, lo que aclara y lo que sobra

**Devolución (Cristian).** Muchas capas, algunas útiles y otras sólo aclaraciones de uso, que no parecen conectadas;
parece que no hay filtro sobre lo que da la IA y hay que leer muchas cosas que no aportan valor por igual.

**Cómo.** Cada bloque de texto de cada pantalla, en uno de tres grupos: (a) lo que se necesita para decidir, se queda;
(b) aclaración de uso, pasa a un «?» que se abre si lo tocan o a Método; (c) nada, se borra. El «?» es un solo
componente (`details.qm`), un círculo gris que se vuelve azul al tocarlo, porque el azul es lo que se toca.

**Lo que se fue (c).** El rótulo «0N · Vista» arriba de cada título, que repetía el menú. En Tendencias, la bajada
«Lo que está ganando y perdiendo terreno afuera… Tocá cualquiera…» y el «12 de 12 atributos». En la ficha, «Recomendación
· tu marca · fast fashion» (repetía el perfil) y los cuatro recuadros Color / Proporción / Material / Precio, que casi
siempre decían «— · no aplica». En Diseñar, el título «Diseñá con lo que se mueve afuera» con su bajada (la pregunta del
paso es el título) y la descripción de cada prenda («De la cintura para abajo, con dos piernas»): el dibujo ya lo dice.
En El ciclo, «Para vos · … · recomendación · interpretación». En Buscar por imagen, «Todavía no hay imagen…» y «jpg · png
· webp…». En Preguntar, el globo vacío «Armá algo en Diseñar o subí una foto…», que repetía la tarjeta y además
llevaba la marca de «interpretado · LLM» sin ser del modelo.

**Lo que pasó al «?» (b).** Cómo leer las tarjetas de Tendencias y qué mide «gana y pierde terreno»; en la ficha, el
porqué largo de la señal, los datos del catálogo, la lectura del equipo y los pies de los gráficos; las aclaraciones
de cada paso de Diseñar («El jean no es una prenda…»); qué es un pico en El ciclo y el porqué de su señal; cómo funciona
CLIP y cómo se validó (el «acierta en el top 3 el 86 %» que se repetía debajo de cada atributo va una sola vez); cómo
lee los datos Preguntar.

**Lo que se queda y cambió (a).** La señal se ve con una sola línea de por qué (`señal()` devuelve ahora también
`corto`: la frase de la regla, o «Gana presencia afuera: +12 puntos…»), y el resto va al «?». La procedencia en las
tarjetas pasa a «● K-means» o «◇ estimada». Buscar por imagen se llama igual que en el menú (antes, «Mandá una
prenda»). «sin validar» se sigue diciendo donde corresponde: es (a), no se esconde.

**Lo que no se tocó todavía.** Las pantallas de «Más» (El modelo, Marcas, Retornos y Método) sólo perdieron el rótulo de
arriba. Para ellas quedan propuestas que no son de texto sino de estructura, y las decide Felipe: El modelo entero a
Método, Retornos como un filtro de El ciclo, y Marcas fuera del menú porque no entra al modelo.

## 2026-11-04 · El repositorio, al día

La devolución pidió el repositorio completo y sincronizado. El readme abre con dos líneas de qué es y para quién, y el
recorrido paso a paso se rehízo con la entrada nueva (`entregas/entrega_4/recorrido/`, `codigo/capturar_recorrido.js`;
el de la Entrega 3 queda como estaba). Se borró `netlify/functions/`: desde el 25/10 la app llama a Groq desde el
navegador y esa función no la usaba nada; está en el historial de git. En historial.md, «Lo que falta» y «Dónde ver cada
versión» llegan a la Entrega 4. `prompts/readme.md` tenía la tabla parada en el asistente v3 y decía que IA-5 usaba una
clave en Netlify; ahora lista hasta v6 y dice cómo es. `codigo/diseno_catalogo.json` se queda: lo leen
`armar_diseno.py` y `calcular_textos_diseno.mjs`. La entrada ya no dice «Lo podés cambiar después».

## 2026-11-04 · El racional, en borrador

`entregas/entrega_4/racional.md` tiene los ocho ítems de la consigna, reorganizados para alguien que no cursó: no
repite decisiones.md, lo ordena por pregunta (qué problema, qué hipótesis, qué datos, qué modelo, qué usuario, qué
diseño, qué recorte, qué proceso). El ítem 1 trae ejemplos reales de cómo decide hoy la industria, buscados el 04/11:
los briefs de compra de WGSN, el tablero de Heuritech (Dior y el bolso Miss Dior), el de Tagwalk, los foros de
Première Vision (de 18 a 24 meses antes) y el circuito tienda-diseño de Zara (Harvard Business Review, 2004). Lo
que es promesa del vendedor se dice. Lo que no se pudo verificar en la fuente primaria no entra: el número de
2.500 a 5.000 millones de prendas sobrantes en 2023, atribuido al *State of Fashion 2025*, aparece en artículos de
segunda mano pero no en el texto que pudimos abrir.

Lo que el repositorio no sostiene solo va marcado **[a confirmar]**. El más importante: los bocetos «anteriores a
cualquier interacción con la IA». `prototipo_felipe_1` es del 13/10, parte de una captura de la app (que ya estaba
escrita con Claude Code) y no puede presentarse como previo. Lo humano más temprano con fecha es la Entrega 1 (25/08),
sin pantallas. Revisados también el prototipo navegable y las láminas de la Entrega 2 en Figma: no hay bocetos a mano
(los frames del prototipo se llaman `screen:*`, que sugiere un script). Tampoco hay entrevistas con quien diseña para
una marca, que es lo que mejor cerraría el ítem 1.

## 2026-11-04 · La pirueta: «Adiviná vos»

**Qué es.** Una pantalla (en «Más», y desde «El cono» de Método, con «Probalo vos →») donde la persona ve una curva real
de búsqueda hasta 2019 y dibuja con el dedo cómo sigue hasta 2024. Después se revelan la curva verdadera, lo que dice
el cono de CICLO y lo que da repetir el último valor, con el error de cada uno. Tres rondas al azar entre las 65 series,
y al final el resultado de todas. El hallazgo más difícil de contar —que estas series no se dejan predecir— se entiende
jugando, sin leer.

**Lo que se verificó antes de construirla.** Que lo que promete es cierto: con el corte en 2019, en las 65 series
(`GREL`, el peso de cada término frente a las otras búsquedas de moda), repetir el último valor queda más cerca de lo
que pasó que el cono 45 veces, y el cono 18 (dos empates); error medio de 14,3 puntos contra 16,4. Con el corte en
2017 y en 2018 da lo mismo (39 a 25, 41 a 21). El cono jugó con ventaja, porque su mediana se calculó con estas mismas
series, y la pantalla lo dice.

**Por qué esta y no «¿De qué año es tu diseño?».** La otra idea (CLIP ubica una prenda en la línea de tiempo de la
pasarela) era una variante de Buscar por imagen y, antes de mostrarla, habría que probar que CLIP distingue años en looks
que no vio; si no los distingue, la pieza mostraría una precisión que no tiene. «Adiviná vos» es honesta por
construcción: muestra el límite del modelo, no una capacidad.

**La nota que pide la consigna: qué IA, para qué y dónde frenamos.**
- *Qué capacidad usamos.* Ninguna generativa adentro del juego, y es a propósito. El modelo que compite es el cono de
  CICLO: estadística, la mediana de lo que pasó en la historia. La IA estuvo en construirla: Felipe propuso las dos ideas;
  Claude recomendó la primera, verificó con los datos que la promesa era cierta antes de escribir una línea, y escribió
  el código.
- *Dónde frenamos.* Se pensó en sumar al LLM como cuarto jugador y se descartó: para adivinar tendría que recibir la
  serie año por año, y la regla de CICLO es que el modelo de lenguaje nunca ve una fila de datos. Romperla para un juego
  contradiría lo que el juego enseña. Tampoco se eligieron las rondas a mano: salen al azar, aunque en alguna gane el
  cono (pasa una de cada tres veces y se muestra igual).
- *La decisión.* Las dos ideas y la elección son de Felipe; la recomendación de no sumar al LLM es de Claude, por la
  regla del proyecto.

## 2026-11-04 · «Más» se achica: cada pantalla, donde se usa

**Quién decidió.** La propuesta es de Claude (en el borrador del racional y en la lista de pendientes). Felipe la delegó:
«punto 3 hace lo que te parezca».

**Qué cambió.** El menú «Más» tenía cinco pantallas de igual peso, y tres eran detalle de otra. Ahora tiene dos:
Adiviná vos y Método. Las otras tres no se borran: se abren desde la pantalla de la que dependen.
- **El modelo** (el K-means) se abre desde Método, en el esquema de datos («Ver el modelo →», en la tarjeta del K-means).
- **Marcas** (Lyst) se abre desde Método, en la fuente «Venta y marcas» («Ver las marcas →»). Es contexto, no entra al
  modelo, y el menú la ponía a la altura de Tendencias.
- **Retornos** se abre desde El ciclo, debajo del título («Qué volvió y cada cuánto →»), y mientras está abierta el menú
  marca El ciclo.

**Por qué así y no fundirlas.** Convertir Retornos en un filtro de El ciclo, como decía la propuesta, obligaba a
reescribir las dos vistas a dos semanas de la entrega. Un link desde donde se usa logra lo mismo para quien navega (el
menú deja de ofrecer cinco cosas iguales) sin tocar los cálculos. Los links de antes (`#etapas`, `#marcas`,
`#retornos`) siguen abriendo cada vista.

**Cómo se probó.** Playwright a 1400 y 393 px: «Más» lista dos pantallas, cada link nuevo abre su vista, el menú marca
la de origen y los links directos andan. Sin errores de consola. Versión anterior en
`diseno/prototipos/versiones_de_la_app/app_2026-11-04_1f33b4d_antes_de_ordenar_mas.html`.

## 2026-11-04 · El racional: quién decidió qué, con las palabras de Felipe

**De dónde sale la tabla de autoría.** Felipe pidió buscarlo en las conversaciones: «vos tenes nuestro chat de todo en
claude sabes perfectamente que decidi yo y que vos». Se leyeron los 244 mensajes suyos en Claude Code, del 13/10 al
04/11, y las respuestas de Claude. Cada fila cita sus palabras textuales, con los errores de tipeo, y se verificaron una
por una contra los mensajes. Antes del 13/10 (el chat de Claude y la otra copia del repositorio) no hay registro en el
repo, y el racional lo dice.

**Lo que corrigió la lectura.** El borrador recomendaba sumar dos o tres entrevistas, pero el 27/10 Felipe las había
descartado («no me gusta esto de las entrevistas es un quilombo») y la prueba con Reddit las reemplazó. Ahora el
racional dice que no hay entrevistas y por qué. Dos filas del borrador estaban mal atribuidas: el calzado no fue «la IA
propuso medirlo como la ropa» (Felipe fue y vino, y está citado), y la portada no la sacó una propuesta de la IA (salió
de su consigna del 26/10).

**Los bocetos previos.** Según Felipe, son las primeras entregas en Figma. Se exportaron cinco láminas de la Entrega 1
(25/08) y tres pantallas del prototipo de la Entrega 2 (05/10) a `entregas/entrega_4/bocetos_previos/`. El racional
aclara lo que son: la Entrega 1 son láminas de ideas, no pantallas, y el prototipo de la Entrega 2 ya convivía con la IA
(el sitio de esa entrega era un artifact de Claude). Los wireframes esquemáticos del 05/10 no quedaron en el Figma.

**Los prompts v5 y v6.** Siguen sin probar en vivo: no hay una clave de Groq a mano y no se pide. Cambian una sola
línea (quién pregunta) respecto de las versiones probadas, así que el riesgo es bajo, y queda en la lista de lo que falta.

## 2026-11-04 · El papel, al día con la app

Cristian pidió los diseños en papel «con todo el flujo actualizado». Después de ordenar «Más» y de sumar la pirueta, el
papel ya no coincidía con la app, así que se actualizó en Figma (página «4 · En papel · Entrega 4») y se rehízo el PDF:
- **Hoja 13 nueva, Adiviná vos.** La ronda ya revelada, con la serie real de la remera (`GREL`, 2010–2024) y el cono de
  la app (el valor de 2019 más la mediana de `CONO`). El trazo de «vos» es un ejemplo, y se nota: sube cuando la serie
  baja. Los errores son los que da la app con esos números: el cono ±7 y repetir 2019 ±6, el más cerca.
- **Hoja 09:** «Qué volvió y cada cuánto →» debajo del título, que lleva a Retornos.
- **Hoja 12:** «Ver el modelo →», «Ver las marcas →» y «Probalo vos →», como en la app.
- **Hoja 00:** la caja 13 con borde punteado (se llega desde la barra).

Se exportaron de nuevo sólo las cuatro hojas que cambiaron (00, 09, 12 y 13), al 200 % y a 288 dpi como las demás.

## 2026-11-04 · El racional, también en PDF

`codigo/exportar_racional_pdf.js` arma `entregas/entrega_4/racional.pdf` (11 páginas A4) a partir de `racional.md`, con
la tipografía y los tonos de la app, para entregarlo o imprimirlo. El Markdown es la fuente: el PDF se rehace con el
script después de cada cambio, y el script falla si alguna imagen no carga. Al revisarlo se cambió una imagen de los
bocetos: la lámina «Perfil de usuario» de la Entrega 1 trae una ilustración que parece hecha con IA de imágenes y no
puede mostrarse como previa a la IA. En su lugar va la lámina de la pregunta (25/08), que ya nombra las cinco etapas.

## 2026-11-04 · La entrada por el objetivo, probada y descartada: vuelve el vínculo

**Qué se probó.** Cristian pidió, en la devolución de la Entrega 3, «piensen si esas son las mejores palabras para armar
la ramificación». Se probó como alternativa una entrada por el objetivo: «¿Qué estás por decidir?», con Qué diseñar,
Qué producir y Si algo ya pasó (la variante «el compromiso», entrada de arriba del mismo día). Se construyó entera: la
app, las hojas en papel y el recorrido del readme.

**Por qué se descartó.** Felipe, al usarla: «no funciona. Es confusa y no se entiende qué elegir». Obliga a la persona a
traducir su situación a una categoría abstracta antes de haber visto nada de la app, y eso la frena en la primera
pantalla.

**Por qué se vuelve al vínculo laboral.** Es una pregunta que un diseñador contesta sin pensar. Y lo que de verdad
cambia la lectura se deduce mejor de ahí que de una pregunta por el objetivo: cuánto cuesta equivocarse sale del vínculo
(por tu cuenta no comprometés producción ni stock, así que donde a una marca le conviene Esperar, a vos te conviene
Explorar), y cuánto falta hasta que la prenda se produce sale de la categoría, que se queda. Lo que la devolución
criticaba no era la pregunta: era el texto de más dentro de los cuadrados, que ya se había sacado el 03/11.

**Cómo quedó.** Vuelven las tres preguntas de antes, tal cual: ¿para quién diseñás?, ¿trabajás para una marca o por tu
cuenta?, la categoría. Se revirtió el cambio de la entrada (`d77109a`) y se conservó todo lo que vino después: los cinco
estilos, la curaduría del texto, el esquema de datos, Adiviná vos y la señal en cada tarjeta de Tendencias. Los links
del 04/11 con `d` siguen andando (`d=disenar` se lee como «por tu cuenta», que era lo que activaba Explorar). La app
vuelve a usar los prompts probados (`prompt_lectura_recomendacion_v4.md`, `prompt_asistente_v5.md`); los v5 y v6 de la
lectura y del chat quedan como descartados, sin borrar. Versión anterior en
`diseno/prototipos/versiones_de_la_app/app_2026-11-04_346ab3c_con_la_entrada_por_la_decision.html`.

## 2026-11-04 · La app no es una entrega: fuera la firma de la materia

CICLO se va a publicar, y quien entre tiene que ver un producto, no un trabajo práctico. Sale de la app todo lo que
nombraba la materia, la facultad, los docentes o una entrega: el bloque del gate («Sistemas generativos e IA para
Diseño · K534/K576 · UdeSA · 2026 · …»), el mismo bloque en el pie de Método y de «Más», el «como pide la consigna» de
El modelo (ahora dice la razón real: los 17 atributos son los que tienen serie en las dos capas a la vez, y la etapa
sale de cruzarlas), la primera línea del archivo de datos del chat («CICLO es una app de la materia…», que el modelo
podía repetir) y seis comentarios del código que nombraban la cátedra o una entrega. El pie queda con lo que le sirve a
quien la usa: qué es CICLO en una línea, la fecha de la última lectura de datos y el link al repositorio, abierto. La
materia, los docentes y los integrantes siguen en el readme y en el racional. Lo que no cambia es el rigor: fuentes,
medido contra interpretado, límites y pruebas preregistradas se quedan como están.

**Un error que salió al revisar.** El cambio de «Más» de hoy usaba `data-ir` para los links entre vistas, y ese atributo
ya lo usaban los chips de la barra de Diseñar y de Preguntar para volver a un paso: tocarlos dejaba la pantalla vacía.
Los links entre vistas pasan a `data-vista`.

## 2026-11-04 · Un producto, no una entrega: lo que sólo tenía sentido en la cursada

Felipe delegó la lista entera («hace todo lo que te parezca hacer en la lista»). El criterio: quien entra tiene que ver un
producto. El rigor se queda (fuentes, medido contra interpretado, límites, pruebas preregistradas); se va lo que existía
para mostrar el trabajo.

- **El catálogo sintético sale de la pantalla.** Tendencias armaba la mitad de sus etapas y todas sus paletas sobre el
  Zara 2018–22, que es sintético («muestra el método, no una conclusión»). Ahora Tendencias muestra sólo atributos con dato
  medido (8 de 12: los otros 4 no tenían etapa ni serie), la etapa sólo si viene del K-means, y sin paleta. En la ficha
  salen la paleta, «Del catálogo (sintético)», la «Lectura del equipo» (que leía esa paleta) y el gráfico «Recorrido en el
  tiempo 2018–2022», que además decía «Dato medido, no estimado» sobre datos sintéticos: estaba mal rotulado. «Sus
  colores, para diseñar» también salía de esa paleta y se va. En Método salen las dos filas de «demostración» y la de la
  etapa estimada.
- **El modelo:** arriba, lo que sirve para decidir (los grupos leídos como etapas, la validación con Shopping, Amazon y
  Lyst). El laboratorio del K-means (los datos, el paso a paso, el selector de k, el codo, la silhouette, «agregá una
  tendencia») queda plegado al final, en «Cómo se calcula». Sale el bloque «Rol de la IA · El prompt que usamos», que
  mostraba un prompt viejo, y la nota sobre el README del archivo de Lyst.
- **Marcas:** sin «le pasó lo mismo que a nosotros» ni «el argumento más fuerte que tenemos para defender»; ahora dice
  qué le sirve eso a quien lee un ranking. Sale «Cómo se construye esta capa», que era planificación del equipo («12 a 15
  horas… repartibles entre los tres»).
- **Textos:** «Cuatro cosas que hay que decir antes de mostrar esto» pasa a «Los límites de estos datos»; «sirve para
  presentar el método» a «es orientativo»; sin «IA-6» (la numeración de la Entrega 2); sin nombres de archivo en
  pantalla (`ciclo_datos.md` pasa a «un resumen de métricas ya calculadas», con su link).
- **Método:** salen las filas de estado interno (el grupo en liquidación sin fuente, Pinterest y TikTok «con una cuenta
  del grupo», los datasets de Kaggle «para la próxima etapa») y las frases de historia del proyecto («16 de septiembre y
  49 de los planes de octubre», «el encaje pasó de estampa a material», «intentamos sumar…»). Las rutas del repositorio
  pasan a ser links a GitHub.
- **El pie:** sólo las fuentes que la app usa (fuera Runways since 2011, Wish y «Piden cuenta: Pinterest, TikTok»).

Probado con Playwright a 1400 y 393 px en todas las vistas, sin errores; el laboratorio del K-means funciona plegado.
Versión anterior en `diseno/prototipos/versiones_de_la_app/app_2026-11-04_3dde1b6_antes_de_sacar_lo_de_cursada.html`.

## 2026-11-04 · La presentación sale de la app publicada

La presentación de la Entrega 3 se servía en `/ciclo/presentacion/`, dentro del sitio del producto, con el título
«CICLO · Entrega 3» y la universidad en pantalla. Pasa a `entregas/entrega_3/presentacion/`: queda en el repositorio,
completa, y se abre con un servidor local. El sitio publicado es sólo la app. Ya se presentó el 03/11, así que su link
público dejó de hacer falta; el guion y el readme dicen dónde está ahora.

**Lo que queda pendiente, y lo tiene que hacer Felipe:** la dirección de Netlify es `ciclo-udesa.netlify.app`. Renombrar el
sitio (por ejemplo, a `ciclo-moda`, que está libre) es un cambio de dominio y no se hace sin su autorización explícita.

## 2026-11-04 · El papel, con la entrada por el vínculo

Las hojas en papel volvieron a la entrada de antes, para corregirlas en clase con el flujo que tiene la app: 01 ¿Para
quién diseñás?, 02 ¿Trabajás para una marca o por tu cuenta?, 03 la categoría. La 05 deja de ser «¿Sigue vigente?» y
pasa a ser Tendencias por tu cuenta, con Explorar donde la marca espera; la 07 y la 08 (Diseñar) son por tu cuenta, por
eso dicen Explorar. En el mapa sale la flecha de la categoría a Diseñar. Las tarjetas de Tendencias pierden la paleta
del catálogo sintético, como en la app. Se exportaron de nuevo las siete hojas que cambiaron.

## 2026-11-10 · Lo que devuelve la IA, filtrado: primero la respuesta (prompt v7)

**Devolución de la Entrega 3, criterio 3 (5/10).** «Hoy parece que no hay filtro sobre lo que devuelve la IA: tienen que
filtrar y curar ese contenido. Como usuario, tengo que leer muchas cosas que no aportan valor por igual.»

**Lo que pasaba.** El chat (prompt v5) devolvía de 2 a 4 oraciones en un párrafo, y la primera era casi siempre una
aclaración («De 2025 y 2026 no tengo lectura porque…»). Abajo venían la señal, la serie, la lista de datos y los
botones, todo con el mismo peso.

**Decisión.** La respuesta se parte en tres campos con límite, y la app los muestra con tres pesos:
la **conclusión** (una frase, hasta 20 palabras, en Subtítulo, con la señal al lado si la pregunta pide decidir), el
**respaldo** (una frase con el número, su fuente y su período, en Cuerpo) y, plegado bajo «Detalle y series», el
**detalle** (0 a 2 oraciones: prestado, CLIP, no medido, el corte de 2024) con las series y los datos citados. Se puede
dejar de leer después de la primera línea. Las reglas de los datos no cambian. Prompt nuevo en
`prompts/prompt_asistente_v7.md`; la v5 queda.

**Tres corridas hasta que anduvo.** Seis preguntas reales con `codigo/probar_asistente.js`, cada vez.
1. Primera: el formato funcionó, pero el modelo coló un id («señal de material_gamuza»), repitió la señal al principio
   de la conclusión («Esperar · Esperar, la falda…») y a los lunares contestó «Sí, están volviendo» con −3 puntos de
   búsqueda como respaldo. La etapa del K-means dice «en retorno», pero la búsqueda todavía cae.
2. Con una regla nueva (si el número va en contra, la conclusión dice las dos cosas) y otra sobre CLIP, retrocedió: a
   «¿Qué color va con un jean baggy?» contestó «No lo sé», aunque el dato existe (azul medio, 48 % de los looks, CLIP).
   La regla sobre CLIP lo había hecho dudar de los colores. Los lunares seguían igual.
3. Con dos ejemplos de ese patrón en vez de más reglas, las seis salen bien: «Azul medio, el que más aparece con jean
   baggy en pasarela» con el detalle de que es CLIP; «Todavía no: la etapa dice que vuelve, pero la búsqueda sigue
   cayendo»; las botinetas ofrecen las zapatillas y los mocasines con su número. Con `gpt-oss-120b` y razonamiento bajo,
   un ejemplo enseña más que una regla.

**Lo que filtra la app.** El prompt no alcanza siempre, así que `asNormalizar()` borra los ids del texto y de los datos
citados, y saca la palabra de la señal si la conclusión empieza con ella (la señal va aparte, con su color y un «·»).
La corrida que queda en `datasets/pruebas/asistente_v7_respuestas.md` es la tercera, sin editar; sus datos citados
todavía muestran un id, porque el filtro de esa lista se agregó después.

## 2026-11-10 · «Cómo se arma una lectura»: la pirueta y el esquema de los datos, en una pieza

**Devolución.** Criterio 2 (5/10): «Debe quedar claro qué datos usan, para qué y cómo conviven en el modelo». Criterio 5:
«encontrar formas más simples de que se entienda esa complejidad».

**Por qué esta y no «Adiviná vos».** Felipe propuso dos piruetas. Adiviná vos, ya construida el 04/11, muestra el límite
del modelo, pero no contesta ninguna de las dos notas bajas. Esta sí, y no agrega una pantalla: reemplaza al esquema
estático de Método y hace innecesarias las explicaciones de El modelo. La recomendación fue de Claude y la elección
de Felipe.

**Lo que se corrigió de la idea antes de construirla.** La propuesta decía «las cinco capas se combinan en una sola
señal» y «sale una etapa y un color». No es así, y la pieza no puede contradecir el modelo:
- Al K-means entran **dos** fuentes (pasarela y búsqueda), con dos números cada una. Reddit, Shopping, Amazon y Lyst
  comprueban después y no entran: van aparte, en gris, sin animar.
- La pasarela de los jeans es **prestada**: Vogue mide «denim», así que baggy, rectos y skinny tienen la misma (en `KM`,
  `pn` y `pm` idénticos). Toda la diferencia sale de la búsqueda. Lejos de esconderlo, la pieza lo muestra: es lo que
  mejor explica por qué tres jeans tienen señales distintas.
- El K-means da la etapa; la señal sale de la etapa más el perfil, por una regla escrita (`CONSEJO`), no por IA.

**Qué es.** Siete pasos, cuatro segundos cada uno, que arrancan solos la primera vez que la pieza entra en pantalla
(no con movimiento reducido) y se pueden recorrer con los números: entra la pasarela, entra la búsqueda, cada curva se
vuelve dos números, los tres jeans contra los otros 14 atributos en la misma escala, el K-means junta a los que se
parecen, cada grupo toma el nombre de su etapa (baggy queda en Pico con el cargo; rectos y skinny, en Saturada) y el
perfil lo vuelve señal. Todo sale de las mismas funciones que usa la app (`REC`, `KM`, `kZ`, `kFit`, `kName`, `consejo`), así
que no puede contradecirla. Sin color nuevo: los cortes usan los tonos de gráfico y el único color de señal está en el
último paso.

**La nota que pide la consigna: qué IA, para qué y dónde frenamos.**
- *Qué capacidad usamos.* Dos, y las dos se ven trabajando: CLIP (un modelo de visión y lenguaje), que convierte las
  fotos de pasarela en una serie por atributo, y el K-means (aprendizaje no supervisado), que agrupa sin etiquetas.
- *Para qué.* Para que la etapa salga de los datos y no de nuestra opinión.
- *Dónde frenamos.* El modelo de lenguaje no narra la pieza: tendría que ver las series, y la regla es que nunca ve una
  fila. La pieza termina en la etapa; el paso a la señal es una regla escrita y se dice así. Y no predice: el último
  paso manda a «Adiviná vos», que muestra por qué.

**Lo que se fue.** El esquema de tres columnas de Método (04/11). Con él se fueron los links «Ver el modelo →» y «Ver
las marcas →»: Felipe decidió sacar El modelo y Marcas de la navegación (no ayudan a tomar una decisión). Las dos vistas
siguen abriendo desde su link directo (`#etapas`, `#marcas`) hasta que se resuelva qué queda de ellas.

Probado con Playwright a 1400 y 393 px, los siete pasos, sin errores de consola ni scroll horizontal.

## 2026-11-10 · La entrada, sin nada que sobre

**Devolución (Cristian e Iván, sobre la versión del 10/11).** «Tu elección anterior» desnivela las tres opciones: la
tarjeta marcada baja el nombre y las otras no. El botón «Continuar» relleno de azul pesa demasiado, y no hace falta en
los tres pasos. El nombre de cada tarjeta se subrayaba al pasar el mouse: ya está dentro de un cuadro, la línea sobra.

**Decisión.** Se va la función entera: la entrada ya no lee el perfil guardado para marcar lo de la visita anterior.
Entre que el botón vaya sólo al final o que no haya botón, elegí que no haya: tocar una tarjeta ya avanzaba, y
«Continuar» sólo existía para confirmar la elección anterior. Sin esa función no tiene trabajo. Lo elegido queda marcado
sólo si se vuelve un paso atrás dentro de la misma visita. «Volver» se queda como está. El perfil se sigue guardando para
los links que lo traen; lo único que cambia es la entrada.

La elección entre las dos opciones fue de Claude, a pedido de Felipe. Probado con Playwright a 1400 y 393 px: tres
toques llevan a Tendencias con el perfil elegido, sin errores de consola.

## 2026-11-10 · «Sólo estoy mirando»: la salida de la entrada, por lo que gana

**Devolución (Cristian e Iván).** Hacía falta una salida de la entrada para quien todavía no quiere contestar, pero
«continuar sin perfil» nombra algo que la persona no conoce: la app nunca le dijo que estaba armando un perfil. Iván
sugirió ir por el lado de «explorar», como el «explorar sin cuenta» de otras apps. Felipe pidió cinco textos pensados
desde lo que gana el usuario, no desde lo que se saltea.

**Las cinco.** «Sólo estoy mirando», «Ver todas las tendencias», «Explorar primero», «Mirar sin elegir» y «Entrar
directo». Felipe delegó la elección («hacé lo que te parezca»).

**Decisión: «Sólo estoy mirando».** Es lo que se le dice al vendedor en un local: cualquiera de moda la reconoce, no
nombra nada técnico y dice exactamente lo que pasa, que puede mirar todo sin comprometerse. Va debajo de las tarjetas,
en los tres pasos, como link y no como botón, para que no compita con las respuestas.

**Qué pasa al tocarla.** Las señales necesitan un perfil, así que la app usa uno general: una marca contemporary, sin
género. No lo esconde: en Tendencias, donde va «Tu perfil», dice «Estás mirando sin elegir: las señales son para una
marca contemporary», con un link a «Decime para quién diseñás». Al contestar la entrada, vuelve la línea de siempre.

Probado con Playwright a 1400 y 393 px: el link queda centrado, lleva a Tendencias y la línea cambia al elegir.

## 2026-11-10 · Tendencias: fuera el bloque negro, entran las curvas

**Devolución (Cristian).** El bloque oscuro de «qué gana y qué pierde terreno» obstruía la vista: era lo primero de la
pantalla principal y era un bloque de texto sobre fondo negro. Lo que más gustó de la versión nueva fue la animación de
«Cómo se arma una lectura», sobre todo el paso 1, donde las curvas se dibujan.

**Decisión.** El bloque sale y su lugar lo toman dos gráficos, «▲ Gana terreno» y «▼ Pierde terreno», con los tres
atributos que más ganan y los tres que más pierden. Son las mismas cuentas que tenía el bloque (`terreno()`: búsqueda
mundial corregida, 2022→2024, en puntos), pero contadas con la curva real de cada uno desde 2016, para que se vea si
el cambio es un salto, una caída larga o una vuelta. Al entrar, las curvas se dibujan de a una, como en el paso 1; al
final aparece el punto y el rótulo con los puntos ganados o perdidos. «↺ Ver de nuevo» repite la animación. Tocar una
curva abre su recorrido en El ciclo, como hacían las filas del bloque.

**Color.** Las curvas usan los colores de los gráficos (`--s1`, `--s2`, `--s4`). El único verde y rojo es el número,
que ya era la excepción fijada el 27/10 para «gana / pierde presencia». Sin fondo oscuro: el bloque era la única
excepción a «siempre claro», y se fue con él.

**Lo que no se tocó.** «Diseñar con esta estampa / corte / material» y «Pedir lectura en vivo» en la ficha: gustaron y
quedan igual.

## 2026-11-10 · Los «?», siempre en el mismo lugar

**Devolución.** Los «?» aparecían a veces centrados debajo del título, a veces a la izquierda y pegados al dato.

**Decisión.** Una sola regla para los 16 de la app: arriba a la derecha del bloque que explican, nunca a la izquierda ni
pegados a un número. Al abrirse no empujan el contenido: se abren como una tarjeta flotante, debajo del «?». El texto que
tiene al lado deja lugar para que no se pisen. Revisados uno por uno con Playwright, a 1400 y 393 px.

## 2026-11-10 · La pirueta, otra vez: «El brief»

**Devolución (Cristian e Iván, sobre «Cómo se arma una lectura»).** Cristian fue directo: está muy floja, no es un
juego, no tiene hook, no es interactiva. Iván la vio un poco mejor. O aparece una idea mejor, o la misma con una
ejecución visual espectacular. Lo que más gustó fue la animación de las curvas.

**La primera propuesta, descartada.** «¿Tenés ojo?»: una tarjeta con un atributo, cuatro botones de etapa, la tarjeta se
da vuelta y revela lo que dice el K-means. Felipe la descartó antes de construirla: «el juego es literal un memo test, no
innovaste nada». Y pidió pensarlo para el target: qué le divierte a un diseñador de ropa.

**La idea.** No adivinar lo que dice el modelo, sino jugar con él. Un diseñador no recibe atributos sueltos: recibe
briefs, y la tensión de su oficio es querer algo en el momento justo de su ciclo. Cada ronda es un brief de un cliente
(«Quiero una falda de cuero en la colección, y que llegue en su mejor momento») y la persona tiene cuatro movidas del
oficio para llevar el atributo a esa etapa:

| Carta | Qué es en la industria | Qué cambia en los datos |
|---|---|---|
| Lo sacás en tu desfile | Lo mostrás y otras marcas te copian | Pasarela 2022–23 ×1,5 |
| Lo usa una it-girl | Sale en street style y todos lo buscan | Búsqueda 2023–24 ×1,5 |
| Lo sacás de la colección | Las marcas lo dejan de mostrar | Pasarela 2022–23 ×0,6 |
| Va a liquidación | Termina en el outlet y la gente se cansa | Búsqueda 2023–24 ×0,6 |

Cada carta vuela al gráfico. La curva real se estira hasta los datos nuevos, los cuatro números corren y la ficha del
atributo se desliza por la pista de etapas (la etapa sigue siendo posición, no color). Menos movidas, más estrellas. Si
se pasa del límite, el brief queda sin cumplir y el juego muestra la jugada mínima. Al final, los cinco briefs arman
«Tu colección»: un line-up con las cinco prendas, la etapa a la que llegó cada una y lo que enseña cada brief.

**Por qué responde a la devolución.** Es un juego: tiene meta, límite de jugadas, puntaje y respuesta correcta. El hook es
del oficio: hacer que algo llegue a su punto justo. Es interactivo de verdad, porque el modelo responde a cada movida. Y
mientras se juega se aprende cómo lee el modelo, que era el 5/10 de rigor con los datos. Pico es búsqueda alta; la
pasarela sola satura; para quedar En retorno tiene que soltarlo la pasarela y cansarse la gente; En ascenso es la
pasarela empujando fuerte.

**El rigor detrás del juego.** Los cuatro números se recalculan con la cuenta del modelo. Escalar lo reciente por f da
nivel = mín(1, nivel · f) y momento = (1 + momento) · f − 1, porque el momento compara lo reciente contra 2020–21. El
atributo se ubica en el grupo más cercano sin reentrenar, igual que una tendencia nueva. Las series de la app no
reproducen la búsqueda detrendeada del K-means, así que el juego mueve los números del modelo y la curva es su
ilustración; las dos se estiran por el mismo factor.

Los cinco briefs y su jugada mínima salen de probar todas las combinaciones de hasta cuatro cartas sobre los 13
atributos que tienen serie en la app:

| Brief | Hoy | Meta | Jugada mínima |
|---|---|---|---|
| Floral | Saturada | Pico | it-girl |
| Cuero | En retorno | Pico | it-girl ×2 |
| Jeans baggy | Pico | En retorno | sacarlo de la colección + liquidación |
| Buzo / hoodie | Saturada | En ascenso | desfile ×2 |
| Lunares | En retorno | Pico | desfile + it-girl ×2 |

Corset, que estaba en la propuesta, no se puede usar: el modelo no lo mide. La pasarela del baggy es la de todo el
denim, y el brief lo dice. Al final, el juego aclara que las movidas son un juego (nadie movió los datos de verdad) y
que lo real es la cuenta.

**Dónde vive.** Discreto: en «Más», en el lugar de «Adiviná vos» (que sigue abriendo por su link), y con un acceso desde
Tendencias y otro al final de «Cómo se arma una lectura», en Método. No aparece solo ni interrumpe Diseñar.

La idea y la construcción fueron de Claude, después de que Felipe descartara la primera y pidiera pensarla para
diseñadores. Probado con Playwright a 1400 y 393 px: los cinco briefs se cumplen con su jugada mínima, sin errores de
consola ni scroll horizontal.

## 2026-11-10 · Tendencias: cinco y cinco, y nada debajo del gráfico

**Devolución (Felipe).** El gráfico animado por año es lo que buscaba y se queda. Pero muestra pocos atributos: hay que
sumar al menos jeans, gamuza y falda, y dos o tres más con serie propia que un diseñador reconozca. Y el link que estaba
debajo («¿Podrías llevar los lunares a Pico? Jugá El brief») no funciona y distrae de la animación.

**Decisión.** Cinco por lado, elegidos a mano entre los que más se mueven en la búsqueda mundial 2022→2024, todos con
serie propia:

| Ganan | Pierden |
|---|---|
| Jeans baggy +50 | Blusa −31 |
| Gamuza +29 | Vestido cruzado −26 |
| Falda maxi +21 | Polera −26 |
| Falda mini +17 | Vestido slip −19 |
| Trench +12 | Corset −17 |

Quedan afuera las fibras que suben tanto o más que estos (lana +20, popelina +19, merino +17): se buscan como insumo y no
le dicen nada a un diseñador sobre qué diseñar. Que es una selección está dicho en el «?», con la lista completa en El
ciclo. Los rótulos se ordenan a la altura donde termina cada curva y no se pisan, también en el celular. El link al juego
sale; el juego se rehace.

## 2026-11-10 · «El brief», rehecho desde cero: diseñar, y enterarse si tuviste ojo

**Por qué falló el de las cartas (Felipe).** Las cartas con gráficos confundían: pedían leer curvas para jugar, y eso no
es jugar, es estudiar. Lo que un diseñador hace y le divierte es diseñar, y después enterarse si tuvo buen ojo.

**El juego.**
1. *El brief.* Una tarjeta con la casa, la temporada y la prenda («Loewe · Otoño 2028 · Un abrigo») y un look real de
   Vogue Runway. Zara, H&M y COS no desfilan: su foto es la referencia de lujo que van a bajar a la calle (Chanel, Bottega
   Veneta, The Row). La temporada es el horizonte al que decide cada categoría en la app (`PERFIL.hasta`: fast fashion
   2026, contemporary 2027, lujo 2028).
2. *Diseñás.* Tres toques con las tarjetas de Diseñar (forma, material, estampa) y la barra de lo elegido abajo. Sin
   señales a la vista, para que el juego no se resuelva solo.
3. *El veredicto, con ritmo.* Primero un titular en lenguaje de moda («Te adelantaste: el fast todavía no lo copió»).
   Después, de a una, las tres elecciones con su momento y su número. Después, qué te subió el puntaje y qué te lo
   bajó. Al final, el golpe: el mismo look puntuado para tres casas, y la del brief, en negro.

**El puntaje.** Cada opción tiene su serie de búsqueda mundial (Google Trends, corregida, la misma de Tendencias) y de ahí
sale su momento:
- **Baja** si perdió más de 3 puntos entre 2022 y 2024.
- **Quieto** si se movió entre −3 y +3.
- **Pico** si ganó y está en su techo (el nivel 2023–24 llega al 80 % de su máximo).
- **Sube** si ganó y todavía no llegó.

Las tres elecciones pesan lo mismo. Lo que cambia por casa es la lógica de la moda, que fijó Felipe: «sube por el lujo y
se pone malo por el fast: las marcas de lujo lo ponen de moda y sube, y después lo copian los de fast y baja».

| | Sube | Pico | Quieto | Baja |
|---|---|---|---|---|
| Lujo (Chanel, Loewe, Prada) | 10 | 4 | 5 | 1 |
| Contemporary (COS) | 7 | 10 | 5 | 2 |
| Fast fashion (Zara, H&M) | 3 | 10 | 5 | 2 |

Es una regla del juego y se dice así en el «?»: no es un pronóstico ni la regla de las fichas (`CONSEJO`), que sigue
igual. El momento sale de las series y la regla, de cómo se mueve la moda. Las opciones se eligieron para que en cada
paso haya de los cuatro momentos: el baggy está en pico, el recto y el skinny bajan, la gamuza y la lana suben, el cuero
está quieto, las rayas y el floral están en pico, el tie-dye baja.

**Fotos de Vogue.** Por decisión de Felipe, las fotos de los briefs son de Vogue Runway, el mismo corpus que usa CLIP, con
la casa, la temporada y la fuente al pie. Se muestran desde los servidores de Vogue, como ya hacían «Ver referencias de
pasarela» y Buscar por imagen: no se descargan ni se suben al repositorio. Sigue sin licencia declarada: está dicho en la
verificación del 13/10.

**Dónde vive.** En «Más» y al final de «Cómo se arma una lectura», en Método («¿Tenés ojo para Chanel?»). No aparece solo.
El juego de las cartas sale entero.

Probado con Playwright a 1400 y 393 px: el brief, los tres pasos y el veredicto, sin errores ni scroll horizontal.

## 2026-11-10 · Tendencias: cinco lecturas que rotan

**Pedido (Felipe).** El gráfico mostraba una sola cosa y se quedaba ahí. Tiene que ir cambiando de vista, como la
secuencia de Método, para que al mirarlo un rato se vean cosas distintas.

**Las cinco, en este orden.** Cada una dura nueve segundos y entra animada. La pausa es automática al pasar el mouse;
también hay botón. Abajo están los nombres de las cinco, para saltar a cualquiera, y el de la que está activa se llena
como una barra de progreso.

| # | Lectura | Qué muestra | De dónde sale |
|---|---|---|---|
| 1 | Qué sube y qué baja | Cinco que ganan y cinco que pierden, con su curva desde 2016 | `terreno()`, 2022→2024 |
| 2 | Qué está en su máximo | Barras del nivel 2023–24 sobre su máximo histórico: tote 98 %, floral 96 %, mocasines 94 % | La serie, desde 2004 |
| 3 | Cuándo picó cada uno | Catorce atributos en el año de su máximo, del skinny (2010) al baggy y el floral (2024); el punto viaja hasta su año | El año del máximo |
| 4 | Lo que vuelve | Floral, mocasines y lunares, con sus dos picos y los años entre uno y otro (7, 8 y 7) | `cicloDe()`, la regla de El ciclo |
| 5 | Uno contra otro | Dos curvas en la misma escala y el año en que se cruzan: skinny y baggy (2021), blusa y corset (2022), zapatillas y mocasines (2023) | El cruce de las dos series |

Todas usan la misma serie (búsqueda mundial corregida, hasta 2024), así que ninguna contradice a otra ni al resto de la
app. Tocar un atributo abre su recorrido. El alto del bloque es el de la lectura más alta, para que la página no salte al
rotar. En el celular, cada lectura se arma al ancho de la pantalla. Con movimiento reducido no rota sola.

**El acceso al juego.** Tendencias vuelve a tener uno, pero al final de la página y no debajo del gráfico: «¿Tenés ojo
para Chanel? Jugá «El brief» →».

Probado con Playwright a 1400 y 393 px: las cinco lecturas, sin errores ni scroll horizontal.

## 2026-11-10 · Fotos de Vogue en Tendencias y El ciclo

**Pedido (Cristian e Iván, y la decisión de Felipe).** Las estampas, materiales y prendas de Tendencias y de El ciclo
tienen que mostrarse con fotos reales, no con ilustraciones. Los cortes conservan la silueta, que gustó, combinada con la
foto. La fuente la decidió Felipe: Vogue Runway, el mismo corpus que ya usa CLIP.

**Lo que cambia respecto de la licencia.** El 13/10 se dibujaron las siluetas porque las fotos de Vogue no tienen licencia
declarada, y eso no cambió. Lo que cambió es la decisión: se muestran igual, como ya se mostraban en «Ver referencias de
pasarela» y en Buscar por imagen. Se cargan desde los servidores de Vogue, no se descargan ni se suben al repositorio, y
cada una lleva diseñador, temporada, año y «Vogue Runway» al pie. El riesgo queda dicho, no escondido.

**Cómo se eligió cada foto.** Con el mismo CLIP de la app: el codificador de texto (Xenova/clip-vit-base-patch32, el
mismo modelo, en el navegador) convierte una frase por atributo, como «a runway look with polka dots», en un vector.
Ese vector se compara con los 14.000 looks del índice, desde 2016, tomando un look por diseñador. De los seis más
parecidos se eligió uno a ojo. Donde ninguno mostraba el atributo, no hay foto y queda el dibujo: popelina, evasé, capa,
corderoy, jean skinny y casi todos los materiales sin forma (seda, gasa, tul, organza, satén, pedrería). Hay 38
atributos con foto, y se revisaron que no se repitiera ninguna.

**Cómo se ven.**
- *Tendencias:* la foto ocupa el cuadro de la tarjeta. En los cortes (amplio, medio), la silueta va en una pastilla
  blanca arriba a la derecha, la opción 1 de las tres que se propusieron. El ajustado no tiene foto que lo muestre, así
  que conserva su silueta sola.
- *El ciclo:* la foto va arriba de cada tarjeta que tiene una.
- *Recorte:* cada foto mira donde está el atributo. Para jeans, mocasines, shorts y faldas, el recorte baja hasta las
  piernas o los pies.

Probado con Playwright a 1400 y 393 px, sin errores ni scroll horizontal.

## 2026-11-10 · Tendencias: lo que vuelve, el año una sola vez y la foto del skinny

**«Lo que vuelve» no se entendía.** Mostraba tres curvas chicas con «7 años entre picos (2012 y 2019)» y había que
deducir qué significaba. Pedido de Felipe: decirlo como frase, no como medida. Ahora muestra un atributo por pasada
(floral, lunares, mocasines y animal print, rotando) con la frase arriba: «Los lunares picaron en 2012. Volvieron a
picar en 2019. Entre una vuelta y la otra pasaron siete años.» El gráfico acompaña la frase: la curva, los dos picos
con su año y el tramo entre ellos sombreado una sola vez, con «siete años» debajo. Sin ejes, porque los años ya están en
los picos. Los picos son los mismos de `cicloDe()` en El ciclo. Se eligieron cuatro con dos picos claros; se dejaron
afuera los que tienen el primer pico en 2010, porque ahí empieza la serie y ese pico puede ser «2010 o antes».

**El año duplicado en «Cuándo picó cada uno».** Se probaron las dos versiones. Queda el año al lado del punto, sin años
en el eje: en el celular el eje sólo entra con tres años (2010, 2017, 2024) y no deja leer 2015 o 2021. Las líneas
verticales quedan, sin número, como ritmo.

**Foto del jean skinny.** Con el mismo método del 10/11 (CLIP texto → look, a ojo entre los mejores), pero buscando con
cuatro frases y desde 2010, porque el skinny picó antes de 2016 y en los looks recientes casi no aparece. Quedó Helmut
Lang, otoño 2010: jean negro ajustado, botas. Con la misma búsqueda aparecieron también cargo (Greg Lauren, primavera
2023), evasé (Ralph Rucci, otoño 2011), capa (Public School, otoño 2014) y satén (Valentin Yudashkin, primavera 2014),
que hacían falta para el juego. Popelina, corderoy y los materiales sin forma (seda, gasa, tul, organza, pedrería)
siguen sin foto que los muestre.

## 2026-11-10 · El brief: fotos en todas las opciones

**Pedido de Felipe.** Que las fotos lleguen a todas las elecciones del juego, no sólo a la foto del brief.
Ahora cada opción de los tres pasos (forma, material y estampa) muestra su look de Vogue Runway, el mismo de
Tendencias (`FOTO_ATR`), con diseñador, temporada y año al pie. En el primer paso, que es la forma, la silueta queda
en la esquina, igual que en los cortes de Tendencias. El veredicto usa la misma foto, chica, al lado de cada elección.
Las 27 opciones tienen foto; las cinco que faltaban (skinny, cargo, evasé, capa y satén) se buscaron con el mismo método
(ver la entrada anterior). Si alguna opción se quedara sin foto, vuelve al dibujo.

**Colores: no hay paso de color en el juego, y no se agrega.** El juego puntúa cada elección con su serie de búsqueda
(GREL, 2022→2024), y los colores no tienen serie de búsqueda: lo que CICLO sabe de color sale de CLIP en la pasarela
(Diseñar), que es otra capa y no se puede mezclar en el mismo puntaje. Si se quisiera, el color podría mostrarse en
Diseñar con un look de Vogue de ese color en lugar del círculo plano (CLIP: «a monochrome red outfit»), pero eso es
Diseñar, no el juego, y queda propuesto, no hecho.

**Fuente y licencia, anotadas.** La fuente está en `datasets/fuentes_y_descargas.md` (Vogue Runway, «Fotos que muestra
la app») y en esta entrada y la del 10/11 sobre Tendencias: sin licencia declarada, cargadas desde los servidores de
Vogue, sin copia en el repo, con crédito al pie.


## 2026-11-10 · Uno contra otro: elegís vos

**Pedido de Felipe.** Poder comparar dos atributos elegidos sin salir de Tendencias y sin sumar controles. Se eligió
la opción que no agrega nada en reposo: en «Uno contra otro», los nombres de las dos curvas son los selectores (en azul,
que en CICLO quiere decir «se puede tocar», subrayados con el color de su curva). Al tocarlos se abre la lista nativa
del sistema con los atributos que tienen serie. Elegir frena la rotación, el botón pasa a «Seguir» y el subtítulo dice
«elegiste vos». Con «Seguir» la rotación sigue; cuando vuelve a «Uno contra otro», retoma los pares de siempre. Se
descartó una sexta pastilla «Comparar» con dos desplegables: suma justo la complejidad que se venía sacando.

**Dos fotos más.** Bouclé (DKNY, otoño 2011) y popelina (Zanini, primavera 2022), con el mismo método. Quedan sin foto
corderoy y los materiales sin forma (seda, gasa, tul, organza, pedrería).
