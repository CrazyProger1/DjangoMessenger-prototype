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
    def save(model, **key_values):
        try:
            if key_values.get('server_id'):
                instance = model.get(server_id=key_values.get('server_id'))
            else:
                instance = model.get(id=key_values.get('id'))
        except Exception:
            return model.create(**key_values)

        for key, value in key_values.items():
            instance.__setattr__(key, value or instance.__getattribute__(key))
        instance.save()
        return instance

    @staticmethod
    def load(model, **key_values):
        try:
            return model.get(**key_values)
        except Exception:
            return None

    def __del__(self):
        self._connection.close()
