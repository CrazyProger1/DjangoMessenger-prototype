import api
import unittest
import api.exceptions


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.user = api.User('TestUserQ1', 'BIGSTRONGPASS', 'testuser@gmail.com', save_tokens=False)
        self.user.register()

    def test_login(self):
        self.user.login()

        self.assertIsNotNone(self.user.access_token)
        self.assertIsNotNone(self.user.id)

    def test_delete(self):
        self.user.delete()
        self.assertRaises(api.exceptions.WrongCredentialsProvidedError, self.user.login)

    def test_refresh_access(self):
        access_before = self.user.access_token
        self.user.refresh_access()
        self.assertNotEqual(access_before, self.user.access_token)

    def test_change_names(self):
        names_before = (self.user._first_name, self.user._last_name)
        self.user.change_names('test', 'testov')
        self.user.login()
        names_after = (self.user._first_name, self.user._last_name)

        self.assertNotEqual(names_before, names_after)

    def test_change_username(self):
        username_before = self.user._username
        self.user.change_username('TestUser1')
        self.user.login()
        self.assertNotEqual(username_before, self.user._username)

    def message_handler(self, msg):
        if msg.text == 'bla bla bla':
            self.bla_bla_got = True

    def test_send_message(self):
        self.bla_bla_got = False
        chat_id = self.user.create_chat('testuserchat')
        self.user.send_message(chat_id, 'bla bla bla')
        self.user.message_handler()(self.message_handler)
        self.user.get_unread_messages(chat_id)
        self.assertTrue(self.bla_bla_got)

    def tearDown(self) -> None:
        try:
            self.user.delete()
        except api.exceptions.WrongCredentialsProvidedError:
            pass
