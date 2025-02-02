from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class CloudKeySettings(BaseSettings):
    # IP Info
    ipinfo: str | None = environ.get("CLOUDKEY_IPINFO", None)
    # Google Cloud
    googleapi: str | None = environ.get("CLOUDKEY_GOOGLE_API", None)

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CLOUDKEY_",
        case_sensitive=False,
        extra="ignore",
    )
