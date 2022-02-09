
import random
import asyncio
from src import core
from defectio.ext import commands


class EightBall(core.Cog):

    @commands.command("8b")
    async def eight_ball(self, ctx, *, question: str):

        await asyncio.sleep(random.uniform(1, 3))

        answers = ["It is certain",
                   "It is decidedly so",
                   "Without a doubt",
                   "Yes, definitely",
                   "You may rely on it",
                   "As I see it, yes",
                   "Most likely",
                   "Outlook good",
                   "Yes",
                   "Signs point to yes",
                   "Reply hazy try again",
                   "Ask again later",
                   "Better not tell you now",
                   "Cannot predict now",
                   "Concentrate and ask again",
                   "Don't count on it",
                   "My reply is no",
                   "My sources say no",
                   "Outlook not so good",
                   "Very doubtful"]

        await ctx.channel.send(f"{random.choice(answers)}")


def setup(bot):
    bot.add_cog(EightBall(bot))
