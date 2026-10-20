"""CICLO · la taxonomía de Diseñar (20/10/2026). Fuente única: de acá salen app/diseno/taxonomia.json y la constante
`const TAX=` de app/index.html. Uso, desde la raíz del repo: python3 codigo/taxonomia.py

Cuatro niveles de prenda —prenda › tipo › corte › tiro— y tres ejes aparte: material, detalle y estampa. El jean no es una
prenda: es pantalón + denim. «Short de jean» existe sin listarlo (short + denim).

Cada atributo dice qué dato lo respalda, si hay alguno:
  km   nombre del atributo en el K-means (etapa → la regla de CICLO para tu perfil)
  rec  id con serie de búsqueda en Recorridos (peso afuera 2023→2025)
  je   términos de Google Trends dentro de las búsquedas de jeans (parte de las búsquedas, 2023→2025)
  clip qué lectura de CLIP sobre la pasarela usa (fit, cuello, manga, color)
Lo que no tiene ninguno aparece igual —con su dibujo y su definición— pero como «sin dato medido».

Mom, boyfriend y jeggings no son cortes: quedan sólo como alias de búsqueda (invisibles en la interfaz), para que las
series de Google Trends que vienen con ese nombre sigan enganchando con el corte que les corresponde."""
import json, os, re

# ---------- nivel 3 · cortes de pantalón largo (los dibujados en app/siluetas/jeans) ----------
CORTES = [
  dict(id='skinny', n='Skinny', d='Ajustado de la cadera al tobillo.', sil='jeans/corte_skinny', km='Jeans skinny', je=['skinny', 'jeggings'], clip_jeans='skinny'),
  dict(id='slim', n='Slim', d='Angosto, sin pegarse a la pierna.', sil='jeans/corte_slim', km='Jeans skinny', je=['slim'], clip_jeans='slim'),
  dict(id='straight', n='Straight', d='Recto de la rodilla al ruedo.', sil='jeans/corte_straight', km='Jeans rectos', je=['straight leg', 'mom'], clip_jeans='recto'),
  dict(id='tapered', n='Tapered', d='Holgado arriba y angosto en el tobillo.', sil='jeans/corte_tapered', km='Jeans rectos', je=['tapered', 'boyfriend'], clip_jeans='tapered'),
  dict(id='cigarette', n='Cigarette', d='Recto y angosto, al tobillo.', sil='jeans/corte_cigarette'),
  dict(id='bootcut', n='Bootcut', d='Recto con una apertura leve abajo, para la bota.', sil='jeans/corte_bootcut', km='Jeans rectos', je=['bootcut'], clip_jeans='bootcut'),
  dict(id='flare', n='Flare', d='Ajustado hasta la rodilla y acampanado.', sil='jeans/corte_flare', km='Jeans rectos', je=['flare'], clip_jeans='flare'),
  dict(id='wideleg', n='Wide leg', d='Ancho de la cadera al ruedo.', sil='jeans/corte_wide-leg', km='Jeans baggy', je=['wide leg'], clip_jeans='wideleg'),
  dict(id='baggy', n='Baggy', d='Amplio y caído, con tiro bajo o medio.', sil='jeans/corte_baggy', km='Jeans baggy', je=['baggy'], clip_jeans='baggy'),
  dict(id='barrel', n='Barrel', d='Curvo, ancho en la rodilla y cerrado en el ruedo.', sil='jeans/corte_barrel', km='Jeans baggy', je=['barrel'], clip_jeans='barrel'),
]
TIROS = [dict(id='bajo', n='Tiro bajo', d='La cintura cae por debajo del ombligo, sobre la cadera.', sil='tiros/bajo'),
         dict(id='medio', n='Tiro medio', d='La cintura a la altura del ombligo.', sil='tiros/medio'),
         dict(id='alto', n='Tiro alto', d='La cintura por encima del ombligo.', sil='tiros/alto')]
# alias de búsqueda: nunca se muestran; sólo enganchan series con el nombre viejo
ALIAS = {'mom': dict(corte='straight', tiro='alto', fit='relaxed'), 'boyfriend': dict(corte='tapered', tiro='medio', fit='relaxed'),
         'jeggings': dict(corte='skinny', tiro='medio', fit='al cuerpo')}

