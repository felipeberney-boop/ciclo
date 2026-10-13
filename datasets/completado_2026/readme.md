# Completado a 2026

Lo que faltaba para que las fuentes lleguen a hoy (13/10/2026). Acá están **sólo los años nuevos**: los que
ya estaban siguen en `datasets_procesados/` y no se tocaron.

Hay dos clases de dato, y no se mezclan:

| Archivo | Qué es | Tipo |
|---|---|---|
| `reddit_2026.csv` | Reddit enero–octubre 2026, contado de verdad | **medido** |
| `pasarela_proyeccion_2024_2026.csv` | Pasarela 2024–2026, proyectada desde 2010–2023 | **proyectado** |

Cada fila trae una columna `tipo` con el valor `medido` o `proyectado`. En la app, lo proyectado va en salmón
y punteado, igual que cualquier otro cálculo de un modelo.

---

## Reddit 2026 · medido

**Fuente.** r/femalefashionadvice vía Arctic Shift, del 01/01/2026 al 12/10/2026: 14.495 posts, el mismo
número que da el conteo oficial de Arctic Shift para esas fechas. Son 25 términos, los mismos de la serie
2004–2025.

**Cómo se empalma.** Para recalcular el índice con la misma regla que la serie del repositorio bajamos
también 2022–2025 (unos 65.000 títulos), y probamos tres reglas posibles contra los valores que ya estaban:

| Regla | Error mediano contra el repo |
|---|---|
| Sin suavizar | 37,2 % |
| Media móvil de 3 años hacia atrás | 17,5 % |
| **Media móvil centrada de 3 años** | **2,4 %** |

Es la centrada; en el último año la media usa ese año y el anterior. Entonces el índice 2026 es la media de
2025 y 2026, llevada a la escala de la serie con el valor de 2025 que ya estaba. Como control, 2024
recalculado así difiere del repo en 1,6 % (mediana de 26 términos; columna `control_2024_error_pct`).

**Columnas.** `posts` y `posts_totales_anio` son conteos crudos; `posts_por_mil` es la proporción sin
suavizar; `indice` es el valor comparable con la serie `RDS` / `REC[].r`; `indice_2025_en_repo` es el 2025
que ya estaba, para ver el cambio de un vistazo.

**Cuidado al leerlo.**
- 2026 es un año parcial: faltan octubre a diciembre. Los términos de invierno (trench, cuero, suede)
  pueden estar un poco abajo de lo que van a cerrar.
- El índice puede pasar de 100: 100 sigue siendo el máximo de 2004–2025. Corset (23 posts), hoodie (46) e
  Y2K (22) marcan récord en 2026.
- **Con pocos posts el índice no se puede leer.** 12 de los 25 términos tienen menos de 10 posts en 2026:
  balaclava, chunky sneakers y mom jeans (0), cargo pants, kimono y polka dot (3), leopard y plaid (4),
  crop top (5), quiet luxury (6), burgundy y stripe (8). Sus subidas y bajadas son ruido, no tendencia.
- Al recalcular, el 2025 del repo se movería un poco (la media centrada ahora tiene un año más a la
  derecha). No se cambió: sólo se agregó 2026.

## Pasarela 2024–2026 · proyectado

**Por qué se proyecta.** No hay dato real público. El dataset de Vogue Runway fue scrapeado el 31/03/2023 y
no se actualizó; no encontramos en HuggingFace ningún reemplazo con looks etiquetados de 2024–2026; el
informe anual de Tagwalk es pago. Los números de esas temporadas que circulan en prensa son crecimientos
contra la temporada anterior, no proporción de looks, y no se pueden empalmar.

**Método, elegido por backtest.** Probamos 21 métodos (repetir el último año, media de 3 años, tendencia
lineal de 5 años y 18 variantes de Holt amortiguado). Para cada uno proyectamos desde 2016, 2017, 2018,
2019 y 2020 a 1, 2 y 3 años, y medimos el error contra lo que de verdad pasó (195 comparaciones). Ganó Holt
amortiguado (α = 0,5, β = 0,3, φ = 0,6).

**Qué tan confiable es: poco.** Su error medio es de **20,1 puntos sobre 100**; repetir el último año da
20,9. La proyección casi no mejora a no hacer nada. Por eso cada fila trae `min_80` y `max_80`: el rango
donde cayó el 80 % de los valores reales en el backtest. A tres años ese rango tiene unos 70 puntos de
ancho.

**Qué no hacer con esto.**
- **No entra al K-means.** El modelo sigue entrenado con pasarela medida hasta 2023. Meter estos valores
  sería clasificar con números que el propio backtest dice que no sabemos.
- Sirve para dibujar la continuación de la curva en punteado, con su banda, y para decir «si siguiera
  como venía». No sirve para decir en qué etapa está un atributo en 2026.
- Jeans amplios, medios y ajustados comparten la misma serie de pasarela (Vogue sólo etiqueta «denim»), así
  que su proyección es idéntica.

## Lo que no se completó, y por qué

| Fuente | Hasta | Por qué queda así |
|---|---|---|
| Google Trends | 2025 | 2026 existe, pero está excluido a propósito: 33 de 35 términos marcan récord en abril de 2026, un salto de medición de Google (ver `decisiones.md`, 22/09) |
| Lyst Index | Q2-26 | Ya está al día. Q3-26 todavía no se publicó; suele salir en noviembre |
| H&M | 2018–2020 | No hay versión más nueva pública. En el repo sólo están métricas resumidas, no la serie: no hay de dónde proyectar sin inventar |
| Amazon Reviews | 2023 | Es la última edición pública. Igual que H&M: sólo hay métricas de validación |
| Zara 2018–22 · Mix de marcas | — | Sintéticos; quedaron como demostración de método |

## Cómo se reproduce

Scripts en `codigo/`:

```bash
# 1. títulos de Reddit, un año por proceso (los títulos crudos no se suben)
for y in 2022 2023 2024 2025 2026; do python3 codigo/bajar_titulos_reddit.py posts_$y.jsonl $y & done; wait
# 2. conteo por término y año
python3 codigo/contar_terminos_reddit.py . conteos.csv posts_20*.jsonl
# 3. proyección de pasarela, con su backtest
python3 codigo/proyectar_pasarela.py . pasarela.csv pasarela_backtest.json
# 4. empalme y salida final
python3 codigo/empalmar_reddit_2026.py conteos.csv datasets/completado_2026/reddit_2026.csv \
        pasarela.csv datasets/completado_2026/pasarela_proyeccion_2024_2026.csv
```

## Hasta 2030 (13/10/2026)

En la app, las curvas de Recorridos siguen hasta 2030 con el **cono medido**: el último dato bueno de cada
capa más el cambio mediano de la búsqueda detrendeada a esa distancia, y la banda de cuánto se movió de
verdad (224 tramos). Viene de la otra copia del repositorio y se verificó: `codigo/calcular_cono.py` lo
reproduce cifra por cifra. Reemplaza a la proyección de Holt de pasarela (que sigue acá como dataset
documentado) y a una primera versión, «lo habitual», que se descartó porque incluía el salto de Google de
2025. Resultado: `datasets_procesados/ciclo_cono__incertidumbre_medida.json`.

**No es un pronóstico.** Ninguno de los cuatro métodos probados le gana a repetir el último valor.
