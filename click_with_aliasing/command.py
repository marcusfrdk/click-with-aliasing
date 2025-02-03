""" The command decorator with alias support. """

from typing import Callable

import click

from ._aliased_command import AliasedCommand


def command(
    name: str, *args, aliases: list[str] = None, **kwargs
) -> click.Command:
    """
    The command decorator with aliasing support which
    replaces the default Click command decorator.

    Usage:
        @command(name="my_command)

        @command(name="my_command), aliases=["mc])
    Args:
        name: str - The name of the command.
        aliases: list[str] - The list of aliases for the command.
        *args: Any - Additional arguments.
        **kwargs: Any - Additional keyword arguments.
    Returns:
        click.Command - The Click command decorator.
    Raises:
        None
    """

    command_decorator = click.command(
        name=name, cls=AliasedCommand, *args, **kwargs
    )

    def decorator(fn: Callable) -> click.Command:
        """
        Decorator for creating a command.

        Args:
            fn: Callable - The function to decorate.
        Returns:
            click.Command - The Click command.
        Raises:
            None
        """
        cmd = command_decorator(fn)
        cmd.aliases = aliases or []
        return cmd

    return decorator
