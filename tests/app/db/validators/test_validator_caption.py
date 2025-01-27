import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_caption_optional


def test_validate_caption_optional() -> None:
    assert validate_caption_optional(cls=None, value=None) is None
    assert validate_caption_optional(cls=None, value="Valid Caption") == "Valid Caption"
    with pytest.raises(ValueError):
        validate_caption_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