# ---------- niveles 1 y 2 · prenda y tipo ----------
PRENDAS = [
  dict(id='pantalones', n='Pantalones', d='De la cintura para abajo, con dos piernas.', sil='pantalones/largo', tipos=[
    dict(id='largo', n='Largo', d='Hasta el tobillo.', sil='pantalones/largo', pasos=['corte', 'tiro'], jeans=['jamplio', 'jmedio', 'jajust']),
    dict(id='short', n='Short', d='Por encima de la mitad del muslo.', sil='pantalones/short', pasos=['tiro']),
    dict(id='bermuda', n='Bermuda', d='Hasta la rodilla.', sil='pantalones/bermuda', pasos=['tiro']),
    dict(id='capri', n='Capri', d='A media pantorrilla.', sil='pantalones/capri', pasos=['tiro'])]),
  dict(id='faldas', n='Faldas', d='De la cintura para abajo, sin piernas.', sil='faldas/midi', solo='mujer', tipos=[
    dict(id='mini', n='Mini', d='Por encima de la mitad del muslo.', sil='faldas/mini'),
    dict(id='midi', n='Midi', d='Entre la rodilla y el tobillo.', sil='faldas/midi'),
    dict(id='maxi', n='Maxi', d='Hasta el tobillo.', sil='faldas/maxi')]),
  dict(id='vestidos', n='Vestidos', d='Una sola pieza de los hombros para abajo.', sil='vestidos/evase', solo='mujer', tipos=[
    dict(id='slip', n='Slip', d='De breteles finos, cae recto.', sil='vestidos/slip'),
    dict(id='camisero', n='Camisero', d='Con cuello y botones, como una camisa larga.', sil='vestidos/camisero'),
    dict(id='cruzado', n='Cruzado', d='Escote en V que se cruza y se ata.', sil='vestidos/cruzado'),
    dict(id='tubo', n='Tubo', d='Al cuerpo, de los hombros al ruedo.', sil='vestidos/tubo'),
    dict(id='evase', n='Evasé', d='Se abre en A desde la cintura.', sil='vestidos/evase')]),
  dict(id='remeras', n='Remeras y tops', d='Parte de arriba de punto o tela liviana.', sil='fits/fit_regular', tipos=[
    dict(id='remera', n='Remera', d='De punto, con mangas.', sil='fits/fit_regular', pasos=['fit', 'cuello', 'manga'], clip='remeras'),
    dict(id='musculosa', n='Musculosa', d='Sin mangas, de breteles anchos.', sil='tops/musculosa'),
    dict(id='top', n='Top', d='Corto, de breteles finos.', sil='tops/top', solo='mujer'),
    dict(id='corset', n='Corset', d='Estructurado, ceñido a la cintura.', sil='tops/corset', solo='mujer', rec='corset', clip_corte='corset')]),
  dict(id='camisas', n='Camisas', d='Parte de arriba de tela plana, con cuello y botones.', sil='camisas/clasica', tipos=[
    dict(id='clasica', n='Clásica', d='Cuello, botones y puño.', sil='camisas/clasica'),
    dict(id='oversize', n='Oversize', d='Más ancha y más larga, de hombro caído.', sil='camisas/oversize'),
    dict(id='cropped', n='Cropped', d='Corta, por encima de la cintura.', sil='camisas/cropped'),
    dict(id='blusa', n='Blusa', d='Más liviana y suelta, sin cuello de camisa.', sil='camisas/blusa', solo='mujer')]),
  dict(id='buzos', n='Buzos y sweaters', d='De punto grueso, para abrigar.', sil='buzos/sweater', tipos=[
    dict(id='buzo', n='Buzo', d='De frisa o algodón, con o sin capucha.', sil='buzos/capucha', pasos=['fit', 'cuello', 'manga'], clip='buzos', km='Buzo / hoodie', rec='buzo'),
    dict(id='sweater', n='Sweater', d='De lana o hilo, cuello redondo.', sil='buzos/sweater'),
    dict(id='cardigan', n='Cárdigan', d='Abierto adelante, con botones.', sil='buzos/cardigan'),
    dict(id='polera', n='Polera', d='Sweater de cuello alto.', sil='buzos/polera')]),
  dict(id='abrigos', n='Camperas y abrigos', d='La capa de afuera.', sil='abrigos/trench', tipos=[
    dict(id='trench', n='Trench', d='Gabardina cruzada con cinturón.', sil='abrigos/trench', km='Trench', rec='trench', clip_corte='trench'),
    dict(id='blazer', n='Blazer', d='Saco de sastrería, aquí más grande.', sil='abrigos/blazer', km='Blazer oversize', clip_corte='blazer'),
    dict(id='campera', n='Campera', d='Corta, a la cadera, con cierre.', sil='abrigos/cuero', clip_corte='cuero'),
    dict(id='tapado', n='Tapado', d='Abrigo largo de paño.', sil='abrigos/tapado'),
    dict(id='capa', n='Capa', d='Sin mangas, cae desde los hombros.', sil='abrigos/capa', km='Capa', rec='capa', clip_corte='capa'),
    dict(id='kimono', n='Kimono', d='Abierto, de mangas anchas y rectas.', sil='abrigos/kimono', km='Kimono', rec='kimono', clip_corte='kimono'),
    dict(id='piel', n='Tapado de piel', d='Piel o piel sintética.', sil='abrigos/piel', km='Piel', clip_corte='piel'),
    dict(id='puffer', n='Puffer', d='Acolchado, relleno de pluma o sintético.', sil='abrigos/puffer')]),
  dict(id='enteritos', n='Enteritos', d='Arriba y abajo en una sola pieza.', sil='enteritos/largo', tipos=[
    dict(id='largo', n='Mono largo', d='Con pierna larga.', sil='enteritos/largo'),
    dict(id='corto', n='Mono corto', d='Con pierna de short.', sil='enteritos/corto'),
    dict(id='jardinero', n='Jardinero', d='Con pechera y tiradores.', sil='enteritos/jardinero')]),
]

