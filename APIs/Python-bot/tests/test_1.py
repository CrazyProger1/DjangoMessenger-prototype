import api
import unittest
import api.exceptions


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.bot = api.Bot('c3d94ba61f36685b4c50469772e60dff94d63c99b2539152d9')
        self.bot.authorize()

    def test_authorize(self):
        self.bot._id = None

        self.bot.authorize()

        self.assertIsNotNone(self.bot._id)
