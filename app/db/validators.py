from typing import Any, List, Union

from app.core.config import settings
from app.core.security.permissions import AclPrivilege
from app.core.utilities import domain_name_regex, email_regex
from app.db.constants import (
    DB_FLOAT_MAX_LEN,
    DB_INT_INTEGER_MAX_LEN,
    DB_STR_BLOB_MAX_LEN,
    DB_STR_LONGTEXT_MAX_LEN,
    DB_STR_NAME_TITLE_MAX_LEN,
    DB_STR_URL_PATH_MAX_LEN,
)

# validation utilities


def require_int_name_min_max_len(
    v: int,
    name: str,
    min_len: int = 0,
    max_len: int = 255,
) -> int:
    if min_len == 0 and v <= 0:
        raise ValueError(f"{name} is required")
    if v < min_len:
        raise ValueError(f"{name} must be greater than {min_len}")
    if v > max_len:
        raise ValueError(f"{name} must be less than {max_len}")
    return v


def optional_int_name_min_max_len(
    v: int | None,
    name: str,
    min_len: int | None = None,
    max_len: int = 255,
) -> int | None:
    if min_len is not None:
        if min_len == 0 and v and v <= 0:
            raise ValueError(f"{name} is required")
        if v and v < min_len:
            raise ValueError(f"{name} must be {min_len} characters or more")
    if v and v > max_len:
        raise ValueError(f"{name} must be {max_len} characters or less")
    return v


def require_float_rounded_to_max_len(
    v: float,
    max_len: int = 20,
) -> float:
    float_str = str(v).strip("0")
    excess_length = (
        max(0, len(float_str) - max_len)
        if len(float_str) > max_len
        else max(0, max_len - len(float_str))
    )
    value = round(v, excess_length)
    return value


def optional_float_rounded_to_max_len(
    v: float | None,
    max_len: int = 20,
) -> float | None:
    value: float | None = None
    if v:
        float_str = str(v).strip("0")
        excess_length = (
            max(0, len(float_str) - max_len)
            if len(float_str) > max_len
            else max(0, max_len - len(float_str))
        )
        value = round(v, excess_length)
    return value


def require_string_name_min_max_len(
    v: str,
    name: str,
    min_len: int = 0,
    max_len: int = 255,
) -> str:
    if min_len == 0 and len(v) <= 0:
        raise ValueError(f"{name} is required")
    if len(v) < min_len:
        raise ValueError(f"{name} must be {min_len} characters or more")
    if len(v) > max_len:
        raise ValueError(f"{name} must be {max_len} characters or less")
    return v


def optional_string_name_min_max_len(
    v: str | None,
    name: str,
    min_len: int | None = None,
    max_len: int = 255,
) -> str | None:
    if min_len is not None:
        if min_len == 0 and v is None:
            raise ValueError(f"{name} is required")
        if v and len(v) < min_len:
            raise ValueError(f"{name} must be {min_len} characters or more")
    if v and len(v) > max_len:
        raise ValueError(f"{name} must be {max_len} characters or less")
    return v


def require_string_domain(
    v: str,
    name: str = "domain",
    min_len: int = 5,
    max_len: int = 255,
) -> str:
    if min_len == 0 and len(v) <= 0:
        raise ValueError(f"{name} is required")
    if len(v) < min_len:
        raise ValueError(f"{name} must be {min_len} characters or more")
    if len(v) > max_len:
        raise ValueError(f"{name} must be {max_len} characters or less")
    if not domain_name_regex.search(v):
        raise ValueError(
            "invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
        )
    return v


def require_string_email(
    v: str,
    name: str = "email",
    min_len: int = 5,
    max_len: int = 255,
) -> str:
    if min_len == 0 and len(v) <= 0:
        raise ValueError(f"{name} is required")
    if len(v) < min_len:
        raise ValueError(f"{name} must be {min_len} characters or more")
    if len(v) > max_len:
        raise ValueError(f"{name} must be {max_len} characters or less")
    if not email_regex.search(v):
        raise ValueError(
            "invalid email provided, please make sure your email fits the following format: example@emaildomain.com"  # noqa: E501
        )
    return v


