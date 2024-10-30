from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities import get_uuid_str
from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT
from app.models import User
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_create_ga4_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        measurement_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        property_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "ga4/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["measurement_id"] == data_in["measurement_id"]
    assert entry["property_id"] == data_in["property_id"]
    assert entry["client_id"] == str(a_client.id)


async def test_create_ga4_property_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    a_website = await create_random_website(db_session)  # noqa: F841
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        measurement_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        property_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        client_id=fake_client_id,
    )
    response: Response = await client.post(
        "ga4/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_ga4_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_user_a_client = await assign_user_to_client(db_session, a_user, a_client)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        measurement_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        property_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        client_id=str(a_user_a_client.client_id),
    )
    response: Response = await client.post(
        "ga4/property/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["measurement_id"] == data_in["measurement_id"]
    assert entry["property_id"] == data_in["property_id"]
    assert entry["client_id"] == str(a_client.id)


async def test_create_ga4_property_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        measurement_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        property_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "ga4/property/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_create_ga4_property_as_superuser_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        measurement_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        property_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "ga4/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["measurement_id"] == data_in["measurement_id"]
    assert entry["property_id"] == data_in["property_id"]
    assert entry["client_id"] == str(a_client.id)
    data_in_2: Dict[str, Any] = dict(
        title=random_lower_string(),
        measurement_id=data_in["measurement_id"],
        property_id=random_lower_string(DB_STR_16BIT_MAXLEN_INPUT),
        client_id=str(a_client.id),
    )
    response_2: Response = await client.post(
        "ga4/property/",
        headers=admin_token_headers,
        json=data_in_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.GA4_PROPERTY_EXISTS
