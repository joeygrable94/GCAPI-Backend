from typing import Any
from unittest.mock import MagicMock

import pytest

from app.core.security.permissions.scope import AclPrivilege
from app.db.constants import DB_STR_LONGTEXT_MAX_LEN, DB_STR_NAME_TITLE_MAX_LEN
from app.db.validators import (
    validate_cls_unit_required,
    validate_corpus_optional,
    validate_corpus_required,
    validate_description_optional,
    validate_device_required,
    validate_domain_optional,
    validate_domain_required,
    validate_fcp_unit_required,
    validate_file_extension_optional,
    validate_file_extension_required,
    validate_lcp_unit_required,
    validate_ps_unit_required,
    validate_ps_value_optional,
    validate_ps_value_required,
    validate_rawtext_optional,
    validate_rawtext_required,
    validate_scopes_optional,
    validate_scopes_required,
    validate_si_unit_required,
    validate_strategy_required,
    validate_tbt_unit_required,
    validate_title_optional,
    validate_title_required,
    validate_url_optional,
    validate_url_required,
)


@pytest.fixture
def mock_settings() -> Any:
    return MagicMock(api=MagicMock(accepted_types=["jpg", "png"]))


def test_validate_file_extension_required(mock_settings: Any) -> None:
    assert validate_file_extension_required(cls=None, value="jpg") == "jpg"
    assert validate_file_extension_required(cls=None, value="png") == "png"
    with pytest.raises(ValueError):
        validate_file_extension_required(cls=None, value="exc")


def test_validate_file_extension_optional(mock_settings: Any) -> None:
    assert validate_file_extension_optional(cls=None, value=None) is None
    assert validate_file_extension_optional(cls=None, value="jpg") == "jpg"
    assert validate_file_extension_optional(cls=None, value="png") == "png"
    with pytest.raises(ValueError):
        validate_file_extension_optional(cls=None, value="exc")


def test_validate_title_required() -> None:
    assert validate_title_required(cls=None, value="Valid Title") == "Valid Title"
    with pytest.raises(ValueError):
        validate_title_required(cls=None, value="a")  # less than min_len
    with pytest.raises(ValueError):
        validate_title_required(
            cls=None, value="a" * (DB_STR_NAME_TITLE_MAX_LEN + 1)
        )  # more than max_len
    with pytest.raises(ValueError):
        validate_title_required(cls=None, value=None)  # type: ignore


def test_validate_title_optional() -> None:
    assert validate_title_optional(cls=None, value=None) is None
    assert validate_title_optional(cls=None, value="Valid Title") == "Valid Title"
    with pytest.raises(ValueError):
        validate_title_optional(cls=None, value="a")  # less than min_len
    with pytest.raises(ValueError):
        validate_title_optional(
            cls=None, value="a" * (DB_STR_NAME_TITLE_MAX_LEN + 1)
        )  # more than max_len


def test_validate_description_optional() -> None:
    assert validate_description_optional(cls=None, value=None) is None
    assert (
        validate_description_optional(cls=None, value="Valid Description")
        == "Valid Description"
    )
    with pytest.raises(ValueError):
        validate_description_optional(cls=None, value="a" * 5001)  # more than max_len


def test_validate_domain_required() -> None:
    assert validate_domain_required(cls=None, value="example.com") == "example.com"
    assert (
        validate_domain_required(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value="example.com/path")
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value="example")  # invalid domain
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value="example.")  # invalid domain
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value=".example.com")  # invalid domain
    with pytest.raises(ValueError):
        validate_domain_required(
            cls=None, value="example.com" + "a" * 253
        )  # domain too long
    with pytest.raises(ValueError):
        validate_domain_required(
            cls=None, value="example.com/path" + "a" * 240
        )  # value too long
    with pytest.raises(ValueError):
        validate_domain_required(cls=None, value=None)  # type: ignore


