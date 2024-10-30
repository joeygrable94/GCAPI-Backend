from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .api import ApiModes, ApiSettings
from .auth import AuthSettings
from .cloud import CloudKeySettings
from .database import DatabaseSettings
from .mail import EmailSettings
from .sentry import SentrySettings

load_dotenv()


class Settings(BaseSettings):
    api: ApiSettings
    auth: AuthSettings
    db: DatabaseSettings
    email: EmailSettings
    sentry: SentrySettings
    cloud: CloudKeySettings


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        api=ApiSettings(),
        auth=AuthSettings(),
        db=DatabaseSettings(),
        email=EmailSettings(),
        sentry=SentrySettings(),
        cloud=CloudKeySettings(),
    )


settings: Settings = get_settings()


__all__: list[str] = [
    "ApiModes",
    "Settings",
    "get_settings",
    "settings",
]
