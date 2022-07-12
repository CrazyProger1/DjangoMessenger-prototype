import json
import os
import requests
import peewee

from typing import Iterable

from .exceptions import *
from .config import *
from .apihelper import *
from .dbhelper import *
from .bot import *
from .message import *
from .models import *


class User:
    def __init__(
            self,
            username: str = None,
            password: str = None,
            email_address: str = None,
            session_filepath: str = 'session.json',
            save_tokens: bool = True,
            host: str = None):

        self._username = username
        self._password = password
        self._email = email_address
        self._session_filepath = session_filepath
        self._allow_tokens_saving = save_tokens
        self._host = host

        self._id: int | None = None
        self._first_name: str | None = None
        self._last_name: str | None = None

        self._access_token: str | None = None
        self._refresh_token: str | None = None

        self._message_handlers = {}
        self._connections = {}

        self._api_helper: APIHelper = APIHelper(self._host)
        self._db_helper: DatabaseHelper = DatabaseHelper()

        self._load_tokens()

    def get_local_database(self) -> peewee.SqliteDatabase:
        return self._db_helper.get_connection()

    def _save_user_to_db(self):
        self._db_helper.save(
            model=UserModel,
            username=self._username,
            server_id=self._id,
            access_token=self._access_token if self._allow_tokens_saving else None,
            refresh_token=self._refresh_token if self._allow_tokens_saving else None
        )

    def _delete_user_from_db(self):
        user = self._db_helper.load(UserModel, server_id=self._id)
        if user:
            user.delete_instance()

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
    def access_token(self):
        return self._access_token

    @property
    def last_name(self):
        return self._last_name

    def _load_tokens(self):
        if not self._allow_tokens_saving:
            return

        user: UserModel = self._db_helper.load(
            UserModel,
            username=self._username
        )
        if user:
            self._access_token = user.access_token
            self._refresh_token = user.refresh_token

    def refresh_access(self):
        response = self._api_helper.post(
            {
                'refresh': self._refresh_token
            },
            'users/token/refresh',
            error401=RefreshExpiredError
        )
        data: dict = response.json()

        self._access_token = data.get('access')
        return True

    def _grab_user_info(self):
        response = self._api_helper.get(
            'users/me',
            self._access_token
        )

        data: dict = response.json()
        self._username = data.get('username')
        self._id = data.get('id')
        self._email = data.get('email')
        self._first_name = data.get('first_name')
        self._last_name = data.get('last_name')
        self._save_user_to_db()
        return True

    def login(self):
        try:
            if self._allow_tokens_saving and self._refresh_token:
                self.refresh_access()
                self._grab_user_info()
                return
        except RefreshExpiredError:
            pass

        response = self._api_helper.post(
            {
                'username': self._username,
                'password': self._password
            },
            'users/token',
            error401=WrongCredentialsProvidedError
        )

        data: dict = response.json()

        self._access_token = data.get('access')
        self._refresh_token = data.get('refresh')
        self._grab_user_info()
        return True

    def register(self):
        response = self._api_helper.post(
            {
                'username': self._username,
                'password': self._password,
                'email': self._email
            },
            'users',
            error400=WrongDataProvidedError
        )

        if response.status_code == 201:
            return self.login()

    def change_names(self, first_name: str, last_name: str):
        response = self._api_helper.put(
            {
                'first_name': first_name,
                'last_name': last_name
            },
            'users/me',
            self._access_token,
            partially=True,
            error401=WrongCredentialsProvidedError
        )

        match response.status_code:
            case 200:
                self._first_name = first_name
                self._last_name = last_name
                return True

    def change_username(self, username: str):
        response = self._api_helper.put(
            {
                'username': username,
            },
            'users/me',
            self._access_token,
            partially=True,
            error401=WrongCredentialsProvidedError
        )

        match response.status_code:
            case 200:
                self._username = username
                return True

    def create_bot(self, name: str) -> Bot:
        response = self._api_helper.post(
            {
                'name': name
            },
            'bots',
            self._access_token,
            error400=WrongDataProvidedError,
            error401=WrongCredentialsProvidedError
        )

        match response.status_code:
            case 201:
                data = response.json()

                bot = Bot(**data)
                return bot

    def create_chat(self, name: str, group: bool = False, private: bool = False) -> int:
        response = self._api_helper.post(
            {
                'name': name,
                'group': group,
                'private': private
            },
            'chats',
            self._access_token,
            error400=WrongDataProvidedError
        )
        match response.status_code:
            case 201:
                data = response.json()

                chat_id = data.get('id')
                return chat_id

    def add_chat_member(self, chat_id: int, user_id: int = None, bot_id: int = None):
        response = self._api_helper.post(
            {
                'user': user_id,
                'bot': bot_id

            },
            f'chats/{chat_id}/members',
            self._access_token,
            error400=WrongDataProvidedError,
            error403=ChatMemberError
        )

        if response.status_code == 201:
            return True

    def message_handler(self, **options):
        def decorator(func):
            self._message_handlers.update({func: options})
            return func

        return decorator

    def get_chat_ids(self) -> Iterable[int]:
        response = self._api_helper.get(
            'chats/members/my',
            self._access_token
        )
        results = response.json().get('results')

        if response.status_code == 200:
            for result in results:
                yield result.get('chat')

    def _handle_message(self, connection, string_data):
        if connection:
            data: dict = json.loads(string_data)
            message_data = data.get('message')
            sender_data = data.get('sender')
        else:
            message_data = string_data.get('message')
            sender_data = string_data.get('sender')

        for handler, options in self._message_handlers.items():
            if options.get('ignore_my'):
                if self._id == sender_data.get('id'):
                    continue

            handler(Message(**message_data, sender=Sender(**sender_data)))
            self._save_last_read_message(message_data.get('id'))

    def _save_last_read_message(self, message_id: int):  # test variant
        with open('lrm', 'w') as f:
            f.write(str(message_id))

    def _load_last_read_message(self):  # test variant
        try:
            with open('lrm', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            self._save_last_read_message(0)

    def get_unread_messages(self, chat_id: int):
        response = self._api_helper.get(
            f'chats/{chat_id}/messages',
            self._access_token,
            last_read=self._load_last_read_message()
        )

        if response.status_code == 200:
            messages_data = response.json().get('results')
            for message_data in messages_data:
                self._handle_message(None, message_data)

    def _connect_to_chat(self, chat_id: int):
        connection = self._api_helper.connect_to_chat(chat_id, self._access_token)
        self._connections.update({chat_id: connection})
        connection.on_message = self._handle_message
        return connection

    def run_polling(self, load_unread_messages: bool = True):
        for chat_id in self.get_chat_ids():
            self._connect_to_chat(chat_id)

            if load_unread_messages:
                self.get_unread_messages(chat_id)

        rel.signal(2, rel.abort)
        rel.dispatch()

    def _send_message(self,
                      chat_id: int,
                      text: str,
                      attach_files: bool = False,
                      files: Iterable[str] = (),
                      files_password: str = None,
                      is_reply: bool = False,
                      reply_on: int = None,
                      initial_message: bool = False
                      ):

        connection: websocket.WebSocketApp = self._connections.get(chat_id)

        if not connection:
            connection = self._connect_to_chat(chat_id)

        if not attach_files:
            message_string = json.dumps({
                'type': 'text',
                'text': text,
                'files_password': files_password,
                'encryption_type': 'RSA',
                'initial': initial_message,
                'is_reply': is_reply,
                'reply_on': reply_on
            })
            connection.send(message_string)

    def send_message(self, chat_id: int, text: str):
        self._send_message(chat_id, text)

    def delete(self):

        response = self._api_helper.delete(
            f'users/{self._id}',
            self._access_token,
            error401=WrongCredentialsProvidedError
        )

        if response.status_code == 204:
            return True

        self._delete_user_from_db()
