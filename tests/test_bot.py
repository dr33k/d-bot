import unittest
from constants import QUESTION, ANSWER
from models.bot import Bot
from tests.db.driver import test_kb

class TestBot(unittest.TestCase):
    def setUp(self):
        self.dbot = Bot(kb=test_kb)
        self.dialogues = self.dbot.dialogues

    def tearDown(self):
        self.dialogues.delete_many({})

    def test_bot_init(self):
        self.assertIsNotNone(self.dbot)
        self.assertEqual(self.dbot.bot_name, 'Dbot')
        self.assertTrue(self.dbot.training_mode)
        self.assertIsNotNone(self.dialogues)


    def test_update_kb(self):

        q, a = 'What is my purpose in life ?', 'The true meaning of your life is to give your\'s purpose'
        self.dbot.update_kb(q, a)

        dialogue = self.dialogues.find_one({QUESTION: q})
        self.assertIsNotNone(dialogue)
        self.assertEqual(dialogue[ANSWER], a)


if __name__ == '__main__':
    unittest.main()