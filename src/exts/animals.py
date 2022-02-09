import dataclasses

from typing import Optional

from defectio.ext import commands

from src.core import Cog


@dataclasses.dataclass(frozen=True)
class Animal:
    url: str


class Animals(Cog):
    @commands.command("axolotl")
    async def axolotl(self, ctx):
        if animal := await self._fetch_animal("https://axoltlapi.herokuapp.com/"):
            return await ctx.send(f"[]({animal.url})")

        await ctx.send(":x: I failed to find an axolotl!")

    @commands.command("dog")
    async def dog(self, ctx):
        if animal := await self._fetch_animal("https://random.dog/woof.json"):
            return await ctx.send(f"[]({animal.url})")

        await ctx.send(":x: I failed to find a dog!")

    @commands.command("fox")
    async def fox(self, ctx):
        if animal := await self._fetch_animal("https://randomfox.ca/floof/", key="image"):
            return await ctx.send(f"[]({animal.url})")

        await ctx.send(":x: I failed to find a fox!")

    @commands.command("cat")
    async def cat(self, ctx):
        if animal := await self._fetch_animal("https://thatcopy.pw/catapi/rest/"):
            return await ctx.send(f"[]({animal.url})")

        await ctx.send(":x: I failed to find a cat!")

    @commands.command("duck")
    async def duck(self, ctx):
        if animal := await self._fetch_animal("https://random-d.uk/api/v2/random"):
            return await ctx.send(f"[]({animal.url})")

        await ctx.send(":x: I failed to find a duck!")

    async def _fetch_animal(self, url, *, key: str = "url") -> Optional[Animal]:
        resp = await self.bot.aiohttp.get(url)

        if resp.status == 200:
            data = await resp.json()

            return Animal(url=data[key])


def setup(bot):
    bot.add_cog(Animals(bot))
