import api
import unittest
import api.exceptions


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self.user = api.User('TestUserQ1', 'BIGSTRONGPASS', 'testuser@gmail.com', save_tokens=False)
        self.user.register()

    def test_bot_creation(self):
        bot = self.user.create_bot('testbot234')

        self.assertIsNotNone(bot.token)

        self.assertRaises(api.exceptions.WrongDataProvidedError, lambda: self.user.create_bot('testbot234'))

    def tearDown(self) -> None:
        self.user.delete()
