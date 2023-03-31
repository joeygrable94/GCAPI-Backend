import pytest

from app.schemas.website_keywordcorpus import (
    ValidateKeywordCorpusOptional,
    ValidateKeywordCorpusRequired,
    ValidateKeywordRawTextOptional,
    ValidateKeywordRawTextRequired,
)


# Test ValidateKeywordCorpusRequired
def test_keyword_corpus_required_with_valid_input():
    input_data = {"corpus": "This is a sample corpus text."}
    assert ValidateKeywordCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_missing_corpus():
    input_data = {}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_empty_str_corpus():
    input_data = {"corpus": ""}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusRequired.validate(input_data)


def test_keyword_corpus_required_with_invalid_corpus():
    input_data = {"corpus": "a" * 50001}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusRequired.validate(input_data)


# Test ValidateKeywordCorpusOptional
def test_keyword_corpus_optional_with_valid_input():
    input_data = {"corpus": "This is a sample corpus text."}
    assert ValidateKeywordCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_missing_corpus():
    input_data = {}
    assert ValidateKeywordCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_empty_str_corpus():
    input_data = {"corpus": ""}
    assert ValidateKeywordCorpusOptional.validate(input_data)


def test_keyword_corpus_optional_with_invalid_corpus():
    input_data = {"corpus": "a" * 50001}
    with pytest.raises(ValueError):
        ValidateKeywordCorpusOptional.validate(input_data)


# Test ValidateKeywordRawTextRequired
def test_keyword_rawtext_required_with_valid_input():
    input_data = {"rawtext": "This is a sample raw text."}
    assert ValidateKeywordRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_missing_rawtext():
    input_data = {}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_empty_str_rawtext():
    input_data = {"rawtext": ""}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextRequired.validate(input_data)


def test_keyword_rawtext_required_with_invalid_rawtext():
    input_data = {"rawtext": "a" * 50001}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextRequired.validate(input_data)


# Test ValidateKeywordRawTextOptional
def test_keyword_rawtext_optional_with_valid_input():
    input_data = {"rawtext": "This is a sample raw text."}
    assert ValidateKeywordRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_missing_rawtext():
    input_data = {}
    assert ValidateKeywordRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_empty_str_rawtext():
    input_data = {"rawtext": ""}
    assert ValidateKeywordRawTextOptional.validate(input_data)


def test_keyword_rawtext_optional_with_invalid_rawtext():
    input_data = {"rawtext": "a" * 50010}
    with pytest.raises(ValueError):
        ValidateKeywordRawTextOptional.validate(input_data)
