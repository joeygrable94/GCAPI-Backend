from typing import Any

import pytest
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.errors import ErrorCode
from app.core.utilities.uuids import get_uuid_str
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.clients import assign_user_to_client, create_random_client
from tests.utils.users import create_random_user, get_user_by_email

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "client_user,status_code",
    [
        ("admin_user", 200),
        ("manager_user", 200),
        pytest.param(
            "employee_user",
            403,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_remove_random_user_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    user_client_rel = await assign_user_to_client(db_session, a_user.id, a_client.id)
    user_client_in = {"user_id": str(a_user.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=current_user.token_headers,
        json=user_client_in,
    )
    assert response.status_code == status_code
    data: dict[str, Any] = response.json()
    assert data["id"] is not None
    assert data["user_id"] == str(user_client_rel.user_id)
    assert data["client_id"] == str(user_client_rel.client_id)


@pytest.mark.parametrize(
    "client_user,status_code",
    [
        ("admin_user", 200),
        ("manager_user", 200),
        pytest.param(
            "employee_user",
            403,
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_remove_current_user_as_user(
    client_user: Any,
    status_code: int,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    this_user = await get_user_by_email(db_session, current_user.email)
    a_client = await create_random_client(db_session)
    user_client_rel = await assign_user_to_client(db_session, this_user.id, a_client.id)
    user_client_in = {"user_id": str(this_user.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=current_user.token_headers,
        json=user_client_in,
    )
    assert response.status_code == status_code
    data: dict[str, Any] = response.json()
    assert data["id"] is not None
    assert data["user_id"] == str(user_client_rel.user_id)
    assert data["client_id"] == str(user_client_rel.client_id)


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        pytest.param(
            "employee_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_remove_user_as_user_missmatching_client_id(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    await assign_user_to_client(db_session, a_user.id, a_client.id)
    a_client_bad_id = get_uuid_str()
    user_client_in = {"user_id": str(a_user.id), "client_id": a_client_bad_id}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=current_user.token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_NOT_FOUND


@pytest.mark.parametrize(
    "client_user",
    [
        ("admin_user"),
        ("manager_user"),
        pytest.param(
            "employee_user",
            marks=pytest.mark.xfail(reason=ErrorCode.INSUFFICIENT_PERMISSIONS_ACTION),
        ),
    ],
)
async def test_clients_remove_user_as_user_user_not_exists(
    client_user: Any,
    client: AsyncClient,
    db_session: AsyncSession,
    request: pytest.FixtureRequest,
) -> None:
    current_user: ClientAuthorizedUser = request.getfixturevalue(client_user)
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    await assign_user_to_client(db_session, a_user.id, a_client.id)
    a_client_bad_id = get_uuid_str()
    user_client_in = {"user_id": a_client_bad_id, "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=current_user.token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.USER_NOT_FOUND


async def test_clients_remove_user_as_superuser_relation_not_found(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_user: ClientAuthorizedUser,
) -> None:
    a_user = await create_random_user(db_session)
    a_client = await create_random_client(db_session)
    user_client_in = {"user_id": str(a_user.id), "client_id": str(a_client.id)}
    response: Response = await client.post(
        f"clients/{a_client.id}/remove/user",
        headers=admin_user.token_headers,
        json=user_client_in,
    )
    assert response.status_code == 404
    data: dict[str, Any] = response.json()
    assert data["detail"] == ErrorCode.CLIENT_RELATIONSHOP_NOT_FOUND
