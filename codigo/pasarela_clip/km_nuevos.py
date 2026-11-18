"""pn/pm de la pasarela para el K-means con la serie corregida.
A (la que entra): mismas ventanas que antes — nivel = media 2022–23 / máximo hasta 2023; momento = media 2021–23 / media 2018–20 − 1.
B (comparación): ventanas de la búsqueda — nivel = media 2023–24 / máximo hasta 2024; momento = media 2023–24 / media 2020–21 − 1."""
import json
P = json.load(open('datos/pasarela_2025.json'))
FILA = {'Jeans baggy': 'denim', 'Jeans rectos': 'denim', 'Jeans skinny': 'denim', 'Buzo / hoodie': 'buzo', 'Floral': 'floral',
        'Lunares': 'lunares', 'Cuero': 'cuero', 'Animal print': 'animal print', 'Kimono': 'kimono', 'Capa': 'capa',
        'Trench': 'trench', 'Encaje': 'encaje', 'Cargo': 'militar', 'Cuadros': 'cuadros', 'Piel': 'piel', 'Blazer oversize': 'blazer', 'Y2K': 'y2k'}
m = lambda v, a: sum(v[str(y)] for y in a) / len(a)
A, B = {}, {}
for fila, vk in FILA.items():
    v = P[vk]['v']; hasta = lambda y: max(v[str(a)] for a in range(2010, y + 1))
    A[fila] = {'pn': round(m(v, (2022, 2023)) / hasta(2023), 3), 'pm': round(m(v, (2021, 2022, 2023)) / m(v, (2018, 2019, 2020)) - 1, 3),
               'pico_pas': max(range(2010, 2024), key=lambda y: v[str(y)])}
    if str(2024) in v:
        B[fila] = {'pn': round(m(v, (2023, 2024)) / hasta(2024), 3), 'pm': round(m(v, (2023, 2024)) / m(v, (2020, 2021)) - 1, 3),
                   'pico_pas': max(range(2010, 2025), key=lambda y: v[str(y)])}
json.dump(A, open('datos/km_A.json', 'w'), indent=1); json.dump(B, open('datos/km_B.json', 'w'), indent=1)
print('A', A); print('B (sólo los que se extienden a 2024)', list(B))
