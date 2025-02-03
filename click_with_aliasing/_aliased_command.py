""" AliasedCommand class for Click commands with alias support. """

import click


class AliasedCommand(click.Command):
    """A Click command that supports aliasing."""

    def __init__(self, *args, **kwargs):
        self.aliases = kwargs.pop("aliases", [])
        super().__init__(*args, **kwargs)
