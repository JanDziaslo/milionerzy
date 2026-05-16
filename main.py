import random
from dane import *

pytania = wczytaj_pytania("pytania.json")
odpowiedzi = wczytaj_odpowiedzi("odpowiedzi.json")

# Losowanie pytania
wszystkie_pytania = []
for kategoria, pytania_lista in pytania.items():
    for p in pytania_lista:
        p['kategoria'] = kategoria
        wszystkie_pytania.append(p)

wylosowane_pytania = random.sample(wszystkie_pytania, min(12, len(wszystkie_pytania)))

for i, wylosowane in enumerate(wylosowane_pytania, 1):
    print(f"--- Pytanie {i} ---")
    print(f"Kategoria: {wylosowane['kategoria'].replace('_', ' ')}")
    print(f"Pytanie: {wylosowane['pytanie']}")
    print(f"Trudność: {wylosowane['trudnosc']}")
    print("Odpowiedzi:")
    for odp in wylosowane['odpowiedzi']:
        print(f"  {odp['id']}. {odp['tresc']}")
    print()