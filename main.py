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

    def __init__(self, root, rows=10, cols=18):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cells = {}

        self._build_grid()

    def _build_grid(self):
        for r in range(1, self.rows+1):
            for c in range(1, self.cols+1):
                button = tk.Button(self.root, width=3, height=3, bg="lightgray")
                button.grid(row=r, column=c, padx=1, pady=1)
                self.cells[(r, c)] = button

class App(tk.Tk):
    
    def __init__(self):
        super().__init__()



def open_file():
    with open(FILE_PATH):
        ...


def main():
    app = App()
    table = Table(app)
    app.mainloop()

if __name__ == "__main__":
    main()
