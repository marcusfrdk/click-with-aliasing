# Rule

The `rule` decorator provides group-level validation for commands, ensuring that options and arguments meet specific constraints before execution. Rules validate the presence and combination of parameters.

## Basic Usage

### All or None Rule

Require that either all specified options are provided or none of them.

```python
from click_with_aliasing import group, command, option, rule

@group()
def cli():
    pass

@command(name="connect")
@option("--host", help="Database host")
@option("--port", type=int, help="Database port")
@option("--database", help="Database name")
@rule(["host", "port", "database"], mode="all_or_none")
def connect(host, port, database):
    """Connect to database"""
    if all([host, port, database]):
        print(f"Connecting to {database} at {host}:{port}")
    else:
        print("Using default connection")

cli.add_command(connect)
```

```bash
$ python app.py connect --host localhost --port 5432 --database mydb
Connecting to mydb at localhost:5432

$ python app.py connect
Using default connection

$ python app.py connect --host localhost
Error: Options ['host', 'port', 'database'] must all be provided or none at all
```

## Validation Modes

### At Least Mode

Require at least N options from the specified list.

```python
from click_with_aliasing import command, option, rule

@command(name="notify")
@option("--email", help="Email address")
@option("--sms", help="Phone number")
@option("--slack", help="Slack webhook")
@rule(["email", "sms", "slack"], mode="at_least", count=1)
def notify(email, sms, slack):
    """Send notification via at least one channel"""
    channels = []
    if email:
        channels.append(f"email to {email}")
    if sms:
        channels.append(f"SMS to {sms}")
    if slack:
        channels.append("Slack")

    print(f"Sending notification via: {', '.join(channels)}")
```

```bash
$ python app.py notify --email user@example.com
Sending notification via: email to user@example.com

$ python app.py notify --email user@example.com --sms 555-1234
Sending notification via: email to user@example.com, SMS to 555-1234

$ python app.py notify
Error: At least 1 of ['email', 'sms', 'slack'] must be provided
```

### At Most Mode

Allow at most N options from the specified list.

```python
from click_with_aliasing import command, option, rule

@command(name="format")
@option("--json", is_flag=True, help="JSON format")
@option("--xml", is_flag=True, help="XML format")
@option("--yaml", is_flag=True, help="YAML format")
@rule(["json", "xml", "yaml"], mode="at_most", count=1)
def format(json, xml, yaml):
    """Format output (choose at most one format)"""
    if json:
        print("Using JSON format")
    elif xml:
        print("Using XML format")
    elif yaml:
        print("Using YAML format")
    else:
        print("Using default format")
```

```bash
$ python app.py format --json
Using JSON format

$ python app.py format
Using default format

$ python app.py format --json --xml
Error: At most 1 of ['json', 'xml', 'yaml'] can be provided
```

### Exactly Mode

Require exactly N options from the specified list.

```python
from click_with_aliasing import command, option, rule

@command(name="compare")
@option("--file1", help="First file")
@option("--file2", help="Second file")
@option("--file3", help="Third file")
@rule(["file1", "file2", "file3"], mode="exactly", count=2)
def compare(file1, file2, file3):
    """Compare exactly two files"""
    files = [f for f in [file1, file2, file3] if f]
    print(f"Comparing: {files[0]} and {files[1]}")
```

```bash
$ python app.py compare --file1 a.txt --file2 b.txt
Comparing: a.txt and b.txt

$ python app.py compare --file1 a.txt
Error: Exactly 2 of ['file1', 'file2', 'file3'] must be provided

$ python app.py compare --file1 a.txt --file2 b.txt --file3 c.txt
Error: Exactly 2 of ['file1', 'file2', 'file3'] must be provided
```

## Exclusivity Constraints

### Exclusive from Options

Ensure rule parameters are not used with specific options.

