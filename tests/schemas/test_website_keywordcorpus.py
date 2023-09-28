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
    assert ValidateSchemaCorpusRequired.model_validate(input_data)


def test_keyword_corpus_required_with_missing_corpus() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusRequired.model_validate(input_data)


def test_keyword_corpus_required_with_empty_str_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": ""}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusRequired.model_validate(input_data)


def test_keyword_corpus_required_with_invalid_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusRequired.model_validate(input_data)


# Test ValidateSchemaCorpusOptional
def test_keyword_corpus_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"corpus": "This is a sample corpus text."}
    assert ValidateSchemaCorpusOptional.model_validate(input_data)


def test_keyword_corpus_optional_with_missing_corpus() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateSchemaCorpusOptional.model_validate(input_data)


def test_keyword_corpus_optional_with_empty_str_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": ""}
    assert ValidateSchemaCorpusOptional.model_validate(input_data)


def test_keyword_corpus_optional_with_invalid_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaCorpusOptional.model_validate(input_data)


# Test ValidateSchemaRawTextRequired
def test_keyword_rawtext_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"rawtext": "This is a sample raw text."}
    assert ValidateSchemaRawTextRequired.model_validate(input_data)


def test_keyword_rawtext_required_with_missing_rawtext() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextRequired.model_validate(input_data)


def test_keyword_rawtext_required_with_empty_str_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": ""}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextRequired.model_validate(input_data)


def test_keyword_rawtext_required_with_invalid_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextRequired.model_validate(input_data)


# Test ValidateSchemaRawTextOptional
def test_keyword_rawtext_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"rawtext": "This is a sample raw text."}
    assert ValidateSchemaRawTextOptional.model_validate(input_data)


def test_keyword_rawtext_optional_with_missing_rawtext() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateSchemaRawTextOptional.model_validate(input_data)


def test_keyword_rawtext_optional_with_empty_str_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": ""}
    assert ValidateSchemaRawTextOptional.model_validate(input_data)


def test_keyword_rawtext_optional_with_invalid_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": "a" * 4000000001}
    with pytest.raises(ValueError):
        ValidateSchemaRawTextOptional.model_validate(input_data)
