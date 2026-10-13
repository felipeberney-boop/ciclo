"""Baja id, fecha y título de todos los posts de r/femalefashionadvice entre dos fechas, vía Arctic Shift.
Uso: python3 bajar_titulos_reddit.py salida.jsonl 2026  (un año por proceso; se pueden correr en paralelo).
Pagina semana por semana. Escribe JSONL reanudable. Los títulos crudos no se suben al repositorio."""
import json, os, sys, time, urllib.request, datetime as dt

OUT = sys.argv[1]
START = int(dt.datetime(int(sys.argv[2]), 1, 1, tzinfo=dt.timezone.utc).timestamp())
END = min(int(dt.datetime(int(sys.argv[2]) + 1, 1, 1, tzinfo=dt.timezone.utc).timestamp()), int(dt.datetime(2026, 10, 13, tzinfo=dt.timezone.utc).timestamp()))
API = 'https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=femalefashionadvice&limit=100&fields=created_utc,title,id'

seen, hechas = set(), set()
if os.path.exists(OUT):
    for l in open(OUT):
        p = json.loads(l)
        if 'semana' in p: hechas.add(p['semana'])
        else: seen.add(p['id'])

SEM = 7 * 86400
with open(OUT, 'a') as f:
  for ini in range(START, END, SEM):
    fin = min(ini + SEM, END)
    if ini in hechas: continue
    before = fin
    while before > ini:
        url = f'{API}&after={ini}&before={before}'
        for intento in range(8):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'ciclo-udesa-investigacion/1.0'}), timeout=90))
                if d.get('data') is not None: break
            except Exception as e:
                d = {'error': str(e)}
            time.sleep(10 * (intento + 1))
        else:
            sys.exit('falló: ' + str(d.get('error')))
        x = d['data']
        if not x: break
        nuevos = 0
        for p in x:
            if p['id'] not in seen:
                seen.add(p['id']); f.write(json.dumps(p, ensure_ascii=False) + '\n'); nuevos += 1
        f.flush()
        before = min(p['created_utc'] for p in x)
        if nuevos == 0: before -= 1
        if len(x) < 100: break
        time.sleep(1)
    f.write(json.dumps({'semana': ini}) + '\n'); f.flush()
    print(dt.datetime.utcfromtimestamp(ini).date(), len(seen), flush=True)
    time.sleep(1)
print('fin', len(seen))
