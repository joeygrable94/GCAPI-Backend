from os import environ
from typing import Any, List, Optional

from dotenv import load_dotenv
from pydantic import EmailStr, FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .utilities import get_root_directory

load_dotenv()


class EmailSettings(BaseSettings):
    smtp_tls: bool = bool(environ.get("EMAIL_SMTP_TLS", True))
    smtp_ssl: bool = bool(environ.get("EMAIL_SMTP_SSL", False))
    smtp_port: int = int(environ.get("EMAIL_SMTP_PORT", 587))
    smtp_host: str = environ.get("EMAIL_SMTP_HOST", "smtp.gmail.com")
    smtp_user: EmailStr = EmailStr(environ.get("EMAIL_SMTP_USER", ""))
    smtp_password: str = environ.get("EMAIL_SMTP_PASSWORD", "")
    enabled: bool = bool(environ.get("EMAIL_ENABLED", False))
    from_email: EmailStr = EmailStr(
        environ.get("EMAIL_FROM_EMAIL", "noreply@getcommunity.com")
    )
    from_name: str = environ.get("EMAIL_FROM_NAME", "FastAPI")
    provider_restriction: bool = bool(environ.get("EMAIL_PROVIDER_RESTRICTION", True))
    allowed_providers: List[str] = list(
        environ.get("EMAIL_ALLOWED_PROVIDERS", ["getcommunity.com"])
    )
    test_user: EmailStr = EmailStr(
        environ.get("EMAIL_TEST_USER", "test@getcommunity.com")
    )
    templates_dir: str = "%s/templates/email/build" % get_root_directory(__file__)

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EMAIL_",
        case_sensitive=False,
    )

    # pydantic field validators
    @field_validator("enabled", mode="before")
    def assemble_emails_enabled(
        cls: Any, v: Optional[bool], info: FieldValidationInfo
    ) -> bool:  # pragma: no cover
        if v:
            return v
        return bool(
            info.data.get("smtp_host")
            and info.data.get("smtp_port")
            and info.data.get("from_email")
            and info.data.get("smtp_user")
            and info.data.get("smtp_password")
        )
