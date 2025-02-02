from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_16BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_INPUT_SCHEMA_INVALID,
)
from app.entities.client.constants import ERROR_MESSAGE_CLIENT_NOT_FOUND
from app.entities.go_property.schemas import GooglePlatformType
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.ga4 import create_random_ga4_property
from tests.utils.platform import get_platform_by_slug
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_client,status_code",
    [
        ("admin_user", False, 200),
        ("manager_user", False, 200),
        ("employee_user", False, 405),
        ("client_a_user", False, 405),
        ("client_a_user", True, 200),
    ],
)
async def test_create_go_property_ga4_as_user(
    client_user: Any,
    assign_client: bool | None,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    a_client = await create_random_client(db_session)
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    data_in: dict[str, Any] = {
        "title": random_lower_string(),
        "property_id": random_lower_string(10),
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        assert all(item in entry.items() for item in data_in.items())
        assert entry["platform_id"] == str(a_platform.id)


@pytest.mark.parametrize(
    "title,property_id,status_code,error_type,error_msg",
    [
        (
            random_lower_string(5),
            random_lower_string(16),
            200,
            None,
            None,
        ),
        (
            random_lower_string(4),
            random_lower_string(16),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
        ),
        (
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            random_lower_string(16),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
        ),
        (
            random_lower_string(),
            "",
            422,
            "detail",
            "Value error, property_id is required",
        ),
        (
            random_lower_string(),
            random_lower_string(DB_STR_16BIT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, property_id must be {DB_STR_16BIT_MAXLEN_INPUT} characters or less",
        ),
    ],
)
async def test_create_go_property_ga4_as_superuser_limits(
    title: str,
    property_id: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    platform_type = GooglePlatformType.ga4.value
    a_client = await create_random_client(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    data_in: dict[str, Any] = {
        "title": title,
        "property_id": property_id,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert status_code == response.status_code
    if error_type == "message":
        assert error_msg in entry["detail"]
    if error_type == "detail":
        assert error_msg in entry["detail"][0]["msg"]
    if error_type is None:
        assert all(item in entry.items() for item in data_in.items())
        assert entry["platform_id"] == str(a_platform.id)


async def test_create_go_property_ga4_as_superuser_invalid_schema(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4.value
    a_client = await create_random_client(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    title = random_lower_string()
    property_id = random_lower_string(10)
    data_in: dict[str, Any] = {
        "title": title,
        "measurement_id": property_id,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert ERROR_MESSAGE_INPUT_SCHEMA_INVALID in entry["detail"]


async def test_create_go_property_ga4_as_superuser_title_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    platform_type = GooglePlatformType.ga4.value
    a_client = await create_random_client(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_client.id, a_platform.id
    )
    property_id = random_lower_string(10)
    data_in: dict[str, Any] = {
        "title": a_ga4_property.title,
        "property_id": property_id,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 400
    assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]


async def test_create_go_property_ga4_as_superuser_property_id_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    platform_type = GooglePlatformType.ga4.value
    a_client = await create_random_client(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_client.id, a_platform.id
    )
    title = random_lower_string()
    data_in: dict[str, Any] = {
        "title": title,
        "property_id": a_ga4_property.property_id,
        "client_id": str(a_client.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 400
    assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]


async def test_create_go_property_ga4_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    platform_type = GooglePlatformType.ga4.value
    a_client = await create_random_client(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    await create_random_ga4_property(db_session, a_client.id, a_platform.id)
    title = random_lower_string()
    property_id = random_lower_string(10)
    bad_client_id = get_uuid_str()
    data_in: dict[str, Any] = {
        "title": title,
        "property_id": property_id,
        "client_id": bad_client_id,
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_CLIENT_NOT_FOUND in entry["detail"]
