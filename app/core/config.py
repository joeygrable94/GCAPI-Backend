from functools import lru_cache
from os import environ
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr, validator
from sqlalchemy import URL

load_dotenv()


class Settings(BaseSettings):
    # APP
    PROJECT_NAME: str = environ.get("PROJECT_NAME", "FastAPI")
    PROJECT_VERSION: str = environ.get("TAG", "0.0.3")
    APP_MODE: str = environ.get("APP_MODE", "test")
    DEBUG_MODE: bool = bool(environ.get("APP_DEBUG", True))
    LOGGING_LEVEL: str = environ.get("BACKEND_LOG_LEVEL", "DEBUG").upper()
    LOGGER_NAME: str = environ.get("PROJECT_NAME", "debug")

    # API
    API_PREFIX_V1: str = "/api/v1"
    SERVER_NAME: str = environ.get("DOMAIN", "localhost")
    SERVER_NAME_STAGING: str = environ.get("DOMAIN_STAGING", "test.localhost")

    # Security
    ASGI_ID_HEADER_KEY: str = "x-request-id"
    SECRET_KEY: str = environ.get(
        "SECRET_KEY", "54295fb3ad6577bf6ec55fc8a4e2ce86b4a490b5f1666f1e871e94855f6dc0a7"
    )
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = [
        f"http://{SERVER_NAME}",
        f"http://{SERVER_NAME}:8888",
        f"http://{SERVER_NAME}:80",
        f"http://{SERVER_NAME}:8080",
        f"http://{SERVER_NAME}:4200",
        f"http://{SERVER_NAME}:3000",
        f"https://{SERVER_NAME}",
        f"https://{SERVER_NAME}:8888",
        f"https://{SERVER_NAME}:80",
        f"https://{SERVER_NAME}:8080",
        f"https://{SERVER_NAME}:4200",
        f"https://{SERVER_NAME}:3000",
        f"http://{SERVER_NAME_STAGING}",
        f"https://{SERVER_NAME_STAGING}",
        f"http://whoami.{SERVER_NAME_STAGING}",
        f"https://whoami.{SERVER_NAME_STAGING}",
        f"http://dbadmin.{SERVER_NAME_STAGING}",
        f"https://dbadmin.{SERVER_NAME_STAGING}",
        f"http://flower.{SERVER_NAME_STAGING}",
        f"https://flower.{SERVER_NAME_STAGING}",
    ]

    # Auth0
    AUTH0_DOMAIN: str = environ.get("AUTH0_DOMAIN", "")
    AUTH0_API_AUDIENCE: str = environ.get("AUTH0_API_AUDIENCE", "")
    BASE_PRINCIPALS: Dict[str, str] = {
        "access:admin": "admins have unrestricted access to api actions",
        "access:manager": "manager have access to most actions administrators have and broaded access to clients' and users' data",  # noqa: E501
        "access:client": "clients have unique access to client scoped data",
        "access:employee": "employees may have access to only to specific clients they are granted permission to access",  # noqa: E501
        "access:user": "users have access to logging in and out and accessing their own data",  # noqa: E501
        "access:tests": "read test data",
    }

    # Database
    DB_ECHO_LOG: bool = False if bool(environ.get("APP_DEBUG", True)) else False
    DATABASE_CONNECTOR: str = environ.get("DATABASE_CONNECTOR", "mysql+pymysql")
    DATABASE_ASYNC_CONNECTOR: str = environ.get(
        "DATABASE_ASYNC_CONNECTOR", "mysql+aiomysql"
    )
    DATABASE_USER: str = environ.get("DATABASE_USER", "root")
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD", "root")
    DATABASE_SERVER: str = environ.get("DATABASE_SERVER", "localhost")
    DATABASE_PORT: str = environ.get("DATABASE_PORT", "3306")
    DATABASE_NAME: str = environ.get("DATABASE_NAME", "database")
    DATABASE_CHARSET: str = environ.get("DATABASE_CHARSET", "UTF8MB4")
    DATABASE_URI: Union[str, URL] = environ.get("DATABASE_URI", "")
    ASYNC_DATABASE_URI: Union[str, URL] = environ.get("ASYNC_DATABASE_URI", "")

    # Redis
    REDIS_CONN_URI: str = environ.get("REDIS_CONN_URI", "redis://localhost:6379")

    # Worker
    SENTRY_DSN: Optional[str] = environ.get("SENTRY_DSN", None)

    # Mail
    SMTP_TLS: bool = bool(environ.get("SMTP_TLS", True))
    SMTP_SSL: bool = bool(environ.get("SMTP_SSL", False))
    SMTP_PORT: int = int(environ.get("SMTP_PORT", 587))
    SMTP_HOST: str = environ.get("SMTP_HOST", "smtp.gmail.com")
    SMTP_USER: str = environ.get("SMTP_USER", "")
    SMTP_PASSWORD: str = environ.get("SMTP_PASSWORD", "")
    EMAILS_ENABLED: bool = bool(environ.get("EMAILS_ENABLED", False))
    EMAILS_FROM_EMAIL: EmailStr = EmailStr(
        environ.get("SMTP_EMAILS_FROM_EMAIL", "noreply@example.com")
    )
    EMAILS_FROM_NAME: Optional[str] = environ.get("SMTP_EMAILS_FROM_NAME", None)
    EMAIL_TEMPLATES_DIR: str = "./app/templates/email/build"
    EMAIL_PROVIDER_RESTRICTION: bool = bool(
        environ.get("EMAIL_PROVIDER_RESTRICTION", True)
    )
    ALLOWED_EMAIL_PROVIDER_LIST: List[str] = list(
        environ.get("ALLOWED_EMAIL_PROVIDER_LIST", ["getcommunity.com"])
    )
    EMAIL_TEST_USER: str = environ.get("SMTP_EMAIL_TEST_USER", "test@getcommunity.com")

    # Data
    FIRST_SUPERUSER: str = environ.get("FIRST_SUPERUSER", "joey@getcommunity.com")
    FIRST_SUPERUSER_PASSWORD: Optional[str] = environ.get(
        "FIRST_SUPERUSER_PASSWORD", None
    )
    TEST_NORMAL_USER: str = environ.get("TEST_NORMAL_USER", "admin@getcommunity.com")
    TEST_NORMAL_USER_PASSWORD: Optional[str] = environ.get(
        "TEST_NORMAL_USER_PASSWORD", None
    )

    # Limits
    # Request Size = 2MB
    PAYLOAD_LIMIT: int = 2048000
    PAYLOAD_LIMIT_KB: int = 2000
    # Query
    QUERY_DEFAULT_LIMIT_OFFSET: int = int(environ.get("QUERY_DEFAULT_LIMIT_OFFSET", 0))
    QUERY_DEFAULT_LIMIT_ROWS: int = int(environ.get("QUERY_DEFAULT_LIMIT_ROWS", 100))
    QUERY_MAX_LIMIT_ROWS: int = int(environ.get("QUERY_MAX_LIMIT_ROWS", 1000))
    # Filetypes
    ACCEPTED_TYPES = [
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

    # Validators
    @validator("DATABASE_CONNECTOR", pre=True)
    def validate_database_connector(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_CONNECTOR not set")

    @validator("DATABASE_ASYNC_CONNECTOR", pre=True)
    def validate_database_async_connector(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_ASYNC_CONNECTOR not set")

    @validator("DATABASE_USER", pre=True)
    def validate_database_user(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_USER not set")

    @validator("DATABASE_PASSWORD", pre=True)
    def validate_database_password(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_PASSWORD not set")

    @validator("DATABASE_SERVER", pre=True)
    def validate_database_server(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_SERVER not set")

    @validator("DATABASE_PORT", pre=True)
    def validate_database_port(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_PORT not set")

    @validator("DATABASE_NAME", pre=True)
    def validate_database_name(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_NAME not set")

    @validator("DATABASE_CHARSET", pre=True)
    def validate_database_charset(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if isinstance(v, str):
            if len(v) > 0:
                return v
        raise ValueError("DATABASE_CHARSET not set")

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if values.get("APP_MODE") == "test":
            return "sqlite:///./test.db"
        if isinstance(v, str):
            if len(v) > 0:
                return "{}://{}".format(values.get("DATABASE_CONNECTOR"), v)
        return "{}://{}:{}@{}:{}/{}?charset={}".format(
            values.get("DATABASE_CONNECTOR"),
            values.get("DATABASE_USER"),
            values.get("DATABASE_PASSWORD"),
            values.get("DATABASE_SERVER"),
            values.get("DATABASE_PORT"),
            values.get("DATABASE_NAME"),
            values.get("DATABASE_CHARSET"),
        )

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_async_db_connection(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> Any:  # pragma: no cover
        if values.get("APP_MODE") == "test":
            return "sqlite+aiosqlite:///./test.db"
        if isinstance(v, str):
            if len(v) > 0:
                return "{}://{}".format(values.get("DATABASE_ASYNC_CONNECTOR"), v)
        return "{}://{}:{}@{}:{}/{}?charset={}".format(
            values.get("DATABASE_ASYNC_CONNECTOR"),
            values.get("DATABASE_USER"),
            values.get("DATABASE_PASSWORD"),
            values.get("DATABASE_SERVER"),
            values.get("DATABASE_PORT"),
            values.get("DATABASE_NAME"),
            values.get("DATABASE_CHARSET"),
        )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls: Any, v: Union[str, List[str]]
    ) -> Union[List[str], str]:  # pragma: no cover
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return ["*"]

    @validator("EMAILS_FROM_NAME")
    def assemble_emails_sent_from(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> str:  # pragma: no cover
        if not v:
            return values["PROJECT_NAME"]
        return v

    @validator("EMAILS_ENABLED", pre=True)
    def assemble_emails_enabled(
        cls: Any, v: Optional[bool], values: Dict[str, Any]
    ) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
            and values.get("SMTP_USER")
            and values.get("SMTP_PASSWORD")
        )

    @validator("FIRST_SUPERUSER_PASSWORD", pre=True)
    def assemble_first_superuser_password(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> str:
        if not v:
            raise ValueError("FIRST_SUPERUSER_PASSWORD not set")  # pragma: no cover
        return v

    @validator("TEST_NORMAL_USER_PASSWORD", pre=True)
    def assemble_test_normal_user_password(
        cls: Any, v: Optional[str], values: Dict[str, Any]
    ) -> str:
        if not v:
            raise ValueError("TEST_NORMAL_USER_PASSWORD not set")  # pragma: no cover
        return v

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings() -> Settings:
    config_name: str = environ.get(  # noqa: F841
        "APP_MODE", "development"
    )  # pragma: no cover  # noqa: E501
    return Settings()


settings: Settings = get_settings()
