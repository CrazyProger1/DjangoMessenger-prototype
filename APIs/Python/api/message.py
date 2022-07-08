from .sender import Sender


class Message:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.chat_id = kwargs.get('chat')
        self.type = kwargs.get('type')
        self.text = kwargs.get('text')
        self.sending_datetime = kwargs.get('sending_datetime')
        self.sender: Sender = kwargs.get('sender')
