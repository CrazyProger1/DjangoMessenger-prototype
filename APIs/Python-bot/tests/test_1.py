import api
import unittest
import api.exceptions
import websocket._exceptions


class TestBot(unittest.TestCase):
    bla_bla_got = False

    def setUp(self) -> None:
        self.bot = api.Bot('c3d94ba61f36685b4c50469772e60dff94d63c99b2539152d9')
        self.bot.authorize()

    def test_authorize(self):
        self.bot._id = None

        self.bot.authorize()

        self.assertIsNotNone(self.bot.id)

    def message_handler(self, msg):
        if msg.text == 'bla bla bla':
            self.bla_bla_got = True

    def test_send_message(self):
        self.bot.send_message(1, 'bla bla bla')
        self.bot.message_handler()(self.message_handler)
        self.bot.get_unread_messages(1)
        self.assertTrue(self.bla_bla_got)
