import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, Button, Label
from tkinter.font import Font
from mutagen.id3 import ID3


class App:
    def __init__(self, master, button_width=12, button_height=2):
        # Wygląd głównego okna
        self.master = master
        self.master.title("---Tagowarka--- PG ---")  # nazwa w belce na górze
        self.master.geometry('800x600')  # wielkość okna
        # Tworzenie obiektu stylu
        self.default_style = ttk.Style()
        self.dark_style = ttk.Style()
        self.dark_style.theme_use('clam')  # tryb ciemny
        self.current_style = 'default'  # tryb podstawowy
        self.button_font = Font(size=10)  # wielkość czcionki w przycisku
        self.font = ("Arial", 12)
        # ----- Tworzenie przycisków ----- #
        # przycisk skórki
        self.toggle_button = ttk.Button(self.master, text="Zmień kolor", command=self.toggle_style, )
        self.toggle_button.pack()
        # przycisk wybierz pliki
        self.choose_files_button = Button(master, text="Wybierz pliki", command=self.choose_files,
                                          width=button_width, height=button_height, font=self.button_font)
        self.choose_files_button.pack(side="right", pady=5)
        # przycisk zamknij
        self.quit_button = tk.Button(master, text="Zamknij", command=master.quit, width=button_width,
                                     height=button_height, font=self.button_font)
        self.quit_button.pack(side="right", pady=5)
        # przycisk TAGUJ
        self.tag_button = Button(master, text="TAGUJ", command=self.tag_files,
                                 width=button_width, height=button_height, font=self.button_font)
        self.tag_button.pack(side="right", pady=5)
        # ---   # Ułożenie przycisków
        self.toggle_button.pack(side=tk.LEFT, anchor="nw", padx=10, pady=10)
        self.quit_button.pack(side="bottom", anchor="se", padx=10, pady=10)
        self.choose_files_button.pack(side="right", anchor="ne", padx=10, pady=10)
        # pole tekstowe z wybranym folderem
        self.folder_path = StringVar()
        self.folder_path_label = Label(master, textvariable=self.folder_path, font=self.font)
        self.folder_path_label.pack(pady=10)
        # tworzenie listy plików
        self.file_listbox = ttk.Treeview(master, columns=("Tags",))
        self.file_listbox.heading("#0", text="Pliki")
        self.file_listbox.heading("Tags", text="Tagi")
        self.file_listbox.column("#0", width=350)
        self.file_listbox.column("Tags", width=100)
        self.file_listbox.pack(side="top", padx=10, pady=10)
        # ----- Kolory w programie -----
        self.file_listbox.tag_configure("red", background="red")
        self.status_label = None

    # ----- Moduł zmiany koloru -----
    def toggle_style(self):
        if self.current_style == 'default':
            # Zmień styl na ciemny
            self.dark_style.theme_use('clam')
            self.master.configure(background='#333')
            self.current_style = 'dark'
        else:
            # Zmień styl na domyślny
            self.default_style.theme_use('winnative')
            self.master.configure(background='white')
            self.current_style = 'default'

    # ----- Działanie przycisku Wybierz pliki -----
    def choose_files(self):
        files = filedialog.askopenfilenames()  # Zwraca listę wybranych plików
        if files:
            # Wyczyść istniejące wpisy w tabeli
            self.file_listbox.delete(*self.file_listbox.get_children())
            for file_path in files:
                file_name = os.path.basename(file_path)
                # Dodaj wybrany plik do tabeli
                self.file_listbox.insert("", "end", text=file_name, values=("FILE",))

    def update_status_bar(self, text):
        if self.status_label is not None:
            self.status_label.config(text=text)
        else:
            self.status_label = Label(self.master, text=text, font=("Arial", 10))
            self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)
            self.master.update_idletasks()  # Force GUI update

    def tag_files(self):
        self.update_status_bar("Odczytywanie tagów...")
        # słownik mapujący nazwy tagów na swoje opisy
        tags_dict = {
            "TIT2": "Tyt=",  # Nazwa utworu[okno do wpisania]
            "TALB": "Pta=",  # Nazwa płyty[okno do wpisania]
            "TPE2": "Wyk=",  # Wykonawca[okno do wpisania]
            "TPE1": "Sol=",  # Solista[okno do wpisania]
            "TCOM": "Kom=",  # Kompozytor[okno do wpisania]
            "TEXT": "Aut=",  # Autor[okno do wpisania]
            "TPUB": "Wyd=",  # Wydawca[okno do wpisania]
            "TYER": "Rok=",  # 1000 - rok
            "TOFN": "PLK=",  # TEST - DOBROMIR MAKOWSKI - CZAS UCIEKA - oryginalna nazwa pliku
            "TIME": "Out=",  # 03:12.722 - całkowity czas utworu
        }

        # ...

        for filename in self.file_listbox.get_children():
            filename = self.file_listbox.item(filename, "text")
            if filename.endswith(".mp3"):
                filepath = os.path.join(self.folder_path.get(), filename)
                # Użyj kodowania utf-8 przy otwieraniu pliku
                try:
                    tags = ID3(filepath, translate=False, v2_version=3, encoding='utf-8')
                    tags_string = ""
                    # przeiteruj po słowniku i dodaj opis i wartość taga do stringa
                    for tag_name, tag_description in tags_dict.items():
                        if tag_name in tags:
                            tag_value = tags[tag_name].text[0].lstrip()
                            tags_string += f"{tag_description}{tag_value}\n"  # dodanie opisu taga i wartości do stringa
                    # zapisanie pliku *.dat (bez rozszerzenia mp3)
                    filename_without_extension = os.path.splitext(filename)[0]
                    dat_filename = f"{filename_without_extension}.dat"
                    with open(os.path.join(self.folder_path.get(), dat_filename), "w", encoding="utf-8") as f:
                        f.write(tags_string)
                except Exception as e:
                    self.update_status_bar(f"Błąd podczas tagowania: {str(e)}")

        # ...

        # wyświetla informacje na pasku programu
        self.update_status_bar("Tagowanie zakończone.")


if __name__ == '__main__':
    # Tworzenie głównego okna
    root = tk.Tk()
    # Tworzenie aplikacji
    app = App(root)
    # Uruchomienie pętli głównej programu
    root.mainloop()