def optional_string_domain(
    v: str | None,
    name: str = "domain",
    min_len: int | None = 5,
    max_len: int = 255,
) -> str | None:
    if min_len is not None:
        if min_len == 0 and v is None:
            raise ValueError(f"{name} is required")
        if v and len(v) < min_len:
            raise ValueError(f"{name} must be {min_len} characters or more")
    if v and len(v) > max_len:
        raise ValueError(f"{name} must be {max_len} characters or less")
    if v and not domain_name_regex.search(v):
        raise ValueError(
            "invalid domain provided, top-level domain names and subdomains only accepted (example.com, sub.example.com)"  # noqa: E501
        )
    return v


def required_string_in_list(
    v: str, name: str = "device", choices: List[str] = []
) -> str:
    if len(v) <= 0:
        raise ValueError(f"{name} is required")
    if v.lower() not in choices:
        choices_str = ", ".join(choices)
        raise ValueError(f"{name} must be one of: {choices_str}")
    return v.lower()


def optional_string_in_list(
    v: str | None, name: str = "device", choices: List[str] = []
) -> str | None:
    if v and len(v) <= 0:
        raise ValueError(f"{name} is required")
    if v and v.lower() not in choices:
        choices_str = ", ".join(choices)
        raise ValueError(f"{name} must be one of: {choices_str}")
    if v:
        return v.lower()
    return v


# validation Schemas


def validate_file_extension_required(cls: Any, value: str) -> str:
    return required_string_in_list(
        v=value,
        name="extension",
        choices=settings.api.accepted_types,
    )


def validate_file_extension_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_in_list(
        v=value,
        name="extension",
        choices=settings.api.accepted_types,
    )


def validate_title_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="title",
        min_len=5,
        max_len=DB_STR_NAME_TITLE_MAX_LEN,
    )


def validate_title_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="title",
        min_len=5,
        max_len=DB_STR_NAME_TITLE_MAX_LEN,
    )


def validate_description_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="description",
        max_len=5000,
    )


def validate_domain_required(cls: Any, value: str) -> str:
    return require_string_domain(v=value)


def validate_domain_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_domain(v=value)


def validate_corpus_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="corpus",
        min_len=0,
        max_len=DB_STR_LONGTEXT_MAX_LEN,
    )


def validate_corpus_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="corpus",
        max_len=DB_STR_LONGTEXT_MAX_LEN,
    )


def validate_rawtext_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="rawtext",
        min_len=0,
        max_len=DB_STR_LONGTEXT_MAX_LEN,
    )


def validate_rawtext_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="rawtext",
        max_len=DB_STR_LONGTEXT_MAX_LEN,
    )


def validate_url_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="url",
        min_len=1,
        max_len=DB_STR_URL_PATH_MAX_LEN,
    )


def validate_url_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="url",
        max_len=DB_STR_URL_PATH_MAX_LEN,
    )


def validate_device_required(cls: Any, value: str) -> str:
    return required_string_in_list(
        v=value,
        name="device",
        choices=["mobile", "desktop"],
    )


def validate_strategy_required(cls: Any, value: str) -> str:
    return required_string_in_list(
        v=value,
        name="strategy",
        choices=["mobile", "desktop"],
    )


def validate_ps_value_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="ps_value",
        max_len=4,
    )


def validate_ps_value_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="ps_value",
        max_len=4,
    )


def validate_ps_unit_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(v=value, name="ps_unit", max_len=16)


def validate_fcp_unit_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(v=value, name="fcp_unit", max_len=16)


def validate_lcp_unit_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(v=value, name="lcp_unit", max_len=16)


def validate_cls_unit_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(v=value, name="cls_unit", max_len=16)


def validate_si_unit_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(v=value, name="si_unit", max_len=16)


def validate_tbt_unit_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(v=value, name="tbt_unit", max_len=16)


def validate_scopes_required(
    cls: Any, value: Union[List[str], List[AclPrivilege]]
) -> List[AclPrivilege]:
    scopes: List[AclPrivilege] = []
    for scope in value:
        if isinstance(scope, str):
            scopes.append(AclPrivilege(scope))
        else:
            scopes.append(scope)
    return scopes


def validate_scopes_optional(
    cls: Any, value: Union[List[str], List[AclPrivilege]] | None
) -> List[AclPrivilege] | None:
    if value:
        scopes: List[AclPrivilege] = []
        for scope in value:
            scopes.append(AclPrivilege(scope))
        return scopes
    return None


def validate_auth_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="auth_id",
        min_len=0,
        max_len=255,
    )


