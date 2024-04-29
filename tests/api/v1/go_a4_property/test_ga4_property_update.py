from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.ga4 import create_random_ga4_property
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.models import User
from app.models.user_client import UserClient
from app.schemas import ClientRead, GoAnalytics4PropertyRead

pytestmark = pytest.mark.asyncio


async def test_update_ga4_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_ga4: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, a_client.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"ga4/property/{a_ga4.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["measurement_id"] == a_ga4.measurement_id
    assert entry["property_id"] == a_ga4.property_id
    assert entry["client_id"] == str(a_client.id)


async def test_update_ga4_property_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    a_client: ClientRead = await create_random_client(db_session)
    a_ga4: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, a_client.id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        client_id=fake_client_id,
    )
    response: Response = await client.patch(
        f"ga4/property/{a_ga4.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_update_ga4_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_client_a_user: UserClient = await assign_user_to_client(
        db_session, a_user, a_client
    )
    a_ga4: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, a_client_a_user.client_id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"ga4/property/{a_ga4.id}",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["measurement_id"] == a_ga4.measurement_id
    assert entry["property_id"] == a_ga4.property_id
    assert entry["client_id"] == str(a_client.id)


async def test_update_ga4_property_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_admin)
    a_client: ClientRead = await create_random_client(db_session)
    a_client_a_user: UserClient = await assign_user_to_client(
        db_session, a_user, a_client
    )
    a_ga4: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, a_client_a_user.client_id
    )
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
    )
    response: Response = await client.patch(
        f"ga4/property/{a_ga4.id}",
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
    a_ga4: GoAnalytics4PropertyRead = await create_random_ga4_property(
        db_session, a_client.id
    )
    data_in: Dict[str, Any] = dict(
        title=a_ga4.title,
        measurement_id=a_ga4.measurement_id,
        property_id=a_ga4.property_id,
    )
    response: Response = await client.patch(
        f"ga4/property/{a_ga4.id}",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 400
    assert entry["detail"] == ErrorCode.GA4_PROPERTY_EXISTS
