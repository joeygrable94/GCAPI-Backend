from enum import Enum
from typing import List, Optional

from pydantic import validator

from app.core.config import settings
from app.core.utilities import domain_name_regex, email_regex
from app.schemas.base import BaseSchema

DB_FLOAT_MAX_LEN = 20
DB_STR_NAME_TITLE_MAX_LEN = 96
DB_STR_URL_PATH_MAX_LEN = 2048
DB_STR_BLOB_MAX_LEN = 65500
DB_STR_LONGTEXT_MAX_LEN = 4000000000  # 4 billion characters
DB_INT_INTEGER_MAX_LEN = 1000000000  # 1 billion


# ----------------------------
# Validation Functions
# ----------------------------


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
    v: Optional[int],
    name: str,
    min_len: Optional[int] = None,
    max_len: int = 255,
) -> Optional[int]:
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
    excess_length = max(0, max_len - len(float_str))
    value = round(v, excess_length)
    return value


def optional_float_rounded_to_max_len(
    v: Optional[float],
    max_len: int = 20,
) -> Optional[float]:
    value: float | None = None
    if v:
        float_str = str(v).strip("0")
        excess_length = max(0, max_len - len(float_str))
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
    v: Optional[str],
    name: str,
    min_len: Optional[int] = None,
    max_len: int = 255,
) -> Optional[str]:
    if min_len is not None:
        if min_len == 0 and v and len(v) <= 0:
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
    v: Optional[str],
    name: str = "domain",
    min_len: Optional[int] = 5,
    max_len: int = 255,
) -> Optional[str]:
    if min_len is not None:
        if min_len == 0 and v and len(v) <= 0:
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
    if len(v) < 0:
        raise ValueError(f"{name} is required")
    if v.lower() not in choices:
        choices_str = ", ".join(choices)
        raise ValueError(f"{name} must be one of: {choices_str}")
    return v.lower()


def optional_string_in_list(
    v: Optional[str], name: str = "device", choices: List[str] = []
) -> Optional[str]:
    if v and len(v) < 0:
        raise ValueError(f"{name} is required")
    if v and v.lower() not in choices:
        choices_str = ", ".join(choices)
        raise ValueError(f"{name} must be one of: {choices_str}")
    if v:
        return v.lower()
    return v


# ----------------------------
# Validation Schemas
# ----------------------------


class ValidFileExtensionEnum(str, Enum):
    webp = "webp"
    gif = "gif"
    jpg = "jpg"
    jpeg = "jpeg"
    png = "png"
    csv = "csv"
    json = "json"
    xml = "xml"
    html = "html"
    md = "md"
    txt = "txt"
    pdf = "pdf"


class ValidateSchemaExtensionRequired(BaseSchema):
    extension: ValidFileExtensionEnum


class ValidateSchemaExtensionOptional(BaseSchema):
    extension: Optional[ValidFileExtensionEnum]


class ValidateSchemaTitleRequired(BaseSchema):
    title: str

    @validator("title", pre=True, allow_reuse=True)
    def validate_title(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="title",
            min_len=5,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaTitleOptional(BaseSchema):
    title: Optional[str]

    @validator("title", pre=True, allow_reuse=True)
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="title",
            min_len=5,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaDescriptionOptional(BaseSchema):
    description: Optional[str]

    @validator("description", pre=True, allow_reuse=True)
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="description",
            max_len=5000,
        )


class ValidateSchemaDomainRequired(BaseSchema):
    domain: str

    @validator("domain", pre=True, allow_reuse=True)
    def validate_domain(cls, value: str) -> str:
        return require_string_domain(
            v=value,
        )


