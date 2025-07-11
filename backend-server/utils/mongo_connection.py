from motor.motor_asyncio import AsyncIOMotorClient
from .types import Singleton


class MongoConnection(metaclass=Singleton):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)

    def get_db(self, db_name: str):
        return self.client[db_name]
