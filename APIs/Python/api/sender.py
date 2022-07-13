import json

from .serializable import Serializable


class Sender(Serializable):
    def __init__(self, **kwargs):
        self.type = kwargs.get('type')
        self.id = kwargs.get('id') or kwargs.get('pk')
        self.name = kwargs.get('name')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @staticmethod
    def de_json(data: dict):
        return Sender(**data)
