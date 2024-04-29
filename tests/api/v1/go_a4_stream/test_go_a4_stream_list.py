from typing import Any, Dict

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

from app.core.config import settings
from app.models import User
from app.schemas import ClientRead, GoAnalytics4PropertyRead, WebsiteRead
from app.schemas.go_a4_stream import GoAnalytics4StreamRead

pytestmark = pytest.mark.asyncio


async def test_list_all_ga4_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    c_website: WebsiteRead = await create_random_website(db_session)
    d_website: WebsiteRead = await create_random_website(db_session)
    a_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    entry_1: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, a_website.id
    )
    entry_2: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, b_website.id
    )
    entry_3: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, c_website.id
    )
    entry_4: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, d_website.id
    )
    response: Response = await client.get("ga4/stream/", headers=admin_token_headers)
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 4
    assert data["size"] == 1000
    assert len(data["results"]) == 4
    for entry in data["results"]:
        if entry["id"] == str(entry_1.id):
            assert entry["title"] == entry_1.title
            assert entry["stream_id"] == entry_1.stream_id
            assert entry["ga4_id"] == str(entry_1.ga4_id)
            assert entry["website_id"] == str(entry_1.website_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["stream_id"] == entry_2.stream_id
            assert entry["ga4_id"] == str(entry_2.ga4_id)
            assert entry["website_id"] == str(entry_2.website_id)
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert entry["stream_id"] == entry_3.stream_id
            assert entry["ga4_id"] == str(entry_3.ga4_id)
            assert entry["website_id"] == str(entry_3.website_id)
        if entry["id"] == str(entry_4.id):
            assert entry["title"] == entry_4.title
            assert entry["stream_id"] == entry_4.stream_id
            assert entry["ga4_id"] == str(entry_4.ga4_id)
            assert entry["website_id"] == str(entry_4.website_id)


async def test_list_all_ga4_property_as_superuser_by_ga4_property_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    c_website: WebsiteRead = await create_random_website(db_session)
    d_website: WebsiteRead = await create_random_website(db_session)
    a_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    b_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=b_client.id
    )
    entry_1: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, a_ga4_property.id, a_website.id
    )
    entry_2: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, a_ga4_property.id, b_website.id
    )
    entry_3: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, b_ga4_property.id, c_website.id
    )
    entry_4: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, b_ga4_property.id, d_website.id
    )
    response: Response = await client.get(
        "ga4/stream/",
        headers=admin_token_headers,
        params=QueryParams(ga4_id=b_ga4_property.id),
    )
    assert 200 <= response.status_code < 300
    data: Any = response.json()
    assert data["page"] == 1
    assert data["total"] == 2
    assert data["size"] == 1000
    assert len(data["results"]) == 2
    for entry in data["results"]:
        if entry["id"] == str(entry_3.id):
            assert entry["title"] == entry_3.title
            assert entry["stream_id"] == entry_3.stream_id
            assert entry["ga4_id"] == str(entry_3.ga4_id)
            assert entry["website_id"] == str(entry_3.website_id)
        if entry["id"] == str(entry_4.id):
            assert entry["title"] == entry_4.title
            assert entry["stream_id"] == entry_4.stream_id
            assert entry["ga4_id"] == str(entry_4.ga4_id)
            assert entry["website_id"] == str(entry_4.website_id)


async def test_list_all_ga4_property_as_superuser_query_ga4_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    c_website: WebsiteRead = await create_random_website(db_session)
    d_website: WebsiteRead = await create_random_website(db_session)
    a_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    b_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=b_client.id
    )
    entry_1: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, a_website.id
    )
    entry_2: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, b_website.id
    )
    entry_3: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, b_ga4_property.id, c_website.id
    )
    entry_4: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, b_ga4_property.id, d_website.id
    )
    response: Response = await client.get(
        "ga4/stream/",
        headers=admin_token_headers,
        params=QueryParams(ga4_id=a_ga4_property.id),
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
            assert entry["stream_id"] == entry_1.stream_id
            assert entry["ga4_id"] == str(entry_1.ga4_id)
            assert entry["website_id"] == str(entry_1.website_id)
        if entry["id"] == str(entry_2.id):
            assert entry["title"] == entry_2.title
            assert entry["stream_id"] == entry_2.stream_id
            assert entry["ga4_id"] == str(entry_2.ga4_id)
            assert entry["website_id"] == str(entry_2.website_id)


async def test_list_all_ga4_property_as_superuser_query_website_id(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    c_website: WebsiteRead = await create_random_website(db_session)
    d_website: WebsiteRead = await create_random_website(db_session)
    a_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    b_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=b_client.id
    )
    entry_1: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, a_ga4_property.id, a_website.id
    )
    entry_2: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, b_website.id
    )
    entry_3: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, b_ga4_property.id, c_website.id
    )
    entry_4: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, b_ga4_property.id, d_website.id
    )
    response: Response = await client.get(
        "ga4/stream/",
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
            assert entry["stream_id"] == entry_2.stream_id
            assert entry["ga4_id"] == str(entry_2.ga4_id)
            assert entry["website_id"] == str(entry_2.website_id)


async def test_list_all_ga4_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    c_website: WebsiteRead = await create_random_website(db_session)
    d_website: WebsiteRead = await create_random_website(db_session)
    a_user_a_client = await assign_user_to_client(db_session, a_user, a_client)
    a_client_a_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    a_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_user_a_client.client_id
    )
    b_ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=b_client.id
    )
    entry_1: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, a_ga4_property.id, a_website.id
    )
    entry_2: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, a_ga4_property.id, b_website.id
    )
    entry_3: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, b_ga4_property.id, c_website.id
    )
    entry_4: GoAnalytics4StreamRead = await create_random_ga4_stream(  # noqa: F841
        db_session, b_ga4_property.id, d_website.id
    )
    response: Response = await client.get(
        "ga4/stream/",
        headers=employee_token_headers,
        params=QueryParams(website_id=a_website.id),
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
            assert entry["stream_id"] == entry_1.stream_id
            assert entry["ga4_id"] == str(entry_1.ga4_id)
            assert entry["website_id"] == str(entry_1.website_id)
