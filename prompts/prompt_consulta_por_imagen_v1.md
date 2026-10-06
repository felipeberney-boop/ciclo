# IA-6 · Consulta por imagen · v1

**Fecha:** 22/09/2026
**Modelo:** clasificador de imagen de moda
**Estado:** en uso

## Qué entra

Una foto, un dibujo o una captura de pantalla que sube la usuaria.

## Qué sale

Los atributos detectados, con su nivel de confianza. Ejemplo:

```
denim · corte amplio · azul lavado · sin estampa     confianza media (4 de 6 atributos)
```

Después la app busca cada atributo en el mapa del ciclo y devuelve su etapa. Esa parte **no es IA**: es
una búsqueda en la tabla del modelo.

## Por qué existe

Responde a la devolución de la Entrega 1: «ida y vuelta con imágenes de prendas». Es la única pantalla
donde la usuaria aporta el dato en vez de leerlo.

## Límite declarado

Si el clasificador no reconoce un atributo que no está entre los 18 del modelo, la app lo muestra como
detectado pero sin etapa. No inventa una posición en el ciclo.
