import json
import os
import requests
from typing import Iterable

from .exceptions import *
from .config import *
from .apihelper import *
from .bot import *
from .message import *


class User:
    def __init__(
            self,
            username: str = None,
            password: str = None,
            email_address: str = None,
            session_filepath: str = 'session.json',
            save_tokens: bool = True,
            host: str = None):
        self.username = username
        self.password = password
        self.email = email_address
        self.session_filepath = session_filepath
        self.save_tokens = save_tokens
        self.host = host

        self.id: int | None = None
        self.first_name: str | None = None
        self.last_name: str | None = None

        self._access_token: str | None = None
        self._refresh_token: str | None = None

        self._message_handlers = {}
        self._connections = {}

        self._api_helper: APIHelper = APIHelper(self.host)

        self._load_tokens()

    def _load_tokens(self):
        if not self.save_tokens:
            return

        if os.path.exists(self.session_filepath):
            with open(self.session_filepath, 'r') as session_file:
                try:
                    tokens: dict = json.load(session_file)
                except json.decoder.JSONDecodeError:
                    raise SessionLoadError('Session file has invalid format')

                self._access_token = tokens.get('access')
                self._refresh_token = tokens.get('refresh')

    def _save_tokens(self):
        if not self.save_tokens:
            return

        with open(self.session_filepath, 'w') as session_file:
            json.dump(
                {
                    'access': self._access_token,
                    'refresh': self._refresh_token
                },
                session_file
            )

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
        self._save_tokens()
        return True

    def _grab_user_info(self):
        response = self._api_helper.get(
            'users/me',
            self._access_token
        )

        data: dict = response.json()
        self.username = data.get('username')
        self.id = data.get('id')
        self.email = data.get('email')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        return True

    def login(self):
        response = self._api_helper.post(
            {
                'username': self.username,
                'password': self.password
            },
            'users/token',
            error401=WrongCredentialsProvidedError
        )

        data: dict = response.json()

        self._access_token = data.get('access')
        self._refresh_token = data.get('refresh')
        self._save_tokens()
        self._grab_user_info()
        return True

    def register(self):
        response = self._api_helper.post(
            {
                'username': self.username,
                'password': self.password,
                'email': self.email
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
                self.first_name = first_name
                self.last_name = last_name
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
                self.username = username
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
                if self.id == sender_data.get('id'):
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

    def run_polling(self, load_unread_messages: bool = True):
        for chat_id in self.get_chat_ids():
            connection = self._api_helper.connect_to_chat(chat_id, self._access_token)
            self._connections.update({chat_id: connection})
            connection.on_message = self._handle_message
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
            connection = self._api_helper.connect_to_chat(chat_id, self.access_token)
            self._connections.update({chat_id: connection})

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

    @property
    def access_token(self):
        return self._access_token

    def delete(self):
        response = self._api_helper.delete(
            f'users/{self.id}',
            self._access_token,
            error401=WrongCredentialsProvidedError
        )

        if response.status_code == 204:
            return True
