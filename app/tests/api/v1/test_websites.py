from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas.website import WebsiteRead
from app.tests.utils.utils import random_domain_name
from app.tests.utils.website import create_random_website

pytestmark = pytest.mark.asyncio


async def test_create_website(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    domain: str = random_domain_name()
    data: Dict[str, Any] = {"domain": domain, "is_secure": False}
    response: Response = await client.post(
        "websites/", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    site: Dict[str, Any] = response.json()
    assert site["domain"] == data["domain"]
    assert site["is_secure"] == data["is_secure"]
    assert "id" in site


async def test_read_website(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    website: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get(
        f"websites/{website.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    site: Dict[str, Any] = response.json()
    assert site["domain"] == website.domain
    assert site["is_secure"] == website.is_secure
    assert site["id"] == str(website.id)


async def test_update_website(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    website: WebsiteRead = await create_random_website(db_session)
    new_domain: str = random_domain_name()
    new_is_secure: bool = True
    data: Dict[str, Any] = {"domain": new_domain, "is_secure": new_is_secure}
    response: Response = await client.patch(
        f"websites/{website.id}", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200
    site: Dict[str, Any] = response.json()
    assert site["domain"] != website.domain
    assert site["domain"] == new_domain
    assert site["is_secure"] != website.is_secure
    assert site["is_secure"] == new_is_secure
    assert site["id"] == str(website.id)


async def test_delete_website(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    website: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.delete(
        f"websites/{website.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    site: Dict[str, Any] = response.json()
    assert site["domain"] == website.domain
    assert site["is_secure"] == website.is_secure
    assert site["id"] == str(website.id)


async def test_list_websites(
    client: AsyncClient,
    superuser_token_headers: Dict[str, str],
    db_session: AsyncSession,
) -> None:
    website_1: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    website_2: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    website_3: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    response: Response = await client.get("websites/", headers=superuser_token_headers)
    assert 200 <= response.status_code < 300
    all_websites: Dict[str, Any] = response.json()
    assert len(all_websites) > 1
    for site in all_websites:
        assert "id" in site
        assert "domain" in site
        assert "is_secure" in site
