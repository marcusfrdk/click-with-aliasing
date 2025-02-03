# Click With Aliasing

![top language](https://img.shields.io/github/languages/top/marcusfrdk/click-with-aliasing)
![code size](https://img.shields.io/github/languages/code-size/marcusfrdk/click-with-aliasing)
![last commit](https://img.shields.io/github/last-commit/marcusfrdk/click-with-aliasing)
![issues](https://img.shields.io/github/issues/marcusfrdk/click-with-aliasing)
![contributors](https://img.shields.io/github/contributors/marcusfrdk/click-with-aliasing)
![PyPI](https://img.shields.io/pypi/v/click-with-aliasing)
![License](https://img.shields.io/github/license/marcusfrdk/click-with-aliasing)

This is a project that adds decorators that replaces the default `click.group` and `click.command` decorators with custom ones that support aliasing.

## Installation

You can install the package from [PyPI](https://pypi.org/project/click-with-aliasing/):

```bash
pip install click-with-aliasing
```

The package is available for Python 3.11 and newer.

## Usage

The package provides two decorators: `group` and `command`. They work exactly like the original `click.group` and `click.command` decorators, but they also support aliasing using the `aliases` argument.

Here is an example of how to use the `group` decorator:

```python
from click_with_aliasing import group
from .my_command import my_command

@group(name="my_group", aliases=['mg'])
def cli():
    """ My Click group """

cli.add_command(my_command)
```

This group works exactly like a normal `click.group`, but while using the CLI, you can use either `my_group` or `mg` to call the group.

The same works for the `command` decorator:

```python
from click_with_aliasing import command

@command(name="my_command", aliases=['mc'])
def my_command():
    """ My Click command """
    ...
```

Like the group, you can call the command using either `my_command` or `mc`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
