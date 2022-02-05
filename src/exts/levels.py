from __future__ import annotations
from typing import TYPE_CHECKING
import datetime as dt
import random
import multipledispatch as md
import defectio
from defectio.ext import commands
from src import core
from collections import defaultdict
import contextlib
from defectio import Message


if TYPE_CHECKING:
    from src.models.config import LevelsConfiguration
    from src.mongo.models.levels import UserServerLevelModel


class Levels(core.Cog):

    def __init__(self, bot):
        super(Levels, self).__init__(bot)

        self.config: LevelsConfiguration = self.bot.config.cogs.levels

        # { "serverId": { "userId": 12/01/19 } }
        self.timers: defaultdict[str, dict[str, dt.datetime]] = defaultdict(dict)

    @core.Cog.listener()
    async def on_server_message(self, message: Message):
        if self._can_reward_exp(message):
            self._set_user_timer(message)

            exp_gained = await self._give_random_exp(message)
            user = await self._get_user_server_info(message)

            if await self._has_user_level_up(user, exp_gained):
                await self.on_user_levelup(message, user)

    @commands.command("level")
    async def level(self, ctx: core.Context):
        """ View your current level and exp required for the next level """
        user = await self._get_user_server_info(ctx)

        exp_next_level = user.exp_from_level(user.level + 1)

        await ctx.reply(f"You are level **{user.level}** (**{user.exp}XP/{exp_next_level}XP**)")

    @classmethod
    async def on_user_levelup(cls, message: Message, user: UserServerLevelModel):
        """
        Event listener called when a user has levelled up at least once
        :param message: Revolt message
        :param user: User level model
        """
        with contextlib.suppress(defectio.HTTPException):
            await message.channel.send(f"{message.author} is now level **{user.level}**!")

    async def _give_random_exp(self, message: Message) -> int:
        """
        Add exp to a user profile for a given server
        :param message: Message which has been sent
        :return:
            The exp the user earned
        """
        exp = random.randint(self.config.min_exp, self.config.max_exp)
        await self.bot.mongo.levels.add_exp(message.author_id, core.utils.get_server_id(message.server), exp)
        return exp

    @classmethod
    async def _has_user_level_up(cls, user: UserServerLevelModel, exp_gained: int):
        """
        Check if the user has levelled up
        :param user: Mongo model
        :param exp_gained: Exp the user previously gained
        :return:
            Boolean whether the exp they gained 'exp_gained' gave them an additional level
        """
        return user.level > user.level_from_exp(user.exp - exp_gained)

    @md.dispatch(Message)
    async def _get_user_server_info(self, message: Message) -> UserServerLevelModel:
        """
        Fetch user data for a preovided server
        :param message: Revolt message
        :return:
            Mongo model for the user
        """
        return await self._get_user_server_info(message.author_id, core.utils.get_server_id(message.server))

    @md.dispatch(core.Context)
    async def _get_user_server_info(self, ctx: core.Context) -> UserServerLevelModel:
        """
        Fetch user data for a provided server
        :param ctx: Revolt command context
        :return:
            Mongo model for the user
        """
        return await self._get_user_server_info(ctx.author.id, core.utils.get_server_id(ctx.server))

    @md.dispatch(str, str)
    async def _get_user_server_info(self, user_id: str, server_id: str) -> UserServerLevelModel:
        """
        Fetch user data for a preovided server
        :param user_id: Revolt user id
        :param server_id: Revolt server id
        :return:
            Mongo model for the user
        """
        return await self.bot.mongo.levels.get_user(user_id, server_id)

    def _set_user_timer(self, message: Message):
        """
        Re-set the timer for the user so that they do not get exp for every message
        :param message: Message which has been sent
        """
        date = dt.datetime.utcnow() + self.config.interval

        self.timers[core.utils.get_server_id(message.server)][message.author_id] = date

    def _can_reward_exp(self, message: Message) -> bool:
        """
        Check whether the user can be rewarded server exp
        :param message: Message which has been sent
        :return:
            Boolean based on if exp can be rewarded
        """
        server_dict = self.timers[core.utils.get_server_id(message.server)]

        return message.author_id not in server_dict or (dt.datetime.utcnow() >= server_dict[message.author_id])


def setup(bot):
    bot.add_cog(Levels(bot))
