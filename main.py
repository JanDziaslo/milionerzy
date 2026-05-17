import random
import json
from dane import *
from datetime import datetime


def main():
    # pobierz imię i nazwisko gracza
    while True:
        player_name = input("Podaj imię i nazwisko: ").strip()
        if player_name:
            break
        print("Proszę podać niepuste imię i nazwisko.")

    pytania = wczytaj_pytania("pytania.json")
    odpowiedzi = wczytaj_odpowiedzi("odpowiedzi.json")

    # losowanie pytania
    wszystkie_pytania = []
    for kategoria, pytania_lista in pytania.items():
        for p in pytania_lista:
            p_copy = p.copy()
            p_copy['kategoria'] = kategoria
            wszystkie_pytania.append(p_copy)

    wylosowane_pytania = random.sample(wszystkie_pytania, min(12, len(wszystkie_pytania)))

    score = 0
    # skala nagród jak w Milionerach (pozycja 1 => 1000 za 1 poprawną odpowiedź)
    nagrody = [1000, 2000, 5000, 10000, 15000, 25000, 50000, 75000, 125000, 250000, 500000, 1000000]
    for i, wylosowane in enumerate(wylosowane_pytania, 1):
        # znajdź treść poprawnej odpowiedzi PRZED tasowaniem
        cat_list = odpowiedzi.get(wylosowane['kategoria'], [])
        correct_entry = next((e for e in cat_list if e.get('id') == wylosowane.get('id')), None)
        correct_tresc = None
        if correct_entry:
            orig_id = correct_entry.get('odpowiedz')
            orig_ans = next((a for a in wylosowane['odpowiedzi'] if a.get('id') == orig_id), None)
            correct_tresc = orig_ans['tresc'] if orig_ans else None

        # losowa kolejność odpowiedzi
        random.shuffle(wylosowane['odpowiedzi'])

        # ponowne przypisanie id odpowiedzi (1, 2, 3, 4) po przetasowaniu
        for idx, odp in enumerate(wylosowane['odpowiedzi'], 1):
            odp['id'] = idx

        # znajdź nową pozycję poprawnej odpowiedzi po tasowaniu
        correct_num = None
        if correct_tresc:
            for odp in wylosowane['odpowiedzi']:
                if odp['tresc'] == correct_tresc:
                    correct_num = odp['id']
                    break

        print(f"--- Pytanie {i} ---")
        print(f"Kategoria: {wylosowane['kategoria'].replace('_', ' ')}")
        print(f"Pytanie: {wylosowane['pytanie']}")
        print(f"Trudność: {wylosowane.get('trudnosc', '?')}")
        print("Odpowiedzi:")
        for odp in wylosowane['odpowiedzi']:
            print(f"  {odp['id']}. {odp['tresc']}")

        # pobierz i sprawdz odpowiedz od uzytkownika
        while True:
            ans = input("Podaj numer odpowiedzi: ").strip()

            if not ans.isdigit():
                print("Proszę wpisać numer odpowiedzi.")
                continue

            ans_num = int(ans)
            available_ids = [o['id'] for o in wylosowane['odpowiedzi']]
            if ans_num not in available_ids:
                print(f"Nieprawidłowy numer. Dostępne numery: {available_ids}")
                continue
            break

        if correct_num is None:
            print("Brak wzorca odpowiedzi dla tego pytania (brak wpisu w odpowiedzi.json).\n")
        elif ans_num == correct_num:
            score += 1
            # ustal aktualną nagrodę na podstawie liczby poprawnych odpowiedzi
            current_prize = nagrody[min(score - 1, len(nagrody) - 1)]
            print(f"Dobra odpowiedź! Aktualna nagroda: {current_prize} PLN\n")
        else:
            # jeśli zła odpowiedź, pokaż prawidłową i zakończ grę
            last_prize = nagrody[score - 1] if score > 0 else 0
            print(f"Zła odpowiedź. Prawidłowy numer to {correct_num}. Zdobyte: {last_prize} PLN\n")
            break

    final_prize = nagrody[score - 1] if score > 0 else 0
    print(f"Twój wynik: {score}/{len(wylosowane_pytania)} — Zdobyte: {final_prize} PLN")

    # zapis wyniku do pliku wyniki.json. Specjalne formatowanie do daty żeby pokazywalo tez dokladny czas a nie date
    result_entry = {
        "Imie i nazwisko": player_name,
        "Poprawne odpowiedzi": score,
        "Nagroda": final_prize,
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open("wyniki.json", "r", encoding="utf-8") as f:
            results = json.load(f)
            if not isinstance(results, list):
                results = []
    except Exception:
        results = []

    results.append(result_entry)
    try:
        with open("wyniki.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("Wynik zapisany do pliku wyniki.json")
    except Exception as e:
        print(f"Nie udało się zapisać wyniku: {e}")


if __name__ == "__main__":
    main()
