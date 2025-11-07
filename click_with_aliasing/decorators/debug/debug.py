"""Debug decorator that allows for easy debugging of decorators."""

from typing import Any, Callable, TypeVar, overload

F = TypeVar("F", bound=Callable[..., Any])


class DebugDecorator:
    """Decorator for debugging functions and decorators."""

    def __call__(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = fn(*args, **kwargs)
            print("Function:", fn.__name__)
            print("Args:", args)
            print("Kwargs:", kwargs)
            return result

        return wrapper


@overload
def debug(fn: F) -> F: ...


@overload
def debug() -> Callable[[F], F]: ...


def debug(fn: Callable[..., Any] | None = None) -> Any:
    """
    Decorator for debugging functions and decorators.

    Can be used with or without parentheses:
        @debug
        def my_func():
            pass

        @debug()
        def my_func():
            pass

    Args:
        fn (Callable[..., Any], optional):
            The function to decorate.

    Returns:
        Callable[..., Any]:
            The decorated function or a decorator function.
    """
    decorator = DebugDecorator()

    if fn is None:
        return decorator
    else:
        return decorator(fn)
