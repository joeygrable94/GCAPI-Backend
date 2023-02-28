from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_random_user

from app.api.errors import ErrorCode
from app.db.schemas.user import UserPrincipals
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_list_users_as_superuser(
    client: AsyncClient,
    user_auth: AuthManager,
    superuser_token_headers: Dict[str, str],
) -> None:
    user_1: UserPrincipals = await create_random_user(user_auth)
    user_2: UserPrincipals = await create_random_user(user_auth)
    response: Response = await client.get("users/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_users: Any = response.json()
    assert len(all_users) > 1
    for api_user in all_users:
        assert "email" in api_user
        assert "hashed_password" not in api_user
        if api_user["email"] == user_1.email:
            assert api_user["email"] == user_1.email
        if api_user["email"] == user_2.email:
            assert api_user["email"] == user_2.email


async def test_list_users_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
    testuser_token_headers: Dict[str, str],
) -> None:
    user_1: UserPrincipals = await create_random_user(user_auth)  # noqa: F841
    user_2: UserPrincipals = await create_random_user(user_auth)  # noqa: F841
    response: Response = await client.get("users/", headers=testuser_token_headers)
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
