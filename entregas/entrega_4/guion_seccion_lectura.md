# Lectura · guion de la pantalla (antes de construir)

16/11/2026. Reemplaza a Tiza (layout A+B, 10/11). Un solo hilo, a lo ancho; todo pasa adentro de la conversación.

## La regla

Lo que estás mirando es el hilo. No hay mesa, ni panel fijo, ni zona de carga. Cada respuesta trae adentro lo suyo
(chips, curva, fotos, recorrido de marca, texto) y queda donde está: si scrolleás para arriba, la lectura de tu imagen
sigue ahí, entera. Columna de 760 px centrada en escritorio; en el celular, la misma columna a todo el ancho.

## 1 · Vacía

```
 CICLO   Tendencias · Diseñar · El ciclo · [Lectura] · Más
 ────────────────────────────────────────────────────────────────────────

                 Lectura
                 Preguntale a CICLO por un atributo, una marca o un
                 diseño tuyo. Te contesta con los datos que tiene.

                 ┌──────────────────────────┐ ┌──────────────────────┐
                 │ ¿Qué está subiendo más   │ │ ¿Cómo está Prada?    │
                 │ ahora?                   │ │                      │
                 └──────────────────────────┘ └──────────────────────┘
                 ┌──────────────────────────┐ ┌──────────────────────┐
                 │ ¿Cómo está Zara?         │ │ ¿Qué material le va  │
                 │                          │ │ a un jean baggy?     │
                 └──────────────────────────┘ └──────────────────────┘
                 ┌─────────────────────────────────────────────────────┐
                 │ ▢ Probá con un look de ejemplo   [foto][foto][foto] │
                 └─────────────────────────────────────────────────────┘





                 ┌─────────────────────────────────────────────────────┐
                 │ Preguntá algo…                                 ＋  ↑ │
                 └─────────────────────────────────────────────────────┘
                 Respuesta escrita: activar (1 min) · también podés soltar
                 una imagen en cualquier parte
```

- Una línea de qué hace; nada de «subí una imagen» como instrucción principal. La imagen aparece recién en la letra chica
  del pie y en el ＋ del campo.
- Las cuatro sugerencias de texto son las de `TZ_SUG`. «Mostrame qué se parece a esto» se va: sin imagen no tiene sentido
  como primera opción. En su lugar, tres looks de ejemplo (los de `rvEjemplo`) que se mandan con un clic, como si los
  hubieras soltado: es la forma de probar la imagen sin tener una.
- El campo queda fijo al pie (sticky), como en cualquier chat. Es lo único fijo de la pantalla.
- Si hay un diseño armado en Diseñar, una quinta sugerencia: «Leé mi diseño: wide leg · lino · rayas».

## 2 · Arrastrás una imagen (en cualquier parte de la pantalla)

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │                                                                     │
 │                  Soltala y CICLO la lee                             │
 │                  (la foto no sale de tu computadora)                │
 │                                                                     │
 └─────────────────────────────────────────────────────────────────────┘
```

Velo sobre toda la ventana, como ahora. Funciona desde cualquier vista: si soltás en Tendencias, te lleva a Lectura con
la imagen ya mandada.

## 3 · La soltaste: tu mensaje y la respuesta

```
                                              ┌─────────────────────┐
                                     tu       │                     │
                                   mensaje →  │    (tu imagen,      │
                                              │     grande, como    │
                                              │     la mandaste)    │
                                              │                     │
                                              └─────────────────────┘
                                                 + texto si escribiste algo

 ┌─ CICLO ────────────────────────────────────────────────────────────┐
 │ Leyendo la imagen… (CLIP, en tu navegador)          ← primero esto │
 └────────────────────────────────────────────────────────────────────┘
                          ↓ y en 2-4 segundos se convierte en:
 ┌─ CICLO ────────────────────────────────────────────────────────────┐
 │ LO QUE LEYÓ   ◇ interpretado · tocá para corregir                  │
 │ (wide leg ●Entrar ×) (lino ■Esperar ×) (rayas ▼Salir ×) (+ agregar)│
 │ color: arena ◇ 0,71                                                │
 │                                                                    │
 │ LA CURVA QUE IMPORTA  ● medido · Google Trends, corregida, ≤2024   │
 │  wide leg  ▁▂▃▄▅▆▇  ▲ Gana presencia                     Entrar    │
 │  [ver las otras dos ▾]                                             │
 │                                                                    │
 │ SE PARECE A   [foto Vogue][foto Vogue][foto Vogue]  créditos       │
 │                                                                    │
 │ LA DEVOLUCIÓN                                                      │
 │  El corte está entrando; el lino espera; las rayas ya bajan.       │
 │  Sostené el wide leg y cambiá el estampado.                        │
 │  ◇ interpretación · Groq (gpt-oss-120b)   o   ⚙ armada con reglas  │
 │  ▸ Qué se le mandó al modelo                                       │
 └────────────────────────────────────────────────────────────────────┘