def validate_email_required(cls: Any, value: str) -> str:
    return require_string_email(
        v=value,
        name="email",
        min_len=5,
        max_len=320,
    )


def validate_username_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="username",
        min_len=0,
        max_len=255,
    )


def validate_password_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="password",
        min_len=0,
        max_len=255,
    )


def validate_username_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="username",
        max_len=255,
    )


def validate_password_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="password",
        min_len=5,
        max_len=255,
    )


def validate_api_key_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="api_key",
        min_len=0,
        max_len=64,
    )


def validate_secret_key_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="secret_key",
        min_len=0,
        max_len=64,
    )


def validate_api_key_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="api_key",
        max_len=64,
    )


def validate_secret_key_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="secret_key",
        max_len=64,
    )


def validate_serverhost_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="serverhost",
        min_len=0,
        max_len=255,
    )


def validate_serverhost_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="serverhost",
        max_len=255,
    )


def validate_keys_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="keys",
        max_len=65500,
    )


def validate_object_key_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="object_key",
        min_len=1,
        max_len=DB_STR_URL_PATH_MAX_LEN,
    )


def validate_object_key_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="object_key",
        max_len=DB_STR_URL_PATH_MAX_LEN,
    )


def validate_bucket_name_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="bucket_name",
        min_len=0,
        max_len=100,
    )


def validate_bucket_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="bucket_name",
        max_len=100,
    )


def validate_caption_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="caption",
        max_len=150,
    )


def validate_filename_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="name",
        min_len=0,
        max_len=DB_STR_NAME_TITLE_MAX_LEN,
    )


def validate_filename_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="name",
        max_len=DB_STR_NAME_TITLE_MAX_LEN,
    )


def validate_size_kb_required(cls: Any, value: int) -> int:
    return require_int_name_min_max_len(
        v=value,
        name="size_kb",
        min_len=0,
        max_len=settings.api.payload_limit_kb,
    )


def validate_size_kb_optional(cls: Any, value: int | None) -> int | None:
    return optional_int_name_min_max_len(
        v=value,
        name="size_kb",
        max_len=settings.api.payload_limit_kb,
    )


def validate_latitude_required(cls: Any, value: float) -> float:
    return require_float_rounded_to_max_len(
        v=value,
        max_len=DB_FLOAT_MAX_LEN,
    )


def validate_latitude_optional(cls: Any, value: float | None) -> float | None:
    return optional_float_rounded_to_max_len(
        v=value,
        max_len=DB_FLOAT_MAX_LEN,
    )


def validate_longitude_required(cls: Any, value: float) -> float:
    return require_float_rounded_to_max_len(
        v=value,
        max_len=DB_FLOAT_MAX_LEN,
    )


def validate_longitude_optional(cls: Any, value: float | None) -> float | None:
    return optional_float_rounded_to_max_len(
        v=value,
        max_len=DB_FLOAT_MAX_LEN,
    )


def validate_address_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="address",
        min_len=0,
        max_len=255,
    )


def validate_address_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="address",
        max_len=255,
    )


def validate_ip_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="ip",
        min_len=0,
        max_len=40,
    )


def validate_ip_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="ip",
        max_len=40,
    )


def validate_isp_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="isp",
        min_len=0,
        max_len=255,
    )


def validate_isp_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="isp",
        max_len=255,
    )


def validate_ip_location_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="location",
        min_len=0,
        max_len=255,
    )


def validate_ip_location_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="location",
        max_len=255,
    )


def validate_group_name_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="group_name",
        min_len=0,
        max_len=255,
    )


def validate_group_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="group_name",
        max_len=255,
    )


def validate_group_slug_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="group_slug",
        min_len=0,
        max_len=12,
    )


def validate_snap_name_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="snap_name",
        min_len=0,
        max_len=255,
    )


def validate_snap_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="snap_name",
        max_len=255,
    )


def validate_snap_slug_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="snap_slug",
        min_len=0,
        max_len=12,
    )


def validate_altitude_required(cls: Any, value: int) -> int:
    return require_int_name_min_max_len(
        v=value,
        name="altitude",
        min_len=0,
        max_len=1000,
    )


def validate_altitude_optional(cls: Any, value: int | None) -> int | None:
    return optional_int_name_min_max_len(
        v=value,
        name="altitude",
        max_len=1000,
    )


