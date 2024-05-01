from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.go_sc import (
    create_random_go_search_console_property,
    create_random_go_search_console_property_metric,
)
from tests.utils.users import get_user_by_email
from tests.utils.websites import create_random_website

from app.api.exceptions.errors import ErrorCode
from app.core.config import settings
from app.models import User
from app.schemas import (
    ClientRead,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsolePropertyRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_list_all_go_sc_property_metric_as_superuser_searchappearance(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
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
            assert entry["keys"] == str(entry_1.keys)
            assert entry["clicks"] == entry_1.clicks
            assert entry["impressions"] == entry_1.impressions
            assert entry["ctr"] == entry_1.ctr
            assert entry["position"] == entry_1.position
            assert entry["gsc_id"] == str(entry_1.gsc_id)


async def test_list_all_go_sc_property_metric_as_superuser_query(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.query
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
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
            assert entry["keys"] == str(entry_1.keys)
            assert entry["clicks"] == entry_1.clicks
            assert entry["impressions"] == entry_1.impressions
            assert entry["ctr"] == entry_1.ctr
            assert entry["position"] == entry_1.position
            assert entry["gsc_id"] == str(entry_1.gsc_id)


async def test_list_all_go_sc_property_metric_as_superuser_page(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.page
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
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
            assert entry["keys"] == str(entry_1.keys)
            assert entry["clicks"] == entry_1.clicks
            assert entry["impressions"] == entry_1.impressions
            assert entry["ctr"] == entry_1.ctr
            assert entry["position"] == entry_1.position
            assert entry["gsc_id"] == str(entry_1.gsc_id)


async def test_list_all_go_sc_property_metric_as_superuser_device(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.device
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
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
            assert entry["keys"] == str(entry_1.keys)
            assert entry["clicks"] == entry_1.clicks
            assert entry["impressions"] == entry_1.impressions
            assert entry["ctr"] == entry_1.ctr
            assert entry["position"] == entry_1.position
            assert entry["gsc_id"] == str(entry_1.gsc_id)


async def test_list_all_go_sc_property_metric_as_superuser_country(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.country
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
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
            assert entry["keys"] == str(entry_1.keys)
            assert entry["clicks"] == entry_1.clicks
            assert entry["impressions"] == entry_1.impressions
            assert entry["ctr"] == entry_1.ctr
            assert entry["position"] == entry_1.position
            assert entry["gsc_id"] == str(entry_1.gsc_id)


async def test_list_all_go_sc_property_metric_as_superuser_invalid_metric_type(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.country
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
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
            assert entry["keys"] == str(entry_1.keys)
            assert entry["clicks"] == entry_1.clicks
            assert entry["impressions"] == entry_1.impressions
            assert entry["ctr"] == entry_1.ctr
            assert entry["position"] == entry_1.position
            assert entry["gsc_id"] == str(entry_1.gsc_id)
    invalid_metric_type = "invalid_metric_type"
    response_2: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{invalid_metric_type}",
        headers=admin_token_headers,
    )
    assert response_2.status_code == 422
    data_2: Any = response_2.json()
    assert data_2["detail"][0]["msg"] == ErrorCode.GO_SEARCH_METRIC_TYPE_INVALID


async def test_list_all_go_sc_property_metric_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    b_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    b_website: WebsiteRead = await create_random_website(db_session)
    await assign_user_to_client(db_session, a_user, a_client)
    await assign_website_to_client(db_session, a_website, a_client)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    b_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=b_client.id, website_id=b_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    entry_1: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    entry_2: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=b_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=employee_token_headers,
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
            assert entry["keys"] == str(entry_2.keys)
            assert entry["clicks"] == entry_2.clicks
            assert entry["impressions"] == entry_2.impressions
            assert entry["ctr"] == entry_2.ctr
            assert entry["position"] == entry_2.position
            assert entry["date_start"] == entry_2.date_start
            assert entry["date_end"] == entry_2.date_end
            assert entry["gsc_id"] == str(entry_2.gsc_id)
