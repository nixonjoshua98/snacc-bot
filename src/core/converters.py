from defectio.ext import commands
from defectio.ext.commands import UserInputError


class Range(commands.Converter):
    def __init__(self, min_: int, max_: int = None):
        self.min_ = min_
        self.max_ = max_

    async def convert(self, ctx: commands.Context, argument: str) -> int:

        try:
            val = int(argument)

            if self.max_ is None:
                if val < self.min_:
                    raise UserInputError(f"Argument should be greater or equal to **{self.min_}**")

            elif val > self.max_ or val < self.min_:
                raise UserInputError(f"Argument should be within **{self.min_:,} - {self.max_}**")

        except ValueError:
            raise UserInputError("Argument should be an integer")

        return val


class CoinSide(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.lower()

        # Convert short names in long names
        if long_name := {"h": "heads", "t": "tails"}.get(argument):
            argument = long_name

        if argument not in ["tails", "heads"]:
            raise UserInputError(f"Coin side should be **heads** or **tails** not **{argument}**")

        return argument
