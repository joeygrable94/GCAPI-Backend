from os import environ
from typing import Dict, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AuthSettings(BaseSettings):
    domain: str = environ.get("AUTH0_DOMAIN", "")
    audience: str = environ.get("AUTH0_API_AUDIENCE", "")
    scopes: Dict[str, str] = {
        "permission:test": "Grant GCAPI Permission to test the API using your email credentials.",  # noqa: E501
    }

    first_superuser: str = environ.get("AUTH0_FIRST_SUPERUSER", "joey@getcommunity.com")
    first_superuser_password: Optional[str] = environ.get(
        "AUTH0_FIRST_SUPERUSER_PASSWORD", None
    )

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AUTH0_",
        case_sensitive=False,
    )
