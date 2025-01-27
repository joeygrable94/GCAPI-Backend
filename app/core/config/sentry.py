from os import environ
from typing import Any

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class SentrySettings(BaseSettings):
    sentry_dsn: str | None = environ.get("SENTRY_DSN", None)

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SENTRY_",
        case_sensitive=False,
        extra="ignore",
    )

    # pydantic field validators
    @field_validator("sentry_dsn", mode="before")
    def validate_database_user(
        cls: Any, v: str | None, info: ValidationInfo
    ) -> str | None:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        return None
