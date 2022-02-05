from __future__ import annotations
from typing import TYPE_CHECKING
from defectio.ext.commands import Cog as _Cog

if TYPE_CHECKING:
    from src.bots import SnaccBot


class Cog(_Cog):
    def __init__(self, bot):
        super(Cog, self).__init__()

        self.bot: SnaccBot = bot
