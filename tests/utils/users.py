from typing import Any, Dict, Tuple

from httpx import AsyncClient, Response
from tests.utils.utils import random_email, random_lower_string

from app.core.config import settings
from app.db.schemas import UserCreate, UserRead, UserAdmin
from app.db.tables import User
from app.security import AuthManager


async def create_random_user(
    user_auth: AuthManager,
) -> UserAdmin:
    email: str = random_email()
    password: str = random_lower_string()
    user: User = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
    )
    return UserAdmin.from_orm(user)


async def create_new_user(
    user_auth: AuthManager,
) -> Tuple[UserAdmin, str]:
    email: str = random_email()
    password: str = random_lower_string()
    user: User = await user_auth.users.create(
        schema=UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=True,
        )
    )
    return UserAdmin.from_orm(user), password


async def get_current_user_tokens(
    client: AsyncClient,
    username: str = settings.FIRST_SUPERUSER,
    password: str = settings.FIRST_SUPERUSER_PASSWORD,
) -> Dict[str, str]:
    response: Response = await client.post(
        "auth/access",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": f"{username}",
            "password": f"{password}",
        },
    )
    auth_data: Dict[str, str] = response.json()
    return auth_data


async def get_current_user(
    client: AsyncClient,
    auth_header: Dict[str, str],
) -> Tuple[UserAdmin | UserRead, Dict[str, str]]:
    response: Response = await client.get(
        "users/me",
        headers=auth_header,
    )
    user_data: Dict[str, Any] = response.json()
    current_user: UserAdmin | UserRead
    if user_data.get("principals"):
        current_user = UserAdmin(**user_data)
    else:
        current_user = UserRead(**user_data)
    return current_user, auth_header
