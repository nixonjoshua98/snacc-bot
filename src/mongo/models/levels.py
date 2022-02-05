from pydantic import Field
from src.models import BaseModel
import functools as ft


def _level_formula(lvl: int): return 5 * ((lvl - 1) ** 2) + (50 * (lvl - 1)) + 100


class UserServerLevelModel(BaseModel):

    class Aliases:
        USER_ID = "userId"
        SERVER_ID = "serverId"
        EXP = "expEarned"

    user_id: str = Field(..., alias=Aliases.USER_ID)
    server_id: str = Field(..., alias=Aliases.SERVER_ID)
    exp: int = Field(0, alias=Aliases.EXP)

    @property
    def level(self) -> int:
        return self.level_from_exp(self.exp)

    @staticmethod
    @ft.cache
    def exp_from_level(level: int):
        return sum(_level_formula(lvl) for lvl in range(1, level))

    @staticmethod
    def level_from_exp(exp: int):
        level = 1

        while exp > 0:
            levelup_exp = _level_formula(level)

            if exp >= levelup_exp:
                level += 1

            exp -= levelup_exp

        return level

    @classmethod
    def default(cls, user_id: str, server_id: str):
        return cls(user_id=user_id, server_id=server_id)
