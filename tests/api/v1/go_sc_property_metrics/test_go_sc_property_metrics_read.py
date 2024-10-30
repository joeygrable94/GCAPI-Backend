from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.go_sc import (
    create_random_go_search_console_property,
    create_random_go_search_console_property_metric,
)
from tests.utils.websites import create_random_website

from app.api.exceptions.errors import ErrorCode
from app.core.utilities import get_uuid_str
from app.crud import GoSearchConsoleMetricRepository
from app.models import (
    GoSearchConsoleCountry,
    GoSearchConsoleDevice,
    GoSearchConsolePage,
    GoSearchConsoleQuery,
    GoSearchConsoleSearchappearance,
    Website,
)
from app.schemas import (
    ClientRead,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsolePropertyRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_read_go_sc_property_metric_by_id_as_superuser_searchappearance(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    entry: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert data["keys"] == entry.keys
    assert data["clicks"] == entry.clicks
    assert data["impressions"] == entry.impressions
    assert data["gsc_id"] == str(a_gsc.id)
    repo: GoSearchConsoleMetricRepository = GoSearchConsoleMetricRepository(
        db_session, metric_type=a_metric_type
    )
    existing_data: (
        GoSearchConsoleCountry
        | GoSearchConsoleDevice
        | GoSearchConsolePage
        | GoSearchConsoleQuery
        | GoSearchConsoleSearchappearance
        | None
    ) = await repo.read(entry.id)
    assert existing_data
    assert existing_data.title == data["title"]
    assert existing_data.keys == data["keys"]
    assert existing_data.clicks == data["clicks"]
    assert str(existing_data.gsc_id) == data["gsc_id"]


async def test_read_go_sc_property_metric_by_id_as_superuser_searchappearance_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GO_SEARCH_METRIC_NOT_FOUND


async def test_read_go_sc_property_metric_by_id_as_superuser_query(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.query
    entry: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert data["keys"] == entry.keys
    assert data["clicks"] == entry.clicks
    assert data["impressions"] == entry.impressions
    assert data["gsc_id"] == str(a_gsc.id)
    repo: GoSearchConsoleMetricRepository = GoSearchConsoleMetricRepository(
        db_session, metric_type=a_metric_type
    )
    existing_data: (
        GoSearchConsoleCountry
        | GoSearchConsoleDevice
        | GoSearchConsolePage
        | GoSearchConsoleQuery
        | GoSearchConsoleSearchappearance
        | None
    ) = await repo.read(entry.id)
    assert existing_data
    assert existing_data.title == data["title"]
    assert existing_data.keys == data["keys"]
    assert existing_data.clicks == data["clicks"]
    assert str(existing_data.gsc_id) == data["gsc_id"]


async def test_read_go_sc_property_metric_by_id_as_superuser_query_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.query
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GO_SEARCH_METRIC_NOT_FOUND


async def test_read_go_sc_property_metric_by_id_as_superuser_page(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.page
    entry: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert data["keys"] == entry.keys
    assert data["clicks"] == entry.clicks
    assert data["impressions"] == entry.impressions
    assert data["gsc_id"] == str(a_gsc.id)
    repo: GoSearchConsoleMetricRepository = GoSearchConsoleMetricRepository(
        db_session, metric_type=a_metric_type
    )
    existing_data: (
        GoSearchConsoleCountry
        | GoSearchConsoleDevice
        | GoSearchConsolePage
        | GoSearchConsoleQuery
        | GoSearchConsoleSearchappearance
        | None
    ) = await repo.read(entry.id)
    assert existing_data
    assert existing_data.title == data["title"]
    assert existing_data.keys == data["keys"]
    assert existing_data.clicks == data["clicks"]
    assert str(existing_data.gsc_id) == data["gsc_id"]


async def test_read_go_sc_property_metric_by_id_as_superuser_page_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.page
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GO_SEARCH_METRIC_NOT_FOUND


async def test_read_go_sc_property_metric_by_id_as_superuser_device(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.device
    entry: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert data["keys"] == entry.keys
    assert data["clicks"] == entry.clicks
    assert data["impressions"] == entry.impressions
    assert data["gsc_id"] == str(a_gsc.id)
    repo: GoSearchConsoleMetricRepository = GoSearchConsoleMetricRepository(
        db_session, metric_type=a_metric_type
    )
    existing_data: (
        GoSearchConsoleCountry
        | GoSearchConsoleDevice
        | GoSearchConsolePage
        | GoSearchConsoleQuery
        | GoSearchConsoleSearchappearance
        | None
    ) = await repo.read(entry.id)
    assert existing_data
    assert existing_data.title == data["title"]
    assert existing_data.keys == data["keys"]
    assert existing_data.clicks == data["clicks"]
    assert str(existing_data.gsc_id) == data["gsc_id"]


async def test_read_go_sc_property_metric_by_id_as_superuser_device_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.device
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GO_SEARCH_METRIC_NOT_FOUND


async def test_read_go_sc_property_metric_by_id_as_superuser_country(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.country
    entry: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry.id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["id"] == str(entry.id)
    assert "title" in data
    assert data["keys"] == entry.keys
    assert data["clicks"] == entry.clicks
    assert data["impressions"] == entry.impressions
    assert data["gsc_id"] == str(a_gsc.id)
    repo: GoSearchConsoleMetricRepository = GoSearchConsoleMetricRepository(
        db_session, metric_type=a_metric_type
    )
    existing_data: (
        GoSearchConsoleCountry
        | GoSearchConsoleDevice
        | GoSearchConsolePage
        | GoSearchConsoleQuery
        | GoSearchConsoleSearchappearance
        | None
    ) = await repo.read(entry.id)
    assert existing_data
    assert existing_data.title == data["title"]
    assert existing_data.keys == data["keys"]
    assert existing_data.clicks == data["clicks"]
    assert str(existing_data.gsc_id) == data["gsc_id"]


async def test_read_go_sc_property_metric_by_id_as_superuser_country_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.country
    entry_id: str = get_uuid_str()
    response: Response = await client.get(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_id}",
        headers=admin_token_headers,
    )
    data: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert data["detail"] == ErrorCode.GO_SEARCH_METRIC_NOT_FOUND
