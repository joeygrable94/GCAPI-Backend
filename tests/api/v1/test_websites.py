from typing import Any, Dict, Optional

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.users import create_new_user, get_current_user_tokens
from tests.utils.utils import random_boolean, random_domain
from tests.utils.websites import create_random_website

from app.api.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.db.repositories import WebsitesRepository
from app.db.schemas import WebsiteRead, WebsiteUpdate
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


async def test_create_website_as_superuser(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain()
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["domain"] == domain
    assert entry["is_secure"] == is_secure


async def test_create_website_as_superuser_website_already_exists(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain()
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    entry: Dict[str, Any] = response.json()
    assert entry["domain"] == domain
    assert entry["is_secure"] == is_secure
    is_secure_2: bool = random_boolean()
    data_2: Dict[str, Any] = {"domain": domain, "is_secure": is_secure_2}
    response_2: Response = await client.post(
        "websites/",
        headers=superuser_token_headers,
        json=data_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == "Website domain exists"


async def test_create_website_as_testuser(
    client: AsyncClient,
    user_auth: AuthManager,
) -> None:
    a_user: UserAdmin
    a_user_password: str
    a_user, a_user_password = await create_new_user(user_auth)
    a_user_access_header = await get_current_user_tokens(
        client, a_user.email, a_user_password
    )
    a_token: str = a_user_access_header["access_token"]
    domain: str = random_domain()
    is_secure: bool = random_boolean()
    data: Dict[str, Any] = {"domain": domain, "is_secure": is_secure}
    response: Response = await client.post(
        "websites/",
        headers={"Authorization": f"Bearer {a_token}"},
        json=data,
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_read_website_by_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get(
        f"websites/{entry.id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    repo: WebsitesRepository = WebsitesRepository(db_session)
    existing_data: Any = await repo.read_by("domain", entry.domain)
    assert existing_data
    assert existing_data.domain == data["domain"]


async def test_read_website_by_id_as_superuser_website_not_found(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"websites/{entry_id}",
        headers=superuser_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Website not found"


async def test_read_website_by_id_as_testuser(
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
    entry: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get(
        f"websites/{entry.id}",
        headers={"Authorization": f"Bearer {a_token}"},
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS


async def test_update_website_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    superuser_token_headers: Dict[str, str],
) -> None:
    entry_a: WebsiteRead = await create_random_website(db_session)
    entry_b: WebsiteRead = await create_random_website(db_session)
    update_dict = WebsiteUpdate(domain=entry_b.domain, is_secure=random_boolean())
    response: Response = await client.patch(
        f"websites/{entry_a.id}",
        headers=superuser_token_headers,
        json=update_dict.dict(),
    )
    updated_entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert updated_entry["detail"] == "Website domain exists"


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
    repo: WebsitesRepository = WebsitesRepository(db_session)
    data_not_found: Optional[Any] = await repo.read_by("domain", entry.domain)
    assert data_not_found is None


async def test_delete_website_by_id_as_testuser(
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
    entry: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{entry.id}",
        headers={"Authorization": f"Bearer {a_token}"},
    )
    error: Dict[str, Any] = response.json()
    assert response.status_code == 403
    assert error["detail"] == ErrorCode.USER_INSUFFICIENT_PERMISSIONS
