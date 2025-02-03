""" Tests for the group decorator. """

# pylint: disable=W0621

import click
import pytest
from click.testing import CliRunner

from click_with_aliasing import command, group


@command(name="test_command", aliases=["tc", "tcmd"])
def cmd():
    """A simple test command."""
    click.echo("Test command executed")


@group(name="test_group", aliases=["tg", "tgrp"])
def grp():
    """A simple test group."""


grp.add_command(cmd)


@pytest.fixture
def runner():
    """Fixture for invoking Click commands."""
    return CliRunner()


def test_group_name():
    """Test that the group name is correctly assigned."""
    assert grp.name == "test_group"


def test_group_aliases():
    """Test that aliases are correctly assigned to the group."""
    assert hasattr(grp, "aliases")
    assert grp.aliases == ["tg", "tgrp"]


def test_group_command_execution(runner: CliRunner):
    """Test that the command within the group runs successfully."""
    result = runner.invoke(grp, ["test_command"])
    assert result.exit_code == 0
    assert "Test command executed" in result.output


def test_group_command_alias_execution(runner: CliRunner):
    """Test that the command within the group executes via its alias."""
    for alias in ["tc", "tcmd"]:
        result = runner.invoke(grp, [alias])
        assert result.exit_code == 0
        assert "Test command executed" in result.output
