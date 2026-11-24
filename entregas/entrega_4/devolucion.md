# Devolución de la Entrega 4

Nota: **6/10** (Hipótesis 6, Datos 5, IA 5, Diseño 6, Comunicación 6). Devolución escrita, anotaciones a mano sobre las
pantallas y lo que pidieron en clase Cristian e Iván (24/11/2026). Copiado tal cual lo pasó Felipe.

=== 1. DEVOLUCIÓN ESCRITA (Entrega 4) ===
- Exceso de información sin recorrido claro: el usuario no sabe en qué punto está ni qué ramificaciones tiene para ir
  y volver. Desarmar cada pantalla, elegir lo más importante, ordenarlo y sacar lo secundario que no suma.
- El home tiene que narrar de dónde sale la información, qué período cubre y qué se puede obtener.
- Diferenciar el uso con y sin logueo. Las tres preguntas sin contexto no arman expectativas; si no ramifican, que
  vayan en una sola pantalla. Con el carrusel de fotos el problema sigue.
- «Qué se está moviendo»: demasiados niveles de información. Un gráfico por vez, con un texto con su conclusión.
  ¿Qué unidad tiene el eje vertical? ¿Qué misión cumple la pantalla? ¿Qué período y qué alcance? ¿Qué son las 8
  tarjetas? Ordenarlas por entrar / esperar / salir.
- El botón «ojo para Chanel» no tiene que verse como link: jerarquizarlo o reubicarlo.
- No se explica cómo se construye el máximo (en Vogue, ¿qué es llegar a 100?). ¿Cada cuánto se actualizan los datos?
- En «Preguntale» no funciona la IA.
- Legibilidad: tamaños muy chicos y fuentes con muy poco cuerpo.

=== 2. ANOTACIONES A MANO DE LOS PROFES SOBRE LAS PANTALLAS ===
- Entrada: «No se entiende el camino». «¿Para qué género?» (no se entiende para qué sirve la pregunta).
- Pidieron un sistema: Paleta por rol (acción / info / foto / ilustración) y Tipografías como escala
  (Heading 1, 2, 3, 4, párrafo), cada estilo con un significado y una acción distintos.
- Tendencias: «Mi perfil» → mis proyectos / mi perfil / salir.
- Ficha de Rayas: «¿Qué algoritmo usan para predecir?» → tiene que quedar claro, en la pantalla, que no predice:
  la etapa sale del K-means y la parte punteada es el cono de lo que se movió la historia.
- Preguntar: «¡Faltan ejemplos de conversación!»
- Boceto de Mis ciclos: arriba dos modos, «Herramienta» (Mis ciclos) y «Explorar»; adentro de Mis ciclos, una barra
  de búsqueda y filtro sticky y un selector «Estadística | Tendencias»; desde los dos se entra a un atributo (Rayas).

=== 3. LO QUE PIDIERON EN CLASE ===

A · TIPOGRAFÍA Y JERARQUÍA (primero, porque cambia todo)
- La Bodoni queda SOLO en el logo CICLO. Todo lo demás vuelve a SF Pro (--sf, la de antes del 17/11; el último commit
  sin Bodoni es fb5baa4). Hacelo a mano, sin git revert.
- Más funcional: tamaños más grandes (texto ≥ 16 px, etiquetas ≥ 12 px), títulos en medium o semibold, NO bold pesado.
- Escala fija H1 / H2 / H3 / H4 / párrafo / etiqueta, documentada. Lo importante en etiquetas MAYÚSCULAS con tracking.
- Todo lo que es link va en color de link y subrayado; un botón se ve como botón. Paleta por rol: acción, info, señal
  (entrar/esperar/salir), foto, ilustración. Documentá el sistema en CLAUDE.md.

B · HOME NUEVO (lo más importante)
- Al entrar no hay preguntas. Una foto o una serie de fotos de pasarela (probá las dos y mostrámelas) que digan
  «herramienta de moda», con un texto al costado sobre qué es CICLO (referencia: i-D).
- Scroll de pocas secciones, cortas, como [PEGAR ACÁ EL LINK DE LA PÁGINA QUE MOSTRÓ CRISTIAN]: qué es CICLO, cómo
  funciona, de dónde salen los datos (Vogue Runway, Google Trends, Reddit, Lyst, H&M…), qué período cubre cada uno,
  cada cuánto se actualizaría y qué obtenés.
- Al final, «Crear tu proyecto»: nombre del proyecto + email + las tres preguntas (público, para una marca / por mi
  cuenta, tipo de marca), TODO EN UNA SOLA PANTALLA, con una línea que diga qué cambia cada respuesta (por ejemplo,
  para qué sirve el género). Se guarda en el navegador (localStorage, sin servidor; declararlo en Acerca de).
