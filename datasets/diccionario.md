# Diccionario de datos

Qué significa cada columna, en qué unidad está y qué filtro se le aplicó.

---

## Vogue Runway · `VogueRunway.parquet`

| Columna | Tipo | Significado |
|---|---|---|
| `designer` | categórica | Casa o diseñador del desfile |
| `season` | categórica | Temporada (ej. «Spring 2020 Ready-to-Wear») |
| `year` | entero | Año del desfile |
| `city` | categórica | Ciudad del desfile |
| `section` | categórica | Tipo de foto: `Collection`, detalle, beauty |
| `tags` | lista | Atributos detectados por un modelo de visión |

**Filtros aplicados:** `section = Collection`, sin Bridal, años 2000–2023.
De 1.281.633 imágenes quedan 902.566 looks.

**Advertencias.** Los tags los generó un modelo genérico: reconoce «Leather Jacket» o «Polka Dot» pero no
«rayas» ni «oversize», y no distingue cortes de jeans. Antes de 2010 las fotos eran más chicas y el
modelo detecta menos: ese tramo se dibuja punteado. En 2020 y 2021 hubo menos desfiles y más lookbooks.

## Google Trends

| Columna | Tipo | Unidad |
|---|---|---|
| `termino` | categórica | Término de búsqueda |
| `anio` | entero | Año |
| `valor` | numérica | Índice relativo de Google, 0–100 dentro de cada consulta |

**Transformación.** Cada término se divide por la media de los 35 términos de moda de ese año, para
sacar la deriva general de Google. Sin ese ajuste casi todo parece estar en su pico.

**Filtros.** Se excluye enero–septiembre de 2026 entero: 33 de 35 términos marcan su récord el mismo mes,
incluso búsquedas sin relación entre sí. Es un salto en la medición, no en la moda.

**Argentina.** Se descartaron «lunares», «rayas», «gamuza» y «bordo»: en español también son manchas de
la piel, líneas, un paño de limpieza y un club de fútbol. Por eso la capa argentina usa términos compuestos.

## H&M · `transactions_train.csv` + `articles.csv`

| Columna | Tipo | Unidad |
|---|---|---|
| `t_dat` | fecha | Día de la compra |
| `article_id` | ID | Artículo |
| `price` | numérica | Escala normalizada de H&M, no pesos ni euros |
| `index_group_name` | categórica | Ladieswear, Menswear, Divided, Sport, Baby/Children |
| `colour_group_name` | categórica | Color del artículo |
| `product_type_name` | categórica | Tipo de prenda |

**Filtros.** Sin Baby/Children (34.711 artículos). Quedan 30.570.975 compras de adulto.

**Métricas derivadas, por mes y por atributo:** `u` unidades vendidas, `p` precio medio, `c` colores
distintos vendidos, `a` artículos distintos vendidos. La base de cada mes son las unidades adultas de ese mes.

## Lyst Index

| Columna | Tipo | Unidad |
|---|---|---|
| `trimestre` | categórica | Q1-18 a Q2-26 |
| `marca` | categórica | Nombre de la marca |
| `puesto` | entero | 1 a 20; 1 es el más alto |

**Advertencia.** Los cuatro trimestres de 2018 son top 10: el índice se amplió a 20 recién en Q1-19.
En Q1-26 Lyst recalibró su fórmula y Chanel y Dior entraron directo al 1º y 3º puesto. Es un corte en la
serie: las métricas se calculan dentro de cada tramo, nunca a través.

## Reddit · Arctic Shift

| Columna | Tipo | Unidad |
|---|---|---|
| `termino` | categórica | Término buscado en el título |
| `anio` | entero | Año |
| `posts` | entero | Posts cuyo título nombra el término |
| `indice` | numérica | `posts` dividido por el total de posts del subreddit ese año |

**Suavizado.** Media móvil de 3 años. En 2012–2013 el subreddit era chico: sus primeros años exageran
lo que se nombraba entonces.

---

# Diccionario de los datos procesados

## `datasets_procesados/ciclo_series__anual_por_atributo.json`

| Clave | Contenido |
|---|---|
| `REC` | Un objeto por atributo: curvas `v` (pasarela), `g` (búsqueda mundo), `a` (búsqueda Argentina), `r` (Reddit), 2004–2025, cada una llevada a su propio máximo (0–100) |
| `JE` | Jeans por corte: `web` y `shop` con las series de amplio, medio y ajustado; `hm` con los artículos distintos en H&M |
| `KM` | Tabla del modelo: 18 filas con `pn`, `pm`, `bn`, `bm` (nivel y momento en pasarela y búsqueda), `cl` (grupo asignado), más la validación `amz_19_22` y `shop_22_25` |
| `LYST` | 34 trimestres × 55 marcas con el puesto, o `null` si esa marca no estaba en el top 20 |
| `COL` | Diccionario de colores medidos, en hexadecimal |
| `RDS` | Series de Reddit por término |

**Nivel** es dónde está hoy contra su propio máximo; 100 % es que está en su pico histórico.
**Momento** es cuánto cambió en los últimos años: pasarela 2021–23 contra 2018–20, búsqueda 2024–25
contra 2021–22.

## `datasets_procesados/ciclo_graficos__geometria_calculada.json`

Coordenadas ya calculadas de cada gráfico del prototipo, en píxeles. Lo genera
`codigo/calcular_geometria_de_graficos.js`. Es un intermedio: no es dato de investigación.

## `datasets/completado_2026/reddit_2026.csv` · medido

| Columna | Contenido |
|---|---|
| `termino` | Término buscado en el título (los combinados, como `baggy jeans + mom jeans`, se suman) |
| `posts` · `posts_totales_anio` | Conteos crudos, 01/01–12/10/2026 |
| `posts_por_mil` | Proporción sin suavizar |
| `indice` | Comparable con `RDS` y `REC[].r`: media móvil centrada, empalmada en el 2025 del repo. Puede pasar de 100 |
| `indice_2025_en_repo` | El 2025 que ya estaba, para comparar |
| `control_2024_error_pct` | Diferencia entre 2024 recalculado y el 2024 del repo |
| `tipo` | Siempre `medido` |

## `datasets/completado_2026/pasarela_proyeccion_2024_2026.csv` · proyectado

| Columna | Contenido |
|---|---|
| `id` · `atributo` · `tag_vogue` | Igual que en `REC` |
| `valor` | Proyección de la curva de pasarela (0–100, misma escala que `REC[].v`) |
| `min_80` · `max_80` | Rango donde cayó el 80 % de los valores reales en el backtest |
| `tipo` | Siempre `proyectado` |
| `fuente_o_metodo` | Método y parámetros |

**No entra al K-means.** El error medio del backtest es 20,1 puntos sobre 100. Ver el readme de la carpeta.
