from os import environ
from typing import Any, Optional, Union

from dotenv import load_dotenv
from pydantic import FieldValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

load_dotenv()

TEST_URI: str = "sqlite:///./test.db"
TEST_URI_ASYNC: str = "sqlite+aiosqlite:///./test.db"


class DatabaseSettings(BaseSettings):
    connector: str = environ.get("DATABASE_CONNECTOR", "mysql+pymysql")
    connector_async: str = environ.get("DATABASE_CONNECTOR_ASYNC", "mysql+aiomysql")
    user: str = environ.get("DATABASE_USER", "root")
    password: str = environ.get("DATABASE_PASSWORD", "root")
    server: str = environ.get("DATABASE_SERVER", "localhost")
    port: str = environ.get("DATABASE_PORT", "3306")
    name: str = environ.get("DATABASE_NAME", "database")
    charset: str = environ.get("DATABASE_CHARSET", "UTF8MB4")
    uri: Union[str, URL] = environ.get("DATABASE_URI", "")
    uri_async: Union[str, URL] = environ.get("DATABASE_URI_ASYNC", "")

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DATABASE_",
        case_sensitive=False,
    )

    # pydantic field validators
    @field_validator("connector", mode="before")
    def validate_database_connector(
        cls, v: Optional[str], info: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_CONNECTOR not set")

    @field_validator("connector_async", mode="before")
    def validate_database_async_connector(
        cls, v: Optional[str], info: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_CONNECTOR_ASYNC not set")

    @field_validator("user", mode="before")
    def validate_database_user(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_USER not set")

    @field_validator("password", mode="before")
    def validate_database_password(
        cls, v: Optional[str], info: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_PASSWORD not set")

    @field_validator("server", mode="before")
    def validate_database_server(
        cls, v: Optional[str], info: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_SERVER not set")

    @field_validator("port", mode="before")
    def validate_database_port(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_PORT not set")

    @field_validator("name", mode="before")
    def validate_database_name(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_NAME not set")

    @field_validator("charset", mode="before")
    def validate_database_charset(
        cls, v: Optional[str], info: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_CHARSET not set")

    @field_validator("uri", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> str:
        if environ.get("API_MODE", "development") == "test":
            return TEST_URI
        if isinstance(v, str):
            if len(v) > 0:
                return "{}://{}".format(info.data.get("connector"), v)
        return "{}://{}:{}@{}:{}/{}?charset={}".format(
            info.data.get("connector"),
            info.data.get("user"),
            info.data.get("password"),
            info.data.get("server"),
            info.data.get("port"),
            info.data.get("name"),
            info.data.get("charset"),
        )

    @field_validator("uri_async", mode="before")
    def assemble_async_db_connection(
        cls, v: Optional[str], info: FieldValidationInfo
    ) -> str:
        if environ.get("API_MODE", "development") == "test":
            return TEST_URI_ASYNC
        if isinstance(v, str):
            if len(v) > 0:
                return "{}://{}".format(info.data.get("connector_async"), v)
        return "{}://{}:{}@{}:{}/{}?charset={}".format(
            info.data.get("connector_async"),
            info.data.get("user"),
            info.data.get("password"),
            info.data.get("server"),
            info.data.get("port"),
            info.data.get("name"),
            info.data.get("charset"),
        )
