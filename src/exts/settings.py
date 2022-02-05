from defectio.ext import commands

from src import core
from src.common import emojis


class Settings(core.Cog):

    @commands.command("prefix")
    async def set_prefix(self, ctx: core.Context, prefix: str):
        """ Update the server command prefix """

        core.checks.server_owner_or_raise(ctx)

        await ctx.bot.mongo.servers.set_prefix(core.utils.get_server_id(ctx.server), prefix)

        await ctx.send(f"I have updated your server prefix to `{prefix}`")

        await ctx.send(f"{emojis.WARNING} My default prefix `s!` will still "
                       f"work until command checks are enabled for my library",
                       delete_after=30
                       )


def setup(bot):
    bot.add_cog(Settings(bot))
