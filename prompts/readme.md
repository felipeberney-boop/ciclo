# Prompts

Los prompts que usa la app, versionados. Cada vez que cambia uno se agrega un archivo nuevo con el
número siguiente, no se pisa el anterior.

| Archivo | Para qué | Estado |
|---|---|---|
| `prompt_lectura_recomendacion_v1.md` | IA-5 · leer el grupo y recomendar | reemplazado por v2 |
| `prompt_lectura_recomendacion_v2.md` | IA-5 · leer un atributo y recomendar, en vivo (función de Netlify) | reemplazado por v3 |
| `prompt_lectura_recomendacion_v3.md` | IA-5 · lo mismo, con `gpt-oss-120b` (Groq ya no tiene Llama) | reemplazado por v4 |
| `prompt_lectura_recomendacion_v4.md` | IA-5 · lo mismo, desde el navegador con la clave de cada uno; peso 2022→2024 | en uso |
| `prompt_asistente_v1.md` | IA-8 · Preguntale a CICLO: chat con la API key de cada uno y `llm/ciclo_datos.md` | reemplazado por v2 |
| `prompt_asistente_v2.md` | IA-8 · Preguntar como herramienta de diseño: tu diseño, imagen por CLIP, el dato en la burbuja y acciones | en uso |
| `prompt_consulta_por_imagen_v1.md` | IA-6 · atributos a partir de una foto | reemplazado por v2 |
| `prompt_consulta_por_imagen_v2.md` | IA-6 · CLIP en el navegador: atributos, looks parecidos y años | reemplazado por v3 |
| `prompt_consulta_por_imagen_v3.md` | IA-6 · lo mismo, con 17 atributos (sin calzado) | en uso |
| `prompt_disenar_referencias_y_colores_v1.md` | IA-7 · Diseñar: fotos de referencia y colores de la pasarela | en uso |

**Regla que atraviesa todo:** el modelo de lenguaje nunca recibe una fila de la base. Recibe métricas ya
calculadas. Lo que devuelve aparece en la interfaz marcado como interpretación, nunca como dato.

**Claves de API.** Ninguna está acá ni en ningún otro archivo del repositorio. IA-5 usa la de Groq guardada
como variable de entorno en Netlify (`GROQ_API_KEY`). IA-8 usa la que pega cada uno en la página, que queda
en su navegador.
