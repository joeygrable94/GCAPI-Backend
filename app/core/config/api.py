from enum import Enum
from os import environ
from typing import Any, Union

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .utilities import get_root_directory

load_dotenv()


class ApiModes(str, Enum):
    test = "test"
    development = "development"
    staging = "staging"
    production = "production"


class ApiSettings(BaseSettings):
    # API
    root_dir: str = get_root_directory(__file__)
    name: str = environ.get("API_NAME", "GCAPI")
    key: str = environ.get("API_KEY", "gcapi")
    version: str = environ.get("API_TAG", "0.0.0")
    mode: str = environ.get("API_MODE", "development")
    debug: bool = bool(
        environ.get("API_MODE", "development") == "test"
        or environ.get("API_MODE", "development") == "development"
        or environ.get("API_MODE", "development") == "staging"
        or environ.get("API_DEBUG", True)
    )
    prefix: str = "/api"
    timezone: str = environ.get("API_TIMEZONE", "America/Los_Angeles")
    domain_name: str = environ.get("API_DOMAIN", "localhost")
    host_ip: str = environ.get("API_HOST_IP", "0.0.0.0")
    host_port: int = int(environ.get("API_HOST_PORT", "8888"))
    logging_level: str = environ.get("API_LOG_LEVEL", "debug").upper()
    logger_name: str = environ.get("API_NAME", "GCAPI").lower()
    # Security
    asgi_header_key: str = "x-request-id"
    allowed_cors: Union[str, list[str]] | None = environ.get("API_ALLOWED_CORS")
    rsa_public_key: str = environ.get("API_RSA_PUBLIC_KEY", "")
    rsa_private_key: str = environ.get("API_RSA_PRIVATE_KEY", "")
    session_secret_key: str = environ.get(
        "API_SECRET_KEY",
        "54295fb3ad6577bf6ec55fc8a4e2ce86b4a490b5f1666f1e871e94855f6dc0a7",
    )
    csrf_header_key: str = "x-csrf-token"
    csrf_name_key: str = "gcapi-csrf-token"
    csrf_salt: str = "lXB*IUFLCcbz45Swnda92laS-DJG{rUX^ASz5Wzz;5sP"
    csrf_secret_key: str = environ.get(
        "API_CSRF_KEY",
        "fb4cd9547245b656a5a44441eebd5960432c95d9c45970be0d7442f91bf64366",
    )
    encryption_salt: str = environ.get(
        "API_ENCRYPTION_SALT", "aUW1+hREL5XAc3qFEJAR7trNW+yYAzOxoqvzsys0Zvs="
    )
    encryption_key: str = environ.get(
        "API_ENCRYPTION_KEY",
        "hNaZZH07R5yxXsbE1mEVPERNOJZwyb/O+jlhqonG2I0=",
    )
    # API Limitations
    payload_limit: int = 2048000  # 2MB
    payload_limit_kb: int = 2048  # 2MB
    query_limit_offset_default: int = int(
        environ.get("API_QUERY_LIMIT_OFFSET_DEFAULT", 0)
    )
    query_limit_rows_default: int = int(
        environ.get("API_QUERY_LIMIT_ROWS_DEFAULT", 100)
    )
    query_limit_rows_max: int = int(environ.get("API_QUERY_LIMIT_ROWS_MAX", 10000))
    allowed_mime_types: list[str] = [
        "webp",
        "gif",
        "jpg",
        "jpeg",
        "png",
        "csv",
        "json",
        "xml",
        "html",
        "md",
        "txt",
        "pdf",
    ]

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="API_",
        case_sensitive=False,
        extra="ignore",
    )

    # pydantic field validators
    @field_validator("allowed_cors", mode="before")
    def assemble_cors_origins(
        cls: Any, v: Union[str, list[str]], info: ValidationInfo
    ) -> list[str]:  # pragma: no cover
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]

    @field_validator("rsa_public_key", mode="before")
    def validate_rsa_public_key(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("RSA Public Key must be a string")

    @field_validator("rsa_private_key", mode="before")
    def validate_rsa_private_key(
        cls, v: str, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("RSA Private Key must be a string")
