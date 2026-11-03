# Del diseño al código

**Entrega 3 · criterio 4 · 03/11/2026**

Archivo de Figma de esta entrega: **CICLO · Del diseño al código**, https://www.figma.com/design/4lvJEf2ZjBX87sXEySXqa7
Tiene tres páginas, una por etapa: el diseño original, la devolución de la cátedra y la referencia, y el sistema
implementado.

Lo primero, para que no haya malentendidos: **la app no se construyó leyendo un Figma.** Se escribió directamente en
código (un solo archivo, `app/index.html`) con Claude Code; 99 de los 101 commits que había al 03/11 lo firman. El
prototipo de Figma de la Entrega 2 y la app de ese mismo día ya eran distintos. Lo que cambió el aspecto de la app de
punta a punta fue una devolución de la cátedra con una referencia concreta, que adaptamos en el código. El camino
fue ese, y este documento lo cuenta así.

---

## Etapa 1 · El diseño original

*Página 1 del archivo de Figma.*

| Qué | Fecha | Dónde |
|---|---|---|
| Prototipo navegable: 10 pantallas a 1440×900 (82 conexiones) y las mismas 10 a 393×852 (63) | 05/10 (Entrega 2) | https://www.figma.com/design/zpHKE7YQLBRXJPcbyrb37I |
| Láminas de la Entrega 2 (la usuaria, la regla del salmón, los wireframes) | 05/10 | `diseno/prototipos/prototipo_entrega_2_laminas/`, presentadas en Figma Slides |
| Propuesta de Felipe: la portada de ese día y un rediseño | 13/10 | `diseno/prototipos/prototipo_felipe_1/` |
| Propuesta de Abril: radar, detalle y consulta, generadas con IA de imágenes, con datos ilustrativos | 13/10 | `diseno/prototipos/prototipo_abril_1/` |

El prototipo estaba en sans serif, con menú de pastillas, tarjetas blancas sobre crema y una caja salmón para lo que
decía la IA. La app de ese mismo día era una revista: Bodoni en los títulos, mono en mayúsculas espaciadas y menú de
texto subrayado. Compartían las diez vistas con los mismos nombres, el titular «Qué se está moviendo», el selector
Fast fashion / Premium / Nicho y la etapa como un punto sobre una pista. El registro no dice cuál se hizo primero.

## Etapa 2 · La devolución de la cátedra y la referencia

*Página 2 del archivo de Figma.*

**La devolución.** El 13/10, Cristian Reynaga marcó que la interfaz era confusa: «un mar de datos y gráficos». De ahí
salieron la entrada de tres preguntas y Diseñar. El 27/10, **Iván Fardjoume seguía viendo la interfaz «muy IA».**
Probamos tres variantes (revista, revista suave y estudio) y no convencieron: «No me gustaron. El profe sigue
diciendo que es muy IA» (Felipe, 27/10). De las tres sólo quedó guardada la revista
(`diseno/prototipos/versiones_de_la_app/app_2026-10-27_c639966_antes_de_apple.html`); las otras dos se probaron en la
conversación y no se guardaron.

**La referencia.** Iván nos pasó https://www.shadcn.io/blocks?page=2. En ese sitio está el DESIGN.md de Apple,
https://www.shadcn.io/design/apple: una versión no oficial del sistema de la web de Apple, con colores, tipografía,
radios, componentes y reglas («Action Blue #0066cc on every link and pill, SF Pro type, and light and dark tiles
stacked edge to edge»). Las capturas de las dos páginas están en `diseno/referencias/`.

**Lo que hicimos nosotros.** Con esa referencia, Felipe definió qué tenía que ser CICLO: «como si Apple vendiese ropa y
un software de hacer ropa encontrando tendencias, que es lo que es CICLO». Después elegimos qué tomar.

