import tkinter as tk
import time
import random

FILE_PATH = "elements_extra.txt"


class PeriodicTable:

    def __init__(self):

        self._elements = []

        with open(FILE_PATH, encoding="utf-8") as file:
            lines = file.readlines()
            lines.sort(key=lambda x: int(x.split()[1]))

            for line in lines:
                line = line.split()
                self._elements.append(Element(*line))

    
    def lookup_by_pos(self, query: tuple):

        for element in self._elements:
            if query == element.pos:
                return element
        return None
        
    def lookup_by_symbol(self, query: str):

        for element in self._elements:
            if query == element.symbol:
                return element
        return None



class Element:

    LOOKUP_KEYS = ["symbol", "atomic_number", "name", "pos"]

    def __init__(self, symbol, atomic_number, name, mass, period, group):
        self.symbol = symbol
        self.atomic_number = int(atomic_number)
        self.name = name
        self.mass = float(mass)
        self.period = int(period)
        self.group = int(group) if group.isdigit() else None

        if 57 <= self.atomic_number <= 71:
            self.pos = (self.period+2, self.atomic_number-53)
        elif 89 <= self.atomic_number <= 103:
            self.pos = (self.period+2, self.atomic_number-85)
        else:
            self.pos = (self.period, self.group)


class Table:

    def __init__(self, left_frame, elements: PeriodicTable, rows=10, cols=18):
        self.left_frame = left_frame
        self.rows = rows
        self.cols = cols
        self.cells = {}
        self.elements = elements

        self.periodic_table_frame = tk.Frame(self.left_frame)
        self.periodic_table_frame.grid()

        self._build_grid()
        self.show_periodic_table()


    def _build_grid(self):

        for r in range(1, self.rows+1):
            for c in range(1, self.cols+1):

                element_data = self.elements.lookup_by_pos((r,c))

                if element_data:
                    element_frame = tk.Frame(self.periodic_table_frame, width=60, height=60)
                    element_frame.grid(row=r, column=c, padx=2, pady=2)
                    element_frame.grid_propagate(False)

                    atomic_number_label = tk.Label(element_frame)
                    atomic_number_label.grid(row=0, column=0, sticky="nw")

                    symbol_label = tk.Label(element_frame)
                    symbol_label.grid(row=1, column=0, columnspan=2, sticky="nw")

                    mass_label = tk.Label(element_frame)
                    mass_label.grid(row=0, column=1, sticky="e")


                    self.cells[(r, c)] = {
                        "frame": element_frame,
                        "element_data": element_data, 
                        "labels": {
                            "symbol": symbol_label, 
                            "atomic_number": atomic_number_label, 
                            "mass": mass_label}}

    def show_element(self, cell: tuple):

        cell_data = self.cells[cell]
        element_data = cell_data["element_data"]

        cell_data["frame"].config(bg="blue")
        cell_data["labels"]["symbol"].config(text=element_data.symbol, anchor="nw", font=("Arial", 28, "bold"), fg="white", bg="blue")
        cell_data["labels"]["atomic_number"].config(text=element_data.atomic_number, font=("Arial", 18), bg="blue")
        cell_data["labels"]["mass"].config(text=round(element_data.mass, 1), font=("Arial", 10), fg="white", bg="blue")

    def show_periodic_table(self):

        for cell in self.cells:
            self.show_element(cell)

    def hide_element(self, cell: tuple):

        cell_data = self.cells[cell]

        cell_data["frame"].config(bg="gray")
        cell_data["labels"]["symbol"].config(text="", bg="gray")
        cell_data["labels"]["atomic_number"].config(text="", bg="gray")
        cell_data["labels"]["mass"].config(text="", bg="gray")

    def clear_periodic_table(self):
        
        for cell in self.cells:
            self.hide_element(cell)

    def flash_cell(self):
        ...

 
class InputPanel:
    
    def __init__(self, right_frame):
        self.right_frame = right_frame
    
    def start_screen(self):
        ...



class App():

    def __init__(self, root):
        self.root = root
        root.configure(bg="white")

        self.elements = PeriodicTable()

        self.left_frame = tk.Frame(self.root, bg="white")
        self.left_frame.grid(column=0, padx=(5, 5), pady=(5, 5))

        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.grid(column=1, padx=5, pady=5)

        self.table = Table(self.left_frame, self.elements)
        self.input_panel = InputPanel(self.right_frame)

    def startscreen(self):
        ...
    



    def atomic_number_training(self):
        ...

    def event_atomic_number_training_answer_choice(self):
        ...



    def symbol_training(self):
        ...
    
    def name_training(self):
        ...
    
    def exit_program(self):
        ...





def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
