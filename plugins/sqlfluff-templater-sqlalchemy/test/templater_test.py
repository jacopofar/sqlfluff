"""Tests for the SQLAlchemy templater."""

import pytest


from sqlfluff.core import FluffConfig

from sqlfluff_templater_sqlalchemy.templater import SqlalchemyTemplater

def test__templater_raw():
    """Test the raw templater."""
    t = SqlalchemyTemplater()
    instr = "SELECT * FROM {{blah}}"
    outstr, _ = t.process(in_str=instr, fname="test")
    assert str(outstr) == "SELECT * FROM {{blah}}"


@pytest.mark.parametrize(
    "instr, expected_outstr",
    [
        (
            "SELECT * FROM f, o, o WHERE a < 10\n\n",
            "SELECT * FROM f, o, o WHERE a < 10\n\n",
        ),
        # Test for issue #968. This was previously raising an UnboundLocalError.
        (
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = :user_id AND date > :start_date
            """,
            """
            SELECT user_mail, city_id
            FROM users_data
            WHERE userid = 42 AND date > '2021-10-01'
            """
        ),
    ],
    ids=["no_changes", "simple_substitution"],
)
def test__templater_sqlalchemy(instr, expected_outstr):
    """Test sqlalchemy templating."""
    t = SqlalchemyTemplater(override_context=dict(user_id="42", start_date="'2021-10-01'"))
    outstr, _ = t.process(in_str=instr, fname="test", config=FluffConfig())
    assert str(outstr) == expected_outstr