```

Orden adentro de la burbuja, siempre el mismo: **lo que leyó → la curva → se parece a → la devolución**. Los tres
primeros son instantáneos y no necesitan clave; la devolución llega después (con clave, en streaming o con «Pensando…»;
sin clave, la de reglas, con su etiqueta).

- **La curva que importa:** una sola, grande: la del chip con señal más fuerte (la que más se mueve). Las otras, plegadas.
  Así la burbuja no se vuelve un tablero.
- **Corregir un chip** (× o + agregar) no crea un mensaje nuevo: rehace la misma burbuja en su lugar (curva, parecidos y
  devolución) y deja una línea chica «corregido: sin rayas, con cuadros». La conversación no se ensucia.
- Medido contra interpretado: cada bloque tiene su marca (● medido / ◇ interpretado / ↪ prestado), como hoy.

## 4 · Escribís sin imagen

```
                                           ┌────────────────────────┐
                                           │ ¿Cómo está Prada?      │ ← tu mensaje
                                           └────────────────────────┘
 ┌─ CICLO ────────────────────────────────────────────────────────────┐
 │ Prada sube en Lyst desde Q3-25: 4 de los últimos 5 trimestres      │
 │ arriba del promedio.                                               │
 │                                                                    │
 │ PRADA EN LYST  ● medido · ranking trimestral                       │
 │  Q1-23 ─────────╮            ┆ Q1-26 ──╮                           │
 │   (tramo 1)      ╰──         ┆ (tramo 2, otra fórmula: no se unen) │
 │                                                                    │
 │ ▸ El detalle                                                       │
 │ ◇ interpretación · Groq     ▸ Qué se le mandó al modelo            │
 └────────────────────────────────────────────────────────────────────┘
```

- La respuesta es la del prompt v9 (conclusión → número que la sostiene → detalle plegado); la pieza de datos (el
  recorrido en Lyst con los dos tramos separados, la curva de un atributo con su foto, el catálogo de Zara feb-2024) va
  **entre la conclusión y el detalle**, porque es el número que la sostiene.
- Qué pieza se muestra lo decide la pregunta (lo que hoy hace `tzMesaDe`), y si la respuesta del modelo nombra otro
  atributo, se suma su curva chica al pie de la burbuja (lo que hoy hace «la mesa sigue a la respuesta»).
- «¿Qué está subiendo más ahora?» trae las tres fotos de lo que más sube con sus curvas: lo que hoy es la mesa vacía,
  ahora como respuesta.

## 5 · Sin clave de Groq

La burbuja se arma igual con todo lo medido; donde iría el texto:

```
 │ Lo que CICLO tiene sobre esto está arriba. Para que además te lo   │
 │ escriba, activá la respuesta escrita: [Activar · 1 minuto]         │
```

Con una imagen, la devolución de reglas ocupa ese lugar y dice «armada con reglas, sin modelo de lenguaje». Si la clave
es inválida o Groq no responde: «Groq no respondió (clave inválida / sin conexión). Lo medido de arriba sigue valiendo.»
Nunca una burbuja vacía ni un error solo.

## 6 · Celular (393 px)

```
 ┌───────────────────────────┐
 │ CICLO            ☰        │
 │                           │
 │ Lectura                   │
 │ Preguntale a CICLO…       │
 │ [¿Qué está subiendo…?]    │
 │ [¿Cómo está Prada?]       │
 │ [¿Cómo está Zara?]        │
 │ [¿Qué material…baggy?]    │
 │ [look][look][look]        │
 │                           │
 │ ┌───────────────────────┐ │
 │ │ Preguntá algo…   ＋  ↑│ │ ← sticky al pie
 │ └───────────────────────┘ │
 └───────────────────────────┘
```

Lo mismo en una columna. La imagen se sube con ＋ (en el celular no hay arrastrar). Las fotos de «se parece a» pasan a
un carrusel horizontal de tres.

## Lo que no cambia

Prompt v9; Lyst por tramo sin cruzar Q1-26; chips corregibles de CLIP; ● medido / ◇ interpretado / ↪ prestado; «Qué se
le mandó al modelo»; respuesta corta; la clave sólo en el navegador. Los links viejos (`#tiza`, `#consulta`,
`#asistente`, `#revision`) abren Lectura.

## Lo que se renombra

«Tiza» → «Lectura» en la navegación, títulos, textos, Método, readme, racional (md y PDF) y CLAUDE.md. La vista pasa a
`#v-lectura` (`#lectura`). Ojo con dos choques de nombre que ya existen y conviene resolver:

1. **Método abre con «Cómo se arma una lectura»** (`pintarLectura()`), que explica una tarjeta de Tendencias. Propuesta:
   pasa a «Cómo se arma una señal», que es lo que explica.
2. **El botón «Pedir lectura en vivo»** (detalle de un atributo) es justamente el que da el nombre. Se queda así: ahora
   apunta a lo mismo que la sección.

## Lo que se borra

La mesa (`#tzmesa`, `tzPintarMesa`, `tzVerMesa`, «Ver en la mesa», «Achicar la mesa»), el velo que manda a la mesa y el
layout de dos columnas. Las funciones que arman las piezas (`tzLyst`, `tzFotos`, `rvCurvas`, `rvPintarLectura`) se
reusan adentro de la burbuja.
