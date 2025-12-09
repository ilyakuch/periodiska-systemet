import random
from enum import Enum
import os

FILE_PATH = "elements.txt"


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
    
    def get_random_element(self):
        return random.choice(self._elements)
    
    def get_all_elements_as_list(self):
        element_list = "Lista över alla grundämnen\n\n"
        for element in self._elements:
            element_list += f"{element}\n"
        return element_list




class Element:

    def __init__(self, symbol, atomic_number, name, mass, period, group, family):
        self.symbol = symbol
        self.atomic_number = int(atomic_number)
        self.name = name
        self.mass = float(mass)
        self.period = int(period)
        self.group = int(group) if group.isdigit() else None
        self.family = family

        if 57 <= self.atomic_number <= 71:
            self.pos = (self.period+2, self.atomic_number-53)
        elif 89 <= self.atomic_number <= 103:
            self.pos = (self.period+2, self.atomic_number-85)
        else:
            self.pos = (self.period, self.group)
    
    def __str__(self):
        return f"{self.symbol}, {self.atomic_number}, {self.name}, {self.mass}"


class Terminal:

    def __init__(self):
        self._clear_terminal()
        print("P-uppgift * Periodiska systemet")
        print("Ilya Kuchinsky\n")
        input("Detta är ett övningsspel för det periodiska systemet.\n" \
        "Tryck Enter för att fortsätta")

    def _clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _input_int(self, prompt):
        while True:
            try:
                usr_input = int(input(prompt))
            except ValueError:
                print("^^^ ska vara en siffra, försök igen...\n")
                continue
            return usr_input

    def _input_choice(self, choices):
        while True:
            try:
                usr_input = int(input("Välj menyval: "))
            except ValueError:
                print("^^^ ska vara en siffra, försök igen...\n")
                continue

            if 1 <= usr_input <= choices:
                return usr_input
            else:
                print("^^^ ska vara en giltigt menyval, försök igen...\n")

    def start_menu(self):
        self._clear_terminal()
        print("-----Meny-----")
        print("1. Lista alla grundämnen")
        print("2. Visa periodiska tabellen")
        print("3. Träna på atomnummer")
        print("4. Träna på atombeteckningar")
        print("5. Träna på atomnamn")
        choice = self._input_choice(5)


def main():

    elements = PeriodicTable()
    terminal = Terminal()

    


if __name__ == "__main__":
    main()
