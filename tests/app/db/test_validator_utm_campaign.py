import pytest

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.db.validators import validate_utm_campaign_optional


def test_validate_utm_campaign_optional() -> None:
    assert validate_utm_campaign_optional(cls=None, value=None) is None
    assert (
        validate_utm_campaign_optional(cls=None, value="Valid-UTM-Campaign")
        == "Valid-UTM-Campaign"
    )
    with pytest.raises(ValueError):
        validate_utm_campaign_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1)
        )
    with pytest.raises(ValueError):
        validate_utm_campaign_optional(cls=None, value="Valid UTM Campaign")
