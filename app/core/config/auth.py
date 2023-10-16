from os import environ
from typing import Dict, Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AuthSettings(BaseSettings):
    domain: str = environ.get("AUTH0_DOMAIN", "")
    audience: str = environ.get("AUTH0_API_AUDIENCE", "")
    scopes: Dict[str, str] = {
        "access:admin": "admins have unrestricted access to api actions",
        "access:manager": "manager have access to most actions administrators have and broaded access to clients' and users' data",  # noqa: E501
        "access:client": "clients have unique access to client scoped data",
        "access:employee": "employees may have access to only to specific clients they are granted permission to access",  # noqa: E501
        "access:user": "users have access to logging in and out and accessing their own data",  # noqa: E501
        "access:tests": "read test data",
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
    )
