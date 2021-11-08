"""Defines the hook endpoints for the sqlalchemy templater plugin."""

from sqlfluff_templater_sqlalchemy.templater import SqlalchemyTemplater
from sqlfluff.core.plugin import hookimpl


@hookimpl
def get_templaters():
    """Get templaters."""
    return [SqlalchemyTemplater]