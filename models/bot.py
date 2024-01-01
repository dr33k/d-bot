import json, re
from difflib import get_close_matches

class Bot:
    """Entity representing a chatbot to be trained in a specific domain"""

    def __init__(self, kb_path='json/knowledge_base.json', name='Dbot', training_mode:bool=True):
        """Creates a trainable bot by default with training_mode=True
            training_mode=False creates a Bot for the production environment
        """
        with open(kb_path, 'r') as file:
            self._knowledge_base: dict = json.load(file)
            self._training_mode: bool = training_mode
            self._bot_name: str = name
            self._function: str = ''

    @property
    def bot_name(self): return self._bot_name

    @bot_name.setter
    def bot_name(self, name: str):
        self._bot_name = name

    @property
    def function(self): return self._function
    @function.setter
    def function(self, function: str):
        function = function.lower()

        if not re.match(r'^to.*$'):
            raise ValueError(
                'The function of the bot must start with the word \'to\' in order to better convey it\'s functio to the user')

        self._function = function

    @property
    def training_mode(self): return self._training_mode
    @training_mode.setter
    def training_mode(self, tm: bool):
        self.training_mode = tm

    def append_kb(self):
        """Appends new data to the knowledge base"""

        with open('json/knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file)

    def __clean_input(self, user_question: str) -> list[str]:
        """Sterilizes and splits input strings into words for matching"""

        words: list = re.split(r'\s+|[.,;:\-/]\s*]', user_question.lower())
        return words

    def __match_question(self, user_question: str) -> list[str]:
        """Returns the closest matching question object from the knowledge base"""

        words = self.__clean_input(user_question)
        possibilities = self.knowledge_base['questions'].keys()

        return get_close_matches(words, possibilities, n=1)

    def __answer(self, question:str) -> str:
        return self.knowledge_base['questions'][question]['answer']

