import json
import requests
import websocket
import rel
import os

from .config import *
from .exceptions import *
from .singleton import *
from .encryption import *
from .message import *
from .bot import *

from typing import Iterable, Type, Callable


@singleton
class APIHelper:
    SUCCESS_CODES = (200, 201)

    def __init__(self, host: str = None):
        self._host = HOST or host
        self._adjust_websocket_host()

    def _adjust_websocket_host(self):
        if 'https' in self._host:
            self.websocket_host = self._host.replace('https', 'ws')
        elif 'http' in self._host:
            self.websocket_host = self._host.replace('http', 'ws')
        else:
            raise InvalidHostError('The host must look like http://... or https://...')

    def _form_url(self, obj: str):
        return self._host + 'api/' + API_VERSION + '/' + obj + '/'

    @staticmethod
    def _form_headers(access_token: str) -> dict | None:
        if not access_token:
            return None

        headers = {
            'Authorization': TOKEN_KEYWORD + ' ' + access_token
        }
        return headers

    def _handle_errors(self, response, **exception_classes) -> requests.Response:
        if response.status_code not in self.SUCCESS_CODES:

            exception = exception_classes.get(f'error{response.status_code}')
            if not exception:
                return response

            errors = response.json()
            error_key = tuple(errors.keys())[0]

            error_text = errors[error_key]
            if isinstance(error_text, list) or isinstance(error_text, tuple):
                error_text = error_text[0]

            raise exception(error_key, error_text)

        return response

    @staticmethod
    def _define_message_type(attach_files: bool, files: Iterable[str]):
        if not attach_files:
            return 'text'

        extensions = map(lambda filename: filename.splitext()[1], files)
        print(extensions)
        return 'document'

    def set_host(
            self,
            host: str):

        self._host = host
        self._adjust_websocket_host()

    def post(
            self,
            data: dict,
            obj: str = 'users',
            access_token: str = None,
            **exception_classes) -> requests.Response:

        return self._handle_errors(requests.post(
            url=self._form_url(obj),
            json=data,
            headers=self._form_headers(access_token=access_token)
        ), **exception_classes)

    def put(
            self,
            data: dict,
            obj: str = 'users',
            partially: bool = False,
            access_token: str = None,
            **exception_classes
    ) -> requests.Response:

        if not partially:
            return self._handle_errors(requests.put(
                url=self._form_url(obj),
                json=data,
                headers=self._form_headers(access_token=access_token)), **exception_classes)
        return self._handle_errors(requests.patch(
            url=self._form_url(obj),
            json=data,
            headers=self._form_headers(access_token=access_token)), **exception_classes)

    def get(
            self,
            obj: str = 'users',
            params: dict = None,
            access_token: str = None,
            **exception_classes):

        return self._handle_errors(requests.get(
            url=self._form_url(obj),
            headers=self._form_headers(access_token=access_token),
            params=params), **exception_classes)

    def delete(
            self,
            obj: str = 'users',
            access_token: str = None,
            **exception_classes):

        return self._handle_errors(
            requests.delete(
                url=self._form_url(obj),
                headers=self._form_headers(access_token=access_token),
            ),
            **exception_classes
        )

    @staticmethod
    def _handle_ws_message(
            handler: Callable,
            data: dict):

        message = Message.de_json(data.get('message'))
        sender = Sender.de_json(data.get('sender'))
        message.sender = sender
        handler(message)

    def connect_to_chat(
            self,
            chat_id: int, load_unread_messages: bool = False,
            last_read_message: int = 0,
            access_token: str = None,
            message_handler: Callable[[Message], None] = None):

        if load_unread_messages:
            for unread_msg in self.get_unread_messages(
                    chat_id=chat_id,
                    last_read_message=last_read_message,
                    access_token=access_token):

                if message_handler:
                    self._handle_ws_message(message_handler, unread_msg)

        websocket.enableTrace(False)

        ws = websocket.WebSocketApp(
            url=f"{self.websocket_host}ws/chat/{chat_id}/",
            header=self._form_headers(access_token=access_token)
        )

        ws.run_forever(dispatcher=rel)

        if message_handler:
            ws.on_message = lambda conn, msg: self._handle_ws_message(message_handler, json.loads(msg))

        return ws

    def send_message(
            self,
            connection,
            text: str = None,
            attach_files: bool = False,
            files: Iterable[str] = (),
            files_password: str = None,
            is_reply: bool = False,
            reply_on: int = None,
            is_initial: bool = False,
            sender_private_key: bytes = None,
            sender_public_key: bytes = None,
            receiver_public_key: bytes = None,
            encryption_class: Type[EncryptionType] | None = RSA) -> int:

        body = {
            'encryption_type': encryption_class.__class__.__name__,
            'initial': is_initial,
            'reply': is_reply,
            'reply_on': reply_on
        }

        if encryption_class:
            if not is_initial:
                body.update({
                    'text': encryption_class.encrypt_message(text, receiver_public_key),
                    'files_password': encryption_class.encrypt_message(files_password, receiver_public_key),
                    'sign': encryption_class.sign(text, sender_private_key)
                })
            else:
                body.update({
                    'text': sender_public_key
                })

        else:
            body.update({
                'text': text
            })

        body.update({
            'type': self._define_message_type(attach_files, files)
        })

        connection.send(json.dumps(body))

    def login(
            self,
            username: str,
            password: str) -> tuple[str, str]:

        response = self.post(
            {
                'username': username,
                'password': password,
            },
            'users/token',
            error401=WrongCredentialsProvidedError
        )

        if response.status_code == 200:
            data: dict = response.json()
            return data.get('access'), data.get('refresh')

    def get_user_info(
            self,
            access_token: str) -> dict:

        response = self.get(
            'users/me',
            access_token=access_token
        )

        data: dict = response.json()
        return data

    def refresh_access(
            self,
            refresh_token: str) -> str:
        response = self.post(
            {
                'refresh': refresh_token
            },
            'users/token/refresh',
            error401=RefreshExpiredError
        )

        if response.status_code == 200:
            data: dict = response.json()
            return data.get('access')

    def register(
            self,
            username: str,
            password: str,
            email: str) -> tuple[str, str]:

        response = self.post(
            {
                'username': username,
                'password': password,
                'email': email
            },
            'users',
            error400=WrongDataProvidedError,
        )

        if response.status_code == 201:
            return self.login(
                username=username,
                password=password
            )

    def change_user_data(
            self,
            data: dict,
            access_token: str) -> bool:

        response = self.put(
            data,
            'users/me',
            partially=True,
            error401=WrongCredentialsProvidedError,
            access_token=access_token
        )

        if response.status_code == 200:
            return True

    def delete_user(
            self,
            access_token: str) -> bool:

        response = self.delete(
            f'users/me',
            error401=WrongCredentialsProvidedError,
            access_token=access_token
        )

        if response.status_code == 204:
            return True

    def get_unread_messages(
            self,
            chat_id: int,
            access_token: str,
            last_read_message: int = 0, ) -> Iterable[dict]:

        response = self.get(
            f'chats/{chat_id}/messages',
            last_read=last_read_message,
            access_token=access_token
        )

        if response.status_code == 200:
            messages_data = response.json().get('results')
            for message_data in messages_data:
                yield message_data

    def get_chat_ids(
            self,
            access_token: str) -> Iterable[int]:

        response = self.get(
            obj='chats/members/my',
            access_token=access_token
        )
        results = response.json().get('results')

        if response.status_code == 200:
            for result in results:
                yield result.get('chat')

    def create_bot(
            self,
            name: str,
            access_token: str) -> Bot:

        response = self.post(
            {
                'name': name
            },
            obj='bots',
            error400=WrongDataProvidedError,
            error401=WrongCredentialsProvidedError,
            access_token=access_token
        )

        if response.status_code == 201:
            data = response.json()

            bot = Bot(**data)
            return bot

    def create_chat(
            self,
            name: str,
            access_token: str,
            group: bool = False,
            private: bool = False) -> int:

        response = self.post(
            {
                'name': name,
                'group': group,
                'private': private
            },
            'chats',
            access_token=access_token,
            error400=WrongDataProvidedError
        )
        if response.status_code == 201:
            data = response.json()

            chat_id = data.get('id')
            return chat_id

    def add_chat_member(
            self,
            chat_id: int,
            access_token: str,
            user_id: int = None,
            bot_id: int = None):

        response = self.post(
            {
                'user': user_id,
                'bot': bot_id

            },
            f'chats/{chat_id}/members',
            error400=WrongDataProvidedError,
            error403=ChatMemberError,
            access_token=access_token
        )

        if response.status_code == 201:
            return True
