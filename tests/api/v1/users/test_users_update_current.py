from time import sleep
from typing import Any, Dict, Tuple

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_random_user
from tests.utils.utils import random_lower_string

from app.api.errors import ErrorCode
from app.core.config import settings
from app.db.schemas import UserRead, UserUpdate
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_update_current_superuser(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token_headers: Dict[str, str]
    current_user, current_token_headers = current_superuser
    update_dict = UserUpdate(is_verified=True)
    response: Response = await client.patch(
        "users/me", headers=current_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_user["email"] == current_user.email
    assert current_user.is_verified is True
    assert updated_user["is_verified"] is True


async def test_update_current_superuser_email_taken(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token: Dict[str, str]
    current_user, current_token = current_superuser
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=settings.TEST_NORMAL_USER,
    )
    response: Response = await client.patch(
        "users/me", headers=current_token, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"] == ErrorCode.USER_ALREADY_EXISTS


# async def test_update_current_superuser_email_too_short():
# async def test_update_current_superuser_email_invalid():
# async def test_update_current_superuser_email_invalid_provider():


async def test_update_current_superuser_password_too_short(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token: Dict[str, str]
    current_user, current_token = current_superuser
    update_dict = UserUpdate(password="short")
    response: Response = await client.patch(
        "users/me", headers=current_token, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MIN} or more characters"
    )


async def test_update_current_superuser_password_too_long(
    client: AsyncClient,
    current_superuser: Tuple[UserAdmin | UserRead, Dict[str, str]],
) -> None:
    current_user: UserAdmin | UserRead
    current_token: Dict[str, str]
    current_user, current_token = current_superuser
    new_pass: str = random_lower_string() * 10
    update_dict = UserUpdate(password=new_pass)
    response: Response = await client.patch(
        "users/me", headers=current_token, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"]["code"] == ErrorCode.USER_PASSWORD_INVALID
    assert (
        updated_user["detail"]["reason"]
        == f"Password must contain {settings.PASSWORD_LENGTH_MAX} or less characters"
    )


async def test_update_current_testuser(
    client: AsyncClient,
    current_testuser: Tuple[UserRead, Dict[str, str]],
) -> None:
    current_user: UserRead
    current_token_headers: Dict[str, str]
    current_user, current_token_headers = current_testuser
    update_dict = UserUpdate(password="NEWvalidPassw0rd")
    sleep(1)
    response: Response = await client.patch(
        "users/me", headers=current_token_headers, json=update_dict.dict()
    )
    updated_user: UserRead = UserRead(**response.json())
    assert 200 <= response.status_code < 300
    assert not current_user.updated_on == updated_user.updated_on


async def test_update_current_testuser_email_taken(
    client: AsyncClient,
    user_auth: AuthManager,
    current_testuser: Tuple[UserRead, Dict[str, str]],
) -> None:
    a_user: UserAdmin = await create_random_user(user_auth)
    current_user: UserRead
    current_token_headers: Dict[str, str]
    current_user, current_token_headers = current_testuser
    update_dict = UserUpdate(
        password="NEWvalidPassw0rd",
        email=a_user.email,
    )
    response: Response = await client.patch(
        "users/me", headers=current_token_headers, json=update_dict.dict()
    )
    updated_user: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_user["detail"] == ErrorCode.USER_ALREADY_EXISTS
