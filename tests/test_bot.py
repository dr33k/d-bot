import unittest
from constants import ANSWER
from models.bot import Bot
import json

class TestBot(unittest.TestCase):

    kb_path = 'tests/json/test_questions_kb.json'

    @classmethod
    def setUpClass(cls):
        with open(cls.kb_path, 'w') as kb_file:
            json.dump({}, kb_file)

    def setUp(self):
        self.dbot = Bot(kb_path=self.kb_path)

    def tearDown(self):
        with open(self.kb_path, 'w') as kb_file:
            json.dump({}, kb_file)

    def test_bot_init(self):

        self.assertIsNotNone(self.dbot)
        self.assertEqual(self.dbot.bot_name, 'Dbot')
        self.assertTrue(self.dbot.training_mode)

    def test_append_kb(self):
        q, a = 'What is my purpose in life ?', 'The true meaning of your life is to give your\'s purpose'
        self.dbot.append_kb(q, a)

        with open(self.kb_path, 'r+') as kb_file:
            kb = json.load(kb_file)
            self.assertTrue(kb[q], a)
            del kb[q]
            json.dump(kb, kb_file)


if __name__ == '__main__':
    unittest.main()