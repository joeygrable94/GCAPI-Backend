from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.client.constants import ERROR_MESSAGE_CLIENT_NOT_FOUND
from app.services.permission.constants import (
    ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS,
)
from app.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        pytest.param(
            "manager_user",
            marks=pytest.mark.xfail(
                reason=ERROR_MESSAGE_INSUFFICIENT_PERMISSIONS_ACCESS
            ),
        ),
    ],
)
async def test_delete_client_by_id_as_user(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    entry = await create_random_client(db_session)
    response: Response = await client.delete(
        f"clients/{entry.id}",
        headers=current_user.token_headers,
    )
    assert 200 <= response.status_code < 300
    response: Response = await client.get(
        f"clients/{entry.id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ERROR_MESSAGE_CLIENT_NOT_FOUND


@pytest.mark.parametrize(
    "client_user",
    [
        ("client_a_user"),
        ("client_b_user"),
    ],
)
async def test_delete_assigned_client_by_id(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_client = await create_random_client(db_session)
    await assign_user_to_client(db_session, this_user.id, a_client.id)
    response: Response = await client.delete(
        f"clients/{a_client.id}",
        headers=current_user.token_headers,
    )
    assert 200 <= response.status_code < 300
    data: dict[str, Any] = response.json()
    assert data["message"] == "Client requested to be deleted"
    assert data["user_id"] == str(this_user.id)
    assert data["client_id"] == str(a_client.id)


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
    ],
)
async def test_delete_client_by_id_not_found(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    bad_client_id = get_uuid_str()
    response: Response = await client.delete(
        f"clients/{bad_client_id}",
        headers=current_user.token_headers,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert ERROR_MESSAGE_CLIENT_NOT_FOUND in data["detail"]
