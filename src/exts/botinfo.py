import aioify
import cpuinfo
import psutil
import defectio
from defectio.ext import commands
from src import core, utils
from src.classes import RevoltTable


class BotInfo(core.Cog):

    @commands.command("info")
    async def info(self, ctx: core.Context):
        tbl = RevoltTable(("Key", "Value"))

        tbl.add_row("Invite Link", ctx.bot.config.invite_link)
        tbl.add_row("Server Link", ctx.bot.config.server_link)
        tbl.add_row("GitHub Link", ctx.bot.config.github_link)

        await ctx.send(tbl.string())

    @commands.command("env")
    async def env(self, ctx: core.Context):
        def bits_to_gb(b):
            return round(b / (1 << 30), 1)

        @aioify.aioify
        def pull_data():
            return cpuinfo.get_cpu_info(), psutil.virtual_memory(), psutil.disk_usage("/")

        cpu, mem, storage = await pull_data()

        tbl = RevoltTable(("Key", "Value"))

        tbl.add_row("Bot Uptime", utils.format_timedelta(ctx.bot.uptime, '{D} days, {H} hours, {M} minutes'))
        tbl.add_row("Python Version", cpu.get('python_version', 'N/A'))
        tbl.add_row("Defectio Version", defectio.__version__)
        tbl.add_row("Processor", cpu.get('brand_raw', 'N/A'))
        tbl.add_row("Memory", f"{bits_to_gb(mem.used)}GB / {bits_to_gb(mem.total)}GB")
        tbl.add_row("Storage", f"{bits_to_gb(storage.used)}GB / {bits_to_gb(storage.total)}GB")
        tbl.add_row("CPU Usage", f"{round(psutil.cpu_percent(), 2)}%")

        await ctx.send(tbl.string())


def setup(bot):
    bot.add_cog(BotInfo(bot))
