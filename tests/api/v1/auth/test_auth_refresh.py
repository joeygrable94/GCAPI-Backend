from typing import Dict

import pytest
from httpx import AsyncClient, Response
from tests.utils.users import get_current_user_tokens

pytestmark = pytest.mark.asyncio


async def test_auth_refresh_superuser_access(client: AsyncClient) -> None:
    su_tokens: Dict[str, str] = await get_current_user_tokens(client)
    a_tok: str = su_tokens["access_token"]
    a_tok_csrf: str = su_tokens["access_token_csrf"]
    r_tok: str = su_tokens["refresh_token"]
    r_tok_csrf: str = su_tokens["refresh_token_csrf"]
    refresh_headers: Dict[str, str] = {"Authorization": f"Bearer {r_tok}"}
    response: Response = await client.post("auth/refresh", headers=refresh_headers)
    data: Dict[str, str] = response.json()
    assert response.status_code == 200
    assert data["token_type"] == "bearer"
    assert data["access_token"] != ""
    assert data["access_token"] != a_tok
    assert data["access_token_csrf"] != a_tok_csrf
    assert data["refresh_token"] != ""
    assert data["refresh_token"] != r_tok
    assert data["refresh_token_csrf"] != r_tok_csrf
