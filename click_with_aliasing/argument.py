"""Argument that extends the Click Argument."""

# pylint: disable=redefined-builtin

from typing import Any, Callable, TypeVar

import click

F = TypeVar("F", bound=Callable[..., Any])


class Argument(click.Argument):
    """Argument that extends the Click Argument."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize a new `Argument` instance.

        Args:
            *args:
                Positional arguments for the base `click.Argument` class.
            **kwargs:
                Keyword arguments for the base `click.Argument` class.
        """
        super().__init__(*args, **kwargs)


def argument(
    *param_decls: str,
    required: bool = True,
    type: Any | None = None,
    default: Any | None = None,
    callback: Callable[..., Any] | None = None,
    metavar: str | None = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: str | None = None,
    shell_complete: Callable[..., Any] | None = None,
    autocompletion: Callable[..., Any] | None = None,
    nargs: int = 1,
    **kwargs: Any,
) -> Callable[[F], F]:
    """
    Create an argument decorator.

    Args:
        *param_decls:
            Parameter declarations (e.g., 'name').
        required (bool):
            Whether the argument is required (default: True).
        type (optional):
            The type to convert the value to (e.g., click.INT, click.Path()).
        default (optional):
            Default value for the argument.
        callback (Callable, optional):
            Callback function to transform the value.
        metavar (str, optional):
            How the value is shown in help text.
        expose_value (bool):
            Whether to pass value to the command function.
        is_eager (bool):
            Process this argument before others.
        envvar (str, optional):
            Environment variable name to read from.
        shell_complete (Callable, optional):
            Shell completion function.
        autocompletion (Callable, optional):
            Deprecated. Use shell_complete instead.
        nargs (int):
            Number of arguments to consume (default: 1, use -1 for
            unlimited).
        **kwargs:
            Additional Click argument parameters.

    Returns:
        Callable[[F], F]:
            A decorator function that takes a command function and returns it
            with the argument attached.

    Examples:
        @command()
        @argument("name")
        def cmd(name: str):
            click.echo(f"Hello {name}")
    """
    kwargs["cls"] = Argument

    # Add standard Click parameters (only if not None/default)
    if not required:
        kwargs["required"] = required
    if type is not None:
        kwargs["type"] = type
    if default is not None:
        kwargs["default"] = default
    if callback is not None:
        kwargs["callback"] = callback
    if metavar is not None:
        kwargs["metavar"] = metavar
    if not expose_value:
        kwargs["expose_value"] = expose_value
    if is_eager:
        kwargs["is_eager"] = is_eager
    if envvar is not None:
        kwargs["envvar"] = envvar
    if shell_complete is not None:
        kwargs["shell_complete"] = shell_complete
    if autocompletion is not None:
        kwargs["autocompletion"] = autocompletion
    if nargs != 1:
        kwargs["nargs"] = nargs

    return click.argument(*param_decls, **kwargs)
