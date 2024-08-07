from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.models import User, UserClient, Website
from app.schemas import (
    ClientRead,
    GoAnalytics4PropertyRead,
    GoAnalytics4StreamRead,
    WebsiteRead,
)

pytestmark = pytest.mark.asyncio


async def test_update_ga4_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    ga4_stream: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"ga4/stream/{ga4_stream.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["stream_id"] == ga4_stream.stream_id
    assert entry["ga4_id"] == str(ga4_property.id)
    assert entry["website_id"] == str(a_website.id)


async def test_update_ga4_property_as_superuser_website_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    b_website: Website | WebsiteRead = await create_random_website(db_session)
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    ga4_stream: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(), website_id=str(b_website.id)
    )
    response: Response = await client.patch(
        f"ga4/stream/{ga4_stream.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["stream_id"] == ga4_stream.stream_id
    assert entry["ga4_id"] == str(ga4_property.id)
    assert entry["website_id"] == str(b_website.id)


async def test_update_ga4_property_as_superuser_website_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_website_id = get_uuid_str()
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    ga4_stream: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(), website_id=fake_website_id
    )
    response: Response = await client.patch(
        f"ga4/stream/{ga4_stream.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_update_ga4_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_client_a_user: UserClient = await assign_user_to_client(  # noqa: F841
        db_session, a_user, a_client
    )
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    ga4_stream: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"ga4/stream/{ga4_stream.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["stream_id"] == ga4_stream.stream_id
    assert entry["ga4_id"] == str(ga4_property.id)
    assert entry["website_id"] == str(a_website.id)


async def test_update_ga4_property_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    ga4_stream: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"ga4/stream/{ga4_stream.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_update_ga4_property_as_superuser_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: Website | WebsiteRead = await create_random_website(db_session)
    ga4_property: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, client_id=a_client.id
    )
    ga4_stream: GoAnalytics4StreamRead = await create_random_ga4_stream(
        db_session, ga4_property.id, a_website.id
    )
    a_client_website = await assign_website_to_client(  # noqa: F841
        db_session, a_website, a_client
    )
    data_in: Dict[str, Any] = dict(
        title=ga4_stream.title,
    )
    response: Response = await client.patch(
        f"ga4/stream/{ga4_stream.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert entry["detail"] == ErrorCode.GA4_STREAM_EXISTS
