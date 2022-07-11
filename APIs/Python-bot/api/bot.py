from .apihelper import APIHelper
from .exceptions import *


class Bot:
    def __init__(self, token: str, host: str = None):
        self.token = token
        self.host = host

        self.name: str | None = None
        self.id: int | None = None
        self.creator_id: int | None = None

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
