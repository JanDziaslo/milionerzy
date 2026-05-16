import json

def wczytaj_pytania(sciezka):
    with open(sciezka, "r", encoding="utf-8") as f:
        return json.load(f)

def wczytaj_odpowiedzi(sciezka):
    with open(sciezka, "r", encoding="utf-8") as f:
        return json.load(f)