# ---------- material, agrupado como se muestra ----------
M = lambda id, n, d, tex, **k: dict(id=id, n=n, d=d, tex=tex, **k)
MATERIALES = [
  dict(grupo='De punto', items=[M('jersey', 'Jersey de algodón', 'El punto de la remera.', 'materiales/jersey'),
    M('rib', 'Rib (morley)', 'Punto acanalado, elástico.', 'materiales/rib'), M('frenchterry', 'French terry', 'Frisa sin perchar: rulos del lado de adentro.', 'materiales/jersey'),
    M('fleece', 'Fleece', 'Frisa perchada, suave y abrigada.', 'materiales/lana'), M('cable', 'Cable knit', 'Tejido de trenzas.', 'materiales/cable'),
    M('boucle', 'Bouclé', 'Hilado con rulos, de superficie rugosa.', 'materiales/boucle')]),
  dict(grupo='Planos de algodón', items=[M('algodon', 'Algodón liso', 'Tafetán: la trama más simple.', 'materiales/tafetan'),
    M('popelina', 'Popelina', 'Algodón fino y apretado, de camisa.', 'materiales/tafetan'), M('pique', 'Piqué', 'Trama en panal, de chomba.', 'materiales/pique'),
    M('gabardina', 'Gabardina', 'Sarga firme, de trench y pantalón.', 'materiales/denim'), M('corduroy', 'Corduroy (pana)', 'Costillas de pelo en relieve.', 'materiales/corduroy'),
    M('lona', 'Lona', 'Algodón grueso y resistente.', 'materiales/tafetan')]),
  dict(grupo='Denim', items=[M('denimrigido', 'Denim rígido', 'Sarga de algodón, sin elastano.', 'materiales/denim'),
    M('denimelastano', 'Denim con elastano', 'Sarga con algo de stretch.', 'materiales/denim'), M('denimlavado', 'Denim lavado', 'Sarga aclarada con lavados.', 'materiales/denim')]),
  dict(grupo='Lanas', items=[M('lana', 'Lana', 'Fibra animal, abriga.', 'materiales/lana'), M('merino', 'Merino', 'Lana fina, no pica.', 'materiales/jersey'),
    M('cashmere', 'Cashmere', 'Lana de cabra, muy suave.', 'materiales/lana'), M('tweed', 'Tweed', 'Lana rústica de hilos de colores.', 'materiales/tweed'),
    M('pano', 'Paño', 'Lana abatanada, de tapado.', 'materiales/lana')]),
  dict(grupo='Naturales finos', items=[M('lino', 'Lino', 'Fibra vegetal fresca, con irregularidades.', 'materiales/lino'),
    M('seda', 'Seda', 'Fibra animal liviana y brillante.', 'materiales/saten'), M('satenseda', 'Satén de seda', 'Seda de cara brillante.', 'materiales/saten')]),
  dict(grupo='Pieles', items=[M('cuero', 'Cuero', 'Piel curtida.', 'materiales/cuero', km='Cuero', rec='cuero'),
    M('gamuza', 'Gamuza (suede)', 'Cuero del lado del revés, aterciopelado.', 'estampas/estampa_gamuza', rec='gamuza'),
    M('cuerina', 'Cuerina (eco-leather)', 'Imitación de cuero sintética.', 'materiales/cuero')]),
  dict(grupo='Sintéticos', items=[M('poliester', 'Poliéster', 'Fibra sintética, no se arruga.', 'materiales/sintetico'),
    M('nylon', 'Nylon', 'Sintético liviano y resistente.', 'materiales/sintetico'), M('acrilico', 'Acrílico', 'Imita la lana en tejidos de punto.', 'materiales/lana'),
    M('elastano', 'Elastano', 'La fibra que da stretch.', 'materiales/jersey'), M('neoprene', 'Neoprene', 'Espuma forrada, con cuerpo.', 'materiales/sintetico')]),
  dict(grupo='Livianos', items=[M('gasa', 'Gasa (chiffon)', 'Transparente y vaporosa.', 'materiales/gasa'), M('tul', 'Tul', 'Red fina y transparente.', 'materiales/gasa'),
    M('organza', 'Organza', 'Transparente y rígida.', 'materiales/gasa'), M('crepe', 'Crepe', 'Superficie granulada, cae bien.', 'materiales/tafetan')]),
]
# detalles y aplicaciones: un eje aparte del material. El encaje es un tejido real, pero no un material base.
DETALLES = [M('encaje', 'Encaje', 'Tejido calado, aplicado o en paneles.', 'estampas/estampa_encaje', km='Encaje', rec='encaje'),
  M('cargo', 'Bolsillos cargo', 'Bolsillos de fuelle a los costados.', 'pantalones/cargo', km='Cargo', rec='cargo'),
  M('bordado', 'Bordado', 'Dibujo hecho con hilo.', 'detalles/bordado'), M('volados', 'Volados', 'Tiras fruncidas que ondulan.', 'detalles/volados'),
  M('tachas', 'Tachas', 'Apliques de metal.', 'detalles/tachas'), M('cutouts', 'Cut-outs', 'Aberturas que dejan ver la piel.', 'detalles/cutouts'),
  M('plisado', 'Plisado', 'Pliegues fijos y parejos.', 'detalles/plisado'), M('acolchado', 'Acolchado', 'Costuras en rombo con relleno.', 'materiales/acolchado'),
  M('flecos', 'Flecos', 'Tiras sueltas en el borde.', 'detalles/flecos'), M('pedreria', 'Pedrería', 'Apliques de cristal o mostacillas.', 'detalles/pedreria')]

