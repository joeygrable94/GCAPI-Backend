from os import environ
from typing import Any, List, Optional, Union

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .utilities import get_root_directory

load_dotenv()


class ApiSettings(BaseSettings):
    # API
    root_dir: str = get_root_directory(__file__)
    name: str = environ.get("API_NAME", "GCAPI")
    key: str = environ.get("API_KEY", "gcapi")
    version: str = environ.get("API_TAG", "0.0.3")
    mode: str = environ.get("API_MODE", "development")
    debug: bool = bool(
        environ.get("API_MODE", "development") == "test"
        or environ.get("API_MODE", "development") == "development"
        or environ.get("API_MODE", "development") == "staging"
        or environ.get("API_DEBUG", True)
    )
    host: str = environ.get("API_HOST_IP", "0.0.0.0")
    port: int = int(environ.get("API_HOST_PORT", 8888))
    prefix: str = "/api"
    domain_name: str = environ.get("API_DOMAIN", "localhost")
    timezone: str = environ.get("API_TIMEZONE", "America/Los_Angeles")
    logging_level: str = environ.get("API_LOG_LEVEL", "debug").upper()
    logger_name: str = environ.get("API_NAME", "GCAPI")
    # Security
    asgi_header_key: str = "x-request-id"
    allowed_cors: Optional[Union[str, List[str]]] = environ.get("API_ALLOWED_CORS")
    secret_key: str = environ.get(
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
    accepted_types: List[str] = [
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
    )

    # pydantic field validators
    @field_validator("allowed_cors", mode="before")
    def assemble_cors_origins(
        cls: Any, v: Union[str, List[str]], info: ValidationInfo
    ) -> List[str]:  # pragma: no cover
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]
