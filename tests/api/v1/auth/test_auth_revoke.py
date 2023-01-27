from typing import Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import get_current_user_tokens

from app.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_auth_revoke_superuser_access(client: AsyncClient) -> None:
    super_user_tokens: Dict[str, str] = await get_current_user_tokens(client)
    a_tok: str = super_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/revoke", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""


async def test_auth_revoke_testuser_access(client: AsyncClient) -> None:
    test_user_tokens: Dict[str, str] = await get_current_user_tokens(
        client,
        username=settings.TEST_NORMAL_USER,
        password=settings.TEST_NORMAL_USER_PASSWORD,
    )
    a_tok: str = test_user_tokens["access_token"]
    access_headers: Dict[str, str] = {"Authorization": f"Bearer {a_tok}"}
    response: Response = await client.delete("auth/revoke", headers=access_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] == ""
    assert data["access_token_csrf"] == ""
    assert data["refresh_token"] == ""
    assert data["refresh_token_csrf"] == ""
