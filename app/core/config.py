from functools import lru_cache
from os import environ
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, validator
from sqlalchemy import URL

load_dotenv()


class Settings(BaseSettings):
    # APP
    PROJECT_NAME: str = environ.get("PROJECT_NAME", "FastAPI")
    PROJECT_VERSION: str = environ.get("TAG", "0.0.1")
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
        "access:admin": "Administrators control administrative actions.",
        "access:client": "User is a client with unique access to their data.",
        "access:user": "User controls things like logging in and out and accessing the api.",  # noqa: E501
        "access:tests": "Read test data.",
    }

    # Database
    DB_ECHO_LOG: bool = False if bool(environ.get("APP_DEBUG", True)) else False
    DATABASE_URI: Union[str, URL] = environ.get("DATABASE_URI", "sqlite:///./app.db")
    ASYNC_DATABASE_URI: Union[str, URL] = environ.get(
        "ASYNC_DATABASE_URI", "sqlite+aiosqlite:///./app.db"
    )

    # Redis
    REDIS_CONN_URI: str = environ.get("REDIS_CONN_URI", "redis://localhost:6379")

    # Worker
    SENTRY_DSN: Optional[str] = environ.get("SENTRY_DSN", None)
    CELERY_WORKER_BROKER: str = environ.get("CELERY_WORKER_BROKER", "/0")
    CELERY_WORKER_BACKEND: str = environ.get("CELERY_WORKER_BACKEND", "/0")
    CELERY_WORKER_TASK_QUEUE: str = environ.get(
        "CELERY_WORKER_TASK_QUEUE", "main-queue"
    )

    # Mail
    SMTP_TLS: Union[str, bool] = bool(environ.get("SMTP_TLS", True))
    SMTP_SSL: Union[str, bool] = bool(environ.get("SMTP_SSL", False))
    SMTP_PORT: Optional[Union[str, int, None]] = environ.get("SMTP_PORT", 587)
    SMTP_HOST: Optional[str] = environ.get("SMTP_HOST", "smtp.gmail.com")
    SMTP_USER: str = environ.get("SMTP_USER", "")
    SMTP_PASSWORD: str = environ.get("SMTP_PASSWORD", "")
    EMAILS_ENABLED: Optional[Union[str, bool]] = environ.get("EMAILS_ENABLED", None)
    EMAILS_FROM_EMAIL: Optional[str] = environ.get(
        "SMTP_EMAILS_FROM_EMAIL", "noreply@example.com"
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
    # Request Size
    PAYLOAD_LIMIT: int = 2000000
    # Query
    QUERY_DEFAULT_LIMIT_OFFSET: int = int(environ.get("QUERY_DEFAULT_LIMIT_OFFSET", 0))
    QUERY_DEFAULT_LIMIT_ROWS: int = int(environ.get("QUERY_DEFAULT_LIMIT_ROWS", 100))
    QUERY_MAX_LIMIT_ROWS: int = int(environ.get("QUERY_MAX_LIMIT_ROWS", 1000))
    # Filetypes
    ACCEPTED_TYPES = ["png", "jpg", "jpeg", "gif", "csv", "xml", "json", "pdf"]

    # Validators
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
    return Settings()


mode: Optional[str] = environ.get("APP_MODE")
settings: Settings = get_settings()
