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

## v1.1 · 20/10/2026 · Netlify, Groq en vivo, el asistente y Diseñar por taxonomía

App oficial en Netlify con IA-5 en vivo y «Preguntar» (el LLM de la clase, con la API key de cada uno). K-means
sin 2025 y sin calzado (17 atributos). Estética de revista. Después, siete frentes: la entrada de tres
preguntas siempre, `señal()` como única fuente de color de estado, la taxonomía nueva (jean = pantalón +
denim), 35 materiales y detalles, combinaciones imposibles fuera, recomendación sólo con evidencia, el
contador de dato medido y la barra que acumula. Commits `d9f6c4f` a `e6a401a`; la versión anterior quedó en
`diseno/prototipos/versiones_de_la_app/app_2026-10-20_9035227.html`.

## v1.2 · 20/10/2026 · Cajas, procedencia sin color, dato prestado y «El ciclo»

Jeans reagrupados (mom y boyfriend a medios) y K-means recalculado, con nombres por asignación óptima. Toda
opción es una caja cerrada; el color es sólo la señal y la procedencia va en texto (medido, interpretado,
prestado); se retira la regla del salmón. Las hojas sin serie toman la de un pariente: 26 directo, 39 prestado,
63 sin dato. Dibujos para detalles y estampas que faltaban. Recorridos pasa a «El ciclo» (cuándo picó y cuánto
tardó en volver) y el gráfico arranca donde arranca el dato. Commits `9f842b8` a `aa99cf9` y siguientes; la
versión anterior quedó en `diseno/prototipos/versiones_de_la_app/app_2026-10-20_cc69c93.html`.

## v1.3 · 20/10/2026 · 65 series de búsqueda y el corte en 2024

Dos planes de Google Trends (70 términos, trench coat de ancla): entran 49 series nuevas a las 16 que había.
Todo el análisis corta en 2024 porque 2026 viene contaminado. Hojas con dato propio: 26 → 75.

## v1.4 · 20/10/2026 · Nombres de taller y el chat como herramienta de diseño

Materiales con nombre rioplatense, término de industria y qué es; la tabla de materiales corregida; Buzos y
Sweaters por separado; fuera los contadores; siluetas enteras; cuero y gamuza como color; los colores de
Tendencias explicados. Preguntar pasa a ser una herramienta: sabe qué estás diseñando, lee una imagen con CLIP,
trae el dato con su serie y termina en un cambio que se aplica con un botón.

## v1.5 · 21/10/2026 · El filtro de estación y por qué no hay calzado

Plan 3 de Google Trends (accesorios y calzado): no entra ninguno. Filtro nuevo de estación sobre todas las series:
caen capris, cashmere y wool coat. Toile confirmado como término equivocado. El calzado queda pendiente por la
pasarela (CLIP). 71 hojas con dato propio, 48 prestadas, 12 sin dato.

## v1.6 · 21/10/2026 · Calzado y accesorios en Diseñar, y todas las series en los gráficos

Calzado y Accesorios como prendas (13 dibujos nuevos); zapatillas, mocasines y tote con dato propio. El ciclo,
Tendencias y el recorrido pasan de 16 a 65 series, con filtro por grupo.

## v1.7 · 25/10/2026 · IA-5 en vivo en la app oficial

«Pedir lectura en vivo» deja de depender de Netlify: llama a Groq desde el navegador con la clave de cada uno, la
misma de «Preguntar». Prompt v4 (el peso en la búsqueda pasa a 2022→2024). Netlify queda pausado y señalado como
tal. La versión anterior quedó en `diseno/prototipos/versiones_de_la_app/app_2026-10-25_9a92475.html`.

## v1.8 · 26/10/2026 · El calzado en la pasarela

Cada estilo de calzado en Diseñar suma su línea de pasarela leída por CLIP, como interpretación y sin señal. Zapatillas
y botas texanas con su curva de 2010 a 2023; el resto, con el motivo por el que CLIP no puede medirlo. El chat pasa a
prompt v3 y deja de decir que no hay calzado. Zoe Dottori Greco deja el grupo. La versión anterior quedó en
`diseno/prototipos/versiones_de_la_app/app_2026-10-26_745a5aa.html`.

## v1.9 · 26/10/2026 · Auditoría: integridad, semáforo y celular

Una auditoría con Playwright en las once vistas, a 1400 y 393 px, en claro y en oscuro, y nueve frentes, cada uno con
su commit:

- **Fuera la portada vieja.** La marca CICLO llevaba a un menú de septiembre, sin calzado ni accesorios y sin salida.
  Ahora abre el cambio de perfil; la bajada y la firma pasan al gate y al colofón.
- **El calzado, contado como resultado.** Dos intentos (Google Trends y CLIP), estilo por estilo, en Diseñar y en Método.
- **El semáforo.** Que algo gane o pierda terreno va en negro; el color queda para Entrar, Esperar y Salir, con su
  palabra. En oscuro dejan de volver el lavanda, el rosa y el verde.
- **Integridad.** Retornos se calcula con la serie y la regla de El ciclo, hasta 2024 (lunares: cada 7 años, no 6).
  Tendencias muestra la etapa del K-means cuando existe. Cifras alineadas en Método y el pie. Los jeans por corte, hasta
  2024 y con el reagrupado.
- **CLIP en Preguntar** con el umbral de Buscar por imagen (0,35), bajadas con progreso y «El dato» completo.
- **Celular.** Gráficos legibles que se deslizan, El ciclo plegado (de 22.000 a 10.200 px), el menú entero a la vista.
- **Hojas sin dato.** Cuatro préstamos y las 24 estampas con definición: 74 medidas, 42 prestadas, 17 sin dato.
- **Capturas y documentación.** 16 capturas nuevas, reproducibles con `codigo/capturar_pantallas_de_la_app.js`.

Commits `64c25a9` a este. La versión anterior quedó en `diseno/prototipos/versiones_de_la_app/app_2026-10-26_d589243.html`.

## v1.10 · 27/10/2026 · La capa de uso

Navegar como una herramienta profesional, sin perder la revista. Encabezado fijo de una línea, menú en letra legible,
«Más» como panel de tarjetas con un dato y su fuente, menú a pantalla completa en el celular, tarjetas con esquinas,
línea de lectura y botón para volver arriba, Método en acordeón. Durante la entrada no se ve el menú. Referencia:
stytrix.com, sin su naranja (el color sigue siendo sólo la señal). Capturas regeneradas. La versión anterior quedó en
`diseno/prototipos/versiones_de_la_app/app_2026-10-27_7e5ebfd.html`.

## Presentación · Entrega 3

Una sola presentación, la web: https://felipeberney-boop.github.io/ciclo/presentacion/ (código en `app/presentacion/`).

El 26/10 también se armaron 22 láminas en Figma Slides y un prototipo navegable en Figma. El 27/10 salen del
repositorio: la referencia de la cátedra es una página web, y el prototipo de Figma ya no coincidía con la app. El
prototipo navegable es la app publicada.

---

## Lo que falta para la Entrega 3

- Separar pasarela y venta por género. Vogue y los agregados de H&M no traen esa columna; está declarado
  como límite en la pantalla de Método, no simulado.

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
