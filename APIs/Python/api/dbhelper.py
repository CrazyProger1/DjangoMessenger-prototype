import peewee
from .config import *
from .models import *
from .singleton import *


@singleton
class DatabaseHelper:
    def __init__(self, path: str = None):
        self._db_path = path or DB_PATH
        self._connection = peewee.SqliteDatabase(self._db_path)
        self._cursor = self._connection.cursor()
        self.set_db_attrs()
        self._connection.create_tables((BaseModel.__subclasses__()))

    def get_connection(self) -> peewee.SqliteDatabase:
        return self._connection

    def set_db_attrs(self):
        for cls in BaseModel.__subclasses__():
            cls._meta.database = self._connection

    @staticmethod
    def save(model, instance=None, **data):
        if not instance:
            if data.get('server_id'):
                instance = model.get_or_none(server_id=data.get('server_id'))
            else:
                instance = model.get_or_none(id=data.get('id'))

            if not instance:
                return model.create(**data)

        for key, value in data.items():
            instance.__setattr__(key, value or instance.__getattribute__(key))

        instance.save()
        return instance

    @staticmethod
    def load(model, **known_data):
        return model.get_or_none(**known_data)

    def __del__(self):
        self._connection.close()
