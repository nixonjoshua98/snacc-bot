from __future__ import annotations

from typing import Optional, TYPE_CHECKING, TypedDict
from defectio.ext import commands
from src import core
import urllib.parse

if TYPE_CHECKING:
    class _DefintionPayload(TypedDict):
        definition: str
        word: str
        permalink: str


class UrbanDictionary(core.Cog):

    @commands.command("ud")
    async def urban_dictionary(self, ctx: core.Context, *, word: str = ""):
        """
        Lookup a word or find a random definition
        """
        define: _DefintionPayload= await self._get_definition(word)

        if define is not None:
            return await ctx.send(f"**[{define['word']}]**\n{define['definition']}")

        await ctx.send(":x: I failed when attempting to look at Urban Dictionary")

    async def _get_definition(self, word: str) -> Optional[dict]:
        """
        Send the API request for the word, or random definition
        :param word: Search term
        :return:
            Dict payload
        """
        if word in ("", None):
            r = await self.bot.aiohttp.get("http://api.urbandictionary.com/v0/random")

        else:
            r = await self.bot.aiohttp.get(f"http://api.urbandictionary.com/v0/define?term={urllib.parse.quote(word)}")

        if r.status == 200 and (data := (await r.json()).get("list", [])):
            return data[0]


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))
