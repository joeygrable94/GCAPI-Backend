import pytest

from app.db.validators import validate_email_required
from tests.constants.limits import LONGTEXT_MAX_STR


def test_validate_email_required() -> None:
    assert (
        validate_email_required(cls=None, value="test@example.com")
        == "test@example.com"
    )
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value="a")
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value=LONGTEXT_MAX_STR + "a")
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value="notanemail")
