from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import create_new_user, get_current_user_tokens

from app.core.config import settings
from app.db.schemas.user import UserAdmin
from app.security import AuthManager

pytestmark = pytest.mark.asyncio


async def test_auth_logout_superuser_access(client: AsyncClient) -> None:
    super_user_tokens: Dict[str, str] = await get_current_user_tokens(client)
    a_tok: str = super_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/logout", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_logout_testuser_access(client: AsyncClient) -> None:
    super_user_tokens: Dict[str, str] = await get_current_user_tokens(
        client, settings.TEST_NORMAL_USER, settings.TEST_NORMAL_USER_PASSWORD
    )
    a_tok: str = super_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/logout", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_logout_random_user(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin
    a_user_pass: str
    a_user, a_user_pass = await create_new_user(user_auth)
    random_user_tokens: Dict[str, str] = await get_current_user_tokens(
        client, username=a_user.email, password=a_user_pass
    )
    a_tok: str = random_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/logout", headers=access_headers)
    data: Dict[str, Any] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""
