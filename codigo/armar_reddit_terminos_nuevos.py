"""Reddit para los atributos que sólo tenían búsqueda (17/11/2026).

Hasta acá la capa social cubría 14 atributos: los 25 términos de r/femalefashionadvice se habían bajado término por término
(4.404 posts) y los de r/malefashionadvice salieron de todos los títulos. Para sumar términos nuevos de mujeres se bajaron
todos los títulos de r/femalefashionadvice 2012–2025 con bajar_titulos_reddit.py (un proceso por año), igual que los de
hombres. Los títulos crudos no se suben al repositorio; sólo los conteos.

Uso (desde la raíz del repo):
  python3 codigo/armar_reddit_terminos_nuevos.py <carpeta con ffa_AAAA.jsonl> <carpeta con mfa_AAAA.jsonl>
Escribe datasets_procesados/reddit_terminos_nuevos_conteos.csv y datasets_procesados/reddit_terminos_nuevos.json, e imprime
las líneas para agregar a RDS (mujeres) y RDH (hombres) y el rk de cada atributo.

Regla, la misma de RDS y RDH: proporción de posts del año cuyo título nombra el término, media móvil centrada de 3 años
(en las puntas, ese año y el vecino), 2012–2025, llevada a 100 en su máximo. Entran sólo los términos con 100 posts o más
en 2012–2025 en ese subreddit. A diferencia de los 25 términos de antes (que buscaban el texto tal cual), acá se busca la
palabra entera, con plural, para que «tee» no cuente «between» ni «tank» cuente «tanker»."""
import json, sys, re, glob, csv, collections, datetime as dt

# atributo → (término que se muestra, expresión regular sobre el título en minúsculas)
TERMINOS = {
    'jmedio': ('straight leg jeans', r'\bstraight[- ]?leg\b|\bstraight jeans\b'),
    'capa': ('cape', r'\bcapes?\b'),
    'corset': ('corset', r'\bcorsets?\b'),
    'pantalones_short': ('shorts', r'\bshorts\b'),
    'faldas_mini': ('mini skirt', r'\bmini[- ]?skirts?\b'),
    'faldas_maxi': ('maxi skirt', r'\bmaxi[- ]?skirts?\b'),
    'vestidos_slip': ('slip dress', r'\bslip[- ]?dress(es)?\b'),
    'vestidos_camisero': ('shirt dress', r'(?<!t-)(?<!t )\bshirt[- ]?dress(es)?\b'),
    'vestidos_cruzado': ('wrap dress', r'\bwrap[- ]?dress(es)?\b'),
    'vestidos_tubo': ('bodycon', r'\bbodycon\b|\bsheath dress(es)?\b'),
    'vestidos_evase': ('a-line', r'\ba[- ]line\b'),
    'remeras_remera': ('t-shirt', r'\bt[- ]?shirts?\b|\btees?\b'),
    'remeras_musculosa': ('tank top', r'\btank[- ]?tops?\b|\btanks\b'),
    'camisas_blusa': ('blouse', r'\bblouses?\b'),
    'buzos_polera': ('turtleneck', r'\bturtle[- ]?necks?\b'),
    'buzos_cardigan': ('cardigan', r'\bcardigans?\b'),
    'abrigos_campera': ('bomber jacket', r'\bbombers?\b'),
    'calzado_zapatillas': ('sneakers', r'\bsneakers?\b'),
    'calzado_mocasines': ('loafers', r'\bloafers?\b'),
    'accesorios_tote': ('tote', r'\btotes?\b'),
    'enteritos_largo': ('jumpsuit', r'\bjumpsuits?\b'),
    'enteritos_corto': ('romper', r'\brompers?\b'),
    'enteritos_jardinero': ('overalls', r'\boveralls\b'),
    'fleece': ('fleece', r'\bfleeces?\b'),
    'cable': ('cable knit', r'\bcable[- ]?knits?\b'),
    'boucle': ('bouclé', r'\bboucl[eé]\b'),
    'algodon': ('cotton', r'\bcotton\b'),
    'popelina': ('poplin', r'\bpoplin\b'),
    'corduroy': ('corduroy', r'\bcorduroys?\b'),
    'lana': ('wool', r'\bwool(en|l?y)?\b'),
    'merino': ('merino', r'\bmerino\b'),
    'tweed': ('tweed', r'\btweed\b'),
    'lino': ('linen', r'\blinen\b'),
    'seda': ('silk', r'\bsilk(y)?\b'),
    'satenseda': ('satin', r'\bsatin\b'),
    'poliester': ('polyester', r'\bpolyester\b'),
    'elastano': ('spandex', r'\bspandex\b|\blycra\b|\belastane\b'),
    'neoprene': ('neoprene', r'\bneoprene\b|\bscuba\b'),
    'gasa': ('chiffon', r'\bchiffon\b'),
    'tul': ('tulle', r'\btulle\b'),
    'organza': ('organza', r'\borganza\b'),
    'bordado': ('embroidery', r'\bembroider(ed|y)\b'),
    'volados': ('ruffles', r'\bruffle[sd]?\b|\bruffly\b'),
    'tachas': ('studded', r'\bstudded\b'),
    'cutouts': ('cut-out', r'\bcut[- ]?outs?\b'),
    'plisado': ('pleated', r'\bpleat(ed|s)?\b'),
    'acolchado': ('quilted', r'\bquilted\b|\bpuffers?\b'),
    'flecos': ('fringe', r'\bfringed?\b'),
    'pedreria': ('sequins', r'\bsequin(s|ned)?\b|\bbeaded\b'),
    'camo': ('camo', r'\bcamo\b|\bcamouflage\b'),
    'tiedye': ('tie-dye', r'\btie[- ]?dye[ds]?\b'),
    'espiga': ('herringbone', r'\bherringbone\b'),
}
A = list(range(2012, 2026))

