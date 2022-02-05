from defectio.ext import commands

from src.classes import RevoltTable


class Help(commands.HelpCommand):
    def __init__(self, **options):
        super(Help, self).__init__(verify_checks=True, show_hidden=False, **options)

    def get_command_signature(self, command):

        parent = command.parent
        entries = []
        while parent is not None:
            entries.append(parent.name)  # type: ignore
            parent = parent.parent  # type: ignore

        parent_sig = ' '.join(reversed(entries))

        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent_sig:
                fmt = parent_sig + ' ' + fmt
            alias = fmt
        else:
            alias = command.name if not parent_sig else parent_sig + ' ' + command.name

        return alias

    def _format_commands(self, outer_cmds):
        def _format(cmds_):
            txt = []

            for c in cmds_:
                if isinstance(c, commands.Group):
                    txt.append(f"`{self.get_command_signature(c)}`")
                    txt.extend(_format(c.commands))

                else:
                    txt.append(f"`{self.get_command_signature(c)}`")

            return txt

        return _format(outer_cmds)

    async def create_help(self, mapping):
        tbl = RevoltTable(("Module", "Commands"))

        for cog, cmds in mapping.items():
            cmds = await self.filter_commands(cmds, sort=False)

            if cog is None or not cmds:
                continue

            tbl.add_row(cog.qualified_name, ', '.join(self._format_commands(cmds)))

        return tbl.string()

    async def send_bot_help(self, mapping):
        txt = await self.create_help(mapping)

        await self.context.send(txt)

    async def send_command_help(self, command: commands.Command):
        await self.send_bot_help({command.cog: [command]})

    async def send_cog_help(self, cog):
        await self.send_bot_help({cog: cog.get_commands()})

    async def send_group_help(self, group: commands.Group):
        await self.send_bot_help({group.cog: group})

    async def send_error_message(self, error):
        ...