# ---------- estampas, por familia (las dibujadas en app/siluetas/estampas) ----------
E = lambda id, n, sil, **k: dict(id=id, n=n, sil=f'estampas/estampa_{sil}', **k)
ESTAMPAS = [
  dict(familia='Liso', items=[dict(id='liso', n='Liso', sil=None)]),
  dict(familia='Rayas', items=[E('rayas', 'Rayas', 'rayas', rec='rayas'), E('breton', 'Bretón', 'breton'), E('pinstripe', 'Diplomática', 'pinstripe'),
    E('bengal', 'Bengala', 'bengal'), E('awning', 'Toldo', 'awning')]),
  dict(familia='Lunares', items=[E('lunares', 'Lunares', 'lunares', km='Lunares', rec='lunares'), E('pindot', 'Pin dot', 'pin-dot')]),
  dict(familia='Cuadros', items=[E('cuadros', 'Escocés (tartán)', 'tartan', km='Cuadros'), E('gingham', 'Vichy', 'gingham'), E('pow', 'Príncipe de Gales', 'pow'),
    E('windowpane', 'Ventana', 'windowpane'), E('argyle', 'Rombos (argyle)', 'argyle')]),
  dict(familia='Animal', items=[E('animal', 'Leopardo', 'leopard', km='Animal print', rec='animal'), E('cebra', 'Cebra', 'zebra'), E('piton', 'Pitón', 'python'), E('vaca', 'Vaca', 'cow')]),
  dict(familia='Floral y otras', items=[E('floral', 'Floral', 'floral', km='Floral', rec='floral'), E('paisley', 'Paisley', 'paisley'), E('toile', 'Toile de Jouy', 'toile'),
    E('camo', 'Camuflado', 'camo'), E('tiedye', 'Tie-dye', 'tie-dye'), E('chevron', 'Chevron', 'chevron'), E('espiga', 'Espiga', 'herringbone')]),
]
# los colores que no tienen lectura de CLIP para esa prenda: el vocabulario, sin dato
COLORES = [('negro', 'Negro', '#1D1C1A'), ('blanco', 'Blanco / crudo', '#F2F0EA'), ('gris', 'Gris', '#8C8C88'), ('beige', 'Beige / arena', '#D9C8AE'),
           ('marron', 'Marrón', '#6B4A2F'), ('marino', 'Azul marino', '#23324F'), ('celeste', 'Celeste', '#93BAD8'), ('verde', 'Verde', '#3F6B4A'),
           ('rojo', 'Rojo', '#B02B31'), ('rosa', 'Rosa', '#E3A0B0'), ('naranja', 'Naranja', '#D4682C'), ('amarillo', 'Amarillo', '#DDB53C')]

