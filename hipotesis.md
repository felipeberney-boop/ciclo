# La hipótesis: qué está verificado y qué falta

Estado al 27/10/2026. Cada línea sale de `decisiones.md` (la fecha entre paréntesis es la entrada); ningún número es
nuevo.

**La hipótesis de la Entrega 1:** «Al cruzar señales tempranas provenientes de los desfiles con el crecimiento de
búsquedas online y datos históricos de consumo, sería posible identificar en qué etapa de su ciclo se encuentra una
tendencia.» Junta tres afirmaciones: que la pasarela **adelanta** a la búsqueda, que se puede **predecir**, y que se
puede **identificar la etapa** del presente.

**Cómo queda:** cruzando pasarela y búsqueda, CICLO distingue los atributos que suben de los que no, y esa lectura
coincide con fuentes que el modelo nunca vio. No predice, y la pasarela no adelanta a la búsqueda:
ni por año ni por temporada. Pasarela y búsqueda se mueven juntas, a la vez.

---

## Verificado

**Con prueba formal**

| Afirmación | Prueba | Contra qué fuente externa |
|---|---|---|
| Lo que el K-means pone en ascenso o pico es lo que más crece afuera | Los tres de arriba (Y2K, cargo, jeans baggy) son los tres que más crecen, de 14: p = 0,0013 (η² = 0,88) barajando las etapas 10.000 veces; por rangos, p = 0,047. Criterio commiteado antes de calcular (27/10) | Reddit, r/femalefashionadvice, 2020–21 contra 2023–24. El modelo no lo usa |
| CLIP reconoce los atributos en una foto | AUC mediano 0,90 en 150.000 looks de Vogue que no están en el índice (13/10) | Las etiquetas de Vogue de esos looks |

**Coherente en los casos, sin prueba formal.** Son ejemplos que el modelo no vio y van en la dirección que dice. No
alcanzan como prueba: son pocos, y en dos de ellos la ventana toca 2025, que tiene el salto de medición de Google.

| Afirmación | El caso | Fuente que el modelo no vio |
|---|---|---|
| Los jeans ajustados están saturados | −39 % en reseñas, 2019→2022 | Amazon Reviews |
| Los jeans amplios están en pico | +79 % en reseñas, 2019→2022; +95 % en búsquedas de compra, 2022→2025 (2025, dudoso) | Amazon Reviews, Google Shopping |
| El Y2K está en ascenso | +203 % en búsquedas de compra (la ventana incluye 2025) | Google Shopping |
| Pico coincide con Lyst | Jeans anchos +55 % (2024) y cargo +56 % (2022), los dos en pico. El corset (+74 %, 2021) coincidía con el modelo de septiembre, de 18 atributos; el de hoy no lo incluye (23/09) | Informe anual de Lyst |

**El límite de esta columna.** Atributo por atributo, contra Amazon (n = 11) no hay correlación; contra Google
Shopping (n = 12) el nivel de búsqueda (+0,61) y el de pasarela (+0,67) pasan raspando el umbral de 0,6, y Shopping
sigue siendo búsqueda, no venta (13/10). Y lo que sí se probó formalmente (Reddit) separa lo que sube de lo que no,
pero **no distingue «en retorno» de «saturada»** (p = 0,88).

---

## Refutado

| Afirmación | Prueba | Resultado |
|---|---|---|
| Se puede predecir la búsqueda | Cuatro métodos contra repetir el último valor, error a cinco años (13/10) | Ninguno gana: suavizado 22,1 contra 21,6; análogos 15,9 contra 15,5; reversión a la media 21,7 contra 21,6; la etapa como regla 62,9 % contra 62,9 % |
| Con más series, sí | Un modelo global sobre las 16 series, validado dejando afuera cada una (13/10) | Tampoco: −2,0 % a un año, +0,4 % a dos, −2,6 % a tres, −5,8 % a cinco |
| La búsqueda predice la venta | VISUELLE: 5.577 productos de Nunalie con venta semanal real, SS17–AW19 (13/10) | Por producto, r = +0,036: explica el 0,1 % y fuera de muestra es 6,5 % peor que el promedio de la categoría. Por categoría y temporada (134 grupos), r = +0,184: cerca del 4 %. El momento, nada |
| La pasarela adelanta a la búsqueda, a escala anual | Correlación con rezagos, en niveles y en cambios año a año (13/10) | Máxima sin rezago (+0,43), cae a +0,12 con dos años. En cambios, pasan 2 de 65 pruebas: lo que da el azar |
| La pasarela adelanta a la búsqueda, por temporada | 14 atributos, cada desfile contra la misma temporada del año anterior y la búsqueda mensual contra el mismo mes del año anterior, rezagos de 0 a 18 meses, 10.000 barajadas, criterio commiteado antes (27/10) | Ningún rezago de 3 a 18 meses pasa: medianas entre −0,04 y +0,04 (p de 0,13 a 0,86; hacía falta menos de 0,007). Sólo el rezago 0 asoma (+0,08, p = 0,026) y tampoco pasa la corrección |
| Los datasets iniciales sirven | K-means y árbol sobre Zara 2018–22 y el mix de marcas (08/09) | Sintéticos: el árbol acierta 50,8 % contra una base de 50,2 % |

