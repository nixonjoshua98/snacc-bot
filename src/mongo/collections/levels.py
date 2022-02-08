from __future__ import annotations
from typing import TYPE_CHECKING
from src.mongo.models.levels import UserServerLevelModel

if TYPE_CHECKING:
    from src.mongo.client import AsyncMongoClient


class LevelsCollection:
    def __init__(self, client: AsyncMongoClient):
        self.col = client.database["userLevels"]

    async def set_show_level_alerts(self, user_id: str, server_id: str, val: bool):
        await self.col.update_one(
            {
                UserServerLevelModel.Aliases.USER_ID: user_id,
                UserServerLevelModel.Aliases.SERVER_ID: server_id
            },
            {
                "$set": {UserServerLevelModel.Aliases.SHOW_LEVEL_ALERTS: val}
            },
            upsert=True
        )

    async def add_exp(self, user_id: str, server_id: str, exp: int):
        """
        Increment the exp a user has earned in a given server
        :param server_id: Revolt server id
        :param user_id: Revolt user id
        :param exp: Exp gained (or lost)
        """
        search = {
            UserServerLevelModel.Aliases.USER_ID: user_id,
            UserServerLevelModel.Aliases.SERVER_ID: server_id
        }
        update = {
            "$inc": {
                UserServerLevelModel.Aliases.EXP: exp,
            }
        }

        await self.col.update_one(search, update, upsert=True)

    async def get_user(self, user_id: str, server_id: str) -> UserServerLevelModel:
        r = await self.col.find_one({
            UserServerLevelModel.Aliases.USER_ID: user_id,
            UserServerLevelModel.Aliases.SERVER_ID: server_id
        })

        user = UserServerLevelModel.parse_obj(r) if r else UserServerLevelModel.default(user_id, server_id)

        await self._update_user_position(user)

        return user

    async def _update_user_position(self, user: UserServerLevelModel):
        """
        Update the model with the server position using an aggregation (inefficient)
        :param user: User model we are updating
        """
        r = await self.col.aggregate([
            {"$match": {
                "$and": [
                    {UserServerLevelModel.Aliases.SERVER_ID: user.server_id},
                    {UserServerLevelModel.Aliases.EXP: {"$gt": user.exp}}
                ]}},
            {"$count": "numUsersAboveExp"}
        ]).to_list(length=None)

        user.server_position = (r[0] if len(r) > 0 else {}).get("numUsersAboveExp", 0) + 1
