import pytest

from app.db.validators import validate_corpus_optional, validate_corpus_required
from tests.constants.limits import LONGTEXT_MAX_STR


def test_validate_corpus_required() -> None:
    assert validate_corpus_required(cls=None, value="Valid Corpus") == "Valid Corpus"
    with pytest.raises(ValueError):
        validate_corpus_required(cls=None, value=LONGTEXT_MAX_STR + "a")
    with pytest.raises(ValueError):
        assert validate_corpus_required(cls=None, value="")


def test_validate_corpus_optional() -> None:
    assert validate_corpus_optional(cls=None, value=None) is None
    assert validate_corpus_optional(cls=None, value="Valid Corpus") == "Valid Corpus"
    with pytest.raises(ValueError):
        validate_corpus_optional(cls=None, value=LONGTEXT_MAX_STR + "a")
