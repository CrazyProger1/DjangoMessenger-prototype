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

    def set_db_attrs(self):
        for cls in BaseModel.__subclasses__():
            cls._meta.database = self._connection

    def __del__(self):
        self._connection.close()
