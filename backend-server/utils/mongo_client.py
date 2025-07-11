from typing import Dict
import os
from .mongo_connection import MongoConnection


class MongoHandler:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        self.connection = MongoConnection(
            mongo_uri)
        self.db = self.connection.get_db(db_name=db_name)
        self.collection = self.db[collection_name]

    async def insert(self, json_data: Dict):
        return await self.collection.insert_one(json_data)

    async def get_all(self):
        return await self.collection.find({}, {"_id": 0}).to_list(length=None)

    async def delete_all(self):
        return await self.collection.delete_many({})

    def close(self):
        self.connection.client.close()
