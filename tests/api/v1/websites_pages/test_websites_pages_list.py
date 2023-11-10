from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map
from tests.utils.website_pages import create_random_website_page
from tests.utils.websites import create_random_website

from app.schemas import WebsiteMapRead, WebsitePageRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_website_pages_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsitePageRead = await create_random_website_page(db_session)
    entry_2: WebsitePageRead = await create_random_website_page(db_session)
    response: Response = await client.get("webpages/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 25
    assert data["size"] == 100
    assert len(data["results"]) == 25
    for entry in data["results"]:
        assert "url" in entry
        assert "status" in entry
        assert "priority" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["url"] == entry_1.url
            assert entry["status"] == entry_1.status
            assert entry["priority"] == entry_1.priority
            assert entry["sitemap_id"] == str(entry_1.sitemap_id)
            assert entry["website_id"] == str(entry_1.website_id)
        if entry["id"] == str(entry_2.id):
            assert entry["url"] == entry_2.url
            assert entry["status"] == entry_2.status
            assert entry["priority"] == entry_2.priority
            assert entry["sitemap_id"] == str(entry_2.sitemap_id)
            assert entry["website_id"] == str(entry_2.website_id)


async def test_list_website_pages_as_superuser_by_website_id_and_sitemap_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    sitemap_a: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_a.id
    )
    sitemap_b: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_a.id
    )
    entry_2: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_a.id
    )
    entry_3: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_b.id
    )
    entry_4: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_b.id
    )
    entry_5: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_a.id, sitemap_id=sitemap_b.id
    )
    entry_6: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_a.id
    )
    entry_7: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session
    )
    entry_8: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session
    )
    response: Response = await client.get(
        "webpages/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
            "sitemap_id": str(sitemap_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 100
    assert len(data["results"]) == 2
    for entry in data["results"]:
        assert "url" in entry
        assert "status" in entry
        assert "priority" in entry
        assert "website_id" in entry
        assert "sitemap_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["url"] == entry_1.url
            assert entry["status"] == entry_1.status
            assert entry["priority"] == entry_1.priority
            assert entry["website_id"] == str(entry_1.website_id)
            assert entry["sitemap_id"] == str(entry_1.sitemap_id)
        if entry["id"] == str(entry_2.id):
            assert entry["url"] == entry_2.url
            assert entry["status"] == entry_2.status
            assert entry["priority"] == entry_2.priority
            assert entry["website_id"] == str(entry_2.website_id)
            assert entry["sitemap_id"] == str(entry_2.sitemap_id)


async def test_list_website_pages_as_superuser_by_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    sitemap_a: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_a.id
    )
    sitemap_b: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_a.id
    )
    entry_2: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_a.id
    )
    entry_3: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_b.id
    )
    entry_4: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_b.id
    )
    entry_5: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_b.id
    )
    entry_6: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_a.id
    )
    entry_7: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session
    )
    entry_8: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session
    )
    response: Response = await client.get(
        "webpages/",
        headers=admin_token_headers,
        params={
            "website_id": str(website_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 100
    assert len(data["results"]) == 3
    for entry in data["results"]:
        assert "url" in entry
        assert "status" in entry
        assert "priority" in entry
        assert "website_id" in entry
        assert "sitemap_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["url"] == entry_1.url
            assert entry["status"] == entry_1.status
            assert entry["priority"] == entry_1.priority
            assert entry["website_id"] == str(entry_1.website_id)
            assert entry["sitemap_id"] == str(entry_1.sitemap_id)
        if entry["id"] == str(entry_2.id):
            assert entry["url"] == entry_2.url
            assert entry["status"] == entry_2.status
            assert entry["priority"] == entry_2.priority
            assert entry["website_id"] == str(entry_2.website_id)
            assert entry["sitemap_id"] == str(entry_2.sitemap_id)
        if entry["id"] == str(entry_5.id):
            assert entry["url"] == entry_5.url
            assert entry["status"] == entry_5.status
            assert entry["priority"] == entry_5.priority
            assert entry["website_id"] == str(entry_5.website_id)
            assert entry["sitemap_id"] == str(entry_5.sitemap_id)


async def test_list_website_pages_as_superuser_by_sitemap_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    sitemap_a: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_a.id
    )
    sitemap_b: WebsiteMapRead = await create_random_website_map(
        db_session, website_id=website_b.id
    )
    # entries
    entry_1: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_a.id
    )
    entry_2: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_a.id, sitemap_id=sitemap_a.id
    )
    entry_3: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_b.id
    )
    entry_4: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_b.id, sitemap_id=sitemap_b.id
    )
    entry_5: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session, website_id=website_a.id, sitemap_id=sitemap_b.id
    )
    entry_6: WebsitePageRead = await create_random_website_page(
        db_session, website_id=website_b.id, sitemap_id=sitemap_a.id
    )
    entry_7: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session
    )
    entry_8: WebsitePageRead = await create_random_website_page(  # noqa: F841
        db_session
    )
    response: Response = await client.get(
        "webpages/",
        headers=admin_token_headers,
        params={
            "sitemap_id": str(sitemap_a.id),
        },
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 3
    assert data["size"] == 100
    assert len(data["results"]) == 3
    for entry in data["results"]:
        assert "url" in entry
        assert "status" in entry
        assert "priority" in entry
        assert "website_id" in entry
        assert "sitemap_id" in entry
        if entry["id"] == str(entry_1.id):
            assert entry["url"] == entry_1.url
            assert entry["status"] == entry_1.status
            assert entry["priority"] == entry_1.priority
            assert entry["website_id"] == str(entry_1.website_id)
            assert entry["sitemap_id"] == str(entry_1.sitemap_id)
        if entry["id"] == str(entry_2.id):
            assert entry["url"] == entry_2.url
            assert entry["status"] == entry_2.status
            assert entry["priority"] == entry_2.priority
            assert entry["website_id"] == str(entry_2.website_id)
            assert entry["sitemap_id"] == str(entry_2.sitemap_id)
        if entry["id"] == str(entry_6.id):
            assert entry["url"] == entry_6.url
            assert entry["status"] == entry_6.status
            assert entry["priority"] == entry_6.priority
            assert entry["website_id"] == str(entry_6.website_id)
            assert entry["sitemap_id"] == str(entry_6.sitemap_id)
