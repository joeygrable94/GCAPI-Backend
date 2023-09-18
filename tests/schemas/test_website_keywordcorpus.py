from typing import Dict

import pytest

from app.db.validators import (
    ValidateSchemaCorpusOptional,
    ValidateSchemaCorpusRequired,
    ValidateSchemaRawTextOptional,
    ValidateSchemaRawTextRequired,
)


# Test ValidateSchemaCorpusRequired
def test_keyword_corpus_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"corpus": "This is a sample corpus text."}
    assert ValidateSchemaCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_missing_corpus() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_empty_str_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": ""}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_invalid_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusRequired.validate(input_data)


# Test ValidateSchemaCorpusOptional
def test_keyword_corpus_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"corpus": "This is a sample corpus text."}
    assert ValidateSchemaCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_missing_corpus() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateSchemaCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_empty_str_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": ""}
    assert ValidateSchemaCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_invalid_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusOptional.validate(input_data)


# Test ValidateSchemaRawTextRequired
def test_keyword_rawtext_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"rawtext": "This is a sample raw text."}
    assert ValidateSchemaRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_missing_rawtext() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_empty_str_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": ""}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_invalid_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextRequired.validate(input_data)


# Test ValidateSchemaRawTextOptional
def test_keyword_rawtext_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"rawtext": "This is a sample raw text."}
    assert ValidateSchemaRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_missing_rawtext() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateSchemaRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_empty_str_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": ""}
    assert ValidateSchemaRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_invalid_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextOptional.validate(input_data)
