import tkinter as tk
import random
import games

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
    
    def get_all_elements(self):
        return self._elements.copy()


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

    def __init__(self, table_frame, app, elements: PeriodicTable, rows=10, cols=18):
        self.table_frame = table_frame
        self.app = app
        self.rows = rows
        self.cols = cols
        self.cells = {}
        self.elements = elements

        self.periodic_table_frame = tk.Frame(self.table_frame)
        self.periodic_table_frame.grid()

        self._build_grid()


    def _build_grid(self):

        for r in range(1, self.rows+1):
            for c in range(1, self.cols+1):

                element_data = self.elements.lookup_by_pos((r,c))

                if element_data:
                    element_frame = tk.Frame(self.periodic_table_frame, width=60, height=60, highlightthickness=1)
                    element_frame.bind("<Button-1>", lambda _, cell=element_data: self.app.submit_table_pos(cell))
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



class InputPanel:

    
    def __init__(self, panel_frame, app):

        self.panel_frame = panel_frame
        self.app = app

        self.header = tk.Frame(self.panel_frame)
        self.header.grid(row=0, column=0, pady=(0, 40))

        self.body = tk.Frame(self.panel_frame)
        self.body.grid(row=1)


    def _clear_widgets(self, title):

        for widget in self.header.winfo_children():
            widget.destroy()
        for widget in self.body.winfo_children():
            widget.destroy()

        btn_text = "Avsluta" if title == "Välj spel" else "Tillbaka"
        btn_type = self.app.quit if title == "Välj spel" else self.app.back
        tk.Label(self.header, text=title, font=("Segoe UI", 32)).grid(column=0, row=0, padx=30)
        tk.Button(self.header, text=btn_text, command= btn_type).grid(column=0, row=1)
    

    def start_screen(self):
        
        self._clear_widgets("Välj spel")
        tk.Button(self.body, text="Öva på atomnummer", command= lambda: self.app.start_game(games.AtnumGame)).grid()
        tk.Button(self.body, text="Öva på atomnamn", command= lambda: self.app.start_game(games.NameGame)).grid()
        tk.Button(self.body, text="Öva på atombeteckningar", command= lambda: self.app.start_game(games.SymbolGame)).grid()
        tk.Button(self.body, text="Öva på atommassa", command= lambda: self.app.start_game(games.MassGame)).grid()
        tk.Button(self.body, text="Öva på periodiska tabellen", command= lambda: self.app.start_game(games.PeriodicGame)).grid()
    

    def update_basegame_layout(self, game_instance: games.BaseGames):
        
        self._clear_widgets(game_instance.title)
        tk.Label(self.body, text=game_instance.get_current_question()).grid(row=0, column=0)
        feedback = tk.Label(self.body, text=game_instance.get_question_status())
        feedback.grid(row=2, column=0)

        usr_input = tk.Entry(self.body)
        usr_input.grid(row=1, column=0)
        usr_input.focus_set()
        tk.Button(self.body,
                  text="Rätta",
                  command=lambda: self.app.submit_answer(usr_input.get())).grid(row=1, column=1)


    def update_periodic_layout(self, game_instance: games.PeriodicGame):

        self._clear_widgets("Fyll i det periodiska systemet")
        tk.Label(self.body, text=game_instance.get_current_question()).grid(row=0, column=0)
        feedback = tk.Label(self.body, text=game_instance.get_question_status())
        feedback.grid(row=2, column=0)

    def update_mass_layout(self, game_instance: games.MassGame):

        self._clear_widgets("Träna på atommassa")
        tk.Label(self.body, text=game_instance.get_current_question()).grid(row=0, column=0)
        feedback = tk.Label(self.body, text=game_instance.get_question_status())
        feedback.grid(row=2, column=0)

        btn_frame = tk.Frame(self.body)
        btn_frame.grid(row=1, column=0)
        for i, content in enumerate(game_instance.get_answers()):
            tk.Button(btn_frame, text=round(content), command=lambda ct=content: self.app.submit_answer(ct)).grid(row=1, column=i)




class App():

    def __init__(self, root):
        self.root = root

        self.elements = PeriodicTable()

        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(column=0, row=2, padx=10, pady=10)

        self.panel_frame = tk.Frame(self.root)
        self.panel_frame.grid(column=0, row=1, padx=10, pady=10)

        self.table = Table(self.table_frame, self, self.elements)
        self.panel = InputPanel(self.panel_frame, self)

        self.game_instance = None

        self.startscreen()


    def startscreen(self):
        self.panel.start_screen()
        self.table.show_periodic_table()


    def quit(self):
        self.root.quit()
    

    def back(self):
        self.startscreen()
        self.game_instance = None
    

    def start_game(self, game):
        self.table.clear_periodic_table()
        self.game_instance = game(self.elements)
        if isinstance(self.game_instance, games.MassGame):
            self.panel.update_mass_layout(self.game_instance)
        elif isinstance(self.game_instance, games.PeriodicGame):
            self.panel.update_periodic_layout(self.game_instance)
        else:
            self.panel.update_basegame_layout(self.game_instance)


    def submit_answer(self, answer):
        if isinstance(self.game_instance, games.MassGame):
            self.game_instance.update(answer)
            self.panel.update_mass_layout(self.game_instance)
        elif self.game_instance:
            self.game_instance.update(answer)
            self.panel.update_basegame_layout(self.game_instance)


    def submit_table_pos(self, answer):
        if isinstance(self.game_instance, games.PeriodicGame):
            is_correct = self.game_instance.update(answer)
            if is_correct:
                self.table.show_element(answer.pos)
            
            self.panel.update_periodic_layout(self.game_instance)


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
