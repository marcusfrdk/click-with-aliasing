# Group

The `group` decorator creates a command group with optional alias support. Groups organize related commands together and support nested subgroups.

## Basic Usage

### Simple Group

```python
from click_with_aliasing import group, command

@group(name="database")
def database():
    """Database management commands"""
    pass

@command(name="migrate")
def migrate():
    """Run migrations"""
    print("Running migrations...")

database.add_command(migrate)
```

```bash
$ python app.py database migrate
Running migrations...
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
    """Run migrations"""
    print("Running migrations...")

database.add_command(migrate)
```

All of these work:

```bash
$ python app.py database migrate
$ python app.py db migrate
$ python app.py database m
$ python app.py db m
```

## Multiple Subcommands

```python
from click_with_aliasing import group, command

@group(name="server", aliases=["srv", "s"])
def server():
    """Server management"""
    pass

@command(name="start", aliases=["run"])
def start():
    """Start the server"""
    print("Server starting...")

@command(name="stop", aliases=["kill"])
def stop():
    """Stop the server"""
    print("Server stopping...")

@command(name="restart", aliases=["reload"])
def restart():
    """Restart the server"""
    print("Server restarting...")

@command(name="status", aliases=["stat", "st"])
def status():
    """Check server status"""
    print("Server is running")

server.add_command(start)
server.add_command(stop)
server.add_command(restart)
server.add_command(status)
```

```bash
$ python app.py server start
Server starting...

$ python app.py srv run
Server starting...

$ python app.py s status
Server is running

$ python app.py s st
Server is running
```

## Nested Groups

```python
from click_with_aliasing import group, command

@group()
def cli():
    """Main CLI"""
    pass

@group(name="database", aliases=["db"])
def database():
    """Database commands"""
    pass

@group(name="cache", aliases=["c"])
def cache():
    """Cache commands"""
    pass

@command(name="migrate", aliases=["m"])
def migrate():
    """Run migrations"""
    print("Migrating...")

@command(name="clear", aliases=["cl"])
def clear():
    """Clear cache"""
    print("Cache cleared")

database.add_command(migrate)
cache.add_command(clear)
cli.add_command(database)
cli.add_command(cache)
```

```bash
$ python app.py database migrate
Migrating...

$ python app.py db m
Migrating...

$ python app.py cache clear
Cache cleared

$ python app.py c cl
Cache cleared
```

## Async Groups

Groups can be async functions:

```python
import asyncio
from click_with_aliasing import group, command

@group(name="api", aliases=["a"])
async def api():
    """API management"""
    print("Initializing API...")
    await asyncio.sleep(0.1)

@command(name="start", aliases=["run"])
async def start():
    """Start API server"""
    print("Starting API server...")
    await asyncio.sleep(1)
    print("API server started!")

api.add_command(start)
```

```bash
$ python app.py api start
Initializing API...
Starting API server...
API server started!

$ python app.py a run
Initializing API...
Starting API server...
API server started!
```

## Group with Context

```python
from click_with_aliasing import group, command
import click

@group(name="config", aliases=["cfg"])
@click.pass_context
def config(ctx):
    """Configuration management"""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = "/etc/myapp/config.yml"

@command(name="show", aliases=["s", "display"])
@click.pass_context
def show(ctx):
    """Show configuration"""
    print(f"Config path: {ctx.obj['config_path']}")

@command(name="edit", aliases=["e"])
@click.pass_context
def edit(ctx):
    """Edit configuration"""
    print(f"Editing: {ctx.obj['config_path']}")

config.add_command(show)
config.add_command(edit)
```

```bash
$ python app.py config show
Config path: /etc/myapp/config.yml

$ python app.py cfg s
Config path: /etc/myapp/config.yml
```

## Help Text

Aliases appear in help text for both groups and commands:

```python
from click_with_aliasing import group, command

@group()
def cli():
    pass

@group(name="database", aliases=["db", "d"])
def database():
    """Database management commands"""
    pass

@command(name="migrate", aliases=["m", "mig"])
def migrate():
    """Run database migrations"""
    pass

@command(name="seed", aliases=["s"])
def seed():
    """Seed the database"""
    pass

database.add_command(migrate)
database.add_command(seed)
cli.add_command(database)
```

```bash
$ python app.py --help
Commands:
  database (db, d)  Database management commands

$ python app.py database --help
Usage: app.py database [OPTIONS] COMMAND [ARGS]...

  Database management commands

Commands:
  migrate (m, mig)  Run database migrations
  seed (s)          Seed the database
```

## API Reference

```python
def group(
    name: Optional[str] = None,
    *,
    aliases: Optional[List[str]] = None,
    **kwargs,
) -> Callable[[Callable[..., Any]], Group]
```

### Parameters

- **name** (str, optional): The name of the group. If not provided, uses the function name
- **aliases** (List[str], optional): List of alternative names for the group
- \***\*kwargs**: Additional keyword arguments passed to `click.group()`

### Returns

A decorator function that creates a `Group` instance with alias support.

## Advanced Examples

### Multi-Level Nested Groups

```python
from click_with_aliasing import group, command

@group()
def cli():
    """Main CLI"""
    pass

@group(name="cloud", aliases=["c"])
def cloud():
    """Cloud services"""
    pass

@group(name="aws", aliases=["a"])
def aws():
    """AWS commands"""
    pass

@group(name="azure", aliases=["az"])
def azure():
    """Azure commands"""
    pass

@command(name="deploy", aliases=["d"])
def aws_deploy():
    """Deploy to AWS"""
    print("Deploying to AWS...")

@command(name="deploy", aliases=["d"])
def azure_deploy():
    """Deploy to Azure"""
    print("Deploying to Azure...")

aws.add_command(aws_deploy)
azure.add_command(azure_deploy)
cloud.add_command(aws)
cloud.add_command(azure)
cli.add_command(cloud)
```

```bash
$ python app.py cloud aws deploy
Deploying to AWS...

$ python app.py c a d
Deploying to AWS...

$ python app.py cloud azure deploy
Deploying to Azure...

$ python app.py c az d
Deploying to Azure...
```

### Group with Shared Options

```python
from click_with_aliasing import group, command
import click

@group(name="docker", aliases=["d"])
@click.option("--host", default="localhost", help="Docker host")
@click.pass_context
def docker(ctx, host):
    """Docker management"""
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    print(f"Using Docker host: {host}")

@command(name="ps", aliases=["list", "ls"])
@click.pass_context
def ps(ctx):
    """List containers"""
    print(f"Listing containers on {ctx.obj['host']}")

@command(name="stop", aliases=["kill"])
@click.argument("container")
@click.pass_context
def stop(ctx, container):
    """Stop a container"""
    print(f"Stopping {container} on {ctx.obj['host']}")

docker.add_command(ps)
docker.add_command(stop)
```

```bash
$ python app.py docker --host remote.server ps
Using Docker host: remote.server
Listing containers on remote.server

$ python app.py d --host remote.server ls
Using Docker host: remote.server
Listing containers on remote.server
```