# ---------- combinaciones que la industria produce ----------
G = {g['grupo']: [i['id'] for i in g['items']] for g in MATERIALES}
DENIM, PUNTO, PLANOS, LANAS, FINOS, PIELES, SINT, LIV = (G[k] for k in ['Denim', 'De punto', 'Planos de algodón', 'Lanas', 'Naturales finos', 'Pieles', 'Sintéticos', 'Livianos'])
MATERIAL_POR_PRENDA = {
  'pantalones': DENIM + ['algodon', 'gabardina', 'corduroy', 'lona', 'lino', 'lana', 'pano', 'tweed', 'satenseda', 'cuero', 'cuerina', 'gamuza',
                         'poliester', 'nylon', 'crepe', 'jersey', 'frenchterry', 'fleece'],
  'faldas': DENIM + ['algodon', 'popelina', 'gabardina', 'corduroy', 'lino', 'seda', 'satenseda', 'lana', 'tweed', 'pano', 'boucle', 'cuero', 'cuerina',
                     'gamuza', 'jersey', 'rib', 'poliester', 'gasa', 'tul', 'organza', 'crepe'],
  'vestidos': ['denimrigido', 'denimlavado', 'algodon', 'popelina', 'pique', 'lino', 'seda', 'satenseda', 'jersey', 'rib', 'cable', 'merino', 'cashmere',
               'cuero', 'poliester', 'neoprene', 'gasa', 'tul', 'organza', 'crepe'],
  'remeras/remera': ['jersey', 'rib', 'pique', 'algodon', 'lino', 'merino', 'poliester', 'elastano'],
  'remeras/musculosa': ['jersey', 'rib', 'algodon', 'lino', 'seda', 'satenseda', 'poliester'],
  'remeras/top': ['jersey', 'rib', 'seda', 'satenseda', 'gasa', 'tul', 'crepe', 'cuero', 'cuerina', 'denimrigido', 'elastano'],
  'remeras/corset': ['satenseda', 'seda', 'algodon', 'denimrigido', 'cuero', 'cuerina', 'tul'],
  'camisas': ['algodon', 'popelina', 'lino', 'seda', 'satenseda', 'gasa', 'crepe', 'corduroy', 'denimrigido', 'denimlavado', 'poliester'],
  'buzos/buzo': ['frenchterry', 'fleece', 'jersey', 'poliester', 'acrilico'],
  'buzos': ['cable', 'merino', 'cashmere', 'lana', 'boucle', 'acrilico', 'rib', 'jersey'],
  'abrigos': ['gabardina', 'lona', 'corduroy', 'denimrigido', 'denimlavado', 'cuero', 'cuerina', 'gamuza', 'lana', 'pano', 'tweed', 'boucle',
              'cashmere', 'nylon', 'poliester', 'fleece', 'satenseda'],
  'abrigos/puffer': ['nylon', 'poliester', 'satenseda'],
  'abrigos/trench': ['gabardina', 'algodon', 'cuero', 'cuerina', 'nylon'],
  'abrigos/piel': ['cuero', 'gamuza', 'cuerina', 'poliester'],
  'enteritos': DENIM + ['algodon', 'gabardina', 'lona', 'lino', 'corduroy', 'crepe', 'satenseda', 'jersey', 'poliester'],
}
TODAS = [i['id'] for f in ESTAMPAS for i in f['items']]
NO = lambda *ids: [e for e in TODAS if e not in ids]
ESTAMPA_POR_MATERIAL = {  # las que se producen en cada grupo de material (por grupo; liso va siempre)
  'Denim': ['liso', 'rayas', 'pinstripe', 'tiedye'],
  'Pieles': ['liso', 'animal', 'cebra', 'piton', 'vaca'],
  'De punto': ['liso', 'rayas', 'breton', 'awning', 'lunares', 'pindot', 'argyle', 'cuadros', 'chevron', 'tiedye', 'floral', 'animal', 'cebra', 'camo', 'paisley'],
  'Planos de algodón': NO('piton', 'vaca', 'argyle'),
  'Lanas': ['liso', 'cuadros', 'pow', 'windowpane', 'espiga', 'argyle', 'rayas', 'pinstripe', 'chevron', 'animal'],
  'Naturales finos': ['liso', 'rayas', 'bengal', 'pinstripe', 'lunares', 'pindot', 'floral', 'paisley', 'toile', 'animal', 'cebra', 'gingham'],
  'Sintéticos': ['liso', 'rayas', 'awning', 'camo', 'animal', 'cebra', 'floral', 'lunares', 'tiedye', 'chevron', 'cuadros'],
  'Livianos': ['liso', 'lunares', 'pindot', 'floral', 'paisley', 'animal', 'rayas'],
}
ESTAMPA_POR_PRENDA = {  # además del material: lo que no se hace en esa prenda
  'pantalones': NO('toile', 'awning', 'breton'), 'abrigos': NO('pindot', 'tiedye', 'awning', 'breton', 'toile'),
  'buzos': NO('toile', 'pow', 'windowpane', 'bengal', 'pinstripe'),
}
DETALLE_POR_PRENDA = {
  'pantalones': ['cargo', 'bordado', 'tachas', 'plisado', 'flecos'], 'faldas': ['encaje', 'bordado', 'volados', 'plisado', 'cargo', 'flecos', 'pedreria', 'tachas'],
  'vestidos': ['encaje', 'bordado', 'volados', 'cutouts', 'plisado', 'flecos', 'pedreria'], 'remeras': ['encaje', 'bordado', 'cutouts', 'pedreria', 'tachas', 'volados'],
  'camisas': ['encaje', 'bordado', 'volados', 'plisado'], 'buzos': ['bordado', 'tachas', 'acolchado'],
  'abrigos': ['bordado', 'tachas', 'acolchado', 'flecos', 'cargo'], 'enteritos': ['cargo', 'bordado', 'cutouts', 'plisado'],
}

