from typing import Dict

from httpx import AsyncClient, Response

from app.core.config import settings

"""
async def create_random_user(
    user_auth: AuthManager,
) -> UserRead:
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
    return UserRead.from_orm(user)
"""


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


"""
async def get_current_user(
    client: AsyncClient,
    auth_header: Dict[str, str],
) -> Tuple[UserRead, Dict[str, str]]:
    response: Response = await client.get(
        "users/me",
        headers=auth_header,
    )
    user_data: Dict[str, Any] = response.json()
    current_user: UserRead = UserRead(**user_data)
    return current_user, auth_header
"""
