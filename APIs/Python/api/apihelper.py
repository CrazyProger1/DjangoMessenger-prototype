import requests
from .config import *

_instances = {}


def singleton(cls):
    def wrapper(*args, **kwargs):
        if cls in _instances.keys():
            return _instances.get(cls)

        _instances.update({cls: cls(*args, **kwargs)})
        return _instances.get(cls)

    return wrapper


@singleton
class APIHelper:
    def __init__(self):
        self.host = HOST

    def set_host(self, host: str):
        self.host = host

    def _form_url(self, obj: str):
        return self.host + 'api/' + API_VERSION + '/' + obj + '/'

    @staticmethod
    def _form_headers(access_token: str = None) -> dict | None:
        if not access_token:
            return None

        headers = {
            'Authorization': TOKEN_KEYWORD + ' ' + access_token
        }
        return headers

    def post(self, json: dict, obj: str = 'users', access_token: str = None) -> requests.Response:
        return requests.post(
            url=self._form_url(obj),
            json=json,
            headers=self._form_headers(access_token)
        )

    def put(self,
            json: dict,
            obj: str = 'users',
            access_token: str = None,
            partially: bool = False) -> requests.Response:

        if not partially:
            return requests.put(
                url=self._form_url(obj),
                json=json,
                headers=self._form_headers(access_token)
            )
        return requests.patch(
            url=self._form_url(obj),
            json=json,
            headers=self._form_headers(access_token)
        )

    def get(self, obj: str = 'users', access_token: str = None):
        return requests.get(
            url=self._form_url(obj),
            headers=self._form_headers(access_token)
        )
