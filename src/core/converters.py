from defectio.ext import commands

from defectio.ext.commands import UserInputError


class Range(commands.Converter):
    def __init__(self, min_: int, max_: int = None):
        self.min_ = min_
        self.max_ = max_

    async def convert(self, ctx: commands.Context, argument: str) -> int:
        try:
            val = int(argument)

            if (self.max_ is not None and val > self.max_) or val < self.min_:
                raise UserInputError(f":x: Argument should be within **{self.min_:,} - {self.max_:,}**")

        except ValueError:
            raise UserInputError(":x: Invalid number entered!")

        return val


# Temp
class TextChannelConverter(commands.Converter):
    async def convert(self, ctx, argument: str):
        text_channels = [
            state
            for channel_id in ctx.server.channel_ids
            if (state := ctx._state.get_channel(channel_id)) and state.type == "TextChannel"
        ]

        if argument.startswith("<#") and argument.endswith(">"):
            for channel in text_channels:
                if channel.id in argument:
                    return channel

        raise UserInputError(f"Channel {argument} was not found. Channels must be a mention")


class CoinSide(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.lower()

        # Convert short names in long names
        if long_name := {"h": "heads", "t": "tails"}.get(argument):
            argument = long_name

        if argument not in ["tails", "heads"]:
            raise UserInputError(f"Coin side should be **heads** or **tails** - not **{argument}**")

        return argument
