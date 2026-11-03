# Preguntas probables · Entrega 3

Dieciséis preguntas que es probable que salgan, cada una con una respuesta corta y el número que la sostiene. Cada cifra
está en el repo; entre paréntesis, dónde.

---

**1 · ¿Por qué cortan en 2024?**
Porque desde 2025 Google cambió cómo mide. En 2026, 69 de 70 series suben a la vez (mediana +99 %), y el trench coat,
que siempre picó entre octubre y diciembre, pica en abril. Es la medición, no la moda. 2025 se dibuja apagado y 2026
se excluye (`decisiones.md`, 20/10; lámina «El trench pica en abril»).

**2 · ¿Cómo saben que el K-means está bien?**
De dos maneras. Por dentro: la silhouette con k = 4 es 0,32. Con k = 2 da más (0,36), pero dos grupos sólo dicen
«sube o baja». Por fuera, contra Reddit, que el modelo no ve: los tres que pone en ascenso o pico son los tres que más
crecen de 14, con p = 0,0013 y el criterio commiteado antes de calcular. Lo que no logra es distinguir «en retorno» de
«saturada» (p = 0,88), y eso también se dice.

**3 · ¿Qué le mandan exactamente al modelo?**
El system prompt (`prompts/prompt_asistente_v5.md`), el perfil, el diseño que se está armando, lo que CLIP leyó en la
imagen y las opciones válidas para cada paso. Además, de `ciclo_datos.md` va lo general y sólo las fichas que nombra
la pregunta: entre 3.600 y 4.600 tokens. Son métricas ya calculadas («61 % de su pico, momento −7 %»), nunca una fila.

**4 · ¿Cómo evitan que el LLM invente?**
Con cuatro barreras. No ve filas, sólo métricas. El prompt le exige que cada número esté en DATOS tal cual. La acción
(Entrar, Esperar, Salir) no la decide el modelo: la calcula la página con la regla fija y avisa si el modelo se aparta.
Y cada respuesta trae «datos», con el número que usó y de dónde sale, para chequearlo. En la prueba de seis preguntas
reales, ninguna inventó un número (`datasets/pruebas/asistente_v5_respuestas.md`).

**5 · ¿Por qué no hay calzado?**
Hay poco, y se intentó dos veces. En Google Trends, de 8 estilos entran zapatillas y mocasines; sandalias mide el
verano y el resto es ruido. Con CLIP sobre la pasarela, acierta zapatillas (8 de 8) y botas texanas (7 de 8), pero
adivina el zapato por la ropa. Cinco estilos no los mide nada: están en la app con el motivo y sin recomendación. Por
eso el K-means es de 17 atributos sin calzado.

**6 · ¿Cómo validaron que esto sirve?**
La lectura, contra fuentes que el modelo no vio: Reddit, con una prueba formal (p = 0,0013), y Lyst y Amazon en casos.
El chat, con seis preguntas reales: la v4 no pasó y la v5 sí. La interfaz, con las devoluciones del profesor y una
auditoría con Playwright de cada vista a 1400 y 393 px. Lo que **no** hicimos son pruebas con diseñadores reales, y
lo digo así: es lo primero con más tiempo.

**7 · ¿Qué pasa si no hay dato de algo?**
La hoja toma la serie de un pariente (primero un hermano, después el padre, nunca otra familia) y lo dice:
«↪ prestado», con el porqué. Si no hay pariente, queda neutra con «○ Sin dato directo», nunca en rojo. Si la ficha no
puede decir de dónde sale cada número, pone «Sin recomendación». De 133 hojas: 74 con dato propio, 42 prestadas y 17
sin dato.

**8 · ¿Por qué Groq y no otra API?**
Es el patrón de la clase (V2): la página llama a la API desde el navegador con la clave de cada usuario, así que no
hace falta servidor y GitHub Pages alcanza. Groq tiene plan gratis y es rápido. El modelo es `openai/gpt-oss-120b`, y la página
valida el JSON que devuelve antes de mostrarlo. Netlify, que hacía de servidor, está pausado desde que se quedó sin créditos.

**9 · ¿Cuánto cuesta correrla?**
Hoy, cero. GitHub Pages es gratis, CLIP y el K-means corren en la computadora de quien la usa, y Groq va en el plan
gratis con la clave de cada uno. El límite real es el plan: 8.000 tokens por minuto, y cada pregunta usa unos 4.000.
Si muchos la usaran a la vez con una sola clave, habría que pasar a un plan pago, que cobra por token.

**10 · ¿Qué harían con más tiempo?**
Probarla con diseñadores reales. Separar hombre y mujer, volviendo a agregar Vogue y H&M desde el archivo original.
Medir el calzado recortando los pies de cada foto de pasarela. Calcular la etapa desde las curvas para todos los
atributos, no sólo para los 17 del K-means. Y sumar pasarela posterior a 2023, que hoy no es pública.

**11 · ¿Por qué K-means y no un modelo supervisado?**
Porque no hay etiquetas de etapa. Etiquetarlas a mano sería contestar la pregunta antes de hacerla. El K-means agrupa
lo que se mueve parecido y después nombramos cada grupo por el prototipo de etapa más cercano. Una tendencia nueva se
asigna al centroide más cercano y nunca reentrena el modelo.

**12 · ¿Entonces CICLO predice?**
No, y lo probamos. Cuatro métodos contra «repetir el último valor», y ninguno le gana. La búsqueda tampoco predice la
venta: en VISUELLE (5.577 productos con venta real) explica el 0,1 %. La pasarela no adelanta a la búsqueda, ni por año
ni por temporada, en una prueba preregistrada. CICLO lee el presente; la línea punteada hasta 2030 no es un pronóstico
y lo dice.

**13 · ¿Qué tan bien reconoce CLIP una prenda?**
En 150.000 looks de Vogue que no están en el índice, el AUC mediano es 0,90, y el atributo correcto queda entre los
tres primeros del 67 % al 92 % de las veces según el atributo (animal print, 20 %). Si ningún atributo pasa 0,35 de
probabilidad, la app dice «No determinado». La foto no sale de la computadora.

**14 · ¿Usan datos sintéticos?**
Zara 2018–22 y el mix de marcas resultaron sintéticos: las variables casi no se correlacionan y un árbol acierta 50,8 %
contra una base de 50,2 %. Quedan como demostración de método, rotulados así en la app, y no entran al K-means ni a
ninguna recomendación. Zara febrero 2024 es mitad real (licencia MIT).

**15 · ¿Cómo pasaron el Figma a código?**
La app no salió de un Figma: se escribió directo en código con Claude Code. Lo que la cambió fue la devolución de Iván
(«muy IA») y la referencia que pasó: el sistema de diseño de Apple publicado en shadcn.io, que adaptamos tomando unas
cosas y otras no. El Figma de esta entrega lo cuenta en tres etapas, y la tercera la armó el MCP de Figma a partir del
código: figma.com/design/4lvJEf2ZjBX87sXEySXqa7. Detalle en `figma_a_codigo.md`.

**16 · ¿Por qué se parece a Apple?**
Porque esa fue la referencia de la cátedra (Iván, 27/10). Se tomó el sistema (tipografía, gris perla, tarjetas sin
sombra, un solo azul para lo que se toca) y no la marca: ni logo, ni nombre, ni fotos. Y se le agregó lo propio: el
color sigue siendo la señal, Entrar, Esperar y Salir, siempre con su palabra.
