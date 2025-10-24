# Command

The `command` decorator creates a CLI command with optional alias support. It's a drop-in replacement for Click's `@click.command()` decorator with added aliasing functionality.

## Basic Usage

### Simple Command

```python
from click_with_aliasing import command

@command(name="hello")
def hello():
    """Say hello"""
    print("Hello, World!")
```

```bash
$ python app.py hello
Hello, World!
```

### Command with Aliases

```python
from click_with_aliasing import command

@command(name="deploy", aliases=["d", "dep"])
def deploy():
    """Deploy the application"""
    print("Deploying...")
```

All of these work:

```bash
python app.py deploy
python app.py d
python app.py dep
```

## With Parameters

### Options

```python
from click_with_aliasing import command
import click

@command(name="greet", aliases=["g"])
@click.option("--name", default="World", help="Name to greet")
def greet(name):
    """Greet someone"""
    print(f"Hello, {name}!")
```

```bash
$ python app.py greet --name Alice
Hello, Alice!

$ python app.py g --name Bob
Hello, Bob!
```

### Arguments

```python
from click_with_aliasing import command
import click

@command(name="copy", aliases=["cp"])
@click.argument("source")
@click.argument("dest")
def copy(source, dest):
    """Copy files"""
    print(f"Copying {source} to {dest}")
```

```bash
$ python app.py copy file1.txt file2.txt
Copying file1.txt to file2.txt

$ python app.py cp file1.txt file2.txt
Copying file1.txt to file2.txt
```

## Async Commands

Async commands are automatically handled:

```python
import asyncio
from click_with_aliasing import command

@command(name="fetch", aliases=["f", "get"])
async def fetch():
    """Fetch data from API"""
    print("Fetching data...")
    await asyncio.sleep(2)
    print("Data fetched!")
```

```bash
$ python app.py fetch
Fetching data...
Data fetched!

$ python app.py f
Fetching data...
Data fetched!
```

## Multiple Commands

```python
from click_with_aliasing import group, command

@group()
def cli():
    """My CLI application"""
    pass

@command(name="start", aliases=["run", "serve"])
def start():
    """Start the server"""
    print("Server starting...")

@command(name="stop", aliases=["kill", "shutdown"])
def stop():
    """Stop the server"""
    print("Server stopping...")

@command(name="restart", aliases=["reload"])
def restart():
    """Restart the server"""
    print("Server restarting...")

cli.add_command(start)
cli.add_command(stop)
cli.add_command(restart)

if __name__ == "__main__":
    cli()
```

```bash
$ python app.py start
Server starting...

$ python app.py run
Server starting...

$ python app.py stop
Server stopping...
```

## Help Text

Aliases automatically appear in help text:

```python
from click_with_aliasing import group, command

@group()
def cli():
    pass

@command(name="deploy", aliases=["d", "dep"])
def deploy():
    """Deploy the application to production"""
    pass

cli.add_command(deploy)
```

```bash
$ python app.py --help
Commands:
  deploy (d, dep)  Deploy the application to production
```

### Help Flag (-h)

By default, commands support both `-h` and `--help` for displaying help:

```python
from click_with_aliasing import command

@command("process")
def process():
    """Process data"""
    print("Processing...")
```

```bash
$ python app.py process -h
Usage: app.py process [OPTIONS]

  Process data

Options:
  -h, --help  Show this message and exit.
```

However, if a command uses `-h` for another option, it will not have `-h` as a help alias:

```python
from click_with_aliasing import command, option

@command("connect")
@option("--host", "-h", help="Server hostname")
def connect(host):
    """Connect to a server"""
    print(f"Connecting to {host}")
```

```bash
# -h is used for --host option
$ python app.py connect -h localhost
Connecting to localhost

# Help is available via --help only
$ python app.py connect --help
Usage: app.py connect [OPTIONS]

  Connect to a server

Options:
  -h, --host TEXT  Server hostname
  --help           Show this message and exit.
```

## API Reference

```python
def command(
    name: str,
    *args,
    aliases: Optional[List[str]] = None,
    **kwargs,
) -> Callable[[Callable[..., Any]], Command]
```

### Parameters

- **name** (str): The name of the command
- **aliases** (List[str], optional): List of alternative names for the command
- **\*args**: Additional positional arguments passed to `click.command()`
- \***\*kwargs**: Additional keyword arguments passed to `click.command()`

### Returns

A decorator function that creates a `Command` instance with alias support.

## Advanced Examples

### Command with Multiple Options

```python
from click_with_aliasing import command
import click

@command(name="process", aliases=["p", "proc"])
@click.option("--input", "-i", required=True, help="Input file")
@click.option("--output", "-o", required=True, help="Output file")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.option("--format", type=click.Choice(["json", "xml", "csv"]), default="json")
def process(input, output, verbose, format):
    """Process data files"""
    if verbose:
        print(f"Processing {input} -> {output} (format: {format})")
    print("Processing complete!")
```

```bash
$ python app.py process -i data.txt -o result.json --verbose
Processing data.txt -> result.json (format: json)
Processing complete!

$ python app.py p -i data.txt -o result.json
Processing complete!
```

### Async Command with Options

```python
import asyncio
from click_with_aliasing import command
import click

@command(name="download", aliases=["dl", "fetch"])
@click.option("--url", required=True, help="URL to download")
@click.option("--output", "-o", help="Output filename")
async def download(url, output):
    """Download file from URL"""
    print(f"Downloading {url}...")
    await asyncio.sleep(1)  # Simulate download

    filename = output or url.split("/")[-1]
    print(f"Saved to {filename}")
```

```bash
$ python app.py download --url https://example.com/file.zip
Downloading https://example.com/file.zip...
Saved to file.zip

$ python app.py dl --url https://example.com/data.json -o mydata.json
Downloading https://example.com/data.json...
Saved to mydata.json
```
