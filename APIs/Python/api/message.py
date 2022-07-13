from .sender import Sender
from .serializable import Serializable
import json


class Message(Serializable):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id') or kwargs.get('pk')
        self.chat_id = kwargs.get('chat') or kwargs.get('chat_id')
        self.type = kwargs.get('type')
        self.text = kwargs.get('text')
        self.sending_datetime = kwargs.get('sending_datetime')
        self.sender: Sender | None = None

    @staticmethod
    def de_json(data: dict):
        return Message(**data)
