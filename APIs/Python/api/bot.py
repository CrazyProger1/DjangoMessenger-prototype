from .config import *


class Bot:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.token = kwargs.get('token')
