from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.go_sc import create_random_go_search_console_property
from tests.utils.users import get_user_by_email
from tests.utils.utils import (
    random_datetime,
    random_float,
    random_integer,
    random_lower_string,
)
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.models import User, Website
from app.schemas import (
    ClientRead,
    GoSearchConsoleMetricType,
    GoSearchConsolePropertyRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_create_go_sc_property_metric_as_superuser(
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
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        keys=random_lower_string(),
        clicks=random_integer(),
        impressions=random_integer(),
        ctr=random_float(),
        position=random_float(),
        date_start=str(random_datetime()),
        date_end=str(random_datetime()),
        gsc_id=str(a_gsc.id),
    )
    response: Response = await client.post(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["keys"] == data_in["keys"]
    assert entry["clicks"] == data_in["clicks"]
    assert entry["impressions"] == data_in["impressions"]
    assert entry["gsc_id"] == str(a_gsc.id)


async def test_create_go_sc_property_metric_as_superuser_gsc_property_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_gsc_id = get_uuid_str()
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_gsc: GoSearchConsolePropertyRead = (  # noqa: F841
        await create_random_go_search_console_property(
            db_session, client_id=a_client.id, website_id=a_website.id
        )
    )
    a_metric_type = GoSearchConsoleMetricType.searchappearance
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        keys=random_lower_string(),
        clicks=random_integer(),
        impressions=random_integer(),
        ctr=random_float(),
        position=random_float(),
        date_start=str(random_datetime()),
        date_end=str(random_datetime()),
        gsc_id=fake_gsc_id,
    )
    response: Response = await client.post(
        f"go/search/metric/{fake_gsc_id}/{a_metric_type.value}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.GO_SEARCH_PROPERTY_NOT_FOUND


async def test_create_go_sc_property_metric_as_employee(
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
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        keys=random_lower_string(),
        clicks=random_integer(),
        impressions=random_integer(),
        ctr=random_float(),
        position=random_float(),
        date_start=str(random_datetime()),
        date_end=str(random_datetime()),
        gsc_id=str(a_gsc.id),
    )
    response: Response = await client.post(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["keys"] == data_in["keys"]
    assert entry["clicks"] == data_in["clicks"]
    assert entry["impressions"] == data_in["impressions"]
    assert entry["gsc_id"] == str(a_gsc.id)


async def test_create_go_sc_property_metric_as_employee_forbidden(
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
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        keys=random_lower_string(),
        clicks=random_integer(),
        impressions=random_integer(),
        ctr=random_float(),
        position=random_float(),
        date_start=str(random_datetime()),
        date_end=str(random_datetime()),
        gsc_id=str(a_gsc.id),
    )
    response: Response = await client.post(
        f"go/search/metric/{a_gsc.id}/{a_metric_type.value}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS
