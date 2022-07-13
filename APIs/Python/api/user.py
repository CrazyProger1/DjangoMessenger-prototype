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
        self._connections = {}

        self._api_helper: APIHelper = APIHelper(self._host)
        self._db_helper: DatabaseHelper = DatabaseHelper()

    @property
    def access_token(self):
        return self._access_token

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

    def _filter_message(self, message: Message, **options):
        if options.get('ignore_my'):
            if self._id == message.sender.id and message.sender.type == 'user':
                return False

    def _handle_message(self, message: Message):
        for handler, options in self._message_handlers.items():
            if self._filter_message(message, **options):
                handler(message)

    def _connect_to_chat(self, chat_id: int, **kwargs):
        connection = self._api_helper.connect_to_chat(
            chat_id=chat_id,
            access_token=self._access_token,
            message_handler=self._handle_message,
            **kwargs)

        self._connections.update({chat_id: connection})
        return connection

    def _save_to_db(self):
        data = {
            'username': self._username,
            'server_id': self._id
        }

        if self._allow_token_saving:
            data.update({
                'access_token': self._access_token,
                'refresh_token': self._refresh_token
            })

        self._db_helper.save(
            UserModel,
            **data
        )

    def _delete_from_db(self):
        instance: UserModel = self._db_helper.load(
            UserModel,
            server_id=self._id,
        )

        if instance:
            instance.delete_instance()

    def _load_tokens_from_db(self) -> UserModel:
        instance: UserModel = self._db_helper.load(
            UserModel,
            username=self._username,
        )
        self._access_token = instance.access_token or self._access_token
        self._refresh_token = instance.refresh_token or self._refresh_token

        return instance

    def change_username(self, username: str):
        if self._api_helper.change_user_data(
                data={
                    'username': username,
                },
                access_token=self._access_token
        ):
            self._username = username
            # save to db
            self._save_to_db()

    def change_names(self, first_name: str, last_name: str):
        if self._api_helper.change_user_data(
                data={
                    'first_name': first_name,
                    'last_name': last_name
                },
                access_token=self._access_token):
            self._first_name = first_name
            self._last_name = last_name
            # save to db
            self._save_to_db()

    def change_password(self, password: str):
        pass

    def send_message(self, chat_id: int, text: str) -> int:
        if not self._connections.get(chat_id):
            self._connect_to_chat(chat_id)

        return self._api_helper.send_message(
            connection=self._connections.get(chat_id),
            text=text,
            sender_private_key=None,
            sender_public_key=None,
            receiver_public_key=None,
            encryption_class=None
        )

    def register(self):
        self._access_token, self._refresh_token = self._api_helper.register(
            username=self._username,
            password=self._password,
            email=self._email,
        )
        self.update_user_info()

    def login(self):
        if self._allow_token_saving:
            self._load_tokens_from_db()
            if self._api_helper.refresh_access(refresh_token=self._refresh_token):
                self.update_user_info()
                return

        self._access_token, self._refresh_token = self._api_helper.login(

            username=self._username,
            password=self._password

        )
        self.update_user_info()

    def delete(self):
        if self._api_helper.delete_user(self._access_token):
            # delete from db
            self._delete_from_db()

    def refresh_access(self):
        self._access_token = self._api_helper.refresh_access(self._refresh_token)

    def update_user_info(self):
        data = self._api_helper.get_user_info(self._access_token)

        self._username = data.get('username')
        self._id = data.get('id')
        self._email = data.get('email')
        self._first_name = data.get('first_name')
        self._last_name = data.get('last_name')
        # save to db
        self._save_to_db()

    def message_handler(self, **options):
        def decorator(func):
            self._message_handlers.update({func: options})
            return func

        return decorator

    def run_polling(self, load_unread_messages: bool = True):
        for chat_id in self._api_helper.get_chat_ids(self._access_token):
            self._connect_to_chat(
                chat_id=chat_id,
                load_unread_messages=load_unread_messages,
                last_read_message=0,

            )

            rel.signal(2, rel.abort)
            rel.dispatch()

    def create_bot(self, name: str) -> Bot:
        return self._api_helper.create_bot(
            name=name,
            access_token=self._access_token
        )

    def create_chat(self, name: str, group: bool = False, private: bool = False) -> int:
        chat_id = self._api_helper.create_chat(
            name=name,
            group=group,
            private=private,
            access_token=self._access_token
        )
        # save to db
        return chat_id

    def add_chat_member(self, chat_id: int, user_id: int = None, bot_id: int = None):
        return self._api_helper.add_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            bot_id=bot_id,
            access_token=self._access_token
        )