| Se tomó | Cómo quedó en CICLO |
|---|---|
| La tipografía del sistema | SF Pro en Mac e iPhone, Inter en el resto (el DESIGN.md sugiere ese mismo respaldo) |
| El lienzo gris perla | #f5f5f7 de fondo, siempre en claro (`data-theme="light"`) |
| Tarjetas blancas sin sombra | Radio de 18 px; al pasar el mouse nada se levanta |
| Títulos centrados | Semibold, apretados, con la bajada como tagline |
| Nada en mayúsculas espaciadas | El rótulo chico es gris, como un pie de foto |
| Píldoras y un encabezado fino | Translúcido, de una línea |
| Un bloque oscuro | #272729, para «qué gana y qué pierde terreno» |
| Un solo color de acción | El azul #0066cc, que en CICLO significa sólo «se puede tocar» |
| El producto como protagonista | La interfaz se corre y la prenda habla. Diseñar funciona como un configurador |

| No se tomó | Por qué |
|---|---|
| El logo y el nombre de Apple | Es su sistema, no su marca: CICLO no se presenta como algo de Apple |
| Su fotografía de producto | Las fotos de pasarela no tienen licencia, así que las prendas siguen dibujadas |
| Que el azul sea el único color | En CICLO el color ya tenía un significado: la señal (▲ Entrar verde, ■ Esperar ámbar, ▼ Salir rojo, siempre con su palabra). Se sumó el azul; no reemplazó a la señal |

## Etapa 3 · El sistema implementado

*Página 3 del archivo de Figma, generada desde `app/index.html` con el MCP de Figma.*

Esta página reconstruye en Figma la app como está hoy, leyendo el código: la «capa Apple» del CSS (27/10). Tiene:

- **Variables:** 16 colores y 3 radios, cada uno con su variable CSS y qué significa. Son el lienzo, la tarjeta, tres
  tintas, dos líneas, el azul y su foco, «interpretado», los cuatro de señal y el bloque oscuro.
- **Estilos de texto:** 24, con los tamaños y pesos reales del CSS. El título va a 64 px en escritorio y 39 px en el
  celular, la bajada a 21 px y el cuerpo a 17 px.
- **Componentes:**
  - la tarjeta de opción de Diseñar, en 4 señales × 4 estados;
  - la tarjeta de Tendencias, con 2 dibujos × 5 etapas;
  - la fila del bloque oscuro, el filtro, el paso de Diseñar, el chip del recorrido y la fila del chat;
  - la ficha de silueta, el encabezado a 1400 y 393, el botón «Diseñar con este…» y las 7 siluetas de la app como
    vectores.
- **Pantallas:** Tendencias, Diseñar y Preguntar, a 1400 y a 393 px, armadas con esos componentes y con los datos
  reales. La respuesta del chat es una respuesta real de la prueba del 27/10.

Qué se leyó con un agente y qué no:

