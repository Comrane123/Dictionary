import tkinter as tk
import sqlite3
from functools import partial


class Dictionary(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_completion_list = partial(self.set_completion_list, self.word_translate_list)

        self.title('Dictionary')
        self.geometry("860x660")

        # Frame setup
        self.outer_frame_1 = tk.LabelFrame(self, padx=5, pady=5)
        self.outer_frame_1.grid(row=0, column=0, padx=10, pady=10)

        self.outer_frame_2 = tk.LabelFrame(self, padx=5, pady=5)
        self.outer_frame_2.grid(row=0, column=1, padx=10, pady=10)

        self.inner_frame_1 = tk.LabelFrame(self.outer_frame_1, text="Введите слово:", padx=5, pady=5)
        self.inner_frame_1.grid(row=0, column=0, padx=10, pady=10)

        self.inner_frame_2 = tk.LabelFrame(self.outer_frame_1, text="Введите аббривиатуру:", padx=5, pady=5)
        self.inner_frame_2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.inner_frame_3 = tk.LabelFrame(self.outer_frame_1, text="Перевод:", padx=5, pady=5)
        self.inner_frame_3.grid(row=2, column=0, padx=10, pady=10)

        self.inner_frame_4 = tk.LabelFrame(self.outer_frame_2, text="Выбор языка", padx=5, pady=5)
        self.inner_frame_4.grid(row=1, column=0, padx=10, pady=10)

        # Input/output modules
        self.word_input_entry = tk.Entry(self.inner_frame_1, width=70, command=lambda: self.set_completion_list(self.word_translate_list))
        self.word_input_entry.pack()

        self.abbreviation_input_entry = tk.Entry(self.inner_frame_2, width=30)
        self.abbreviation_input_entry.pack()

        self.output_text = tk.Text(self.inner_frame_3, width=70)
        self.output_text.pack()

        self.translate_button = tk.Button(self.outer_frame_2, text="Перевести", height=5, bg="light green", command=self.translate)
        self.translate_button.grid(row=0, column=0, padx=10, pady=10)

        # Choose language
        self.language_first = tk.StringVar()
        self.language_second = tk.StringVar()

        self.language_first.set("Английский")
        self.language_second.set("Русский")

        self.first_language_label = tk.Label(self.inner_frame_4, textvariable=self.language_first)
        self.first_language_label.grid(row=0, column=0, padx=10, pady=10)

        self.second_language_label = tk.Label(self.inner_frame_4, textvariable=self.language_second)
        self.second_language_label.grid(row=2, column=0, padx=10, pady=10)

        self.change_language_button = tk.Button(self.inner_frame_4, text="Поменять язык", command=lambda: self.choose_language(self.language_first, self.language_second))
        self.change_language_button.grid(row=1, column=0, padx=10, pady=10)

    def translate(self):
        word = self.word_input_entry.get()
        abbreviation = self.abbreviation_input_entry.get()

        # Clear output field
        self.output_text.delete('1.0', tk.END)

        # Create a database or connect to one
        conn = sqlite3.connect('dictionary.db')
        # Create cursor
        c = conn.cursor()

        if len(word) > 0:
            word_translate = self.word_input_entry.get()
            result = c.execute("SELECT rus FROM D1 WHERE eng=?", (word_translate,))
            check = result.fetchall()
            if len(check) == 0:
                self.output_text.insert(tk.INSERT, "Слово отсутствует")
            else:
                self.output_text.insert(tk.INSERT, check)
        elif len(abbreviation) > 0:
            abbreviation_translate = self.abbreviation_input_entry.get()
            result = c.execute("SELECT eng FROM D1 WHERE rus=?", (abbreviation_translate,))
            check = result.fetchall()
            if len(check) == 0:
                self.output_text.insert(tk.INSERT, "Аббревиатура отсутствует")
            else:
                self.output_text.insert(tk.INSERT, check)
        else:
            self.output_text.insert(tk.INSERT, "Введите слово или аббривиатуру")

        # Commit changes
        conn.commit()
        # Close connection
        conn.close()

    @classmethod
    def choose_language(self, language_first, language_second):
        if language_first == "Английский":
            self.language_first.set("Русский")
            self.language_second.set("Английский")
        elif language_second == "Английский":
            self.language_first.set("Английский")
            self.language_second.set("Русский")


if __name__ == "__main__":
    dictionary = AutocompleteEntry()
    dictionary.mainloop()
