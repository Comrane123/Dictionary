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


class AutocompleteEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(self, parent, **kwargs)
    def word_translate_list(self):
                # Create a database or connect to one
                conn = sqlite3.connect('dictionary.db')
                # Create cursor
                conn.row_factory = lambda cursor, row: row[0]
                c = conn.cursor()

                completion_list = c.execute("SELECT eng FROM D1").fetchall()
                return completion_list

                # Commit changes
                conn.commit()
                # Close connection
                conn.close()

    def set_completion_list(self, completion_list):
                self._completion_list = completion_list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
                if delta:  # need to delete selection otherwise we would fix the current position
                    self.delete(self.position, tk.END)
                else:  # set position to end so selection starts where textentry ended
                    self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                    if element.startswith(self.get().lower()):
                        _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                    self._hit_index = 0
                    self._hits = _hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                    self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                    self.delete(0, tk.END)
                    self.insert(0, self._hits[self._hit_index])
                    self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                    self.delete(self.index(tk.INSERT), tk.END)
                    self.position = self.index(tk.END)
                if event.keysym == "Left":
                    if self.position < self.index(tk.END):  # delete the selection
                        self.delete(self.position, tk.END)
                    else:
                        self.position = self.position - 1  # delete one character
                        self.delete(self.position, tk.END)
                if event.keysym == "Right":
                    self.position = self.index(tk.END)  # go to end (no selection)
                if event.keysym == "Down":
                    self.autocomplete(1)  # cycle to next hit
                if event.keysym == "Up":
                    self.autocomplete(-1)  # cycle to previous hit


if __name__ == "__main__":
    dictionary = AutocompleteEntry()
    dictionary.mainloop()
