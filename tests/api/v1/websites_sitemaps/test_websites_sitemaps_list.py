from typing import Any
from typing import Dict

import pytest
from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map
from tests.utils.websites import create_random_website

from app.schemas import WebsiteMapRead
from app.schemas import WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_website_sitemaps_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsiteMapRead = await create_random_website_map(db_session)
    entry_2: WebsiteMapRead = await create_random_website_map(db_session)
    response: Response = await client.get("sitemaps/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    all_entries: Any = response.json()
    assert len(all_entries) >= 1
    for entry in all_entries:
        assert "url" in entry
        if entry["id"] == entry_1.id:
            assert entry["url"] == entry_1.url
            assert entry["website_id"] == entry_1.website_id
        if entry["id"] == entry_2.id:
            assert entry["url"] == entry_2.url
            assert entry["website_id"] == entry_2.website_id


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
    all_entries: Any = response.json()
    assert len(all_entries) == 3
    for entry in all_entries:
        assert "url" in entry
        if entry["id"] == entry_1.id:
            assert entry["url"] == entry_1.url
            assert entry["website_id"] == entry_1.website_id
        if entry["id"] == entry_2.id:
            assert entry["url"] == entry_2.url
            assert entry["website_id"] == entry_2.website_id
        if entry["id"] == entry_3.id:
            assert entry["url"] == entry_3.url
            assert entry["website_id"] == entry_3.website_id
