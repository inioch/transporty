import pandas as pd
import csv
import tkinter as tk
from tkinter import filedialog, messagebox


class App:
    def __init__(self,root):
        self.root = root
        self.root.title("Tranporty")
        self.root.geometry("400x300") 

        self.file_path = None
        self.tables = {}

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Wybierz plik CSV:").pack()
        tk.Button(self.root, text="Wybierz plik", command=self.select_file).pack()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            response = messagebox.askquestion("Wybrany plik", f"Wybrany plik: {file_path}")
            if response == "yes":
                self.convert_file(file_path, self.tables)
            else:
                print("Nie")
        else:
            messagebox.showinfo("Plik nie wybrany", "Nie wybrano pliku")
        # Wczytaj plik poprawnie obsługując cudzysłowy i znaki specjalne
    def convert_file(self, file_path, tables):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)  # Automatyczna obsługa formatowania CSV
                for row in reader:
                    if not row:
                        continue  # Pomijamy puste wiersze
                    key = row[0].strip('"')  # Pierwsza kolumna jako klucz
                    if key not in tables:
                        tables[key] = []
                    tables[key].append(row)

            # Jeśli istnieje tabela "A", zapisujemy ją do pliku
            if "A" in tables:
                df_a = pd.DataFrame(tables["A"])

                # Usuwanie cudzysłowów z komórek
                df_a = df_a.applymap(lambda x: str(x) if isinstance(x, (int, float)) else x)
                # Zapisz dane do pliku CSV bez cudzysłowów
                df_a.to_csv("A_clean.csv", index=False, header=False, encoding='utf-8', sep=';')
            else:
                messagebox.showinfo("Brak A w pliku CSV", "Brak A w pliku CSV. Wczytanio niepoprawny plik")

        except FileNotFoundError:
            print(f"Plik {file_path} nie istnieje.")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()