from os import environ
from typing import Any, List, Union

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .utilities import get_root_directory

load_dotenv()


class EmailSettings(BaseSettings):
    allowed_providers: str | List[str] = environ.get(
        "EMAIL_ALLOWED_PROVIDERS", "getcommunity.com"
    )
    allowed_from_emails: str | List[str] = environ.get(
        "EMAIL_ALLOWED_FROM_EMAILS", "admin@getcommunity.com"
    )
    enabled: bool = bool(environ.get("EMAIL_ENABLED", False))
    from_email: str = environ.get(
        "EMAIL_FROM_EMAIL", "'Get Community, Inc.' <admin@getcommunity.com>"
    )
    from_name: str = environ.get("EMAIL_FROM_NAME", "FastAPI")
    provider_restriction: bool = bool(environ.get("EMAIL_PROVIDER_RESTRICTION", True))
    test_user: str = environ.get("EMAIL_TEST_USER", "test@getcommunity.com")
    templates_dir: str = "%s/templates/email/build" % get_root_directory(__file__)

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EMAIL_",
        case_sensitive=False,
        extra="ignore",
    )

    # pydantic field validators
    @field_validator("allowed_providers", mode="before")
    def assemble_allowed_providers(
        cls: Any, v: Union[str, List[str]], info: ValidationInfo
    ) -> List[str]:  # pragma: no cover
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["getcommunity.com"]

    @field_validator("allowed_from_emails", mode="before")
    def assemble_allowed_from_emails(
        cls: Any, v: Union[str, List[str]], info: ValidationInfo
    ) -> List[str]:  # pragma: no cover
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["admin@getcommunity.com"]