---

## Probado el 27/10: la pasarela, temporada a temporada → refutado

**Resultado.** Con el criterio fijado y commiteado antes de calcular
(`datasets/pruebas/prueba_temporada_preregistro.md`, `codigo/prueba_temporada.py`), la pasarela **no adelanta** a la
búsqueda a escala de temporada. Entraron 14 atributos (Lunares quedó afuera: 7 looks por temporada; Floral no se
exportó). Ningún rezago entre 3 y 18 meses tiene una mediana distinta de cero: van de −0,04 a +0,04, con p entre 0,13 y
0,86. Atributo por atributo no hay un patrón: cada uno cambia de signo según el rezago. La única señal, chica, está en
el rezago 0 (+0,08, p = 0,026, que no pasa la corrección por siete rezagos): las dos capas se mueven juntas, que es lo
mismo que se vio a escala anual. Resultado completo en `datasets/pruebas/prueba_temporada_resultado.json`.

**Qué cierra.** La primera afirmación de la hipótesis original —«señales tempranas de los desfiles»— queda rechazada
con la mejor resolución que permiten los datos públicos. CICLO lee el presente cruzando capas; no anticipa.

Lo que sigue es el plan tal como se escribió antes de correrla.


**Qué sigue vivo.** A escala anual la pasarela no adelanta. Pero un adelanto de seis a nueve meses —el desfile de
febrero, la búsqueda del otoño siguiente— queda adentro del mismo año, y con datos anuales no se puede ver.

**Una precisión antes de prometerla.** Del lado de la pasarela la prueba no puede ser mes a mes: Vogue Runway
(1,71 millones de filas) trae `season` (Spring, Fall, Resort, Pre-Fall), `year` y `category`, pero no la fecha del
desfile. Cada temporada se ubica en su mes por calendario: Fall en febrero–marzo, Spring en septiembre–octubre del año
anterior, Resort en mayo–junio, Pre-Fall en diciembre–enero. Son cuatro puntos por año, no doce. La búsqueda sí es
mensual (los lotes de Google Trends, 2004–2026, ya están en `datasets/trends_lotes/`).

**Qué haría falta**
1. Bajar `VogueRunway.parquet` (99 MB, público, `traopia/vogue-runway`). No hacen falta las imágenes.
2. Volver a agregar la pasarela por temporada en vez de por año, con las mismas etiquetas de cada atributo que ya
   usa `codigo/verificar_pasarela.py`: la proporción de looks de cada temporada que lleva el atributo, 2000–2023.
3. Pasar la búsqueda mensual a esas ventanas y **quitarle la estación**. Es la trampa de esta prueba: un abrigo que
   desfila en marzo y se busca en noviembre parece un adelanto de ocho meses y es sólo el invierno. Se compara cada
   temporada con la misma temporada del año anterior (Fall contra Fall).
4. Correlacionar los cambios con rezagos de una a seis temporadas, por atributo, con el criterio escrito y commiteado
   antes (como la prueba de Reddit) y corregido por cantidad de pruebas: unos 17 atributos por 6 rezagos son ~100
   pruebas, y por azar pasarían 5.
5. Contarlo salga como salga, en la app (Método) y en el making of.

**Cuánto trabajo.** Dos o tres días: medio día para bajar y filtrar (las mismas reglas: «Collection», sin novias,
2000–2023), un día para el script y los controles, medio día para escribirlo. El corte de la búsqueda en 2024 deja
unos 20 años: unas 40 temporadas principales por atributo.

**Riesgos que conviene decir antes.** Los atributos de nicho tienen pocos looks por temporada y van a dar series
ruidosas; puede que sólo los grandes (denim, cuero, floral, cargo) tengan señal suficiente. Y si aparece un adelanto,
hay que mirarlo con el mismo cuidado que el «casi-hallazgo» del 13/10, que se desarmó al pasar de niveles a cambios.

**Estado (27/10).** El diseño, las etiquetas, el criterio y la corrección por cantidad de pruebas están fijados en
`datasets/pruebas/prueba_temporada_preregistro.md`, commiteado antes de tener los datos. El parquet de Vogue ya está
bajado. Falta la búsqueda mensual de los atributos de CICLO: tres lotes de Google Trends
(`datasets/plan_exportacion_trends_4.csv`, lotes 23 a 25).

**¿Entra antes del 17/11?** Sí, con margen: son unos tres días de trabajo y faltan tres semanas. Si da que sí, es el
mejor cierre posible para la entrega final, porque rescata la primera afirmación de la hipótesis original («señales
tempranas de los desfiles») con una prueba que se pudo haber caído. Si da que no, cierra la pregunta con la mejor
resolución que permiten los datos públicos.
