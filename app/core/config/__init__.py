import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv

load_dotenv()

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):

    DEBUG_MODE: bool = bool(os.environ.get("APP_DEBUG", True))

    # LOG: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOGGING_LEVEL: str = "DEBUG"
    LOGGER_NAME: str = os.environ.get("STACK_NAME", "debug")

    PROJECT_NAME: str = os.environ.get("PROJECT_NAME", "FastAPI")
    PROJECT_VERSION: str = os.environ.get("PROJECT_VERSION", "0.0.1")

    API_PREFIX_V1: str = "/api/v1"

    SERVER_NAME: str = os.environ.get("DOMAIN", "localhost")
    SERVER_HOST: str = os.environ.get("DOMAIN_HOST", "http://localhost")
    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY", "54295fb3ad6577bf6ec55fc8a4e2ce86b4a490b5f1666f1e871e94855f6dc0a7"
    )
    # seconds * minutes * hours * days = total seconds
    ACCESS_TOKEN_LIFETIME: int = 60 * 60 * 1 * 1  # = 3600
    RESET_PASSWORD_TOKEN_AUDIENCE: str = "users:reset"
    VERIFY_USER_TOKEN_AUDIENCE: str = "users:verify"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = os.environ.get(
        "BACKEND_CORS_ORIGINS", []
    )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls: Any, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SENTRY_DSN: Optional[str] = os.environ.get("SENTRY_DSN", "")

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls: Any, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    DB_ECHO_LOG: bool = False if bool(os.environ.get("APP_DEBUG", True)) else False
    DATABASE_SERVER: str = os.environ.get("DATABASE_SERVER", "localhost")
    DATABASE_PORT: int = int(os.environ.get("DATABASE_PORT", 3306))
    DATABASE_USER: str = os.environ.get("DATABASE_USER", "root")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "root")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "app.db")
    DATABASE_URI: Optional[str] = os.environ.get(
        "DATABASE_URI",
        "mysql+pymysql://{}:{}@{}:{}/{}?charset=UTF8MB4".format(
            DATABASE_USER,
            DATABASE_PASSWORD,
            DATABASE_SERVER,
            DATABASE_PORT,
            DATABASE_NAME,
        ),
    )
    ASYNC_DATABASE_URI: Optional[str] = os.environ.get(
        "DATABASE_URI",
        "mysql+aiomysql://{}:{}@{}:{}/{}?charset=UTF8MB4".format(
            DATABASE_USER,
            DATABASE_PASSWORD,
            DATABASE_SERVER,
            DATABASE_PORT,
            DATABASE_NAME,
        ),
    )

    C_BROKER_URI: str = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
    C_BACKEND_URI: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379"
    )

    SMTP_TLS: Union[str, bool] = bool(os.environ.get("SMTP_TLS", True))
    SMTP_PORT: Optional[Union[str, int, None]] = os.environ.get("SMTP_PORT", None)
    SMTP_HOST: Optional[str] = os.environ.get("SMTP_HOST", None)
    SMTP_USER: Optional[str] = os.environ.get("SMTP_USER", None)
    SMTP_PASSWORD: Optional[str] = os.environ.get("SMTP_PASSWORD", None)
    EMAILS_FROM_EMAIL: Optional[str] = os.environ.get("SMTP_EMAILS_FROM_EMAIL", None)
    EMAILS_FROM_NAME: Optional[str] = os.environ.get("SMTP_EMAILS_FROM_NAME", None)

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls: Any, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/templates/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls: Any, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_PROVIDER_RESTRICTION: bool = bool(
        os.environ.get("EMAIL_PROVIDER_RESTRICTION", True)
    )
    ALLOWED_EMAIL_PROVIDER_LIST: List[Any] = list(
        os.environ.get("ALLOWED_EMAIL_PROVIDER_LIST", ["getcommunity.com"])
    )

    EMAIL_TEST_USER: str = os.environ.get(
        "SMTP_EMAIL_TEST_USER", "test@getcommunity.com"
    )
    FIRST_SUPERUSER: str = os.environ.get("FIRST_SUPERUSER", "admin@getcommunity.com")
    FIRST_SUPERUSER_PASSWORD: str = os.environ.get(
        "FIRST_SUPERUSER_PASSWORD", "password"
    )
    TEST_NORMAL_USER: str = os.environ.get("TEST_NORMAL_USER", "joey@getcommunity.com")
    TEST_NORMAL_USER_PASSWORD: str = os.environ.get(
        "TEST_NORMAL_USER_PASSWORD", "password"
    )
    USERS_OPEN_REGISTRATION: bool = bool(
        os.environ.get("USERS_OPEN_REGISTRATION", False)
    )
    USERS_REQUIRE_VERIFICATION: bool = bool(
        os.environ.get("USERS_REQUIRE_VERIFICATION", False)
    )

    # Query parameters.
    PER_PAGE_MAX_COUNT: int = int(os.environ.get("PER_PAGE_MAX_COUNT", 100))

    class Config:
        case_sensitive: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


mode: Optional[str] = os.environ.get("APP_MODE")
settings: Settings = get_settings()
