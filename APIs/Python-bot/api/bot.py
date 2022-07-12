from .apihelper import APIHelper
from .exceptions import *
from .sender import *
from .message import *

from typing import Iterable

import json
import websocket
import rel


class Bot:
    def __init__(self, token: str, host: str = None):
        self._token = token
        self._host = host

        self._name: str | None = None
        self._id: int | None = None
        self._creator_id: int | None = None

        self._message_handlers = {}
        self._connections = {}

        self._api_helper: APIHelper = APIHelper(self._host)

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def creator_id(self):
        return self._creator_id

    @property
    def token(self):
        return self._token

    def authorize(self):
        response = self._api_helper.get(
            'bots/me',
            self._token,
            error401=WrongCredentialsProvidedError
        )

        if response.status_code == 200:
            data: dict = response.json()
            self._id = data.get('id')
            self._creator_id = data.get('creator')
            self._name = data.get('name')

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
            connection = self._api_helper.connect_to_chat(chat_id, self._token)
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

    def message_handler(self, **options):
        def decorator(func):
            self._message_handlers.update({func: options})
            return func

        return decorator

    def get_chat_ids(self) -> Iterable[int]:
        response = self._api_helper.get(
            'chats/members/my',
            self._token
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
            self._token,
            last_read=self._load_last_read_message()
        )

        if response.status_code == 200:
            messages_data = response.json().get('results')
            for message_data in messages_data:
                self._handle_message(None, message_data)

    def run_polling(self, load_unread_messages: bool = True):
        for chat_id in self.get_chat_ids():
            connection = self._api_helper.connect_to_chat(chat_id, self._token)
            self._connections.update({chat_id: connection})
            connection.on_message = self._handle_message
            if load_unread_messages:
                self.get_unread_messages(chat_id)

        rel.signal(2, rel.abort)
        rel.dispatch()
