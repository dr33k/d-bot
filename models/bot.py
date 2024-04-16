import re
from constants import QUESTION, ANSWER
from difflib import get_close_matches
from db.driver import kb


class Bot:
    """Entity representing a chatbot to be trained in a specific domain"""

    def __init__(self, name='Dbot', training_mode: bool = True, kb=kb):
        """Creates a trainable bot by default with training_mode=True
            training_mode=False creates a Bot for the production environment
        """
        self.__dialogues = kb['dialogues'] #Dialogues collection
        
        self.__training_mode: bool = training_mode
        self.__bot_name: str = name
        self.__function: str = ''

    @property
    def dialogues(self): return self.__dialogues

    @property
    def bot_name(self): return self.__bot_name

    @bot_name.setter
    def bot_name(self, name: str):
        self.__bot_name = name

    @property
    def bot__function(self): return self.__function

    @bot__function.setter
    def bot__function(self, function: str):
        function = function.lower()

        assert re.search('^to', function) is not None, '''
        The function of the bot must start with the word \'to\' in order to better convey it\'s function to the user
        '''
        self.__function = function

    @property
    def training_mode(self): return self.__training_mode

    @training_mode.setter
    def training_mode(self, tm: bool):
        self.__training_mode = tm


    def update_kb(self, q: str, answer: str):
        """Adds new data to the knowledge base"""

        assert bool(q), 'No question to add to knowledge base'
        assert bool(answer), 'No answer to add to knowledge base'

        self.__dialogues.insert_one({QUESTION: q, ANSWER: answer})


    def __clean_input(self, user_question: str) -> list[str]:
        """Sterilizes and splits input strings into words for matching"""

        words = re.split(r'\s+|[.,;:\-/]\s*]', user_question.lower())
        return words

    def __match_question(self, user_question: str) -> list[str]:
        """Returns the closest matching question object from the knowledge base"""

        user_question = ' '.join(self.__clean_input(user_question))
        dialogue_object_list = self.__dialogues.find({}, {QUESTION: 1, '_id': 0}) # Possible dialogues to match in the kb

        possibilities = [dialogue[QUESTION] for dialogue in dialogue_object_list]

        return get_close_matches(user_question, possibilities, n=1, cutoff=0.6)

    def __answer(self, question: str) -> str:
        dialogue: list = self.__dialogues.find_one({QUESTION: question}, {'_id': 0, ANSWER: 1}) # List of one object
        return dialogue[ANSWER]

    def peep(self):
        for x in self.__dialogues.find():
            print(x)

    def converse(self):
        print(f'''
        {self.__bot_name}: Hello, I am {self.__bot_name}.
        {' I was created ' + self.__function if self.__function else ''}
        How may I help you today? Enter \'q\' to quit at any time
         ''')

        while True:
            try:
                user_input = input('You: ')

                if user_input == 'q':
                    self.__dialogues.delete_many({})
                    break

                matches = self.__match_question(user_input)

                if matches:
                    answer = self.__answer(matches[0])
                    print(f'{self.__bot_name}: {answer}')
                    continue

                if self.training_mode:
                    print(f'{self.__bot_name}: Input unrecognized, please train by entering human-like response for input \'{user_input}\'')
                    new_answer = input('You: ')
                    self.update_kb(user_input, new_answer)
                    print(f'{self.__bot_name}: Updated knowledge base, moving on...')

                else:
                    print(f'{self.__bot_name}: I didn\'t quite get that, could you rephrase ?')

            except Exception as ex: print(ex)

        print(f'{self.__bot_name}: Bye bye :)')
