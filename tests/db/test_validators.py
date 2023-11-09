from typing import Any
from unittest.mock import MagicMock

import pytest

from app.core.config import settings
from app.core.security.permissions.scope import AclPrivilege
from app.db.constants import DB_INT_INTEGER_MAX_LEN
from app.db.constants import DB_STR_BLOB_MAX_LEN
from app.db.constants import DB_STR_LONGTEXT_MAX_LEN
from app.db.constants import DB_STR_NAME_TITLE_MAX_LEN
from app.db.constants import DB_STR_TINYTEXT_MAX_LEN
from app.db.constants import DB_STR_URL_PATH_MAX_LEN
from app.db.validators import validate_active_seconds_required
from app.db.validators import validate_address_optional
from app.db.validators import validate_address_required
from app.db.validators import validate_altitude_optional
from app.db.validators import validate_altitude_required
from app.db.validators import validate_api_key_optional
from app.db.validators import validate_api_key_required
from app.db.validators import validate_auth_id_required
from app.db.validators import validate_bg_color_optional
from app.db.validators import validate_browser_optional
from app.db.validators import validate_browser_version_optional
from app.db.validators import validate_bucket_name_optional
from app.db.validators import validate_bucket_name_required
from app.db.validators import validate_caption_optional
from app.db.validators import validate_city_optional
from app.db.validators import validate_clicks_required
from app.db.validators import validate_cls_unit_required
from app.db.validators import validate_corpus_optional
from app.db.validators import validate_corpus_required
from app.db.validators import validate_country_optional
from app.db.validators import validate_description_optional
from app.db.validators import validate_device_required
from app.db.validators import validate_domain_optional
from app.db.validators import validate_domain_required
from app.db.validators import validate_email_required
from app.db.validators import validate_fcp_unit_required
from app.db.validators import validate_file_extension_optional
from app.db.validators import validate_file_extension_required
from app.db.validators import validate_filename_optional
from app.db.validators import validate_filename_required
from app.db.validators import validate_group_name_optional
from app.db.validators import validate_group_name_required
from app.db.validators import validate_group_slug_required
from app.db.validators import validate_hotspot_content_optional
from app.db.validators import validate_hotspot_icon_name_optional
from app.db.validators import validate_hotspot_name_optional
from app.db.validators import validate_hotspot_type_name_optional
from app.db.validators import validate_hotspot_user_icon_name_optional
from app.db.validators import validate_icon_color_optional
from app.db.validators import validate_impressions_required
from app.db.validators import validate_ip_location_optional
from app.db.validators import validate_ip_location_required
from app.db.validators import validate_ip_optional
from app.db.validators import validate_ip_required
from app.db.validators import validate_isp_optional
from app.db.validators import validate_isp_required
from app.db.validators import validate_keys_optional
from app.db.validators import validate_keys_required
from app.db.validators import validate_language_optional
from app.db.validators import validate_lcp_unit_required
from app.db.validators import validate_linked_snap_name_optional
from app.db.validators import validate_measurement_id_required
from app.db.validators import validate_object_key_optional
from app.db.validators import validate_object_key_required
from app.db.validators import validate_password_optional
from app.db.validators import validate_password_required
from app.db.validators import validate_platform_optional
from app.db.validators import validate_platform_version_optional
from app.db.validators import validate_project_id_optional
from app.db.validators import validate_project_id_required
from app.db.validators import validate_project_name_optional
from app.db.validators import validate_project_name_required
from app.db.validators import validate_project_number_optional
from app.db.validators import validate_project_number_required
from app.db.validators import validate_property_id_required
from app.db.validators import validate_ps_unit_required
from app.db.validators import validate_ps_value_optional
from app.db.validators import validate_ps_value_required
from app.db.validators import validate_rawtext_optional
from app.db.validators import validate_rawtext_required
from app.db.validators import validate_referrer_required
from app.db.validators import validate_reporting_id_required
from app.db.validators import validate_scopes_optional
from app.db.validators import validate_scopes_required
from app.db.validators import validate_secret_key_optional
from app.db.validators import validate_secret_key_required
from app.db.validators import validate_serverhost_optional
from app.db.validators import validate_serverhost_required
from app.db.validators import validate_service_account_optional
from app.db.validators import validate_service_account_required
from app.db.validators import validate_si_unit_required
from app.db.validators import validate_size_kb_optional
from app.db.validators import validate_size_kb_required
from app.db.validators import validate_snap_file_name_optional
from app.db.validators import validate_snap_name_optional
from app.db.validators import validate_snap_name_required
from app.db.validators import validate_snap_slug_required
from app.db.validators import validate_state_optional
from app.db.validators import validate_strategy_required
from app.db.validators import validate_stream_id_required
from app.db.validators import validate_tbt_unit_required
from app.db.validators import validate_text_color_optional
from app.db.validators import validate_title_optional
from app.db.validators import validate_title_required
from app.db.validators import validate_tracking_id_required
from app.db.validators import validate_url_optional
from app.db.validators import validate_url_required
from app.db.validators import validate_username_optional
from app.db.validators import validate_username_required
from app.db.validators import validate_utm_campaign_optional
from app.db.validators import validate_utm_content_optional
from app.db.validators import validate_utm_medium_optional
from app.db.validators import validate_utm_source_optional
from app.db.validators import validate_utm_term_optional
from app.db.validators import validate_view_id_required


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
        assert validate_corpus_required(cls=None, value="")


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
    assert validate_scopes_required(cls=None, value=["read:test", "write:test"]) == [
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
    assert validate_scopes_optional(cls=None, value=["read:test", "write:test"]) == [
        AclPrivilege("read:test"),
        AclPrivilege("write:test"),
    ]
    with pytest.raises(ValueError):
        assert validate_scopes_optional(cls=None, value=["read", "write"])
    with pytest.raises(ValueError):
        assert validate_scopes_optional(cls=None, value=["read", AclPrivilege("write")])


def test_validate_auth_id_required() -> None:
    assert validate_auth_id_required(cls=None, value="valid_auth_id") == "valid_auth_id"
    assert validate_auth_id_required(cls=None, value="a" * 255) == "a" * 255
    with pytest.raises(ValueError):
        assert validate_auth_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_auth_id_required(cls=None, value="a" * 256)


def test_validate_email_required() -> None:
    assert (
        validate_email_required(cls=None, value="test@example.com")
        == "test@example.com"
    )
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value="a")  # less than min_len
    with pytest.raises(ValueError):
        validate_email_required(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_email_required(cls=None, value="notanemail")  # invalid email format


def test_validate_username_required() -> None:
    assert (
        validate_username_required(cls=None, value="ValidUsername") == "ValidUsername"
    )
    with pytest.raises(ValueError):
        assert validate_username_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_username_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_username_required(cls=None, value="a" * 256)  # more than max_len


def test_validate_password_required() -> None:
    assert validate_password_required(cls=None, value="password") == "password"
    with pytest.raises(ValueError):
        assert validate_password_required(cls=None, value="")
    assert validate_password_required(cls=None, value="a" * 255) == "a" * 255
    with pytest.raises(ValueError):
        validate_password_required(cls=None, value="a" * 256)  # more than max_len


def test_validate_username_optional() -> None:
    assert validate_username_optional(cls=None, value=None) is None
    assert (
        validate_username_optional(cls=None, value="valid_username") == "valid_username"
    )
    with pytest.raises(ValueError):
        validate_username_optional(cls=None, value="a")  # less than min_len
    with pytest.raises(ValueError):
        validate_username_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_password_optional() -> None:
    assert validate_password_optional(cls=None, value=None) is None
    assert validate_password_optional(cls=None, value="12345") == "12345"
    assert validate_password_optional(cls=None, value="a" * 255) == "a" * 255
    with pytest.raises(ValueError):
        validate_password_optional(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_password_optional(cls=None, value="1234")  # less than min_len
    with pytest.raises(ValueError):
        validate_password_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_api_key_required() -> None:
    assert validate_api_key_required(cls=None, value="valid_api_key") == "valid_api_key"
    assert validate_api_key_required(cls=None, value="a" * 64) == "a" * 64
    with pytest.raises(ValueError):
        assert validate_api_key_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_api_key_required(cls=None, value="a" * 65)  # more than max_len


def test_validate_secret_key_required() -> None:
    assert (
        validate_secret_key_required(cls=None, value="valid_secret_key")
        == "valid_secret_key"
    )
    assert validate_secret_key_required(cls=None, value="a" * 64) == "a" * 64
    with pytest.raises(ValueError):
        assert validate_secret_key_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_secret_key_required(cls=None, value="a" * 65)  # more than max_len


def test_validate_api_key_optional() -> None:
    assert validate_api_key_optional(cls=None, value="valid_api_key") == "valid_api_key"
    assert validate_api_key_optional(cls=None, value="a" * 64) == "a" * 64
    assert validate_api_key_optional(cls=None, value=None) is None
    with pytest.raises(ValueError):
        assert validate_api_key_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_api_key_optional(cls=None, value="a" * 65)  # more than max_len


def test_validate_secret_key_optional() -> None:
    assert validate_secret_key_optional(cls=None, value="a" * 64) == "a" * 64
    assert validate_secret_key_optional(cls=None, value=None) is None
    with pytest.raises(ValueError):
        assert validate_secret_key_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_secret_key_optional(cls=None, value="a" * 65)  # more than max_len


def test_validate_serverhost_required() -> None:
    assert validate_serverhost_required(cls=None, value="example.com") == "example.com"
    assert (
        validate_serverhost_required(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        assert validate_serverhost_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_serverhost_required(cls=None, value="a" * 256)  # more than max_len


def test_validate_serverhost_optional() -> None:
    assert validate_serverhost_optional(cls=None, value=None) is None
    assert validate_serverhost_optional(cls=None, value="example.com") == "example.com"
    assert (
        validate_serverhost_optional(cls=None, value="subdomain.example.com")
        == "subdomain.example.com"
    )
    with pytest.raises(ValueError):
        validate_serverhost_optional(cls=None, value="a")  # less than min_len
    with pytest.raises(ValueError):
        validate_serverhost_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_keys_optional() -> None:
    assert validate_keys_optional(cls=None, value=None) is None
    assert validate_keys_optional(cls=None, value="valid keys") == "valid keys"
    assert validate_keys_optional(cls=None, value="a" * 65500) == "a" * 65500
    with pytest.raises(ValueError):
        assert validate_keys_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_keys_optional(cls=None, value="a" * 65501)  # more than max_len


def test_validate_object_key_required() -> None:
    assert validate_object_key_required(cls=None, value="valid_key") == "valid_key"
    with pytest.raises(ValueError):
        validate_object_key_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_object_key_required(
            cls=None, value="a" * (DB_STR_URL_PATH_MAX_LEN + 1)
        )  # more than max_len


def test_validate_object_key_optional() -> None:
    assert validate_object_key_optional(cls=None, value=None) is None
    assert validate_object_key_optional(cls=None, value="valid_key") == "valid_key"
    with pytest.raises(ValueError):
        validate_object_key_optional(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_object_key_optional(
            cls=None, value="a" * (DB_STR_URL_PATH_MAX_LEN + 1)
        )  # more than max_len


def test_validate_bucket_name_required() -> None:
    assert (
        validate_bucket_name_required(cls=None, value="valid_bucket_name")
        == "valid_bucket_name"
    )
    with pytest.raises(ValueError):
        validate_bucket_name_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_bucket_name_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_bucket_name_required(cls=None, value="a" * 101)  # more than max_len


def test_validate_bucket_name_optional() -> None:
    assert validate_bucket_name_optional(cls=None, value=None) is None
    assert (
        validate_bucket_name_optional(cls=None, value="valid_bucket_name")
        == "valid_bucket_name"
    )
    with pytest.raises(ValueError):
        validate_bucket_name_optional(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_bucket_name_optional(cls=None, value="a" * 101)  # more than max_len


def test_validate_caption_optional() -> None:
    assert validate_caption_optional(cls=None, value=None) is None
    assert validate_caption_optional(cls=None, value="Valid Caption") == "Valid Caption"
    with pytest.raises(ValueError):
        validate_caption_optional(cls=None, value="a" * 151)  # more than max_len


def test_validate_filename_required() -> None:
    assert validate_filename_required(cls=None, value="ValidName") == "ValidName"
    with pytest.raises(ValueError):
        assert validate_filename_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_filename_required(
            cls=None, value="a" * (DB_STR_NAME_TITLE_MAX_LEN + 1)
        )


def test_validate_filename_optional() -> None:
    assert validate_filename_optional(cls=None, value=None) is None
    assert validate_filename_optional(cls=None, value="ValidName") == "ValidName"
    with pytest.raises(ValueError):
        validate_filename_optional(cls=None, value="a")  # less than min_len
    with pytest.raises(ValueError):
        validate_filename_optional(
            cls=None, value="a" * (DB_STR_NAME_TITLE_MAX_LEN + 1)
        )  # more than max_len


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
        validate_size_kb_optional(cls=None, value=-1)  # less than min_len
    with pytest.raises(ValueError):
        validate_size_kb_optional(
            cls=None, value=settings.api.payload_limit_kb + 1
        )  # more than max_len


def test_validate_address_required() -> None:
    assert validate_address_required(cls=None, value="Valid Address") == "Valid Address"
    with pytest.raises(ValueError):
        assert validate_address_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_address_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len
    with pytest.raises(ValueError):
        validate_address_required(cls=None, value=None)  # type: ignore


def test_validate_address_optional() -> None:
    assert validate_address_optional(cls=None, value=None) is None
    assert validate_address_optional(cls=None, value="Valid Address") == "Valid Address"
    with pytest.raises(ValueError):
        validate_address_optional(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_ip_required() -> None:
    assert validate_ip_required(cls=None, value="192.168.0.1") == "192.168.0.1"
    assert validate_ip_required(cls=None, value="::1") == "::1"
    assert (
        validate_ip_required(cls=None, value="2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    with pytest.raises(ValueError):
        validate_ip_required(cls=None, value="")  # invalid IP address
    with pytest.raises(ValueError):
        validate_ip_required(cls=None, value=None)  # type: ignore


def test_validate_ip_optional() -> None:
    assert validate_ip_optional(cls=None, value=None) is None
    assert validate_ip_optional(cls=None, value="192.168.0.1") == "192.168.0.1"
    assert (
        validate_ip_optional(cls=None, value="2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        == "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    )
    with pytest.raises(ValueError):
        validate_ip_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_ip_optional(cls=None, value="a" * 41)  # more than max_len


def test_validate_isp_required() -> None:
    assert validate_isp_required(cls=None, value="Valid ISP") == "Valid ISP"
    with pytest.raises(ValueError):
        validate_isp_required(cls=None, value="a" * 256)  # more than max_len
    with pytest.raises(ValueError):
        assert validate_isp_required(cls=None, value="")


def test_validate_isp_optional() -> None:
    assert validate_isp_optional(cls=None, value=None) is None
    assert validate_isp_optional(cls=None, value="Valid ISP") == "Valid ISP"
    with pytest.raises(ValueError):
        validate_isp_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_ip_location_required() -> None:
    assert (
        validate_ip_location_required(cls=None, value="Valid Location")
        == "Valid Location"
    )
    with pytest.raises(ValueError):
        validate_ip_location_required(cls=None, value="a" * 256)  # more than max_len
    with pytest.raises(ValueError):
        assert validate_ip_location_required(cls=None, value="")


def test_validate_ip_location_optional() -> None:
    assert validate_ip_location_optional(cls=None, value=None) is None
    assert (
        validate_ip_location_optional(cls=None, value="Valid Location")
        == "Valid Location"
    )
    with pytest.raises(ValueError):
        validate_ip_location_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_group_name_required() -> None:
    assert (
        validate_group_name_required(cls=None, value="Valid Group Name")
        == "Valid Group Name"
    )
    with pytest.raises(ValueError):
        validate_group_name_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_group_name_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_group_name_required(cls=None, value="a" * 256)  # more than max_len


def test_validate_group_name_optional() -> None:
    assert validate_group_name_optional(cls=None, value=None) is None
    assert (
        validate_group_name_optional(cls=None, value="Valid Group Name")
        == "Valid Group Name"
    )
    with pytest.raises(ValueError):
        validate_group_name_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_group_slug_required() -> None:
    assert validate_group_slug_required(cls=None, value="valid_slug") == "valid_slug"
    assert validate_group_slug_required(cls=None, value="a" * 12) == "a" * 12
    with pytest.raises(ValueError):
        assert validate_group_slug_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_group_slug_required(cls=None, value="a" * 13)  # more than max_len


def test_validate_snap_name_required() -> None:
    assert (
        validate_snap_name_required(cls=None, value="Valid Snap Name")
        == "Valid Snap Name"
    )
    with pytest.raises(ValueError):
        validate_snap_name_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_snap_name_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_snap_name_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_snap_name_optional() -> None:
    assert validate_snap_name_optional(cls=None, value=None) is None
    assert (
        validate_snap_name_optional(cls=None, value="Valid Snap Name")
        == "Valid Snap Name"
    )
    with pytest.raises(ValueError):
        assert validate_snap_name_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_snap_name_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_snap_slug_required() -> None:
    assert validate_snap_slug_required(cls=None, value="validslug") == "validslug"
    assert validate_snap_slug_required(cls=None, value="123456789012") == "123456789012"
    with pytest.raises(ValueError):
        assert validate_snap_slug_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_snap_slug_required(cls=None, value="toolongslug1234")


def test_validate_altitude_required() -> None:
    assert validate_altitude_required(cls=None, value=0) == 0
    assert validate_altitude_required(cls=None, value=500) == 500
    assert validate_altitude_required(cls=None, value=1000) == 1000
    with pytest.raises(ValueError):
        assert validate_altitude_required(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_altitude_required(cls=None, value=-1)  # less than min_len
    with pytest.raises(ValueError):
        validate_altitude_required(cls=None, value=1001)  # more than max_len


def test_validate_altitude_optional() -> None:
    assert validate_altitude_optional(cls=None, value=None) is None
    assert validate_altitude_optional(cls=None, value=0) == 0
    assert validate_altitude_optional(cls=None, value=500) == 500
    assert validate_altitude_optional(cls=None, value=1000) == 1000
    with pytest.raises(ValueError):
        assert validate_altitude_optional(cls=None, value=-1)
    with pytest.raises(ValueError):
        validate_altitude_optional(cls=None, value=-1)  # less than min_len
    with pytest.raises(ValueError):
        validate_altitude_optional(cls=None, value=1001)  # more than max_len


def test_validate_referrer_required() -> None:
    assert (
        validate_referrer_required(cls=None, value="https://example.com")
        == "https://example.com"
    )
    assert (
        validate_referrer_required(cls=None, value="https://example.com/path")
        == "https://example.com/path"
    )
    assert validate_referrer_required(cls=None, value="/") == "/"
    with pytest.raises(ValueError):
        validate_referrer_required(
            cls=None, value="http://example.com/path" + "a" * 2049
        )  # value too long
    with pytest.raises(ValueError):
        validate_referrer_required(cls=None, value=None)  # type: ignore


def test_validate_utm_campaign_optional() -> None:
    assert validate_utm_campaign_optional(cls=None, value=None) is None
    assert (
        validate_utm_campaign_optional(cls=None, value="Valid UTM Campaign")
        == "Valid UTM Campaign"
    )
    with pytest.raises(ValueError):
        validate_utm_campaign_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_utm_content_optional() -> None:
    assert validate_utm_content_optional(cls=None, value=None) is None
    assert (
        validate_utm_content_optional(cls=None, value="Valid UTM Content")
        == "Valid UTM Content"
    )
    with pytest.raises(ValueError):
        validate_utm_content_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_utm_medium_optional() -> None:
    assert validate_utm_medium_optional(cls=None, value=None) is None
    assert (
        validate_utm_medium_optional(cls=None, value="Valid UTM Medium")
        == "Valid UTM Medium"
    )
    with pytest.raises(ValueError):
        assert validate_utm_medium_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_utm_medium_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_utm_source_optional() -> None:
    assert validate_utm_source_optional(cls=None, value=None) is None
    assert (
        validate_utm_source_optional(cls=None, value="Valid UTM Source")
        == "Valid UTM Source"
    )
    with pytest.raises(ValueError):
        validate_utm_source_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_utm_term_optional() -> None:
    assert validate_utm_term_optional(cls=None, value=None) is None
    assert (
        validate_utm_term_optional(cls=None, value="Valid UTM Term") == "Valid UTM Term"
    )
    with pytest.raises(ValueError):
        validate_utm_term_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_reporting_id_required() -> None:
    assert (
        validate_reporting_id_required(cls=None, value="valid_reporting_id")
        == "valid_reporting_id"
    )
    with pytest.raises(ValueError):
        validate_reporting_id_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_reporting_id_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_reporting_id_required(cls=None, value="a" * 33)  # more than max_len


def test_validate_hotspot_type_name_optional() -> None:
    assert validate_hotspot_type_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_type_name_optional(cls=None, value="Valid Name")
        == "Valid Name"
    )
    assert validate_hotspot_type_name_optional(cls=None, value="a" * 32) == "a" * 32
    with pytest.raises(ValueError):
        validate_hotspot_type_name_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_hotspot_type_name_optional(cls=None, value="a" * 33)  # too long


def test_validate_hotspot_content_optional() -> None:
    assert validate_hotspot_content_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_content_optional(cls=None, value="Valid hotspot content")
        == "Valid hotspot content"
    )
    with pytest.raises(ValueError):
        validate_hotspot_content_optional(
            cls=None, value="a" * (DB_STR_BLOB_MAX_LEN + 1)
        )  # more than max_len


def test_validate_hotspot_icon_name_optional() -> None:
    assert validate_hotspot_icon_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_icon_name_optional(cls=None, value="Valid Icon Name")
        == "Valid Icon Name"
    )
    with pytest.raises(ValueError):
        validate_hotspot_icon_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_hotspot_name_optional() -> None:
    assert validate_hotspot_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_name_optional(cls=None, value="Valid Hotspot Name")
        == "Valid Hotspot Name"
    )
    with pytest.raises(ValueError):
        validate_hotspot_name_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_hotspot_user_icon_name_optional() -> None:
    assert validate_hotspot_user_icon_name_optional(cls=None, value=None) is None
    assert (
        validate_hotspot_user_icon_name_optional(
            cls=None, value="Valid Hotspot User Icon Name"
        )
        == "Valid Hotspot User Icon Name"
    )
    with pytest.raises(ValueError):
        validate_hotspot_user_icon_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_linked_snap_name_optional() -> None:
    assert validate_linked_snap_name_optional(cls=None, value=None) is None
    assert (
        validate_linked_snap_name_optional(cls=None, value="Valid Linked Snap Name")
        == "Valid Linked Snap Name"
    )
    with pytest.raises(ValueError):
        validate_linked_snap_name_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_snap_file_name_optional() -> None:
    assert validate_snap_file_name_optional(cls=None, value=None) is None
    assert (
        validate_snap_file_name_optional(cls=None, value="valid_file_name.jpg")
        == "valid_file_name.jpg"
    )
    with pytest.raises(ValueError):
        validate_snap_file_name_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_icon_color_optional() -> None:
    assert validate_icon_color_optional(cls=None, value=None) is None
    assert validate_icon_color_optional(cls=None, value="red") == "red"
    assert validate_icon_color_optional(cls=None, value="green") == "green"
    assert validate_icon_color_optional(cls=None, value="blue") == "blue"
    with pytest.raises(ValueError):
        validate_icon_color_optional(cls=None, value="a" * 33)  # more than max_len


def test_validate_bg_color_optional() -> None:
    assert validate_bg_color_optional(cls=None, value=None) is None
    assert validate_bg_color_optional(cls=None, value="") == ""
    assert validate_bg_color_optional(cls=None, value="red") == "red"
    assert validate_bg_color_optional(cls=None, value="green") == "green"
    assert validate_bg_color_optional(cls=None, value="blue") == "blue"
    assert validate_bg_color_optional(cls=None, value="yellow") == "yellow"
    assert validate_bg_color_optional(cls=None, value="purple") == "purple"
    assert validate_bg_color_optional(cls=None, value="orange") == "orange"
    assert validate_bg_color_optional(cls=None, value="black") == "black"
    assert validate_bg_color_optional(cls=None, value="white") == "white"
    assert validate_bg_color_optional(cls=None, value="gray") == "gray"
    assert validate_bg_color_optional(cls=None, value="grey") == "grey"
    assert validate_bg_color_optional(cls=None, value="pink") == "pink"
    assert validate_bg_color_optional(cls=None, value="brown") == "brown"
    assert validate_bg_color_optional(cls=None, value="cyan") == "cyan"
    assert validate_bg_color_optional(cls=None, value="magenta") == "magenta"
    assert validate_bg_color_optional(cls=None, value="teal") == "teal"
    assert validate_bg_color_optional(cls=None, value="navy") == "navy"
    assert validate_bg_color_optional(cls=None, value="maroon") == "maroon"
    assert validate_bg_color_optional(cls=None, value="olive") == "olive"
    assert validate_bg_color_optional(cls=None, value="silver") == "silver"
    assert validate_bg_color_optional(cls=None, value="lime") == "lime"
    assert validate_bg_color_optional(cls=None, value="aqua") == "aqua"
    assert validate_bg_color_optional(cls=None, value="fuchsia") == "fuchsia"
    with pytest.raises(ValueError):
        validate_bg_color_optional(cls=None, value="red" * 11)  # more than max_len


def test_validate_text_color_optional() -> None:
    assert validate_text_color_optional(cls=None, value=None) is None
    assert validate_text_color_optional(cls=None, value="red") == "red"
    assert validate_text_color_optional(cls=None, value="green") == "green"
    assert validate_text_color_optional(cls=None, value="blue") == "blue"
    assert validate_text_color_optional(cls=None, value="black") == "black"
    assert validate_text_color_optional(cls=None, value="white") == "white"
    assert validate_text_color_optional(cls=None, value="yellow") == "yellow"
    assert validate_text_color_optional(cls=None, value="purple") == "purple"
    assert validate_text_color_optional(cls=None, value="orange") == "orange"
    assert validate_text_color_optional(cls=None, value="pink") == "pink"
    assert validate_text_color_optional(cls=None, value="brown") == "brown"
    assert validate_text_color_optional(cls=None, value="gray") == "gray"
    assert validate_text_color_optional(cls=None, value="grey") == "grey"
    assert validate_text_color_optional(cls=None, value="") == ""
    with pytest.raises(ValueError):
        validate_text_color_optional(cls=None, value="a" * 33)  # more than max_len


def test_validate_browser_optional() -> None:
    assert validate_browser_optional(cls=None, value=None) is None
    assert validate_browser_optional(cls=None, value="Valid Browser") == "Valid Browser"
    with pytest.raises(ValueError):
        validate_browser_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_browser_version_optional() -> None:
    assert validate_browser_version_optional(cls=None, value=None) is None
    assert (
        validate_browser_version_optional(cls=None, value="Valid Browser Version")
        == "Valid Browser Version"
    )
    with pytest.raises(ValueError):
        validate_browser_version_optional(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_platform_optional() -> None:
    assert validate_platform_optional(cls=None, value=None) is None
    assert (
        validate_platform_optional(cls=None, value="Valid Platform") == "Valid Platform"
    )
    assert validate_platform_optional(cls=None, value="") == ""
    with pytest.raises(ValueError):
        validate_platform_optional(
            cls=None, value="a" * (DB_STR_LONGTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_platform_version_optional() -> None:
    assert validate_platform_version_optional(cls=None, value=None) is None
    assert validate_platform_version_optional(cls=None, value="") == ""
    assert (
        validate_platform_version_optional(cls=None, value="Valid Platform Version")
        == "Valid Platform Version"
    )
    with pytest.raises(ValueError):
        validate_platform_version_optional(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_city_optional() -> None:
    assert validate_city_optional(cls=None, value=None) is None
    assert validate_city_optional(cls=None, value="New York") == "New York"
    assert validate_city_optional(cls=None, value="San Francisco") == "San Francisco"
    assert validate_city_optional(cls=None, value="Los Angeles") == "Los Angeles"
    with pytest.raises(ValueError):
        validate_city_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_country_optional() -> None:
    assert validate_country_optional(cls=None, value=None) is None
    assert validate_country_optional(cls=None, value="") == ""
    assert validate_country_optional(cls=None, value="United States") == "United States"
    assert validate_country_optional(cls=None, value="Canada") == "Canada"
    with pytest.raises(ValueError):
        validate_country_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_state_optional() -> None:
    assert validate_state_optional(cls=None, value=None) is None
    assert validate_state_optional(cls=None, value="") == ""
    assert validate_state_optional(cls=None, value="Valid State") == "Valid State"
    with pytest.raises(ValueError):
        validate_state_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_language_optional() -> None:
    assert validate_language_optional(cls=None, value=None) is None
    assert validate_language_optional(cls=None, value="") == ""
    assert validate_language_optional(cls=None, value="English") == "English"
    assert validate_language_optional(cls=None, value="French") == "French"
    assert validate_language_optional(cls=None, value="Spanish") == "Spanish"
    with pytest.raises(ValueError):
        validate_language_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_active_seconds_required() -> None:
    assert validate_active_seconds_required(cls=None, value=0) == 0
    assert validate_active_seconds_required(cls=None, value=86400) == 86400
    assert validate_active_seconds_required(cls=None, value=60) == 60
    with pytest.raises(ValueError):
        validate_active_seconds_required(cls=None, value=-1)  # less than min_len
    with pytest.raises(ValueError):
        validate_active_seconds_required(cls=None, value=86401)  # more than max_len


def test_validate_project_name_required() -> None:
    assert (
        validate_project_name_required(cls=None, value="Valid Project Name")
        == "Valid Project Name"
    )
    with pytest.raises(ValueError):
        validate_project_name_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_project_name_required(
            cls=None, value="a" * (DB_STR_TINYTEXT_MAX_LEN + 1)
        )  # more than max_len


def test_validate_project_name_optional() -> None:
    assert validate_project_name_optional(cls=None, value=None) is None
    assert (
        validate_project_name_optional(cls=None, value="Valid Project Name")
        == "Valid Project Name"
    )
    with pytest.raises(ValueError):
        assert validate_project_name_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_project_name_optional(cls=None, value="a" * 256)  # more than max_len


def test_validate_project_id_required() -> None:
    assert (
        validate_project_id_required(cls=None, value="valid_project_id")
        == "valid_project_id"
    )
    with pytest.raises(ValueError):
        validate_project_id_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_project_id_required(cls=None, value="a" * 65)  # value too long


def test_validate_project_number_required() -> None:
    assert (
        validate_project_number_required(cls=None, value="valid_project_number")
        == "valid_project_number"
    )
    with pytest.raises(ValueError):
        validate_project_number_required(cls=None, value="")  # empty string
    with pytest.raises(ValueError):
        validate_project_number_required(cls=None, value=None)  # type: ignore
    with pytest.raises(ValueError):
        validate_project_number_required(cls=None, value="a" * 65)  # more than max_len


def test_validate_service_account_required() -> None:
    assert (
        validate_service_account_required(cls=None, value="valid_service_account")
        == "valid_service_account"
    )
    assert validate_service_account_required(cls=None, value="a" * 64) == "a" * 64
    with pytest.raises(ValueError):
        assert validate_service_account_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_service_account_required(cls=None, value="a" * 65)


def test_validate_project_id_optional() -> None:
    assert validate_project_id_optional(cls=None, value=None) is None
    assert validate_project_id_optional(cls=None, value="a" * 64) == "a" * 64
    with pytest.raises(ValueError):
        assert validate_project_id_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_project_id_optional(cls=None, value="a" * 65)  # more than max_len


def test_validate_project_number_optional() -> None:
    assert validate_project_number_optional(cls=None, value=None) is None
    assert validate_project_number_optional(cls=None, value="1234") == "1234"
    assert validate_project_number_optional(cls=None, value="a" * 64) == "a" * 64
    with pytest.raises(ValueError):
        assert validate_project_number_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_project_number_optional(cls=None, value="a" * 65)  # more than max_len


def test_validate_service_account_optional() -> None:
    assert validate_service_account_optional(cls=None, value=None) is None
    assert (
        validate_service_account_optional(cls=None, value="valid_service_account")
        == "valid_service_account"
    )
    with pytest.raises(ValueError):
        assert validate_service_account_optional(cls=None, value="")
    with pytest.raises(ValueError):
        validate_service_account_optional(cls=None, value="a" * 65)  # more than max_len


def test_validate_measurement_id_required() -> None:
    assert validate_measurement_id_required(cls=None, value="valid_id") == "valid_id"
    assert validate_measurement_id_required(cls=None, value="0") == "0"
    assert validate_measurement_id_required(cls=None, value="a" * 16) == "a" * 16
    with pytest.raises(ValueError):
        assert validate_measurement_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_measurement_id_required(cls=None, value="a" * 17)


def test_validate_property_id_required() -> None:
    assert validate_property_id_required(cls=None, value="valid_id") == "valid_id"
    assert validate_property_id_required(cls=None, value="0") == "0"
    assert validate_property_id_required(cls=None, value="a" * 16) == "a" * 16
    with pytest.raises(ValueError):
        assert validate_property_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_property_id_required(cls=None, value="a" * 17)


def test_validate_stream_id_required() -> None:
    assert validate_stream_id_required(cls=None, value="valid_id") == "valid_id"
    assert validate_stream_id_required(cls=None, value="0") == "0"
    assert validate_stream_id_required(cls=None, value="a" * 16) == "a" * 16
    with pytest.raises(ValueError):
        assert validate_stream_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_stream_id_required(cls=None, value="a" * 17)


def test_validate_keys_required() -> None:
    assert validate_keys_required(cls=None, value="Valid Keys") == "Valid Keys"
    with pytest.raises(ValueError):
        assert validate_keys_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_keys_required(
            cls=None, value="a" * (DB_STR_BLOB_MAX_LEN + 1)
        )  # more than max_len


def test_validate_clicks_required() -> None:
    assert validate_clicks_required(cls=None, value=0) == 0
    assert (
        validate_clicks_required(cls=None, value=DB_INT_INTEGER_MAX_LEN)
        == DB_INT_INTEGER_MAX_LEN
    )
    with pytest.raises(ValueError):
        validate_clicks_required(cls=None, value=-1)  # less than min_len
    with pytest.raises(ValueError):
        validate_clicks_required(
            cls=None, value=DB_INT_INTEGER_MAX_LEN + 1
        )  # more than max_len


def test_validate_impressions_required() -> None:
    assert validate_impressions_required(cls=None, value=0) == 0
    assert validate_impressions_required(cls=None, value=1) == 1
    assert (
        validate_impressions_required(cls=None, value=DB_INT_INTEGER_MAX_LEN)
        == DB_INT_INTEGER_MAX_LEN
    )
    with pytest.raises(ValueError):
        validate_impressions_required(cls=None, value=-1)  # less than min_len
    with pytest.raises(ValueError):
        validate_impressions_required(
            cls=None, value=DB_INT_INTEGER_MAX_LEN + 1
        )  # more than max_len


def test_validate_tracking_id_required() -> None:
    assert validate_tracking_id_required(cls=None, value="a") == "a"
    assert validate_tracking_id_required(cls=None, value="a" * 16) == "a" * 16
    with pytest.raises(ValueError):
        assert validate_tracking_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_tracking_id_required(cls=None, value="a" * 17)


def test_validate_view_id_required() -> None:
    assert validate_view_id_required(cls=None, value="valid_view_id") == "valid_view_id"
    assert validate_view_id_required(cls=None, value="0") == "0"
    assert validate_view_id_required(cls=None, value="1" * 16) == "1" * 16
    with pytest.raises(ValueError):
        assert validate_view_id_required(cls=None, value="")
    with pytest.raises(ValueError):
        validate_view_id_required(cls=None, value="1" * 17)
