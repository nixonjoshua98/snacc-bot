from __future__ import annotations
from typing import TYPE_CHECKING
from motor.motor_asyncio import AsyncIOMotorClient

from src.mongo.collections import LevelsCollection, EconomyCollection, ServerConfigCollection

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorDatabase

    from src.models.config import BotConfiguration


class AsyncMongoClient:
    def __init__(self, config: BotConfiguration):

        # Clients
        self.__client: AsyncIOMotorClient = AsyncIOMotorClient(config.mongo.connection)

        # Databases
        self.database: AsyncIOMotorDatabase = self.__client[config.mongo.database_name]

        # Collections
        self.servers = ServerConfigCollection(self)
        self.levels = LevelsCollection(self)
        self.economy = EconomyCollection(self)

