from __future__ import annotations

from defectio.ext import commands, tasks

import contextlib
from src.models.config import BotConfiguration
from src import utils, core
from typing import Union, TYPE_CHECKING
from src.logger import logger
from src.mongo import AsyncMongoClient
import datetime as dt

if TYPE_CHECKING:
    from defectio import Message


class BotBase(commands.Bot):

    def __init__(self):
        super(BotBase, self).__init__(
            command_prefix="!",
            help_command=core.Help(),
            case_insensitive=True,
            strip_after_prefix=True
        )

        self.config = self._load_config()
        self.mongo = AsyncMongoClient(self.config)

        self._started_at = None
        self._on_ready_called = False

        self._load_launch_extensions()

    @property
    def uptime(self) -> dt.timedelta: return dt.datetime.utcnow() - self._started_at

    async def on_ready(self):
        if not self._on_ready_called:
            self._on_ready_called = True

            self.dispatch("startup")

        logger.info(f"Bot '{self.user}' is ready")

    async def on_startup(self):
        self._started_at = dt.datetime.utcnow()

        self._profile_update_loop.start()

        logger.info("Startup callback called")

    async def get_user_username(self, user_id: str) -> str:
        if (user := self.get_user(user_id)) and hasattr(user, "name"):
            return user.name

        elif (user := await self.fetch_user(user_id)) and hasattr(user, "name"):
            return user.name

        return user_id

    @tasks.loop(seconds=30)
    async def _profile_update_loop(self):
        await self.user.edit(status=f"s!help • Serving {len(self.servers):,} servers")

    async def get_prefix(self, message: Message) -> Union[list[str], str]:
        with contextlib.suppress(Exception):
            profile = await self.mongo.servers.get_server(core.utils.get_server_id(message.server))
            return ["s!", profile.prefix]
        return "s!"

    async def get_context(self, message, *, cls=None) -> core.Context:
        return await super(BotBase, self).get_context(message, cls=core.Context)

    async def on_message(self, message):
        if message.author.id != self.user.id:
            await super(BotBase, self).on_message(message)

    def run_with_token(self):
        self.run(token=self.config.bot_token)

    def _load_launch_extensions(self):
        for ext in self.config.launch_extensions:
            self.load_extension(ext)
            logger.info(f"Loaded extension '{ext}'")

    @staticmethod
    def _load_config() -> BotConfiguration:
        return BotConfiguration.parse_obj(utils.load_yaml("botconfig.yml"))
