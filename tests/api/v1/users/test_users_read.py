from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_random_user

from app.api.errors import ErrorCode
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_read_user_by_id_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    user: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.get(
        f"users/{user.id}",
        headers=superuser_token_headers,
    )
    fetched_user: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert fetched_user["id"] == str(user.id)
    existing_user: Any = await user_auth.users.read_by_email(user.email)
    assert existing_user
    assert existing_user.email == fetched_user["email"]


async def test_read_user_by_id_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    user: UserAdmin = await create_random_user(user_auth)
    response: Response = await client.get(
        f"users/{user.id}",
        headers=testuser_token_headers,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
