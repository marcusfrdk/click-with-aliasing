# Click With Aliasing

![top language](https://img.shields.io/github/languages/top/marcusfrdk/click-with-aliasing)
![code size](https://img.shields.io/github/languages/code-size/marcusfrdk/click-with-aliasing)
![last commit](https://img.shields.io/github/last-commit/marcusfrdk/click-with-aliasing)
![issues](https://img.shields.io/github/issues/marcusfrdk/click-with-aliasing)
![contributors](https://img.shields.io/github/contributors/marcusfrdk/click-with-aliasing)
![PyPI](https://img.shields.io/pypi/v/click-with-aliasing)
![License](https://img.shields.io/github/license/marcusfrdk/click-with-aliasing)
![Downloads](https://static.pepy.tech/badge/click-with-aliasing)
![Monthly Downloads](https://static.pepy.tech/badge/click-with-aliasing/month)

A powerful extension for [Click](https://click.palletsprojects.com/) that adds **command and group aliasing** support with **automatic async function handling**.

## Features

-   **Command Aliases**: Create multiple names for your commands
-   **Group Aliases**: Add aliases to command groups
-   **Automatic Async Support**: Seamlessly handle async functions without extra configuration
-   **Drop-in Replacement**: Works exactly like standard Click decorators
-   **Type Safe**: Full type hints support with proper IDE integration
-   **Help Integration**: Aliases automatically appear in help text

## Installation

```bash
pip install click-with-aliasing
```

**Requirements:** Python 3.10 or newer

## Quick Start

### Basic Command with Aliases

```python
from click_with_aliasing import command

@command(name="deploy", aliases=["d", "dep"])
def deploy():
    """Deploy the application"""
    print("Deploying application...")
```

Now you can run any of these:

```bash
my-cli deploy
my-cli d
my-cli dep
```

### Group with Aliases

```python
from click_with_aliasing import group, command

@group(name="database", aliases=["db"])
def database():
    """Database management commands"""
    pass

@command(name="migrate", aliases=["m"])
def migrate():
    """Run database migrations"""
    print("Running migrations...")

database.add_command(migrate)
```

Usage:

```bash
my-cli database migrate  # Full names
my-cli db m              # Using aliases
my-cli database m        # Mixed usage
```

## Async Support

The library automatically detects and handles async functions, meaning no extra configuration is needed.

### Async Commands

```python
import asyncio
from click_with_aliasing import command

@command(name="fetch", aliases=["f"])
async def fetch():
    """Fetch data asynchronously"""
    await asyncio.sleep(1)
    print("Data fetched!")
```

### Async Groups

```python
import asyncio
from click_with_aliasing import group, command

@group(name="api", aliases=["a"])
async def api_group():
    """API management commands"""
    await asyncio.sleep(0.1)  # Simulate async setup

@command(name="start", aliases=["s"])
async def start_server():
    """Start the API server"""
    print("Starting server...")

api_group.add_command(start_server)
```

## Complete Example

Here's a full CLI application demonstrating all features:

```python
import asyncio
import click
from click_with_aliasing import group, command

@group(name="myapp", aliases=["app"])
def cli():
    """My Application CLI"""
    pass

@group(name="database", aliases=["db"])
async def database():
    """Database management commands"""
    await asyncio.sleep(0.1)  # Simulate async setup

@command(name="migrate", aliases=["m", "mig"])
async def migrate():
    """Run database migrations"""
    print("Running migrations...")
    await asyncio.sleep(1)
    print("Migrations completed!")

@command(name="seed", aliases=["s"])
def seed():
    """Seed the database"""
    print("Seeding database...")

@command(name="start", aliases=["run", "serve"])
def start():
    """Start the application server"""
    print("Starting server on port 8000...")

@command(name="stop", aliases=["kill"])
def stop():
    """Stop the application server"""
    print("Stopping server...")

database.add_command(migrate)
database.add_command(seed)
cli.add_command(database)
cli.add_command(start)
cli.add_command(stop)

if __name__ == "__main__":
    cli()
```

Usage examples:

```bash
python myapp.py database migrate
python myapp.py db m
python myapp.py database mig

python myapp.py start
python myapp.py stop

python myapp.py --help
python myapp.py db --help
```

## API Reference

### `@command(name, *, aliases=None, **kwargs)`

Creates a command with optional aliases.

**Parameters:**

-   `name` (str): Primary command name
-   `aliases` (List[str], optional): List of alternative names
-   `**kwargs`: Additional arguments passed to `click.command()`

**Returns:** `AliasedCommand` instance

### `@group(name=None, *, aliases=None, **kwargs)`

Creates a command group with optional aliases.

**Parameters:**

-   `name` (str, optional): Group name (defaults to function name)
-   `aliases` (List[str], optional): List of alternative names
-   `**kwargs`: Additional arguments passed to `click.group()`

**Returns:** `AliasedGroup` instance

## Migration from Click

Migrating from standard Click is straightforward:

### Before (Standard Click)

```python
import click

@click.group()
def cli():
    pass

@click.command()
def deploy():
    pass
```

### After (Click with Aliasing)

```python
from click_with_aliasing import group, command

@group(aliases=["c"])
def cli():
    pass

@command(name="deploy", aliases=["d", "dep"])
def deploy():
    pass
```

## Help Text Integration

Aliases automatically appear in help text:

```txt
myapp database --help
Usage: myapp database [OPTIONS] COMMAND [ARGS]...

  Database management commands

Options:
  --help  Show this message and exit.

Commands:
  migrate (m, mig)  Run database migrations
  seed (s)          Seed the database
```

## Troubleshooting

### Common Issues

**Q: My async function isn't working**
A: The library automatically wraps async functions. Make sure you're using Python 3.10+ and have proper async/await syntax.

**Q: Aliases don't appear in help**
A: Ensure you're using the `AliasedGroup` class (automatic when using the `@group` decorator).

**Q: Type hints are not working**
A: Make sure you're importing from `click_with_aliasing` and have the latest version installed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built on top of the great [Click](https://click.palletsprojects.com/) library by the Pallets team.