# ---------- dato prestado: cuando una hoja no tiene serie propia ----------
# Orden del préstamo: hermano de la misma familia → padre en el árbol → el atributo suelto sin cruzar con la prenda.
# Nunca se salta a otra familia sin parentesco. Referencias: tipo:<prenda>/<tipo>, corte:, tiro:, mat:, det:, estampa:,
# rec:<id con búsqueda>, km:<atributo del K-means>, je:<término de jean>. Los colores sin lectura de CLIP para esa prenda
# toman el color suelto en toda la pasarela (se calcula en la app).
PRESTA = {
  'tipo:pantalones/short': ('tipo:pantalones/largo', 'Hermano: el mismo pantalón, más corto. Short no tiene serie propia todavía.'),
  'tipo:pantalones/bermuda': ('tipo:pantalones/largo', 'Hermano: el mismo pantalón, hasta la rodilla. (Antes tomaba el cargo, que no es su pariente en el árbol.)'),
  'tipo:pantalones/capri': ('tipo:pantalones/largo', 'Hermano: el mismo pantalón, cortado a media pierna.'),
  'tipo:remeras/top': ('rec:corset', 'Hermano: misma familia de tops al cuerpo.'),
  'tipo:buzos/sweater': ('tipo:buzos/buzo', 'Hermano: misma familia de punto abrigado.'),
  'tipo:buzos/cardigan': ('tipo:buzos/buzo', 'Hermano: misma familia de punto abrigado.'),
  'tipo:buzos/polera': ('tipo:buzos/buzo', 'Hermano: misma familia de punto abrigado.'),
  'tipo:abrigos/tapado': ('tipo:abrigos/trench', 'Hermano: el otro abrigo largo de la familia.'),
  'corte:cigarette': ('corte:slim', 'Hermano: el corte más parecido, recto y angosto.'),
  'tiro:alto': ('je:mom', 'La única búsqueda de jean que nombra el tiro: «mom», un recto de tiro alto.'),
  'tiro:bajo': ('km:Y2K', 'Padre: el tiro bajo es la marca del Y2K, que sí tiene serie.'),
  'mat:cuerina': ('mat:cuero', 'Hermano: imita al cuero y se lee con su serie.'),
  'mat:denimrigido': ('tipo:pantalones/largo', 'El denim se mide por los jeans: las tres series de jean.'),
  'mat:denimelastano': ('tipo:pantalones/largo', 'El denim se mide por los jeans: las tres series de jean.'),
  'mat:denimlavado': ('tipo:pantalones/largo', 'El denim se mide por los jeans: las tres series de jean.'),
  'mat:gabardina': ('tipo:abrigos/trench', 'La gabardina es la tela del trench.'),
  **{f'estampa:{e}': ('estampa:rayas', 'Familia: la búsqueda mide las rayas, no cada variante.') for e in ('breton', 'pinstripe', 'bengal', 'awning')},
  'estampa:pindot': ('estampa:lunares', 'Familia: la búsqueda mide los lunares, no su tamaño.'),
  **{f'estampa:{e}': ('estampa:cuadros', 'Familia: la búsqueda mide los cuadros, no cada trama.') for e in ('gingham', 'pow', 'windowpane', 'argyle')},
  **{f'estampa:{e}': ('estampa:animal', 'Familia: la búsqueda mide la estampa animal por el leopardo.') for e in ('cebra', 'piton', 'vaca')},
  'estampa:paisley': ('estampa:floral', 'Familia: motivo orgánico, se lee con el floral.'),
}
def hoja(ref):
    k, v = ref.split(':', 1)
    if k == 'tipo': pr, t = v.split('/'); return next(x for x in next(p for p in PRENDAS if p['id'] == pr)['tipos'] if x['id'] == t)
    if k == 'corte': return next(x for x in CORTES if x['id'] == v)
    if k == 'tiro': return next(x for x in TIROS if x['id'] == v)
    if k == 'mat': return next(i for g in MATERIALES for i in g['items'] if i['id'] == v)
    if k == 'estampa': return next(i for f in ESTAMPAS for i in f['items'] if i['id'] == v)
    raise KeyError(ref)