def contar(carpeta, pref):
    posts = {}
    for f in sorted(glob.glob(f'{carpeta}/{pref}_*.jsonl')):
        for l in open(f):
            p = json.loads(l)
            if 'id' in p: posts[p['id']] = p
    tot = collections.Counter(); n = collections.Counter()
    R = {k: re.compile(v[1]) for k, v in TERMINOS.items()}
    for p in posts.values():
        y = dt.datetime.fromtimestamp(p['created_utc'], dt.timezone.utc).year
        if y not in A: continue
        tot[y] += 1; t = (p.get('title') or '').lower()
        for k, r in R.items():
            if r.search(t): n[(k, y)] += 1
    return tot, n

def serie(tot, n):
    out, fuera = {}, {}
    for k, (term, _) in TERMINOS.items():
        total = sum(n[(k, y)] for y in A)
        if total < 100: fuera[term] = total; continue
        R = {y: n[(k, y)] / tot[y] for y in A}
        m = {y: sum(R[z] for z in (y - 1, y, y + 1) if z in R) / len([z for z in (y - 1, y, y + 1) if z in R]) for y in A}
        mx = max(m.values())
        out[term] = {'i': [None] * (2012 - 2004) + [round(100 * m[y] / mx, 1) for y in A], 'pk': max(A, key=lambda y: m[y]), 'n': total}
    return out, fuera

ffa, mfa = sys.argv[1], sys.argv[2]
tf, nf = contar(ffa, 'ffa'); tm, nm = contar(mfa, 'mfa')
print('posts mujeres 2012–2025:', sum(tf.values()), dict(sorted(tf.items())))
print('posts hombres 2012–2025:', sum(tm.values()))
with open('datasets_procesados/reddit_terminos_nuevos_conteos.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['atributo', 'termino', 'expresion', 'subreddit', 'anio', 'posts', 'posts_totales_anio'])
    for k, (term, rx) in TERMINOS.items():
        for sub, tot, n in (('femalefashionadvice', tf, nf), ('malefashionadvice', tm, nm)):
            for y in A: w.writerow([k, term, rx, sub, y, n[(k, y)], tot[y]])
M, fM = serie(tf, nf); H, fH = serie(tm, nm)
json.dump({'regla': 'posts cuyo título nombra el término (palabra entera) / posts del año, media centrada de 3 años, 100 = su máximo 2012–2025; sólo términos con 100 posts o más',
           'terminos': {k: v[0] for k, v in TERMINOS.items()}, 'expresiones': {k: v[1] for k, v in TERMINOS.items()},
           'mujeres': M, 'hombres': H, 'fuera_mujeres': fM, 'fuera_hombres': fH},
          open('datasets_procesados/reddit_terminos_nuevos.json', 'w'), ensure_ascii=False, indent=1)
print('mujeres entran', len(M), 'fuera', fM)
print('hombres entran', len(H), 'fuera', fH)
