from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from app.db.constants import DB_STR_TINYTEXT_MAXLEN_INPUT
from app.schemas.go import GooglePlatformType
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_user_to_client,
    assign_website_to_client,
    create_random_client,
)
from tests.utils.go_sc import create_random_go_search_console_property
from tests.utils.platform import get_platform_by_slug
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string
from tests.utils.websites import create_random_website

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,assign_client,assign_gsc,status_code",
    [
        ("admin_user", False, False, 200),
        ("manager_user", False, False, 200),
        ("employee_user", False, False, 405),
        ("client_a_user", False, False, 405),
        ("client_a_user", True, False, 200),
        ("client_a_user", True, True, 400),
    ],
)
async def test_create_go_property_gsc_as_user(
    client_user: Any,
    assign_client: bool,
    assign_gsc: bool,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.gsc.value)
    a_client = await create_random_client(db_session)
    b_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    b_website = await create_random_website(db_session)
    c_website = await create_random_website(db_session)
    await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id, a_platform.id
    )
    await create_random_go_search_console_property(
        db_session, b_client.id, a_website.id, a_platform.id
    )
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, b_client.id)
        await assign_website_to_client(db_session, a_website.id, a_website.id)
        await assign_website_to_client(db_session, a_website.id, b_client.id)
        await assign_website_to_client(db_session, b_website.id, b_client.id)
        await assign_website_to_client(db_session, c_website.id, b_client.id)
    data_in: dict[str, Any] = {
        "title": random_lower_string(),
        "client_id": str(b_client.id),
        "website_id": str(c_website.id),
    }
    if assign_gsc:
        data_in["client_id"] = str(b_client.id)
        data_in["website_id"] = str(a_website.id)
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
    "title,status_code,error_type,error_msg",
    [
        (
            random_lower_string(5),
            200,
            None,
            None,
        ),
        (
            random_lower_string(4),
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
        ),
        (
            random_lower_string(DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
        ),
    ],
)
async def test_create_go_property_gsc_as_superuser_limits(
    title: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_platform = await get_platform_by_slug(db_session, GooglePlatformType.gsc.value)
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, a_website.id)
    data_in: dict[str, Any] = {
        "title": title,
        "client_id": str(a_client.id),
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
        assert all(item in entry.items() for item in data_in.items())
        assert entry["platform_id"] == str(a_platform.id)


async def test_create_go_property_gsc_as_superuser_invalid_schema(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    title = random_lower_string()
    property_id = random_lower_string(10)
    data_in: dict[str, Any] = {
        "title": title,
        "property_id": property_id,
        "client_id": str(a_client.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 422
    assert ErrorCode.INPUT_SCHEMA_INVALID in entry["detail"]


async def test_create_go_property_gsc_as_superuser_title_exists(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_platform = await get_platform_by_slug(db_session, platform_type)
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, a_website.id)
    a_gsc = await create_random_go_search_console_property(
        db_session, a_client.id, a_website.id, a_platform.id
    )
    data_in: dict[str, Any] = {
        "title": a_gsc.title,
        "client_id": str(a_client.id),
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 400
    assert ErrorCode.ENTITY_EXISTS in entry["detail"]


async def test_create_go_property_gsc_as_superuser_client_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, a_website.id)
    title = random_lower_string()
    bad_client_id = get_uuid_str()
    data_in: dict[str, Any] = {
        "title": title,
        "client_id": bad_client_id,
        "website_id": str(a_website.id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.CLIENT_NOT_FOUND in entry["detail"]


async def test_create_go_property_gsc_as_superuser_website_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    platform_type = GooglePlatformType.gsc.value
    a_client = await create_random_client(db_session)
    a_website = await create_random_website(db_session)
    this_user = await get_user_by_email(db_session, admin_user.email)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    await assign_website_to_client(db_session, a_website.id, a_website.id)
    title = random_lower_string()
    bad_website_id = get_uuid_str()
    data_in: dict[str, Any] = {
        "title": title,
        "client_id": str(a_client.id),
        "website_id": str(bad_website_id),
    }
    response: Response = await client.post(
        f"go/{platform_type}",
        headers=admin_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert response.status_code == 404
    assert ErrorCode.ENTITY_NOT_FOUND in entry["detail"]
