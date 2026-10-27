# Prueba por temporada · preregistro

Escrito y commiteado el 27/10/2026, **antes de tener la búsqueda mensual de los atributos y antes de calcular nada**.
Si algo cambia después de ver datos, se agrega abajo como enmienda fechada; no se reescribe.

## La pregunta

¿La pasarela adelanta a la búsqueda a escala de temporada? A escala anual se rechazó (13/10: máxima sin rezago, +0,43;
en cambios año a año pasan 2 de 65 pruebas). Un adelanto de seis a nueve meses —el desfile de febrero, la búsqueda del
otoño siguiente— queda adentro del mismo año y con datos anuales no se puede ver.

> **H.** Cuando un atributo crece en la pasarela de una temporada frente a la misma temporada del año anterior, crece
> también su búsqueda mundial entre 3 y 18 meses después, más de lo que daría el azar.

## Datos

- **Pasarela:** `traopia/vogue-runway` (Hugging Face, 1,71 M de filas): sección «Collection», sin novias, 2004–2023.
  Por temporada, la proporción de looks con la etiqueta del atributo. Vogue trae temporada y año, no la fecha del
  desfile: cada temporada se ubica en su mes por calendario. **Fall Y → marzo de Y; Spring Y → septiembre de Y−1;
  Resort Y → junio de Y−1; Pre-Fall Y → diciembre de Y−1.**
- **Búsqueda:** Google Trends mundial, mensual, 2004-01 a 2024-12 (2025 y 2026 fuera, por el salto de medición).
  Los atributos de CICLO salen del plan 4 (`datasets/plan_exportacion_trends_4.csv`, lotes 23 a 25); los cinco que ya
  tienen serie mensual y etiqueta en Vogue salen de los lotes existentes.

| Atributo | Etiquetas de Vogue | Búsqueda |
|---|---|---|
| Trench | Trench Coat | trench coat |
| Cuero | Leather Jacket | leather jacket |
| Encaje | Lace | lace dress |
| Lunares | Polka Dot | polka dot dress |
| Floral | Flower, Floral Design, Flower Arrangement, Flower Bouquet | floral dress |
| Cuadros | Plaid, Tartan | plaid skirt |
| Kimono | Kimono | kimono jacket |
| Capa | Cape, Cloak | cape coat |
| Animal print | Zebra, Giraffe, Cow, Animal | leopard print |
| Buzo | Sweatshirt, Hoodie | hoodie |
| Piel | Fur | fur coat |
| Denim | Denim, Jeans | jeans |
| Cardigan | Cardigan | cardigan |
| Blusa | Blouse | blouse |
| Lino | Linen | linen |
| Minifalda | Miniskirt | mini skirt |

Las etiquetas de los atributos de CICLO son las de `codigo/verificar_pasarela.py`. Un atributo entra sólo si tiene, en
promedio, al menos 20 looks etiquetados por temporada principal (Fall y Spring); si no, se informa y queda afuera.

## La trampa, y cómo se evita

La búsqueda tiene estación: un abrigo que desfila en marzo y se busca en noviembre parece un adelanto de ocho meses y
es sólo el invierno. Por eso **todo se compara contra el mismo momento del año anterior**:

- pasarela: proporción de la temporada S del año Y menos la de S del año Y−1;
- búsqueda: logaritmo del mes m menos el del mes m−12.

## Análisis

1. Para cada atributo y cada desfile (temporada S, año Y, ubicado en el mes t), el cambio de la pasarela contra el
   cambio de la búsqueda en t + L, con **L = 0, 3, 6, 9, 12, 15 y 18 meses**.
2. Correlación de Spearman por atributo y rezago; el estadístico de cada rezago es la mediana entre atributos.
3. Contra el azar: se barajan los años de la pasarela dentro de cada atributo 10.000 veces y se recalcula.
4. Corrección por siete rezagos: Bonferroni, α = 0,05 / 7 ≈ 0,007.

## Criterio de decisión

- **H se sostiene** si algún rezago entre 3 y 18 meses tiene mediana positiva con p < 0,007 **y** es mayor que la del
  rezago 0 (si no, es la misma moda vista a la vez, no un adelanto).
- **H se rechaza** si ningún rezago entre 3 y 18 meses pasa.
- Si quedan menos de 6 atributos con datos suficientes, **no concluye**.

Se informa salga como salga: en `decisiones.md`, `hipotesis.md`, Método y el making of.

## Lo que esta prueba no controla

- La fecha de cada desfile es aproximada (por temporada), así que un rezago de 3 meses tiene un margen de ±1 mes.
- Las etiquetas de Vogue las puso un modelo de visión y no siempre separan bien (Floral junta varias).
- Es correlación: aunque aparezca un adelanto, no prueba que el desfile cause la búsqueda.

## Enmienda 1 · 27/10/2026, con los lotes bajados y antes de calcular

- **Floral queda afuera:** el lote 23 se exportó sin «floral dress».
- **Animal print usa «leopard»** en vez de «leopard print»: es el término que trae el lote 24.
- **Ceros:** varias series mensuales tienen meses en 0 o «<1». El cambio de la búsqueda es log(x+1) del mes m menos
  log(x+1) del mes m−12, con «<1» tomado como 0,5.
- **Mínimo de pares:** un atributo entra a un rezago si tiene al menos 10 pares desfile–búsqueda en ese rezago.
