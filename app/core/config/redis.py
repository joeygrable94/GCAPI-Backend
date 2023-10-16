from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RedisSettings(BaseSettings):
    uri: str = environ.get("REDIS_URI", "redis://localhost:6379")

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
    )
