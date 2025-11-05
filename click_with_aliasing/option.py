"""Option that extends the Click Option."""

# pylint: disable=redefined-builtin

from typing import Any, Callable, TypeVar

import click

F = TypeVar("F", bound=Callable[..., Any])


class Option(click.Option):
    """Option that extends the Click Option."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a new `Option` instance."""
        super().__init__(*args, **kwargs)


def option(
    *param_decls: str,
    default: Any | None = None,
    required: bool = False,
    type: Any | None = None,
    help: str | None = None,
    hidden: bool = False,
    show_default: bool = False,
    prompt: bool = False,
    confirmation_prompt: bool = False,
    hide_input: bool = False,
    is_flag: bool | None = None,
    flag_value: Any | None = None,
    multiple: bool = False,
    count: bool = False,
    allow_from_autoenv: bool = True,
    show_choices: bool = True,
    show_envvar: bool = False,
    callback: Callable[..., Any] | None = None,
    metavar: str | None = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: str | None = None,
    shell_complete: Callable[..., Any] | None = None,
    autocompletion: Callable[..., Any] | None = None,
    **kwargs: Any,
) -> Callable[[F], F]:
    """
    Create an option decorator.

    Args:
        *param_decls:
            Parameter declarations (e.g., "--name", "-n").
        default (optional):
            Default value for the option.
        required (bool):
            Whether the option is required.
        type (optional):
            The type to convert the value to (e.g., click.INT, click.Path()).
        help (str, optional):
            Help text for the option.
        hidden (bool):
            Hide this option from help output.
        show_default (bool):
            Show the default value in help text.
        prompt (bool):
            Prompt the user for input if not provided.
        confirmation_prompt (bool):
            Prompt twice for confirmation (for passwords).
        hide_input (bool):
            Hide user input (for passwords).
        is_flag (bool, optional):
            Whether this is a boolean flag.
        flag_value (optional):
            Value to use when flag is set.
        multiple (bool):
            Allow the option to be specified multiple times.
        count (bool):
            Count the number of times the option is specified.
        allow_from_autoenv (bool):
            Allow value from environment variable.
        show_choices (bool):
            Show valid choices in help text.
        show_envvar (bool):
            Show environment variable name in help text.
        callback (Callable, optional):
            Callback function to transform the value.
        metavar (str, optional):
            How the value is shown in help text.
        expose_value (bool):
            Whether to pass value to the command function.
        is_eager (bool):
            Process this option before others.
        envvar (str, optional):
            Environment variable name to read from.
        shell_complete (Callable, optional):
            Shell completion function.
        autocompletion (Callable, optional):
            Deprecated. Use shell_complete instead.
        **kwargs:
            Additional Click option parameters.

    Returns:
        Callable[[F], F]:
            A decorator function that takes a command function and returns it
            with the option attached.

    Examples:
        @command()
        @option("--name", "-n", help="Your name")
        def cmd(name: str):
            click.echo(f"Hello {name}")
    """
    kwargs["cls"] = Option

    if default is not None:
        kwargs["default"] = default
    if required:
        kwargs["required"] = required
    if type is not None:
        kwargs["type"] = type
    if help is not None:
        kwargs["help"] = help
    if hidden:
        kwargs["hidden"] = hidden
    if show_default:
        kwargs["show_default"] = show_default
    if prompt:
        kwargs["prompt"] = prompt
    if confirmation_prompt:
        kwargs["confirmation_prompt"] = confirmation_prompt
    if hide_input:
        kwargs["hide_input"] = hide_input
    if is_flag is not None:
        kwargs["is_flag"] = is_flag
    if flag_value is not None:
        kwargs["flag_value"] = flag_value
    if multiple:
        kwargs["multiple"] = multiple
    if count:
        kwargs["count"] = count
    if not allow_from_autoenv:
        kwargs["allow_from_autoenv"] = allow_from_autoenv
    if not show_choices:
        kwargs["show_choices"] = show_choices
    if show_envvar:
        kwargs["show_envvar"] = show_envvar
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

    return click.option(*param_decls, **kwargs)
