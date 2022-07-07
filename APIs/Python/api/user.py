import json
import os
import requests

from .exceptions import *
from .config import *
from .apihelper import *
from .bot import *


class User:
    def __init__(
            self,
            username: str = None,
            password: str = None,
            email_address: str = None,
            session_filepath: str = 'session.json',
            save_tokens: bool = True,
            host: str = 'http://127.0.0.1:8000/'):
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

        self.api_helper: APIHelper = APIHelper()

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

    def _refresh_access(self):
        response = self.api_helper.post(
            {
                'refresh': self._refresh_token
            },
            'users/token/refresh'
        )

        match response.status_code:
            case 200:
                data: dict = response.json()

                self._access_token = data.get('access')
                self._save_tokens()
                return True
            case 401:
                raise RefreshExpiredError('Refresh token is expired')

    def _grab_user_info(self):
        response = self.api_helper.get(
            'users/me',
            self._access_token
        )

        match response.status_code:
            case 200:
                data: dict = response.json()
                self.username = data.get('username')
                self.id = data.get('id')
                self.email = data.get('email')
                self.first_name = data.get('first_name')
                self.last_name = data.get('last_name')
                return True

    def login(self):
        response = self.api_helper.post(
            {
                'username': self.username,
                'password': self.password
            },
            'users/token'
        )

        match response.status_code:
            case 200:
                data: dict = response.json()

                self._access_token = data.get('access')
                self._refresh_token = data.get('refresh')
                self._save_tokens()
                self._grab_user_info()
                return True

            case 401:
                raise WrongCredentials('Password is wrong')

    def register(self):
        response = self.api_helper.post(
            {
                'username': self.username,
                'password': self.password,
                'email': self.email
            },
            'users'
        )

        match response.status_code:
            case 201:
                return True

            case 400:
                raise AlreadyExistsError('User with that username already exists')

    def authorize(self):
        if self._access_token and self._refresh_token:
            if self._refresh_access():
                self._grab_user_info()
                return True

        try:
            self.register()
        except AlreadyExistsError:
            pass

        return self.login()

    def change_names(self, first_name: str, last_name: str):
        response = self.api_helper.put(
            {
                'first_name': first_name,
                'last_name': last_name
            },
            'users/me',
            self._access_token,
            partially=True
        )

        match response.status_code:
            case 200:
                return True
            case 401:
                self._refresh_access()
                return self.change_names(first_name, last_name)

    def change_username(self, username: str):
        pass

    def create_bot(self, name: str) -> Bot:
        response = self.api_helper.post(
            {
                'name': name
            },
            'bots',
            self._access_token
        )

        match response.status_code:
            case 201:
                data = response.json()

                bot = Bot(**data)
                return bot

            case 400:
                raise AlreadyExistsError('Bot with this bot name already exists')

            case 401:
                self._refresh_access()
                return self.create_bot(name)

    def create_chat(self, name: str, group: bool = False, private: bool = False) -> int:
        response = self.api_helper.post(
            {
                'name': name,
                'group': group,
                'private': private
            },
            'chats',
            self._access_token
        )
        match response.status_code:
            case 201:
                data = response.json()

                chat_id = data.get('id')
                return chat_id

            case 400:
                raise AlreadyExistsError('Chat with that name already exists')

    def add_chat_member(self, chat_id: int, username: str = None, user_id: int = None):
        response = self.api_helper.post(
            {
                'user': user_id

            },
            f'chats/{chat_id}/members',
            self._access_token
        )

        match response.status_code:
            case 201:
                return True
            case 400:
                raise AlreadyExistsError('Member already in chat')

    @property
    def access_token(self):
        return self._access_token
