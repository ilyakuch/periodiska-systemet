import random

class BaseGames:
    def __init__(self, elements, attempts, title, correct_attr, question_format):
        self.elements = elements
        self.attempts = attempts
        self.max_attempts = attempts
        self.current_question = self.elements.random_element()

        self.title = title
        self.correct_attr = correct_attr
        self.question_format = question_format

    def get_current_question(self):
        return self.current_question
    
    def generate_new_question(self):
        self.attempts = self.max_attempts
        self.current_question = self.elements.random_element()
        return self.current_question

    def check_answer(self, answer):
        correct_value = getattr(self.current_question, self.correct_attr)

        if str(correct_value).casefold() == str(answer).casefold():
            return {"correct": True, "next_question": True}

        # No attempts left → move on
        if self.attempts <= 1:
            return {"correct": False, "next_question": True}

        self.attempts -= 1
        return {"correct": False, "next_question": False}

    def get_display_info(self):
        if self.current_question:
            return {
                "title": self.title,
                "question": self.question_format(self.current_question),
                "attempts": str(self.attempts) if self.attempts < self.max_attempts else None,
                "answer": None
            }


class AtnumGame(BaseGames):
    def __init__(self, elements):
        super().__init__(
            elements,
            attempts=3,
            title = "Träna på atomnummer",
            correct_attr = "atnum",
            question_format = lambda q: f"Vilket atomnummer har grundämnet: {q.name}?")



class NameGame(BaseGames):
    def __init__(self, elements):
        super().__init__(
            elements,
            attempts=3,
            title = "Träna på namn",
            correct_attr = "name",
            question_format = lambda q: f"Vad heter grundämnet: {q.symbol}?")


class SymbolGame(BaseGames):
    def __init__(self, elements):
        super().__init__(
            elements,
            attempts=3,
            title = "Träna på atombeteckningar",
            correct_attr = "symbol",
            question_format = lambda q: f"Vilken atombeteckning har grundämnet: {q.name}?")


class MassGame: #LAGG TILL NÄR MAN HAR FYLLT I
    def __init__(self, elements):
        self.elements = elements
        self.attempts = None
        self.current_question = random.choice(self.elements.random_element())


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

    def get_current_question(self):
        return self.current_question
    
    def generate_new_question(self):
        self.current_question = random.choice(self.elements.random_element())
        return self.current_question

    def get_display_info(self):
        if self.current_question:
            return {
                "title": "Träna på atommassa",
                "question": f"Vilken massa har grundämnet: {self.current_question.name}",
                "attempts": None,
                "answer": self._generate_mass_question_set(self.current_question)
            }

    def check_answer(self, answer):
        if self.current_question.mass == answer:
            return {"correct": True, "next_question": True}
        return {"correct": False, "next_question": True}


class PeriodicGame:
        
    def __init__(self, elements):
        self.elements = elements
        self.attempts = None
        self.shuffled_elements = self.elements.get_all_elements()
        random.shuffle(self.shuffled_elements)
        self.current_question = self.shuffled_elements.pop(0)

    def get_current_question(self):
        return self.current_question
    
    def generate_new_question(self):
        self.current_question = self.shuffled_elements.pop(0)
        return self.current_question

    def get_display_info(self):
        if self.current_question:
            return {
                "title": "Fyll i den periodiska tabellen",
                "question": f"Placera ut: {self.current_question.name}",
                "attempts": None,
                "answer": None
            }

    def check_answer(self, answer):
        if self.current_question.pos == answer:
            return {"correct": True, "next_question": True}
        return {"correct": False, "next_question": True}
