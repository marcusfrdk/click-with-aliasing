"""The group decorator with alias support."""

import asyncio
import functools
from typing import Callable, List, Optional

import click

from ._aliased_group import AliasedGroup


def group(
    name: Optional[str] = None,
    *,
    aliases: Optional[List[str]] = None,
    **kwargs,
) -> Callable[[Callable], AliasedGroup]:
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
        Callable[[Callable], AliasedGroup]: The Click group decorator.
    Raises:
        None
    """

    def decorator(func) -> AliasedGroup:
        """Decorator for creating a group."""
        inferred_name = name or func.__name__

        original_func = func

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            def sync_wrapper(*wrapper_args, **wrapper_kwargs):
                return asyncio.run(
                    original_func(*wrapper_args, **wrapper_kwargs)
                )

            func = sync_wrapper

        group_decorator = click.group(
            name=inferred_name,
            cls=AliasedGroup,
            aliases=aliases,
            **kwargs,
        )
        cmd = group_decorator(func)
        return cmd

    return decorator
