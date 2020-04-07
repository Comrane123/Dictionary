import tkinter as tk
# from Dictionary import AutocompleteEntry
from Autocomplete import AutocompleteEntry
import sqlite3


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        conn = sqlite3.connect('dictionary.db')
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        test_list = c.execute("SELECT eng FROM D1").fetchall()
        conn.commit()
        conn.close()

        entry = AutocompleteEntry(self)
        entry.set_completion_list(test_list)
        entry.pack()
        entry.focus_set()


if __name__ == "__main__":
    App().mainloop()
