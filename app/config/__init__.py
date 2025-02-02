from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .api import ApiModes, ApiSettings
from .cloud import CloudKeySettings
from .database import DatabaseSettings
from .mail import EmailSettings

load_dotenv()


class Settings(BaseSettings):
    api: ApiSettings
    db: DatabaseSettings
    email: EmailSettings
    cloud: CloudKeySettings


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        api=ApiSettings(),
        db=DatabaseSettings(),
        email=EmailSettings(),
        cloud=CloudKeySettings(),
    )


settings: Settings = get_settings()


__all__: list[str] = [
    "ApiModes",
    "Settings",
    "get_settings",
    "settings",
]