class ValidateSchemaDomainOptional(BaseSchema):
    domain: Optional[str]

    @validator("domain", pre=True, allow_reuse=True)
    def validate_domain(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_domain(
            v=value,
        )


class ValidateSchemaCorpusRequired(BaseSchema):
    corpus: str

    @validator("corpus", pre=True, allow_reuse=True)
    def validate_corpus(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="corpus",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaCorpusOptional(BaseSchema):
    corpus: Optional[str]

    @validator("corpus", pre=True, allow_reuse=True)
    def validate_corpus(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="corpus",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaRawTextRequired(BaseSchema):
    rawtext: str

    @validator("rawtext", pre=True, allow_reuse=True)
    def validate_rawtext(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="rawtext",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaRawTextOptional(BaseSchema):
    rawtext: Optional[str]

    @validator("rawtext", pre=True, allow_reuse=True)
    def validate_rawtext(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="rawtext",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaUrlRequired(BaseSchema):
    url: str

    @validator("url", pre=True, allow_reuse=True)
    def validate_url(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="url",
            min_len=1,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaUrlOptional(BaseSchema):
    url: Optional[str]

    @validator("url", pre=True, allow_reuse=True)
    def validate_url(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="url",
            min_len=1,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaDeviceRequired(BaseSchema):
    device: str

    @validator("device", pre=True, allow_reuse=True)
    def validate_device(cls, value: str) -> str:
        return required_string_in_list(
            v=value,
            name="device",
            choices=["mobile", "desktop"],
        )


class ValidateSchemaStrategyRequired(BaseSchema):
    strategy: str

    @validator("strategy", pre=True, allow_reuse=True)
    def validate_strategy(cls, value: str) -> str:
        return required_string_in_list(
            v=value,
            name="strategy",
            choices=["mobile", "desktop"],
        )


class ValidateSchemaPerformanceValueRequired(BaseSchema):
    ps_value: str

    @validator("ps_value", pre=True, allow_reuse=True)
    def validate_ps_value(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="ps_value",
            min_len=0,
            max_len=4,
        )


class ValidateSchemaPerformanceValueOptional(BaseSchema):
    ps_value: Optional[str]

    @validator("ps_value", pre=True, allow_reuse=True)
    def validate_ps_value(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="ps_value",
            min_len=0,
            max_len=4,
        )


class ValidateSchemaAuthIdRequired(BaseSchema):
    auth_id: str

    @validator("auth_id", pre=True, allow_reuse=True)
    def validate_auth_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="auth_id",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaEmailRequired(BaseSchema):
    email: str

    @validator("email", pre=True, allow_reuse=True)
    def validate_email(cls, value: str) -> str:
        return require_string_email(
            v=value,
            name="email",
            min_len=5,
            max_len=320,
        )


class ValidateSchemaUsernameRequired(BaseSchema):
    username: str

    @validator("username", pre=True, allow_reuse=True)
    def validate_username(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="username",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaPasswordRequired(BaseSchema):
    password: str

    @validator("password", pre=True, allow_reuse=True)
    def validate_password(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="password",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUsernameOptional(BaseSchema):
    username: Optional[str]

    @validator("username", pre=True, allow_reuse=True)
    def validate_username(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="username",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaPasswordOptional(BaseSchema):
    password: Optional[str]

    @validator("password", pre=True, allow_reuse=True)
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="password",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaHashedApiKeyRequired(BaseSchema):
    hashed_api_key: str

    @validator("hashed_api_key", pre=True, allow_reuse=True)
    def validate_hashed_api_key(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_api_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedSecretKeyRequired(BaseSchema):
    hashed_secret_key: str

    @validator("hashed_secret_key", pre=True, allow_reuse=True)
    def validate_hashed_secret_key(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_secret_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedApiKeyOptional(BaseSchema):
    hashed_api_key: Optional[str]

    @validator("hashed_api_key", pre=True, allow_reuse=True)
    def validate_hashed_api_key(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_api_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedSecretKeyOptional(BaseSchema):
    hashed_secret_key: Optional[str]

    @validator("hashed_secret_key", pre=True, allow_reuse=True)
    def validate_hashed_secret_key(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_secret_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaServerhostRequired(BaseSchema):
    serverhost: str

    @validator("serverhost", pre=True, allow_reuse=True)
    def validate_serverhost(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="serverhost",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaServerhostOptional(BaseSchema):
    serverhost: Optional[str]

    @validator("serverhost", pre=True, allow_reuse=True)
    def validate_serverhost(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="serverhost",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaKeysOptional(BaseSchema):
    keys: Optional[str]

    @validator("keys", pre=True, allow_reuse=True)
    def validate_keys(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="keys",
            max_len=65500,
        )


class ValidateSchemaObjectKeyRequired(BaseSchema):
    object_key: str

    @validator("object_key", pre=True, allow_reuse=True)
    def validate_object_key(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="object_key",
            min_len=0,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaObjectKeyOptional(BaseSchema):
    object_key: Optional[str]

    @validator("object_key", pre=True, allow_reuse=True)
    def validate_object_key(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="object_key",
            min_len=0,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaBucketNameRequired(BaseSchema):
    bucket_name: str

    @validator("bucket_name", pre=True, allow_reuse=True)
    def validate_bucket_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="bucket_name",
            min_len=0,
            max_len=100,
        )


class ValidateSchemaBucketNameOptional(BaseSchema):
    bucket_name: Optional[str]

    @validator("bucket_name", pre=True, allow_reuse=True)
    def validate_bucket_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="bucket_name",
            min_len=0,
            max_len=100,
        )


class ValidateSchemaCaptionOptional(BaseSchema):
    caption: Optional[str]

    @validator("caption", pre=True, allow_reuse=True)
    def validate_caption(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="caption",
            max_len=150,
        )


class ValidateSchemaNameRequired(BaseSchema):
    name: str

    @validator("name", pre=True, allow_reuse=True)
    def validate_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="name",
            min_len=0,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaNameOptional(BaseSchema):
    name: Optional[str]

    @validator("name", pre=True, allow_reuse=True)
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="name",
            min_len=0,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaSizeKbRequired(BaseSchema):
    size_kb: int

    @validator("size_kb", pre=True, allow_reuse=True)
    def validate_size_kb(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="size_kb",
            min_len=0,
            max_len=settings.PAYLOAD_LIMIT_KB,
        )


class ValidateSchemaSizeKbOptional(BaseSchema):
    size_kb: Optional[int]

    @validator("size_kb", pre=True, allow_reuse=True)
    def validate_size_kb(cls, value: Optional[int]) -> Optional[int]:
        return optional_int_name_min_max_len(
            v=value,
            name="size_kb",
            min_len=0,
            max_len=settings.PAYLOAD_LIMIT_KB,
        )


class ValidateSchemaLatitudeRequired(BaseSchema):
    latitude: float

    @validator("latitude", pre=True, allow_reuse=True)
    def validate_latitude(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaLatitudeOptional(BaseSchema):
    latitude: Optional[float]

    @validator("latitude", pre=True, allow_reuse=True)
    def validate_latitude(cls, value: Optional[float]) -> Optional[float]:
        return optional_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaLongitudeRequired(BaseSchema):
    longitude: float

    @validator("longitude", pre=True, allow_reuse=True)
    def validate_longitude(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaLongitudeOptional(BaseSchema):
    longitude: Optional[float]

    @validator("longitude", pre=True, allow_reuse=True)
    def validate_longitude(cls, value: Optional[float]) -> Optional[float]:
        return optional_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaAddressRequired(BaseSchema):
    address: str

    @validator("address", pre=True, allow_reuse=True)
    def validate_address(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="address",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaAddressOptional(BaseSchema):
    address: Optional[str]

    @validator("address", pre=True, allow_reuse=True)
    def validate_address(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="address",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIpRequired(BaseSchema):
    ip: str

    @validator("ip", pre=True, allow_reuse=True)
    def validate_ip(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="ip",
            min_len=0,
            max_len=40,
        )


class ValidateSchemaIpOptional(BaseSchema):
    ip: Optional[str]

    @validator("ip", pre=True, allow_reuse=True)
    def validate_ip(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="ip",
            min_len=0,
            max_len=40,
        )


class ValidateSchemaIspRequired(BaseSchema):
    isp: str

    @validator("isp", pre=True, allow_reuse=True)
    def validate_isp(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="isp",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIspOptional(BaseSchema):
    isp: Optional[str]

    @validator("isp", pre=True, allow_reuse=True)
    def validate_isp(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="isp",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIpLocationRequired(BaseSchema):
    location: str

    @validator("location", pre=True, allow_reuse=True)
    def validate_location(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="location",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIpLocationOptional(BaseSchema):
    location: Optional[str]

    @validator("location", pre=True, allow_reuse=True)
    def validate_location(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="location",
            min_len=0,
            max_len=255,
        )


class ValidateGroupNameRequired(BaseSchema):
    group_name: str

    @validator("group_name", pre=True, allow_reuse=True)
    def validate_group_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="group_name",
            min_len=0,
            max_len=255,
        )


class ValidateGroupNameOptional(BaseSchema):
    group_name: Optional[str]

    @validator("group_name", pre=True, allow_reuse=True)
    def validate_group_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="group_name",
            min_len=0,
            max_len=255,
        )


class ValidateGroupSlugRequired(BaseSchema):
    group_slug: str

    @validator("group_slug", pre=True, allow_reuse=True)
    def validate_group_slug(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="group_slug",
            min_len=0,
            max_len=12,
        )


class ValidateSchemaSnapNameRequired(BaseSchema):
    snap_name: str

    @validator("snap_name", pre=True, allow_reuse=True)
    def validate_snap_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="snap_name",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaSnapNameOptional(BaseSchema):
    snap_name: Optional[str]

    @validator("snap_name", pre=True, allow_reuse=True)
    def validate_snap_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="snap_name",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaSnapSlugRequired(BaseSchema):
    snap_slug: str

    @validator("snap_slug", pre=True, allow_reuse=True)
    def validate_snap_slug(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="snap_slug",
            min_len=0,
            max_len=12,
        )


class ValidateSchemaAltitudeRequired(BaseSchema):
    altitude: int

    @validator("altitude", pre=True, allow_reuse=True)
    def validate_altitude(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="altitude",
            min_len=0,
            max_len=1000,
        )


class ValidateSchemaAltitudeOptional(BaseSchema):
    altitude: Optional[int]

    @validator("altitude", pre=True, allow_reuse=True)
    def validate_altitude(cls, value: Optional[int]) -> Optional[int]:
        return optional_int_name_min_max_len(
            v=value,
            name="altitude",
            min_len=0,
            max_len=1000,
        )


class ValidateSchemaReferrerRequired(BaseSchema):
    referrer: str

    @validator("referrer", pre=True, allow_reuse=True)
    def validate_referrer(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="referrer",
            min_len=0,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaUtmCampaignOptional(BaseSchema):
    utm_campaign: Optional[str]

    @validator("utm_campaign", pre=True, allow_reuse=True)
    def validate_utm_campaign(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_campaign",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmContentOptional(BaseSchema):
    utm_content: Optional[str]

    @validator("utm_content", pre=True, allow_reuse=True)
    def validate_utm_content(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_content",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmMediumOptional(BaseSchema):
    utm_medium: Optional[str]

    @validator("utm_medium", pre=True, allow_reuse=True)
    def validate_utm_medium(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_medium",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmSourceOptional(BaseSchema):
    utm_source: Optional[str]

    @validator("utm_source", pre=True, allow_reuse=True)
    def validate_utm_source(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_source",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmTermOptional(BaseSchema):
    utm_term: Optional[str]

    @validator("utm_term", pre=True, allow_reuse=True)
    def validate_utm_term(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_term",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaReportingIdRequired(BaseSchema):
    reporting_id: str

    @validator("reporting_id", pre=True, allow_reuse=True)
    def validate_reporting_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="reporting_id",
            min_len=0,
            max_len=32,
        )


class ValidateSchemaHotspotTypeNameOptional(BaseSchema):
    hotspot_type_name: Optional[str]

    @validator("hotspot_type_name", pre=True, allow_reuse=True)
    def validate_hotspot_type_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_type_name",
            max_len=32,
        )


class ValidateSchemaHotspotContentOptional(BaseSchema):
    hotspot_content: Optional[str]

    @validator("hotspot_content", pre=True, allow_reuse=True)
    def validate_hotspot_content(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_content",
            max_len=DB_STR_BLOB_MAX_LEN,
        )


class ValidateSchemaHotspotIconNameOptional(BaseSchema):
    hotspot_icon_name: Optional[str]

    @validator("hotspot_icon_name", pre=True, allow_reuse=True)
    def validate_hotspot_icon_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_icon_name",
            max_len=255,
        )


class ValidateSchemaHotspotNameOptional(BaseSchema):
    hotspot_name: Optional[str]

    @validator("hotspot_name", pre=True, allow_reuse=True)
    def validate_hotspot_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_name",
            max_len=255,
        )


class ValidateSchemaHotspotUserIconNameOptional(BaseSchema):
    hotspot_user_icon_name: Optional[str]

    @validator("hotspot_user_icon_name", pre=True, allow_reuse=True)
    def validate_hotspot_user_icon_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_user_icon_name",
            max_len=255,
        )


class ValidateSchemaLinkedSnapNameOptional(BaseSchema):
    linked_snap_name: Optional[str]

    @validator("linked_snap_name", pre=True, allow_reuse=True)
    def validate_linked_snap_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="linked_snap_name",
            max_len=255,
        )


class ValidateSchemaSnapFileNameOptional(BaseSchema):
    snap_file_name: Optional[str]

    @validator("snap_file_name", pre=True, allow_reuse=True)
    def validate_snap_file_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="snap_file_name",
            max_len=255,
        )


class ValidateSchemaIconColorOptional(BaseSchema):
    icon_color: Optional[str]

    @validator("icon_color", pre=True, allow_reuse=True)
    def validate_icon_color(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="icon_color",
            max_len=32,
        )


class ValidateSchemaBgColorOptional(BaseSchema):
    bg_color: Optional[str]

    @validator("bg_color", pre=True, allow_reuse=True)
    def validate_bg_color(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="bg_color",
            max_len=32,
        )


class ValidateSchemaTextColorOptional(BaseSchema):
    text_color: Optional[str]

    @validator("text_color", pre=True, allow_reuse=True)
    def validate_text_color(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="text_color",
            max_len=32,
        )


class ValidateSchemaBrowserOptional(BaseSchema):
    browser: Optional[str]

    @validator("browser", pre=True, allow_reuse=True)
    def validate_browser(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="browser",
            max_len=255,
        )


class ValidateSchemaBrowserVersionOptional(BaseSchema):
    browser_version: Optional[str]

    @validator("browser_version", pre=True, allow_reuse=True)
    def validate_browser_version(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="browser_version",
            max_len=255,
        )


class ValidateSchemaPlatformOptional(BaseSchema):
    platform: Optional[str]

    @validator("platform", pre=True, allow_reuse=True)
    def validate_platform(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="platform",
            max_len=255,
        )


class ValidateSchemaPlatformVersionOptional(BaseSchema):
    platform_version: Optional[str]

    @validator("platform_version", pre=True, allow_reuse=True)
    def validate_platform_version(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="platform_version",
            max_len=255,
        )


class ValidateSchemaCityOptional(BaseSchema):
    city: Optional[str]

    @validator("city", pre=True, allow_reuse=True)
    def validate_city(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="city",
            max_len=255,
        )


class ValidateSchemaCountryOptional(BaseSchema):
    country: Optional[str]

    @validator("country", pre=True, allow_reuse=True)
    def validate_country(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="country",
            max_len=255,
        )


class ValidateSchemaStateOptional(BaseSchema):
    state: Optional[str]

    @validator("state", pre=True, allow_reuse=True)
    def validate_state(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="state",
            max_len=255,
        )


class ValidateSchemaLanguageOptional(BaseSchema):
    language: Optional[str]

    @validator("language", pre=True, allow_reuse=True)
    def validate_language(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="language",
            max_len=255,
        )


class ValidateSchemaActiveSecondsRequired(BaseSchema):
    active_seconds: int

    @validator("active_seconds", pre=True, allow_reuse=True)
    def validate_active_seconds(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="active_seconds",
            min_len=0,
            max_len=86400,
        )


class ValidateSchemaProjectNameRequired(BaseSchema):
    project_name: str

    @validator("project_name", pre=True, allow_reuse=True)
    def validate_project_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="project_name",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaHashedProjectIdRequired(BaseSchema):
    hashed_project_id: str

    @validator("hashed_project_id", pre=True, allow_reuse=True)
    def validate_hashed_project_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_project_id",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedProjectNumberRequired(BaseSchema):
    hashed_project_number: str

    @validator("hashed_project_number", pre=True, allow_reuse=True)
    def validate_hashed_project_number(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_project_number",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedServiceAccountRequired(BaseSchema):
    hashed_service_account: str

    @validator("hashed_service_account", pre=True, allow_reuse=True)
    def validate_hashed_service_account(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_service_account",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedProjectIdOptional(BaseSchema):
    hashed_project_id: Optional[str]

    @validator("hashed_project_id", pre=True, allow_reuse=True)
    def validate_hashed_project_id(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_project_id",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedProjectNumberOptional(BaseSchema):
    hashed_project_number: Optional[str]

    @validator("hashed_project_number", pre=True, allow_reuse=True)
    def validate_hashed_project_number(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_project_number",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedServiceAccountOptional(BaseSchema):
    hashed_service_account: Optional[str]

    @validator("hashed_service_account", pre=True, allow_reuse=True)
    def validate_hashed_service_account(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_service_account",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaMeasurementIdRequired(BaseSchema):
    measurement_id: str

    @validator("measurement_id", pre=True, allow_reuse=True)
    def validate_measurement_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="measurement_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaPropertyIdRequired(BaseSchema):
    property_id: str

    @validator("property_id", pre=True, allow_reuse=True)
    def validate_property_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="property_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaStreamIdRequired(BaseSchema):
    stream_id: str

    @validator("stream_id", pre=True, allow_reuse=True)
    def validate_stream_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="stream_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaKeysRequired(BaseSchema):
    keys: str

    @validator("keys", pre=True, allow_reuse=True)
    def validate_keys(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="keys",
            min_len=0,
            max_len=DB_STR_BLOB_MAX_LEN,
        )


class ValidateSchemaClicksRequired(BaseSchema):
    clicks: int

    @validator("clicks", pre=True, allow_reuse=True)
    def validate_clicks(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="clicks",
            min_len=0,
            max_len=DB_INT_INTEGER_MAX_LEN,
        )


class ValidateSchemaImpressionsRequired(BaseSchema):
    impressions: int

    @validator("impressions", pre=True, allow_reuse=True)
    def validate_impressions(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="impressions",
            min_len=0,
            max_len=DB_INT_INTEGER_MAX_LEN,
        )


class ValidateSchemaCtrRequired(BaseSchema):
    ctr: float

    @validator("ctr", pre=True, allow_reuse=True)
    def validate_ctr(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaPositionRequired(BaseSchema):
    position: float

    @validator("position", pre=True, allow_reuse=True)
    def validate_position(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaTrackingIdRequired(BaseSchema):
    tracking_id: str

    @validator("tracking_id", pre=True, allow_reuse=True)
    def validate_tracking_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="tracking_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaViewIdRequired(BaseSchema):
    view_id: str

    @validator("view_id", pre=True, allow_reuse=True)
    def validate_view_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="view_id",
            min_len=0,
            max_len=16,
        )
