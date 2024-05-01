from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

from app.api.exceptions import ErrorCode
from app.core.config import settings
from app.core.utilities.uuids import get_uuid_str
from app.models import User
from app.schemas import ClientRead, WebsiteRead

pytestmark = pytest.mark.asyncio


async def test_create_go_sc_property_as_superuser(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=str(a_website.id),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "go/search/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["website_id"] == str(data_in["website_id"])
    assert entry["client_id"] == str(a_client.id)


async def test_create_go_sc_property_as_superuser_client_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_client_id = get_uuid_str()
    a_website: WebsiteRead = await create_random_website(db_session)  # noqa: F841
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=str(a_website.id),
        client_id=fake_client_id,
    )
    response: Response = await client.post(
        "go/search/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.CLIENT_NOT_FOUND


async def test_create_go_sc_property_as_superuser_website_not_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    fake_website_id = get_uuid_str()
    a_client: ClientRead = await create_random_client(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=fake_website_id,
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "go/search/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 404
    assert entry["detail"] == ErrorCode.WEBSITE_NOT_FOUND


async def test_create_go_sc_property_as_employee(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_user: User = await get_user_by_email(db_session, settings.auth.first_employee)
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    a_user_a_client = await assign_user_to_client(db_session, a_user, a_client)
    a_client_a_website = await assign_website_to_client(db_session, a_website, a_client)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=str(a_client_a_website.website_id),
        client_id=str(a_user_a_client.client_id),
    )
    response: Response = await client.post(
        "go/search/property/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["website_id"] == str(data_in["website_id"])
    assert entry["client_id"] == str(a_client.id)


async def test_create_go_sc_property_as_employee_forbidden(
    client: AsyncClient,
    db_session: AsyncSession,
    employee_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=str(a_website.id),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "go/search/property/",
        headers=employee_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert response.status_code == 405
    assert entry["detail"] == ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS


async def test_create_go_sc_property_as_superuser_already_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    a_client: ClientRead = await create_random_client(db_session)
    a_website: WebsiteRead = await create_random_website(db_session)
    data_in: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=str(a_website.id),
        client_id=str(a_client.id),
    )
    response: Response = await client.post(
        "go/search/property/",
        headers=admin_token_headers,
        json=data_in,
    )
    entry: Dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert entry["title"] == data_in["title"]
    assert entry["website_id"] == str(a_website.id)
    assert entry["client_id"] == str(a_client.id)
    data_in_2: Dict[str, Any] = dict(
        title=random_lower_string(),
        website_id=str(a_website.id),
        client_id=str(a_client.id),
    )
    response_2: Response = await client.post(
        "go/search/property/",
        headers=admin_token_headers,
        json=data_in_2,
    )
    assert response_2.status_code == 400
    entry_2: Dict[str, Any] = response_2.json()
    assert entry_2["detail"] == ErrorCode.GO_SEARCH_PROPERTY_EXISTS
