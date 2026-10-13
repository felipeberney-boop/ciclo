# Prompts

Los prompts que usa la app, versionados. Cada vez que cambia uno se agrega un archivo nuevo con el
número siguiente, no se pisa el anterior.

| Archivo | Para qué | Estado |
|---|---|---|
| `prompt_lectura_recomendacion_v1.md` | IA-5 · leer el grupo y recomendar | en uso, con prompt fijo |
| `prompt_consulta_por_imagen_v1.md` | IA-6 · atributos a partir de una foto | reemplazado por v2 |
| `prompt_consulta_por_imagen_v2.md` | IA-6 · CLIP en el navegador: atributos, looks parecidos y años | en uso |

**Regla que atraviesa todo:** el modelo de lenguaje nunca recibe una fila de la base. Recibe métricas ya
calculadas. Lo que devuelve aparece en la interfaz marcado como interpretación, nunca como dato.

**Claves de API.** Ninguna está acá ni en ningún otro archivo del repositorio. La de Groq se configura
como variable de entorno en Netlify (`GROQ_API_KEY`).
