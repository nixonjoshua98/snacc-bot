from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core import Context

from defectio.ext.commands import CommandError


def server_owner_or_raise(ctx: Context):
    if ctx.author.id == ctx.server.owner:
        return True

    raise CommandError("This command is temporarily locked to the server owner")
