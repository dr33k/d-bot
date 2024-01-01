import json, re
from difflib import get_close_matches

class Bot:

    def __init__(self, training_mode:bool=True):
        """Creates a trainable bot by default with training_mode=True
            training_mode=False creates a Bot for the production environment
        """
        with open('json/knowledge_base.json', 'r') as file:
            self.knowledge_base: dict = json.load(file)
            self.training_mode: bool = training_mode

    def append_kb(self):
        """Appends new data to the knowledge base"""

        with open('json/knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file)

    def __clean_input(self, user_question: str) -> list[str]:
        """Sterilizes and splits input strings into words for matching"""

        words: list = re.split(r'\s+|[.,;:\-/]\s*]', user_question.lower())
        return words

    def match_question(self, user_question: str):
        """Returns the closest matching question object from the knowledge base"""

        words = self.__clean_input(user_question)
        possibilities = [q['question'] for q in self.knowledge_base['questions']]

        return get_close_matches(words, possibilities, n=1)

