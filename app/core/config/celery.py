from os import environ
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class CelerySettings(BaseSettings):
    broker_url: str = environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    result_backend: str = environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    sentry_dsn: Optional[str] = environ.get("CELERY_SENTRY_DSN", None)

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CELERY_",
        case_sensitive=False,
    )

    # pydantic field validators
    @field_validator("sentry_dsn", mode="before")
    def validate_database_user(
        cls: Any, v: Optional[str], info: FieldValidationInfo
    ) -> str | None:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        return None
