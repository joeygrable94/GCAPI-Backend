from typing import Dict

import pytest

from app.schemas.website_keywordcorpus import (
    ValidateKeywordCorpusOptional,
    ValidateKeywordCorpusRequired,
    ValidateKeywordRawTextOptional,
    ValidateKeywordRawTextRequired,
)


# Test ValidateKeywordCorpusRequired
def test_keyword_corpus_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"corpus": "This is a sample corpus text."}
    assert ValidateKeywordCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_missing_corpus() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_empty_str_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": ""}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_invalid_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": "a" * 50001}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusRequired.validate(input_data)


# Test ValidateKeywordCorpusOptional
def test_keyword_corpus_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"corpus": "This is a sample corpus text."}
    assert ValidateKeywordCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_missing_corpus() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateKeywordCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_empty_str_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": ""}
    assert ValidateKeywordCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_invalid_corpus() -> None:
    input_data: Dict[str, str] = {"corpus": "a" * 50001}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusOptional.validate(input_data)


# Test ValidateKeywordRawTextRequired
def test_keyword_rawtext_required_with_valid_input() -> None:
    input_data: Dict[str, str] = {"rawtext": "This is a sample raw text."}
    assert ValidateKeywordRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_missing_rawtext() -> None:
    input_data: Dict[str, str] = {}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_empty_str_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": ""}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_invalid_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": "a" * 50001}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextRequired.validate(input_data)


# Test ValidateKeywordRawTextOptional
def test_keyword_rawtext_optional_with_valid_input() -> None:
    input_data: Dict[str, str] = {"rawtext": "This is a sample raw text."}
    assert ValidateKeywordRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_missing_rawtext() -> None:
    input_data: Dict[str, str] = {}
    assert ValidateKeywordRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_empty_str_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": ""}
    assert ValidateKeywordRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_invalid_rawtext() -> None:
    input_data: Dict[str, str] = {"rawtext": "a" * 50010}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextOptional.validate(input_data)
