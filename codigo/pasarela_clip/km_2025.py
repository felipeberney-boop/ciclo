"""pn/pm de la pasarela con 2024–2025 (18/11, entra al modelo).
Ventanas corridas dos años: nivel = media 2024–25 / máximo 2010–2025; momento = media 2023–25 / media 2020–22 − 1.
Lunares y piel no llegan a 2025 (intervalo ancho) y conservan las de antes: 2022–23 y 2021–23 contra 2018–20.
Uso, desde la raíz: python3 codigo/pasarela_clip/km_2025.py  → datasets_procesados/pasarela_clip/km_C_2025.json"""
import json
P = json.load(open('datasets_procesados/pasarela_clip/pasarela_2025.json'))
FILA = {'Jeans baggy': 'denim', 'Jeans rectos': 'denim', 'Jeans skinny': 'denim', 'Buzo / hoodie': 'buzo', 'Floral': 'floral',
        'Lunares': 'lunares', 'Cuero': 'cuero', 'Animal print': 'animal print', 'Kimono': 'kimono', 'Capa': 'capa',
        'Trench': 'trench', 'Encaje': 'encaje', 'Cargo': 'militar', 'Cuadros': 'cuadros', 'Piel': 'piel', 'Blazer oversize': 'blazer', 'Y2K': 'y2k'}
m = lambda v, a: sum(v[str(y)] for y in a) / len(a)
C = {}
for f, k in FILA.items():
    v = P[k]['v']; u = max(int(a) for a in v)
    hasta = max(v[str(a)] for a in range(2010, u + 1))
    C[f] = {'pn': round(m(v, (u - 1, u)) / hasta, 3), 'pm': round(m(v, (u - 2, u - 1, u)) / m(v, (u - 5, u - 4, u - 3)) - 1, 3),
            'pico_pas': max(range(2010, u + 1), key=lambda y: v[str(y)])}
json.dump(C, open('datasets_procesados/pasarela_clip/km_C_2025.json', 'w'), indent=1)
print(C)
