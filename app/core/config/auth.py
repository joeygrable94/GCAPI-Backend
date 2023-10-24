from os import environ
from typing import Dict

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AuthSettings(BaseSettings):
    domain: str = environ.get("AUTH0_DOMAIN", "")
    audience: str = environ.get("AUTH0_API_AUDIENCE", "")
    scopes: Dict[str, str] = {
        "permission:test": "Grant GCAPI Permission to test the API using your email credentials.",  # noqa: E501
    }

    first_admin: str = environ.get("AUTH0_FIRST_ADMIN", "")
    first_admin_password: str = environ.get("AUTH0_FIRST_ADMIN_PASSWORD", "")
    first_admin_auth_id: str = environ.get("AUTH0_FIRST_ADMIN_AUTH_ID", "")
    first_manager: str = environ.get("AUTH0_FIRST_MANAGER", "")
    first_manager_password: str = environ.get("AUTH0_FIRST_MANAGER_PASSWORD", "")
    first_manager_auth_id: str = environ.get("AUTH0_FIRST_MANAGER_AUTH_ID", "")
    first_employee: str = environ.get("AUTH0_FIRST_EMPLOYEE", "")
    first_employee_password: str = environ.get("AUTH0_FIRST_EMPLOYEE_PASSWORD", "")
    first_employee_auth_id: str = environ.get("AUTH0_FIRST_EMPLOYEE_AUTH_ID", "")
    first_client_a: str = environ.get("AUTH0_FIRST_CLIENT_A", "")
    first_client_a_password: str = environ.get("AUTH0_FIRST_CLIENT_A_PASSWORD", "")
    first_client_a_auth_id: str = environ.get("AUTH0_FIRST_CLIENT_A_AUTH_ID", "")
    first_client_b: str = environ.get("AUTH0_FIRST_CLIENT_B", "")
    first_client_b_password: str = environ.get("AUTH0_FIRST_CLIENT_B_PASSWORD", "")
    first_client_b_auth_id: str = environ.get("AUTH0_FIRST_CLIENT_B_AUTH_ID", "")
    first_user_verified: str = environ.get("AUTH0_FIRST_USER_VERIFIED", "")
    first_user_verified_password: str = environ.get(
        "AUTH0_FIRST_USER_VERIFIED_PASSWORD", ""
    )
    first_user_verified_auth_id: str = environ.get(
        "AUTH0_FIRST_USER_VERIFIED_AUTH_ID", ""
    )
    first_user_unverified: str = environ.get("AUTH0_FIRST_USER_UNVERIFIED", "")
    first_user_unverified_password: str = environ.get(
        "AUTH0_FIRST_USER_UNVERIFIED_PASSWORD", ""
    )
    first_user_unverified_auth_id: str = environ.get(
        "AUTH0_FIRST_USER_UNVERIFIED_AUTH_ID", ""
    )

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AUTH0_",
        case_sensitive=False,
    )
