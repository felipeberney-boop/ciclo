# Plan del rediseño después de la Entrega 4 (24/11/2026)

Sale de `devolucion.md`. Orden de la cátedra: A → B+C → D → G → E → H → F → I → J. Cada fase cierra igual:

1. capturas antes y después a 1400 y 393 px (en `diseno/rediseno_2026-11-24/<fase>/`);
2. `node codigo/probar_demo.js` sin clave (y con la función de Netlify desde G);
3. entrada en `decisiones.md` que cita la devolución;
4. commit y push. Netlify, con el borrador y `restoreSiteDeploy` (CLAUDE.md), al cerrar cada fase que cambia lo que se ve.

Lo que se mantiene en todas (K): fotos de pasarela, logo, fondo blanco, la señal en verde/ámbar/rojo con su palabra.
Se ordena, no se borra.

---

## Qué se puede filtrar por proyecto (D) — revisado en los datos, antes de tocar nada

| Fuente | Público (mujer / hombre / sin género) | Tipo de marca | Categoría de prenda |
|---|---|---|---|
| Google Trends (65 series, 2004–2024) | **No.** Búsqueda mundial, sin género | **No** | Sí (cada serie es un atributo de un grupo) |
| Vogue Runway, serie de pasarela (`REC[].v`, 1,28 M looks) | **No.** La serie mezcla mujer y hombre | **No** (todo es pasarela de diseñador) | Sí |
| Vogue Runway, muestra CLIP (14.000 looks, 2010–2023) | Sólo *estimado*: el archivo dice «menswear» en parte de los looks. Sería una serie nueva, interpretada y chica; no la armo sin que lo decidas | No | Parcial (10 etiquetas) |
| Reddit | **Sí**: r/femalefashionadvice (`RDS`) y r/malefashionadvice (`RDH`), 2012–2025 | No | Sí |
| Lyst Index | No | Las marcas sí, pero el índice es casi todo lujo; no alcanza para «fast» | No |
| H&M (30,6 M compras, 2018–2020) | La tabla original trae sección (Ladieswear/Menswear) pero no está cargada en la app | Es fast fashion, una sola marca | Sí |
| Zara (feb-2024, 252 prendas) | No | Una sola marca, fast | Sí |

**Entonces:** en Mis ciclos, «Mujer» / «Hombre» cambia de verdad sólo la capa de Reddit (y la foto de cada tarjeta). La
búsqueda, la pasarela y el modelo son los mismos para todos, y la pantalla lo dice en una línea: «Google y Vogue no
separan por género: estas curvas son de todos». El **tipo de marca no filtra datos**: cambia la regla (Entrar / Esperar /
Salir, plazos, puntos del brief), y también se dice. Lo que sí filtra de verdad es la **categoría de prenda**. «Sin
género» muestra Reddit de los dos foros, por separado.

---

## Fases

### 0 · Hoy, antes del código
- `devolucion.md` (hecho), este plan y la **lámina del sistema** (escala tipográfica + paleta por rol) en
  `diseno/sistema_2026-11-24/`.

### A · Tipografía y paleta (primero: cambia todo)
- Bodoni Moda **sólo en el logo** (se carga sólo ese peso). Todo lo demás en `--sf`, a mano, sin revert (ya está hecho
  el paso a `--sf`; falta devolverle la Bodoni al logo).
- Escala fija: H1 · H2 · H3 · H4 · Párrafo · Etiqueta (MAYÚSCULAS con tracking) · Dato. Títulos 600/500, nunca 700+.
  Nada de texto bajo 16 px; etiquetas desde 12 px, también adentro de los gráficos.
- Link = azul y subrayado. Botón = se ve como botón (relleno azul el principal, borde el secundario). Paleta por rol:
  acción, info, señal, foto, ilustración. Documentado en CLAUDE.md.

### B + C · Home nuevo y menú
- Home sin preguntas: portada de pasarela con texto al costado (pruebo **una foto** y **una serie** y te muestro las dos).
  Secciones cortas: qué es · cómo funciona · de dónde salen los datos (fuente, período, cada cuánto se actualizaría) ·
  qué obtenés · **Crear tu proyecto** (nombre + email + las tres preguntas en una pantalla, una línea por respuesta
  con lo que cambia; se guarda en localStorage, declarado en Acerca de). «Sólo estoy mirando» → Explorar ciclos.
  Falta el link de la página que mostró Cristian (quedó «[PEGAR ACÁ…]»): sigo con la referencia de i-D hasta que lo pases.
- Menú: CICLO · Mis ciclos · Diseñar · Explorar ciclos · Preguntar · El brief · Acerca de. Sale «Más». Avatar con
  iniciales → Mis proyectos · Mi perfil · Salir / cambiar de proyecto. Sin proyecto, el avatar dice «Crear proyecto».
- El email sólo se guarda en tu navegador; no se manda a ningún lado (no hay servidor). Se dice al lado del campo.

### D · Mis ciclos (reemplaza a Tendencias)
- Arriba: NOMBRE DEL PROYECTO · Mujer · Para una marca · Fast fashion · Editar. Barra de búsqueda y filtro sticky.
  Selector **Gráfica | Tendencias** (los nombres del boceto).
- Gráficos: salen «en su máximo», «lo que vuelve», «uno contra otro». «Qué sube y qué baja» queda, más grande, Gana
  arriba y Pierde abajo, con la línea de qué es «+50». Nombres propuestos: **«Tu ciclo, 2022→2024»**, **«Lo que se
  mueve en tu proyecto»**, **«Gana y pierde terreno»**. «Cuándo picó» pasa a línea de tiempo con años y ficha en cada punto.
- Tarjetas: qué son en una línea y ordenadas Entrar → Esperar → Salir.

### G · Preguntar
- Netlify Function `netlify/functions/preguntar.js` que llama a Groq con `GROQ_API_KEY` (variable de entorno, nunca en
  el repo). GitHub Pages no corre funciones: desde ahí la app llama a la de Netlify. **Lo que tenés que configurar:**
  Netlify → Site configuration → Environment variables → `GROQ_API_KEY` = tu clave de console.groq.com, scope Functions.
  La clave propia en localStorage sigue como respaldo.
- Ejemplos de conversación visibles (pregunta + respuesta real, generada una vez y marcada con fecha y modelo; no
  simulada). Sale el aviso de tokens de arriba; queda la línea chica debajo de la caja.

### E · Explorar ciclos (reemplaza a El ciclo), sin filtro de proyecto
- Queda el selector y el gráfico de lo que tocás, y abajo sólo los tres gráficos de jeans (amplios, medios, ajustados).
  Sale el apilado por corte, el de color, el último y el texto extra.

### H · El brief
- Centrado, con veredicto y puntaje centrados. Sale «Tu look hasta ahora». Temporadas sólo en años con datos (hasta 2025).

### F · Ficha del atributo
- Tres líneas fijas: la etapa sale de un K-means (agrupa, no predice); lo punteado es el cono de cuánto se movió la
  historia en atributos parecidos; 100 = el máximo de ese término en su fuente.

### I · Acerca de
- Corto, en bloques, cada desplegable con «+» / «−» y su estado. Incluye qué se guarda en el navegador.

### J · Texto
- Releo cada línea; te paso la lista de lo que sale y lo que se reescribe en `entregas/entrega_4/texto_que_sale.md`.

## Lo que necesito de vos
- El link de la página que mostró Cristian.
- Configurar `GROQ_API_KEY` en Netlify cuando lleguemos a G.
- Decidir si querés la pasarela «estimada» por género con la muestra de CLIP (hoy: no).
