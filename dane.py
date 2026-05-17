import json


def wczytaj_pytania(sciezka):
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{sciezka}'.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Błąd: Plik '{sciezka}' zawiera nieprawidłowy format JSON: {e}")
        exit(1)
    except Exception as e:
        print(f"Błąd: Nie udało się wczytać pliku '{sciezka}': {e}")
        exit(1)


def wczytaj_odpowiedzi(sciezka):
    try:
        with open(sciezka, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{sciezka}'.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Błąd: Plik '{sciezka}' zawiera nieprawidłowy format JSON: {e}")
        exit(1)
    except Exception as e:
        print(f"Błąd: Nie udało się wczytać pliku '{sciezka}': {e}")
        exit(1)