def validate_referrer_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="referrer",
        min_len=0,
        max_len=DB_STR_URL_PATH_MAX_LEN,
    )


def validate_utm_campaign_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="utm_campaign",
        max_len=255,
    )


def validate_utm_content_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="utm_content",
        max_len=255,
    )


def validate_utm_medium_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="utm_medium",
        max_len=255,
    )


def validate_utm_source_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="utm_source",
        max_len=255,
    )


def validate_utm_term_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="utm_term",
        max_len=255,
    )


def validate_reporting_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="reporting_id",
        max_len=32,
    )


def validate_hotspot_type_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="hotspot_type_name",
        max_len=32,
    )


def validate_hotspot_content_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="hotspot_content",
        max_len=DB_STR_BLOB_MAX_LEN,
    )


def validate_hotspot_icon_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="hotspot_icon_name",
        max_len=255,
    )


def validate_hotspot_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="hotspot_name",
        max_len=255,
    )


def validate_hotspot_user_icon_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="hotspot_user_icon_name",
        max_len=255,
    )


def validate_linked_snap_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="linked_snap_name",
        max_len=255,
    )


def validate_snap_file_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="snap_file_name",
        max_len=255,
    )


def validate_icon_color_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="icon_color",
        max_len=32,
    )


def validate_bg_color_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="bg_color",
        max_len=32,
    )


def validate_text_color_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="text_color",
        max_len=32,
    )


def validate_browser_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="browser",
        max_len=255,
    )


def validate_browser_version_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="browser_version",
        max_len=255,
    )


def validate_platform_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="platform",
        max_len=255,
    )


def validate_platform_version_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="platform_version",
        max_len=255,
    )


def validate_city_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="city",
        max_len=255,
    )


def validate_country_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="country",
        max_len=255,
    )


def validate_state_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="state",
        max_len=255,
    )


def validate_language_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="language",
        max_len=255,
    )


def validate_active_seconds_required(cls: Any, value: int) -> int:
    return require_int_name_min_max_len(
        v=value,
        name="active_seconds",
        min_len=0,
        max_len=86400,
    )


def validate_project_name_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="project_name",
        min_len=0,
        max_len=255,
    )


def validate_project_name_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="project_name",
        max_len=255,
    )


def validate_project_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="project_id",
        min_len=0,
        max_len=64,
    )


def validate_project_number_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="project_number",
        min_len=0,
        max_len=64,
    )


def validate_service_account_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="service_account",
        min_len=0,
        max_len=64,
    )


def validate_project_id_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="project_id",
        max_len=64,
    )


def validate_project_number_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="project_number",
        max_len=64,
    )


def validate_service_account_optional(cls: Any, value: str | None) -> str | None:
    return optional_string_name_min_max_len(
        v=value,
        name="service_account",
        max_len=64,
    )


def validate_measurement_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="measurement_id",
        min_len=0,
        max_len=16,
    )


def validate_property_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="property_id",
        min_len=0,
        max_len=16,
    )


def validate_stream_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="stream_id",
        min_len=0,
        max_len=16,
    )


def validate_keys_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="keys",
        min_len=0,
        max_len=DB_STR_BLOB_MAX_LEN,
    )


def validate_clicks_required(cls: Any, value: int) -> int:
    return require_int_name_min_max_len(
        v=value,
        name="clicks",
        min_len=0,
        max_len=DB_INT_INTEGER_MAX_LEN,
    )


def validate_impressions_required(cls: Any, value: int) -> int:
    return require_int_name_min_max_len(
        v=value,
        name="impressions",
        min_len=0,
        max_len=DB_INT_INTEGER_MAX_LEN,
    )


def validate_ctr_required(cls: Any, value: float) -> float:
    return require_float_rounded_to_max_len(
        v=value,
        max_len=DB_FLOAT_MAX_LEN,
    )


def validate_position_required(cls: Any, value: float) -> float:
    return require_float_rounded_to_max_len(
        v=value,
        max_len=DB_FLOAT_MAX_LEN,
    )


def validate_tracking_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="tracking_id",
        min_len=0,
        max_len=16,
    )


def validate_view_id_required(cls: Any, value: str) -> str:
    return require_string_name_min_max_len(
        v=value,
        name="view_id",
        min_len=0,
        max_len=16,
    )
