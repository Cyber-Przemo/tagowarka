import os
import tkinter as tk
import eyed3
from tkinter import filedialog, ttk
from tkinter.font import Font
from mutagen.id3 import ID3

# ustawienie kodowania
eyed3.core.get_default_encoding = "utf8"


class App:
    def __init__(self, master, button_width=12, button_height=2):
        self.master = master
        self.master.title("---Tagowarka- - -")         # nazwa w belce na górze
        self.master.geometry('300x300')                     # wielkość okna
        self.folder_path = tk.StringVar()
        self.log_path = "app.log"

# Tworzenie obiektu stylu
        self.default_style = ttk.Style()
        self.dark_style = ttk.Style()
        self.dark_style.theme_use('clam')                   # tryb ciemny
        self.current_style = 'default'                      # tryb podstawowy
        self.button_font = Font(size=10)                    # wielkosć czcionki w przycisku
        self.font = ("Arial", 12)

# napis w oknie
        self.label = tk.Label(master, text="Eksport tagów do pliku *.dat:")
        self.label.pack()

# Wskazanie folderu do tagowania
        self.folder_button = tk.Button(master, text="Wybierz folder", command=self.choose_folder, width=button_width,
                                       height=button_height, font=self.button_font)
        self.folder_button.pack()

# Napis na pasku dolnym (status)
        self.status_bar = tk.Label(master, text="Tagowanie plików", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Zamyka aplikacje
        self.quit_button = tk.Button(master, text="Zamknij", command=master.quit, width=button_width,
                                     height=button_height, font=self.button_font, bg="white", fg="blue")
        self.quit_button.pack()
        self.quit_button.pack(side="bottom", anchor="se", padx=10, pady=10)

# wybieranie folderu
    def choose_folder(self):
        self.folder_path.set(filedialog.askdirectory())
        self.tag_files()

# praca na tagach z mp3
    def tag_files(self):
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

        # lista plików mp3 w folderze
        mp3_files = [f for f in os.listdir(self.folder_path.get()) if f.endswith(".mp3")]

        # zapisanie pliku z tagami dla każdego pliku mp3
        for filename in mp3_files:
            filepath = os.path.join(self.folder_path.get(), filename)
            tags = ID3(filepath)
            tags_string = ""

            # przeiteruj po słowniku i dodaj opis i wartość taga do stringa
            for tag_name, tag_description in tags_dict.items():
                if tag_name in tags:
                    tag_value = tags[tag_name].text[0].lstrip()  # usunięcie spacji z początku i końca oraz ze środka wartości taga
                    tags_string += f"{tag_description}{tag_value}\n"  # dodanie opisu taga i wartości do stringa

            # zapisanie pliku *.dat (bez rozszerzenia mp3)
            filename_without_extension = os.path.splitext(filename)[0]
            with open(os.path.join(self.folder_path.get(), f"{filename_without_extension}.dat"), "w",
                      encoding="utf-8") as f: 
                f.write(tags_string)

        # if not mp3_files:
        #     tk.messagebox.showinfo("Brak plików", "Brak plików do tagowania w wybranym folderze.")

    def update_status_bar(self, text):
        self.status_bar.config(text=text)
        self.master.update()


root = tk.Tk()
app = App(root)
root.mainloop()
