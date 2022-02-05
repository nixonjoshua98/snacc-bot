from __future__ import annotations

from typing import TYPE_CHECKING
from src.core import Cog

if TYPE_CHECKING:
    from defectio import Message


class Listeners(Cog):

    @Cog.listener()
    async def on_message(self, message: Message):
        # on_message -> on_server_message

        if message.server and message.author_id != self.bot.user.id:
            self.bot.dispatch("server_message", message)


def setup(bot):
    bot.add_cog(Listeners(bot))
