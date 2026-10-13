# Prototipo Felipe 1

Carpeta de trabajo de Felipe Berney.

## ejemplo_01_portada.png

La portada actual de la web (`app/index.html`), renderizada a 1440×1440. Es la base de la que parte la
propuesta.

## propuesta_01_portada_v2.png · portada_v2.html

Rediseño de la portada, inspirado en la actual. El HTML es la fuente: se abre en el navegador a 1440 px.

Qué cambia respecto de la actual:

- **La portada ya muestra el dato.** En lugar de dos índices de texto, el panel «El ciclo hoy» pone los
  18 atributos sobre la curva de vida, en la etapa que les asignó el K-means. La etapa sigue siendo
  posición, no color: el color de cada punto es el de la prenda.
- **Lo emergente aparece rayado y vacío**, con la nota «sin datos después de 2023». El límite se ve en
  la portada en vez de quedar solo en Método.
- **Búsqueda y consulta por imagen en el primer pliegue.** «Subir una prenda» va en salmón porque es IA-6.
- **Fila de números con su fuente** debajo de cada uno: ningún número sin fuente.
- **Tres fichas de ejemplo** (jeans amplios, ajustados, lunares) con la pista de cinco etapas y las series
  reales de búsqueda y pasarela 2004–2025, tomadas de `datasets_procesados/`.
- **La lectura de la IA en su propio bloque salmón**, marcada como interpretación y atada al cliente
  elegido arriba. El texto de esa lectura es de ejemplo, no salida real del modelo.
- **Fondo claro** (`--paper`) en lugar del negro de la portada actual, para que los colores de las prendas
  se lean como color.
- **Límites declarados** en una franja al pie.

Fuentes, paleta y tokens son los de la app (Bodoni Moda, Archivo, IBM Plex Mono).
