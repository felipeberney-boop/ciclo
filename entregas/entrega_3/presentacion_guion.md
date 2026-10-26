# Entrega 3 · guion de la presentación (03/11/2026)

Texto de cada lámina, verificado contra el repo el 26/10/2026. Cada cifra dice de dónde sale; si una cifra no está
en el repo, no va. Las correcciones respecto del guion original están marcadas con **(corregido)**.

**01 · Portada.** CICLO. «Dónde está una tendencia en su ciclo de vida». Sistemas generativos e IA para Diseño
(K534/K576), UdeSA, 2º semestre 2026. Felipe Berney · Abril Dobler **(corregido: el readme y la app nombran a los dos;
confirmar)**. Entrega 3 · 03.11.2026.

**02 · La hipótesis.** Cruzando pasarela, búsqueda y venta se puede anticipar qué va a estar de moda.

**03 · La mitad que sí: leer el presente.** Validado contra fuentes que el modelo nunca vio (El modelo, «¿Acertó?»):
- Jeans ajustados, en «saturada»: −39 % en reseñas de Amazon 2019–2022.
- Jeans amplios: +79 % en Amazon y +95 % en Google Shopping.
- Y2K, el único en ascenso: +203 % en búsquedas de compra.
- El K-means agrupó los 17 atributos sin ver ninguno de esos datos.
**(corregido: sale el chi² 782,6. Es la estructura de Zara 2018–22, un archivo sintético; en la app ahora está
rotulado «demostración».)**

**04 · La mitad que no: anticipar.** Cuatro métodos, ninguno le gana a repetir el último valor (Método, «Hasta 2030»):
suavizado con tendencia amortiguada 22,1 contra 21,6 de error a 5 años · análogos históricos 15,9 contra 15,5 ·
reversión a la media 21,7 contra 21,6 · la etapa del ciclo como regla 62,9 % contra 62,9 %.

**05 · Y no es por falta de datos.** **(corregido: no «sumamos series».)** Un solo modelo global entrenado sobre las 16
series juntas tampoco le gana a repetir el último valor: −2,0 % a un año, −5,8 % a cinco (decisiones.md, 13/10). Y contra
ventas reales: VISUELLE, 5.577 productos de Nunalie con ventas semanales; a nivel producto la búsqueda previa no explica
la venta (correlación +0,036). La tendencia de un atributo, año a año, casi no tiene memoria más allá del último valor.

**06 · Qué es CICLO entonces.** Un instrumento descriptivo, no un predictor. La punteada hasta 2030 no es un pronóstico:
es dónde quedaría la curva si se moviera como la mediana de la historia; error medido ±8,8 a un año y ±23,1 a cinco
(calibrado con 2025 corregido adentro, como dice Método). La ventana de cada perfil marca hasta dónde ese error sirve.

**07 · Las fuentes.**
- Vogue Runway: 1.281.633 imágenes con diseñador, temporada y etiquetas, 2000–2023.
- Google Trends: 65 series mundiales en inglés y 14 términos en español para Argentina, hasta 2024.
- Zara febrero 2024: 228 prendas únicas, descripciones reales (licencia MIT).
- Lyst Index: 34 trimestres, Q1-18 a Q2-26.
**(corregido: salen «Zara 660 productos 2018–22», sintético, y «ocho marcas, 1.814 productos», que no tiene fuente en el
repo. Si se nombran, como datasets de demostración.)**

**08 · El procesamiento.** De 1,28 millones de imágenes a series anuales por atributo. Tres planes de exportación de
Google Trends con «trench coat» de ancla. **(corregido)** En los lotes nuevos entraron 49 términos y 35 no, cada uno con
su motivo: ruido (máximo bajo 6 o menos de 24 meses con señal), menos de 12 años útiles, o estacionalidad (7 términos)
— `datasets/trends_lotes/informe.md`. Hoy, sobre 133 hojas: **74 con dato propio, 42 prestadas, 17 sin dato** (10 de
calzado y accesorios) **(corregido: era 71/48/12)**.

**09 · El hallazgo: 2026 está contaminado.** Desde 2025 Google cambió cómo mide: en 2026, 69 de 70 series suben a la vez,
mediana +99 %, y el trench coat, que picó siempre entre septiembre y febrero, pica en abril. Es la medición, no la moda.
Todo el análisis corta en 2024. Sin el ancla no lo hubiéramos visto.

**10 · Lo que no se pudo medir.** Calzado, dos intentos. Google Trends: de 8 estilos entran zapatillas y mocasines;
sandalias mide el verano (20,1 puntos dentro del año contra 11,6 entre años). CLIP sobre 14.000 looks: zapatillas 8 de
8, botas texanas 7 de 8, pero lee la ropa, no el zapato. Cinco estilos sin medición, en la app igual, con el motivo.

**11 · El rol de la IA.** CLIP (visión) · K-means (no supervisado, 17 atributos, k = 4, silhouette 0,32; los nombres de
los grupos los pusimos nosotros) · modelo de lenguaje (Groq, en vivo). EL MODELO DE LENGUAJE NUNCA VE UNA FILA DE DATOS.

**12 · Medido contra interpretado.** ● medido · ↪ prestado · punteado = interpretado. El color sólo para la señal:
▲ Entrar · ■ Esperar · ▼ Salir · ○ Sin dato directo, siempre con la palabra. Que algo gane o pierda terreno va en negro.

**13 · Demo en vivo.** Tendencias → la ficha y su recomendación → Diseñar → Preguntar con foto (guion de la demo aparte).

**14 · Límites declarados.** Google Trends no tiene datos antes de 2004. La pasarela no adelanta a escala anual:
correlación máxima sin rezago +0,43, +0,12 con dos años. No hay columna de género en Vogue ni en H&M, y no la simulamos.
**(corregido)** Seis de las doce fichas de Tendencias no están en el K-means: su etapa es la estimada sobre un catálogo
sintético. Ninguna recomienda con esa etapa: rayas y gamuza recomiendan por su serie de búsqueda, y las otras cuatro no
recomiendan.

**15 · Qué sigue.** Calcular la etapa desde las curvas para todos los atributos. La pasarela mes a mes, para volver a
probar si adelanta a una resolución más fina: es la única versión de la hipótesis que todavía no pudimos descartar.