- «Sólo estoy mirando» como link subrayado: entra a Explorar ciclos sin proyecto. Que se note qué tiene uno y otro
  modo (con y sin logueo).

C · MENÚ
- CICLO (logo) · Mis ciclos · Diseñar · Explorar ciclos · Preguntar · El brief · Acerca de (al final). Sale «Más».
- «Cambiar perfil» pasa a ser un avatar con iniciales (Felipe Berney → FB; un solo nombre → una letra). Al tocarlo:
  Mis proyectos · Mi perfil · Salir / cambiar de proyecto. Siempre se ve que estás logueado.

D · MIS CICLOS (reemplaza a Tendencias, es la HERRAMIENTA)
- Todo filtrado por el proyecto: tarjetas Y gráficos con los datos de tu público, tipo de marca y categoría. Revisá
  qué se puede filtrar de verdad (Reddit hombres/mujeres sí; Vogue y Trends no traen género) y decímelo antes; lo que
  no se pueda filtrar, decirlo en la pantalla, nunca simularlo.
- Arriba, en vez de «Tu perfil»: el NOMBRE DEL PROYECTO · Mujer · Para una marca · Fast fashion · Editar.
- Barra de búsqueda y filtro sticky; selector Estadística | Tendencias, como en el boceto.
- Gráficos: salen «Qué está en su máximo», «Lo que vuelve» y «Uno contra otro».
  · «Qué sube y qué baja» queda, con otro nombre propio de tus ciclos (proponeme 3): GANA TERRENO arriba y PIERDE
    TERRENO abajo, uno debajo del otro, más grandes. Explicar en una línea qué son los puntos (ej. «+50»): índice de
    Google Trends 0–100 (100 = el máximo de ese término), diferencia 2022→2024.
  · «Cuándo picó cada uno» pasa a ser una LÍNEA DE TIEMPO de verdad, con años en el eje. Al pasar por cualquier punto
    (también los naranjas) aparece la ficha: de dónde viene, cómo se procesó, qué sacamos.
  · Cada gráfico con su conclusión escrita en una frase.
- Tarjetas: decir qué son y ordenarlas por Entrar / Esperar / Salir.

E · EXPLORAR CICLOS (reemplaza a El ciclo, la parte INFORMATIVA)
- Todo, SIN el filtro del proyecto.
- Queda: el selector y el gráfico de lo que clickeás, y abajo SOLO los tres gráficos separados de jeans (amplios,
  medios, ajustados), uno cada uno.
- Sale: el gráfico apilado de jeans por corte, el de color, el último gráfico y toda la información extra.

F · FICHA DEL ATRIBUTO (Rayas)
- Que quede claro que no predice: qué es la etapa (K-means), qué es lo punteado (cono), qué es 100 en el eje.

G · PREGUNTAR
- Que la IA funcione sin pegar una clave: Netlify Function con GROQ_API_KEY como variable de entorno (nunca en el
  repo). Decime qué tengo que configurar en Netlify.
- Ejemplos de conversación visibles (pregunta + respuesta), no solo botones.
- Sale lo de los tokens de arriba (los 8.000 por minuto). Queda sólo la línea chica debajo de la caja.

H · EL BRIEF
- Centrado como antes, el veredicto y el puntaje también.
- Sale «Tu look hasta ahora».
- Sin temporadas 2028: solo años que cubren los datos.

I · ACERCA DE
- Rediseñarlo entero: organizado, corto, y que lo que se despliega se vea desplegable (flecha o +, estado abierto o
  cerrado).

J · TEXTO (en toda la app)
- Sacar todo el texto de relleno escrito por IA. Releé cada línea: si no explica un dato ni ayuda a decidir, sale.
  Ejemplo de lo que no tiene sentido: «la búsqueda de 2023–24 sobre su punto más alto de 2004». Pasame la lista de lo
  que sacás y lo que reescribís.

ORDEN SUGERIDO: A → B+C → D → G → E → H → F → I → J. Arrancá por el plan y por la escala tipográfica y la paleta
(mostrame una lámina con el sistema antes de aplicarlo).

K · EXTRA
- La devolución escrita también dice: «hay buenas posibilidades para robustecer las decisiones que tomaron de forma
  acertada sobre el estilo gráfico y sostener la impronta estética». O sea: la identidad de moda (fotos de pasarela,
  logo, blanco) se mantiene; se ordena, no se borra.
- En el boceto, Mis ciclos abre a dos vistas: «Gráfica» y «Tendencias». Usá esos nombres si no proponés uno mejor.
