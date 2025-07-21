"""The command decorator with alias support."""

import asyncio
import functools
from typing import Callable, List, Optional

import click

from ._aliased_command import AliasedCommand


def command(
    name: str,
    *args,
    aliases: Optional[List[str]] = None,
    **kwargs,
) -> Callable[[Callable], AliasedCommand]:
    """
    The command decorator with aliasing support which
    replaces the default Click command decorator.

    Usage:
        @command(name="my_command")
        @command(name="my_command", aliases=["mc"])
    Args:
        name (str): The name of the command.
        aliases (Optional[List[str]]): The list of aliases for the command.
        *args (Any): Additional arguments.
        **kwargs (Any): Additional keyword arguments.
    Returns:
        Callable[[Callable], AliasedCommand]: The Click command decorator.
    Raises:
        None
    """

    def decorator(fn: Callable) -> AliasedCommand:
        """
        Decorator for creating a command.

        Args:
            fn: Callable - The function to decorate.
        Returns:
            click.Command - The Click command.
        Raises:
            None
        """
        original_fn = fn

        if asyncio.iscoroutinefunction(fn):

            @functools.wraps(fn)
            def sync_wrapper(*wrapper_args, **wrapper_kwargs):
                return asyncio.run(original_fn(*wrapper_args, **wrapper_kwargs))

            fn = sync_wrapper

        command_decorator = click.command(
            name=name, cls=AliasedCommand, *args, **kwargs
        )
        cmd = command_decorator(fn)
        cmd.aliases = aliases or []
        return cmd

    return decorator