# ---------- series propias nuevas (codigo/pegar_lotes_trends.py): la hoja pasa a dato directo y deja de pedir prestado ----------
import csv as _csv
SERIES = {}
import glob as _glob
for _f in sorted(_glob.glob('datasets/plan_exportacion_trends*.csv')):
    for r in _csv.DictReader(open(_f)): SERIES.setdefault(r['hoja_taxonomia'], [])
    for r in _csv.DictReader(open(_f)): SERIES[r['hoja_taxonomia']].append(r['termino'])
_hay = {r['atributo_id'] for r in _csv.DictReader(open('datasets_procesados/series_google_trends/trends_mundo__web_anual.csv'))}
def hoja_ref(ref):
    k, v = ref.split(':', 1)
    if k == 'det': return next(d for d in DETALLES if d['id'] == v)
    if k == 'tiro': return next(t for t in TIROS if t['id'] == v)
    return hoja(ref)
for ref, terminos in SERIES.items():  # si hubo reintento, vale el último término que entró
    aid = ref.split(':')[1].replace('/', '_')
    if aid in _hay:
        _t = {r['termino_buscado'] for r in _csv.DictReader(open('datasets_procesados/series_google_trends/trends_mundo__web_anual.csv')) if r['atributo_id'] == aid}
        h = hoja_ref(ref); h['serie'], h['termino'] = aid, next((t for t in reversed(terminos) if t in _t), terminos[-1])
        PRESTA.pop(ref, None)