def test_validate_domain_optional() -> None:
    assert validate_domain_optional(cls=None, value=None) is None
    assert validate_domain_optional(cls=None, value="example.com") == "example.com"
    assert (
        validate_domain_optional(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        assert validate_domain_optional(cls=None, value="example.com/path")
    with pytest.raises(ValueError):
        validate_domain_optional(cls=None, value="example")  # invalid domain
    with pytest.raises(ValueError):
        validate_domain_optional(cls=None, value="example.")  # invalid domain
    with pytest.raises(ValueError):
        validate_domain_optional(cls=None, value=".example.com")  # invalid domain
    with pytest.raises(ValueError):
        validate_domain_optional(
            cls=None, value="example.com" + "a" * 253
        )  # domain too long
    with pytest.raises(ValueError):
        validate_domain_optional(
            cls=None, value="example.com/path" + "a" * 240
        )  # value too long


def test_validate_corpus_required() -> None:
    assert validate_corpus_required(cls=None, value="Valid Corpus") == "Valid Corpus"
    with pytest.raises(ValueError):
        validate_corpus_required(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len
    with pytest.raises(ValueError):
        assert validate_corpus_required(cls=None, value="") == ""


def test_validate_corpus_optional() -> None:
    assert validate_corpus_optional(cls=None, value=None) is None
    assert validate_corpus_optional(cls=None, value="Valid Corpus") == "Valid Corpus"
    with pytest.raises(ValueError):
        validate_corpus_optional(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_rawtext_required() -> None:
    assert validate_rawtext_required(cls=None, value="Valid Rawtext") == "Valid Rawtext"
    with pytest.raises(ValueError):
        validate_rawtext_required(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len
    with pytest.raises(ValueError):
        validate_rawtext_required(cls=None, value=None)  # type: ignore


def test_validate_rawtext_optional() -> None:
    assert validate_rawtext_optional(cls=None, value=None) is None
    assert validate_rawtext_optional(cls=None, value="Valid Rawtext") == "Valid Rawtext"
    with pytest.raises(ValueError):
        validate_rawtext_optional(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_url_required() -> None:
    assert (
        validate_url_required(cls=None, value="https://example.com")
        == "https://example.com"
    )
    with pytest.raises(ValueError):
        validate_url_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_url_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_url_required(
            cls=None, value="http://example.com/path" + "a" * 2049
        )  # value too long


def test_validate_url_optional() -> None:
    assert validate_url_optional(cls=None, value=None) is None
    assert (
        validate_url_optional(cls=None, value="https://example.com")
        == "https://example.com"
    )
    assert (
        validate_url_optional(cls=None, value="https://example.com/path")
        == "https://example.com/path"
    )
    assert (
        validate_url_optional(cls=None, value="https://example.com/path?query=string")
        == "https://example.com/path?query=string"
    )
    assert validate_url_optional(cls=None, value="/") == "/"
    with pytest.raises(ValueError):
        validate_url_optional(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_url_optional(
            cls=None, value="http://example.com/path" + "a" * 2049
        )  # value too long


def test_validate_device_required() -> None:
    assert validate_device_required(cls=None, value="mobile") == "mobile"
    assert validate_device_required(cls=None, value="desktop") == "desktop"
    assert validate_device_required(cls=None, value="Mobile") == "mobile"
    with pytest.raises(ValueError):
        validate_device_required(cls=None, value="laptop")
    with pytest.raises(ValueError):
        validate_device_required(cls=None, value=None)  # type: ignore


def test_validate_strategy_required() -> None:
    assert validate_strategy_required(cls=None, value="mobile") == "mobile"
    assert validate_strategy_required(cls=None, value="desktop") == "desktop"
    with pytest.raises(ValueError):
        validate_strategy_required(cls=None, value="web")  # invalid strategy
    with pytest.raises(ValueError):
        validate_strategy_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_strategy_required(cls=None, value="")  # empty string


def test_validate_ps_value_required() -> None:
    assert validate_ps_value_required(cls=None, value="1234") == "1234"
    with pytest.raises(ValueError):
        validate_ps_value_required(cls=None, value="12345")  # more than max_len
    with pytest.raises(ValueError):
        validate_ps_value_required(cls=None, value=None)  # type: ignore


def test_validate_ps_value_optional() -> None:
    assert validate_ps_value_optional(cls=None, value=None) is None
    assert validate_ps_value_optional(cls=None, value="1234") == "1234"
    assert validate_ps_value_optional(cls=None, value="1") == "1"
    with pytest.raises(ValueError):
        validate_ps_value_optional(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_ps_value_optional(cls=None, value="12345")  # too long


def test_validate_ps_unit_required() -> None:
    assert validate_ps_unit_required(cls=None, value="ValidUnit") == "ValidUnit"
    with pytest.raises(ValueError):
        validate_ps_unit_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_ps_unit_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_ps_unit_required(cls=None, value="a" * 17)  # more than max_len


def test_validate_fcp_unit_required() -> None:
    assert validate_fcp_unit_required(cls=None, value="ValidUnit") == "ValidUnit"
    with pytest.raises(ValueError):
        validate_fcp_unit_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_fcp_unit_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_fcp_unit_required(cls=None, value="a" * 17)  # more than max_len


def test_validate_lcp_unit_required() -> None:
    assert validate_lcp_unit_required(cls=None, value="ValidUnit") == "ValidUnit"
    with pytest.raises(ValueError):
        validate_lcp_unit_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_lcp_unit_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_lcp_unit_required(cls=None, value="a" * 17)  # more than max_len


def test_validate_cls_unit_required() -> None:
    assert validate_cls_unit_required(cls=None, value="ValidClsUnit") == "ValidClsUnit"
    with pytest.raises(ValueError):
        validate_cls_unit_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_cls_unit_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_cls_unit_required(cls=None, value="a" * 17)  # value too long


def test_validate_si_unit_required() -> None:
    assert validate_si_unit_required(cls=None, value="ValidUnit") == "ValidUnit"
    with pytest.raises(ValueError):
        validate_si_unit_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_si_unit_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_si_unit_required(cls=None, value="a" * 17)  # more than max_len


def test_validate_tbt_unit_required() -> None:
    assert validate_tbt_unit_required(cls=None, value="ValidUnit") == "ValidUnit"
    with pytest.raises(ValueError):
        validate_tbt_unit_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_tbt_unit_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_tbt_unit_required(cls=None, value="a" * 17)  # more than max_len


def test_validate_scopes_required() -> None:
    assert validate_scopes_required(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    assert validate_scopes_required(
        cls=None, value=[AclPrivilege("read:test"), AclPrivilege("write:test")]
    ) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    with pytest.raises(ValueError):
        validate_scopes_required(
            cls=None, value=["read", "write", "execute"]
        )  # invalid scope
    with pytest.raises(ValueError):
        validate_scopes_required(cls=None, value=None)  # type: ignore


def test_validate_scopes_optional() -> None:
    assert validate_scopes_optional(cls=None, value=None) is None
    assert validate_scopes_optional(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    assert validate_scopes_optional(
        cls=None, value=[AclPrivilege("read:test"), AclPrivilege("write:test")]
    ) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    with pytest.raises(ValueError):
        assert validate_scopes_optional(cls=None, value=["read", "write"])
    with pytest.raises(ValueError):
        assert validate_scopes_optional(cls=None, value=["read", AclPrivilege("write")])
