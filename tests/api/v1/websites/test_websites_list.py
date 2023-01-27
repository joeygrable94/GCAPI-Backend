from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_new_user, get_current_user_tokens
from tests.utils.websites import create_random_website

from app.api.errors import ErrorCode
from app.db.schemas import WebsiteRead
from app.db.schemas.user import UserAdmin
from app.security.auth.manager import AuthManager

pytestmark = pytest.mark.asyncio


async def test_list_websites_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsiteRead = await create_random_website(db_session)
    entry_2: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get("websites/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) > 1
    for entry in all_entries:
        assert "domain" in entry
        assert "is_secure" in entry
        if entry["domain"] == entry_1.domain:
            assert entry["domain"] == entry_1.domain
            assert entry["is_secure"] == entry_1.is_secure
        if entry["domain"] == entry_2.domain:
            assert entry["domain"] == entry_2.domain
            assert entry["is_secure"] == entry_2.is_secure


async def test_list_websites_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin
    a_user_password: str
    a_user, a_user_password = await create_new_user(user_auth)
    a_user_access_header = await get_current_user_tokens(
        client, a_user.email, a_user_password
    )
    a_token: str = a_user_access_header["access_token"]
    entry_1: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    entry_2: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    response: Response = await client.get(
        "websites/", headers={"Authorization": f"Bearer {a_token}"}
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
