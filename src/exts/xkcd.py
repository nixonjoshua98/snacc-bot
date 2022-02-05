from typing import Union, Optional
from cachetools import LRUCache
from src.models import BaseModel
from defectio.ext import commands
from pydantic import Field
from src.core import Cog


class ComicPage(BaseModel):
    title: str = Field(..., alias="safe_title")
    url: str = Field(..., alias="img")
    number: int = Field(..., alias="num")


class XKCD(Cog):
    def __init__(self, bot):
        super(XKCD, self).__init__(bot)

        # Cache some pages
        self._page_cache: LRUCache[int, ComicPage] = LRUCache(maxsize=32)

    @commands.command("xkcd")
    async def xkcd(self, ctx, number: Optional[int] = None):

        data = await self._get_page(number)

        if data is None:
            return await ctx.send(f":x: I failed to find this comic")

        await ctx.send(f"Comic #{data.number} | {data.title}\n{data.url}")

    async def _get_page(self, num: Union[int, None]) -> Union[ComicPage, None]:

        if num is None:  # Fetch the current page
            return await self._fetch_page("https://xkcd.com/info.0.json")

        # We have the page cached and ready to send
        if comic_page := self._page_cache.get(num):
            return comic_page

        # Fetch the page from the site and download the image
        elif new_page := await self._fetch_page(f"https://xkcd.com/{num}/info.0.json"):
            self._page_cache[num] = new_page
            return new_page

    async def _fetch_page(self, url) -> Union[ComicPage, None]:
        resp = await self.http_session.get(url)  # Fetch the xkcd url

        if resp.status == 200:
            data = await resp.json()

            return ComicPage.parse_obj(data)


def setup(bot):
    bot.add_cog(XKCD(bot))