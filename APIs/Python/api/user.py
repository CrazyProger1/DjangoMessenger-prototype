import json
import os
import requests

from .exceptions import *
from .config import *
from .apihelper import *


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
        self.email_address = email_address
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

    def login(self):
        response = self.api_helper.post(
            {
                'username': self.username,
                'password': self.password
            },
            'users/token'
        )

        print(response.json())

        match response.status_code:
            case 200:
                data: dict = response.json()

                self._access_token = data.get('access')
                self._refresh_token = data.get('refresh')
                self._save_tokens()
                return True

            case 401:
                raise WrongCredentials('Password is wrong')

    def register(self):
        response = self.api_helper.post(
            {
                'username': self.username,
                'password': self.password
            },
            'users'
        )

        match response.status_code:
            case 201:
                return True

            case 400:
                raise AlreadyExistsError('A user with that username already exists')

    def authorize(self):
        if self._access_token and self._refresh_token:
            if self._refresh_access():
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
            'users',
            self._access_token
        )

        print(response.status_code, response.text)
