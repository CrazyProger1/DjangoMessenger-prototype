from .apihelper import APIHelper
from .exceptions import *

from typing import Iterable

import json
import websocket


class Bot:
    def __init__(self, token: str, host: str = None):
        self.token = token
        self.host = host

        self.name: str | None = None
        self.id: int | None = None
        self.creator_id: int | None = None

        self._message_handlers = {}
        self._connections = {}

        self._api_helper: APIHelper = APIHelper(self.host)

    def authorize(self):
        response = self._api_helper.get(
            'bots/me',
            self.token,
            error401=WrongCredentialsProvidedError
        )

        if response.status_code == 200:
            data: dict = response.json()
            self.id = data.get('id')
            self.creator_id = data.get('creator')
            self.name = data.get('name')

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
            connection = self._api_helper.connect_to_chat(chat_id, self.token)
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
