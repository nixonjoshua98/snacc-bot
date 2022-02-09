from defectio.ext import tasks

from src.bots.botbase import BotBase


class SnaccBot(BotBase):
    async def on_startup(self):
        await super(SnaccBot, self).on_startup()

        self._profile_update_loop.start()

    @tasks.loop(seconds=15)
    async def _profile_update_loop(self):
        ls = [
            f"s!help • Serving {len(self.servers):,} servers",
            f"s!info • Join our server!",
            f"s!help • What feature next?"
        ]

        await self.user.edit(status=ls[self._profile_update_loop._current_loop % len(ls)])

