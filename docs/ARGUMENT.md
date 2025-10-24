# Argument

The `argument` decorator extends Click's argument functionality with mutual exclusivity, requirement dependencies, and group-level constraints, just like the `option` decorator but for positional arguments.

## Basic Usage

### Simple Argument

```python
from click_with_aliasing import command, argument

@command(name="greet")
@argument("name")
def greet(name):
    """Greet someone"""
    print(f"Hello, {name}!")
```

```bash
$ python app.py greet Alice
Hello, Alice!
```

### Multiple Arguments

```python
from click_with_aliasing import command, argument

@command(name="copy")
@argument("source")
@argument("dest")
def copy(source, dest):
    """Copy files"""
    print(f"Copying {source} to {dest}")
```

```bash
$ python app.py copy file1.txt file2.txt
Copying file1.txt to file2.txt
```

## Mutual Exclusivity

Ensure only one argument from a set is provided.

### Choose Input Type

```python
from click_with_aliasing import command, argument, option

@command(name="process")
@argument("file", required=False, mutually_exclusive=["data"])
@option("--data", mutually_exclusive=["file"], help="Process inline data")
def process(file, data):
    """Process a file or inline data"""
    if file:
        print(f"Processing file: {file}")
    elif data:
        print(f"Processing data: {data}")
    else:
        print("Please provide a file or --data option")
```

```bash
$ python app.py process input.txt
Processing file: input.txt

$ python app.py process --data "test content"
Processing data: test content

$ python app.py process input.txt --data "test"
Error: Argument 'file' is mutually exclusive with option '--data'
```

## Required Arguments

Specify arguments that must be used together with options.

### Database Credentials

```python
from click_with_aliasing import command, argument, option

@command(name="connect")
@argument("database", requires=["username", "password"])
@option("--username", requires=["database", "password"], help="Username")
@option("--password", requires=["database", "username"], help="Password")
@option("--host", default="localhost", help="Database host")
def connect(database, username, password, host):
    """Connect to a database"""
    if all([database, username, password]):
        print(f"Connecting to {database} at {host} as {username}")
```

```bash
$ python app.py connect mydb --username admin --password secret
Connecting to mydb at localhost as admin

$ python app.py connect mydb
Error: Argument 'database' requires options '--username' and '--password'
```

## Group-Level Constraints

Organize arguments and options into groups with collective constraints.

### Input Sources

```python
from click_with_aliasing import command, argument, option

@command(name="import")
@argument("file", required=False, group="source", group_mutually_exclusive=["api"])
@option("--url", group="api", group_mutually_exclusive=["source"], help="API URL")
@option("--token", group="api", group_mutually_exclusive=["source"], help="API token")
@option("--format", type=click.Choice(["json", "xml", "csv"]), default="json")
def import_data(file, url, token, format):
    """Import data from file or API"""
    if file:
        print(f"Importing from file: {file} (format: {format})")
    elif url and token:
        print(f"Importing from API: {url} (format: {format})")
    else:
        print("Please provide a file or --url with --token")
```

```bash
$ python app.py import data.json
Importing from file: data.json (format: json)

$ python app.py import --url https://api.example.com --token abc123
Importing from API: https://api.example.com (format: json)

$ python app.py import data.json --url https://api.example.com
Error: Argument 'file' (group 'source') is mutually exclusive with option '--url' (group 'api')
```

## Combined Features

### Deploy Command

```python
from click_with_aliasing import command, argument, option

@command(name="deploy")
@argument("target", mutually_exclusive=["all-targets"])
@option("--all-targets", is_flag=True, mutually_exclusive=["target"],
        help="Deploy to all targets")
@option("--config", requires=["target"], help="Configuration file")
@option("--force", is_flag=True, help="Force deployment")
def deploy(target, all_targets, config, force):
    """Deploy to a specific target or all targets"""
    if all_targets:
        print("Deploying to all targets")
    elif target:
        config_msg = f" with config {config}" if config else ""
        force_msg = " (forced)" if force else ""
        print(f"Deploying to {target}{config_msg}{force_msg}")
```

```bash
$ python app.py deploy production --config prod.yml
Deploying to production with config prod.yml

$ python app.py deploy --all-targets
Deploying to all targets

$ python app.py deploy production --all-targets
Error: Argument 'target' is mutually exclusive with option '--all-targets'
```

## Variadic Arguments

