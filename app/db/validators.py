from enum import Enum
from typing import List, Optional

from pydantic import field_validator

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
    extension: Optional[ValidFileExtensionEnum] = None


class ValidateSchemaTitleRequired(BaseSchema):
    title: str

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="title",
            min_len=5,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaTitleOptional(BaseSchema):
    title: Optional[str] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="title",
            min_len=5,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaDescriptionOptional(BaseSchema):
    description: Optional[str] = None

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="description",
            max_len=5000,
        )


class ValidateSchemaDomainRequired(BaseSchema):
    domain: str

    @field_validator("domain", mode="before")
    @classmethod
    def validate_domain(cls, value: str) -> str:
        return require_string_domain(
            v=value,
        )


class ValidateSchemaDomainOptional(BaseSchema):
    domain: Optional[str] = None

    @field_validator("domain", mode="before")
    @classmethod
    def validate_domain(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_domain(
            v=value,
        )


class ValidateSchemaCorpusRequired(BaseSchema):
    corpus: str

    @field_validator("corpus", mode="before")
    @classmethod
    def validate_corpus(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="corpus",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaCorpusOptional(BaseSchema):
    corpus: Optional[str] = None

    @field_validator("corpus", mode="before")
    @classmethod
    def validate_corpus(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="corpus",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaRawTextRequired(BaseSchema):
    rawtext: str

    @field_validator("rawtext", mode="before")
    @classmethod
    def validate_rawtext(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="rawtext",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaRawTextOptional(BaseSchema):
    rawtext: Optional[str] = None

    @field_validator("rawtext", mode="before")
    @classmethod
    def validate_rawtext(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="rawtext",
            min_len=0,
            max_len=DB_STR_LONGTEXT_MAX_LEN,
        )


class ValidateSchemaUrlRequired(BaseSchema):
    url: str

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="url",
            min_len=1,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaUrlOptional(BaseSchema):
    url: Optional[str] = None

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="url",
            min_len=1,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaDeviceRequired(BaseSchema):
    device: str

    @field_validator("device", mode="before")
    @classmethod
    def validate_device(cls, value: str) -> str:
        return required_string_in_list(
            v=value,
            name="device",
            choices=["mobile", "desktop"],
        )


class ValidateSchemaStrategyRequired(BaseSchema):
    strategy: str

    @field_validator("strategy", mode="before")
    @classmethod
    def validate_strategy(cls, value: str) -> str:
        return required_string_in_list(
            v=value,
            name="strategy",
            choices=["mobile", "desktop"],
        )


class ValidateSchemaPerformanceValueRequired(BaseSchema):
    ps_value: str

    @field_validator("ps_value", mode="before")
    @classmethod
    def validate_ps_value(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="ps_value",
            min_len=0,
            max_len=4,
        )


class ValidateSchemaPerformanceValueOptional(BaseSchema):
    ps_value: Optional[str] = None

    @field_validator("ps_value", mode="before")
    @classmethod
    def validate_ps_value(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="ps_value",
            min_len=0,
            max_len=4,
        )


class ValidateSchemaAuthIdRequired(BaseSchema):
    auth_id: str

    @field_validator("auth_id", mode="before")
    @classmethod
    def validate_auth_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="auth_id",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaEmailRequired(BaseSchema):
    email: str

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return require_string_email(
            v=value,
            name="email",
            min_len=5,
            max_len=320,
        )


class ValidateSchemaUsernameRequired(BaseSchema):
    username: str

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="username",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaPasswordRequired(BaseSchema):
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="password",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUsernameOptional(BaseSchema):
    username: Optional[str] = None

    @field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="username",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaPasswordOptional(BaseSchema):
    password: Optional[str] = None

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="password",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaHashedApiKeyRequired(BaseSchema):
    hashed_api_key: str

    @field_validator("hashed_api_key", mode="before")
    @classmethod
    def validate_hashed_api_key(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_api_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedSecretKeyRequired(BaseSchema):
    hashed_secret_key: str

    @field_validator("hashed_secret_key", mode="before")
    @classmethod
    def validate_hashed_secret_key(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_secret_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedApiKeyOptional(BaseSchema):
    hashed_api_key: Optional[str] = None

    @field_validator("hashed_api_key", mode="before")
    @classmethod
    def validate_hashed_api_key(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_api_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedSecretKeyOptional(BaseSchema):
    hashed_secret_key: Optional[str] = None

    @field_validator("hashed_secret_key", mode="before")
    @classmethod
    def validate_hashed_secret_key(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_secret_key",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaServerhostRequired(BaseSchema):
    serverhost: str

    @field_validator("serverhost", mode="before")
    @classmethod
    def validate_serverhost(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="serverhost",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaServerhostOptional(BaseSchema):
    serverhost: Optional[str] = None

    @field_validator("serverhost", mode="before")
    @classmethod
    def validate_serverhost(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="serverhost",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaKeysOptional(BaseSchema):
    keys: Optional[str] = None

    @field_validator("keys", mode="before")
    @classmethod
    def validate_keys(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="keys",
            max_len=65500,
        )


class ValidateSchemaObjectKeyRequired(BaseSchema):
    object_key: str

    @field_validator("object_key", mode="before")
    @classmethod
    def validate_object_key(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="object_key",
            min_len=0,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaObjectKeyOptional(BaseSchema):
    object_key: Optional[str] = None

    @field_validator("object_key", mode="before")
    @classmethod
    def validate_object_key(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="object_key",
            min_len=0,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaBucketNameRequired(BaseSchema):
    bucket_name: str

    @field_validator("bucket_name", mode="before")
    @classmethod
    def validate_bucket_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="bucket_name",
            min_len=0,
            max_len=100,
        )


class ValidateSchemaBucketNameOptional(BaseSchema):
    bucket_name: Optional[str] = None

    @field_validator("bucket_name", mode="before")
    @classmethod
    def validate_bucket_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="bucket_name",
            min_len=0,
            max_len=100,
        )


class ValidateSchemaCaptionOptional(BaseSchema):
    caption: Optional[str] = None

    @field_validator("caption", mode="before")
    @classmethod
    def validate_caption(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="caption",
            max_len=150,
        )


class ValidateSchemaNameRequired(BaseSchema):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="name",
            min_len=0,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaNameOptional(BaseSchema):
    name: Optional[str] = None

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="name",
            min_len=0,
            max_len=DB_STR_NAME_TITLE_MAX_LEN,
        )


class ValidateSchemaSizeKbRequired(BaseSchema):
    size_kb: int

    @field_validator("size_kb", mode="before")
    @classmethod
    def validate_size_kb(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="size_kb",
            min_len=0,
            max_len=settings.PAYLOAD_LIMIT_KB,
        )


class ValidateSchemaSizeKbOptional(BaseSchema):
    size_kb: Optional[int] = None

    @field_validator("size_kb", mode="before")
    @classmethod
    def validate_size_kb(cls, value: Optional[int]) -> Optional[int]:
        return optional_int_name_min_max_len(
            v=value,
            name="size_kb",
            min_len=0,
            max_len=settings.PAYLOAD_LIMIT_KB,
        )


class ValidateSchemaLatitudeRequired(BaseSchema):
    latitude: float

    @field_validator("latitude", mode="before")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaLatitudeOptional(BaseSchema):
    latitude: Optional[float] = None

    @field_validator("latitude", mode="before")
    @classmethod
    def validate_latitude(cls, value: Optional[float]) -> Optional[float]:
        return optional_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaLongitudeRequired(BaseSchema):
    longitude: float

    @field_validator("longitude", mode="before")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaLongitudeOptional(BaseSchema):
    longitude: Optional[float] = None

    @field_validator("longitude", mode="before")
    @classmethod
    def validate_longitude(cls, value: Optional[float]) -> Optional[float]:
        return optional_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaAddressRequired(BaseSchema):
    address: str

    @field_validator("address", mode="before")
    @classmethod
    def validate_address(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="address",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaAddressOptional(BaseSchema):
    address: Optional[str] = None

    @field_validator("address", mode="before")
    @classmethod
    def validate_address(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="address",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIpRequired(BaseSchema):
    ip: str

    @field_validator("ip", mode="before")
    @classmethod
    def validate_ip(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="ip",
            min_len=0,
            max_len=40,
        )


class ValidateSchemaIpOptional(BaseSchema):
    ip: Optional[str] = None

    @field_validator("ip", mode="before")
    @classmethod
    def validate_ip(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="ip",
            min_len=0,
            max_len=40,
        )


class ValidateSchemaIspRequired(BaseSchema):
    isp: str

    @field_validator("isp", mode="before")
    @classmethod
    def validate_isp(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="isp",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIspOptional(BaseSchema):
    isp: Optional[str] = None

    @field_validator("isp", mode="before")
    @classmethod
    def validate_isp(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="isp",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIpLocationRequired(BaseSchema):
    location: str

    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="location",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaIpLocationOptional(BaseSchema):
    location: Optional[str] = None

    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="location",
            min_len=0,
            max_len=255,
        )


class ValidateGroupNameRequired(BaseSchema):
    group_name: str

    @field_validator("group_name", mode="before")
    @classmethod
    def validate_group_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="group_name",
            min_len=0,
            max_len=255,
        )


class ValidateGroupNameOptional(BaseSchema):
    group_name: Optional[str] = None

    @field_validator("group_name", mode="before")
    @classmethod
    def validate_group_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="group_name",
            min_len=0,
            max_len=255,
        )


class ValidateGroupSlugRequired(BaseSchema):
    group_slug: str

    @field_validator("group_slug", mode="before")
    @classmethod
    def validate_group_slug(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="group_slug",
            min_len=0,
            max_len=12,
        )


class ValidateSchemaSnapNameRequired(BaseSchema):
    snap_name: str

    @field_validator("snap_name", mode="before")
    @classmethod
    def validate_snap_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="snap_name",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaSnapNameOptional(BaseSchema):
    snap_name: Optional[str] = None

    @field_validator("snap_name", mode="before")
    @classmethod
    def validate_snap_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="snap_name",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaSnapSlugRequired(BaseSchema):
    snap_slug: str

    @field_validator("snap_slug", mode="before")
    @classmethod
    def validate_snap_slug(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="snap_slug",
            min_len=0,
            max_len=12,
        )


class ValidateSchemaAltitudeRequired(BaseSchema):
    altitude: int

    @field_validator("altitude", mode="before")
    @classmethod
    def validate_altitude(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="altitude",
            min_len=0,
            max_len=1000,
        )


class ValidateSchemaAltitudeOptional(BaseSchema):
    altitude: Optional[int] = None

    @field_validator("altitude", mode="before")
    @classmethod
    def validate_altitude(cls, value: Optional[int]) -> Optional[int]:
        return optional_int_name_min_max_len(
            v=value,
            name="altitude",
            min_len=0,
            max_len=1000,
        )


class ValidateSchemaReferrerRequired(BaseSchema):
    referrer: str

    @field_validator("referrer", mode="before")
    @classmethod
    def validate_referrer(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="referrer",
            min_len=0,
            max_len=DB_STR_URL_PATH_MAX_LEN,
        )


class ValidateSchemaUtmCampaignOptional(BaseSchema):
    utm_campaign: Optional[str] = None

    @field_validator("utm_campaign", mode="before")
    @classmethod
    def validate_utm_campaign(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_campaign",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmContentOptional(BaseSchema):
    utm_content: Optional[str] = None

    @field_validator("utm_content", mode="before")
    @classmethod
    def validate_utm_content(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_content",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmMediumOptional(BaseSchema):
    utm_medium: Optional[str] = None

    @field_validator("utm_medium", mode="before")
    @classmethod
    def validate_utm_medium(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_medium",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmSourceOptional(BaseSchema):
    utm_source: Optional[str] = None

    @field_validator("utm_source", mode="before")
    @classmethod
    def validate_utm_source(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_source",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaUtmTermOptional(BaseSchema):
    utm_term: Optional[str] = None

    @field_validator("utm_term", mode="before")
    @classmethod
    def validate_utm_term(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="utm_term",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaReportingIdRequired(BaseSchema):
    reporting_id: str

    @field_validator("reporting_id", mode="before")
    @classmethod
    def validate_reporting_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="reporting_id",
            min_len=0,
            max_len=32,
        )


class ValidateSchemaHotspotTypeNameOptional(BaseSchema):
    hotspot_type_name: Optional[str] = None

    @field_validator("hotspot_type_name", mode="before")
    @classmethod
    def validate_hotspot_type_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_type_name",
            max_len=32,
        )


class ValidateSchemaHotspotContentOptional(BaseSchema):
    hotspot_content: Optional[str] = None

    @field_validator("hotspot_content", mode="before")
    @classmethod
    def validate_hotspot_content(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_content",
            max_len=DB_STR_BLOB_MAX_LEN,
        )


class ValidateSchemaHotspotIconNameOptional(BaseSchema):
    hotspot_icon_name: Optional[str] = None

    @field_validator("hotspot_icon_name", mode="before")
    @classmethod
    def validate_hotspot_icon_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_icon_name",
            max_len=255,
        )


class ValidateSchemaHotspotNameOptional(BaseSchema):
    hotspot_name: Optional[str] = None

    @field_validator("hotspot_name", mode="before")
    @classmethod
    def validate_hotspot_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_name",
            max_len=255,
        )


class ValidateSchemaHotspotUserIconNameOptional(BaseSchema):
    hotspot_user_icon_name: Optional[str] = None

    @field_validator("hotspot_user_icon_name", mode="before")
    @classmethod
    def validate_hotspot_user_icon_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hotspot_user_icon_name",
            max_len=255,
        )


class ValidateSchemaLinkedSnapNameOptional(BaseSchema):
    linked_snap_name: Optional[str] = None

    @field_validator("linked_snap_name", mode="before")
    @classmethod
    def validate_linked_snap_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="linked_snap_name",
            max_len=255,
        )


class ValidateSchemaSnapFileNameOptional(BaseSchema):
    snap_file_name: Optional[str] = None

    @field_validator("snap_file_name", mode="before")
    @classmethod
    def validate_snap_file_name(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="snap_file_name",
            max_len=255,
        )


class ValidateSchemaIconColorOptional(BaseSchema):
    icon_color: Optional[str] = None

    @field_validator("icon_color", mode="before")
    @classmethod
    def validate_icon_color(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="icon_color",
            max_len=32,
        )


class ValidateSchemaBgColorOptional(BaseSchema):
    bg_color: Optional[str] = None

    @field_validator("bg_color", mode="before")
    @classmethod
    def validate_bg_color(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="bg_color",
            max_len=32,
        )


class ValidateSchemaTextColorOptional(BaseSchema):
    text_color: Optional[str] = None

    @field_validator("text_color", mode="before")
    @classmethod
    def validate_text_color(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="text_color",
            max_len=32,
        )


class ValidateSchemaBrowserOptional(BaseSchema):
    browser: Optional[str] = None

    @field_validator("browser", mode="before")
    @classmethod
    def validate_browser(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="browser",
            max_len=255,
        )


class ValidateSchemaBrowserVersionOptional(BaseSchema):
    browser_version: Optional[str] = None

    @field_validator("browser_version", mode="before")
    @classmethod
    def validate_browser_version(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="browser_version",
            max_len=255,
        )


class ValidateSchemaPlatformOptional(BaseSchema):
    platform: Optional[str] = None

    @field_validator("platform", mode="before")
    @classmethod
    def validate_platform(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="platform",
            max_len=255,
        )


class ValidateSchemaPlatformVersionOptional(BaseSchema):
    platform_version: Optional[str] = None

    @field_validator("platform_version", mode="before")
    @classmethod
    def validate_platform_version(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="platform_version",
            max_len=255,
        )


class ValidateSchemaCityOptional(BaseSchema):
    city: Optional[str] = None

    @field_validator("city", mode="before")
    @classmethod
    def validate_city(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="city",
            max_len=255,
        )


class ValidateSchemaCountryOptional(BaseSchema):
    country: Optional[str] = None

    @field_validator("country", mode="before")
    @classmethod
    def validate_country(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="country",
            max_len=255,
        )


class ValidateSchemaStateOptional(BaseSchema):
    state: Optional[str] = None

    @field_validator("state", mode="before")
    @classmethod
    def validate_state(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="state",
            max_len=255,
        )


class ValidateSchemaLanguageOptional(BaseSchema):
    language: Optional[str] = None

    @field_validator("language", mode="before")
    @classmethod
    def validate_language(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="language",
            max_len=255,
        )


class ValidateSchemaActiveSecondsRequired(BaseSchema):
    active_seconds: int

    @field_validator("active_seconds", mode="before")
    @classmethod
    def validate_active_seconds(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="active_seconds",
            min_len=0,
            max_len=86400,
        )


class ValidateSchemaProjectNameRequired(BaseSchema):
    project_name: str

    @field_validator("project_name", mode="before")
    @classmethod
    def validate_project_name(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="project_name",
            min_len=0,
            max_len=255,
        )


class ValidateSchemaHashedProjectIdRequired(BaseSchema):
    hashed_project_id: str

    @field_validator("hashed_project_id", mode="before")
    @classmethod
    def validate_hashed_project_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_project_id",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedProjectNumberRequired(BaseSchema):
    hashed_project_number: str

    @field_validator("hashed_project_number", mode="before")
    @classmethod
    def validate_hashed_project_number(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_project_number",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedServiceAccountRequired(BaseSchema):
    hashed_service_account: str

    @field_validator("hashed_service_account", mode="before")
    @classmethod
    def validate_hashed_service_account(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="hashed_service_account",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedProjectIdOptional(BaseSchema):
    hashed_project_id: Optional[str] = None

    @field_validator("hashed_project_id", mode="before")
    @classmethod
    def validate_hashed_project_id(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_project_id",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedProjectNumberOptional(BaseSchema):
    hashed_project_number: Optional[str] = None

    @field_validator("hashed_project_number", mode="before")
    @classmethod
    def validate_hashed_project_number(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_project_number",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaHashedServiceAccountOptional(BaseSchema):
    hashed_service_account: Optional[str] = None

    @field_validator("hashed_service_account", mode="before")
    @classmethod
    def validate_hashed_service_account(cls, value: Optional[str]) -> Optional[str]:
        return optional_string_name_min_max_len(
            v=value,
            name="hashed_service_account",
            min_len=0,
            max_len=64,
        )


class ValidateSchemaMeasurementIdRequired(BaseSchema):
    measurement_id: str

    @field_validator("measurement_id", mode="before")
    @classmethod
    def validate_measurement_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="measurement_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaPropertyIdRequired(BaseSchema):
    property_id: str

    @field_validator("property_id", mode="before")
    @classmethod
    def validate_property_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="property_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaStreamIdRequired(BaseSchema):
    stream_id: str

    @field_validator("stream_id", mode="before")
    @classmethod
    def validate_stream_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="stream_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaKeysRequired(BaseSchema):
    keys: str

    @field_validator("keys", mode="before")
    @classmethod
    def validate_keys(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="keys",
            min_len=0,
            max_len=DB_STR_BLOB_MAX_LEN,
        )


class ValidateSchemaClicksRequired(BaseSchema):
    clicks: int

    @field_validator("clicks", mode="before")
    @classmethod
    def validate_clicks(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="clicks",
            min_len=0,
            max_len=DB_INT_INTEGER_MAX_LEN,
        )


class ValidateSchemaImpressionsRequired(BaseSchema):
    impressions: int

    @field_validator("impressions", mode="before")
    @classmethod
    def validate_impressions(cls, value: int) -> int:
        return require_int_name_min_max_len(
            v=value,
            name="impressions",
            min_len=0,
            max_len=DB_INT_INTEGER_MAX_LEN,
        )


class ValidateSchemaCtrRequired(BaseSchema):
    ctr: float

    @field_validator("ctr", mode="before")
    @classmethod
    def validate_ctr(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaPositionRequired(BaseSchema):
    position: float

    @field_validator("position", mode="before")
    @classmethod
    def validate_position(cls, value: float) -> float:
        return require_float_rounded_to_max_len(
            v=value,
            max_len=DB_FLOAT_MAX_LEN,
        )


class ValidateSchemaTrackingIdRequired(BaseSchema):
    tracking_id: str

    @field_validator("tracking_id", mode="before")
    @classmethod
    def validate_tracking_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="tracking_id",
            min_len=0,
            max_len=16,
        )


class ValidateSchemaViewIdRequired(BaseSchema):
    view_id: str

    @field_validator("view_id", mode="before")
    @classmethod
    def validate_view_id(cls, value: str) -> str:
        return require_string_name_min_max_len(
            v=value,
            name="view_id",
            min_len=0,
            max_len=16,
        )
