from typing import Any, Dict

from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import UserAlreadyExists
from app.core.config import settings
from app.core.security.manager import UserManager
from app.db.schemas import ID, UP, UserCreate, UserRead, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string


async def create_random_user(
    db_session: AsyncSession,
) -> UserRead:
    user_manager: UserManager = UserManager(session=db_session)
    email: str = random_email()
    password: str = random_lower_string()
    user: Any = await user_manager.create(
        user_create=UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
    )
    return user


async def get_superuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    response: Response = await client.post(
        "auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.FIRST_SUPERUSER,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
        },
    )
    auth_data: Dict[str, Any] = response.json()
    auth_token: str = auth_data["access_token"]
    auth_header: Dict[str, str] = {"Authorization": f"Bearer {auth_token}"}
    return auth_header


async def get_testuser_token_headers(client: AsyncClient) -> Dict[str, str]:
    response: Response = await client.post(
        "auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": settings.TEST_NORMAL_USER,
            "password": settings.TEST_NORMAL_USER_PASSWORD,
        },
    )
    auth_data: Dict[str, Any] = response.json()
    auth_token: str = auth_data["access_token"]
    auth_header: Dict[str, str] = {"Authorization": f"Bearer {auth_token}"}
    return auth_header


async def get_user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> Dict[str, str]:
    response: Response = await client.post(
        "auth/jwt/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": email, "password": password},
    )
    auth_data: Dict[str, Any] = response.json()
    auth_token: str = auth_data["access_token"]
    auth_headers: Dict[str, str] = {"Authorization": f"Bearer {auth_token}"}
    return auth_headers


async def authentication_token_from_email(
    *,
    client: AsyncClient,
    email: str,
    user_manager: UserManager[UP, ID],
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password: str = settings.TEST_NORMAL_USER_PASSWORD
    user: Any = await user_manager.get_by_email(user_email=email)
    if not user:
        try:
            user = await user_manager.create(
                user_create=UserCreate(email=email, password=password)
            )
        except UserAlreadyExists:
            pass
    else:
        user = await user_manager.update(
            user_update=UserUpdate(password=password), user=user
        )
    return await get_user_authentication_headers(
        client=client, email=email, password=password
    )
