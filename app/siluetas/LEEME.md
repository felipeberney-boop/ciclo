# Siluetas y muestras de CICLO

Ilustraciones propias, dibujadas como SVG. No hay ninguna foto: las imágenes de pasarela que
tenemos son de Vogue y no tienen licencia, y una foto de un jean trae un lavado, un color, una
modelo y un fondo que distraen de lo único que se quiere ver, que es la forma.

## Cómo usarlas

Van en `currentColor`, así que toman el color del texto del contenedor y funcionan igual en claro
y en oscuro sin tocar nada. Se pueden insertar inline o como `<img>`.

```html
<div style="color: var(--ink); width: 90px">
  <!-- pegar acá el contenido del SVG -->
</div>
```

## jeans/ — 10 cortes

Todas comparten **la misma cintura y la misma caja**: sólo cambia la pierna. Esa es la decisión que
las hace comparables de un vistazo, que es lo que una grilla de fotos no da nunca.

`skinny · slim · cigarette · straight · tapered · bootcut · flare · wide-leg · baggy · barrel`

Mom, boyfriend, jeggings y relaxed no están: no son cortes. Mom es tiro alto con taper, boyfriend
es un fit, jeggings es una prenda híbrida y relaxed es un descriptor de holgura. Van en los ejes de
tiro y de fit, que son preguntas aparte.

## estampas/ — 22 muestras

Fichas de 120×120 que repiten sin costura, así que sirven igual de miniatura o de fondo. Cuando un
patrón necesita dos valores se usa `currentColor` con opacidad, nunca un segundo color: el color
queda reservado para las prendas.

Agrupadas por familia: rayas (Breton, pinstripe, bengala, awning), lunares (polka dot, pin dot),
cuadros (tartán, vichy, pied-de-poule, Príncipe de Gales, windowpane, argyle), animal (leopardo,
cebra, pitón, vaca) y otros (camuflado, paisley, tie-dye, chevron, espiga, toile de Jouy).

## fits/ — 6

Buzos y remeras vistos en plano. Mismo hombro, mismo escote: cambia el ancho, el largo y la caída
de hombro.

`fitted · regular · relaxed · oversized · boxy · cropped`

## cuellos/ — 9

Recorte de hombros y pecho. Lo único que cambia es la abertura.

`crew · escote en V · scoop · bateau · escote cuadrado · turtleneck · mock · cowl · halter`

## mangas/ — 10

Mismo cuerpo, misma axila: cambia sólo la manga.

`sin manga · cap · corta · tres cuartos · larga · drop shoulder · raglan · puff · bishop · balloon`

Son tres ejes **independientes**: un buzo oversized puede tener cuello crew y manga raglan. En la
interfaz se eligen por separado, no como una lista única.

### Pendiente

**`estampa_houndstooth.svg` no está bien.** Es la única que no salió: los dientes se fusionan con
los cuadros vecinos y lee como damero diagonal en vez de pied-de-poule. Hay que rehacerla.

La espiga es técnicamente un tejido, no un estampado. Se deja en el grupo porque el diseñador la
busca ahí.
