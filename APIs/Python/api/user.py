import json

from typing import Iterable

from .apihelper import *
from .bot import *
from .dbhelper import *
from .message import *
from .models import *


class User:
    def __init__(
            self,
            username: str = None,
            password: str = None,
            email_address: str = None,
            save_tokens=False,
            host: str = None):

        self._username = username
        self._password = password
        self._email = email_address
        self._first_name = None
        self._last_name = None
        self._id = None
        self._access_token = None
        self._refresh_token = None

        self._allow_token_saving = save_tokens
        self._host = host

        self._message_handlers = {}

        self._api_helper: APIHelper = APIHelper(self._host)
        self._db_helper: DatabaseHelper = DatabaseHelper()

        self._api_helper.set_message_handler(self._filter_message)

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    def _filter_message(self, message: Message):
        for handler, options in self._message_handlers.items():
            if options.get('ignore_my'):
                if self._id == message.sender.id and message.sender.type == 'user':
                    continue

            handler(message)

    def change_username(self, username: str):
        if self._api_helper.change_user_data(
                data={
                    'username': username,
                }):
            self._username = username
            # save to db

    def change_names(self, first_name: str, last_name: str):
        if self._api_helper.change_user_data(
                data={
                    'first_name': first_name,
                    'last_name': last_name
                }):
            self._first_name = first_name
            self._last_name = last_name
            # save to db

    def change_password(self, password: str):
        pass

    def send_message(self, chat_id: int, text: str) -> int:
        return self._api_helper.send_message(
            chat_id=chat_id,
            text=text,
            sender_private_key=None,
            sender_public_key=None,
            receiver_public_key=None,
            encryption_class=None
        )

    def register(self):
        self._api_helper.register(

            username=self._username,
            password=self._password,
            email=self._email

        )
        self.update_user_info()

    def login(self):
        # self._api_helper.set_tokens(
        #     access_token=,
        #     refresh_token=
        # )
        # if self._api_helper.refresh_access():
        #     self.update_user_info()
        #     return

        self._api_helper.login(

            username=self._username,
            password=self._password

        )
        self.update_user_info()

    def delete(self):
        if self._api_helper.delete_user():
            pass
            # delete from db

    def refresh_access(self):
        self._api_helper.refresh_access()

    def update_user_info(self):
        data = self._api_helper.get_user_info()

        self._username = data.get('username')
        self._id = data.get('id')
        self._email = data.get('email')
        self._first_name = data.get('first_name')
        self._last_name = data.get('last_name')
        # save to db

    def message_handler(self, **options):
        def decorator(func):
            self._message_handlers.update({func: options})
            return func

        return decorator

    def run_polling(self, load_unread_messages: bool = True):
        for chat_id in self._api_helper.get_chat_ids():
            self._api_helper.connect_to_chat(
                chat_id=chat_id,
                load_unread_messages=load_unread_messages,
                last_read_message=0  # load from db
            )

        rel.signal(2, rel.abort)
        rel.dispatch()

    def create_bot(self, name: str) -> Bot:
        return self._api_helper.create_bot(
            name=name
        )

    def create_chat(self, name: str, group: bool = False, private: bool = False) -> int:
        return self._api_helper.create_chat(
            name=name,
            group=group,
            private=private
        )
        # save to db

    def add_chat_member(self, chat_id: int, user_id: int = None, bot_id: int = None):
        return self._api_helper.add_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            bot_id=bot_id
        )
