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

                self._access_token = tokens.get('access_token')
                self._refresh_token = tokens.get('refresh_token')

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
                raise AlreadyExistsError('User with the same name already exists')

    def authorize(self):
        try:
            self.register()
        except AlreadyExistsError:
            pass

        return self.login()
