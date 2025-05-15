# Cel programu i kontekst zastosowania:
# Program służy do generowania losowej sekwencji DNA w formacie FASTA, powszechnie wykorzystywanego w bioinformatyce.
# Pozwala użytkownikowi wygenerować sekwencję o zadanej długości, wstawić imię w losowe miejsce,
# zapisać wynik do pliku oraz obliczyć statystyki dotyczące zawartości nukleotydów.

import random  # biblioteka do losowania
import os  # biblioteka do operacji na plikach


# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length):
    # Lista nukleotydów
    nucleotides = ['A', 'C', 'G', 'T']
    # Zwraca losową sekwencję o zadanej długości
    return ''.join(
        random.choices(nucleotides, k=length))  # Losowy wybór znaków z listy nukleotydów i ich połączenie w string


# Funkcja obliczająca statystyki zawartości nukleotydów
def calculate_statistics(sequence):
    length = len(sequence)  # Obliczenie długości sekwencji
    # Obliczanie procentowej zawartości każdego nukleotydu
    stats = {nuc: sequence.count(nuc) / length * 100 for nuc in
             'ACGT'}  # Tworzenie słownika z procentową zawartością A, C, G, T
    # Sumaryczna zawartość C i G
    cg_content = stats['C'] + stats['G']  # Dodanie zawartości C i G
    # Sumaryczna zawartość A i T
    at_content = stats['A'] + stats['T']  # Dodanie zawartości A i T
    # Stosunek CG/AT
    cg_at_ratio = cg_content / at_content if at_content != 0 else 0  # Obliczenie stosunku CG/AT z zabezpieczeniem przed dzieleniem przez 0
    return stats, cg_content, cg_at_ratio  # Zwrócenie statystyk, zawartości CG i stosunku CG/AT


# Główna funkcja programu
def main():
    # --- Pobieranie danych od użytkownika ---

    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))
    # MODIFIED (dodanie walidacji długości sekwencji - nie może być ujemna ani zerowa):
    while True:  # Pętla zewnętrzna umożliwiająca wielokrotne generowanie sekwencji
        while True:  # Pętla wewnętrzna do walidacji długości sekwencji
            try:
                length = int(input(
                    "Podaj długość sekwencji: "))  # Pobranie długości sekwencji od użytkownika i konwersja na liczbę
                if length > 0:  # Sprawdzenie, czy długość jest większa od zera
                    break  # Wyjście z pętli, jeśli dane są poprawne
                else:
                    print("Długość musi być większa od zera.")  # Komunikat o błędnej długości
            except ValueError:
                print("Proszę podać poprawną liczbę całkowitą.")  # Obsługa błędu konwersji na int

        # Pobranie ID, opisu i imienia
        seq_id = input("Podaj ID sekwencji: ")  # Pobranie ID sekwencji od użytkownika
        description = input("Podaj opis sekwencji: ")  # Pobranie opisu sekwencji od użytkownika
        name = input("Podaj imię: ")  # Pobranie imienia od użytkownika

        # --- Generowanie sekwencji DNA ---
        sequence = generate_dna_sequence(length)  # Generowanie losowej sekwencji DNA

        # Wstawienie imienia w losowe miejsce (litery imienia nie wpływają na statystyki)
        insert_position = random.randint(0, len(sequence))  # Wylosowanie pozycji do wstawienia imienia w sekwencji
        sequence_with_name = sequence[:insert_position] + name + sequence[
                                                                 insert_position:]  # Wstawienie imienia do sekwencji

        # --- Zapis do pliku FASTA ---

        filename = f"{seq_id}.fasta"  # Utworzenie nazwy pliku na podstawie ID
        with open(filename, 'a') as file:  # Otwarcie pliku do dopisania danych
            file.write(f">{seq_id} {description}\n")  # Zapisanie nagłówka FASTA do pliku

            # ORIGINAL:
            # file.write(sequence_with_name + "\n")
            # MODIFIED (dzielenie sekwencji na linie po 60 znaków dla czytelności i zgodności z FASTA):
            for i in range(0, len(sequence_with_name), 60):  # Iteracja po sekwencji co 60 znaków
                file.write(sequence_with_name[i:i + 60] + "\n")  # Zapisanie fragmentu sekwencji do pliku

        print(f"Sekwencja została zapisana do pliku {filename}")  # Informacja o zapisaniu sekwencji

        # --- Obliczanie i wyświetlanie statystyk ---
        stats, cg_content, cg_at_ratio = calculate_statistics(
            sequence)  # Obliczenie statystyk dla oryginalnej sekwencji (bez imienia)

        print("Statystyki sekwencji:")  # Nagłówek sekcji statystyk
        for nuc in 'ACGT':  # Iteracja po nukleotydach
            print(f"{nuc}: {stats[nuc]:.1f}%")  # Wyświetlenie procentowej zawartości danego nukleotydu
        print(f"%CG: {cg_content:.1f}")  # Wyświetlenie zawartości CG
        print(f"Stosunek CG/AT: {cg_at_ratio:.2f}")  # Wyświetlenie stosunku CG/AT

        # MODIFIED
        # Pytanie, czy użytkownik chce wprowadzić kolejną sekwencję
        continue_choice = input(
            "Czy chcesz wygenerować kolejną sekwencję? (tak/nie): ").strip().lower()  # Pobranie decyzji użytkownika
        if continue_choice != 'tak':  # Sprawdzenie, czy użytkownik chce kontynuować
            print("Dziękujemy za użycie programu!")  # Pożegnanie użytkownika
            break  # Wyjście z pętli głównej i zakończenie programu


# Wywołanie funkcji głównej
if __name__ == "__main__":  # Sprawdzenie, czy plik został uruchomiony bezpośrednio
    main()  # Wywołanie funkcji main()