```python
from click_with_aliasing import command, option, rule

@command(name="backup")
@option("--full", is_flag=True, help="Full backup")
@option("--incremental", is_flag=True, help="Incremental backup")
@option("--restore", help="Restore from backup file")
@rule(["full", "incremental"], mode="exactly", count=1,
      exclusive_from_options=["restore"])
def backup(full, incremental, restore):
    """Create backup or restore"""
    if restore:
        print(f"Restoring from {restore}")
    elif full:
        print("Creating full backup")
    elif incremental:
        print("Creating incremental backup")
```

```bash
$ python app.py backup --full
Creating full backup

$ python app.py backup --restore backup.tar.gz
Restoring from backup.tar.gz

$ python app.py backup --full --restore backup.tar.gz
Error: Options ['full', 'incremental'] cannot be used with options: restore
```

### Exclusive from Groups

Ensure rule parameters are not used with options from specific groups.

```python
from click_with_aliasing import command, option, rule

@command(name="process")
@option("--file", group="input", help="Input file")
@option("--url", group="input", help="Input URL")
@option("--json", group="format", help="JSON format")
@option("--xml", group="format", help="XML format")
@option("--output", help="Output location")
@rule(["file", "url"], mode="exactly", count=1, exclusive_from_groups=["format"])
def process(file, url, json, xml, output):
    """Process input"""
    source = file or url
    format_type = "json" if json else "xml" if xml else "default"
    print(f"Processing {source} in {format_type} format")
```

```bash
$ python app.py process --file data.txt
Processing data.txt in default format

$ python app.py process --file data.txt --json
Error: Options ['file', 'url'] cannot be used with options from groups: format
```

## Multiple Rules

You can apply multiple rules to the same command.

```python
from click_with_aliasing import command, option, rule

@command(name="deploy")
@option("--production", is_flag=True, help="Deploy to production")
@option("--staging", is_flag=True, help="Deploy to staging")
@option("--development", is_flag=True, help="Deploy to development")
@option("--tag", help="Git tag to deploy")
@option("--branch", help="Git branch to deploy")
@option("--commit", help="Git commit to deploy")
@rule(["production", "staging", "development"], mode="exactly", count=1)
@rule(["tag", "branch", "commit"], mode="exactly", count=1)
def deploy(production, staging, development, tag, branch, commit):
    """Deploy to environment"""
    env = "production" if production else "staging" if staging else "development"
    source = f"tag {tag}" if tag else f"branch {branch}" if branch else f"commit {commit}"
    print(f"Deploying {source} to {env}")
```

```bash
$ python app.py deploy --production --tag v1.0.0
Deploying tag v1.0.0 to production

$ python app.py deploy --staging --branch main
Deploying branch main to staging

$ python app.py deploy --production --staging --tag v1.0.0
Error: Exactly 1 of ['production', 'staging', 'development'] must be provided

$ python app.py deploy --production --tag v1.0.0 --branch main
Error: Exactly 1 of ['tag', 'branch', 'commit'] must be provided
```

## API Reference

```python
def rule(
    params: List[str],
    *,
    mode: str = "all_or_none",
    count: int = 0,
    exclusive_from_options: Optional[List[str]] = None,
    exclusive_from_groups: Optional[List[str]] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]
```

### Parameters

- **params** (List[str]): List of parameter names (options or arguments) to validate
- **mode** (str): Validation mode - one of:
  - `"all_or_none"`: All params must be provided or none at all
  - `"at_least"`: At least `count` params must be provided
  - `"at_most"`: At most `count` params can be provided
  - `"exactly"`: Exactly `count` params must be provided
- **count** (int): Number used with `at_least`, `at_most`, or `exactly` modes
- **exclusive_from_options** (List[str], optional): List of option names that cannot be used with the rule params
- **exclusive_from_groups** (List[str], optional): List of group names that cannot be used with the rule params

### Returns

A decorator function that adds validation rules to the command.

## Advanced Examples

### CI/CD Pipeline

