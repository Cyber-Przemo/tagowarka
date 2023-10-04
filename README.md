# Tagowarka mp3
Pierwszy mały projekcik, mający na celu wyciągnięcie tagów z pliku mp3 do pliku *.dat (plik tekstowy)

Tagi ID3 są przyporządkowane opisom w utworzonym złowniku.

W programie:
1. wybieramy ścieżkę do folderu
2. Automatyczny odczyt plików,
3. Wyciągnięcie tagów 
4. Utworzenie pliku z rozszerzeniem *.DAT
5. Zapisanie tagów w pliku
5. Przejście do kolejnego pliku 
6. Zakończenie działania

# Rozwój programu:

- Dodanie do pliku skrótu tagów bez wpisu, (wg katalogu dunamixa) 
- Wybieranie pojedyńczych plików
- Po wskazaniu ścieżki folderu, pokazać listę z plikami mp3 które mają już wyeksportowane tagi do pliku
- Wybór plików które tych tagów nie mają eksportowanych
- Dodanie wykonania obwiedni plików, i zapisanie ich w osobnym pliku *.OBW
- Edycja tagów w okienku
- Dodanie większej ilości tagów
- Eksport tagów do pliku pod program DynaMIX
-
- Zgrywanie mp3 z płyt
- Pobieranie danych (opisu z sewrwerów)
- Podział działających funkcji na moduły, aby móc rozwijać program 
- Edycja pliku mp3 (obwiedni) wskazanie początku, końca, czy mixów

# Daleka przyszłość

- stworzenie aplikacji webowej do sprawdzenia tagów i skatalogowania plików mp3 dostępnych na dysku (które są z tagami a które bez. wg podziału, z wyszukiwarką itp


# OPIS PLIKÓW

Plik --tagowarka-- ver-01.py - działający.

Plik --tagowarka- ver-02.py
rozszerzony.

Po uruchomieniu programu, wybieramy Wybierz pliki,
Pliki wyświewtlają się w tabeli na liście

Klikamy przycisk TAGUJ
- Program powinien odczytać tagi, zapisać je do pliku tekstowego dat, ale tak się nie dzieje
