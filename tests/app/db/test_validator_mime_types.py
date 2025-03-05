from typing import Any
from unittest.mock import MagicMock

import pytest

from app.db.validators import validate_mime_type_optional, validate_mime_type_required


@pytest.fixture(scope="module")
def mock_settings() -> Any:
    yield MagicMock(api=MagicMock(allowed_mime_types=["jpg", "png"]))


def test_validate_mime_type_required(mock_settings: Any) -> None:
    assert validate_mime_type_required(cls=None, value="jpg") == "jpg"
    assert validate_mime_type_required(cls=None, value="png") == "png"
    with pytest.raises(ValueError):
        validate_mime_type_required(cls=None, value="exc")


def test_validate_mime_type_optional(mock_settings: Any) -> None:
    assert validate_mime_type_optional(cls=None, value=None) is None
    assert validate_mime_type_optional(cls=None, value="jpg") == "jpg"
    assert validate_mime_type_optional(cls=None, value="png") == "png"
    with pytest.raises(ValueError):
        validate_mime_type_optional(cls=None, value="exc")
