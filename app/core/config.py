from functools import lru_cache
from os import environ
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv
from pydantic import AnyUrl, BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):

    # APP
    PROJECT_NAME: str = environ.get("PROJECT_NAME", "FastAPI")
    PROJECT_VERSION: str = environ.get("PROJECT_VERSION", "0.0.1")
    DEBUG_MODE: bool = bool(environ.get("APP_DEBUG", True))
    LOGGING_LEVEL: str = environ.get("BACKEND_LOG_LEVEL", "DEBUG").upper()
    LOGGER_NAME: str = environ.get("PROJECT_NAME", "debug")

    # API
    API_PREFIX_V1: str = "/api/v1"
    SERVER_NAME: str = environ.get("DOMAIN", "localhost:8888")

    # Security
    SECURITY_ALGORITHM: str = "HS256"
    ASGI_ID_HEADER_KEY: str = "x-request-id"
    SECRET_KEY: str = environ.get(
        "SECRET_KEY", "54295fb3ad6577bf6ec55fc8a4e2ce86b4a490b5f1666f1e871e94855f6dc0a7"
    )
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = environ.get(
        "BACKEND_CORS_ORIGINS", []
    )

    # Tokens: lifetime = seconds * minutes * hours * days = total seconds
    ACCESS_TOKEN_AUDIENCE: str = "auth:access"
    ACCESS_TOKEN_LIFETIME: int = 60 * 60 * 1 * 1  # 3600
    REFRESH_TOKEN_AUDIENCE: str = "auth:refresh"
    REFRESH_TOKEN_LIFETIME: int = 60 * 60 * 24 * 1  # 86400
    RESET_PASSWORD_TOKEN_AUDIENCE: str = "auth:reset"
    RESET_PASSWORD_TOKEN_LIFETIME: int = 60 * 60 * 1 * 1  # 3600
    VERIFY_USER_TOKEN_AUDIENCE: str = "auth:verify"
    VERIFY_USER_TOKEN_LIFETIME: int = 60 * 60 * 1 * 1  # 3600
    BASE_PRINCIPALS: Dict[str, str] = {
        "role:admin": "Administrators control administrative actions.",
        "role:user": "User controls things like logging in and out, \
            reset their password, etc.",
        "user:example@email.com": "Read information about the current user.",
    }

    # Database
    DB_ECHO_LOG: bool = False if bool(environ.get("APP_DEBUG", True)) else False
    DATABASE_SERVER: str = environ.get("DATABASE_SERVER", "")
    DATABASE_USER: str = environ.get("DATABASE_USER", "")
    DATABASE_PASSWORD: str = environ.get("DATABASE_PASSWORD", "")
    DATABASE_NAME: str = environ.get("DATABASE_NAME", "gcapidb")
    DATABASE_URI: Optional[Union[str, AnyUrl]] = environ.get("DATABASE_URI", None)
    ASYNC_DATABASE_URI: Optional[Union[str, AnyUrl]] = environ.get(
        "ASYNC_DATABASE_URI", None
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
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "./app/templates/email/build"
    EMAIL_PROVIDER_RESTRICTION: bool = bool(
        environ.get("EMAIL_PROVIDER_RESTRICTION", True)
    )
    ALLOWED_EMAIL_PROVIDER_LIST: List[str] = list(
        environ.get("ALLOWED_EMAIL_PROVIDER_LIST", ["getcommunity.com"])
    )
    EMAIL_TEST_USER: str = environ.get("SMTP_EMAIL_TEST_USER", "test@getcommunity.com")

    # Data
    FIRST_SUPERUSER: str = environ.get("FIRST_SUPERUSER", "admin@getcommunity.com")
    FIRST_SUPERUSER_PASSWORD: str = environ.get("FIRST_SUPERUSER_PASSWORD", "password")
    TEST_NORMAL_USER: str = environ.get("TEST_NORMAL_USER", "joey@getcommunity.com")
    TEST_NORMAL_USER_PASSWORD: str = environ.get(
        "TEST_NORMAL_USER_PASSWORD", "password"
    )
    USERS_OPEN_REGISTRATION: bool = bool(environ.get("USERS_OPEN_REGISTRATION", False))
    USERS_REQUIRE_VERIFICATION: bool = bool(
        environ.get("USERS_REQUIRE_VERIFICATION", True)
    )

    # Query Limits
    PASSWORD_LENGTH_MIN: int = 8
    PASSWORD_LENGTH_MAX: int = 100
    PAYLOAD_LIMIT: int = 2000000
    QUERY_DEFAULT_LIMIT_ROWS: int = int(environ.get("QUERY_DEFAULT_LIMIT_ROWS", 100))
    ACCEPTED_TYPES = ["png", "jpg", "jpeg", "gif", "csv", "xml", "json", "pdf"]
    # URL_DEFAULT_TTL=300
    # QUERY_DEFAULT_TTL=10
    # QUERY_CONCURRENT_LIMIT=10
    # QUERY_DEFAULT_WAITING_TIME=1

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

    @validator("DATABASE_URI", pre=True)
    def assemble_db_uri(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Union[str, AnyUrl]:  # pragma: no cover
        # .env provided connection string
        if isinstance(v, str):
            return v
        else:
            # no connection string provided
            # debug mode active
            if values.get("DEBUG_MODE"):
                return "sqlite:///./{}.db".format(values.get("DATABASE_NAME"))
            else:
                # default connection driver: mysql+pymysql
                return "mysql+pymysql://{}:{}@{}/{}?charset=UTF8MB4".format(
                    values.get("DATABASE_USER"),
                    values.get("DATABASE_PASSWORD"),
                    values.get("DATABASE_SERVER"),
                    values.get("DATABASE_NAME"),
                )

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_async_db_uri(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Union[str, AnyUrl]:  # pragma: no cover
        # .env provided connection string
        if isinstance(v, str):
            return v
        else:
            # no connection string provided
            # debug mode active
            if values.get("DEBUG_MODE"):
                return "sqlite+aiosqlite:///./{}.db".format(values.get("DATABASE_NAME"))
            else:
                # default asynchronous connection driver: mysql+aiomysql
                return "mysql+aiomysql://{}:{}@{}/{}?charset=UTF8MB4".format(
                    values.get("DATABASE_USER"),
                    values.get("DATABASE_PASSWORD"),
                    values.get("DATABASE_SERVER"),
                    values.get("DATABASE_NAME"),
                )

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

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


mode: Optional[str] = environ.get("APP_MODE")
settings: Settings = get_settings()
