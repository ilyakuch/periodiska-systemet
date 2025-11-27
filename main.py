import tkinter as tk

FILE_PATH = "elements.txt"

class Element:
    """
    """

    def __init__(self, symbol, atomicnum, name, mass, row, col):
        self.symbol = symbol
        self.atomicnum = atomicnum
        self.name = name
        self.mass = mass
        self._row = row
        self._col = col
        self.widget = None


class Table:

    def __init__(self, root):
        ...
        

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()


def open_file():
    with open(FILE_PATH):
        ...


def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
