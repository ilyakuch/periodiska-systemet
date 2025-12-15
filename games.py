import random

class BaseGames:
    """Game blueprint for the base games."""

    def __init__(self, elements, attempts: int, title: str, correct_attr: str, question):
        self.elements = elements
        self.attempts = attempts
        self.max_attempts = attempts
        self.current_question = self.elements.random_element()
        self.feedback = ""

        self.title = title
        self.correct_attr = correct_attr
        self.question = question


    def _generate_new_question(self):
        self.attempts = self.max_attempts
        self.current_question = self.elements.random_element()
        return self.current_question


    def get_current_question(self) -> str:
        """Returns the current formatted question"""

        return self.question(self.current_question)


    def get_question_status(self) -> str:
        """Returns the feedback from the previous question. E.g. correct."""

        return self.feedback


    def update(self, answer: str) -> None:
        """Updates the game based on the provided answer."""

        correct_value = getattr(self.current_question, self.correct_attr)

        if str(correct_value).casefold() == str(answer).casefold():
            self.feedback = "Rätt!"
            self._generate_new_question()

        elif self.attempts <= 1:
            self.feedback = f"Fel! Rätt svar var: {correct_value}"
            self._generate_new_question()

        else:
            self.attempts -= 1
            self.feedback = f"Fel, {self.attempts} försök kvar."


class AtnumGame(BaseGames):
    """Game class for atomic number training. Inherits from BaseGame"""

    def __init__(self, elements):
        super().__init__(
            elements,
            attempts=3,
            title = "Träna på atomnummer",
            correct_attr = "atnum",
            question = lambda q: f"Vilket atomnummer har grundämnet: {q.name}?")



class NameGame(BaseGames):
    """Game class for name training. Inherits from BaseGame"""

    def __init__(self, elements):
        super().__init__(
            elements,
            attempts=3,
            title = "Träna på namn",
            correct_attr = "name",
            question = lambda q: f"Vad heter grundämnet: {q.symbol}?")


class SymbolGame(BaseGames):
    """Game class for symbol training. Inherits from BaseGame"""

    def __init__(self, elements):
        super().__init__(
            elements,
            attempts=3,
            title = "Träna på atombeteckningar",
            correct_attr = "symbol",
            question = lambda q: f"Vilken atombeteckning har grundämnet: {q.name}?")


class MassGame:
    """Game class for the mass game."""

    def __init__(self, elements):
        self.elements = elements
        self.attempts = None
        self.current_question = self.elements.random_element()
        self.feedback = ""


    def _generate_mass_question_set(self, question):

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


    def _generate_new_question(self):
        self.current_question = self.elements.random_element()
        return self.current_question


    def get_current_question(self) -> str:
        """Returns the current formatted question"""

        return f"Vilken massa har grundämnet {self.current_question.name}"


    def get_answers(self) -> list[float]:
        """Returns an answer set consisting of 3 choices."""

        return self._generate_mass_question_set(self.current_question)


    def get_question_status(self) -> str:
        """Returns feedback for the prevoius question."""
        return self.feedback


    def update(self, answer: float) -> None:
        """Updates the game based on the provided answer."""

        correct_value = self.current_question.mass

        if self.current_question.mass == answer:
            self.feedback = "Rätt!"
            self._generate_new_question()

        else:
            self.feedback = f"Fel Svar! Rätt svar var {round(correct_value)}"
            self._generate_new_question()


class PeriodicGame:
        
    def __init__(self, elements):
        self.elements = elements
        self.attempts = None
        self.shuffled_elements = self.elements.get_all_elements()
        random.shuffle(self.shuffled_elements)
        self.current_question = self._generate_new_question()
        self.feedback = ""


    def _generate_new_question(self):
        if len(self.shuffled_elements) > 0:
            self.current_question = self.shuffled_elements.pop(0)
            return self.current_question
        self.current_question = None
        return self.current_question


    def get_current_question(self) -> str:
        """Returns the current formatted question"""

        return f"Placera ut: {self.current_question.name}" if self.current_question else ""


    def get_question_status(self) -> str:
        """Returns feedback for the prevoius question."""

        return self.feedback


    def update(self, answer):
        """Updates the game based on the provided answer."""

        if self.current_question is None:
            self.feedback = "Grattis! Du klarade det!"
            return False

        if self.current_question.pos == answer.pos:
            self.feedback = "Rätt!"

            if self.shuffled_elements:
                self._generate_new_question()
            else:
                self.current_question = None
                self.feedback = "Grattis! Du klarade det!"

            return True

        else:
            self.feedback = f"Detta är inte {self.current_question.name}"
            return False
