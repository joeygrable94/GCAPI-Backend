from functools import lru_cache
from os import environ

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ClerkSettings(BaseSettings):
    secret_key: str = environ.get("CLERK_SECRET_KEY", "")
    jwks_url: str = environ.get("CLERK_JWKS_URL", "")
    issuer: str = environ.get("CLERK_ISSUER", "")
    pem_public_key: str = environ.get("CLERK_PEM_PUBLIC_KEY", "")

    first_admin: str = environ.get("CLERK_FIRST_ADMIN", "")
    first_admin_password: str = environ.get("CLERK_FIRST_ADMIN_PASSWORD", "")
    first_admin_auth_id: str = environ.get("CLERK_FIRST_ADMIN_CLERK_ID", "")
    first_admin_picture: str = environ.get(
        "CLERK_FIRST_ADMIN_PICTURE", "https://www.gravatar.com/avatar/?d=identicon"
    )
    first_manager: str = environ.get("CLERK_FIRST_MANAGER", "")
    first_manager_password: str = environ.get("CLERK_FIRST_MANAGER_PASSWORD", "")
    first_manager_auth_id: str = environ.get("CLERK_FIRST_MANAGER_CLERK_ID", "")
    first_manager_picture: str = environ.get(
        "CLERK_FIRST_MANAGER_PICTURE", "https://www.gravatar.com/avatar/?d=identicon"
    )
    first_employee: str = environ.get("CLERK_FIRST_EMPLOYEE", "")
    first_employee_password: str = environ.get("CLERK_FIRST_EMPLOYEE_PASSWORD", "")
    first_employee_auth_id: str = environ.get("CLERK_FIRST_EMPLOYEE_CLERK_ID", "")
    first_employee_picture: str = environ.get(
        "CLERK_FIRST_EMPLOYEE_PICTURE", "https://www.gravatar.com/avatar/?d=identicon"
    )
    first_client_a: str = environ.get("CLERK_FIRST_CLIENT_A", "")
    first_client_a_password: str = environ.get("CLERK_FIRST_CLIENT_A_PASSWORD", "")
    first_client_a_auth_id: str = environ.get("CLERK_FIRST_CLIENT_A_CLERK_ID", "")
    first_client_a_picture: str = environ.get(
        "CLERK_FIRST_CLIENT_A_PICTURE", "https://www.gravatar.com/avatar/?d=identicon"
    )
    first_client_b: str = environ.get("CLERK_FIRST_CLIENT_B", "")
    first_client_b_password: str = environ.get("CLERK_FIRST_CLIENT_B_PASSWORD", "")
    first_client_b_auth_id: str = environ.get("CLERK_FIRST_CLIENT_B_CLERK_ID", "")
    first_client_b_picture: str = environ.get(
        "CLERK_FIRST_CLIENT_B_PICTURE", "https://www.gravatar.com/avatar/?d=identicon"
    )
    first_user_verified: str = environ.get("CLERK_FIRST_USER_VERIFIED", "")
    first_user_verified_password: str = environ.get(
        "CLERK_FIRST_USER_VERIFIED_PASSWORD", ""
    )
    first_user_verified_auth_id: str = environ.get(
        "CLERK_FIRST_USER_VERIFIED_CLERK_ID", ""
    )
    first_user_unverified: str = environ.get("CLERK_FIRST_USER_UNVERIFIED", "")
    first_user_unverified_password: str = environ.get(
        "CLERK_FIRST_USER_UNVERIFIED_PASSWORD", ""
    )
    first_user_unverified_auth_id: str = environ.get(
        "CLERK_FIRST_USER_UNVERIFIED_CLERK_ID", ""
    )

    # pydantic settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="CLERK_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_clerk_settings() -> ClerkSettings:
    return ClerkSettings()


clerk_settings: ClerkSettings = get_clerk_settings()


__all__: list[str] = [
    "ClerkSettings",
    "get_clerk_settings",
    "clerk_settings",
]
