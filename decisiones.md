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