for ref, (de, porque) in PRESTA.items():
    h = hoja(ref); assert not any(h.get(x) for x in ('km', 'rec', 'je', 'jeans', 'serie')), ('ya tiene serie propia', ref)
    if de.split(':')[0] in ('tipo', 'corte', 'mat', 'estampa'): hoja(de)  # el pariente existe
    h['presta_de'], h['presta_porque'] = de, porque

# ---------- control: todo lo que se nombra existe ----------
ids_mat = {i['id'] for g in MATERIALES for i in g['items']}
for k, v in MATERIAL_POR_PRENDA.items(): assert set(v) <= ids_mat, (k, set(v) - ids_mat)
for k, v in list(ESTAMPA_POR_MATERIAL.items()) + list(ESTAMPA_POR_PRENDA.items()): assert set(v) <= set(TODAS), (k, set(v) - set(TODAS))
assert 'lunares' not in ESTAMPA_POR_MATERIAL['Denim'] and 'camo' not in ESTAMPA_POR_MATERIAL['Naturales finos'] and 'toile' not in ESTAMPA_POR_MATERIAL['De punto']
ids_det = {d['id'] for d in DETALLES}
for k, v in DETALLE_POR_PRENDA.items(): assert set(v) <= ids_det, (k, set(v) - ids_det)

# ---------- los dibujos que usa, embebidos (la app no carga archivos sueltos) ----------
usados = {c['sil'] for c in CORTES} | {t['sil'] for t in TIROS} | {p['sil'] for p in PRENDAS} | {t['sil'] for p in PRENDAS for t in p['tipos']} | \
         {i['tex'] for g in MATERIALES for i in g['items']} | {'estampas/estampa_corazones', 'estampas/estampa_geometrico', 'estampas/estampa_rayas', 'estampas/estampa_lunares', 'estampas/estampa_floral', 'estampas/estampa_gamuza'} | {d['tex'] for d in DETALLES if d['tex']} | {i['sil'] for f in ESTAMPAS for i in f['items'] if i['sil']}
# los que ya viajan en DIS (app/diseno/diseno.json, de codigo/armar_diseno.py) no se repiten: la app busca en los dos
_h = open('app/index.html').read()
en_dis = set(json.loads(_h.split('\nconst DIS=')[1].split('\n')[0][:-1])['svg']) if '\nconst DIS=' in _h else set()
svg = {}
for k in sorted(usados - en_dis):
    t = open(f'app/siluetas/{k}.svg').read()
    svg[k] = re.sub(r'>\s+<', '><', t.strip())

TAX = dict(cortes=CORTES, tiros=TIROS, alias=ALIAS, prendas=PRENDAS, materiales=MATERIALES, detalles=DETALLES, estampas=ESTAMPAS,
           colores=[dict(id=i, n=n, hex=h) for i, n, h in COLORES], material_por_prenda=MATERIAL_POR_PRENDA,
           estampa_por_material=ESTAMPA_POR_MATERIAL, estampa_por_prenda=ESTAMPA_POR_PRENDA, detalle_por_prenda=DETALLE_POR_PRENDA, svg=svg)
os.makedirs('app/diseno', exist_ok=True)
js = json.dumps(TAX, ensure_ascii=False, separators=(',', ':'))
open('app/diseno/taxonomia.json', 'w').write(js)
h = open('app/index.html').read()
linea = 'const TAX=' + js + ';'
if '\nconst TAX=' in h:
    i = h.index('\nconst TAX=') + 1; j = h.index('\n', i); h = h[:i] + linea + h[j:]
else:
    i = h.index('\nconst DIS=') + 1; j = h.index('\n', i) + 1; h = h[:j] + linea + '\n' + h[j:]
open('app/index.html', 'w').write(h)
n_attr = len(CORTES) + len(TIROS) + sum(len(p['tipos']) for p in PRENDAS) + len(ids_mat) + len(DETALLES) + len(TODAS)
print(f'taxonomía: {len(PRENDAS)} prendas, {sum(len(p["tipos"]) for p in PRENDAS)} tipos, {len(CORTES)} cortes, {len(ids_mat)} materiales, '
      f'{len(DETALLES)} detalles, {len(TODAS)} estampas · {n_attr} atributos · {len(svg)} dibujos · {len(js)//1024} KB')
