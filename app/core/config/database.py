from os import environ
from typing import Union

from dotenv import load_dotenv
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

load_dotenv()

TEST_URI: str = "sqlite:///./test.db"
TEST_URI_ASYNC: str = "sqlite+aiosqlite:///./test.db"


class DatabaseSettings(BaseSettings):
    uri: Union[str, URL] = environ.get("DATABASE_URI", "")
    uri_async: Union[str, URL] = environ.get("DATABASE_URI_ASYNC", "")

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DATABASE_",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("uri", mode="before")
    def assemble_db_connection(
        cls, v: str | None, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if environ.get("API_MODE", "development") == "test":
            return TEST_URI
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_URI not set")

    @field_validator("uri_async", mode="before")
    def assemble_async_db_connection(
        cls, v: str | None, info: ValidationInfo
    ) -> str:  # pragma: no cover
        if environ.get("API_MODE", "development") == "test":
            return TEST_URI_ASYNC
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_URI_ASYNC not set")
