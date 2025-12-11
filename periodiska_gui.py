import tkinter as tk
import random
from enum import Enum

FILE_PATH = "elements.txt"

class Btn(Enum):
    MENU_PRAC_ATNUM = 0
    MENU_PRAC_NAME = 1
    MENU_PRAC_SYMB = 2
    MENU_PRAC_MASS = 3
    MENU_PRAC_PERIODIC = 4
    QUIT = 9
    BACK = 5
    SUBMIT_PRAC_ATNUM = 6
    SUBMIT_PRAC_NAME = 7
    SUBMIT_PRAC_SYMB = 8


COLORS = {
    "Alkali_metals": "#DB2E2E",
    "Alkaline_earth_metals": "#DB8A2E",
    "Lanthanides": "#CA2EDB",
    "Actinides": "#8A2EDB",
    "Transition_metals": "#2E68DB",
    "Poor_metals": "#2E34DB",
    "Metalloids": "#25666B",
    "Nonmetals": "#2EDB93",
    "Halogens": "#34DB2E",
    "Noble_gases": "#2ED5DB",
    "Other": "#4F4F4F"
}


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
    
    def lookup_by_atnum(self, query: str):

        for element in self._elements:
            if int(query) == element.atnum:
                return element
        return None
    
    def lookup_by_name(self, query: str):

        for element in self._elements:
            if int(query) == element.name:
                return element
        return None
    
    def random_element(self):
        return random.choice(self._elements)


class Element:

    def __init__(self, symbol, atnum, name, mass, period, group, family):
        self.symbol = symbol
        self.atnum = int(atnum)
        self.name = name
        self.mass = float(mass)
        self.period = int(period)
        self.group = int(group) if group.isdigit() else None
        self.color = COLORS[family]

        if 57 <= self.atnum <= 71:
            self.pos = (self.period+2, self.atnum-53)
        elif 89 <= self.atnum <= 103:
            self.pos = (self.period+2, self.atnum-85)
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

                    atnum_label = tk.Label(element_frame)
                    atnum_label.grid(row=0, column=0, sticky="nw")

                    symbol_label = tk.Label(element_frame)
                    symbol_label.grid(row=1, column=0, columnspan=2, sticky="nw")

                    mass_label = tk.Label(element_frame)
                    mass_label.grid(row=0, column=1, sticky="e")


                    self.cells[(r, c)] = {
                        "frame": element_frame,
                        "element_data": element_data, 
                        "labels": {
                            "symbol": symbol_label, 
                            "atnum": atnum_label, 
                            "mass": mass_label}}

    def show_element(self, cell: tuple):

        cell_data = self.cells[cell]
        element_data = cell_data["element_data"]

        cell_data["frame"].config(bg=element_data.color)
        cell_data["labels"]["symbol"].config(text=element_data.symbol, anchor="nw", font=("Arial", 28, "bold"), fg="white", bg=element_data.color)
        cell_data["labels"]["atnum"].config(text=element_data.atnum, font=("Arial", 18), bg=element_data.color)
        cell_data["labels"]["mass"].config(text=round(element_data.mass, 1), font=("Arial", 10), fg="white", bg=element_data.color)

    def show_periodic_table(self):

        for cell in self.cells:
            self.show_element(cell)

    def hide_element(self, cell: tuple):

        cell_data = self.cells[cell]

        cell_data["frame"].config(bg="gray")
        cell_data["labels"]["symbol"].config(text="", bg="gray")
        cell_data["labels"]["atnum"].config(text="", bg="gray")
        cell_data["labels"]["mass"].config(text="", bg="gray")

    def clear_periodic_table(self):
        
        for cell in self.cells:
            self.hide_element(cell)

    def flash_cell(self):
        ...


