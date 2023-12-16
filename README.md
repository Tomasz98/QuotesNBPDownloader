
---

# Aplikacja do Zarządzania Danymi Walutowymi

Aplikacja do zarządzania danymi walutowymi służy do pobierania, 
przetwarzania, zapisywania i analizowania informacji o kursach walut.
Dane są pobierane z API Narodowego Banku Polskiego, przetwarzane, a następnie zapisywane w bazie danych. 
Dodatkowo, aplikacja umożliwia generowanie statystyk i zapisywanie danych do plików CSV.

## Funkcje

- Pobieranie danych o kursach walut
- Przetwarzanie i zapisywanie danych do bazy danych
- Generowanie statystyk
- Zapis danych do plików CSV

## Konfiguracja

Aplikacja korzysta z Docker i docker-compose do łatwej konfiguracji i uruchomienia.

### Wymagania

- Docker
- docker-compose

### Instalacja i Uruchomienie

1. **Klonowanie Repozytorium**
   Sklonuj repozytorium do lokalnego katalogu:
   ```bash
   git clone 
   ```

2. **Uruchomienie za pomocą docker-compose**
   Użyj `docker-compose` do zbudowania i uruchomienia kontenerów:
   ```bash
   docker-compose build
   docker-compose up
   ```

## Użycie

Po uruchomieniu kontenerów, aplikacja będzie dostępna i gotowa do użycia. 
Aplikacja cyklicznie pobiera i zapisuje dane do pliku all_currency_data.csv o 12:00 każdego dnia. 
Można też użyć aplikacji przez wykonanie skryptu `main.py` z odpowiednimi flagami:


- `--currency`: Wybór walut do analizy (np. `eur_pln`, `usd_pln`)
- `--days`: Liczba dni do analizy (np. `30`)
- `--stat`: Flaga do generowania statystyk (np. `True`)

### Przykłady Komend

- Pobieranie i analiza danych dla EUR/PLN z ostatnich 30 dni:
  ```bash
  python main.py --currency "eur_pln" --days 30
  ```
  - Pobieranie i analiza danych dla kilku par walut EUR/PLN  USD/PLN  z ostatnich 30 dni (separator spacja):
  ```bash
  python main.py --currency "eur_pln usd_pln" --days 30
  ```
- Generowanie statystyk dla wszystkich walut z ostatnich 10 dni:
  ```bash
  python main.py --currency "*" --days 10 --stat "True"
  ```

## Licencja

MIT


