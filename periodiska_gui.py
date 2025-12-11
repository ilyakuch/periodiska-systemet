import tkinter as tk
import random
from enum import Enum

FILE_PATH = "elements.txt"


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

BG_COLORS = {
    "Alkali_metals": "#f3a5a5",
    "Alkaline_earth_metals": "#f3cfa5",
    "Lanthanides": "#edb5f3",
    "Actinides": "#d5b5f3",
    "Transition_metals": "#a5bdf3",
    "Poor_metals": "#a5aef3",
    "Metalloids": "#92bdc3",
    "Nonmetals": "#a5f3ce",
    "Halogens": "#b0f3a5",
    "Noble_gases": "#a5f0f3",
    "Other": "#c4c4c4"
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
            if str(query) == element.name:
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
        self.bg_color = BG_COLORS[family]

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
        element_data = cell_data["element_data"]

        cell_data["frame"].config(bg=element_data.bg_color)
        cell_data["labels"]["symbol"].config(text="", bg=element_data.bg_color)
        cell_data["labels"]["atnum"].config(text="", bg=element_data.bg_color)
        cell_data["labels"]["mass"].config(text="", bg=element_data.bg_color)

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
    

    def _clear_widgets(self, title):

        for widget in self.header.winfo_children():
            widget.destroy()
        for widget in self.body.winfo_children():
            widget.destroy()

        btn_text = "Avsluta" if title == "Välj spel" else "Tillbaka"
        btn_type = self.app.quit if title == "Välj spel" else self.app.back
        tk.Label(self.header, text=title).grid(column=0, row=0)
        tk.Button(self.header, text=btn_text, command= btn_type).grid(column=1, row=0)
    

    def start_screen(self):
        
        self._clear_widgets("Välj spel")
        tk.Button(self.body, text="Öva på atomnummer", command= self.app.prac_atnum).grid()
        tk.Button(self.body, text="Öva på atomnamn", command= self.app.prac_name).grid()
        tk.Button(self.body, text="Öva på atombeteckningar", command= self.app.prac_symb).grid()
        tk.Button(self.body, text="Öva på atommassa", command= self.app.prac_mass).grid()
        tk.Button(self.body, text="Öva på periodiska tabellen", command= None).grid()
    

    def atnum_prac_layout(self, question: Element, attempts: int):
        self._clear_widgets("Träna på atomnummer")
        tk.Label(self.body, text=f"Vilket atomnummer har grundämnet: {question.name}?").grid(row=0)
        if attempts < 3:
            tk.Label(self.body, text=f"{str(attempts)} försök kvar!").grid(row=0, column=1)
        usr_input = tk.Entry(self.body)
        usr_input.grid(row=2, column=0)
        tk.Button(self.body, text="Rätta", command=lambda: self.app.check_atnum_ans(question, usr_input.get(), attempts)).grid(row=2, column=1)


    def name_prac_layout(self, question: Element, attempts: int):
        self._clear_widgets("Träna på namn")
        tk.Label(self.body, text=f"Vad heter grundämnet: {question.symbol}?").grid(row=0)
        if attempts < 3:
            tk.Label(self.body, text=f"{str(attempts)} försök kvar!").grid(row=0, column=1)
        usr_input = tk.Entry(self.body)
        usr_input.grid(row=2, column=0)
        tk.Button(self.body, text="Rätta", command=lambda: self.app.check_name_ans(question, usr_input.get(), attempts)).grid(row=2, column=1)


    def symb_prac_layout(self, question: Element, attempts: int):
        self._clear_widgets("Träna på atombeteckningar")
        tk.Label(self.body, text=f"Vilken atombeteckning har grundämnet: {question.name}?").grid(row=0)
        if attempts < 3:
            tk.Label(self.body, text=f"{str(attempts)} försök kvar!").grid(row=0, column=1)
        usr_input = tk.Entry(self.body)
        usr_input.grid(row=2, column=0)
        tk.Button(self.body, text="Rätta", command=lambda: self.app.check_symb_ans(question, usr_input.get(), attempts)).grid(row=2, column=1)


    def mass_prac_layout(self, question: Element):
        self._clear_widgets("Träna på atommassa")
        tk.Label(self.body, text=f"Vilken massa har grundämnet: {question.name}?").grid(row=0, column=0)

        btn_frame = tk.Frame(self.body)
        btn_frame.grid(row=1, column=0)
        btn_contents = self.app.generate_mass_question_set(question)

        for i, content in enumerate(btn_contents):
            tk.Button(btn_frame, text=round(content), command=lambda ct=content: self.app.check_mass_ans(question, ct)).grid(row=1, column=i)

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

        self.startscreen()


    def startscreen(self):
        self.panel.start_screen()
        self.table.show_periodic_table()


    def quit(self):
        self.root.quit()
    

    def back(self):
        self.startscreen()


    def generate_mass_question_set(self, question: Element) -> list[float]:

        true_mass = question.mass
        offset = max(true_mass*0.125, 5)
        lower = max(true_mass-offset, 1)
        upper = true_mass+offset

        # Sets can only contain unique elements - duplicates are ruled out.
        question_set = {true_mass}
        while len(question_set) < 3:
            decoy_ans = random.uniform(lower, upper)
            if round(decoy_ans) != round(true_mass): #TBD: FINNS SAMMA
                question_set.add(decoy_ans)

        # Convert to list in order to shuffle
        question_list = list(question_set)
        random.shuffle(question_list)
        return question_list




    def prac_atnum(self, question=None, attempts=3):
        self.table.clear_periodic_table()
        if question:
            self.panel.atnum_prac_layout(question, attempts)
        else:
            self.panel.atnum_prac_layout(self.elements.random_element(), attempts)


    def prac_name(self, question=None, attempts=3):
        self.table.clear_periodic_table()
        if question:
            self.panel.name_prac_layout(question, attempts)
        else:
            self.panel.name_prac_layout(self.elements.random_element(), attempts)


    def prac_symb(self, question=None, attempts=3):
        self.table.clear_periodic_table()
        if question:
            self.panel.symb_prac_layout(question, attempts)
        else:
            self.panel.symb_prac_layout(self.elements.random_element(), attempts)


    def prac_mass(self):
        self.table.clear_periodic_table()
        self.panel.mass_prac_layout(self.elements.random_element())


    def prac_periodic(self):
        


    def check_atnum_ans(self, question: Element, answer: str, attempts: int):
        if str(question.atnum).casefold() == answer.casefold():
            self.prac_atnum()
        elif attempts <= 1:
            self.prac_atnum()
        else:
            self.prac_atnum(question, attempts-1)


    def check_name_ans(self, question: Element, answer: str, attempts: int):
        if str(question.name).casefold() == answer.casefold():
            self.prac_name()
        elif attempts <= 1:
            self.prac_name()
        else:
            self.prac_name(question, attempts-1)


    def check_symb_ans(self, question: Element, answer: str, attempts: int):
        if str(question.symbol).casefold() == answer.casefold():
            self.prac_symb()
        elif attempts <= 1:
            self.prac_symb()
        else:
            self.prac_symb(question, attempts-1)


    def check_mass_ans(self, question: Element, answer: int):
        if question.mass == answer:
            self.prac_mass()
        else:
            self.prac_mass()



def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
