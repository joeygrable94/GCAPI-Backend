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
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.models import User, Website
from app.schemas import (
    ClientRead,
    GoSearchConsoleMetricRead,
    GoSearchConsoleMetricType,
    GoSearchConsolePropertyRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_update_go_sc_property_metric_as_superuser(
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
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        impressions=entry_1.impressions + 1,
        clicks=entry_1.clicks + 1,
    )
    response: Response = await client.patch(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_1.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["title"] == data_in["title"]
    assert data["keys"] == entry_1.keys
    assert data["clicks"] == data_in["clicks"]
    assert data["impressions"] == data_in["impressions"]
    assert data["ctr"] == entry_1.ctr
    assert data["position"] == entry_1.position
    assert data["gsc_id"] == str(a_gsc.id)


async def test_update_go_sc_property_metric_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    await assign_user_to_client(db_session, a_user, a_client)
    await assign_website_to_client(db_session, a_website, a_client)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        impressions=entry_1.impressions + 1,
        clicks=entry_1.clicks + 1,
    )
    response: Response = await client.patch(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_1.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    data: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert data["title"] == data_in["title"]
    assert data["keys"] == entry_1.keys
    assert data["clicks"] == data_in["clicks"]
    assert data["impressions"] == data_in["impressions"]
    assert data["ctr"] == entry_1.ctr
    assert data["position"] == entry_1.position
    assert data["gsc_id"] == str(a_gsc.id)


async def test_update_go_sc_property_metric_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = await create_random_go_search_console_property(
        db_session, client_id=a_client.id, website_id=a_website.id
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    entry_1: GoSearchConsoleMetricRead = (
        await create_random_go_search_console_property_metric(
            db_session, gsc_id=a_gsc.id, metric_type=a_metric_type
        )
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}/{entry_1.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS
