from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_new_user, get_current_user_tokens
from tests.utils.websites import create_random_website

from app.api.errors import ErrorCode
from app.db.repositories import WebsiteRepository
from app.db.schemas import WebsiteRead
from app.db.schemas.user import UserPrincipals
from app.security.auth.manager import AuthManager

pytestmark = pytest.mark.asyncio


async def test_delete_website_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{entry.id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    repo: WebsiteRepository = WebsiteRepository(db_session)
    data_not_found: Optional[Any] = await repo.read_by("domain", entry.domain)
    assert data_not_found is None


async def test_delete_website_by_id_as_testuser(
    client: AsyncClient,
    db_session: AsyncSession,
    user_auth: AuthManager,
) -> None:
    a_user: UserPrincipals
    a_user_password: str
    a_user, a_user_password = await create_new_user(user_auth)
    a_user_access_header = await get_current_user_tokens(
        client, a_user.email, a_user_password
    )
    a_token: str = a_user_access_header["access_token"]
    entry: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{entry.id}",
        headers={"Authorization": f"Bearer {a_token}"},
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
