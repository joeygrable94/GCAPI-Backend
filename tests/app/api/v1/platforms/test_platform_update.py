from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import (
    assign_platform_to_client,
    assign_user_to_client,
    create_random_client,
)
from tests.utils.platform import create_random_platform
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


DUPLICATE_PLATFORM_SLUG = random_lower_string()
DUPLICATE_PLATFORM_TITLE = random_lower_string()


# @pytest.mark.parametrize(
#     "client_user,assign_client",
#     [
#         ("admin_user", False),
#         ("manager_user", False),
#         pytest.param(
#             "employee_user",
#             False,
#             marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
#         ),
#         pytest.param(
#             "client_a_user",
#             False,
#             marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS),
#         ),
#         pytest.param(
#             "unverified_user",
#             False,
#             marks=pytest.mark.xfail(reason=ErrorCode.UNVERIFIED_ACCESS_DENIED),
#         ),
#     ],
#     # ids=[],  # TODO: Add ids
# )
# async def test_update_platform_as_user(
#     client_user: Any,
#     assign_client: bool,
#     client: AsyncClient,
#     db_session: AsyncSession,
#     request: pytest.FixtureRequest,
# ) -> None:
#     current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
#     a_client = await create_random_client(db_session)
#     a_platform = await create_random_platform(
#         db_session, DUPLICATE_PLATFORM_SLUG, DUPLICATE_PLATFORM_TITLE
#     )
#     await assign_platform_to_client(db_session, a_client.id, a_platform.id)
#     if assign_client:
#         this_user = await get_user_by_email(db_session, current_user.email)
#         await assign_user_to_client(db_session, this_user.id, a_client.id)
#     data_in: dict[str, Any] = {
#         "slug": random_lower_string(),
#         "title": random_lower_string(),
#     }
#     response: Response = await client.patch(
#         f"platforms/{a_platform.id}",
#         headers=current_user.token_headers,
#         json=data_in,
#     )
#     entry: dict[str, Any] = response.json()
#     assert 200 <= response.status_code < 300
#     assert all(item in entry.items() for item in data_in.items())


# @pytest.mark.parametrize(
#     "slug,title,status_code,error_type,error_msg",
#     [
#         (
#             random_lower_string(),
#             random_lower_string(),
#             200,
#             None,
#             None,
#         ),
#         (
#             "",
#             random_lower_string(),
#             422,
#             "detail",
#             "Value error, slug is required",
#         ),
#         (
#             "aa",
#             random_lower_string(),
#             422,
#             "detail",
#             f"Value error, slug must be {3} characters or more",
#         ),
#         (
#             "a" * (DB_STR_64BIT_MAXLEN_INPUT + 1),
#             random_lower_string(),
#             422,
#             "detail",
#             f"Value error, slug must be {DB_STR_64BIT_MAXLEN_INPUT} characters or less",
#         ),
#         (
#             random_lower_string(),
#             "",
#             422,
#             "detail",
#             "Value error, title is required",
#         ),
#         (
#             random_lower_string(),
#             "aa",
#             422,
#             "detail",
#             f"Value error, title must be {5} characters or more",
#         ),
#         (
#             random_lower_string(),
#             "a" * (DB_STR_TINYTEXT_MAXLEN_INPUT + 1),
#             422,
#             "detail",
#             f"Value error, title must be {DB_STR_TINYTEXT_MAXLEN_INPUT} characters or less",
#         ),
#         (
#             DUPLICATE_PLATFORM_SLUG,
#             DUPLICATE_PLATFORM_TITLE,
#             400,
#             "message",
#             ErrorCode.ENTITY_EXISTS,
#         ),
#         (
#             DUPLICATE_PLATFORM_SLUG,
#             random_lower_string(),
#             400,
#             "message",
#             ErrorCode.ENTITY_EXISTS,
#         ),
#         (
#             random_lower_string(),
#             DUPLICATE_PLATFORM_TITLE,
#             400,
#             "message",
#             ErrorCode.ENTITY_EXISTS,
#         ),
#     ],
#     # ids=[],  # TODO: Add ids
# )
# async def test_update_platform_as_superuser_limits(
#     slug: str,
#     title: str,
#     status_code: int,
#     error_type: str | None,
#     error_msg: str | None,
#     client: AsyncClient,
#     db_session: AsyncSession,
#     admin_user: ClientAuthorizedUser,
# ) -> None:
#     a_client = await create_random_client(db_session)
#     a_platform = await create_random_platform(
#         db_session, DUPLICATE_PLATFORM_SLUG, DUPLICATE_PLATFORM_TITLE
#     )
#     await assign_platform_to_client(db_session, a_client.id, a_platform.id)
#     data_in: dict[str, Any] = {
#         "slug": slug,
#         "title": title,
#     }
#     print(data_in)
#     response: Response = await client.patch(
#         f"platforms/{a_platform.id}",
#         headers=admin_user.token_headers,
#         json=data_in,
#     )
#     entry: dict[str, Any] = response.json()
#     print(entry)
#     assert status_code == response.status_code
#     if error_type == "message":
#         assert error_msg in entry["detail"]
#     if error_type == "detail":
#         assert error_msg in entry["detail"][0]["msg"]
#     if error_type is None:
#         assert all(item in entry.items() for item in data_in.items())


@pytest.mark.parametrize(
    "client_user,assign_client,title,desc,status_code,error_type,error_msg",
    [
        (
            "admin_user",
            True,
            None,
            random_lower_string(),
            200,
            None,
            None,
        ),
        (
            "manager_user",
            True,
            None,
            random_lower_string(),
            200,
            None,
            None,
        ),
        (
            "manager_user",
            True,
            random_lower_string(),
            random_lower_string(),
            200,
            None,
            None,
        ),
        (
            "client_a_user",
            True,
            random_lower_string(),
            random_lower_string(),
            405,
            "message",
            ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION,
        ),
        (
            "client_a_user",
            False,
            None,
            random_lower_string(),
            405,
            "message",
            ErrorCode.INSUFFICIENT_PERMISSIONS_ACCESS,
        ),
        (
            "manager_user",
            True,
            DUPLICATE_PLATFORM_TITLE,
            None,
            400,
            "message",
            ErrorCode.ENTITY_EXISTS,
        ),
    ],
    ids=[
        "admin user assigned to client with platform update description",
        "manager user assigned to client with platform update description",
        "manager user assigned to client with platform update description and title",
        "client_a user assigned to client with platform update title action not allowed",
        "client_a user not assigned to client not allowed to access platform update",
        "manager user assigned to client with platform update title already exists",
    ],
)
async def test_update_platform_as_user_field_restrictions(
    client_user: Any,
    assign_client: bool,
    title: str | None,
    desc: str | None,
    status_code: int,
    error_type: str | None,
    error_msg: str | None,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client = await create_random_client(db_session)
    a_platform = await create_random_platform(
        db_session, DUPLICATE_PLATFORM_SLUG, DUPLICATE_PLATFORM_TITLE
    )
    await assign_platform_to_client(db_session, a_client.id, a_platform.id)
    if assign_client:
        this_user = await get_user_by_email(db_session, current_user.email)
        await assign_user_to_client(db_session, this_user.id, a_client.id)
    data_in: dict[str, Any] = {}
    if title is not None:
        data_in["title"] = title
    if desc is not None:
        data_in["description"] = desc
    response: Response = await client.patch(
        f"platforms/{a_platform.id}",
        headers=current_user.token_headers,
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
