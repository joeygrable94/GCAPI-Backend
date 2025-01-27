import pytest

from app.core.config import settings
from app.db.validators import validate_size_kb_optional, validate_size_kb_required


def test_validate_size_kb_required() -> None:
    assert (
        validate_size_kb_required(cls=None, value=settings.api.payload_limit_kb)
        == settings.api.payload_limit_kb
    )
    with pytest.raises(ValueError):
        assert validate_size_kb_required(cls=None, value=0)
    with pytest.raises(ValueError):
        validate_size_kb_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_size_kb_required(cls=None, value=settings.api.payload_limit_kb + 1)


def test_validate_size_kb_optional() -> None:
    assert validate_size_kb_optional(cls=None, value=None) is None
    assert (
        validate_size_kb_optional(cls=None, value=settings.api.payload_limit_kb)
        == settings.api.payload_limit_kb
    )
    with pytest.raises(ValueError):
        assert validate_size_kb_optional(cls=None, value=0)
    with pytest.raises(ValueError):
        validate_size_kb_optional(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_size_kb_optional(cls=None, value=settings.api.payload_limit_kb + 1)
