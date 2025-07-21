"""AliasedGroup class for click_with_alias."""

from typing import Optional

import click


class AliasedGroup(click.Group):
    """A Click group that supports aliasing."""

    def __init__(self, *args, **kwargs):
        self.aliases = kwargs.pop("aliases", [])
        super().__init__(*args, **kwargs)

    def add_command(
        self, cmd: click.Command, name: Optional[str] = None
    ) -> None:
        """
        Add a command to the group.

        Args:
            cmd (click.Command): The command to add.
            name (Optional[str]): The name of the command.
        Returns:
            None
        Raises:
            ValueError: If the command name is already taken.
        """
        aliases = getattr(cmd, "aliases", None)
        if aliases is None:
            aliases = []
        elif not isinstance(aliases, (list, tuple)):
            aliases = [aliases] if isinstance(aliases, str) else []

        super().add_command(cmd, name)
        for alias in aliases:
            if isinstance(alias, str) and alias.strip():
                super().add_command(cmd, alias)

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """
        Format the commands for the group.

        Args:
            ctx (click.Context): The click context.
            formatter (click.HelpFormatter): The help formatter.
        Returns:
            None
        Raises:
            None
        """
        commands = {}
        for name, cmd in self.commands.items():
            if name == cmd.name:
                aliases = getattr(cmd, "aliases", None)
                if aliases is None:
                    aliases = []
                elif not isinstance(aliases, (list, tuple)):
                    aliases = [aliases] if isinstance(aliases, str) else []

                valid_aliases = [
                    a for a in aliases if isinstance(a, str) and a.strip()
                ]

                if valid_aliases:
                    name = f"{name} ({', '.join(valid_aliases)})"
                commands[name] = cmd

        rows = [
            (name, cmd.get_short_help_str()) for name, cmd in commands.items()
        ]

        if rows:
            with formatter.section("Commands"):
                formatter.write_dl(rows)
