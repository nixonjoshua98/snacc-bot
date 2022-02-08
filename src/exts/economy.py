from __future__ import annotations

import random

import datetime as dt

from defectio.ext import commands
from defectio.ext.commands import BucketType
from typing import TYPE_CHECKING
from src import utils
from src.classes import RevoltTable
from src.common import emojis
from src.core import Cog, Context
from src.core.converters import CoinSide, Range
from src.mongo.models.economy import UserEconomyProfile

if TYPE_CHECKING:
    from defectio.models.user import PartialUser
    from src.models.config import EconomyConfiguration


class Economy(Cog):

    def __init__(self, bot):
        super(Economy, self).__init__(bot)

        self.config: EconomyConfiguration = self.bot.config.cogs.economy

    @commands.command("bal")
    async def bal(self, ctx: Context):
        profile: UserEconomyProfile = await self._get_user_profile(ctx.author)

        await ctx.send(f"You have **{profile.currency:,}** :cookie:")

    @commands.command("richest")
    async def richest(self, ctx: Context):
        users: list[UserEconomyProfile] = await ctx.bot.mongo.economy.get_top_richest(15)

        tbl = RevoltTable(("Rank", "Username", "Total"))

        for rank, profile in enumerate(users, start=1):
            user = await ctx.bot.fetch_user(profile.user_id)

            tbl.add_row(rank, getattr(user, "display_name", "N/A"), f"{profile.currency} {emojis.COOKIE}")

        await ctx.send(tbl.string())

    @commands.command("daily")
    async def daily(self, ctx: Context):
        now = dt.datetime.utcnow()  # Timezone unaware

        profile: UserEconomyProfile = await self._get_user_profile(ctx.author)

        streak = 1

        if profile.last_daily_claim is not None:  # Previous daily login found
            days_since = (time_since := now - profile.last_daily_claim).days

            if days_since < 1:  # Checked without 24 hours already
                delta_str = utils.format_timedelta(dt.timedelta(days=1) - time_since, "{H:02}:{M:02}:{S:02}")

                return await ctx.send(f"You have already claimed your daily reward! Try again in `{delta_str}`")

            # New day, so we can advance the streak (over 1 day and the streak is destroyed)
            if days_since == 1:
                streak = profile.daily_streak + 1

        # Calculate login reward
        reward = self.config.base_daily_reward  # Base reward
        reward += (min(self.config.max_daily_streak_reward, streak) * self.config.reward_per_daily_sreak)  # Streak

        # Create the default claim text
        txt = (f"You have received {reward} {emojis.COOKIE}\n"
               f"{self.config.base_daily_reward} {emojis.COOKIE}\n"
               f"{self.config.reward_per_daily_sreak} {emojis.COOKIE} * "
               f"{streak}d (max {self.config.max_daily_streak_reward} days)")

        # Claiming in the support server offers a bonus multiplier
        if ctx.is_support_server():
            reward *= self.config.support_server_multiplier

            txt += f"\n**x{self.config.support_server_multiplier} support server bonus**"

        # User is not in the support server, so cross out the bonus and do not apply it
        else:
            txt += f"\n~~x{self.config.support_server_multiplier} support server bonus~~"

        # Perform the daily login
        await ctx.bot.mongo.economy.daily_login(ctx.author.id, now, streak, reward)

        await ctx.send(txt)

    @commands.command("flip")
    @commands.max_concurrency(1, BucketType.user)
    async def flip(self, ctx: Context, side: CoinSide, bet: Range(0, 50_000)):  # type: ignore
        profile: UserEconomyProfile = await self._get_user_profile(ctx.author)

        if profile.currency < bet:
            return await ctx.send("You cannot afford to cover that bet!")

        side_landed = random.choice(["heads", "tails"])

        correct_side = side_landed == side

        winnings = bet if correct_side else -bet

        await ctx.bot.mongo.economy.inc_currency(ctx.author.id, winnings)

        await ctx.send(f"It's **{side_landed}**! You {'won' if correct_side else 'lost'} **{bet:,}** {emojis.COOKIE}!")

    @commands.command(name="bet")
    @commands.max_concurrency(1, BucketType.user)
    async def bet(
            self,
            ctx: Context,
            bet: Range(0, 50_000) = 0,  # type: ignore
            side: Range(1, 6) = 6  # type: ignore
    ):
        """ Roll a die and bet on which side the die lands on """

        sides = 6

        profile: UserEconomyProfile = await self._get_user_profile(ctx.author)

        if profile.currency < bet:
            return await ctx.send("You cannot afford to cover that bet!")

        side_landed = random.randint(1, sides)

        bet_won = side_landed == side

        winnings = bet * (sides - 1) if bet_won else -bet

        await ctx.bot.mongo.economy.inc_currency(ctx.author.id, winnings)

        await ctx.send(f"{emojis.N1234} You {f'won {winnings}' if bet_won else f'lost {bet}'} {bet}{emojis.COOKIE} "
                       f"The dice landed on `{side_landed}`")

    async def _get_user_profile(self, user: PartialUser) -> UserEconomyProfile:
        """
        Fetch a user profile from the database
        :param user:
        :return:
        """
        return await self.bot.mongo.economy.get_user(user.id)


def setup(bot):
    bot.add_cog(Economy(bot))
