# Series de Google Trends, Lyst y H&M en CSV

Las series procesadas que usa la app, exportadas a CSV plano. Armadas el **13/10/2026**, también
para poder compartirlas con otros grupos de la cátedra.
Proyecto CICLO — Sistemas generativos e IA para Diseño, UdeSA, 2º semestre 2026.
Berney · Dobler.

---

## Leé esto primero: qué hay y qué no

**Los CSV crudos de Google Trends, tal como se exportaron, no están en este paquete.** No están en el
repositorio del proyecto ni en los archivos de trabajo: viven en la carpeta de Drive del grupo. Si
necesitás el export original, pedíselo a Felipe Berney.

Lo que sí está acá son **las series ya procesadas** que alimentan la app. Son datos reales y
verificables, pero pasaron por dos transformaciones que tenés que conocer antes de usarlos; están
explicadas abajo en «Cómo se procesaron».

**Hay columnas de la tabla que no puedo completar con certeza** — la categoría de Trends que se usó
y si cada término se exportó solo o comparado con otro. Esa información sólo está en el export
original. Las dejo marcadas como **no consta** en vez de suponerlas. No las completes de memoria sin
abrir el archivo original.

---

## Los archivos

| Archivo | Qué contiene | Filas |
|---|---|---|
| `trends_mundo__web_anual.csv` | Búsqueda web mundial, un término por atributo, 2004–2025 | 352 |
| `trends_argentina__web_anual.csv` | Búsqueda web en Argentina, 2004–2025 | 154 |
| `trends_mundo__jeans_por_termino.csv` | Los 12 términos de jean sin agrupar, uno por uno | 286 |
| `trends_mundo__jeans_corte_web.csv` | Participación por corte (amplio / medio / ajustado), búsqueda web | 66 |
| `trends_mundo__jeans_corte_shopping.csv` | Lo mismo, pero en Google Shopping | 66 |
| `lyst_index__34_trimestres.csv` | Lyst Index, Q1-18 a Q2-26 | 640 |
| `hm__articulos_distintos_por_corte_de_jean.csv` | H&M, artículos distintos por corte | 3 |

---

## Tabla de términos

Una fila por término. «Idioma» sale del término mismo; «categoría» y «comparado con» no constan.

### Búsqueda web · mundial · `trends_mundo__web_anual.csv`

| Término buscado | Atributo | Región | Idioma | Rango | Frecuencia | Descargado | Categoría | Tipo | ¿Comparado? |
|---|---|---|---|---|---|---|---|---|---|
| `cargo pants` | Cargo | Mundial | inglés | 2004–2025 | anual (ver nota) | 22/09/2026 | no consta | Búsqueda web | no consta |
| `hoodie` | Buzo / athleisure | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `leather jacket` | Cuero | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `polka dot dress` | Lunares | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `floral dress` | Floral | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `leopard print` | Animal print | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `lace dress` | Encaje | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `kimono jacket` | Kimono | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `cape coat` | Capa | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `trench coat` | Trench | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `corset top` | Corset | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `striped shirt` | Rayas | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `suede jacket` | Gamuza | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| jeans amplios *(suma)* | Jeans amplios | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | suma de 6 términos |
| jeans medios *(suma)* | Jeans medios | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | suma de 4 términos |
| jeans ajustados *(suma)* | Jeans ajustados | Mundial | inglés | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | suma de 3 términos |

### Búsqueda web · Argentina · `trends_argentina__web_anual.csv`

| Término buscado | Atributo | Región | Idioma | Rango | Frecuencia | Descargado | Categoría | Tipo | ¿Comparado? |
|---|---|---|---|---|---|---|---|---|---|
| `jean baggy` | Jeans amplios | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `jean chupin` | Jeans ajustados | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `buzo oversize` | Buzo / athleisure | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `campera de cuero` | Cuero | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `animal print` | Animal print | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `pantalon cargo` | Cargo | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |
| `corset` | Corset | Argentina | español | 2004–2025 | anual | 22/09/2026 | no consta | Búsqueda web | no consta |

> **Por qué la capa argentina usa términos compuestos.** Se descartaron «lunares», «rayas»,
> «gamuza» y «bordo»: en español también son manchas de la piel, líneas, un paño de limpieza y un
> club de fútbol. El ruido se comía la señal.

### Los 12 términos de jean · `trends_mundo__jeans_por_termino.csv`

Todos mundiales, en inglés, 2004–2025, descargados el 22/09/2026, búsqueda web, categoría no consta.

| Corte | Términos |
|---|---|
| Ajustado | `skinny` · `slim` · `jeggings` |
| Medio | `straight leg` · `bootcut` · `flare` · `tapered` |
| Amplio | `baggy` · `mom` · `wide leg` · `barrel` · `boyfriend` · `relaxed fit` |

