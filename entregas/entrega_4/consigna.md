# Entrega 4 · la consigna

Copiada el 10/11/2026 de la página de la materia en Superhuman Docs (K576 · IA Aplicada Diseño UdeSA · Estudiantes → Entrega 4), sin editar el texto.

Fecha de entrega: 17/11/2026
Modalidad: Presentación oral de 10 minutos por grupo
Consigna: Entrega 4. Prototipo online funcional
App operativa. 
Incluye integración con IA en tiempo real
Una página de racional que explique la hipótesis, el procesamiento de datos y el rol de la IA.
Incluye “una pirueta” (ver más abajo). 
Demo en vivo durante la clase.
Criterio
Qué se evalúa
Entrega 4
1. Hipótesis y foco
Claridad del problema, del cliente/usuario y de la hipótesis de trabajo. Que la propuesta responda a algo específico del tópico elegido, no genérico.
Presentar la hipótesis en su versión ajustada tras las entregas anteriores, indicando qué cambió y por qué. Verificar que la herramienta construida sirva efectivamente para comprobarla: que el usuario definido en la Entrega 1 pueda tomar, con la app, la decisión que hoy no puede tomar bien. Si el foco se redefinió, justificarlo con lo aprendido al trabajar con los datos.
2. Rigor con los datos
Uso correcto de los datasets, análisis que sostiene la hipótesis, y distinción explícita entre lo que es dato verificado/calculado y lo que es inferencia del LLM.
Incorporar a la app los datasets definitivos, con los cálculos realizados directamente sobre los datos (agregaciones, comparaciones, segmentaciones) y verificables por el grupo. Hacer visible dentro de la interfaz la diferencia entre lo calculado y lo inferido por el LLM (etiquetas, secciones separadas o similar). Documentar las limitaciones del dataset (cobertura, sesgos, ausencias) y cómo afectan las conclusiones.
3. Integración de IA
Que la IA cumpla un rol funcional real en el flujo: qué pregunta responde, con qué prompt, con qué límites.
Tener la IA funcionando dentro del prototipo, conectada mediante la API de groq o el LLM que hayan elegido. Presentar el system prompt utilizado, qué datos se le envían como contexto y qué se le pide devolver.
4. Diseño / UX
Coherencia visual, jerarquía de información, usabilidad de la herramienta como apoyo a la toma de decisiones.
Presentar el diseño de Figma pasado a código. Documentar el proceso de traducción: qué se leyó del diseño a través de un agente de IA, qué se implementó a mano o con asistencia de herramientas y qué decisiones se tomaron por fuera de Figma en la instancia de código (estados, responsive, casos de error o carga). Señalar las diferencias entre el diseño original y la versión implementada, y contextualizarlas.
5. Comunicación
Capacidad del grupo de explicar y defender sus decisiones (de diseño, de datos, de prompting) en la instancia de presentación.
Presentar en 15 minutos la aplicación online y los puntos 2, 3 y 4. Presentar link a los repositorios actualizados y completos.



A. Qué es el racional
Es el documento que explica por qué su herramienta es como es. No describe la interfaz: justifica decisiones. Tiene que poder leerlo alguien que no vio la cursada y entender el problema, los datos, el modelo y el diseño, y poder replicar el razonamiento. Si algo está en la herramienta, tiene que estar explicado acá.
Regla de autoría: las decisiones de diseño son de ustedes, no de la IA. El racional tiene que mostrar el proceso humano: bocetos en Figma anteriores a cualquier interacción con Claude u otra IA, y una nota sobre qué propuso la IA, qué descartaron y por qué.
Ítems fundamentales
Problema y contexto. ¿A quién le sirve esto, en qué situación y qué decisión necesita tomar? Sumen evidencia real del negocio: ¿las personas o empresas usan hoy un brief, un tablero o un informe para decidir? Si es así, incluyan ejemplos reales.
Hipótesis. Enunciada en una frase, con sus límites. Puede ser simple, pero tienen que decir qué asumen y qué no pueden afirmar.
Datos y trazabilidad.
Tabla de fuentes: origen, quién las produce, cada cuánto se actualizan, licencia y limitaciones.
Cómo se relacionan entre sí las fuentes (qué cruzan y con qué clave).
Diccionario de variables: todas, con definición, unidad, rango y cálculo.
Cómo se construye cada índice, puntaje o cluster (algoritmo, parámetros, cómo se interpretan los colores).
Repositorio con decisiones, fuentes y README actualizados.
Modelo o lógica de análisis. Qué entra, qué se calcula y qué sale. Un esquema simple de entradas, proceso y salidas. Qué quedó afuera y por qué.
Usuario (perfil, objetivos y recorrido) y flujo diseñado. Justifiquen también las decisiones de ramificación si las hubiera.
Decisiones de diseño. Qué es lo más importante de cada pantalla (o grupo de pantallas similares) y cómo lo jerarquizaron. Sistema de color, grilla y tipografía: qué decidieron, por qué y cómo favorece la experiencia.
Recorte territorial o de alcance, si aplica. Mapa del límite real que incorporaron a la herramienta, con la terminología correcta (por ejemplo, barrios y no comunas).
Proceso y uso de IA. Bocetos previos, iteraciones, y un registro de qué le pidieron a la IA, qué aceptaron, qué corrigieron y qué rechazaron. Qué modelos están usando y cómo gestionaron el system prompt.


Algunos ejemplos:
Data Sketches - The Words of the Lord of the Rings


Voices of Peace


The Design Philosophy of the QQL Algorithm | Tyler Hobbs


An Interactive Visualization of Every Line in Hamilton


Myriad (Tulips) | Anna Ridler


B. La Pirueta
La pirueta es una pieza de diseño que va un paso más allá de lo esperable en el proyecto y que muestra, de forma sorprendente, un valor agregado: narrativo, funcional o estético o de otra índole. Puede vivir dentro de la herramienta (una pantalla, una interacción, un modo de explorar los datos) o dentro del racional (una forma distinta de contar el proceso, el modelo o los datos). No puede ser un link extra ni estar fuera de la app o racional.
La pirueta no reemplaza lo que el proyecto ya tiene que resolver. El objetivo es demostrar que el equipo puede dirigir a la IA con criterio propio: elegir qué capacidad usar, para qué, y dónde frenar.
No hay limitaciones para la pirueta.

