from __future__ import annotations

from defectio.ext.commands import Context as _Context

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.bots.botbase import BotBase


class Context(_Context):
    bot: BotBase

    def is_support_server(self) -> bool:
        from src import core  # Circular import
        return core.utils.get_server_id(self.server) == self.bot.config.support_server_id