### Google Shopping · `trends_mundo__jeans_corte_shopping.csv`

Misma lista de términos, pero sobre la propiedad **Shopping** de Google Trends en vez de búsqueda
web. Rango **2008–2025** (Shopping no tiene datos antes de 2008), descargado el 22/09/2026.
Categoría y comparación: no constan.

---

## Nota sobre la frecuencia

Las series de este paquete son **anuales**. La exportación original de Google Trends para un rango
de 2004 a hoy devuelve datos **mensuales**, así que lo más probable es que el crudo sea mensual y la
agregación a año la hayamos hecho nosotros — pero **no lo puedo confirmar sin abrir el export
original**. Si necesitás granularidad mensual, pedí los archivos de Drive.

---

## Cómo se procesaron

Dos transformaciones, en este orden. Las dos importan si vas a comparar estos datos con los tuyos.

**1 · Detrend.** Cada término se divide por la media de los 35 términos de moda de ese año. Es para
sacar la deriva general de Google: el volumen total de búsquedas crece con los años y sin corregirlo
casi todo parece estar en su pico. **Consecuencia:** estos valores son *relativos al resto del
mercado de moda*, no absolutos. Un término que baja acá puede estar creciendo en términos absolutos
y perdiendo contra los demás.

**2 · Normalización.** Cada serie se lleva a su propio máximo, en escala 0–100. **Consecuencia:** se
comparan formas y momentos, no volúmenes. Que dos series lleguen a 100 no significa que se busquen
lo mismo.

### Advertencias

- **2025 está contaminado.** El cambio medio anual de los 16 atributos es de +3,2 puntos; en 2025 es
  **+18,9**, suben 15 de 16 series y 12 tocan su máximo histórico el mismo año. Es un salto de
  medición de Google, no de la moda. **Nosotros excluimos 2025 de todos los cálculos.** Si lo vas a
  usar, tenelo en cuenta.
- **2026 excluido entero.** 33 de 35 términos marcan su récord el mismo mes (abril de 2026).
- **Shopping arranca en 2008.** Las celdas de 2004–2007 van vacías a propósito: ahí no hay dato, no hay un cero.
- Los CSV de corte de jean están en **porcentaje de participación** dentro de la categoría jeans, no
  en el índice de Trends.

---

## Las otras dos fuentes

### Lyst Index · `lyst_index__34_trimestres.csv`

- **Qué es:** ranking trimestral de las marcas más buscadas. 34 trimestres (Q1-18 a Q2-26), 55
  marcas en 640 puestos.
- **Fuente:** https://www.lyst.com/the-lyst-index/ — transcrito a mano el **15/09/2026**.
- **Licencia:** contenido editorial de Lyst. Se cita la fuente y el trimestre; **no se redistribuye
  el informe**. Si lo usás, atribuí a Lyst.
- **Advertencia 1:** los cuatro trimestres de 2018 son top 10, no top 20 — el índice se amplió en
  Q1-19. Un puesto vacío en 2018 no significa lo mismo que en 2019.
- **Advertencia 2:** en Q1-26 Lyst recalibró su fórmula y Chanel y Dior entraron directo al 1º y 3º
  puesto. Es un corte en la serie, no un crecimiento real. No calcules métricas que crucen ese corte.

### H&M · `hm__articulos_distintos_por_corte_de_jean.csv`

- **Qué es:** cuántos artículos distintos de cada corte de jean hay en el catálogo. Es **el único
  agregado de H&M que quedó en los archivos del proyecto** — el resto de las métricas de H&M
  (unidades, precio medio, colores por mes) están en la app pero no las extrajimos a CSV.
- **Fuente:** H&M Personalized Fashion Recommendations, Kaggle —
  https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations
  Descargado el **22/09/2026**.
- **Base:** 31.788.324 transacciones (2018-09-20 a 2020-09-22), de las que se usaron 30.570.975
  compras de adulto, sin Baby/Children.
- **Licencia:** reglas de la competencia de Kaggle — **uso académico y no comercial**. Requiere
  cuenta de Kaggle para descargarlo. No lo redistribuyas: pasá el link.

---

## Licencia de los datos de Google Trends

Términos de servicio de Google. Uso académico con atribución; **no es dato abierto** y no se
redistribuye como producto. Si los usás en una entrega, citá Google Trends y la fecha de descarga.

---

## Qué no hay en este paquete

Ninguna clave de API, token ni archivo `.env` — verificado antes de empaquetar.

Tampoco están los datasets pesados del proyecto (Vogue Runway, 99 MB; las transacciones completas de
H&M; Amazon Reviews). Están documentados con su link de descarga y su fecha en
`datasets/fuentes_y_descargas.md` del repositorio: https://github.com/felipeberney-boop/ciclo
