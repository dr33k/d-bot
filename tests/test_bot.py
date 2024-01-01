import unittest
from models.bot import Bot

class TestBot(unittest.TestCase):
    def test_bot_init(self):
        dbot = Bot(kb_path='tests/json/test_knowledge_base.json')

        self.assertIsNotNone(dbot)
        self.assertEqual(dbot.bot_name, 'Dbot')
        self.assertTrue(dbot.training_mode)

if __name__ == '__main__':
    unittest.main()