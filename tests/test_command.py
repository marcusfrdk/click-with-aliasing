""" Test the command decorator and the AliasedCommand class. """

# pylint: disable=W0621

import click
import pytest
from click.testing import CliRunner

from click_with_aliasing import command, group


@command(name="test_command", aliases=["tc", "tcmd"])
def cmd():
    """A simple test command."""
    click.echo("Test command executed")


@group()
def cli():
    """A simple Click group."""


cli.add_command(cmd)


@pytest.fixture
def runner():
    """Fixture for invoking Click commands."""
    return CliRunner()


def test_command_name():
    """Test that the command name is correctly assigned."""
    assert cmd.name == "test_command"


def test_command_aliases():
    """Test that aliases are correctly assigned."""
    assert hasattr(cmd, "aliases")
    assert cmd.aliases == ["tc", "tcmd"]


def test_command_execution(runner: CliRunner):
    """Test that the command runs successfully."""
    result = runner.invoke(cli, ["test_command"])
    assert result.exit_code == 0
    assert "Test command executed" in result.output


def test_command_alias_execution(runner: CliRunner):
    """Test that the command executes via its alias."""
    for alias in ["tc", "tcmd"]:
        result = runner.invoke(cli, [alias])
        assert result.exit_code == 0
        assert "Test command executed" in result.output
