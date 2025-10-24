# Option

The `option` decorator extends Click's option functionality with mutual exclusivity, requirement dependencies, and group-level constraints. It's a drop-in replacement for `@click.option()` with enhanced validation capabilities.

## Basic Usage

### Simple Option

```python
from click_with_aliasing import command, option

@command(name="greet")
@option("--name", default="World", help="Name to greet")
def greet(name):
    """Greet someone"""
    print(f"Hello, {name}!")
```

```bash
$ python app.py greet --name Alice
Hello, Alice!
```

## Mutual Exclusivity

Ensure only one option from a set can be used at a time.

### Two Mutually Exclusive Options

```python
from click_with_aliasing import command, option

@command(name="format")
@option("--json", is_flag=True, mutually_exclusive=["xml", "yaml"])
@option("--xml", is_flag=True, mutually_exclusive=["json", "yaml"])
@option("--yaml", is_flag=True, mutually_exclusive=["json", "xml"])
def format(json, xml, yaml):
    """Format output"""
    if json:
        print("Using JSON format")
    elif xml:
        print("Using XML format")
    elif yaml:
        print("Using YAML format")
```

```bash
$ python app.py format --json
Using JSON format

$ python app.py format --xml
Using XML format

$ python app.py format --json --xml
Error: Option '--json' is mutually exclusive with '--xml'
```

### File or URL Input

```python
from click_with_aliasing import command, option

@command(name="load")
@option("--file", mutually_exclusive=["url"], help="Load from file")
@option("--url", mutually_exclusive=["file"], help="Load from URL")
def load(file, url):
    """Load data from file or URL"""
    if file:
        print(f"Loading from file: {file}")
    elif url:
        print(f"Loading from URL: {url}")
    else:
        print("Please specify --file or --url")
```

```bash
$ python app.py load --file data.json
Loading from file: data.json

$ python app.py load --url https://api.example.com
Loading from URL: https://api.example.com

$ python app.py load --file data.json --url https://api.example.com
Error: Option '--file' is mutually exclusive with '--url'
```

## Required Options

Specify options that must be used together.

### Credentials Example

```python
from click_with_aliasing import command, option

@command(name="login")
@option("--username", requires=["password"], help="Username")
@option("--password", requires=["username"], help="Password")
def login(username, password):
    """Login to the system"""
    if username and password:
        print(f"Logging in as {username}")
```

```bash
$ python app.py login --username admin --password secret
Logging in as admin

$ python app.py login --username admin
Error: Option '--username' requires '--password'
```

### Database Connection

```python
from click_with_aliasing import command, option

@command(name="connect")
@option("--host", requires=["port", "database"], help="Database host")
@option("--port", requires=["host", "database"], help="Database port")
@option("--database", requires=["host", "port"], help="Database name")
@option("--ssl", is_flag=True, help="Use SSL connection")
def connect(host, port, database, ssl):
    """Connect to database"""
    if all([host, port, database]):
        protocol = "ssl" if ssl else "tcp"
        print(f"Connecting to {host}:{port}/{database} via {protocol}")
```

```bash
$ python app.py connect --host localhost --port 5432 --database mydb
Connecting to localhost:5432/mydb via tcp

$ python app.py connect --host localhost
Error: Option '--host' requires '--port' and '--database'
```

## Group-Level Constraints

Organize related options into groups with collective constraints.

### Mutually Exclusive Groups

```python
from click_with_aliasing import command, option

@command(name="process")
@option("--json", is_flag=True, group="format", group_mutually_exclusive=["output"])
@option("--xml", is_flag=True, group="format", group_mutually_exclusive=["output"])
@option("--csv", is_flag=True, group="format", group_mutually_exclusive=["output"])
@option("--stdout", is_flag=True, group="output", group_mutually_exclusive=["format"])
@option("--file", group="output", group_mutually_exclusive=["format"])
def process(json, xml, csv, stdout, file):
    """Process data with format and output options"""
    format_type = "json" if json else "xml" if xml else "csv" if csv else "default"

    if stdout:
        print(f"Output to stdout in {format_type} format")
    elif file:
        print(f"Output to {file} in {format_type} format")
    else:
        print(f"Using {format_type} format")
```

```bash
$ python app.py process --json
Using json format

$ python app.py process --json --stdout
Error: Option '--json' (group 'format') is mutually exclusive with '--stdout' (group 'output')

$ python app.py process --xml --file output.txt
Error: Option '--xml' (group 'format') is mutually exclusive with '--file' (group 'output')
```

## Combined Features

### Authentication Options

```python
from click_with_aliasing import command, option

@command(name="auth")
@option("--username", requires=["password"], mutually_exclusive=["token"])
@option("--password", requires=["username"], mutually_exclusive=["token"])
@option("--token", mutually_exclusive=["username", "password"])
def auth(username, password, token):
    """Authenticate with username/password or token"""
    if token:
        print(f"Authenticating with token")
    elif username and password:
        print(f"Authenticating as {username}")
```

