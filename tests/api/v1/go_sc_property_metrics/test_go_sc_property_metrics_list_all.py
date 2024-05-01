from typing import Any, Dict

import pytest
from httpx import AsyncClient, QueryParams, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.go_sc import (
    create_random_go_search_console_property,
    create_random_go_search_console_property_metric,
)
from tests.utils.utils import random_date
from tests.utils.websites import create_random_website

from app.api.exceptions.errors import ErrorCode
from app.schemas import (
    ClientRead,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsolePropertyRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_list_all_go_sc_property_metric_as_superuser_all_metric_types(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session,
            gsc_id=a_gsc.id,
            metric_type=GoSearchConsoleMetricType.searchappearance,
        )
    )
    entry_2: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.query
        )
    )
    entry_3: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.page
        )
    )
    entry_4: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.device
        )
    )
    entry_5: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.country
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}",
        headers=admin_token_headers,
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    for metric_type_str, metric_type_pages in data.items():
        if metric_type_str == "searchappearance":
            assert metric_type_str == "searchappearance"
            assert metric_type_pages["total"] == 1
            assert metric_type_pages["page"] == 1
            assert metric_type_pages["size"] == 1000
            assert metric_type_pages["results"][0]["id"] == str(entry_1.id)
        if metric_type_str == "query":
            assert metric_type_str == "query"
            assert metric_type_pages["total"] == 1
            assert metric_type_pages["page"] == 1
            assert metric_type_pages["size"] == 1000
            assert metric_type_pages["results"][0]["id"] == str(entry_2.id)
        if metric_type_str == "page":
            assert metric_type_str == "page"
            assert metric_type_pages["total"] == 1
            assert metric_type_pages["page"] == 1
            assert metric_type_pages["size"] == 1000
            assert metric_type_pages["results"][0]["id"] == str(entry_3.id)
        if metric_type_str == "device":
            assert metric_type_str == "device"
            assert metric_type_pages["total"] == 1
            assert metric_type_pages["page"] == 1
            assert metric_type_pages["size"] == 1000
            assert metric_type_pages["results"][0]["id"] == str(entry_4.id)
        if metric_type_str == "country":
            assert metric_type_str == "country"
            assert metric_type_pages["total"] == 1
            assert metric_type_pages["page"] == 1
            assert metric_type_pages["size"] == 1000
            assert metric_type_pages["results"][0]["id"] == str(entry_5.id)


async def test_list_all_go_sc_property_metric_as_superuser_by_metric_types(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session,
            gsc_id=a_gsc.id,
            metric_type=GoSearchConsoleMetricType.searchappearance,
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.query
        )
    )
    entry_3: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.page
        )
    )
    entry_4: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.device
        )
    )
    entry_5: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.country
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}",
        headers=admin_token_headers,
        params=QueryParams(
            {"metric_types": GoSearchConsoleMetricType.searchappearance.value}
        ),
    )
    assert 200 <= response.status_code < 300
    data: Dict[str, Any] = response.json()
    for metric_type_str, metric_type_pages in data.items():
        if metric_type_str == "searchappearance":
            assert metric_type_str == "searchappearance"
            assert metric_type_pages["total"] == 1
            assert metric_type_pages["page"] == 1
            assert metric_type_pages["size"] == 1000
            assert metric_type_pages["results"][0]["id"] == str(entry_1.id)
        if metric_type_str == "query":
            assert metric_type_str == "query"
            assert metric_type_pages is None
        if metric_type_str == "page":
            assert metric_type_str == "page"
            assert metric_type_pages is None
        if metric_type_str == "device":
            assert metric_type_str == "device"
            assert metric_type_pages is None
        if metric_type_str == "country":
            assert metric_type_str == "country"
            assert metric_type_pages is None


async def test_list_all_go_sc_property_metric_as_superuser_invalid_metric_type(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    entry_1: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session,
            gsc_id=a_gsc.id,
            metric_type=GoSearchConsoleMetricType.searchappearance,
        )
    )
    entry_2: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.query
        )
    )
    entry_3: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.page
        )
    )
    entry_4: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.device
        )
    )
    entry_5: GoSearchConsoleMetricRead = (  # noqa: F841
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=GoSearchConsoleMetricType.country
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}",
        headers=admin_token_headers,
        params=QueryParams({"metric_types": "invalid"}),
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 422
    assert data["detail"] == ErrorCode.GO_SEARCH_METRIC_TYPE_INVALID


async def test_list_all_go_sc_property_metric_as_superuser_by_date_start(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}",
        headers=admin_token_headers,
        params=QueryParams({"date_start": str(random_date())}),
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    for metric_type_str, metric_type_pages in data.items():
        assert metric_type_pages["total"] == 0
        assert metric_type_pages["page"] == 1
        assert metric_type_pages["size"] == 1000
        assert metric_type_pages["results"] == []


async def test_list_all_go_sc_property_metric_as_superuser_by_date_end(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}",
        headers=admin_token_headers,
        params=QueryParams({"date_end": str(random_date())}),
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    for metric_type_str, metric_type_pages in data.items():
        assert metric_type_pages["total"] == 0
        assert metric_type_pages["page"] == 1
        assert metric_type_pages["size"] == 1000
        assert metric_type_pages["results"] == []


async def test_list_all_go_sc_property_metric_as_superuser_between_date(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}",
        headers=admin_token_headers,
        params=QueryParams(
            {
                "date_start": str(random_date()),
                "date_end": str(random_date()),
            }
        ),
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    for metric_type_str, metric_type_pages in data.items():
        assert metric_type_pages["total"] == 0
        assert metric_type_pages["page"] == 1
        assert metric_type_pages["size"] == 1000
        assert metric_type_pages["results"] == []
