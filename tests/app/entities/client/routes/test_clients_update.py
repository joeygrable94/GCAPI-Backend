from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.constants import DB_STR_DESC_MAXLEN_INPUT, DB_STR_TINYTEXT_MAXLEN_INPUT
from app.entities.auth.constants import ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED
from app.entities.client.constants import ERROR_MESSAGE_CLIENT_EXISTS
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION,
)
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email
from tests.utils.utils import random_lower_string

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        pytest.param(
            "employee_user",
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
        pytest.param(
            "client_a_user",
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACTION
            ),
        ),
        pytest.param(
            "unverified_user",
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_update_client_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_client = await create_random_client(db_session)
    title: str = "New Client Title"
    data: dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{a_client.id}",
        headers=current_user.token_headers,
        json=data,
    )
    updated_entry: dict[str, Any] = response.json()
    assert 200 <= response.status_code < 300
    assert updated_entry["title"] == title
    assert updated_entry["id"] == str(a_client.id)
    assert updated_entry["description"] == a_client.description


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        ("employee_user"),
        ("client_a_user"),
        ("client_b_user"),
        pytest.param(
            "verified_user",
            marks=pytest.mark.xfail(reason=ERROR_MESSAGE_UNVERIFIED_ACCESS_DENIED),
        ),
    ],
)
async def test_update_assigned_client_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_client = await create_random_client(db_session)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    title: str = "New Client Title"
    data: dict[str, str] = {"title": title}
    response: Response = await client.patch(
        f"clients/{a_client.id}",
        headers=current_user.token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300
    updated_entry: dict[str, Any] = response.json()
    assert updated_entry["id"] == str(a_client.id)
    assert updated_entry["title"] == title
    assert updated_entry["description"] == a_client.description


@pytest.mark.parametrize(
    "title,description,error_msg",
    [
        (
            random_lower_string(4),
            None,
            "Value error, title must be 5 characters or more",
        ),
        (
            random_lower_string() * 100,
            None,
            "Value error, title must be {} characters or less".format(
                DB_STR_TINYTEXT_MAXLEN_INPUT
            ),
        ),
        (
            None,
            random_lower_string() * 160,
            "Value error, description must be {} characters or less".format(
                DB_STR_DESC_MAXLEN_INPUT
            ),
        ),
        (
            None,
            None,
            ERROR_MESSAGE_CLIENT_EXISTS,
        ),
    ],
)
async def test_update_client_as_superuser_client_limits(
    title: str | None,
    description: str | None,
    error_msg: str,
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_client = await create_random_client(db_session)
    data: dict[str, str]
    if title is not None:
        data = {"title": title}
    if description is not None:
        data = {"description": description}
    if title is None and description is None:
        data = {"title": a_client.title}
    response: Response = await client.patch(
        f"clients/{a_client.id}",
        headers=admin_user.token_headers,
        json=data,
    )
    if title is not None or description is not None:
        updated_entry: dict[str, Any] = response.json()
        assert response.status_code == 422
        assert updated_entry["detail"][0]["msg"] == error_msg
    else:
        assert response.status_code == 400
        updated_entry: dict[str, Any] = response.json()
        assert updated_entry["detail"] == error_msg
