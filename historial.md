# Historial de versiones

Cómo llegó CICLO de una hipótesis en un papel a un prototipo navegable. Cada punto de este historial
tiene su commit en el repositorio, fechado el día en que pasó.

> **Nota de método.** El repositorio se creó el 06/10/2026, al cerrar la Entrega 2. El historial de
> commits se reconstruyó a partir del registro de trabajo del equipo (`decisiones.md`), fechando cada
> commit en el día real del hito y agregando en él el material producido en ese momento. No es un
> historial capturado en vivo: es el registro del proyecto, declarado como tal.

---

## v0 · 25/08/2026 · Entrega 1

**Qué era.** Una hipótesis, un dataset elegido y un usuario genérico. Sin modelo y sin interfaz.

**Hipótesis.** Cruzar señales de pasarela con búsquedas online y consumo histórico para ubicar una
tendencia en su ciclo.

**Nota: 7,4.** La devolución pidió cinco cosas: usuaria concreta, IA que investigue sola, relaciones
entre líneas, ida y vuelta con imágenes, y fast fashion contra marcas grandes.

## v0.1 · 01/09/2026 · La unidad de análisis

El cambio conceptual más importante del proyecto. «Tendencia» no se puede contar: no existe esa columna
en ningún dataset. La unidad pasa a ser el **atributo** — un color, una estampa, un corte, un material —
porque es lo único que aparece a la vez en la pasarela, en la búsqueda y en el catálogo.

Todo lo que vino después depende de esta decisión.

## v0.2 · 08/09/2026 · Los primeros datasets eran sintéticos

Corrimos K-means y árboles de decisión sobre Zara 2018–22 y Mix de marcas 2025. Correlación máxima entre
variables numéricas: 0,099 y 0,018. El árbol predecía al 50,8 % contra una base de 50,2 %.

**Resultado negativo, documentado y conservado.** Los dos quedan como demostración de método. Está
declarado en la pantalla de Método de la app, no escondido.

## v0.3 · 15/09/2026 · Fuentes reales

Entran Vogue Runway (1,28 M de imágenes de pasarela), Google Trends web y Shopping, Reddit vía Arctic
Shift, H&M (31,8 M de transacciones), Amazon, Lyst, Launchmetrics, Zara y Wish.

También se documenta lo que **no** se pudo: Instagram no tiene serie histórica de hashtags a ningún
precio, TikTok Research API no acepta instituciones argentinas, Pinterest Trends es solo Enterprise.

## v0.4 · 22/09/2026 · El modelo

K-means con k=4 sobre 18 atributos. Se eligió contra regresión lineal y árbol de decisión porque no
tenemos etiquetas de etapa, y etiquetarlas a mano sería contestar la pregunta antes de hacerla.

Silhouette: 0,303 / 0,323 / **0,326** / 0,316 para k de 2 a 5.

**Un error corregido en esta versión.** Al agregar una tendencia nueva, el modelo se reentrenaba y la
tendencia nueva se volvía su propio grupo, renombrando todos los demás. Ahora se entrena sobre las filas
base y las nuevas se asignan al centroide más cercano.

## v0.5 · 23/09/2026 · Jeans por corte, y el jurado externo

Los jeans se separan en amplios, medios y ajustados. Agregados como «denim» no se ve nada, porque las
curvas se cancelan: los ajustados eran el 73 % de la búsqueda en 2012 y en 2025 es 55 / 22 / 23.

Se cargan 19 señales del informe anual de Lyst **sin meterlas al modelo**, para contrastarlo después.
Coinciden donde el modelo se la juega. No coinciden en calzado, que no medimos: es el agujero más
concreto que tenemos y está declarado.

## v1.0 · 05/10/2026 · Prototipo de la Entrega 2

**La regla del salmón.** Lo negro es medido, lo salmón es calculado o interpretado por un modelo. Rige
dentro de la app y dentro de la presentación.

**De baja a alta fidelidad.** Empezamos con wireframes esquemáticos y los reemplazamos por pantallas con
los gráficos dibujados a partir de los datos reales. Un esquema decide qué información entra; una
pantalla real permite además discutir si el dato se entiende.

**Dos prototipos navegables.** Escritorio (10 pantallas de 1440×900, 82 conexiones) y teléfono (las
mismas 10 a 393×852, 63 conexiones). El mobile no es el de escritorio achicado: siete secciones pasan a
cinco pestañas abajo, y en Consulta los botones son Cámara y Galería porque arrastrar un archivo en un
teléfono no existe.

**Presentación.** 20 láminas generadas por código, recortadas a 17 al ensayarla.

## Lo que falta para la Entrega 3

- Conectar la Groq API en vivo. Hoy IA-5 corre con prompt fijo.
- Separar pasarela y venta por género. Vogue y los agregados de H&M no traen esa columna; está declarado
  como límite en la pantalla de Método, no simulado.
- Sumar calzado, que es donde el contraste con Lyst no coincide.
- Verificar la licencia exacta de las cuatro fuentes marcadas *a verificar* en
  `datasets/fuentes_y_descargas.md`.

---

## Dónde ver cada versión

| | |
|---|---|
| Registro de decisiones, fechado | `decisiones.md` |
| Entrega 1 | `entregas/entrega_1/` |
| Entrega 2 | `entregas/entrega_2/` |
| App funcionando | `app/index.html` |
| Láminas de la presentación | `diseno/prototipos/prototipo_entrega_2_laminas/` |
| Prompts versionados | `prompts/` |
