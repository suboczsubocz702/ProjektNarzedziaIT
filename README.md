Konwerter Danych (JSON, YAML, XML)
Ten projekt to aplikacja w języku Python do konwersji danych między formatami JSON, YAML i XML. Oferuje zarówno interfejs wiersza poleceń (CLI), jak i graficzny (GUI) oparty na PyQt5. Projekt jest hostowany na GitHubie, z automatycznym budowaniem plików wykonywalnych (.exe) za pomocą GitHub Actions.
Spis treści

1. Funkcjonalności
2. Wymagania
3. Instalacja
4. Użycie
    - Wersja CLI
    - Wersja GUI


5. Struktura repozytorium
6. Budowanie plików EXE
7. GitHub Actions
8. Testowanie
9. Obsługa błędów
10. Autor

1. Funkcjonalności

Konwersja danych między formatami: 
    JSON, 
    YAML (.yaml lub .yml), 
    XML.
Wersja CLI (project.py): 
    Przyjmuje ścieżki do pliku wejściowego i wyjściowego jako argumenty wiersza poleceń.
Wersja GUI (project_gui.py): 
    Intuicyjny interfejs graficzny z wyborem plików i asynchroniczną konwersją.
Obsługa błędów: 
    Walidacja rozszerzeń, sprawdzanie istnienia plików, obsługa nieprawidłowej składni.
    Automatyczne budowanie plików .exe za pomocą GitHub Actions.

2. Wymagania

- Python 3.8 lub nowszy
- Zależności Pythona:
- pyyaml (do obsługi YAML)
- lxml (do obsługi XML)
- PyQt5 (do GUI)
- pyinstaller (do budowania .exe)


System operacyjny: Windows (dla budowania .exe i uruchamiania GUI)
Git (do klonowania repozytorium)
PowerShell (do uruchamiania skryptu instalacyjnego)

3. Instalacja

Sklonuj repozytorium:
git clone [https://github.com/<twoje-nazwa-uzytkownika>/<nazwa-repozytorium>.git](https://github.com/suboczsubocz702/ProjektNarzedziaIT/)
cd ProjektNarzedziaIT


Zainstaluj zależności za pomocą skryptu PowerShell:
.\installResources.ps1

Skrypt instaluje pyyaml, lxml, PyQt5 i pyinstaller.

(Opcjonalnie) Zainstaluj zależności ręcznie:
pip install pyyaml lxml PyQt5 pyinstaller



4. Użycie
Wersja CLI
Plik project.py umożliwia konwersję danych przez wiersz poleceń.
Składnia:
python project.py <plik_wejsciowy> <plik_wyjsciowy>


<plik_wejsciowy>: Plik w formacie .json, .yaml, .yml lub .xml.
<plik_wyjsciowy>: Docelowy plik w formacie .json, .yaml, .yml lub .xml.

Przykłady:

Konwersja JSON na YAML:python project.py test.json output.yaml


Konwersja XML na JSON:python project.py test.xml output.json



Uruchomienie EXE:
dist\project.exe test.json output.yaml

Wersja GUI
Plik project_gui.py uruchamia interfejs graficzny.
Uruchomienie:
python project_gui.py

Można również pobrać plik z releases i uruchomić jako .exe

5. Instrukcja:

Kliknij "Wybierz plik wejściowy" i wybierz plik (.json, .yaml, .yml, .xml).
Kliknij "Wybierz plik wyjściowy" i określ nazwę oraz format pliku wyjściowego.
Kliknij "Konwertuj", aby wykonać konwersję.
Status konwersji pojawi się w oknie (np. "Konwersja zakończona pomyślnie" lub komunikat błędu).

Uruchomienie EXE:
dist\project_gui.exe

Struktura repozytorium
├── .github/
│   └── workflows/
│       └── build.yml       # Workflow GitHub Actions do budowania .exe
├── installResources.ps1    # Skrypt PowerShell do instalacji zależności
├── project.py              # Wersja CLI (obsługa JSON, YAML, XML)
├── project_gui.py          # Wersja GUI (PyQt5, asynchroniczna konwersja)
├── README.md               # Dokumentacja projektu

6. Budowanie plików EXE

Lokalnie:

- Wersja CLI:pyinstaller --onefile project.py


- Wersja GUI (bez konsoli):pyinstaller --onefile --noconsole project_gui.py


Wynik: Pliki dist\project.exe i dist\project_gui.exe.


Automatyczne budowanie:

- GitHub Actions buduje pliki .exe automatycznie po pushu na branch main, co tydzień (w niedzielę o północy) lub ręcznie przez workflow_dispatch.
- Artefakty (data-converter-cli i data-converter-gui) są dostępne w zakładce Actions w repozytorium.



7. GitHub Actions
Workflow (build.yml) wykonuje następujące kroki:

- Pobiera kod z repozytorium.
- Konfiguruje Pythona (3.x).
- Instaluje zależności za pomocą installResources.ps1.
- Buduje pliki .exe dla project.py i project_gui.py.
- Przesyła artefakty (data-converter-cli, data-converter-gui) za pomocą actions/upload-artifact@v4.

Uruchomienie ręczne:

W zakładce Actions wybierz workflow i kliknij "Run workflow".

Debugowanie:

Sprawdź logi w Actions, aby zweryfikować poprawność instalacji zależności i budowania.

8 . Testowanie

Przykładowe pliki testowe:

test.json:{
    "name": "Test",
    "value": 123,
    "items": [1, 2, 3]
}


test.yaml:name: Test
value: 123
items:
  - 1
  - 2
  - 3


test.xml:<?xml version="1.0" encoding="UTF-8"?>
<root>
    <name>Test</name>
    <value>123</value>
    <items>
        <item>1</item>
        <item>2</item>
        <item>3</item>
    </items>
</root>




9. Przypadki testowe:

Konwersja między wszystkimi formatami (np. JSON → YAML, XML → JSON).
Test błędów: nieistniejący plik, nieprawidłowa składnia, nieobsługiwane rozszerzenie.


Uruchomienie testów:
python project.py test.json output.yaml
python project_gui.py



Obsługa błędów

CLI:
Nieprawidłowe rozszerzenie: "Plik wejściowy musi mieć jedno z rozszerzeń: .json, .yaml, .yml, .xml"
Nieistniejący plik: "Plik wejściowy 'nazwa' nie istnieje"
Błędy składni: "Nieprawidłowa składnia JSON/YAML/XML w nazwa_pliku"


GUI:
Komunikaty o błędach wyświetlane w oknie (np. "Błąd: Nieprawidłowa składnia JSON").
Blokada przycisku "Konwertuj" podczas asynchronicznej operacji.



10. Autor

Mateusz Subocz 51935
Kontakt: suboczmateusz08@gmail.com

