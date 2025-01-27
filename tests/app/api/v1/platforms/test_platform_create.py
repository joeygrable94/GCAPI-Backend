from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ErrorCode
from app.db.constants import DB_STR_64BIT_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.platform import create_random_platform
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


DUPLICATE_PLATFORM_SLUG = random_lower_string()
DUPLICATE_PLATFORM_TITLE = random_lower_string()


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        pytest.param(
            "employee_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "client_a_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "verified_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "client_a_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "verified_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
        ),
        pytest.param(
            "unverified_user",
            marks=pytest.mark.xfail(reason=ErrorCode.UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_create_platform_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    data_in: dict[str, Any] = {
        "slug": random_lower_string(),
        "title": random_lower_string(),
    }
    response: Response = await client.post(
        "platforms/",
        headers=current_user.token_headers,
        json=data_in,
    )
    entry: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert all(item in entry.items() for item in data_in.items())


@pytest.mark.parametrize(
    "slug,title,status_code,error_type,error_msg",
    [
        (
            random_lower_string(),
            random_lower_string(),
            200,
            None,
            None,
        ),
        (
            "",
            random_lower_string(),
            422,
            "detail",
            "Value error, slug is required",
        ),
        (
            "aa",
            random_lower_string(),
            422,
            "detail",
            f"Value error, slug must be {3} characters or more",
        ),
        (
            "a" * (DB_STR_64BIT_MAXLEN_INPUT + 1),
            random_lower_string(),
            422,
            "detail",
            f"Value error, slug must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less",
        ),
        (
            random_lower_string(),
            "",
            422,
            "detail",
            "Value error, title is required",
        ),
        (
            random_lower_string(),
            "aa",
            422,
            "detail",
            f"Value error, title must be {5} characters or more",
        ),
        (
            random_lower_string(),
            "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
            422,
            "detail",
            f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
        ),
        (
            DUPLICATE_PLATFORM_SLUG,
            DUPLICATE_PLATFORM_TITLE,
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
        (
            DUPLICATE_PLATFORM_SLUG,
            random_lower_string(),
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
        (
            random_lower_string(),
            DUPLICATE_PLATFORM_TITLE,
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
    ],
)
async def test_create_platform_as_superuser_limits(
    slug: str,
    title: str,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    await create_random_platform(
        db_session, DUPLICATE_PLATFORM_SLUG, DUPLICATE_PLATFORM_TITLE
    )
    data_in: dict[str, Any] = {
        "slug": slug,
        "title": title,
    }
    response: Response = await client.post(
        "platforms/",
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
