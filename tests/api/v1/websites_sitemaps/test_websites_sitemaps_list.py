from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

from app.schemas import WebsiteMapRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_website_sitemaps_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsiteMapRead = await create_random_website_map(db_session)
    entry_2: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.get("sitemaps/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 99
    assert data["size"] == 1000
    assert len(data["results"]) == 99
    for entry in data["results"]:
        assert "url" in entry
        assert "website_id" in entry
        assert "is_active" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["url"] == entry_1.url
            assert entry["is_active"] == entry_1.is_active
            assert entry["website_id"] == str(entry_1.website_id)
        if entry["id"] == str(entry_2.id):
            assert entry["url"] == entry_2.url
            assert entry["is_active"] == entry_2.is_active
            assert entry["website_id"] == str(entry_2.website_id)


async def test_list_website_sitemaps_as_superuser_by_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    entry_1: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_a.id
    )
    entry_2: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_a.id
    )
    entry_3: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_a.id
    )
    entry_4: WebsiteMapRead = await create_random_website_map(  # noqa: F841
        db_session, website_id=website_b.id
    )
    entry_5: WebsiteMapRead = await create_random_website_map(  # noqa: F841
        db_session, website_id=website_b.id
    )
    response: Response = await client.get(
        "sitemaps/",
        headers=admin_token_headers,
        params={"website_id": str(website_a.id)},
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 1000
    assert len(data["results"]) == 3
    for entry in data["results"]:
        assert "url" in entry
        assert "website_id" in entry
        assert "is_active" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["url"] == entry_1.url
            assert entry["is_active"] == entry_1.is_active
            assert entry["website_id"] == str(entry_1.website_id)
        if entry["id"] == str(entry_2.id):
            assert entry["url"] == entry_2.url
            assert entry["is_active"] == entry_2.is_active
            assert entry["website_id"] == str(entry_2.website_id)
        if entry["id"] == str(entry_3.id):
            assert entry["url"] == entry_3.url
            assert entry["is_active"] == entry_3.is_active
            assert entry["website_id"] == str(entry_3.website_id)
        if entry["id"] == str(entry_4.id):
            assert entry["url"] == entry_4.url
            assert entry["is_active"] == entry_4.is_active
            assert entry["website_id"] == str(entry_4.website_id)
        if entry["id"] == str(entry_5.id):
            assert entry["url"] == entry_5.url
            assert entry["is_active"] == entry_5.is_active
            assert entry["website_id"] == str(entry_5.website_id)


async def test_list_all_website_sitemaps_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get("sitemaps/", headers=employee_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 0
    assert data["size"] == 1000
    assert len(data["results"]) == 0