```python
from click_with_aliasing import command, option, rule

@command(name="pipeline")
@option("--build", is_flag=True, help="Build stage")
@option("--test", is_flag=True, help="Test stage")
@option("--deploy", is_flag=True, help="Deploy stage")
@option("--skip-tests", is_flag=True, help="Skip test stage")
@option("--environment", type=click.Choice(["dev", "staging", "prod"]))
@rule(["build", "test", "deploy"], mode="at_least", count=1)
@rule(["test", "skip-tests"], mode="at_most", count=1)
@rule(["environment"], mode="exactly", count=1, exclusive_from_options=["skip-tests"])
def pipeline(build, test, deploy, skip_tests, environment):
    """Run CI/CD pipeline"""
    stages = []
    if build:
        stages.append("build")
    if test and not skip_tests:
        stages.append("test")
    if deploy:
        stages.append("deploy")

    print(f"Running pipeline stages: {', '.join(stages)}")
    print(f"Environment: {environment}")
```

```bash
$ python app.py pipeline --build --test --environment dev
Running pipeline stages: build, test
Environment: dev

$ python app.py pipeline --build --skip-tests --environment staging
Running pipeline stages: build
Environment: staging
```

### Database Migration

```python
from click_with_aliasing import command, option, rule

@command(name="migrate")
@option("--up", is_flag=True, help="Migrate up")
@option("--down", is_flag=True, help="Migrate down")
@option("--to-version", type=int, help="Migrate to specific version")
@option("--steps", type=int, help="Number of steps")
@option("--dry-run", is_flag=True, help="Dry run mode")
@option("--force", is_flag=True, help="Force migration")
@rule(["up", "down"], mode="exactly", count=1)
@rule(["to-version", "steps"], mode="at_most", count=1)
@rule(["force"], mode="all_or_none", exclusive_from_options=["dry-run"])
def migrate(up, down, to_version, steps, dry_run, force):
    """Run database migrations"""
    direction = "up" if up else "down"

    if to_version:
        target = f"to version {to_version}"
    elif steps:
        target = f"{steps} steps"
    else:
        target = "all pending"

    mode = "DRY RUN" if dry_run else "FORCE" if force else "normal"
    print(f"Migrating {direction} {target} ({mode} mode)")
```

```bash
$ python app.py migrate --up
Migrating up all pending (normal mode)

$ python app.py migrate --down --steps 3 --dry-run
Migrating down 3 steps (DRY RUN mode)

$ python app.py migrate --up --to-version 5 --force
Migrating up to version 5 (FORCE mode)
```

### Complex Validation

```python
from click_with_aliasing import command, option, rule
import click

@command(name="transfer")
@option("--source-file", group="source", help="Source file")
@option("--source-url", group="source", help="Source URL")
@option("--dest-file", group="dest", help="Destination file")
@option("--dest-url", group="dest", help="Destination URL")
@option("--credentials", help="Authentication credentials")
@option("--timeout", type=int, default=30, help="Transfer timeout")
@rule(["source-file", "source-url"], mode="exactly", count=1)
@rule(["dest-file", "dest-url"], mode="exactly", count=1)
@rule(["credentials"], mode="exactly", count=1,
      exclusive_from_groups=["source"], exclusive_from_options=["source-file"])
def transfer(source_file, source_url, dest_file, dest_url, credentials, timeout):
    """Transfer data between locations"""
    source = source_file or source_url
    dest = dest_file or dest_url

    auth = f" (with credentials)" if credentials else ""
    print(f"Transferring {source} -> {dest}{auth} (timeout: {timeout}s)")
```

```bash
$ python app.py transfer --source-file data.txt --dest-url https://example.com
Transferring data.txt -> https://example.com (timeout: 30s)

$ python app.py transfer --source-url https://api.com --dest-file output.txt --credentials token123
Transferring https://api.com -> output.txt (with credentials) (timeout: 30s)
```
