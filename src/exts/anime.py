
from typing import Optional
from src.models import BaseModel
from defectio.ext import commands

from src.core import Cog


class Waifu(BaseModel):
    url: str


class Quote(BaseModel):
    anime: str
    character: str
    quote: str


class Anime(Cog):

    @commands.command("waifu")
    async def waifu(self, ctx):

        if waifu := await self._fetch_waifu("sfw"):
            return await ctx.send(f"[]({waifu.url})")

        await ctx.send("An unexpected error occurred")

    @commands.command("quote")
    async def anime_quote(self, ctx):

        if quote := await self._fetch_quote():
            return await ctx.send(f"**{quote.character} ({quote.anime})**\n{quote.quote}")

        await ctx.send("An unexpected error occurred")

    async def _fetch_quote(self) -> Optional[Quote]:
        resp = await self.bot.aiohttp.get("https://animechan.vercel.app/api/random")

        if resp.status == 200:
            data = await resp.json()

            return Quote.parse_obj(data)

    async def _fetch_waifu(self, type_) -> Optional[Waifu]:
        resp = await self.bot.aiohttp.get(f"https://api.waifu.pics/{type_}/waifu")

        if resp.status == 200:
            data = await resp.json()

            return Waifu.parse_obj(data)


def setup(bot):
    bot.add_cog(Anime(bot))