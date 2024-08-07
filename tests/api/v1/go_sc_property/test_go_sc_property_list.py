from typing import Any, Dict

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.go_sc import create_random_go_search_console_property
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

from app.core.config import settings
from app.models import ClientWebsite, User, Website
from app.schemas import ClientRead, GoSearchConsolePropertyRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_list_all_go_sc_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    entry_1: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, client_id=a_client.id, website_id=a_website.id
        )
    )
    entry_2: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, client_id=a_client.id, website_id=a_website.id
        )
    )
    entry_3: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, client_id=a_client.id, website_id=a_website.id
        )
    )
    entry_4: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, client_id=b_client.id, website_id=a_website.id
        )
    )
    response: Response = await client.get(
        "go/search/property/", headers=admin_token_headers
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["website_id"] == str(entry_1.website_id)
            assert entry["client_id"] == str(entry_1.client_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["website_id"] == str(entry_2.website_id)
            assert entry["client_id"] == str(entry_2.client_id)
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert entry["website_id"] == str(entry_3.website_id)
            assert entry["client_id"] == str(entry_3.client_id)
        if entry["id"] == str(entry_4.id):
            assert entry["title"] == entry_4.title
            assert entry["website_id"] == str(entry_4.website_id)
            assert entry["client_id"] == str(entry_4.client_id)


async def test_list_all_go_sc_property_as_superuser_query_client_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    entry_1: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, client_id=a_client.id, website_id=a_website.id
        )
    )
    entry_2: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session, client_id=a_client.id, website_id=a_website.id
        )
    )
    entry_3: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session, client_id=b_client.id, website_id=a_website.id
        )
    )
    entry_4: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session, client_id=b_client.id, website_id=a_website.id
        )
    )
    response: Response = await client.get(
        "go/search/property/",
        headers=admin_token_headers,
        params=QueryParams(client_id=a_client.id),
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["website_id"] == str(entry_1.website_id)
            assert entry["client_id"] == str(entry_1.client_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["website_id"] == str(entry_2.website_id)
            assert entry["client_id"] == str(entry_2.client_id)


async def test_list_all_go_sc_property_as_superuser_query_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    c_website: Website | WebsiteRead = await create_random_website(db_session)
    a_client_a_website: ClientWebsite = await assign_website_to_client(
        db_session,
        a_website,
        a_client,
    )
    a_client_b_website: ClientWebsite = await assign_website_to_client(
        db_session,
        b_website,
        a_client,
    )
    a_client_c_website: ClientWebsite = await assign_website_to_client(
        db_session,
        c_website,
        a_client,
    )
    entry_1: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session,
            client_id=a_client_a_website.client_id,
            website_id=a_client_a_website.website_id,
        )
    )
    entry_2: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session,
            client_id=a_client_b_website.client_id,
            website_id=a_client_b_website.website_id,
        )
    )
    entry_3: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session,
            client_id=a_client_c_website.client_id,
            website_id=a_client_c_website.website_id,
        )
    )
    response: Response = await client.get(
        "go/search/property/",
        headers=admin_token_headers,
        params=QueryParams(website_id=b_website.id),
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
    for entry in data["results"]:
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["website_id"] == str(entry_2.website_id)
            assert entry["client_id"] == str(entry_2.client_id)


async def test_list_all_go_sc_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    c_website: Website | WebsiteRead = await create_random_website(db_session)
    await assign_user_to_client(db_session, a_user, a_client)
    a_client_a_website: ClientWebsite = await assign_website_to_client(
        db_session,
        a_website,
        a_client,
    )
    a_client_b_website: ClientWebsite = await assign_website_to_client(
        db_session,
        b_website,
        b_client,
    )
    a_client_c_website: ClientWebsite = await assign_website_to_client(
        db_session,
        c_website,
        b_client,
    )
    entry_1: GoSearchConsolePropertyRead = (
        await create_random_go_search_console_property(
            db_session,
            client_id=a_client_a_website.client_id,
            website_id=a_client_a_website.website_id,
        )
    )
    entry_2: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session,
            client_id=a_client_b_website.client_id,
            website_id=a_client_b_website.website_id,
        )
    )
    entry_3: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session,
            client_id=a_client_c_website.client_id,
            website_id=a_client_c_website.website_id,
        )
    )
    response: Response = await client.get(
        "go/search/property/",
        headers=employee_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 1
    assert data["size"] == 1000
    assert len(data["results"]) == 1
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["website_id"] == str(entry_1.website_id)
            assert entry["client_id"] == str(entry_1.client_id)
