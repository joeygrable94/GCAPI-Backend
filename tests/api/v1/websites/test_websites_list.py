from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_website_to_client, create_random_client
from tests.utils.websites import create_random_website

from app.models.client_website import ClientWebsite
from app.schemas import WebsiteRead
from app.schemas.client import ClientRead

pytestmark = pytest.mark.asyncio


async def test_list_all_websites_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    entry_1: WebsiteRead = await create_random_website(db_session)
    response: Response = await client.get("websites/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 12
    assert data["size"] == 1000
    assert len(data["results"]) == 12
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["domain"] == entry_1.domain
            assert entry["is_secure"] == entry_1.is_secure


async def test_list_websites_by_client_id_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    # 1 make a client
    client_a: ClientRead = await create_random_client(db_session)
    # 2 make a website
    website_a: WebsiteRead = await create_random_website(db_session)
    website_b: WebsiteRead = await create_random_website(db_session)
    # 3 associate website with client
    client_website_a: ClientWebsite = await assign_website_to_client(  # noqa: F841
        db_session, website_a, client_a
    )
    client_website_b: ClientWebsite = await assign_website_to_client(  # noqa: F841
        db_session, website_b, client_a
    )
    # 4 list websites by client id
    response: Response = await client.get("websites/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    # 5 assert website is in list
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 14
    assert data["size"] == 1000
    assert len(data["results"]) == 14
    for entry in data["results"]:
        if entry["id"] == str(website_a.id):
            assert entry["domain"] == website_a.domain
            assert entry["is_secure"] == website_a.is_secure
        if entry["id"] == str(website_b.id):
            assert entry["domain"] == website_b.domain
            assert entry["is_secure"] == website_b.is_secure


async def test_list_all_websites_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    response: Response = await client.get("websites/", headers=employee_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 0
    assert data["size"] == 1000
    assert len(data["results"]) == 0
