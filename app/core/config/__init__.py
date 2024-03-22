from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .api import ApiSettings
from .auth import AuthSettings
from .cloud import CloudKeySettings
from .database import DatabaseSettings
from .mail import EmailSettings
from .redis import RedisSettings
from .worker import WorkerSettings

load_dotenv()


class Settings(BaseSettings):
    api: ApiSettings
    auth: AuthSettings
    db: DatabaseSettings
    email: EmailSettings
    redis: RedisSettings
    worker: WorkerSettings
    cloud: CloudKeySettings


@lru_cache()
def get_settings() -> Settings:
    return Settings(
        api=ApiSettings(),
        auth=AuthSettings(),
        db=DatabaseSettings(),
        email=EmailSettings(),
        redis=RedisSettings(),
        worker=WorkerSettings(),
        cloud=CloudKeySettings(),
    )


settings: Settings = get_settings()
