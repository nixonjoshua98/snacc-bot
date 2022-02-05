from __future__ import annotations

import datetime as dt
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import Context

from defectio.ext import commands
from defectio.ext.commands import (CheckAnyFailure, CheckFailure,
                                   CommandNotFound, CommandOnCooldown,
                                   MaxConcurrencyReached,
                                   MissingRequiredArgument,
                                   NotOwner)
from src.logger import logger


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        bot.on_command_error = self.on_command_error

    @staticmethod
    async def on_command_error(ctx: Context, esc):

        if isinstance(esc, (CommandNotFound,)):
            return None

        elif isinstance(esc, NotOwner):
            await ctx.send("You do not have access to this command")

        elif isinstance(esc, CommandOnCooldown):
            await ctx.send(f"You are on cooldown! Try again in `{dt.timedelta(seconds=math.ceil(esc.retry_after))}`")

        elif isinstance(esc, MissingRequiredArgument):
            await ctx.send(f"`{esc.param.name}` is a required argument that is missing")

        elif isinstance(esc, MaxConcurrencyReached):
            await ctx.send("I am busy! Please retry shortly")

        elif isinstance(esc, (CheckFailure, CheckAnyFailure)):
            await ctx.send("You do not have access to this command")

        else:
            if str(esc).casefold().startswith("command raised an exception".casefold()):
                logger.error(f"{ctx.message.content} | {esc}")

            await ctx.send(esc)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
