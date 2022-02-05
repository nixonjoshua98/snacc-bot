from __future__ import annotations
from typing import TYPE_CHECKING
from src.mongo.models.economy import UserEconomyProfile
from pymongo import ReturnDocument
import datetime as dt

if TYPE_CHECKING:
    from src.mongo.client import AsyncMongoClient


class EconomyCollection:
    def __init__(self, client: AsyncMongoClient):
        self.col = client.database["economyProfiles"]

    async def get_user(self, user_id: str) -> UserEconomyProfile:
        r = await self.col.find_one({UserEconomyProfile.Aliases.USER_ID: user_id})

        return UserEconomyProfile.parse_obj(r) if r else UserEconomyProfile(user_id=user_id)

    async def inc_currency(self, user_id: str, value: int) -> UserEconomyProfile:
        r = await self.col.find_one_and_update(
            {UserEconomyProfile.Aliases.USER_ID: user_id},
            {"$inc": {UserEconomyProfile.Aliases.CURRENCY: value}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        return UserEconomyProfile.parse_obj(r)

    async def daily_login(
        self,
        user_id: str,
        claim_time: dt.datetime,
        streak: int,
        currency: int
    ) -> UserEconomyProfile:
        """
        Update a user daily login streak
        :param user_id:
        :param claim_time:
        :param streak:
        :param currency:
        :return:
        """
        r = await self.col.find_one_and_update(
            {UserEconomyProfile.Aliases.USER_ID: user_id},
            {
                "$set": {
                    UserEconomyProfile.Aliases.LAST_DAILY_CLAIM: claim_time,
                    UserEconomyProfile.Aliases.DAILY_STREAK: streak
                },
                "$inc": {
                    UserEconomyProfile.Aliases.CURRENCY: currency
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        return UserEconomyProfile.parse_obj(r)

    async def get_top_richest(self, length: int) -> list[UserEconomyProfile]:
        results = await self.col.find().sort(UserEconomyProfile.Aliases.CURRENCY, -1).to_list(length=length)

        return [UserEconomyProfile.parse_obj(r) for r in results]