```bash
$ python app.py auth --token abc123
Authenticating with token

$ python app.py auth --username admin --password secret
Authenticating as admin

$ python app.py auth --username admin
Error: Option '--username' requires '--password'

$ python app.py auth --token abc123 --username admin
Error: Option '--token' is mutually exclusive with '--username'
```

### Complex Validation

```python
from click_with_aliasing import command, option

@command(name="backup")
@option("--full", is_flag=True, mutually_exclusive=["incremental"],
        group="type", group_mutually_exclusive=["restore"])
@option("--incremental", is_flag=True, mutually_exclusive=["full"],
        group="type", group_mutually_exclusive=["restore"])
@option("--restore", group="restore", group_mutually_exclusive=["type"])
@option("--output", help="Output location")
def backup(full, incremental, restore, output):
    """Backup or restore data"""
    if restore:
        print(f"Restoring from {restore}")
    elif full:
        print("Creating full backup")
    elif incremental:
        print("Creating incremental backup")

    if output:
        print(f"Output: {output}")
```

```bash
$ python app.py backup --full --output /backups
Creating full backup
Output: /backups

$ python app.py backup --full --restore backup.tar.gz
Error: Option '--full' (group 'type') is mutually exclusive with '--restore' (group 'restore')
```

## API Reference

```python
def option(
    *param_decls: str,
    mutually_exclusive: Optional[List[str]] = None,
    requires: Optional[List[str]] = None,
    group: Optional[str] = None,
    group_mutually_exclusive: Optional[List[str]] = None,
    **kwargs: Any,
) -> Callable[[F], F]
```

### Parameters

- **\*param_decls** (str): Option declarations (e.g., "--name", "-n")
- **mutually_exclusive** (List[str], optional): List of option names that cannot be used with this option
- **requires** (List[str], optional): List of option names that must be provided with this option
- **group** (str, optional): Group name for this option
- **group_mutually_exclusive** (List[str], optional): List of group names that are mutually exclusive with this option's group
- \***\*kwargs**: All standard Click option parameters (default, type, help, etc.)

### Returns

A decorator function that adds the option to the command.

## Advanced Examples

### API Configuration

```python
from click_with_aliasing import command, option
import click

@command(name="api-call")
@option("--endpoint", required=True, help="API endpoint")
@option("--method", type=click.Choice(["GET", "POST", "PUT", "DELETE"]), default="GET")
@option("--data", help="Request data (JSON)", mutually_exclusive=["file"])
@option("--file", help="Request data from file", mutually_exclusive=["data"])
@option("--header", "-H", multiple=True, help="HTTP headers")
@option("--timeout", type=int, default=30, help="Request timeout in seconds")
@option("--verbose", "-v", is_flag=True, help="Verbose output")
def api_call(endpoint, method, data, file, header, timeout, verbose):
    """Make an API call"""
    if verbose:
        print(f"Method: {method}")
        print(f"Endpoint: {endpoint}")
        print(f"Timeout: {timeout}s")
        if header:
            print(f"Headers: {', '.join(header)}")

    if data:
        print(f"Sending data: {data}")
    elif file:
        print(f"Sending data from: {file}")

    print(f"Calling {method} {endpoint}")
```

```bash
$ python app.py api-call --endpoint /users --method POST --data '{"name":"Alice"}' -v
Method: POST
Endpoint: /users
Timeout: 30s
Sending data: {"name":"Alice"}
Calling POST /users
```

### Docker-like Options

```python
from click_with_aliasing import command, option

@command(name="run")
@option("--image", required=True, help="Container image")
@option("--name", help="Container name")
@option("--detach", "-d", is_flag=True, help="Run in background")
@option("--interactive", "-i", is_flag=True, mutually_exclusive=["detach"])
@option("--tty", "-t", is_flag=True, requires=["interactive"])
@option("--port", "-p", multiple=True, help="Port mapping")
@option("--volume", "-v", multiple=True, help="Volume mapping")
@option("--env", "-e", multiple=True, help="Environment variables")
def run(image, name, detach, interactive, tty, port, volume, env):
    """Run a container"""
    mode = "detached" if detach else "interactive" if interactive else "default"
    print(f"Running {image} in {mode} mode")

    if name:
        print(f"Container name: {name}")
    if port:
        print(f"Ports: {', '.join(port)}")
    if volume:
        print(f"Volumes: {', '.join(volume)}")
    if env:
        print(f"Environment: {', '.join(env)}")
```

```bash
$ python app.py run --image nginx --detach --port 80:8080 --name web
Running nginx in detached mode
Container name: web
Ports: 80:8080

$ python app.py run --image ubuntu -it
Running ubuntu in interactive mode
```
