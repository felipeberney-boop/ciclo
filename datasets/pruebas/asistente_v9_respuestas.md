# Prompt v9 · respuestas reales en Lectura (16/11/2026)

Groq, `openai/gpt-oss-120b`, temperatura 0,3, `reasoning_effort: low`. Perfil: mujer · para una marca · fast fashion.
Corridas con `codigo/probar_demo.js` y con la prueba de Lectura de esa tarde, en la app servida en local. Se copian la
conclusión y el respaldo tal como volvieron. El modelo no es determinista: la redacción cambia de una corrida a otra; los
números tienen que ser los de DATOS.

| Qué se le pidió | Conclusión | Respaldo | Contexto |
|---|---|---|---|
| «¿Qué material le va a un jean baggy?», con el diseño baggy de Diseñar | Gamuza, el material que más sube, le va a un jean baggy. | Gamuza +29 puntos fuera 2022→2024, fuente: datos de materiales. | Unos 6.600 tokens. La pieza de datos que trajo la burbuja: Gamuza (foto y curva) |
| «¿Cómo está Prada?» | Prada está #6 en Lyst al cierre de Q2-26. | #6 en el tramo 2 (Q2-26), Lyst Index, tramo 2 (Q1-26 en adelante). | Nombró el tramo y no cruzó el corte de Q1-26. La pieza: Prada en el Lyst Index, con los dos tramos separados |
| La devolución de una foto subida (un look con jean ancho; CLIP leyó Jeans baggy) | El corte baggy está bien; cambiaría a un material que sube, como gamuza. | — (se ve en la captura de la prueba) | Pregunta interna: «Revisá este diseño: qué está bien y qué cambiarías.» |
| La devolución del look de ejemplo Trench, después de sacar el chip «Trench» (quedó sólo el color) | El color beige/camel está bien; cambiaría el material a gamuza para seguir la tendencia ascendente. | Gamuza +29 puntos en la búsqueda mundial 2022→2024; el color leído por CLIP es beige/camel (interpretación de pasarela). | La misma burbuja, rehecha al corregir |

**Lo que se aprendió del límite de Groq.** Cada llamada usa unos 6.000 tokens y el plan gratis deja 8.000 por minuto: dos
llamadas seguidas (la devolución de una imagen y una pregunta) dan 429. Desde el 16/11 la app espera lo que Groq pide,
con la cuenta regresiva en la burbuja, y reintenta sola; en la prueba, la segunda respuesta llegó a los 47 s.
