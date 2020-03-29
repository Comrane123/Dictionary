import tkinter as tk
from Dictionary import AutocompleteEntry

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        auto_entry = AutocompleteEntry(self)
        auto_entry.grid()


if __name__ == "__main__":
    App().mainloop()
