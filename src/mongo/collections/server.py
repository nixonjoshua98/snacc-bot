from __future__ import annotations
from typing import TYPE_CHECKING
from src.mongo.models.server import ServerConfigModel

if TYPE_CHECKING:
    from src.mongo.client import AsyncMongoClient


class ServerConfigCollection:
    def __init__(self, client: AsyncMongoClient):
        self.servers = client.database["serversConfig"]

    async def get_server(self, server_id: str) -> ServerConfigModel:
        r = await self.servers.find_one({ServerConfigModel.Aliases.SERVER_ID: server_id})

        return ServerConfigModel.parse_obj(r) if r else ServerConfigModel(server_id=server_id)

    async def set_prefix(self, server_id: str, prefix: str):
        await self.servers.update_one(
            {ServerConfigModel.Aliases.SERVER_ID: server_id},
            {"$set": {ServerConfigModel.Aliases.PREFIX: prefix}},
            upsert=True
        )