| | ¿Con un agente? | Cómo |
|---|---|---|
| Construir la app | Sí, sin leer un Figma | Claude Code en el repositorio, a partir de lo que pedía Felipe y de la referencia |
| Los valores de la capa Apple | Sí, desde la referencia | Los valores del DESIGN.md (#f5f5f7, #0066cc, #0071e3, #272729, 18 px, 17 px), escritos como variables CSS |
| Las páginas 1 y 2 del Figma | En parte | El MCP de Figma leyó el prototipo de la Entrega 2 (`get_metadata`, `get_screenshot`) y subió las capturas y las láminas |
| La página 3 del Figma | Sí, del código al diseño | El MCP de Figma (`use_figma`) armó variables, estilos, componentes y pantallas a partir de los valores leídos en `app/index.html` y de capturas de la app con Playwright |

**Una diferencia entre el Figma y la app.** En Figma el texto va en Inter, porque SF Pro es una fuente local de Apple
y no se vería en otras computadoras. Es la misma fuente que la app usa fuera de Apple.

---

## Lo que se decidió en el código y no en Figma

Ningún Figma de este proyecto dibujó estos casos. Todos se decidieron al escribir la app, que es donde aparecieron.

### Los cuatro estados de lo que se toca

| Estado | Cómo se ve | Por qué |
|---|---|---|
| Reposo | Tarjeta blanca sobre gris perla, sin borde ni sombra | La interfaz se corre para que hablen las prendas |
| Hover | Aparece un borde gris (#e0e0e0); nada se levanta | La capa Apple sacó la sombra y el levantado que había puesto la capa de uso ese mismo día |
| Foco visible | Contorno azul de 2 px (#0071e3), separado 2 px, sólo con teclado (`:focus-visible`) | Se ve navegando con teclado y no aparece al hacer clic |
| Elegido | Borde azul de 2 px (#0066cc) y `aria-pressed="true"` | El azul es «se puede tocar / está elegido»; un filtro elegido va en negro porque filtra, no actúa |

En la página 3 del Figma están los cuatro estados de la tarjeta de opción, cruzados con las cuatro señales.

### El celular, a 393 px

- **Qué se reordena:** la navegación. El Figma tenía cinco pestañas abajo, y con once vistas escondían la mitad.
  Ahora hay un botón «Menú» que abre todas las vistas; las secundarias van como tarjetas con un dato y su fuente.
- **Qué se pliega:** El ciclo pasó de 22.000 a 10.200 px. Muestra doce tarjetas y «Ver los 65 atributos»; la lista
  repetida queda en «Ver otro atributo». Método va en acordeón.
- **Los gráficos se deslizan:** conservan un ancho donde ningún rótulo baja de unos 9 px, y se mueven de costado
  dentro de su caja con el aviso «Deslizá el gráfico →». Antes se achicaban hasta rótulos de 3 a 7 px.
- **Diseñar:** los pasos van en una fila que se desliza, con el paso actual centrado, y las opciones en dos columnas.
- Verificado con Playwright: el ancho de la página es el del teléfono, sin scroll horizontal (de nuevo el 03/11).

### La carga de CLIP

Buscar por imagen usa el modelo CLIP (89 MB) y un índice de 14.000 looks (8 MB). **No se baja nada al abrir la app**:
al abrir hay 3 pedidos y 266 KB (medido el 03/11). El índice baja con la primera consulta y el modelo, sólo con una
foto propia. La pantalla lo avisa antes («La primera consulta baja el modelo CLIP (89 MB) y el índice (8 MB)») y
durante la carga muestra el avance («Bajando el modelo CLIP: 34 de 89 MB…»). Después queda guardado en el navegador.
Con los looks de ejemplo sólo se baja el índice.

### Los casos de error

| Caso | Qué hace la app |
|---|---|
| Sin clave de Groq | No llama a nada: abre «Activar el chat» y dice «Primero activá el chat: son tres pasos, en "Activar el chat". Lo hacés una sola vez.» |
| Clave mal pegada (401) | «Groq rechazó la API key. Revisá que esté completa y sin espacios.» |
| Límite del plan gratis (429) | «Llegaste al límite del plan gratis de Groq (8.000 tokens por minuto). Esperá un minuto…» |
| Sin conexión | «No hubo conexión con api.groq.com. Revisá internet o si un bloqueador impide ese dominio.» |
| CLIP no reconoce nada | Si ningún atributo pasa 0,35 de probabilidad: «No determinado», y los tres más cercanos «para orientar, no como respuesta» |
| El archivo no es una imagen | «Ese archivo no es una imagen.» |
| Atributo sin serie medida | Toma la de un pariente y lo dice («↪ prestado», con el motivo); si no hay pariente, queda neutro con «○ Sin dato directo», nunca en rojo |
| Recomendación sin evidencia | Si no puede decir de dónde sale cada número, pone «Sin recomendación» |

Sin clave, con una clave inválida y sin conexión, cada caso se probó el 03/11 contra la app publicada.

### La regla de color, ampliada

Hasta el 27/10 el único color de la interfaz era la señal. Desde la capa Apple hay uno más: **el azul, que significa
«se puede tocar»** (botones de acción, links, lo elegido). Verde, ámbar y rojo siguen siendo sólo la señal, siempre
con su palabra y su ícono, para que se lea en blanco y negro y por quien no distingue rojo de verde. Que algo gane o
pierda terreno es un dato y va en tinta, no en el color de la señal. La procedencia (`● medido`, `◇ interpretado` con
borde punteado, `↪ prestado`) va en texto y trazo, nunca en color.

### El modo oscuro

La app lo tuvo desde el principio, siguiendo la preferencia del sistema; la auditoría del 26/10 lo corrigió. El 27/10
**se apagó**: `<html data-theme="light">`. El lienzo gris perla y las tarjetas blancas son la identidad de la capa
nueva, y mantener dos temas duplicaba cada revisión. El CSS del oscuro sigue en el archivo, desactivado.

---

## Las diferencias entre el prototipo y la app de hoy

Prototipo de la Entrega 2 a la izquierda, app del 03/11 a la derecha.

### La entrada por perfil

![Figma: portada. App: tres preguntas](figma_a_codigo/par_portada.png)

El prototipo abría en una portada con dos listas. La app abre en tres preguntas: para quién diseñás, si trabajás
para una marca o por tu cuenta, y la categoría. **La provocó** la devolución de Cristian del 13/10: un mar de datos, y
separar el vínculo laboral, porque cambia el riesgo. Donde a una marca le conviene «Esperar», a quien trabaja por su
cuenta le conviene «Explorar». La portada vieja salió el 26/10: era un menú escrito a mano, sin calzado y sin salida.

### Tendencias como pantalla principal

![Figma: radar. App: Tendencias](figma_a_codigo/par_radar.png)

El Radar del prototipo tenía ocho fichas y búsqueda «2004–2025». Tendencias abre con el bloque oscuro «Qué gana y qué
pierde terreno afuera», medido de 2022 a 2024, y las doce fichas. **Lo provocaron** tres cosas:
- las cifras grandes salieron el 13/10 porque no ayudaban a decidir;
- el corte en 2024 entró el 20/10, porque los datos de 2025 y 2026 de Google Trends vienen con un cambio de medición;
- el 26/10 decidimos que lo principal de CICLO es ver qué se mueve.

### El semáforo, y el salto de Tendencias a Diseñar

![Figma: detalle con la caja salmón. App: ficha con su procedencia y el botón a Diseñar](figma_a_codigo/par_detalle.png)

En el prototipo, la recomendación iba en una caja salmón, el color de la IA. En la app, la acción va en semáforo con
su palabra, y lo interpretado se marca con borde punteado. **Lo provocó** un problema del 20/10: «Entrar» salía en
rojo, porque el salmón y su terracota competían con la acción. El botón azul «Diseñar con este corte · Baggy →» no
estaba en Figma, porque Diseñar no existía todavía. Desde el 27/10, cada ficha de Tendencias entra a Diseñar con el
atributo fijo y pregunta sólo lo que falta.

### Los nombres de taller

El prototipo decía «Jeans amplios», «Tejidos», «Materiales». La app dice baggy, wide leg, barrel, o «Frisa · french
terry · Punto afelpado por dentro, la tela del buzo». **Lo provocó** la regla del 20/10: si un diseñador no puede
decir el nombre en voz alta en un taller y que le entiendan, no va en la interfaz.

### El pivot visual completo

Del prototipo en sans serif y crema (05/10) se pasó a la app en revista con Bodoni (hasta el 27/10) y de ahí a la capa
Apple. **La provocó** la devolución de Iván y la referencia que pasó (etapa 2). Sin buscarlo, la app de hoy quedó más
cerca del prototipo que la revista: sans serif, pastillas y tarjetas blancas.

### El celular

![Figma: radar a 393 px con pestañas. App: Tendencias a 393 px y el menú abierto](figma_a_codigo/par_celular.png)

Cinco pestañas no alcanzaban para once vistas: el menú entero (ver «El celular, a 393 px»).

---

## Archivos

- `figma_a_codigo/par_*.png`: los pares, con el prototipo a la izquierda y la app a la derecha.
- `figma_a_codigo/figma_*.png`: el prototipo de la Entrega 2, bajado con el MCP de Figma el 03/11.
- `figma_a_codigo/app_*.png`: la app el 03/11, con Playwright a 1440×900 y 393×852; `app_revista_antes_de_apple.png`
  es la revista del 27/10.
- `diseno/referencias/shadcn_*.png`: la referencia que pasó Iván.
- Cada versión anterior de la app está en `diseno/prototipos/versiones_de_la_app/`, con fecha y commit.
