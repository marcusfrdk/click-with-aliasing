"""The group decorator with alias support."""

from typing import Callable, List, Optional

import click

from ._aliased_group import AliasedGroup


def group(
    name: Optional[str] = None,
    *,
    aliases: Optional[List[str]] = None,
    **kwargs,
) -> Callable[[Callable], click.Group]:
    """
    The group decorator with aliasing support
    which replaces the default Click group decorator.

    Usage:
        @group(name="my_group")

        @group(name="my_group", aliases=["mg"])
    Args:
        name (Optional[str]): The name of the group.
        aliases (Optional[List[str]]): The list of aliases for the group.
        **kwargs (Any): Additional keyword arguments.
    Returns:
        Callable[[Callable], click.Group]: The Click group decorator.
    Raises:
        None
    """

    def decorator(func) -> click.Group:
        """Decorator for creating a group."""
        inferred_name = name or func.__name__
        group_decorator = click.group(
            name=inferred_name,
            cls=AliasedGroup,
            aliases=aliases,
            **kwargs,
        )
        cmd = group_decorator(func)
        return cmd

    return decorator
