from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .api import ApiSettings
from .auth import AuthSettings
from .celery import CelerySettings
from .database import DatabaseSettings
from .mail import EmailSettings
from .redis import RedisSettings

load_dotenv()


class Settings(BaseSettings):
    api: ApiSettings
    auth: AuthSettings
    db: DatabaseSettings
    email: EmailSettings
    redis: RedisSettings
    celery: CelerySettings


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        api=ApiSettings(),
        auth=AuthSettings(),
        db=DatabaseSettings(),
        email=EmailSettings(),
        redis=RedisSettings(),
        celery=CelerySettings(),
    )


settings: Settings = get_settings()
