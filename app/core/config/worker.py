from os import environ
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class WorkerSettings(BaseSettings):
    broker_url: str = environ.get("WORKER_BROKER_URL", "redis://localhost:6379/0")
    result_backend: str = environ.get(
        "WORKER_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    schedule_src: str = environ.get(
        "WORKER_SCHEDULE_SOURCE", "redis://localhost:6379/0"
    )
    sentry_dsn: Optional[str] = environ.get("WORKER_SENTRY_DSN", None)

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="WORKER_",
        case_sensitive=False,
        extra="ignore",
    )

    # pydantic field validators
    @field_validator("sentry_dsn", mode="before")
    def validate_database_user(
        cls: Any, v: Optional[str], info: ValidationInfo
    ) -> str | None:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        return None
