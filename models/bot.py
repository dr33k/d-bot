import json, re
from constants import ANSWER
from difflib import get_close_matches


class Bot:
    """Entity representing a chatbot to be trained in a specific domain"""

    def __init__(self, kb_path='json/questions_kb.json', name='Dbot', training_mode: bool = True):
        """Creates a trainable bot by default with training_mode=True
            training_mode=False creates a Bot for the production environment
        """
        with open(kb_path, 'r') as file:
            self._questions_kb: dict = json.load(file)
            self._kb_path: str = kb_path

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
                'The function of the bot must start with the word \'to\' in order to better convey it\'s function to the user')

        self._function = function

    @property
    def training_mode(self): return self._training_mode

    @training_mode.setter
    def training_mode(self, tm: bool):
        self.training_mode = tm

    def append_kb(self, question: str, answer: str):
        """Appends new data to the knowledge base"""

        assert bool(question), 'No question to add to knowledge base'
        assert bool(answer), 'No answer to add to knowledge base'

        self._questions_kb[question] = {ANSWER: answer}

        with open(self._kb_path, 'w') as file:
            json.dump(self._questions_kb, file)

    def __clean_input(self, user_question: str) -> list[str]:
        """Sterilizes and splits input strings into words for matching"""

        words: list = re.split(r'\s+|[.,;:\-/]\s*]', user_question.lower())
        return words

    def __match_question(self, user_question: str) -> list[str]:
        """Returns the closest matching question object from the knowledge base"""

        word = ' '.join(self.__clean_input(user_question))
        possibilities = self._questions_kb.keys()

        return get_close_matches(word, possibilities, n=1, cutoff=0.6)

    def __answer(self, question: str) -> str:
        return self._questions_kb[question]['answer']

    def converse(self):
        print(f'{self._bot_name}: Hello, I am {self._bot_name}{'and I was created' + self._function if self._function else ''}. How may I help you today? Type \'q\' to quit')

        while True:
            user_input = input('You: ')

            if user_input == 'q':
                print(f'{self._bot_name}: Bye bye :)')
                break

            matches = self.__match_question(user_input)

            if matches:
                answer = self.__answer(matches[0])
                print(f'{self._bot_name}: {answer}')
                continue

            if self.training_mode:
                print(f'{self._bot_name}: Input unrecognized, please train by entering appropriate response')
                new_answer = input('You: ')
                self.append_kb(user_input, new_answer)
                print(f'{self._bot_name}: Updated kb, moving on...')
                continue

            else:
                print(f'{self._bot_name}: I didn\'t quite get that, could you rephrase ?')
                continue
