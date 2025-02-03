""" The group decorator with alias support. """

import click

from ._aliased_group import AliasedGroup


def group(
    *args, name: str = None, aliases: list[str] = None, **kwargs
) -> click.Group:
    """
    The group decorator with aliasing support
    which replaces the default Click group decorator.

    Usage:
        @group(name="my_group)

        @group(name="my_group", aliases=["mg"])
    Args:
        name: str - The name of the group.
        aliases: list[str] - The list of aliases for the group.
        *args: Any - Additional arguments.
        **kwargs: Any - Additional keyword arguments.
    Returns:
        click.Group - The Click group decorator.
    Raises:
        None
    """

    def decorator(func) -> click.Group:
        """Decorator for creating a group."""
        inferred_name = name or func.__name__
        group_decorator = click.group(
            name=inferred_name, cls=AliasedGroup, *args, **kwargs
        )
        cmd = group_decorator(func)
        cmd.aliases = aliases or []
        return cmd

    return decorator
