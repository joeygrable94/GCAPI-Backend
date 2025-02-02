from functools import lru_cache
from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class CsrfSettings(BaseSettings):
    csrf_header_key: str = "x-csrf-token"
    csrf_name_key: str = "gcapi-csrf-token"
    csrf_salt: str = "lXB*IUFLCcbz45Swnda92laS-DJG{rUX^ASz5Wzz;5sP"
    csrf_secret_key: str = environ.get(
        "API_CSRF_KEY",
        "fb4cd9547245b656a5a44441eebd5960432c95d9c45970be0d7442f91bf64366",
    )
    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="API_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_csrf_settings() -> CsrfSettings:
    return CsrfSettings()


csrf_settings: CsrfSettings = get_csrf_settings()


__all__: list[str] = [
    "CsrfSettings",
    "get_csrf_settings",
    "csrf_settings",
]
