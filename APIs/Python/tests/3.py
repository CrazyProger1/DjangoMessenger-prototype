import api
import unittest
import api.exceptions


class TestChat(unittest.TestCase):
    def setUp(self) -> None:
        self.user = api.User('TestUser', 'BIGSTRONGPASS', 'testuser@gmail.com', save_tokens=False)
        self.user2 = api.User('TestUser2', 'BIGSTRONGPASS', 'testuser2@gmail.com', save_tokens=False)
        self.user3 = api.User('TestUser3', 'BIGSTRONGPASS', 'testuser3@gmail.com', save_tokens=False)

        self.user.register()
        self.user2.register()
        self.user3.register()

    def test_chat_creation(self):
        chat_id = self.user.create_chat('bla bla bla', False, False)

        self.user.add_chat_member(chat_id, self.user2.id)
        self.assertRaises(api.exceptions.ChatOverflowError, lambda: self.user.add_chat_member(chat_id, self.user3.id))

    def tearDown(self) -> None:
        self.user.delete()
        self.user2.delete()
        self.user3.delete()
