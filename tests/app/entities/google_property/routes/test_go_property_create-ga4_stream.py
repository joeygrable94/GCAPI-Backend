from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.api.constants import (
    ERROR_MESSAGE_ENTITY_EXISTS,
    ERROR_MESSAGE_ENTITY_NOT_FOUND,
    ERROR_MESSAGE_INPUT_SCHEMA_INVALID,
)
from app.entities.go_property.schemas import GooglePlatformType
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.ga4 import create_random_ga4_property, create_random_ga4_stream
from tests.utils.organizations import (
    assign_user_to_organization,
    assign_website_to_organization,
    create_random_organization,
)
from tests.utils.platform import get_platform_by_slug
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_organization,assign_website,status_code",
    [
        ("admin_user", False, False, 200),
        ("manager_user", False, False, 200),
        ("employee_user", False, False, 405),
        ("client_a_user", False, False, 405),
        ("client_a_user", True, False, 200),
        ("client_a_user", True, True, 405),
    ],
)
async def test_create_go_property_ga4_stream_as_user(
    client_user: Any,
    assign_organization: bool,
    assign_website: bool,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    a_organization = await create_random_organization(db_session)
    b_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_organization.id, a_platform.id
    )
    if assign_organization:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_organization(db_session, this_user.id, a_organization.id)
        await assign_user_to_organization(db_session, this_user.id, b_organization.id)
        await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    data_in: dict[str, Any] = {
        "title": random_lower_string(),
        "stream_id": random_lower_string(10),
        "measurement_id": random_lower_string(10),
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    if assign_website:
        data_in["organization_id"] = str(b_organization.id)
        data_in["website_id"] = str(b_website.id)
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == status_code
    if status_code == 200:
        del data_in["organization_id"]
        assert all(item in entry.items() for item in data_in.items())
        # assert entry["platform_id"] == str(a_platform.id)


@pytest.mark.parametrize(
    "title,stream_id,measurement_id,status_code,error_type,error_msg",
    [
        (
            random_lower_string(5),
            random_lower_string(10),
            random_lower_string(10),
            200,
            None,
            None,
        ),
        (
            random_lower_string(4),
            random_lower_string(10),
            random_lower_string(10),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
        ),
        (
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            random_lower_string(10),
            random_lower_string(10),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
        ),
    ],
)
async def test_create_go_property_ga4_stream_as_superuser_limits(
    title: str,
    stream_id: str,
    measurement_id: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_organization.id, a_platform.id
    )
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_organization(db_session, this_user.id, a_organization.id)
    await assign_website_to_organization(db_session, a_website.id, a_organization.id)
    data_in: dict[str, Any] = {
        "title": title,
        "stream_id": stream_id,
        "measurement_id": measurement_id,
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
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
        del data_in["organization_id"]
        assert all(item in entry.items() for item in data_in.items())
        # assert entry["platform_id"] == str(a_platform.id)


async def test_create_go_property_ga4_stream_as_superuser_invalid_schema(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_organization.id, a_platform.id
    )
    title = random_lower_string()
    stream_id = random_lower_string()
    measurement_id = random_lower_string()
    data_in: dict[str, Any] = {
        "title": title,
        "stream_id": stream_id,
        "property_id": measurement_id,
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert ERROR_MESSAGE_INPUT_SCHEMA_INVALID in entry["detail"]


async def test_create_go_property_ga4_stream_as_superuser_title_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_organization.id, a_platform.id
    )
    a_ga4_stream = await create_random_ga4_stream(
        db_session, a_ga4_property.id, a_website.id
    )
    stream_id = random_lower_string(10)
    measurement_id = random_lower_string(10)
    data_in: dict[str, Any] = {
        "title": a_ga4_stream.title,
        "stream_id": stream_id,
        "measurement_id": measurement_id,
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 400
    assert ERROR_MESSAGE_ENTITY_EXISTS in entry["detail"]
    assert "GoAnalytics4Stream" in entry["detail"]


async def test_create_go_property_ga4_stream_as_superuser_website_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.ga4.value)
    a_organization = await create_random_organization(db_session)
    a_ga4_property = await create_random_ga4_property(
        db_session, a_organization.id, a_platform.id
    )
    title = random_lower_string(10)
    stream_id = random_lower_string(10)
    measurement_id = random_lower_string(10)
    bad_website_id = get_uuid_str()
    data_in: dict[str, Any] = {
        "title": title,
        "stream_id": stream_id,
        "measurement_id": measurement_id,
        "ga4_id": str(a_ga4_property.id),
        "organization_id": str(a_organization.id),
        "website_id": bad_website_id,
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]


async def test_create_go_property_ga4_stream_as_superuser_ga4_property_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.ga4_stream.value
    a_organization = await create_random_organization(db_session)
    a_website = await create_random_website(db_session)
    title = random_lower_string(10)
    stream_id = random_lower_string(10)
    measurement_id = random_lower_string(10)
    bad_ga4_id = get_uuid_str()
    data_in: dict[str, Any] = {
        "title": title,
        "stream_id": stream_id,
        "measurement_id": measurement_id,
        "ga4_id": bad_ga4_id,
        "organization_id": str(a_organization.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ERROR_MESSAGE_ENTITY_NOT_FOUND in entry["detail"]