class InputPanel:

    
    def __init__(self, right_frame, app):

        self.right_frame = right_frame
        self.app = app

        self.header = tk.Frame(self.right_frame, bg="white")
        self.header.grid(row=0)

        self.body = tk.Frame(self.right_frame, bg="white")
        self.body.grid(row=1)
    

    def _fwd_press(self, btnid: Btn):
        self.app.handle_press(btnid)

    def _fwd_input(self, btnid: Btn, question: Element, answer, attempts: int):
        self.app.handle_input(btnid, question, answer, attempts)

    def _clear_widgets(self, title):

        for widget in self.header.winfo_children():
            widget.destroy()
        for widget in self.body.winfo_children():
            widget.destroy()

        btn_text = "Avsluta" if title == "Välj spel" else "Tillbaka"
        btn_type = Btn.QUIT if title == "Välj spel" else Btn.BACK
        tk.Label(self.header, text=title).grid()
        tk.Button(self.header, text=btn_text, command= lambda: self._fwd_press(btn_type)).grid(column=1)


    def start_screen(self):
        
        self._clear_widgets("Välj spel")
        tk.Button(self.body, text="Öva på atomnummer", command=lambda: self._fwd_press(Btn.MENU_PRAC_ATNUM)).grid()
        tk.Button(self.body, text="Öva på atomnamn", command=lambda: self._fwd_press(Btn.MENU_PRAC_NAME)).grid()
        tk.Button(self.body, text="Öva på atombeteckningar", command=lambda: self._fwd_press(Btn.MENU_PRAC_SYMB)).grid()
        tk.Button(self.body, text="Öva på atommassa", command=lambda: self._fwd_press(Btn.MENU_PRAC_MASS)).grid()
        tk.Button(self.body, text="Öva på periodiska tabellen", command=lambda: self._fwd_press(Btn.MENU_PRAC_PERIODIC)).grid()
    

    def atnum_prac_layout(self, question: Element, attempts: int):
        self._clear_widgets("Träna på atomnummer")
        tk.Label(self.body, text=f"Vilket atomnummer har grundämnet: {question.name}?").grid(row=0)
        if attempts < 3:
            tk.Label(self.body, text=f"{str(attempts)} försök kvar!").grid(row=0, column=1)
        usr_input = tk.Entry(self.body)
        usr_input.grid(row=2, column=0)
        tk.Button(self.body, text="Rätta", command=lambda: self._fwd_input(Btn.SUBMIT_PRAC_ATNUM, question, usr_input.get(), attempts)).grid(row=2, column=1)


    def name_prac_layout(self, question: Element, attempts: int):
        self._clear_widgets("Träna på namn")
        tk.Label(self.body, text=f"Vad heter grundämnet: {question.symbol}?").grid(row=0)
        if attempts < 3:
            tk.Label(self.body, text=f"{str(attempts)} försök kvar!").grid(row=0, column=1)
        usr_input = tk.Entry(self.body)
        usr_input.grid(row=2, column=0)
        tk.Button(self.body, text="Rätta", command=lambda: self._fwd_input(Btn.SUBMIT_PRAC_NAME, question, usr_input.get(), attempts)).grid(row=2, column=1)


    def symb_prac_layout(self, question: Element, attempts: int):
        self._clear_widgets("Träna på atombeteckningar")
        tk.Label(self.body, text=f"Vilken atombeteckning har grundämnet: {question.name}?").grid(row=0)
        if attempts < 3:
            tk.Label(self.body, text=f"{str(attempts)} försök kvar!").grid(row=0, column=1)
        usr_input = tk.Entry(self.body)
        usr_input.grid(row=2, column=0)
        tk.Button(self.body, text="Rätta", command=lambda: self._fwd_input(Btn.SUBMIT_PRAC_SYMB, question, usr_input.get(), attempts)).grid(row=2, column=1)



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
        self.panel = InputPanel(self.right_frame, self)

        self._startscreen()


    def _startscreen(self):
        self.panel.start_screen()
        self.table.show_periodic_table()


    def _quit(self):
        self.root.quit()
    

    def _back(self):
        self._startscreen()


    def _prac_atnum(self, question=None, attempts=3):
        if question:
            self.panel.atnum_prac_layout(question, attempts)
        else:
            self.panel.atnum_prac_layout(self.elements.random_element(), attempts)


    def _prac_name(self, question=None, attempts=3):
        if question:
            self.panel.name_prac_layout(question, attempts)
        else:
            self.panel.name_prac_layout(self.elements.random_element(), attempts)


    def _prac_symb(self, question=None, attempts=3):
        if question:
            self.panel.symb_prac_layout(question, attempts)
        else:
            self.panel.symb_prac_layout(self.elements.random_element(), attempts)


    def _check_atnum_ans(self, question: Element, answer: str, attempts: int):
        if str(question.atnum).casefold() == answer.casefold():
            self._prac_atnum()
        elif attempts <= 1:
            self._prac_atnum()
        else:
            self._prac_atnum(question, attempts-1)


    def _check_name_ans(self, question: Element, answer: str, attempts: int):
        if str(question.symbol).casefold() == answer.casefold():
            self._prac_name()
        elif attempts <= 1:
            self._prac_name()
        else:
            self._prac_atnum(question, attempts-1)


    def _check_symb_ans(self, question: Element, answer: str, attempts: int):
        if str(question.name).casefold() == answer.casefold():
            self._prac_symb()
        elif attempts <= 1:
            self._prac_symb()
        else:
            self._prac_symb(question, attempts-1)


    def handle_press(self, btnid: Btn):
        match btnid:
            case Btn.QUIT:
                self._quit()
            case Btn.BACK:
                self._back()
            case Btn.MENU_PRAC_ATNUM:
                self._prac_atnum()
                self.table.clear_periodic_table()
            case Btn.MENU_PRAC_NAME:
                self._prac_name()
                self.table.clear_periodic_table()
            case Btn.MENU_PRAC_SYMB:
                self._prac_symb()
                self.table.clear_periodic_table()


    def handle_input(self, btnid: Btn, question: Element, answer: str, attempts: int):
        match btnid:
            case Btn.SUBMIT_PRAC_ATNUM:
                self._check_atnum_ans(question, answer, attempts)
            case Btn.SUBMIT_PRAC_NAME:
                self._check_name_ans(question, answer, attempts)
            case Btn.SUBMIT_PRAC_SYMB:
                self._check_symb_ans(question, answer, attempts)



def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
