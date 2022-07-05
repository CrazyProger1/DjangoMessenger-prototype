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

    def post(self, json: dict, obj: str = 'users') -> requests.Response:
        return requests.post(self.host + 'api/' + API_VERSION + '/' + obj + '/', json=json)
