from functools import lru_cache
from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class EncryptionSettings(BaseSettings):
    rsa_public_key: str = environ.get("API_RSA_PUBLIC_KEY", "")
    rsa_private_key: str = environ.get("API_RSA_PRIVATE_KEY", "")
    encryption_salt: str = environ.get(
        "API_ENCRYPTION_SALT", "aUW1+hREL5XAc3qFEJAR7trNW+yYAzOxoqvzsys0Zvs="
    )
    encryption_key: str = environ.get(
        "API_ENCRYPTION_KEY",
        "hNaZZH07R5yxXsbE1mEVPERNOJZwyb/O+jlhqonG2I0=",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="API_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_encryption_settings() -> EncryptionSettings:
    return EncryptionSettings()


encryption_settings: EncryptionSettings = get_encryption_settings()


__all__: list[str] = [
    "EncryptionSettings",
    "get_encryption_settings",
    "encryption_settings",
]