```python
from click_with_aliasing import command, argument, option
import click

@command(name="process")
@argument("files", nargs=-1, required=True)
@option("--output", "-o", help="Output directory")
@option("--verbose", "-v", is_flag=True)
def process(files, output, verbose):
    """Process multiple files"""
    if verbose:
        print(f"Processing {len(files)} files")

    for file in files:
        dest = f"{output}/{file}" if output else file
        print(f"Processing: {file} -> {dest}")
```

```bash
$ python app.py process file1.txt file2.txt file3.txt -o /output
Processing: file1.txt -> /output/file1.txt
Processing: file2.txt -> /output/file2.txt
Processing: file3.txt -> /output/file3.txt
```

## API Reference

```python
def argument(
    *param_decls: str,
    mutually_exclusive: Optional[List[str]] = None,
    requires: Optional[List[str]] = None,
    group: Optional[str] = None,
    group_mutually_exclusive: Optional[List[str]] = None,
    **kwargs: Any,
) -> Callable[[F], F]
```

### Parameters

- **\*param_decls** (str): Argument name
- **mutually_exclusive** (List[str], optional): List of parameter names (arguments or options) that cannot be used with this argument
- **requires** (List[str], optional): List of parameter names that must be provided with this argument
- **group** (str, optional): Group name for this argument
- **group_mutually_exclusive** (List[str], optional): List of group names that are mutually exclusive with this argument's group
- \***\*kwargs**: All standard Click argument parameters (type, nargs, required, etc.)

### Returns

A decorator function that adds the argument to the command.

## Advanced Examples

### Build Command

```python
from click_with_aliasing import command, argument, option
import click

@command(name="build")
@argument("target", type=click.Choice(["debug", "release"]), default="debug")
@option("--output", "-o", help="Output directory")
@option("--parallel", "-j", type=int, default=1, help="Parallel jobs")
@option("--verbose", "-v", is_flag=True, help="Verbose output")
@option("--clean", is_flag=True, help="Clean before build")
def build(target, output, parallel, verbose, clean):
    """Build the project"""
    if clean:
        print("Cleaning build directory...")

    if verbose:
        print(f"Building {target} with {parallel} parallel jobs")

    output_dir = output or f"build/{target}"
    print(f"Building to {output_dir}")
```

```bash
$ python app.py build release -o dist -j 4 --clean
Cleaning build directory...
Building release with 4 parallel jobs
Building to dist
```

### File Conversion

```python
from click_with_aliasing import command, argument, option
import click

@command(name="convert")
@argument("input-file")
@argument("output-file", required=False)
@option("--format", type=click.Choice(["json", "xml", "yaml"]), required=True)
@option("--pretty", is_flag=True, help="Pretty-print output")
@option("--validate", is_flag=True, help="Validate before converting")
def convert(input_file, output_file, format, pretty, validate):
    """Convert file between formats"""
    if validate:
        print(f"Validating {input_file}...")

    output = output_file or f"{input_file}.{format}"
    pretty_msg = " (pretty-printed)" if pretty else ""
    print(f"Converting {input_file} to {output} as {format}{pretty_msg}")
```

```bash
$ python app.py convert data.json --format yaml --pretty
Converting data.json to data.json.yaml as yaml (pretty-printed)

$ python app.py convert input.xml output.json --format json --validate
Validating input.xml...
Converting input.xml to output.json as json
```

### Package Manager

```python
from click_with_aliasing import command, argument, option

@command(name="install")
@argument("packages", nargs=-1, required=False, mutually_exclusive=["requirements"])
@option("--requirements", "-r", mutually_exclusive=["packages"],
        help="Install from requirements file")
@option("--upgrade", is_flag=True, help="Upgrade packages")
@option("--force", is_flag=True, help="Force reinstall")
def install(packages, requirements, upgrade, force):
    """Install packages"""
    flags = []
    if upgrade:
        flags.append("--upgrade")
    if force:
        flags.append("--force-reinstall")

    flag_str = " " + " ".join(flags) if flags else ""

    if requirements:
        print(f"Installing from {requirements}{flag_str}")
    elif packages:
        print(f"Installing: {', '.join(packages)}{flag_str}")
    else:
        print("Please specify packages or --requirements file")
```

```bash
$ python app.py install requests flask
Installing: requests, flask

$ python app.py install -r requirements.txt --upgrade
Installing from requirements.txt --upgrade

$ python app.py install requests -r requirements.txt
Error: Argument 'packages' is mutually exclusive with option '--requirements'
```
