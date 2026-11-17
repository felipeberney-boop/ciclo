# Preguntale a CICLO · tres propuestas con la dirección de 032c (17/11/2026)

**Quedó la A**, aplicada también a El ciclo y a la entrada (ver `decisiones.md`, 17/11, «Impronta: queda la A»).

La devolución de la Entrega 4: el diseño es blanco y con poca cosa, sin identidad propia. La dirección: la gramática de
maquetado de 032c (escala y recorte: el gráfico a sangre, bordes duros, etiquetas chicas en mayúsculas contra una
imagen enorme) y, como imagen, **nuestros gráficos**, no fotos. El sistema de color no se toca.

Lo común a las tres: fondo blanco, cero esquinas redondeadas y cero sombras en esta pantalla, el título como etiqueta
chica, el campo de escribir como una barra a todo el ancho con un filo negro arriba, y la respuesta sin tarjeta (el
texto en una columna de 760 px, el gráfico de borde a borde). La respuesta es igual en las tres
(`respuesta_prada_*.png`).

| | Qué es lo primero que se ve | A favor | En contra |
|---|---|---|---|
| **A · Portada** | El gráfico que rota en Tendencias, a sangre; debajo, las preguntas como un índice con filetes | Reusa tal cual lo mejor que tiene la app; tocar una curva pregunta por ella | Repite el arranque de Tendencias |
| **B · Índice** | Cada pregunta sugerida es una banda con su gráfico: la respuesta antes de preguntar | Cada sugerencia se entiende sin tocarla; los gráficos se dibujan al entrar en pantalla | Es la más larga; en el celular hay que bajar para ver la segunda |
| **C · Hoja de contacto** | Todos los atributos con serie, cada uno con su curva 2010–2024, en una grilla ordenada por lo que más ganó | La más 032c; se ve todo de un golpe y cada celda es una pregunta | Es un formato nuevo (curvas chicas), no un gráfico de Tendencias agrandado |

Archivos: `a_1400.png`, `a_393.png`, `a_1400_entera.png` (y lo mismo para b y c). Se renderizaron con Playwright
sobre una copia de la app con `fuente/build.py` (lee `app/index.html`, le inyecta `comun.css` más el CSS y el JS de
cada propuesta y escribe `prop_a.html`… al lado de la app). La app publicada no cambió.
